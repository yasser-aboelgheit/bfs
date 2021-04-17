from django.db import models
from nodes.models.node import Node


class Edge(models.Model):
    node_from = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="node_from")
    node_to = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="node_to")

    class Meta:
        unique_together = ('node_from', 'node_to')

    @staticmethod
    def bfs(src, dest):
        """
        get graph of nodes
        get graph, by adding to queue all nodes and it's prev node
        return index of last node
        TODO lma aro7 n3mel el queue dictonary we ne return true ao false
        """
        
        visited = []
        queue = {src.name: {"node": src,
                            "prev": src}}
        graph = queue.copy()
        while queue:
            current_node = list(queue.keys())[0]
            visited.append(current_node)
            node = queue[current_node]["node"]
            neighbors = node.get_neighbors()
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue[neighbor] = {"node": Node.objects.get(name=neighbor),
                                        "prev": current_node}
                    graph[neighbor] = {"node": Node.objects.get(name=neighbor),
                                        "prev": current_node}
            if current_node == dest.name:
                return graph
            queue.pop(current_node)
        return False

    @staticmethod
    def get_shortest_path(graph, src, dest):
        last_node = dest.name
        path = [last_node]
        prev = last_node
        while prev != src.name:
            prev = graph[last_node]["prev"]
            path.append(prev)
            last_node = prev
        path.reverse()
        return ', '.join(path)
