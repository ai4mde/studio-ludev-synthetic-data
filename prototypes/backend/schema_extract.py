import os
import sys

PROTOTYPE_NAME = sys.argv[1]
SYSTEM = sys.argv[2]

print("my name is:", PROTOTYPE_NAME)
print("part of system:", SYSTEM)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'generated_prototypes', SYSTEM, PROTOTYPE_NAME))
sys.path.append(PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE",f"{PROTOTYPE_NAME}.settings")


import django
django.setup()

from django.apps import apps
import json

hidden_models = ["LogEntry", "Permission", "Group", "User", "ContentType", "Session"]
models = apps.get_models()

model_fields = []
enums = []

for model in models:
    if model.__name__ not in hidden_models :
        model_fields.append("model: " + model.__name__ + str(model._meta.get_fields()))
        for field in model._meta.fields:
            if field.choices == None:
                continue
            enums.append("model: " + model.__name__ + ", field: " + field.name + ", choices: " + str(field.choices))

prompt_string = "\n".join(model_fields) + "\n" + "\n".join(enums)
print(prompt_string)


for model in models:
    if model.__name__ not in hidden_models:
        print(f"Injecting data into model: {model.__name__}")

        instance = model()

        for field in model._meta.fields:
            field_name = field.name
            
            if isinstance(field, django.db.models.fields.AutoField): #skip primary key
                continue

            try:
                if isinstance(field, django.db.models.CharField):
                    setattr(instance, field_name, "testdata")
                elif isinstance(field, django.db.models.IntegerField):
                    setattr(instance, field_name, 123)
                elif isinstance(field, django.db.models.FloatField):
                    setattr(instance, field_name, 123.45)
                elif isinstance(field, django.db.models.BooleanField):
                    setattr(instance, field_name, True)
                elif isinstance(field, django.db.models.TextField):
                    setattr(instance, field_name, "testdata testdata testdata testdata")
                elif isinstance(field, django.db.models.ForeignKey):
                    continue  #skipping foreignley for now, need to be implemented in the future
                
            except Exception as e:
                print(f"Skipping field '{field_name}' due to error: {e}")

        try:
            instance.save()
            print(f"Data injected into {model.__name__} successfully!")
        except Exception as e:
            print(f"Failed to save data for {model.__name__}: {e}")