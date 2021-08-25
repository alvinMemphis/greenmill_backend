from rest_framework import serializers
from .models import GreenUser
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class RegisterGreenUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GreenUser
        fields = ('email', 'user_name', 'password')
        extra_fields = {'password': {'write_only': True}}
 
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class EmailVerifyGreenUserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = GreenUser
        fields = ['token']


class LoginGreenUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField()

    # just to help know what token is associated with what user
    def get_tokens(self, incoming_data):
        user = GreenUser.objects.get(email=incoming_data['email'])
        return {
            'refresh_token': user.tokens()['refresh'],
            'access_token': user.tokens()['access']
        }

    class Meta:
        model = GreenUser
        fields = ('email', 'password', 'tokens')
        extra_fields = {'password': {'write_only': True}}


    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        get_user = GreenUser.objects.filter(email=email)
        user = auth.authenticate(password=password, username=email)

        if  get_user.exists() and get_user[0].is_verified != True:
            raise AuthenticationFailed('Verify your account to proceed.')

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')

        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')

        return {
            'email': user.email,
            'username': user.user_name,
            'tokens': user.tokens
        }


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


