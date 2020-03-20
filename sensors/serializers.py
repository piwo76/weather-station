from rest_framework import serializers

from .models import DHT22

class DHT22Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DHT22
        fields = '__all__'