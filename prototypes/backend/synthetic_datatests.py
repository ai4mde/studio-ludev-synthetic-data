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
        "id": "f7fdf00f-a567-4923-84e7-04f31dce3b73",
        "name": "Diagram",
        "type": "classes",
        "edges": [],
        "nodes": [
        {
            "id": "c16d3fae-5292-481b-a00c-e17cb954d98f",
            "cls": 
            {
                "leaf": False,
                "name": "Customer",
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
            "data": 
            {
                "position": {
                    "x": 0,
                    "y": 0
                }
            },
            "cls_ptr": "1da630b8-e28b-41e3-8175-6ab2c4ba3dcb"
        }
        ],
        "system": PROTOTYPE_SYSTEM,
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
        "system": PROTOTYPE_SYSTEM,
        "project": "2265b83e-4c7f-47a3-b89c-8206fd591ce9",
        "description": ""
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
    
    # Thought I'd add this test because it seems like a straightforward (though perhaps unlikely) edge case
    def test_make_prompt_no_models(self):
        with self.assertRaises(ValueError):
            schema_extract.make_synthetic_data_prompt(None, 3)

class ToposortUnitTests(unittest.TestCase):
    def test_toposort_no_dependencies(self):
        models = [
            {'model_name': 'A', 'fields': [{'name': 'id', 'type': 'BigAutoField', 'choices': None}]},
            {'model_name': 'B', 'fields': [{'name': 'id', 'type': 'BigAutoField', 'choices': None}]}
            ]
        sorted_models = schema_extract.toposort_models(models, hidden_models=[])
        # Made it dynamic to avoid hardcoding the order if the model names change or the list gets longer
        input_names = [m['model_name'] for m in sorted_models]
        output_names = [m['model_name'] for m in models]
        assert input_names == output_names, f"Toposort with no dependencies failed: {sorted_models}"

    def test_toposort_single_dependency(self):
        models = [
            {'model_name': 'A', 'fields': [{'name': 'id', 'type': 'BigAutoField', 'choices': None},
                                           {'name': 'B', 'type': 'ForeignKey', 'choices': None}]},
            {'model_name': 'B', 'fields': [{'name': 'id', 'type': 'BigAutoField', 'choices': None}]}
            ]
        sorted_names = schema_extract.toposort_models(models, hidden_models=[])
        assert sorted_names.index('A') < sorted_names.index('B'), f"'A' should come before 'B': {sorted_names}"

    def test_toposort_multiple_dependencies(self):
        models = [
            {'model_name': 'A', 'fields': [{'name': 'id', 'type': 'BigAutoField', 'choices': None},
                                           {'name': 'B', 'type': 'ForeignKey', 'choices': None}]},
            {'model_name': 'B', 'fields': [{'name': 'id', 'type': 'BigAutoField', 'choices': None},
                                           {'name': 'C', 'type': 'ForeignKey', 'choices': None}]},
            {'model_name': 'C', 'fields': [{'name': 'id', 'type': 'BigAutoField', 'choices': None}]}
            ]
        sorted_names = schema_extract.toposort_models(models, hidden_models=[])
        assert sorted_names.index('A') < sorted_names.index('B'), f"'A' should come before 'B': {sorted_names}"
        assert sorted_names.index('B') < sorted_names.index('C'), f"'B' should come before 'C': {sorted_names}"
    

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

        print("prototypename before", PROTOTYPE_NAME)
        print("prototypeid before", PROTOTYPE_ID)
        print("Protype system before", PROTOTYPE_SYSTEM)

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


if __name__ == '__main__':
    unittest.main()
