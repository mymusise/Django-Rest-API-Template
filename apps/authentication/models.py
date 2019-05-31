from datetime import datetime, timedelta
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    用户表，新增字段如下
    """
    nickname = models.CharField(max_length=30, null=True,
                                blank=True, verbose_name="姓名")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.username}: <{self.nickname}>"

    @property
    def roles(self):
        names = self.groups.all().values_list('name')
        names = list(map(lambda x: x[0], names))
        self._roles = names
        return self._roles
