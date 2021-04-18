import factory
from faker import Factory
from .models import Edge, Node
faker = Factory.create()


class NodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Node
    name = factory.Faker('text')


class EdgeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Edge
    node_from = factory.SubFactory(NodeFactory)
    node_to = factory.SubFactory(NodeFactory)