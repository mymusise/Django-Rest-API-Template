import json
import os

from django.conf import settings
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from common.util.sms_client import SmsClient
from server.exception import BizException
from .models import SMS
from .serializers import SendSmsSerializer


class SendSMSView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SendSmsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_num = serializer.validated_data['phone_num']
        purpose = serializer.validated_data['purpose']

        if purpose not in (SMS.Purpose.all()):
            raise APIException('非法操作')

        elif purpose == SMS.Purpose.SIGN_IN:
            pass

        try:
            sms = SMS.create(phone_num=phone_num, purpose=purpose)
        except SMS.IntervalTooShortException:
            raise BizException('请稍后再试', 'SMS.IntervalTooShort')

        sms_client = SmsClient(
            os.environ.get('ALIYUN_SMS_ACCESS_KEY', ''),
            os.environ.get('ALIYUN_SMS_ACCESS_KEY_SECRET', ''),
        )

        param = json.dumps({"code": sms.code})
        sms_client.send(phone_num, 'SMS_101195030', param)

        return Response({})
