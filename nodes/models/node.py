from django.db import models
from django.db.models import Q


class Node(models.Model):
    name = models.CharField(max_length=5)
    is_visited = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_neighbors(self):
        from .edge import Edge
        """
            Get all neighbors of a given node
            Returns:
                neighbors: list of node objects
        """
        neighbors = []
        edges = Edge.objects.filter(Q(node_from=self) | Q(
            node_to=self)).select_related("node_from", "node_to")
        for edge in edges:
            if edge.node_from != self:
                neighbors.append(edge.node_from)
                continue
            neighbors.append(edge.node_to)
        return neighbors
