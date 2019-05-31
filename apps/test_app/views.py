from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from utils.base import BaseView


class NoAuthTestView(BaseView):
    _ignore_model_permissions = True

    def get(self, request):
        return JsonResponse({'msg': 'A view not need auth!'})


class NeedAuthTestView(BaseView):

    def get(self, request):
        return JsonResponse({'msg': 'Verifed!'})
