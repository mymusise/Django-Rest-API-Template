from django.contrib import admin
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/sms/', include('apps.sms.urls')),
    path('api/v1/user/', include('apps.user.urls')),
]

swagger_info = openapi.Info(
    title="A simple template of django rest api",
    default_version='v1',
    description="""I'm description.""",
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="your@company.local"),
    license=openapi.License(name="BSD License"),
)

SchemaView = get_schema_view(
    validators=['ssv', 'flex'],
    public=True,
    permission_classes=[],
)
