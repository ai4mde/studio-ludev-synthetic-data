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
from generate_synthetic_data import toposort_models

PROTOTYPE_NAME = sys.argv[1]
SYSTEM = sys.argv[2]

setup_django(SYSTEM, PROTOTYPE_NAME)

hidden_models = ["LogEntry", "Permission", "Group", "User", "ContentType", "Session"]

model_names_sorted = toposort_models(apps.get_models(), hidden_models)

"""Check that the sorted list contains exactly 3 models."""
if len(model_names_sorted) != 3:
    print("Expected 3 models, got:", model_names_sorted)
    exit(1)

"""Check that the models are in the expected topological order."""
if model_names_sorted != ['Car', 'Person', 'Manufacturer']:
    print("Incorrect topological order:", model_names_sorted)
    exit(2)

"""Check that the models are in the expected order."""
# More dynamic than the previous test
def assert_order(before, after):
    if model_names_sorted.index(before) > model_names_sorted.index(after):
        print(f"Model {before} should come before {after}")
        exit(3)

assert_order("Car", "Manufacturer")
assert_order("Car", "Person")

"""Check that all hidden models are excluded from the sorted list."""
for hidden in hidden_models:
    if hidden in model_names_sorted:
        print(f"Hidden model {hidden} was not excluded.")
        exit(4)

"""Check for cycles in the model graph. Not strictly necessary for this test, but good to have I guess."""
try:
    toposort_models(apps.get_models(), hidden_models)
except Exception as e:
    if "cycle" in str(e).lower():
        print("Cycle detected when there should be none")
        exit(6)

"""Check that if all models are hidden, the sorted list is empty."""
# Get all model names
all_model_names = [model.__name__ for model in apps.get_models()]

# Now treat ALL models as hidden
all_model_names_sorted = toposort_models(apps.get_models(), all_model_names)

if all_model_names_sorted != []:
    print("Expected empty list when all models are hidden, got:", all_model_names_sorted)
    exit(7)


exit(0)
