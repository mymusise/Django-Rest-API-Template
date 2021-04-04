from django.urls import path

from .views import SendSMSView

urlpatterns = [
    path('', SendSMSView.as_view()),
]
