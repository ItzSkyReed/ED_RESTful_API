from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1',
        description="Крутое описание",
        contact=openapi.Contact(email="contact"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],  # Разрешаем доступ без аутентификации
    authentication_classes=[SessionAuthentication, BasicAuthentication],  # Добавьте аутентификацию для Swagger
)