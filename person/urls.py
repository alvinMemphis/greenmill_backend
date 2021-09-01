from django.urls import path
from .views import GreenUserCreate, LoginGreenUser, LogoutGreenUser, VerifyEmailGreenUser, RequestPasswordResetEmail, PasswordTokenCheckAPI, SetNewPasswordAPIView


app_name = 'person'

urlpatterns = [
#     path('register/', GreenUserCreate.as_view(), name="create_green_user"),
    path('emailverify/', VerifyEmailGreenUser.as_view(), name="email-verify"),
    path('login/', LoginGreenUser.as_view(), name="login_green_user"),
    path('logout/', LogoutGreenUser.as_view(), name="logout_green_user"),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),
]
