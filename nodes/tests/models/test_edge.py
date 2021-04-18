from django.test import TestCase
from nodes.factories import NodeFactory, EdgeFactory
from nodes.models import Edge, Node


class TestEdgeModel(TestCase):
    def setUp(self):
        self.node1 = NodeFactory.create()
        self.node2 = NodeFactory.create()
        self.node3 = NodeFactory.create()
        self.node4 = NodeFactory.create()
        self.edge1 = EdgeFactory.create(node_from=self.node1, node_to=self.node2)
        self.edge2 = EdgeFactory.create(node_from=self.node2, node_to=self.node3)

    def test_bfs_no_path(self):
        """
        Test bfs function, in case of no path should return False
        """
        path = Edge.bfs(self.node1, self.node4)
        self.assertEqual(False, path)

    def test_bfs_path(self):
        """
        Test bfs function, should return dict of nodes objects and prev nodes
        """
        path = Edge.bfs(self.node1, self.node2)
        node2_content = {"node": self.node2,
                        "prev":self.node1.name}
        self.assertEqual(path[self.node2.name], node2_content)
        self.assertEqual([*path].sort(), [self.node1.name, self.node2.name].sort())

    def test_get_shortest_path(self):
        """
        Test get_shortest_path, should return string of nodes visited to get from certain node to another
        """
        graph = {self.node1.name: {"node":self.node1,
                                    "prev":self.node1},
                self.node2.name: {"node":self.node2,
                                    "prev":self.node1.name},
                self.node3.name: {"node":self.node3,
                                    "prev":self.node2.name}}
        path = Edge.get_shortest_path(graph, self.node1, self.node3)
        self.assertEqual(path, "%s, %s, %s" %(self.node1.name, self.node2.name, self.node3.name))