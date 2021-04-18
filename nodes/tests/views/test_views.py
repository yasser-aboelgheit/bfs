from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from nodes.factories import NodeFactory, EdgeFactory
from nodes.models import Edge, Node


class TestRegisterNodeViewSet(APITestCase):
    def setUp(self):
        self.url = reverse('node-register')
        self.data = {"node_from": "A",
                     "node_to": "B"}

    def test_nodes_created(self):
        """
        Test if nodes with the names sent to API are saved in the database
        """
        self.assertFalse(Node.objects.filter(name="A").exists())
        self.assertFalse(Node.objects.filter(name="B").exists())
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Node.objects.filter(name="A").exists())
        self.assertTrue(Node.objects.filter(name="B").exists())

    def test_nodes_connected(self):
        """
        Test if nodes with the names sent to API are connected
        """
        node_a = Node.objects.filter(name="A").last()
        node_b = Node.objects.filter(name="B").last()
        self.assertFalse(node_a)
        self.assertFalse(node_b)
        self.assertFalse(Edge.objects.filter(node_from=node_a, node_to=node_b).exists())

        response = self.client.post(self.url, self.data)
        node_a = Node.objects.filter(name="A").last()
        node_b = Node.objects.filter(name="B").last()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Node.objects.filter(name="A").exists())
        self.assertTrue(Node.objects.filter(name="B").exists())
        self.assertTrue(Edge.objects.filter(node_from=node_a, node_to=node_b).exists())

    def test_empty_field(self):
        self.data = {"node_from": "A",}
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'node_to': ['This field is required.']})

        self.data = {"node_to": "B",}
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'node_from': ['This field is required.']})

    def test_redundant_edge(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get("message"), "This Edge is already existed")


class TestDisplayNodeViewSet(APITestCase):
    def setUp(self):
        self.url = reverse('path')
        self.node1 = NodeFactory.create()
        self.node2 = NodeFactory.create()
        self.node3 = NodeFactory.create()
        self.edge1 = EdgeFactory.create(node_from=self.node1, node_to=self.node2)

    def test_get_path(self):
        response = self.client.get(self.url, {'node_from':self.node1.name, "node_to": self.node2.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("path"), "%s, %s" %(self.node1.name, self.node2.name))

    def test_no_path(self):
        response = self.client.get(self.url, {'node_from':self.node1.name, "node_to": self.node3.name})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("message"), "No path found")
