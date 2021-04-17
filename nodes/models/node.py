from django.db import models


class Node(models.Model):
    name = models.CharField(max_length=5)
    is_visited = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    # __create__
    # def __init__(self, n):
    #     self.name = n
    #     self.neighbors = list()
        
    #     self.distance = 9999
    #     self.color = 'black'
    
    # def add_neighbor(self, v):
    #     if v not in self.neighbors:
    #         self.neighbors.append(v)
    #         self.neighbors.sort()