from rest_framework import serializers, fields
from .models import GreenUser
from supplier.models import Supplier
from hubmanager.models import HubManager, LogicHub
from loader.models import HubLoader
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from greenadmin.models import GreenAdmin


class RegisterGreenUserSerializer(serializers.ModelSerializer):
    user_type = fields.ChoiceField(GreenUser.USER_TYPE_CHOICES)
    password = serializers.CharField(
        write_only=True,
        required=False,
    )

    hub = serializers.PrimaryKeyRelatedField(
        queryset=LogicHub.objects.all(),
        required=False, 
        allow_null=True, 
        default=None
    )
    
    class Meta:
        model = GreenUser
        fields = ('email', 'user_name', 'password', 'user_type','hub')
        # extra_fields = {'password': {'write_only': True}}



 
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        user_type = validated_data.pop('user_type', None)
        hub = validated_data.pop('hub', None)

        if password is not None and user_type in ['admin']:
            instance.set_password(password)

        if password is None and user_type in ['loader', 'supplier', 'manager']:
            default_pass = GreenUser.objects.make_random_password()
            # instance.set_password(default_pass)
            instance.set_password(str(default_pass))
            # print(user_type)
            print(default_pass)
        instance.save()

        # user type reg
        usert = None
        print(user_type)
        if user_type == 'admin':
            usert = GreenAdmin(user=instance)
            usert.save()
        if user_type == 'supplier':
            request = self.context.get("request").user
            current = GreenAdmin.objects.get(user=request)
            # print(current)
            # r = serializers.CurrentUserDefault()
            usert = Supplier(person=instance, admin=current)
            usert.save()
        if user_type == 'manager':
            request = self.context.get("request").user
            # print(request)
            current = GreenAdmin.objects.get(user=request)
            # print(current)
            # r = serializers.CurrentUserDefault()
            usert = HubManager(user=instance, admin=current)
            usert.save()

        if user_type == 'loader':
            request = self.context.get("request").user
            # print(request)
            current = HubManager.objects.get(user=request)
            # print(current)
            # r = serializers.CurrentUserDefault()
            usert = HubLoader(user=instance, manager=current, his_hub=hub)
            usert.save()
        return instance


class EmailVerifyGreenUserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = GreenUser
        fields = ['token']


# class LoginGreenUserSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(max_length=255, min_length=3)
#     password = serializers.CharField(
#         max_length=68, min_length=6, write_only=True)
#     tokens = serializers.SerializerMethodField()

#     # just to help know what token is associated with what user
#     def get_tokens(self, incoming_data):
#         user = GreenUser.objects.get(email=incoming_data['email'])
#         return {
#             'refresh_token': user.tokens()['refresh'],
#             'access_token': user.tokens()['access']
#         }

#     class Meta:
#         model = GreenUser
#         fields = ('email', 'password', 'tokens')
#         extra_fields = {'password': {'write_only': True}}


#     def validate(self, attrs):
#         email = attrs.get('email', '')
#         password = attrs.get('password', '')
#         get_user = GreenUser.objects.filter(email=email)
#         user = auth.authenticate(password=password, username=email)

#         if  get_user.exists() and get_user[0].is_verified != True:
#             raise AuthenticationFailed('Verify your account to proceed.')

#         if not user:
#             raise AuthenticationFailed('Invalid credentials, try again')

#         if not user.is_active:
#             raise AuthenticationFailed('Account disabled, contact admin')

#         return {
#             'email': user.email,
#             'username': user.user_name,
#             'tokens': user.tokens
#         }


class LogoutGreenUserSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            # store it in blacklist table
            RefreshToken(self.token).blacklist()
        except TokenError:
            # get error from error message dic
            self.fail('bad_token')




class LoginGreenUserSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(
        max_length="100", read_only=True)
    tokens = serializers.SerializerMethodField()

    # just to help know what token is associated with what user
    def get_tokens(self, incoming_data):
        user = GreenUser.objects.get(email=incoming_data['email'])
        return {
            'refresh_token': user.tokens()['refresh'],
            'access_token': user.tokens()['access']
        }

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        # get_user = GreenUser.objects.filter(email=email)
        user = auth.authenticate(password=password, username=email)
        # print(user.user_name)
        # if  get_user.exists() and get_user[0].is_verified != True:
        #     raise AuthenticationFailed('Verify your account to proceed.')

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')

        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')

        # return attrs
        return {
            'email': user.email,
            'username': user.user_name,
            'tokens': user.tokens
        }


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = GreenUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)

        