from django.urls import path
from .views import PackageGreenCreate

app_name = 'supplier'

urlpatterns = [
    path('create-package/', PackageGreenCreate.as_view(), name="supplier_create_package"),
]