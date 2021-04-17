from django.db import models
from nodes.models.node import Node


class Edge(models.Model):
    node_from = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="node_from")
    node_to = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="node_to")

    class Meta:
        unique_together = ('node_from', 'node_to')
