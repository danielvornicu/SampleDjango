# serializers.py

#Import the REST Framework serializer
from rest_framework import serializers

from .models import Client

#Create a new class that links the Hero with its serializer
class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = ('nom', 'prenom')