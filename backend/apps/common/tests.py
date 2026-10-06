from rest_framework import status
from rest_framework.test import APITestCase


class HealthApiTests(APITestCase):
	def test_health_endpoint_returns_expected_response(self):
		response = self.client.get('/api/v1/health/')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(
			response.json(),
			{
				'success': True,
				'message': 'API is running',
				'data': {
					'service': 'english-kids-backend',
					'version': 'v1',
				},
			},
		)

	def test_database_health_endpoint_returns_healthy(self):
		response = self.client.get('/api/v1/health/db/')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.json()['success'], True)
		self.assertEqual(response.json()['data']['database'], 'mysql')

	def test_health_endpoint_is_versioned(self):
		response = self.client.get('/health/')

		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_api_documentation_endpoints_are_available(self):
		schema_response = self.client.get('/api/schema/')
		swagger_response = self.client.get('/api/docs/')
		redoc_response = self.client.get('/api/redoc/')

		self.assertEqual(schema_response.status_code, status.HTTP_200_OK)
		self.assertEqual(swagger_response.status_code, status.HTTP_200_OK)
		self.assertEqual(redoc_response.status_code, status.HTTP_200_OK)
		self.assertIn(b'/api/v1/health/', schema_response.content)
		self.assertIn(b'/api/v1/health/db/', schema_response.content)
