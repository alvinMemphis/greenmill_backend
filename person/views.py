from .serializers import RegisterGreenUserSerializer, LoginGreenUserSerializer, LogoutGreenUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string



from . models import GreenUser
# Create your views here.


class GreenUserCreate(generics.GenericAPIView):

    serializer_class = RegisterGreenUserSerializer

    def post(self, request):
        # save user in db
        reg_serializer = self.serializer_class(data=request.data)
        reg_serializer.is_valid(raise_exception=True)
        reg_serializer.save()

        # get serialized data
        user_data = reg_serializer.data

        # get user from db
        user =  GreenUser.objects.get(email=user_data['email'])

        # email verification setup
        # 1. get access token for user
        acc_token = RefreshToken.for_user(user).access_token

        # 2. get current domain
        current_site =  get_current_site(request).domain

        # 3. reverse email
        # relativeLink = reverse('email-verify')

        # absurl = 'http://'+ current_site+relativeLink+"?token="+str(acc_token)
        
        # email_body = 'Hi '+ user.user_name + \
        #     ' Use the link below to verify your email \n' + absurl
        
    

        # send mail
        message = render_to_string('person/acc_active_email.html', {
            'username': user.user_name,
            'user': user.email,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': str(acc_token)
        })
        send_mail('Verification Message',
                    message,
                    'okkerjohn@gmail.com',
                    [str(user.email)],
                    fail_silently=False, html_message=message)


        user_data = reg_serializer.data
        # if reg_serializer.is_valid():
        #     newuser = reg_serializer.save()
        #     if newuser:
        #         return Response(status=status.HTTP_201_CREATED)
        return Response(user_data, status=status.HTTP_400_BAD_REQUEST)


class LoginGreenUser(generics.GenericAPIView):
    serializer_class = LoginGreenUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutGreenUser(generics.GenericAPIView):
    serializer_class = LogoutGreenUserSerializer
    permission_class = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

