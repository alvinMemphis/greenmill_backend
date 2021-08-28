from django.urls import path
from .views import GreenAdminCreateManager


app_name = 'hubmanager'

urlpatterns = [
    path('register/hubmanager', GreenAdminCreateManager.as_view(), name="create_hubmanager"),
]
