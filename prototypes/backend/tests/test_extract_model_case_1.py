import sys
import os
import django
from django.apps import apps
from django.db.models import ForeignKey, OneToOneField

GENERATION_PATH = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "generation", "generation_scripts")
    )

sys.path.append(GENERATION_PATH)

from generate_synthetic_data import setup_django
from generate_synthetic_data import extract_model_definitions

PROTOTYPE_NAME = sys.argv[1]
SYSTEM = sys.argv[2]

# print("Prototypename: ",PROTOTYPE_NAME)

setup_django(SYSTEM, PROTOTYPE_NAME)

hidden_models = ["LogEntry", "Permission", "Group", "User", "ContentType", "Session"]

model_definition = extract_model_definitions(apps.get_models(), hidden_models)

# print(model_definition)

if len(model_definition) != 3:
    exit(1)

if not isinstance(model_definition[0], dict):
    exit(2)

if not "model_name" in model_definition[0]:
    exit(3)

if not "fields" in model_definition[0]:
    exit(4)

if len(model_definition[0].get("fields")) != 6:
    exit(6)

if not isinstance(model_definition[1], dict):
    exit(7)

if not "model_name" in model_definition[1]:
    exit(8)

if not "fields" in model_definition[1]:
    exit(9)

if len(model_definition[1].get("fields")) != 5:
    exit(10)

if not isinstance(model_definition[2], dict):
    exit(11)

if not "model_name" in model_definition[2]:
    exit(12)

if not "fields" in model_definition[2]:
    exit(13)

if len(model_definition[2].get("fields")) != 5:
    exit(14)

exit(0)



