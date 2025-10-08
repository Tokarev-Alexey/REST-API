from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="A NEW BEGINING REST-API",
      default_version='v1',
      description="Образовательный проект REST-API для презентации.",
   ),
   public=True,
   permission_classes=[permissions.AllowAny,]
)