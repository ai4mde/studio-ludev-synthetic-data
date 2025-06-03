from schema_extract import setup_django
from schema_extract import toposort_models
import sys
import django
from django.apps import apps
from django.db.models import ForeignKey, OneToOneField

PROTOTYPE_NAME = sys.argv[1]
SYSTEM = sys.argv[2]

setup_django(PROTOTYPE_NAME, SYSTEM)

hidden_models = ["LogEntry", "Permission", "Group", "User", "ContentType", "Session"]

model_names_sorted = toposort_models(apps.get_models(), hidden_models)

if len(model_names_sorted) != 3:
    exit(1)

if model_names_sorted != ['Car', 'Person', 'Manufacturer']:
    print(model_names_sorted)
    exit(2)


exit(0)



