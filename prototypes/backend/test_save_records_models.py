import sys
import os
import django
import json
from django.apps import apps
from django.db import transaction
from django.db.models import ForeignKey, OneToOneField
from schema_extract import setup_django, save_records, \
    extract_model_definitions, toposort_models, extract_json_from_response
from django.core.management import call_command

def save_records_test(model_class, synthetic_data, model_name, name_to_id_to_id_mapping_mapping):

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

PROTOTYPE_NAME = sys.argv[1]
SYSTEM = sys.argv[2]

setup_django(PROTOTYPE_NAME, SYSTEM)

hidden_models = ["LogEntry", "Permission", "Group", "User", "ContentType", "Session"]
models = apps.get_models()
print(f"Models found: {[model.__name__ for model in models]}")
model_definitions = extract_model_definitions(models, hidden_models)
print(f"Model definitions extracted: {model_definitions}")
insert_order = toposort_models(models,hidden_models)
print(f"Models sorted in topological order: {insert_order}")

llm_response = """
{
  "Person": [
    {
      "id": 1,
      "name": "James Porter",
      "adress": "123 Baker Street, London",
      "House": true,
      "Car": 1
    }
  ],
  "Car": [
    {
      "id": 1,
      "brand": "Toyota",
      "licence": 8745932,
      "manual": false,
      "automatic": true
    }
  ],
  "Manufacturer": [
    {
      "id": 1,
      "CompanyName": "Toyota Motor Corporation",
      "kvk": 32145678,
      "international": true,
      "Car": 1
    }
  ]
}
"""

total_json = extract_json_from_response(llm_response)
print(f"Extracted JSON: {json.dumps(total_json, indent=2)}")

name_to_id_to_id_mapping_mapping = {}

for model_name in insert_order:
    model_class = next((m for m in models if m.__name__ == model_name), None)
    print(f"Processing model: {model_name}")
    if not model_class:
        continue
    
    id_to_id_mapping = save_records_test(model_class, total_json[model_name], model_name, name_to_id_to_id_mapping_mapping)
    print(f"ID to ID mapping for {model_name}: {id_to_id_mapping}")
    # This one should exit with 0

    # Need tests for non-0 exits

    # The 2 lines below could technically be removed, as they're not explicitly tested
    name_to_id_to_id_mapping_mapping[model_name] = id_to_id_mapping
    print(f"Name to ID mapping for {model_name}: {name_to_id_to_id_mapping_mapping[model_name]}")

exit(0)