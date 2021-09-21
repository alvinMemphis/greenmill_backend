from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from person.AuthToken import MyTokenObtainPairView
schema_view = get_schema_view(
    openapi.Info(
        title="Green Mile API",
        default_version='1.0.0',
        description="API for Green Mile",
        terms_of_service="none",
        contact=openapi.Contact(email="contact@alvin.mercy.johnspeny"),
        license=openapi.License(name="Green Mile License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # login or logout of api
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # access and refresh token
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', MyTokenObtainPairView.as_view(), name='token_refresh'),

    # green user api / person
    path('api/person/', include('person.urls', namespace='person')),

    # green supplier api
    path('api/supplier/', include('supplier.urls', namespace='supplier')),
    
    # green admin api
    path('api/greenadmin/', include('greenadmin.urls', namespace='greenadmin')),

    # green admin api
    path('api/hubmanager/', include('hubmanager.urls', namespace='greenmanager')),
    
    # api documentation
    path('docs/', include_docs_urls(title='Green Mile API')),
    path('', schema_view.with_ui('swagger',
                                 cache_timeout=0), name='schema-swagger-ui'),
    path('api/api.json/', schema_view.without_ui(cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
                                       cache_timeout=0), name='schema-redoc'),

    # superuser admin access
    path('admin/', admin.site.urls),
]
