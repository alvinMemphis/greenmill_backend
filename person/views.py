from rest_framework import views
from .serializers import RegisterGreenUserSerializer, LoginGreenUserSerializer, LogoutGreenUserSerializer, EmailVerifyGreenUserSerializer, SetNewPasswordSerializer, ResetPasswordEmailRequestSerializer
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
import jwt
from django.conf import settings
from . models import GreenUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
import os
from django.http import HttpResponsePermanentRedirect

# Create your views here.

class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


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
        # acc_token = RefreshToken.for_user(user)

        # 2. get current domain
        current_site =  get_current_site(request).domain

        # 3. reverse email
        relativeLink = reverse('person:email-verify')

        absurl = 'http://'+ current_site+relativeLink+"?token="+str(acc_token)
        
        email_body = 'Hi '+ user.user_name + \
            ' Use the link below to verify your email \n' + absurl
        
    

        # send mail
        # message = render_to_string('person/acc_active_email.html', {
        #     'username': user.user_name,
        #     'user': user.email,
        #     'domain': current_site,
        #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #     'token': str(acc_token),
        #     'current_site': current_site,
        #     'relative_link': relativeLink,
        # })
        send_mail('Verification Message',
                    absurl,
                    'okkerjohn@gmail.com',
                    [str(user.email)],
                    fail_silently=False)
                    # fail_silently=False, html_message=message)


        # if reg_serializer.is_valid():
        #     newuser = reg_serializer.save()
        #     if newuser:
        #         return Response(status=status.HTTP_201_CREATED)
        return Response(user_data, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailGreenUser(views.APIView):
    serializer_class = EmailVerifyGreenUserSerializer

    def get(self, request):
        # get incoming token eg from mail sent
        token = request.GET.get('token')
        # payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        # print('payload 0' + str(settings.SECRET_KEY))
        # print('payload 1' + str(payload))
        try:
            # never you forget to add an algorithm
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = GreenUser.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            verify_message = {
                'email': 'Successfully verified, login to continue'
            }
            return Response(verify_message, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            verify_message = {
                'error': 'Activation Expired'
            }
            return Response(verify_message, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            verify_message = {
                'error': 'Invalid token'
            }
            return Response(verify_message, status=status.HTTP_400_BAD_REQUEST)


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


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if GreenUser.objects.filter(email=email).exists():
            user = GreenUser.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'person:password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl+"?redirect_url="+redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            send_mail('Verification Message',
                    email_body,
                    'okkerjohn@gmail.com',
                    [str(user.email)],
                    fail_silently=False)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = GreenUser.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url+'?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url+'?token_valid=False')
                    
            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)



class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)