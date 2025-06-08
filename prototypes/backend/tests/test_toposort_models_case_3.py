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

model_names_sorted_single = toposort_models(apps.get_models(), hidden_models)

"""Check that exactly one model is returned."""
if len(model_names_sorted_single) != 1:
    print("Expected 1 model, got:", model_names_sorted_single)
    exit(1)

# Kind of redundant, but why not
"""Check that the model is named 'single'."""
if model_names_sorted_single[0] != "single":
    print("Expected model 'single', got:", model_names_sorted_single)
    exit(2)

exit(0)
