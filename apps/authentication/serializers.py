from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=11)
    password = serializers.CharField(max_length=16)
