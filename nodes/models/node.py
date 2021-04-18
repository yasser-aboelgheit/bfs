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
            Args:
                src: String represents name of the Node
            Returns:
                neighbors: list of strings, each represents node name
        """
        neighbors = set()
        edges = Edge.objects.filter(Q(node_from=self) | Q(node_to=self)).\
            values_list('node_from__name', 'node_to__name')
        for edge in edges:
            neighbors.update([edge[0], edge[1]])
        return neighbors
