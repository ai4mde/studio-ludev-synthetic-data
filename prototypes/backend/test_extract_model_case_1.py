from schema_extract import setup_django
from schema_extract import extract_model_definitions
import sys
import django
from django.apps import apps
from django.db.models import ForeignKey, OneToOneField

PROTOTYPE_NAME = sys.argv[1]
SYSTEM = sys.argv[2]

setup_django(PROTOTYPE_NAME, SYSTEM)

hidden_models = ["LogEntry", "Permission", "Group", "User", "ContentType", "Session"]
print(extract_model_definitions(apps.get_models(), hidden_models))



