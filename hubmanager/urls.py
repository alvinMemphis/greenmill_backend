from django.urls import path
from .views import HubManagerCreateLoader

app_name = 'hubmanager'

urlpatterns = [
    # path('register/hubmanager', GreenAdminCreateManager.as_view(), name="create_hubmanager"),
    path('register/loader', HubManagerCreateLoader.as_view(), name="create_hubloader"),
]
