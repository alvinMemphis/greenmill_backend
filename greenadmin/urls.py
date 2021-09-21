from django.urls import path
from .views import GreenAdminCreateSupplier, LogicHubCreate, UpdateLogicHub
from hubmanager.views import GreenAdminCreateManager


app_name = 'greenadmin'

urlpatterns = [
    path('register/supplier', GreenAdminCreateSupplier.as_view(), name="create_green_supplier"),
    path('register/hubmanager', GreenAdminCreateManager.as_view(), name="create_hubmanager"),
    path('register/logichub', LogicHubCreate.as_view(), name="create_logichub"),
    path('update/logichub', UpdateLogicHub.as_view(), name="update_logichub"),
]
