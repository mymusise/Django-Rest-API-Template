from rest_framework import serializers


class SendSmsSerializer(serializers.Serializer):
    phone_num = serializers.CharField(required=True)
    purpose = serializers.CharField(required=True)
