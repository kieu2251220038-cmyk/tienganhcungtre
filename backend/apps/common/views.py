from django.db import DatabaseError, connection
from rest_framework import status
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, inline_serializer


HealthResponseSerializer = inline_serializer(
	name='HealthResponse',
	fields={
		'success': serializers.BooleanField(),
		'message': serializers.CharField(),
		'data': inline_serializer(
			name='HealthData',
			fields={
				'service': serializers.CharField(),
				'version': serializers.CharField(),
			},
		),
	},
)

DatabaseHealthResponseSerializer = inline_serializer(
	name='DatabaseHealthResponse',
	fields={
		'success': serializers.BooleanField(),
		'message': serializers.CharField(),
		'data': inline_serializer(
			name='DatabaseHealthData',
			fields={
				'database': serializers.CharField(),
			},
		),
	},
)


@extend_schema(responses=HealthResponseSerializer)
@api_view(['GET'])
def health_check(request):
	return Response(
		{
			'success': True,
			'message': 'API is running',
			'data': {
				'service': 'english-kids-backend',
				'version': 'v1',
			},
		}
	)


@extend_schema(responses=DatabaseHealthResponseSerializer)
@api_view(['GET'])
def database_health_check(request):
	try:
		with connection.cursor() as cursor:
			cursor.execute('SELECT 1')
	except DatabaseError:
		return Response(
			{
				'success': False,
				'message': 'Database connection failed',
				'data': None,
			},
			status=status.HTTP_503_SERVICE_UNAVAILABLE,
		)

	return Response(
		{
			'success': True,
			'message': 'Database connection is healthy',
			'data': {
				'database': 'mysql',
			},
		}
	)
