from django.urls import path
from .views import GreenAdminCreateSupplier


app_name = 'greenadmin'

urlpatterns = [
    path('register/supplier', GreenAdminCreateSupplier.as_view(), name="create_green_supplier"),
]
