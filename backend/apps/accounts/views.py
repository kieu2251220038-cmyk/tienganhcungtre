from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
	LoginSerializer,
	RefreshTokenSerializer,
	RegisterSerializer,
	LogoutSerializer,
	UserSerializer,
)


RegisterResponseSerializer = inline_serializer(
	name='RegisterResponse',
	fields={
		'success': serializers.BooleanField(),
		'message': serializers.CharField(),
		'data': inline_serializer(
			name='RegisterData',
			fields={'user': UserSerializer()},
		),
	},
)

LoginResponseSerializer = inline_serializer(
	name='LoginResponse',
	fields={
		'success': serializers.BooleanField(),
		'message': serializers.CharField(),
		'data': inline_serializer(
			name='LoginData',
			fields={
				'access': serializers.CharField(),
				'refresh': serializers.CharField(),
				'user': UserSerializer(),
			},
		),
	},
)

RefreshResponseSerializer = inline_serializer(
	name='RefreshResponse',
	fields={
		'success': serializers.BooleanField(),
		'message': serializers.CharField(),
		'data': inline_serializer(
			name='RefreshData',
			fields={'access': serializers.CharField()},
		),
	},
)

CurrentUserResponseSerializer = inline_serializer(
	name='CurrentUserResponse',
	fields={
		'success': serializers.BooleanField(),
		'message': serializers.CharField(),
		'data': UserSerializer(),
	},
)

LogoutResponseSerializer = inline_serializer(
	name='LogoutResponse',
	fields={
		'success': serializers.BooleanField(),
		'message': serializers.CharField(),
		'data': serializers.JSONField(allow_null=True),
	},
)


class RegisterView(APIView):
	permission_classes = (AllowAny,)

	@extend_schema(
		request=RegisterSerializer,
		responses={status.HTTP_201_CREATED: RegisterResponseSerializer},
	)
	def post(self, request):
		serializer = RegisterSerializer(data=request.data)
		if not serializer.is_valid():
			return Response(
				{
					'success': False,
					'message': 'Registration validation failed',
					'errors': serializer.errors,
				},
				status=status.HTTP_400_BAD_REQUEST,
			)

		user = serializer.save()
		return Response(
			{
				'success': True,
				'message': 'Registration successful',
				'data': {
					'user': UserSerializer(user).data,
				},
			},
			status=status.HTTP_201_CREATED,
		)


class LoginView(APIView):
	permission_classes = (AllowAny,)

	@extend_schema(
		request=LoginSerializer,
		responses={status.HTTP_200_OK: LoginResponseSerializer},
	)
	def post(self, request):
		serializer = LoginSerializer(data=request.data)
		try:
			serializer.is_valid(raise_exception=True)
		except AuthenticationFailed as exc:
			return Response(
				{
					'success': False,
					'message': 'Invalid email or password',
					'errors': {'non_field_errors': [str(exc.detail)]},
				},
				status=status.HTTP_401_UNAUTHORIZED,
			)
		except serializers.ValidationError as exc:
			return Response(
				{
					'success': False,
					'message': 'Login validation failed',
					'errors': exc.detail,
				},
				status=status.HTTP_400_BAD_REQUEST,
			)

		return Response(
			{
				'success': True,
				'message': 'Login successful',
				'data': {
					'access': serializer.validated_data['access'],
					'refresh': serializer.validated_data['refresh'],
					'user': UserSerializer(serializer.user).data,
				},
			},
			status=status.HTTP_200_OK,
		)


class RefreshTokenView(APIView):
	permission_classes = (AllowAny,)

	@extend_schema(
		request=RefreshTokenSerializer,
		responses={status.HTTP_200_OK: RefreshResponseSerializer},
	)
	def post(self, request):
		serializer = RefreshTokenSerializer(data=request.data)
		try:
			serializer.is_valid(raise_exception=True)
		except (TokenError, AuthenticationFailed) as exc:
			return Response(
				{
					'success': False,
					'message': 'Refresh token is invalid or expired',
					'errors': {'refresh': [str(exc)]},
				},
				status=status.HTTP_401_UNAUTHORIZED,
			)
		except serializers.ValidationError as exc:
			return Response(
				{
					'success': False,
					'message': 'Refresh token validation failed',
					'errors': exc.detail,
				},
				status=status.HTTP_400_BAD_REQUEST,
			)

		return Response(
			{
				'success': True,
				'message': 'Token refreshed successfully',
				'data': {
					'access': serializer.validated_data['access'],
				},
			},
			status=status.HTTP_200_OK,
		)


class CurrentUserView(APIView):
	permission_classes = (IsAuthenticated,)

	@extend_schema(responses={status.HTTP_200_OK: CurrentUserResponseSerializer})
	def get(self, request):
		return Response(
			{
				'success': True,
				'message': 'User retrieved successfully',
				'data': UserSerializer(request.user).data,
			},
			status=status.HTTP_200_OK,
		)


class LogoutView(APIView):
	permission_classes = (AllowAny,)

	@extend_schema(
		request=LogoutSerializer,
		responses={status.HTTP_200_OK: LogoutResponseSerializer},
	)
	def post(self, request):
		serializer = LogoutSerializer(data=request.data)
		if not serializer.is_valid():
			return Response(
				{
					'success': False,
					'message': 'Logout validation failed',
					'errors': serializer.errors,
				},
				status=status.HTTP_400_BAD_REQUEST,
			)

		try:
			refresh_token = RefreshToken(serializer.validated_data['refresh'])
			refresh_token.blacklist()
		except TokenError as exc:
			return Response(
				{
					'success': False,
					'message': 'Refresh token is invalid or expired',
					'errors': {'refresh': [str(exc)]},
				},
				status=status.HTTP_401_UNAUTHORIZED,
			)

		return Response(
			{
				'success': True,
				'message': 'Logout successful',
				'data': None,
			},
			status=status.HTTP_200_OK,
		)
