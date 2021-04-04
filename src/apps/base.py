import datetime
from django.contrib.admin import ModelAdmin
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.inspectors.view import SwaggerAutoSchema
from rest_framework import filters
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import CharField, DecimalField
from server.logger_middleware import APILogMiddleware


class AmountCentField(DecimalField):
    def to_representation(self, value):
        value = super(AmountCentField, self).to_representation(value)
        return value / 100

    def to_internal_value(self, data):
        data = super(AmountCentField, self).to_internal_value(data)
        return data * 100


class LogicDeleteMixin(object):
    is_deleted = None
    deleted_at = None

    def save(self, *args, **kwargs):
        pass

    def logic_delete(self):
        self.is_deleted = True
        self.deleted_at = datetime.datetime.now()
        self.save(update_fields=['is_deleted', 'deleted_at'])

    def logic_restore(self):
        self.is_deleted = False
        self.save(update_fields=['is_deleted'])


class NoDeleteModalAdmin(ModelAdmin):

    def has_delete_permission(self, request, *args, **kwargs):
        return False


class PagePagination(PageNumberPagination):
    page_size = 20


class FullDjangoModelPermissions(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class BaseModelViewSet(ModelViewSet):
    pagination_class = PagePagination
    swagger_schema = SwaggerAutoSchema
    filter_backends = [filters.SearchFilter,
                       DjangoFilterBackend, filters.OrderingFilter]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated,
                          FullDjangoModelPermissions]

    def perform_destroy(self, instance):
        if getattr(instance, 'logic_delete'):
            instance.logic_delete()

    def initialize_request(self, request, *args, **kwargs):
        request = super(BaseModelViewSet, self).initialize_request(
            request, *args, **kwargs)
        APILogMiddleware.log_request(request)
        return request


class NoPagePagination(PagePagination):

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        self.page = self.django_paginator_class([], 1).page(1)
        self.page.paginator.count = queryset.count()
        queryset.page = 1
        return queryset


class NoPaginationViewSet(ModelViewSet):
    pagination_class = NoPagePagination

