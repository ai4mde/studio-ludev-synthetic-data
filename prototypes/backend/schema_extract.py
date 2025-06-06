import os
import sys
import re
import json
import django
from django.apps import apps
from django.db.models import ForeignKey, OneToOneField
import requests
from graphlib import TopologicalSorter
##############################################

# PLEASE PUT YOUR GROQ API KEY IN THE call_groq FUNCTION BELOW

##############################################

def call_groq(prompt: str, model: str = 'llama-3.3-70b-versatile') -> str:
    api_key = ""    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        raise Exception("Failed to call Groq LLM: " + str(e))

def setup_django(PROTOTYPE_NAME, SYSTEM):
    print("my name is:", PROTOTYPE_NAME)
    print("part of system:", SYSTEM)

    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'generated_prototypes', SYSTEM, PROTOTYPE_NAME))
    sys.path.append(PROJECT_ROOT)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{PROTOTYPE_NAME}.settings")
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
                    "choices": field.choices if hasattr(field, 'choices') and field.choices else None
                }
                fields_info.append(field_info)
            model_def = {
                "model_name": model.__name__,
                "fields": fields_info
            }
            model_definitions.append(model_def)
    return model_definitions


#Returns a list of models topologically sorted based on key constraints
#The model that has no dependencies will appear first in the list
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


def make_synthetic_data_prompt(model_definitions, syntheticInstructions, syntheticCounts, syntheticInstructionsPerNode):
    prompt = f"""

    You are going to generate synthetic sample data for a database based on Django model definitions.
    1) Make sure values match the expected type for each field. 
    2) Make sure that the data are plausible real world values.
    3) You are going to return one json object, within this json object each model name is associated with an array of instances.
    4) Return only one unified json object made from the model arrays please, NO OTHER TEXT THAN JSON.
    """
    if syntheticInstructions.strip():
        prompt += f"5) Apply the following global instructions for each model when applicable:\n{syntheticInstructions.strip()}\n"

    for model_def in model_definitions:
        model_name = model_def["model_name"]

        num_records = syntheticCounts.get(model_name, 10)  #fallback to 10
        table_instruction = syntheticInstructionsPerNode.get(model_name, "").strip() #fallback to empty
        
        print(f"\nGenerating data for model: {model_name} ({num_records} records)")
        if table_instruction:
            print(f"Using custom instruction: {table_instruction}")

        single_model_def = {
            "model_name": model_def["model_name"],
            "fields": model_def["fields"],
        }
        formatted_model_def = json.dumps(single_model_def, indent=2)

        prompt += f"\nGenerate {num_records} synthetic records based on the following model definition:\n{formatted_model_def}\n"

        if table_instruction:
            prompt += f"With these additional instructions for model {model_name}: {table_instruction}\n"
    
    print("prompt to llm: " , prompt)
    return prompt

def extract_json_from_response(llm_response):
    json_start = llm_response.find('{')
    json_end = llm_response.rfind('}') + 1
    json_string = llm_response[json_start:json_end]
    return json.loads(json_string)

def save_records(model_class, synthetic_data, model_name, name_to_id_to_id_mapping_mapping):

    #This is a dictionary that keeps track of which "id" that the LLM generated
    #maps to which actual primarykey (autofield)
    llm_id_to_auto_id = {}

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

def main(PROTOTYPE_NAME, SYSTEM, syntheticInstructions, syntheticCounts, syntheticInstructionsPerNode):
    setup_django(PROTOTYPE_NAME, SYSTEM)

    hidden_models = ["LogEntry", "Permission", "Group", "User", "ContentType", "Session"]
    models = apps.get_models()
    model_definitions = extract_model_definitions(models, hidden_models)

    insert_order = toposort_models(models,hidden_models)

    SYN_DATA_PROMPT = make_synthetic_data_prompt(model_definitions, syntheticInstructions, syntheticCounts, syntheticInstructionsPerNode)
    # print(SYN_DATA_PROMPT)
    
    total_json = None

    try:
        llm_response = call_groq(SYN_DATA_PROMPT)
        print(llm_response)
        try: 
            total_json = extract_json_from_response(llm_response)
        except json.JSONDecodeError as e:
                    print(f"Failed to parse JSON from LLM response: {e}")
                    print(f"Raw response: {llm_response}")
    except Exception as e:
            print(f"Error generating synthetic data: {e}")

    if total_json is None:
        return 

    name_to_id_to_id_mapping_mapping = {}

    for model_name in insert_order:
        model_class = next((m for m in models if m.__name__ == model_name), None)
        if not model_class:
            continue

        id_to_id_mapping = save_records(model_class, total_json[model_name], model_name, name_to_id_to_id_mapping_mapping)
        name_to_id_to_id_mapping_mapping[model_name] = id_to_id_mapping

if __name__ == "__main__":
    PROTOTYPE_NAME = sys.argv[1]
    SYSTEM = sys.argv[2]
    syntheticInstructions = sys.argv[3] if len(sys.argv) > 3 else ""
    syntheticCounts = json.loads(sys.argv[4]) if len(sys.argv) > 4 else {}
    syntheticInstructionsPerNode = json.loads(sys.argv[5]) if len(sys.argv) > 5 else {}

    #print("schema_extract.py global instruciton: " , syntheticInstructions)
    print("schema_extract.py count: " , syntheticCounts)
    print("schema_extract.py cusotm instruciton: ", syntheticInstructionsPerNode)
    main(PROTOTYPE_NAME, SYSTEM, syntheticInstructions, syntheticCounts, syntheticInstructionsPerNode)



