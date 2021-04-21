from django.test import TestCase
from nodes.factories import NodeFactory, EdgeFactory


class TestNodeModel(TestCase):
    def setUp(self):
        self.node1 = NodeFactory.create()
        self.node2 = NodeFactory.create()
        self.edge1 = EdgeFactory.create(
            node_from=self.node1, node_to=self.node2)

    def test_get_neighbors(self):
        """
        Test get_neighbors function, should return node's neighbors
        """
        node1_neighbors = self.node1.get_neighbors()
        self.assertEqual(node1_neighbors, [self.node2])
