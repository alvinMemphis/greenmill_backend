from django.urls import path,include
from .views import PackageGreenCreate, PackageGreenUpdate,SupplierViewSet
from rest_framework import routers
app_name = 'supplier'
router = routers.DefaultRouter()
router.register(r'', SupplierViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('create-package/', PackageGreenCreate.as_view(), name="supplier_create_package"),
    path('update-package/', PackageGreenUpdate.as_view(), name="supplier_update_package"),
]
