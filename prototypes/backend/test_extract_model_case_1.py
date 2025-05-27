from schema_extract import setup_django
from schema_extract import extract_model_definitions
import sys
import django
from django.apps import apps
from django.db.models import ForeignKey, OneToOneField

PROTOTYPE_NAME = sys.argv[1]
SYSTEM = sys.argv[2]

print("Prototypename: ",PROTOTYPE_NAME)

setup_django(PROTOTYPE_NAME, SYSTEM)

hidden_models = ["LogEntry", "Permission", "Group", "User", "ContentType", "Session"]

model_definition = extract_model_definitions(apps.get_models(), hidden_models)

if len(model_definition) != 1:
    exit(1)

if not isinstance(model_definition[0], dict):
    exit(2)

if not "model_name" in model_definition[0]:
    exit(3)

if not "fields" in model_definition[0]:
    exit(4)

if len(model_definition[0].get("fields")) != 6:
    exit(5)

exit(0)



