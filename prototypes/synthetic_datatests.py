import unittest
import requests
import backend.generation.generation_scripts.generate_synthetic_data as generate_synthetic_data
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

ZERO_MODELS_METADATA = {
    "diagrams": [
    {
        "project": "a6987223-392e-4e9a-8a3d-9e80b12a3538",
        "id": "ed031cd6-9e07-4261-a4de-5b9c8f33b538",
        "name": "Diagram",
        "description": "",
        "type": "classes",
        "system": "ef54ea76-ee62-4d15-8d0e-bb4549d8dfbf",
        "nodes": [],
        "edges": []
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
    "interfaces": [],
    "useSyntheticData": False,
    "useAuthentication": False
}

ONE_MODEL_METADATA = {
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
            "name": "single",
            "type": "class",
            "attributes": [
                {
                "name": "name",
                "type": "str",
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
        }
        ],
        "edges": []
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

CYCLE_METADATA = {
  "diagrams": [
    {
      "id": "fcccfa68-15ae-4c5e-9b8e-702208424072",
      "name": "Diagram",
      "type": "usecase",
      "edges": [],
      "nodes": [
        {
          "id": "18b9d728-65bd-4c88-906f-6603bc5bb728",
          "cls": {
            "name": "aa",
            "type": "actor"
          },
          "data": {
            "position": {
              "x": 0,
              "y": 0
            }
          },
          "cls_ptr": "6226bcb7-7901-4e55-9fea-ebe8de3a0d76"
        }
      ],
      "system": "4c722d94-3e58-42c4-937a-abf11932e945",
      "project": "581b0436-fa69-48de-bf37-93bf838dc8f6",
      "description": ""
    },
    {
      "id": "23d44848-89d8-4b2e-bca7-c79a46ad3381",
      "name": "Diagram",
      "type": "classes",
      "edges": [
        {
          "id": "0d0591d7-1b46-4813-a81c-67e4f4efbffc",
          "rel": {
            "type": "association",
            "label": "PM",
            "labels": None,
            "derived": False,
            "multiplicity": {
              "source": "1",
              "target": "*"
            }
          },
          "data": {},
          "rel_ptr": "7828f66f-83ef-47e6-ac08-038c45239026",
          "source_ptr": "3ade4d12-d9f4-4dfd-8adc-ecf347df3b04",
          "target_ptr": "46182770-a062-45a9-9c16-d61b5a1c114e"
        },
        {
          "id": "6172b291-e82a-4eff-822e-5ece1a38b8fa",
          "rel": {
            "type": "association",
            "label": "MC",
            "labels": None,
            "derived": False,
            "multiplicity": {
              "source": "1",
              "target": "*"
            }
          },
          "data": {},
          "rel_ptr": "e7fec052-da7e-441e-933a-57252e70deed",
          "source_ptr": "46182770-a062-45a9-9c16-d61b5a1c114e",
          "target_ptr": "98986fa8-d1f5-438c-8451-522cad2fc0d4"
        },
        {
          "id": "15eb06f5-d180-4c6b-9ab7-75966fb13b17",
          "rel": {
            "type": "association",
            "label": "MP",
            "labels": None,
            "derived": False,
            "multiplicity": {
              "source": "1",
              "target": "*"
            }
          },
          "data": {},
          "rel_ptr": "7c8cc18f-bc58-4dff-90f7-3450ce3e7fa4",
          "source_ptr": "98986fa8-d1f5-438c-8451-522cad2fc0d4",
          "target_ptr": "3ade4d12-d9f4-4dfd-8adc-ecf347df3b04"
        }
      ],
      "nodes": [
        {
          "id": "46182770-a062-45a9-9c16-d61b5a1c114e",
          "cls": {
            "leaf": False,
            "name": "Manufacturer",
            "type": "class",
            "methods": [],
            "abstract": False,
            "namespace": "",
            "attributes": []
          },
          "data": {
            "position": {
              "x": 270,
              "y": -135
            }
          },
          "cls_ptr": "53ca3af7-3562-40eb-a48d-5919614df6ec"
        },
        {
          "id": "98986fa8-d1f5-438c-8451-522cad2fc0d4",
          "cls": {
            "leaf": False,
            "name": "Car",
            "type": "class",
            "methods": [],
            "abstract": False,
            "namespace": "",
            "attributes": []
          },
          "data": {
            "position": {
              "x": 45,
              "y": -30
            }
          },
          "cls_ptr": "bc74cf91-c985-40e8-b903-8cc9a18cac13"
        },
        {
          "id": "3ade4d12-d9f4-4dfd-8adc-ecf347df3b04",
          "cls": {
            "leaf": False,
            "name": "Person",
            "type": "class",
            "methods": [],
            "abstract": False,
            "namespace": "",
            "attributes": []
          },
          "data": {
            "position": {
              "x": 345,
              "y": 60
            }
          },
          "cls_ptr": "4da86857-924a-475f-885b-1dd899bd37ef"
        }
      ],
      "system": "4c722d94-3e58-42c4-937a-abf11932e945",
      "project": "581b0436-fa69-48de-bf37-93bf838dc8f6",
      "description": ""
    }
  ],
  "interfaces": [
    {
      "label": "aa",
      "value": {
        "id": "e4a37908-f633-498f-8c9c-648ae15cb0da",
        "data": {
          "pages": [
            {
              "id": "30965282-8274-4200-a83a-cf967ca60798",
              "name": "Page 1",
              "category": None,
              "sections": [
                {
                  "label": "Section Component 1",
                  "value": "1055a55d-64c1-4701-a766-cee4cde90d71"
                },
                {
                  "label": "Section Component 2",
                  "value": "74b3ad69-bc4e-414d-9217-ee439df2401c"
                },
                {
                  "label": "Section Component 3",
                  "value": "da0caffe-c763-4a12-929d-cecb30f77e8e"
                }
              ]
            }
          ],
          "styling": {
            "radius": 0,
            "textColor": "#000000",
            "accentColor": "#F5F5F4",
            "selectedStyle": "modern",
            "backgroundColor": "#FFFFFF"
          },
          "sections": [
            {
              "id": "1055a55d-64c1-4701-a766-cee4cde90d71",
              "name": "Section Component 1",
              "text": "1",
              "class": "4da86857-924a-475f-885b-1dd899bd37ef",
              "attributes": [],
              "operations": {
                "create": True,
                "delete": True,
                "update": True
              }
            },
            {
              "id": "74b3ad69-bc4e-414d-9217-ee439df2401c",
              "name": "Section Component 2",
              "text": "2",
              "class": "53ca3af7-3562-40eb-a48d-5919614df6ec",
              "attributes": [],
              "operations": {
                "create": True,
                "delete": True,
                "update": True
              }
            },
            {
              "id": "da0caffe-c763-4a12-929d-cecb30f77e8e",
              "name": "Section Component 3",
              "text": "3",
              "class": "bc74cf91-c985-40e8-b903-8cc9a18cac13",
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
        "name": "aa",
        "actor": "6226bcb7-7901-4e55-9fea-ebe8de3a0d76",
        "system": "4c722d94-3e58-42c4-937a-abf11932e945",
        "description": "aa application"
      }
    }
  ],
  "syntheticCounts": {},
  "useSyntheticData": False,
  "useAuthentication": False
}

class SyntheticDataUnitTests(unittest.TestCase):
    def test_make_prompt_correct_model(self):
        response = generate_synthetic_data.make_prompt([{'model_name': 'Manufacturer', 'fields': [{'name': 'id', 'type': 'BigAutoField', 'choices': None}, {'name': 'name1', 'type': 'CharField', 'choices': None}, {'name': 'age1', 'type': 'IntegerField', 'choices': None}]}], "", {"Manufacturer":3}, {})
        assert type(response) == str, f"Make prompt correct_model failed: {response}"

    def test_make_prompt_correct_multiple_models(self):
        response = generate_synthetic_data.make_prompt([
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
            ], "", {"Manufacturer": 3, "Delivery": 3, "Person10": 3}, {})
        assert type(response) == str, f"Make prompt multiple_models failed: {response}"

    def test_make_prompt_incorrect_model(self):
        with self.assertRaises(ValueError):
            generate_synthetic_data.make_prompt([{'model_name': 'Manufacturer', 'fields': [{'name': 'id'}, {'name': 'age1', 'type': 'IntegerField', 'choices': None}]}], "", {"Manufacturer":3}, {})

    def test_make_prompt_incorrect_multiple_models(self):
        with self.assertRaises(ValueError):
            generate_synthetic_data.make_prompt([{'model_name': 'Manufacturer', 'fields': [{'name': 'id'}, {'name': 'age1', 'type': 'IntegerField', 'choices': None}]}, {'model_name': 'Delivery', 'fields': [{'name': 'id', 'type': 'BigAutoField', 'choices': None}, {'name': 'name', 'type': 'CharField', 'choices': None}, {'name': 'licence1', 'type': 'IntegerField', 'choices': None}, {'name': 'Manufacturer', 'type': 'ForeignKey', 'choices': None}]}, {'model_name': 'Person10', 'fields': [{'name': 'id', 'type': 'BigAutoField', 'choices': None}, {'name': 'name10', 'type': 'CharField', 'choices': None}, {'name': 'age10', 'type': 'IntegerField', 'choices': None}]}], "", {"Manufacturer": 3, "Delivery": 3, "Person10": 3}, { })

    def test_make_prompt_negative_nrecords(self):
        with self.assertRaises(ValueError):
            generate_synthetic_data.make_prompt([{'model_name': 'Manufacturer', 'fields': [{'name': 'id', 'type': 'BigAutoField', 'choices': None}, {'name': 'name1', 'type': 'CharField', 'choices': None}, {'name': 'age1', 'type': 'IntegerField', 'choices': None}]}], "", {"Manufacturer": -3}, {})

    def test_make_prompt_zero_nrecords(self):
        with self.assertRaises(ValueError):
            generate_synthetic_data.make_prompt([{'model_name': 'Manufacturer', 'fields': [{'name': 'id', 'type': 'BigAutoField', 'choices': None}, {'name': 'name1', 'type': 'CharField', 'choices': None}, {'name': 'age1', 'type': 'IntegerField', 'choices': None}]}], "", {"Manufacturer": 0}, {})

    def test_make_prompt_no_fields(self):
        with self.assertRaises(ValueError):
            generate_synthetic_data.make_prompt([], "", {}, {})

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

        testsubprocess = subprocess.run(
        ["python3", "/usr/src/prototypes/backend/tests/test_extract_model_case_1.py", PROTOTYPE_NAME, PROTOTYPE_SYSTEM]
        )

        #Remove the prototype
        requests.delete(f"{PROTOTYPE_API}/remove", json={
            "id": PROTOTYPE_ID,
            "name": PROTOTYPE_NAME,
            "system": PROTOTYPE_SYSTEM,
        })
        
        assert testsubprocess.returncode == 0, f"Extract model definitions test failed with return code {testsubprocess.returncode}: {testsubprocess.stderr}"

    def test_toposort_models_three_chain(self):
        response = requests.post(f"{PROTOTYPE_API}/generate", json={
            "id": PROTOTYPE_ID,
            "name": PROTOTYPE_NAME,
            "system": PROTOTYPE_SYSTEM,
            "metadata": json.dumps(PROTOTYPE_METADATA)
        })
        
        assert response.status_code == 200, f"Setup failed: {response.text}" 

        testsubprocess = subprocess.run(
        ["python3", "/usr/src/prototypes/backend/tests/test_toposort_models_case_1.py", PROTOTYPE_NAME, PROTOTYPE_SYSTEM]
        )

        #Remove the prototype
        requests.delete(f"{PROTOTYPE_API}/remove", json={
            "id": PROTOTYPE_ID,
            "name": PROTOTYPE_NAME,
            "system": PROTOTYPE_SYSTEM,
        })
        assert testsubprocess.returncode == 0, f"Toposort test failed with return code {testsubprocess.returncode}: {testsubprocess.stderr}"

    # ZERO MODELS METADATA TOPOSORT TEST
    def test_toposort_zero_models(self):
        response = requests.post(f"{PROTOTYPE_API}/generate", json={
            "id": PROTOTYPE_ID,
            "name": PROTOTYPE_NAME,
            "system": PROTOTYPE_SYSTEM,
            "metadata": json.dumps(ZERO_MODELS_METADATA)
        })
        
        assert response.status_code == 200, f"Setup failed: {response.text}" 

        testsubprocess = subprocess.run(
        ["python3", "/usr/src/prototypes/backend/tests/test_toposort_models_case_2.py", PROTOTYPE_NAME, PROTOTYPE_SYSTEM]
        )

        #Remove the prototype
        requests.delete(f"{PROTOTYPE_API}/remove", json={
            "id": PROTOTYPE_ID,
            "name": PROTOTYPE_NAME,
            "system": PROTOTYPE_SYSTEM,
        })
        assert testsubprocess.returncode == 0, f"Toposort test failed with return code {testsubprocess.returncode}: {testsubprocess.stderr}"

    # ONE MODEL METADATA TOPOSORT TEST
    def test_toposort_one_model(self):
        response = requests.post(f"{PROTOTYPE_API}/generate", json={
            "id": PROTOTYPE_ID,
            "name": PROTOTYPE_NAME,
            "system": PROTOTYPE_SYSTEM,
            "metadata": json.dumps(ONE_MODEL_METADATA)
        })
        
        assert response.status_code == 200, f"Setup failed: {response.text}" 

        testsubprocess = subprocess.run(
        ["python3", "/usr/src/prototypes/backend/tests/test_toposort_models_case_3.py", PROTOTYPE_NAME, PROTOTYPE_SYSTEM]
        )

        #Remove the prototype
        requests.delete(f"{PROTOTYPE_API}/remove", json={
            "id": PROTOTYPE_ID,
            "name": PROTOTYPE_NAME,
            "system": PROTOTYPE_SYSTEM,
        })
        assert testsubprocess.returncode == 0, f"Toposort test failed with return code {testsubprocess.returncode}: {testsubprocess.stderr}"

    # CYCLE MODEL METADATA TOPOSORT TEST
    def test_toposort_cycle_model(self):
        response = requests.post(f"{PROTOTYPE_API}/generate", json={
            "id": PROTOTYPE_ID,
            "name": PROTOTYPE_NAME,
            "system": PROTOTYPE_SYSTEM,
            "metadata": json.dumps(CYCLE_METADATA)
        })
        
        assert response.status_code == 200, f"Setup failed: {response.text}" 

        testsubprocess = subprocess.run(
        ["python3", "/usr/src/prototypes/backend/tests/test_toposort_models_case_4.py", PROTOTYPE_NAME, PROTOTYPE_SYSTEM]
        )

        #Remove the prototype
        requests.delete(f"{PROTOTYPE_API}/remove", json={
            "id": PROTOTYPE_ID,
            "name": PROTOTYPE_NAME,
            "system": PROTOTYPE_SYSTEM,
        })
        assert testsubprocess.returncode == 0, f"Toposort test failed with return code {testsubprocess.returncode}: {testsubprocess.stderr}"

#####################################################################################################################

    # def test_save_records_models(self):
    #     # First, create the prototype using the same setup pattern
    #     response = requests.post(f"{PROTOTYPE_API}/generate", json={
    #         "id": PROTOTYPE_ID,
    #         "name": PROTOTYPE_NAME,
    #         "system": PROTOTYPE_SYSTEM,
    #         "metadata": json.dumps(PROTOTYPE_METADATA)
    #     })
        
    #     assert response.status_code == 200, f"Setup failed: {response.text}"

    #     # Run the test script for save_records
    #     testsubprocess = subprocess.run(
    #         ["python3", "/usr/src/prototypes/backend/tests/test_save_records_models.py", PROTOTYPE_NAME, PROTOTYPE_SYSTEM]
    #     )

    #     # Clean up the prototype
    #     requests.delete(f"{PROTOTYPE_API}/remove", json={
    #         "id": PROTOTYPE_ID,
    #         "name": PROTOTYPE_NAME,
    #         "system": PROTOTYPE_SYSTEM,
    #     })

    #     assert testsubprocess.returncode == 0, f"Save records test failed with return code {testsubprocess.returncode}: {testsubprocess.stderr}"


if __name__ == '__main__':
    unittest.main()
