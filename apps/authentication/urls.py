from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^login', views.LoginView.as_view()),
    url(r'^regist', views.RegistView.as_view()),
]
