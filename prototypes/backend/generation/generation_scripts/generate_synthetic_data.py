import os
import sys
import json
import django
from django.apps import apps
from django.db.models import ForeignKey, OneToOneField
from groq import Groq
from graphlib import TopologicalSorter


def call_groq(prompt: str, model: str = "llama-3.3-70b-versatile") -> str:
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model,
        )
        response = chat_completion.choices[0].message.content
        if response is not None:
            return response
        else:
            raise Exception("LLM returned None")
    except Exception as e:
        raise Exception("Failed to call LLM, error " + str(e))


def setup_django(system_name, prototype_name):
    PROJECT_ROOT = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../..", "generated_prototypes", system_name, prototype_name)
    )
    sys.path.append(PROJECT_ROOT)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{prototype_name}.settings")
    django.setup()


def extract_model_definitions(models, hidden_models):
    model_definitions = []
    for model in models:
        if model.__name__ not in hidden_models:
            fields_info = []
            for field in model._meta.fields:
                field_info = {
                    "name": field.name,
                    "type": field.__class__.__name__,
                    "choices": field.choices if hasattr(field, "choices") and field.choices else None
                }
                fields_info.append(field_info)
            model_def = {
                "model_name": model.__name__,
                "fields": fields_info
            }
            model_definitions.append(model_def)
    return model_definitions


def toposort_models(models, hidden_models):
    ts = TopologicalSorter()
    for model in models:
        if model.__name__ in hidden_models:
            continue
        key_constraints = []
        for field in model._meta.fields:
            if isinstance(field, ForeignKey) or isinstance(field, OneToOneField):
                key_constraints.append(field.name)
        ts.add(model.__name__, *key_constraints)
    return [*ts.static_order()]


def make_prompt(model_definitions, synthetic_instructions, synthetic_counts, synthetic_instructions_per_node):
    prompt = f"""
    You are going to generate synthetic sample data for a database based on Django model definitions.
    1) Make sure values match the expected type for each field. 
    2) Make sure that the data are plausible real world values.
    3) You are going to return one json object, within this json object each model name is associated with an array of instances.
    4) Return only one unified json object made from the model arrays please, NO OTHER TEXT THAN JSON.
    """
    if synthetic_instructions.strip():
        prompt += f"5) Apply the following global instructions for each model when applicable: {synthetic_instructions.strip()}\n"

    for model_def in model_definitions:
        if not isinstance(model_def, dict):
            raise ValueError("At least one model definition is not a dictionary")
        if not isinstance(model_def.get("model_name"), str):
            raise ValueError
        fields = model_def.get("fields")
        if not isinstance(fields, list):
            raise ValueError
        required_keys = {"name", "type", "choices"}
        for field in fields:
            if field.keys() != required_keys:
                raise ValueError

        model_name = model_def["model_name"]
        per_node_instructions = synthetic_instructions_per_node.get(model_name, "").strip()
        if per_node_instructions:
            print(f"Using custom instruction: {per_node_instructions}")
        single_model_def = {
            "model_name": model_def["model_name"],
            "fields": model_def["fields"],
        }
        formatted_model_def = json.dumps(single_model_def, indent=2)

        num_records = synthetic_counts.get(model_name, 10)
        prompt += f"\nGenerate {num_records} synthetic records based on the following model definition:\n{formatted_model_def}\n"
        if per_node_instructions:
            prompt += f"With these additional instructions for model {model_name}: {per_node_instructions}\n"

    return prompt


def save_records(model_class, synthetic_data, model_name, name_to_id_to_id_mapping_mapping):
    llm_id_to_auto_id = {}  # Dictionary that keeps track of which "id" that the LLM generated maps to which actual primarykey (autofield)
    for record in synthetic_data:
        instance = model_class()
        for field_name, field_value in record.items():
            if field_name == "id" or field_name is None:
                continue
            try:
                field = model_class._meta.get_field(field_name)
                if isinstance(field, (ForeignKey, OneToOneField)):
                    related_model = field.remote_field.model
                    related_instance = related_model.objects.get(id=name_to_id_to_id_mapping_mapping[field_name][str(field_value)])
                    setattr(instance, field_name, related_instance)
                else:
                    setattr(instance, field_name, field_value)
            except Exception as e:
                print(f"Failed to set field {field_name} with value {field_value}: {e}")
        try:
            instance.save()
            print(f"Saved record for {model_name}")
            llm_id_to_auto_id[f'{record["id"]}'] = instance.id
        except Exception as e:
            print(f"Failed to save record for {model_name}: {e}")
    return llm_id_to_auto_id


def main():
    prototype_name = sys.argv[1]
    system_name = sys.argv[2]
    synthetic_instructions = sys.argv[3] if len(sys.argv) > 3 else ""
    synthetic_counts = json.loads(sys.argv[4]) if len(sys.argv) > 4 else {}
    synthetic_instructions_per_node = json.loads(sys.argv[5]) if len(sys.argv) > 5 else {}

    setup_django(system_name, prototype_name)
    hidden_models = ["LogEntry", "Permission", "Group", "User", "ContentType", "Session"]
    models = apps.get_models()
    model_definitions = extract_model_definitions(models, hidden_models)
    insert_order = toposort_models(models, hidden_models)
    prompt = make_prompt(
        model_definitions, synthetic_instructions, synthetic_counts, synthetic_instructions_per_node
    )

    generated_data = None
    try:
        llm_response = call_groq(prompt)
        try:
            generated_data = json.loads(llm_response[llm_response.find('{'):llm_response.rfind('}')+1])
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON from LLM response: {e}")
            print(f"Raw response: {llm_response}")
    except Exception as e:
        print(f"Error generating synthetic data: {e}")

    if generated_data is None:
        return

    name_to_id_to_id_mapping_mapping = {}
    for model_name in insert_order:
        model_class = next((m for m in models if m.__name__ == model_name), None)
        if not model_class:
            continue
        id_to_id_mapping = save_records(model_class, generated_data[model_name], model_name, name_to_id_to_id_mapping_mapping)
        name_to_id_to_id_mapping_mapping[model_name] = id_to_id_mapping


if __name__ == "__main__":
    main()
