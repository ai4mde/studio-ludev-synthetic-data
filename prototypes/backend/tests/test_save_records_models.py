import sys
import os
import django
import json
from django.apps import apps
from django.db import transaction
from django.db.models import ForeignKey, OneToOneField
GENERATION_PATH = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "generation", "generation_scripts")
    )

sys.path.append(GENERATION_PATH)

from generate_synthetic_data import setup_django, save_records, extract_model_definitions, toposort_models

PROTOTYPE_NAME = sys.argv[1]
SYSTEM = sys.argv[2]

setup_django(SYSTEM, PROTOTYPE_NAME)

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

total_json = json.loads(llm_response[llm_response.find('{'):llm_response.rfind('}')+1])
print(f"Extracted JSON: {json.dumps(total_json, indent=2)}")

name_to_id_to_id_mapping_mapping = {}

print(insert_order)
for model_name in insert_order:
    model_class = next((m for m in models if m.__name__ == model_name), None)
    print(f"Processing model: {model_name}")
    if not model_class:
        continue
  
    
    id_to_id_mapping = save_records(model_class, total_json[model_name], model_name, name_to_id_to_id_mapping_mapping)
    print(f"ID to ID mapping for {model_name}: {id_to_id_mapping}")
    # This one should exit with 0

    # # Need tests for non-0 exits

    # # The 2 lines below could technically be removed, as they're not explicitly tested
    name_to_id_to_id_mapping_mapping[model_name] = id_to_id_mapping
    print(f"Name to ID mapping for {model_name}: {name_to_id_to_id_mapping_mapping[model_name]}")

exit(0)