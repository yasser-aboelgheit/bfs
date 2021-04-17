from rest_framework.response import Response
from rest_framework import generics
from .models import Node, Edge
from .serializers import EdgeSerializer, PathSerializer
from rest_framework.views import APIView
from django.db.models import Q


class RegisterNodeViewSet(generics.CreateAPIView):

    def create(self, *args, **kwargs):
        serializer = EdgeSerializer(data=self.request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, 400)
        try:
            Edge.objects.create(**serializer.validated_data)
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                return Response({"message": "This Edge is already existed"}, status=400)
            return Response({"message": str(e)}, status=400)

        return Response({"message": "Node added successfully"}, status=201)


class DisplayNodeViewSet(APIView):

    def get(self, request, format=None):
        serializer = PathSerializer(data=self.request.GET)
        if not serializer.is_valid():
            return Response(serializer.errors, 400)
        src = serializer.validated_data.get("node_from")
        dest = serializer.validated_data.get("node_to")
        graph = Edge.bfs(src, dest)

        #Check if Nodes are not connected
        if not graph:
            return Response({"message": "No path found"}, status=400)
        # GET SHORTEST PATH, GO THROUGH ALL OLD NODES
        shortest_path = Edge.get_shortest_path(graph, src, dest)
        return Response({"path": shortest_path}, status=200)

