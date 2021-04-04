import datetime
import random

from django.db import models
from django.utils import timezone


class SMS(models.Model):
    id = models.AutoField(primary_key=True)
    phone_num = models.CharField(max_length=32)
    code = models.CharField(max_length=16)
    purpose = models.CharField(max_length=32)
    is_used = models.BooleanField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Purpose:
        UPDATE_PHONE_NUM = 'UPDATE_PHONE_NUM'
        REGISTER = 'REGISTER'
        SIGN_IN = 'SIGN_IN'

        @classmethod
        def all(cls):
            return cls.UPDATE_PHONE_NUM, cls.REGISTER, cls.SIGN_IN

    class IntervalTooShortException(Exception):
        pass

    @classmethod
    def create(cls, phone_num, purpose):
        code = ''.join(random.choices('0123456789', k=4))
        now = timezone.now()

        latest = cls.objects.filter(phone_num=phone_num).order_by(
            '-created_at').first()

        if latest:
            delta = now - latest.created_at
            if delta < datetime.timedelta(minutes=1):
                raise cls.IntervalTooShortException()

        obj = cls.objects.create(phone_num=phone_num,
                                 code=code,
                                 purpose=purpose,
                                 is_used=False,
                                 created_at=now,
                                 updated_at=now,
                                 )
        return obj

    @classmethod
    def load_latest(cls, phone_num, purpose):
        obj = cls.objects.filter(phone_num=phone_num, purpose=purpose).order_by(
            "-created_at").first()
        return obj

    def set_used(self):
        self.is_used = True
        self.updated_at = timezone.now()
        self.save(update_fields=['is_used', 'updated_at'])
