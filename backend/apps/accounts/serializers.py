from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')
        read_only_fields = fields


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
    )

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'password_confirm',
            'first_name',
            'last_name',
        )

    def validate_email(self, value):
        normalized_email = value.strip().lower()
        if User.objects.filter(email__iexact=normalized_email).exists():
            raise serializers.ValidationError(
                'A user with this email already exists.'
            )
        return normalized_email

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm', None)

        if password != password_confirm:
            raise serializers.ValidationError(
                {'password_confirm': 'Passwords do not match.'}
            )

        validate_password(password)
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        return User.objects.create_user(password=password, **validated_data)


class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
    )

    def validate(self, attrs):
        attrs['email'] = attrs['email'].strip().lower()
        return super().validate(attrs)


class RefreshTokenSerializer(TokenRefreshSerializer):
    pass


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True, required=True)
