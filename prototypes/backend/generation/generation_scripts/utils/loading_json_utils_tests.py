import unittest
import requests
from unittest.mock import patch
from utils import loading_json_utils 
from utils.definitions.model import AttributeType, Cardinality
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

class LoadingJsonUtilsUnitTests(unittest.TestCase):

    # This uses the PROTOTYPE_METADATA defined above
    def setUp(self):
        self.metadata = json.dumps(PROTOTYPE_METADATA)
    
    # This uses the PROTOTYPE_METADATA defined above
    def test_get_apps(self):
        result = loading_json_utils.get_apps(self.metadata)
        expected = "TestInterface"
        self.assertEqual(result, expected, f"Expected '{expected}', got '{result}'")

    def test_get_apps_invalid_json(self):
        metadata_broken = "{this is not valid json}"
        with self.assertRaises(Exception) as c:
            loading_json_utils.get_apps(metadata_broken)
        self.assertIn("Failed to retrieve names of interfaces", str(c.exception),
                      f"Expected error message to include 'Failed to retrieve names of interfaces', got: {c.exception}")

    def test_authentication_is_present_true(self):
        metadata_auth = json.dumps({"useAuthentication": True})
        result = loading_json_utils.authentication_is_present(metadata_auth)
        self.assertTrue(result, "Expected authentication to be present, but got False")

    def test_authentication_is_present_empty(self):
        with self.assertRaises(Exception, msg="Expected exception when metadata is empty"):
            loading_json_utils.authentication_is_present("")

    def test_use_synthetic_data_is_present_true(self):
        metadata_data = json.dumps({"useSyntheticData": True})
        result = loading_json_utils.use_synthetic_data_is_present(metadata_data)
        self.assertTrue(result, "Expected synthetic data to be present, but got False")

    def test_use_synthetic_data_is_present_empty(self):
        with self.assertRaises(Exception, msg="Expected exception when metadata is empty"):
            loading_json_utils.use_synthetic_data_is_present("")

    def test_get_synthetic_instructions_present(self):
        metadata_instr = json.dumps({"syntheticInstructions": "Generate 5 cars"})
        result = loading_json_utils.get_synthetic_instructions(metadata_instr)
        self.assertEqual(result, "Generate 5 cars", f"Expected 'Generate 5 cars', got '{result}'")

    def test_get_synthetic_instructions_empty(self):
        with self.assertRaises(Exception, msg="Expected exception when metadata is empty"):
            loading_json_utils.get_synthetic_instructions("")

    def test_get_synthetic_counts_present(self):
        metadata_counts = json.dumps({"syntheticCounts": {"Car": 5}})
        result = loading_json_utils.get_synthetic_counts(metadata_counts)
        self.assertEqual(result, {"Car": 5}, f"Expected {{'Car': 5}}, got {result}")

    def test_get_synthetic_counts_empty(self):
        with self.assertRaises(Exception, msg="Expected exception when metadata is empty"):
            loading_json_utils.get_synthetic_counts("")

    def test_get_enum_literals_found(self):
        metadata_enum = json.dumps({
            "diagrams": [
                {
                    "type": "classes",
                    "nodes": [
                        {
                            "cls_ptr": "qwe123",
                            "cls": {
                                "type": "enum",
                                "literals": ["A", "B", "C"]
                            }
                        }
                    ]
                }
            ]
        })
        result = loading_json_utils.get_enum_literals(metadata_enum, "qwe123")
        self.assertEqual(result, ["A", "B", "C"], f"Expected ['A', 'B', 'C'], got {result}")

    def test_get_enum_literals_not_found(self):
        metadata_enum_empty = json.dumps({"diagrams": []})
        result = loading_json_utils.get_enum_literals(metadata_enum_empty, "not_there")
        self.assertEqual(result, [], f"Expected empty list, got {result}")

    def test_find_model_by_class_ptr_found(self):
        metadata_ptr = json.dumps({
            "diagrams": [
                {
                    "type": "classes",
                    "nodes": [
                        {
                            "cls_ptr": "qwe123",
                            "cls": {
                                "name": "User",
                                "type": "class"
                            }
                        }
                    ]
                }
            ]
        })
        result = loading_json_utils.find_model_by_class_ptr(metadata_ptr, "qwe123")
        self.assertEqual(result, "cls_user", f"Expected 'cls_user', got {result}")

    def test_find_model_by_class_ptr_not_found(self):
        metadata_ptr_empty = json.dumps({"diagrams": []})
        result = loading_json_utils.find_model_by_class_ptr(metadata_ptr_empty, "missing")
        self.assertIsNone(result, f"Expected None when class_ptr not found, got {result}")

    def test_find_model_by_id_found(self):
        metadata_id = json.dumps({
            "diagrams": [
                {
                    "type": "classes",
                    "nodes": [
                        {
                            "id": "some_uuid",
                            "cls": {
                                "name": "Account",
                                "type": "class"
                            }
                        }
                    ]
                }
            ]
        })
        result = loading_json_utils.find_model_by_id(metadata_id, "some_uuid")
        self.assertEqual(result, "Account", f"Expected 'Account', got {result}")

    def test_find_model_by_id_not_found(self):
        metadata_id_empty = json.dumps({"diagrams": []})
        result = loading_json_utils.find_model_by_id(metadata_id_empty, "not_here")
        self.assertIsNone(result, f"Expected None when id not found, got {result}")

    def test_find_model_id_by_class_ptr_found(self):
        metadata_id_ptr = json.dumps({
            "diagrams": [
                {
                    "type": "classes",
                    "nodes": [
                        {
                            "id": "some_uuid",
                            "cls_ptr": "class_ptr_qwe"
                        }
                    ]
                }
            ]
        })
        result = loading_json_utils.find_model_id_by_class_ptr(metadata_id_ptr, "class_ptr_qwe")
        self.assertEqual(result, "some_uuid", f"Expected 'some_uuid', got {result}")

    def test_find_model_id_by_class_ptr_not_found(self):
        metadata_id_ptr_empty = json.dumps({"diagrams": []})
        result = loading_json_utils.find_model_id_by_class_ptr(metadata_id_ptr_empty, "missing_ptr")
        self.assertIsNone(result, f"Expected None when class_ptr not found, got {result}")




# TESTS USING OLD PROTOTYPE_METADATA
# opted out of that as i think it is better to use new small metadata for each test, 
# but tests could be rewritten to use one big metadata, but that is not recommended in my opinion 
# as some need different metadata to test different behavior which will only clutter this file
    def test_authentication_is_present(self):
        self.assertFalse(loading_json_utils.authentication_is_present(self.metadata))

    def test_use_synthetic_data_is_present(self):
        self.assertFalse(loading_json_utils.use_synthetic_data_is_present(self.metadata))

    def test_find_model_by_class_ptr(self):
        self.assertEqual(loading_json_utils.find_model_by_class_ptr(self.metadata, "05a02f6b-9236-4d34-bc9f-d2f25112a1bc"), "Person")
        self.assertEqual(loading_json_utils.find_model_by_class_ptr(self.metadata, "9816aca2-fadd-4944-97ce-ee2c1b6cf50f"), "Car")

    def test_find_model_by_id(self):
        self.assertEqual(loading_json_utils.find_model_by_id(self.metadata, "a07c0553-b238-4947-9303-e354509723ae"), "Person")
        self.assertEqual(loading_json_utils.find_model_by_id(self.metadata, "0d2763bf-ad3e-4ea5-a1ee-a3f902da2573"), "Car")

    def test_find_model_id_by_class_ptr(self):
        self.assertEqual(loading_json_utils.find_model_id_by_class_ptr(self.metadata, "05a02f6b-9236-4d34-bc9f-d2f25112a1bc"), "a07c0553-b238-4947-9303-e354509723ae")
        self.assertEqual(loading_json_utils.find_model_id_by_class_ptr(self.metadata, "9816aca2-fadd-4944-97ce-ee2c1b6cf50f"), "0d2763bf-ad3e-4ea5-a1ee-a3f902da2573")

if __name__ == '__main__':
    unittest.main()