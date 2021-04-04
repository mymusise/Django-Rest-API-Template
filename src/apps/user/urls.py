from django.urls import path

from . import views

urlpatterns = [
    path('', views.UserView.as_view({'get': 'list', 'post': 'create'})),
    path('<int:pk>', views.UserView.as_view({'get': 'retrieve', 'put': 'update'})),
    path('tokens', views.TokenView.as_view()),
    path('sign_in/sms', views.SMSLoginView.as_view()),
]
