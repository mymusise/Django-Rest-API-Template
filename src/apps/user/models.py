from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group


class ROLES:
    MANAGER = "manager"


class UserInfoMixin(models.Model):
    telephone = models.CharField(max_length=64, verbose_name="手机号", unique=True)
    remark = models.CharField(null=True, blank=True, max_length=255, verbose_name="备注")

    class Meta:
        abstract = True


class User(AbstractUser, UserInfoMixin):
    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    @property
    def roles(self):
        if hasattr(self, "_roles"):
            return self._roles
        names = self.groups.all().values_list("name")
        names = list(map(lambda x: x[0], names))
        self._roles = names
        return self._roles

    @property
    def is_manager(self):
        # TODO: 新增第三中管理员身份时候这块需要修改
        return ROLES.MANAGER in self.roles
