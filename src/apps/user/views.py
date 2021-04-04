from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters import FilterSet, CharFilter
from .models import User, ROLES
from .serializers import UserSerializer, TokenResponseSerializer, SMSLoginSerializer
from ..base import NoPaginationViewSet
from ..sms.models import SMS
from server.exception import ObjectNotFoundException


class TokenView(ObtainAuthToken):

    @swagger_auto_schema(operation_description='登录获取Token',
                         responses={
                             201: openapi.Response("返回用户Token, ID, 以及其权限: ", TokenResponseSerializer
                                                   )
                         })
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'user_id': user.pk,
            'roles': user.roles
        })


class UserFilter(FilterSet):
    role = CharFilter(required=False, method='role_filter', label='role')

    class Meta:
        model = User
        fields = ['id', 'username', 'role']

    def role_filter(self, queryset, name, value):
        if value == ROLES.TEACHER:
            return queryset.filter(groups__name__in=[ROLES.TEACHER])
        else:
            return queryset.filter(groups__name__in=[ROLES.ASSISTANT])


class UserView(NoPaginationViewSet):
    serializer_class = UserSerializer
    filterset_class = UserFilter

    queryset = User.objects.all()

    def perform_create(self, serializer):
        serializer.save()
        user_id = serializer.data.get('id')
        user = User.objects.get(id=user_id)
        user.set_password(user.telephone)
        user.save(update_fields=['password'])


class SMSLoginView(APIView):
    serializer_class = SMSLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        phone_num = serializer.validated_data['phone_num']
        code = serializer.validated_data['code']

        sms = SMS.objects.filter(
            phone_num=phone_num, code=code, purpose=SMS.Purpose.SIGN_IN).first()

        if sms is None:
            raise ObjectNotFoundException("验证码错误")

        if sms.is_used:
            raise ObjectNotFoundException("验证码已失效")

        sms.set_used()
        user, _ = User.objects.get_or_create(telephone=phone_num)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username,
            'user_id': user.pk,
            'roles': user.roles
        })
