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

try:
    toposort_models(apps.get_models(), hidden_models)
    print("Expected cycle detection, but no error was raised")
    exit(1)
except Exception as e:
    if "cycle" not in str(e).lower():
        print("Unexpected error raised (not a cycle):", str(e))
        exit(2)

exit(0)
