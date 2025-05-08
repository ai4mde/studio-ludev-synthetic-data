from django.urls import reverse
from rest_framework.test import APITestCase
from generator.models import Prototype
from metadata.models import Project, System
from django.contrib.auth.models import User
from uuid import uuid4
import json

prototype_metadata = {
    "diagrams": [],
    "interfaces": [],
    "useAuthentication": True
}

synthetic_data_prototype_metadata = {
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


class PrototypeAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', password='sequoias')

        auth_url = '/api/v1/auth/token'
        auth_response = self.client.post(auth_url, {'username': 'admin', 'password': 'sequoias'}, format='json')
        self.assertEqual(auth_response.status_code, 200)
        self.token = auth_response.json()['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.project1 = Project.objects.create(name="TestProject",
                                               description="Testing description."
                                               )
        self.system1 = System.objects.create(name="TestSystem1",
                                             project=self.project1,
                                             description="Testing system 1."
                                             )
        self.system2 = System.objects.create(name="TestSystem2",
                                             project=self.project1,
                                             description="Testing system 2."
                                             )
        
        self.system3 = System.objects.create(name="TestSystem3",
                                             project=self.project1,
                                             description="Testing system 3."
                                             )

        self.prototype1 = Prototype.objects.create(name="TestPrototype1",
                                                   system=self.system1,
                                                   description="Testing prototype 1.",
                                                   metadata=prototype_metadata,
                                                   database_hash=uuid4())
        self.prototype2 = Prototype.objects.create(name="TestPrototype2",
                                                   system=self.system1,
                                                   description="Testing prototype 2.",
                                                   metadata=prototype_metadata,
                                                   database_hash=uuid4())
        self.prototype3 = Prototype.objects.create(name="TestPrototype3",
                                                   system=self.system2,
                                                   description="Testing prototype 3.",
                                                   metadata=prototype_metadata,
                                                   database_hash=uuid4())
        
        self.prototype4 = Prototype.objects.create(name="TestPrototype4_a",
                                                   system=self.system3,
                                                   description="Testing...",
                                                   metadata=synthetic_data_prototype_metadata,
                                                   database_hash=uuid4())

        self.url = reverse('api-0.0.1:list_prototypes')

    def test_list_all_prototypes(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)  # All prototypes
        
        response_data = response.json()
        prototype_names = [prototype['name'] for prototype in response_data]
        self.assertIn(self.prototype1.name, prototype_names)
        self.assertIn(self.prototype2.name, prototype_names)
        self.assertIn(self.prototype3.name, prototype_names)

    def test_list_prototypes_by_system(self):
        response = self.client.get(self.url, {'system': self.system1.id})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)  # Prototype 1 & Prototype 2
        
        response_data = response.json()
        prototype_names = [prototype['name'] for prototype in response_data]
        self.assertIn(self.prototype1.name, prototype_names)
        self.assertIn(self.prototype2.name, prototype_names)

    def test_list_prototypes_empty_system(self):
        response = self.client.get(self.url, {'system': uuid4()}) # Random uuid
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)  # No prototypes

    def test_generate_and_remove_prototype(self):
        url2 = reverse('api-0.0.1:test_create_prototype',kwargs={'id': self.prototype4.id})
        response2 = self.client.post(url2)
        self.assertEqual(response2.status_code, 200)

        url3 = reverse('api-0.0.1:delete_system_prototypes',kwargs={'system_id': self.prototype4.system.id})
        response3 = self.client.delete(url3)
        self.assertEqual(response3.status_code, 200)

