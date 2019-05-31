from django.urls import path
from .views import NoAuthTestView, NeedAuthTestView


urlpatterns = [
    path('no_auth', NoAuthTestView.as_view()),
    path('need_auth', NeedAuthTestView.as_view()),
]
