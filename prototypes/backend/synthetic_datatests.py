import unittest
import requests
import schema_extract  
import time
import subprocess
import json
from uuid import uuid4

PROTOTYPE_API = "http://localhost:8010" 

PROTOTYPE_ID = str(uuid4())
PROTOTYPE_NAME = "TestPrototype"
PROTOTYPE_SYSTEM = str(uuid4())
PROTOTYPE_METADATA = {
    "diagrams": [
    {
        "project": "a6987223-392e-4e9a-8a3d-9e80b12a3538",
        "id": "ed031cd6-9e07-4261-a4de-5b9c8f33b538",
        "name": "Diagram",
        "description": "",
        "type": "classes",
        "system": "ef54ea76-ee62-4d15-8d0e-bb4549d8dfbf",
        "nodes": [
        {
            "cls": {
            "namespace": "",
            "name": "Person",
            "type": "class",
            "attributes": [
                {
                "name": "name",
                "type": "str",
                "enum": None,
                "derived": False,
                "description": None,
                "body": None
                },
                {
                "name": "id",
                "type": "int",
                "enum": None,
                "derived": False,
                "description": None,
                "body": None
                },
                {
                "name": "adress",
                "type": "str",
                "enum": None,
                "derived": False,
                "description": None,
                "body": None
                },
                {
                "name": "House",
                "type": "bool",
                "enum": None,
                "derived": False,
                "description": None,
                "body": None
                }
            ],
            "methods": [],
            "abstract": False,
            "leaf": False
            },
            "cls_ptr": "05a02f6b-9236-4d34-bc9f-d2f25112a1bc",
            "data": {
            "position": {
                "x": -255,
                "y": -60
            }
            },
            "id": "a07c0553-b238-4947-9303-e354509723ae"
        },
        {
            "cls": {
            "namespace": "",
            "name": "Car",
            "type": "class",
            "attributes": [
                {
                "name": "brand",
                "type": "str",
                "enum": None,
                "derived": False,
                "description": None,
                "body": None
                },
                {
                "name": "licence",
                "type": "int",
                "enum": None,
                "derived": False,
                "description": None,
                "body": None
                },
                {
                "name": "manual",
                "type": "bool",
                "enum": None,
                "derived": False,
                "description": None,
                "body": None
                },
                {
                "name": "automatic",
                "type": "bool",
                "enum": None,
                "derived": False,
                "description": None,
                "body": None
                }
            ],
            "methods": [],
            "abstract": False,
            "leaf": False
            },
            "cls_ptr": "9816aca2-fadd-4944-97ce-ee2c1b6cf50f",
            "data": {
            "position": {
                "x": -15,
                "y": -60
            }
            },
            "id": "0d2763bf-ad3e-4ea5-a1ee-a3f902da2573"
        },
        {
            "cls": {
            "namespace": "",
            "name": "Manufacturer",
            "type": "class",
            "attributes": [
                {
                "name": "CompanyName",
                "type": "str",
                "enum": None,
                "derived": False,
                "description": None,
                "body": None
                },
                {
                "name": "kvk",
                "type": "int",
                "enum": None,
                "derived": False,
                "description": None,
                "body": None
                },
                {
                "name": "international",
                "type": "bool",
                "enum": None,
                "derived": False,
                "description": None,
                "body": None
                }
            ],
            "methods": [],
            "abstract": False,
            "leaf": False
            },
            "cls_ptr": "fb4356b9-2607-40e9-aaa8-564bf87548aa",
            "data": {
            "position": {
                "x": 255,
                "y": -45
            }
            },
            "id": "34ebf363-de6e-4c56-baee-1405bf719f05"
        }
        ],
        "edges": [
        {
            "rel": {
            "type": "association",
            "derived": False,
            "multiplicity": {
                "source": "1",
                "target": "*"
            },
            "labels": None,
            "label": "made_by"
            },
            "rel_ptr": "95263542-c316-45b8-9a88-4ef967827071",
            "data": {},
            "source_ptr": "0d2763bf-ad3e-4ea5-a1ee-a3f902da2573",
            "target_ptr": "34ebf363-de6e-4c56-baee-1405bf719f05",
            "id": "b497a3c6-621b-4b8d-bf4f-eb279347b0dd"
        },
        {
            "rel": {
            "type": "association",
            "derived": False,
            "multiplicity": {
                "source": "*",
                "target": "1"
            },
            "labels": None,
            "label": "owns"
            },
            "rel_ptr": "b837b977-6225-4ab3-a898-d18e1b6579cd",
            "data": {},
            "source_ptr": "a07c0553-b238-4947-9303-e354509723ae",
            "target_ptr": "0d2763bf-ad3e-4ea5-a1ee-a3f902da2573",
            "id": "84f0f529-e40d-49a7-be75-e259479b42fa"
        }
        ]
    },
    {
        "project": "a6987223-392e-4e9a-8a3d-9e80b12a3538",
        "id": "3bdb9ec8-bd71-455f-a6dc-74017fe23ddc",
        "name": "Diagram",
        "description": "",
        "type": "usecase",
        "system": "ef54ea76-ee62-4d15-8d0e-bb4549d8dfbf",
        "nodes": [
        {
            "cls": {
            "name": "Person",
            "type": "actor"
            },
            "cls_ptr": "9f936870-0fb3-4b09-b853-c95ba58851db",
            "data": {
            "position": {
                "x": 0,
                "y": 0
            }
            },
            "id": "a6e5b19d-4a67-494a-a0a6-e2f3dde94a41"
        }
        ],
        "edges": []
    }
    ],
    "interfaces": [
    {
        "label": "TestInterface",
        "value": 
        {
            "id": "ba483f50-6919-4ddb-81ca-f3a361e1e74c",
            "data": {
                "pages": [
                {
                    "id": "f5005759-2148-4747-b610-44cd83cbc108",
                    "name": "Test page",
                    "category": None,
                    "sections": [
                    {
                        "label": "Test SC",
                        "value": "ac5071f9-fc50-437e-8a8e-ae6bd560bf01"
                    }
                    ]
                }
                ],
                "styling": {},
                "sections": [
                {
                    "id": "ac5071f9-fc50-437e-8a8e-ae6bd560bf01",
                    "name": "Test SC",
                    "text": "Sample text",
                    "class": "1da630b8-e28b-41e3-8175-6ab2c4ba3dcb",
                    "attributes": [],
                    "operations": {
                    "create": True,
                    "delete": True,
                    "update": True
                    }
                }
                ],
                "categories": []
            },
            "name": "TestInterface",
            "actor": "7ac07882-151d-4359-9558-d7e28319f52f",
            "system": PROTOTYPE_SYSTEM,
            "description": "imagine"
        }
    }
    ],
    "useSyntheticData": False,
    "useAuthentication": False
}



class SyntheticDataUnitTests(unittest.TestCase):
    def test_make_prompt_correct_model(self):
        response = schema_extract.make_synthetic_data_prompt([{'model_name': 'Manufacturer', 'fields': [{'name': 'id', 'type': 'BigAutoField', 'choices': None}, {'name': 'name1', 'type': 'CharField', 'choices': None}, {'name': 'age1', 'type': 'IntegerField', 'choices': None}]}], 3)
        assert type(response) == str, f"Make prompt correct_model failed: {response}"

    def test_make_prompt_correct_multiple_models(self):
        response = schema_extract.make_synthetic_data_prompt([
            {'model_name': 'Delivery', 'fields': [{'name': 'id', 'type': 'BigAutoField', 'choices': None}, 
                                                  {'name': 'name', 'type': 'CharField', 'choices': None}, 
                                                  {'name': 'licence1', 'type': 'IntegerField', 'choices': None}, 
                                                  {'name': 'Manufacturer', 'type': 'ForeignKey', 'choices': None}]}, 
            {'model_name': 'Manufacturer', 'fields': [{'name': 'id', 'type': 'BigAutoField', 'choices': None}, 
                                                      {'name': 'name1', 'type': 'CharField', 'choices': None}, 
                                                      {'name': 'age1', 'type': 'IntegerField', 'choices': None}]}, 
            {'model_name': 'Person10', 'fields': [{'name': 'id', 'type': 'BigAutoField', 'choices': None}, 
                                                  {'name': 'name10', 'type': 'CharField', 'choices': None}, 
                                                  {'name': 'age10', 'type': 'IntegerField', 'choices': None}]}
            ], 3)
        assert type(response) == str, f"Make prompt multiple_models failed: {response}"

    def test_make_prompt_incorrect_model(self):
        with self.assertRaises(ValueError):
            schema_extract.make_synthetic_data_prompt([{'model_name': 'Manufacturer', 'fields': [{'name': 'id'}, {'name': 'age1', 'type': 'IntegerField', 'choices': None}]}], 3)

    def test_make_prompt_incorrect_multiple_models(self):
        with self.assertRaises(ValueError):
            schema_extract.make_synthetic_data_prompt([{'model_name': 'Manufacturer', 'fields': [{'name': 'id'}, {'name': 'age1', 'type': 'IntegerField', 'choices': None}]}, {'model_name': 'Delivery', 'fields': [{'name': 'id', 'type': 'BigAutoField', 'choices': None}, {'name': 'name', 'type': 'CharField', 'choices': None}, {'name': 'licence1', 'type': 'IntegerField', 'choices': None}, {'name': 'Manufacturer', 'type': 'ForeignKey', 'choices': None}]}, {'model_name': 'Person10', 'fields': [{'name': 'id', 'type': 'BigAutoField', 'choices': None}, {'name': 'name10', 'type': 'CharField', 'choices': None}, {'name': 'age10', 'type': 'IntegerField', 'choices': None}]}], 3)

    def test_make_prompt_negative_nrecords(self):
        with self.assertRaises(ValueError):
            schema_extract.make_synthetic_data_prompt([{'model_name': 'Manufacturer', 'fields': [{'name': 'id', 'type': 'BigAutoField', 'choices': None}, {'name': 'name1', 'type': 'CharField', 'choices': None}, {'name': 'age1', 'type': 'IntegerField', 'choices': None}]}], -3)

    def test_make_prompt_zero_nrecords(self):
        with self.assertRaises(ValueError):
            schema_extract.make_synthetic_data_prompt([{'model_name': 'Manufacturer', 'fields': [{'name': 'id', 'type': 'BigAutoField', 'choices': None}, {'name': 'name1', 'type': 'CharField', 'choices': None}, {'name': 'age1', 'type': 'IntegerField', 'choices': None}]}], 0)

    def test_make_prompt_no_fields(self):
        with self.assertRaises(ValueError):
            schema_extract.make_synthetic_data_prompt([], 3)
    
    

class SyntheticDataIntegrationTests(unittest.TestCase):
    def test_extract_model_definitions(self):

        #Generate the prototype to perform a test on
        response = requests.post(f"{PROTOTYPE_API}/generate", json={
            "id": PROTOTYPE_ID,
            "name": PROTOTYPE_NAME,
            "system": PROTOTYPE_SYSTEM,
            "metadata": json.dumps(PROTOTYPE_METADATA)
        })
        #I think this assert should only be done on the first integration test
        assert response.status_code == 200, f"Setup failed: {response.text}" 

        # print("prototypename before", PROTOTYPE_NAME)
        # print("prototypeid before", PROTOTYPE_ID)
        # print("Protype system before", PROTOTYPE_SYSTEM)

        testsubprocess = subprocess.run(
        ["python3", "/usr/src/prototypes/backend/test_extract_model_case_1.py", PROTOTYPE_NAME, PROTOTYPE_SYSTEM]
        )

        #Remove the prototype
        requests.delete(f"{PROTOTYPE_API}/remove", json={
            "id": PROTOTYPE_ID,
            "name": PROTOTYPE_NAME,
            "system": PROTOTYPE_SYSTEM,
        })
        
        assert testsubprocess.returncode == 0

class ToposortUnitTests(unittest.TestCase):
    def test_toposort_models(self):

        response = requests.post(f"{PROTOTYPE_API}/generate", json={
            "id": PROTOTYPE_ID,
            "name": PROTOTYPE_NAME,
            "system": PROTOTYPE_SYSTEM,
            "metadata": json.dumps(PROTOTYPE_METADATA)
        })
        
        assert response.status_code == 200, f"Setup failed: {response.text}" 

        testsubprocess = subprocess.run(
        ["python3", "/usr/src/prototypes/backend/test_toposort_models_.py", PROTOTYPE_NAME, PROTOTYPE_SYSTEM]
        )

        #Remove the prototype
        requests.delete(f"{PROTOTYPE_API}/remove", json={
            "id": PROTOTYPE_ID,
            "name": PROTOTYPE_NAME,
            "system": PROTOTYPE_SYSTEM,
        })
        assert testsubprocess.returncode == 0

if __name__ == '__main__':
    unittest.main()
