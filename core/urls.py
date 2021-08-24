from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # login or logout of api
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # access and refresh token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # green user api / person
    path('api/person/', include('person.urls', namespace='person')),

    # superuser admin access
    path('admin/', admin.site.urls),
]
