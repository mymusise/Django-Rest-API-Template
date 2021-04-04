from rest_framework import serializers
from .models import User, ROLES


class TokenResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    user_id = serializers.CharField()
    roles = serializers.ListField(serializers.CharField())


class UserSerializer(serializers.ModelSerializer):
    telephone = serializers.CharField(min_length=11, max_length=11)
    role = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'telephone', 'remark', 'date_joined', 'role')

    def create(self, validated_data):
        role = validated_data.pop('role') if 'role' in validated_data else None
        instance = super(UserSerializer, self).create(validated_data)
        if role == ROLES.TEACHER:
            instance.being_teacher()
        else:
            instance.being_assistant()
        return instance


class SMSLoginSerializer(serializers.Serializer):
    phone_num = serializers.CharField(max_length=32)
    code = serializers.CharField(max_length=12)
