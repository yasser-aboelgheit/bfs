from rest_framework.response import Response
from rest_framework import generics
from .models import Node, Edge
from .serializers import EdgeSerializer
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.db.models import Q
import sys
# TODO (sys.setrecursionlimit(2000)) sys.getrecursionlimit()


class RegisterNodeViewSet(generics.CreateAPIView):
    # serializer_class = PassengerRegisterSerializer
    # connectNode/
    def create(self, *args, **kwargs):
        serializer = EdgeSerializer(data=self.request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, 400)
        try:
            Edge.objects.create(**serializer.validated_data)
        except Exception as e:
            # import ipdb;ipdb.set_trace()
            if "UNIQUE constraint failed" in str(e):
                return Response({"message": "This Edge is already existed"}, status=400)
            return Response({"message": str(e)}, status=400)
        return Response({"message": "Node added successfully"}, status=201)


# path?from=A&to=C
class DisplayNodeViewSet(APIView):

    def get(self, request, format=None):
        src = self.request.GET["from"]
        dest = self.request.GET["to"]
        start = Node.objects.get(name=src)
        queue = {src: src}
        visited = []
        
        def get_neighbors(src):
            node = Node.objects.get(name=src)
            neighbors = set()
            edges = Edge.objects.filter(Q(node_from=node) | Q(node_to=node)).values_list('node_from__name', 'node_to__name')
            for edge in edges:
                neighbors.update([edge[0], edge[1]])
            return neighbors

        def bfs():
            """
            get graph, by adding to queue all nodes and it's prev node
            return index of last node
            TODO lma aro7 n3mel el queue dictonary we ne return true ao false
            """
            new_queue = queue.copy()
            while queue:
                src = list(queue.keys())[0]
                visited.append(src)
                neighbors = get_neighbors(src)
                for node in neighbors:
                    if node not in visited:
                        queue[node] = src
                        new_queue[node] = src
                if src == dest:
                    return new_queue
                queue.pop(src)
            return False
        graph = bfs()
        # print(graph)

        # #CHECK IF NOT THERE
        if not graph:
            return Response({"message": "No path found"}, status=400)
        # print(queue)
      
        # # GET PREV NODE
        def get_prev(node):
            return graph[node]

        # # GET SHORTEST PATH, GO THROUGH ALL OLD NODES
        def get_shortest_path(graph):
            last_node = dest
            path = [dest]
            prev = dest
            while prev != src:
                prev = get_prev(last_node)
                path.append(prev)
                last_node = prev
            path.reverse()
            return path
        shortest_path = get_shortest_path(graph)
        print(*shortest_path)
        # get_shortest_path(graph)
        return Response({"path": ', '.join(shortest_path)}, status=200)



# class DisplayNodeViewSet2(APIView):

#     def get(self, request, format=None):
#         src = self.request.GET["from"]
#         dest = self.request.GET["to"]
#         start = Node.objects.get(name=src)
#         queue = [(src, src)]
#         visited = []
        
#         def get_neighbors(src):
#             node = Node.objects.get(name=src)
#             neighbors = set()
#             edges = Edge.objects.filter(Q(node_from=node) | Q(node_to=node)).values_list('node_from__name', 'node_to__name')
#             for edge in edges:
#                 neighbors.update([edge[0], edge[1]])
#             return neighbors

#         def bfs():
#             """
#             get graph, by adding to queue all nodes and it's prev node
#             return index of last node
#             TODO lma aro7 n3mel el queue dictonary we ne return true ao false
#             """
#             for count, src in enumerate(queue):
#                 visited.append(src[0])
#                 neighbors = get_neighbors(src[0])
#                 for node in neighbors:
#                     if node not in visited:
#                         queue.append((node,src[0]))
#                 if src[0] == dest:
#                     return count
#             return False
#         dest_index = bfs()

#         # print(queue)
#         # #CHECK IF NOT THERE
#         if not dest_index:
#             return Response({"message": "No path found"}, status=400)
#         # print(queue)
      
#         # # GET PREV NODE
#         def get_prev(node):
#             return node[1]
        
#         # # GET SHORTEST PATH, GO THROUGH ALL OLD NODES
#         def get_shortest_path(queue):
#             last_node = queue[dest_index]
#             path = [last_node[0]]
#             prev = dest
#             while prev != src:
#                 prev = get_prev(last_node)
#                 path.append(prev)
#                 for count, i in enumerate(queue):
#                     if i[0] == prev:
#                         last_node = queue[count]
#                 # dest_index = prev[]
#             return path
#         print(get_shortest_path(queue))

#         return Response({"message": "Hello indeed"}, status=200)
