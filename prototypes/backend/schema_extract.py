import os
import sys
import re
import json
import django
from django.apps import apps
from django.db.models import ForeignKey, OneToOneField
import requests
from graphlib import TopologicalSorter
from openai import OpenAI
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
    
def call_openai(prompt: str, model: str = 'gpt-4o-mini') -> str:
    client = OpenAI(
        api_key="",
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
         return chat_completion.choices[0].message.content
    except Exception as e:
         raise Exception("Failed to call LLM, error " + str(e))


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


def make_synthetic_data_prompt(model_definitions, N_RECORDS):
    prompt = f"""

    You are going to generate synthetic sample data for a database based on Django model definitions.
    1) Make sure values match the expected type for each field. 
    2) Make sure that the data are plausible real world values.
    3) You are going to return one json object, within this json object each model name is associated with an array of instances.
    4) Return only one unified json object made from the model arrays please, NO OTHER TEXT THAN JSON.

    """

    for model_def in model_definitions:
        model_name = model_def["model_name"]
        
        print(f"\nGenerating data for model: {model_name}")

        single_model_def = {
            "model_name": model_def["model_name"],
            "fields": model_def["fields"],
        }
        formatted_model_def = json.dumps(single_model_def, indent=2)

        prompt = prompt + f"  Generate {N_RECORDS} synthetic records based on this model definition. {formatted_model_def}   "
        
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
                # print("insterting: ", field_name, " into field:", model_name)
                # print(field)
                # print(f"Field class: {field.__class__.__name__}")
                # if isinstance(field, (ForeignKey, OneToOneField)):
                #     print(f"Field {field_name} is recognized as ForeignKey or OneToOneField")
                #     related_model = field.remote_field.model
                #     print(related_model)
                #     related_instance = related_model.objects.get(id=1)
                #     print(related_instance)
                # else:
                #     print(f"Field {field_name} is not ForeignKey or OneToOneField")
                if isinstance(field, (ForeignKey, OneToOneField)):
                    related_model = field.remote_field.model
                    # print("RECOG!:", related_model)
                    # print(" I think the id the foreign key should be: ", name_to_id_to_id_mapping_mapping[field_name][str(field_value)])
                    related_instance = related_model.objects.get(id=name_to_id_to_id_mapping_mapping[field_name][str(field_value)])
                    # print(name_to_id_to_id_mapping_mapping[field_name])
                    # print(name_to_id_to_id_mapping_mapping[field_name][str(field_value)])
                    # print(related_instance)
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

def main(PROTOTYPE_NAME, SYSTEM, N_RECORDS):
    setup_django(PROTOTYPE_NAME, SYSTEM)

    hidden_models = ["LogEntry", "Permission", "Group", "User", "ContentType", "Session"]
    models = apps.get_models()
    model_definitions = extract_model_definitions(models, hidden_models)

    insert_order = toposort_models(models,hidden_models)

    SYN_DATA_PROMPT = make_synthetic_data_prompt(model_definitions, N_RECORDS)
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
            print(f"Model {model_name} not found in models")
            continue

        print("for this im gonna use the following name to id id map map:", name_to_id_to_id_mapping_mapping)
        id_to_id_mapping = save_records(model_class, total_json[model_name], model_name, name_to_id_to_id_mapping_mapping)
        name_to_id_to_id_mapping_mapping[model_name] = id_to_id_mapping
        print(model_name, "Map", id_to_id_mapping)





    # for synthetic_data_array in total_json:
    #     print(synthetic_data_array)
        # for m in models:
        #     if m.__name__ == synthetic_data_array[0]:
        #         # save_records(m,synthetic_data_array[1],m.__name__)
        #         print(m.__name__, synthetic_data_array[1])


        # try:
        #     synthetic_data = extract_json_from_response(llm_response)
        #     print(f"Successfully parsed {len(synthetic_data)} records for {model_name}")
        #     save_records(model_class, synthetic_data, model_name)
        # except json.JSONDecodeError as e:
        #     print(f"Failed to parse JSON from LLM response: {e}")
        #     print(f"Raw response: {llm_response}")
        # except Exception as e:
        #     print(f"Error generating synthetic data for {model_name}: {e}")

if __name__ == "__main__":
    PROTOTYPE_NAME = sys.argv[1]
    SYSTEM = sys.argv[2]
    N_RECORDS = 50

    main(PROTOTYPE_NAME, SYSTEM, N_RECORDS)
