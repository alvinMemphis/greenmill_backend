from django.urls import path
from .views import PackageGreenCreate, PackageGreenUpdate

app_name = 'supplier'

urlpatterns = [
    path('create-package/', PackageGreenCreate.as_view(), name="supplier_create_package"),
    path('update-package/', PackageGreenUpdate.as_view(), name="supplier_update_package"),
]