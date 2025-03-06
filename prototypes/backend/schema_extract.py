import os
import sys

PROTOTYPE_NAME = sys.argv[1]

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'generated_prototypes',PROTOTYPE_NAME))
sys.path.append(PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE",f"{PROTOTYPE_NAME}.settings")


import django
django.setup()

from django.apps import apps
import json

hidden_models = ["LogEntry", "Permission", "Group", "User", "ContentType", "Session"]

for model in apps.get_models():
    if model.__name__ not in hidden_models :
        print("model: ")
        print(model.__name__, model._meta.get_fields())
        for field in model._meta.fields:
            if field.choices == None:
                continue
            print(field.name, "choices: ", field.choices)