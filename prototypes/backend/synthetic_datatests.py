import unittest
import requests
import schema_extract  
import time
import subprocess
from uuid import uuid4

PROTOTYPE_API = "http://localhost:8010" 

PROTOTYPE_ID = str(uuid4())
PROTOTYPE_NAME = "Test prototype"
PROTOTYPE_SYSTEM = str(uuid4())
PROTOTYPE_METADATA = {
    "diagrams": [
        {
        "id": "f7fdf00f-a567-4923-84e7-04f31dce3b73",
        "name": "Diagram",
        "type": "classes",
        "edges": [],
        "nodes": [
        {
            "id": "c16d3fae-5292-481b-a00c-e17cb954d98f",
            "cls": {
            "leaf": False,
            "name": "Users",
            "type": "class",
            "methods": [],
            "abstract": None,
            "namespace": "",
            "attributes": [
                {
                "body": None,
                "enum": None,
                "name": "Name",
                "type": "str",
                "derived": False,
                "description": None
                },
                {
                "body": None,
                "enum": None,
                "name": "Surname",
                "type": "str",
                "derived": False,
                "description": None
                },
                {
                "body": None,
                "enum": None,
                "name": "Email",
                "type": "str",
                "derived": False,
                "description": None
                },
                {
                "body": None,
                "enum": None,
                "name": "Age",
                "type": "int",
                "derived": False,
                "description": None
                },
                {
                "body": None,
                "enum": None,
                "name": "Premium",
                "type": "bool",
                "derived": False,
                "description": None
                }
            ]
            },
            "data": {
            "position": {
                "x": 0,
                "y": 0
            }
            },
            "cls_ptr": "1da630b8-e28b-41e3-8175-6ab2c4ba3dcb"
        }
        ],
        "system": "c9692c4e-b4cb-40f2-90c8-168d8d832fd5",
        "project": "2265b83e-4c7f-47a3-b89c-8206fd591ce9",
        "description": ""
    },
    {
        "id": "53dde750-4440-4dfc-8e61-403dabc5f5d8",
        "name": "Diagram",
        "type": "usecase",
        "edges": [],
        "nodes": [
        {
            "id": "17901aea-92af-4da8-a9f4-ad0c0ee12187",
            "cls": {
            "name": "Actor1",
            "type": "actor"
            },
            "data": {
            "position": {
                "x": 0,
                "y": 0
            }
            },
            "cls_ptr": "7ac07882-151d-4359-9558-d7e28319f52f"
        }
        ],
        "system": "c9692c4e-b4cb-40f2-90c8-168d8d832fd5",
        "project": "2265b83e-4c7f-47a3-b89c-8206fd591ce9",
        "description": ""
    }
    ],
    "interfaces": [
    {
        "label": "Test interface",
        "value": {
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
        "name": "Test interface",
        "actor": "7ac07882-151d-4359-9558-d7e28319f52f",
        "system": "c9692c4e-b4cb-40f2-90c8-168d8d832fd5",
        "description": ""
        }
    }
    ],
    "useSyntheticData": False,
    "useAuthentication": False
}



class SyntheticDataTests(unittest.TestCase):
    # def setUp(self):
    #     response = requests.post(f"{PROTOTYPE_API}/generate", json={
    #         "id": PROTOTYPE_ID,
    #         "name": PROTOTYPE_NAME,
    #         "system": PROTOTYPE_SYSTEM,
    #         "metadata": "{}"
    #     })
    #     assert response.status_code == 200, f"Setup failed: {response.text}"
    #     time.sleep(2)

    # def tearDown(self):
    #     response = requests.delete(f"{PROTOTYPE_API}/remove", json={
    #         "id": PROTOTYPE_ID,
    #         "name": PROTOTYPE_NAME,
    #         "system": PROTOTYPE_SYSTEM
    #     })
    #     assert response.status_code == 200, f"Teardown failed: {response.text}"

    def test_make_prompt_correct_model(self):
        response = schema_extract.make_synthetic_data_prompt([{'model_name': 'Manufacturer', 'fields': [{'name': 'id', 'type': 'BigAutoField', 'choices': None}, {'name': 'name1', 'type': 'CharField', 'choices': None}, {'name': 'age1', 'type': 'IntegerField', 'choices': None}]}], 3)
        assert type(response) == str, f"make prompt correct_model failed: {response}"

    def test_make_prompt_correct_multiple_models(self):
        response = schema_extract.make_synthetic_data_prompt([{'model_name': 'Delivery', 'fields': [{'name': 'id', 'type': 'BigAutoField', 'choices': None}, {'name': 'name', 'type': 'CharField', 'choices': None}, {'name': 'licence1', 'type': 'IntegerField', 'choices': None}, {'name': 'Manufacturer', 'type': 'ForeignKey', 'choices': None}]}, {'model_name': 'Manufacturer', 'fields': [{'name': 'id', 'type': 'BigAutoField', 'choices': None}, {'name': 'name1', 'type': 'CharField', 'choices': None}, {'name': 'age1', 'type': 'IntegerField', 'choices': None}]}, {'model_name': 'Person10', 'fields': [{'name': 'id', 'type': 'BigAutoField', 'choices': None}, {'name': 'name10', 'type': 'CharField', 'choices': None}, {'name': 'age10', 'type': 'IntegerField', 'choices': None}]}], 3)
        assert type(response) == str, f"make prompt multiple_models failed: {response}"

    def test_make_prompt_incorrect_model(self):
        with self.assertRaises(ValueError):
            schema_extract.make_synthetic_data_prompt([{'model_name': 'Manufacturer', 'fields': [{'name': 'id'}, {'name': 'age1', 'type': 'IntegerField', 'choices': None}]}], 3)
        # assert type(response) != str, f"make prompt incorrect_model failed: {response}"

    def test_make_prompt_incorrect_multiple_models(self):
        with self.assertRaises(ValueError):
            schema_extract.make_synthetic_data_prompt([{'model_name': 'Manufacturer', 'fields': [{'name': 'id'}, {'name': 'age1', 'type': 'IntegerField', 'choices': None}]}, {'model_name': 'Delivery', 'fields': [{'name': 'id', 'type': 'BigAutoField', 'choices': None}, {'name': 'name', 'type': 'CharField', 'choices': None}, {'name': 'licence1', 'type': 'IntegerField', 'choices': None}, {'name': 'Manufacturer', 'type': 'ForeignKey', 'choices': None}]}, {'model_name': 'Person10', 'fields': [{'name': 'id', 'type': 'BigAutoField', 'choices': None}, {'name': 'name10', 'type': 'CharField', 'choices': None}, {'name': 'age10', 'type': 'IntegerField', 'choices': None}]}], 3)
        # assert type(response) != str, f"make prompt multiple_incorrect_models failed: {response}"

    def test_make_prompt_negative_nrecords(self):
        with self.assertRaises(ValueError):
            schema_extract.make_synthetic_data_prompt([{'model_name': 'Manufacturer', 'fields': [{'name': 'id', 'type': 'BigAutoField', 'choices': None}, {'name': 'name1', 'type': 'CharField', 'choices': None}, {'name': 'age1', 'type': 'IntegerField', 'choices': None}]}], -3)
        # assert type(response) == str, f"make prompt negative_nrecords failed: {response}"

    def test_make_prompt_zero_nrecords(self):
        with self.assertRaises(ValueError):
            schema_extract.make_synthetic_data_prompt([{'model_name': 'Manufacturer', 'fields': [{'name': 'id', 'type': 'BigAutoField', 'choices': None}, {'name': 'name1', 'type': 'CharField', 'choices': None}, {'name': 'age1', 'type': 'IntegerField', 'choices': None}]}], 0)

    def test_make_prompt_no_fields(self):
        with self.assertRaises(ValueError):
            schema_extract.make_synthetic_data_prompt([], 3)

    def test_extract_model_definitions(self):
        response = requests.post(f"{PROTOTYPE_API}/generate", json={
            "id": PROTOTYPE_ID,
            "name": PROTOTYPE_NAME,
            "system": PROTOTYPE_SYSTEM,
            "metadata": str(PROTOTYPE_METADATA)
        })
        assert response.status_code == 200, f"Setup failed: {response.text}"
        time.sleep(2)

        testsubprocess1 = subprocess.run(
        ["python3", "/usr/src/prototypes/backend/test_extract_model_case_1.py", PROTOTYPE_NAME, PROTOTYPE_SYSTEM],
        stdout=subprocess.PIPE,
        text=True
        )
        print(testsubprocess1)
if __name__ == '__main__':
    unittest.main()
