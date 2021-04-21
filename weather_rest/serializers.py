from rest_framework import serializers


class CitySerializer(serializers.Serializer):
    city = serializers.CharField()
