from django.urls import path
from .views import GreenUserCreate, LoginGreenUser, LogoutGreenUser, VerifyEmailGreenUser


app_name = 'person'

urlpatterns = [
    path('register/', GreenUserCreate.as_view(), name="create_green_user"),
    path('emailverify/', VerifyEmailGreenUser.as_view(), name="email-verify"),
    path('login/', LoginGreenUser.as_view(), name="login_green_user"),
    path('logout/', LogoutGreenUser.as_view(), name="logout_green_user")
]
