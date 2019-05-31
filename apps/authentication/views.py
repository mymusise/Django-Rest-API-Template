from django.shortcuts import render
from rest_framework_jwt.serializers import (
    jwt_encode_handler,
    jwt_payload_handler
)
from ratelimit.mixins import RatelimitMixin
from utils.base import BaseView
from apps.authentication.models import User
from . import serializers


class LoginView(RatelimitMixin, BaseView):
    _ignore_model_permissions = True
    input_serializer = {
        'POST': serializers.LoginSerializer
    }
    ratelimit_key = 'ip'
    ratelimit_rate = '100/m'
    ratelimit_block = True
    ratelimit_method = 'POST'

    def check_login_time(self, data):
        pass

    def post(self, request, *args, **kwargs):
        data = request.serializer.data
        user = User.objects.filter(username=data.get('username'), is_active=True).first()
        if not user:
            return self.object_not_exit(msg='用户不存在')
        if not user.check_password(data.get('password')):
            return self.object_not_exit(msg='密码不正确')

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        return self.success(data={
            'token': token,
            'username': user.username,
            'role': '',
        })


class RegistView(BaseView):

    def post(self, request):
        return self.success({})