import os
import sys
import re
import json
import django
from django.apps import apps
import requests
##############################################

# PLEASE PUT YOUR OPENAI API KEY IN THE CALL_OPENAI FUNCTION BELOW

##############################################

def call_groq(prompt: str, model: str = 'llama3-70b-8192') -> str:
    api_key = "PUT API KEY HERE"    
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

def make_synthetic_data_prompt(model_def, N_RECORDS):
    single_model_def = {
        "model_name": model_def["model_name"],
        "fields": model_def["fields"],
    }
    formatted_model_def = json.dumps(single_model_def, indent=2)

    SYN_DATA_PROMPT = f"""
    Generate {N_RECORDS} synthetic records based on this model definition. 
    Return the data as a valid JSON array of objects, where each object represents a record with field names as keys.
    Do not include the id field if it's an AutoField.
    Make sure values match the expected type for each field.

    {formatted_model_def}
    """
    return SYN_DATA_PROMPT

def extract_json_from_response(llm_response):
    json_start = llm_response.find('[')
    json_end = llm_response.rfind(']') + 1
    json_string = llm_response[json_start:json_end]
    return json.loads(json_string)

def save_records(model_class, synthetic_data, model_name):
    for record in synthetic_data:
        instance = model_class()
        for field_name, field_value in record.items():
            if field_name == "id" or field_name is None:
                continue
            try:
                setattr(instance, field_name, field_value)
            except Exception as e:
                print(f"Failed to set field {field_name} with value {field_value}: {e}")
        try:
            instance.save()
            print(f"Saved record for {model_name}")
        except Exception as e:
            print(f"Failed to save record for {model_name}: {e}")

def main(PROTOTYPE_NAME, SYSTEM, N_RECORDS):
    setup_django(PROTOTYPE_NAME, SYSTEM)

    hidden_models = ["LogEntry", "Permission", "Group", "User", "ContentType", "Session"]
    models = apps.get_models()
    model_definitions = extract_model_definitions(models, hidden_models)

    for model_def in model_definitions:
        model_name = model_def["model_name"]
        print(f"\nGenerating data for model: {model_name}")

        model_class = next((m for m in models if m.__name__ == model_name), None)
        if not model_class:
            print(f"Model {model_name} not found in models")
            continue

        SYN_DATA_PROMPT = make_synthetic_data_prompt(model_def, N_RECORDS)
        print(SYN_DATA_PROMPT)

        print(f"Calling LLM to generate data for {model_name}...")
        try:
            llm_response = call_groq(SYN_DATA_PROMPT)
            try:
                synthetic_data = extract_json_from_response(llm_response)
                print(f"Successfully parsed {len(synthetic_data)} records for {model_name}")
                save_records(model_class, synthetic_data, model_name)
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON from LLM response: {e}")
                print(f"Raw response: {llm_response}")
        except Exception as e:
            print(f"Error generating synthetic data for {model_name}: {e}")

if __name__ == "__main__":
    PROTOTYPE_NAME = sys.argv[1]
    SYSTEM = sys.argv[2]
    N_RECORDS = 2

    main(PROTOTYPE_NAME, SYSTEM, N_RECORDS)
