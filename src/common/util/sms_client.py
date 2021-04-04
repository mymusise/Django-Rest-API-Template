from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
import os


class SmsClient:
    def __init__(self, access_key, access_key_secret):
        self.access_key = access_key
        self.access_key_secret = access_key_secret

        self._client = self.create_client(access_key, access_key_secret)

    @staticmethod
    def create_client(access_key_id, access_key_secret):
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config()
        # 您的AccessKey ID
        config.access_key_id = access_key_id
        # 您的AccessKey Secret
        config.access_key_secret = access_key_secret
        # 访问的域名
        config.endpoint = "dysmsapi.aliyuncs.com"
        return Dysmsapi20170525Client(config)

    def send(self, phone_num, code, param):
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers=phone_num,
            sign_name=os.environ.get("ALIYUN_SMS_SIGN_NAME", ""),
            template_code=code,
            template_param=param,
        )
        self._client.send_sms(send_sms_request)
