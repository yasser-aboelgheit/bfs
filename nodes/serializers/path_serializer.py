from rest_framework import serializers
from nodes.models import Node, Edge


class PathSerializer(serializers.Serializer):
    node_from = serializers.CharField(required=True)
    node_to = serializers.CharField(required=True)

    def validate_node_from(self, value):
        
        node_from = Node.objects.filter(name=value).last()
        if not node_from:
            raise serializers.ValidationError('No Node with the name %s exists' % value)
        return node_from
        
    def validate_node_to(self, value):
        node_to = Node.objects.filter(name=value).last()
        if not node_to:
            raise serializers.ValidationError('No Node with the name %s exists' % value)
        return node_to
