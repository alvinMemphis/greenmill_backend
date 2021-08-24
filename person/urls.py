from django.urls import path
from .views import GreenUserCreate, BlacklistTokenView


app_name = 'person'

urlpatterns = [
    path('register/', GreenUserCreate.as_view(), name="create_green_user"),
    path('logout/', BlacklistTokenView.as_view(), name="blacklist")
]
