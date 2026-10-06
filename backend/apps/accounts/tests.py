from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class UserModelTests(TestCase):
	def test_create_user_normalizes_email_and_hashes_password(self):
		user = User.objects.create_user(
			email='  Parent@Example.COM ',
			password='Password123!',
			first_name='Ngoc',
			last_name='Bich',
		)

		self.assertEqual(user.email, 'parent@example.com')
		self.assertTrue(user.check_password('Password123!'))
		self.assertNotEqual(user.password, 'Password123!')
		self.assertEqual(User.USERNAME_FIELD, 'email')

	def test_email_is_unique(self):
		User.objects.create_user(email='parent@example.com', password='Password123!')

		with self.assertRaises(IntegrityError):
			User.objects.create_user(
				email='PARENT@example.com',
				password='Password123!',
			)

	def test_create_superuser_sets_required_flags(self):
		user = User.objects.create_superuser(
			email='admin@example.com',
			password='Password123!',
		)

		self.assertTrue(user.is_active)
		self.assertTrue(user.is_staff)
		self.assertTrue(user.is_superuser)

	def test_create_user_requires_email(self):
		with self.assertRaises(ValueError):
			User.objects.create_user(email='', password='Password123!')

	def test_create_user_requires_password(self):
		with self.assertRaises(ValueError):
			User.objects.create_user(email='parent@example.com', password='')

	def test_create_superuser_rejects_invalid_staff_flag(self):
		with self.assertRaises(ValueError):
			User.objects.create_superuser(
				email='admin@example.com',
				password='Password123!',
				is_staff=False,
			)

	def test_create_superuser_rejects_invalid_superuser_flag(self):
		with self.assertRaises(ValueError):
			User.objects.create_superuser(
				email='admin@example.com',
				password='Password123!',
				is_superuser=False,
			)


class UserAdminTests(TestCase):
	def setUp(self):
		admin_user = User.objects.create_superuser(
			email='admin@example.com',
			password='Password123!',
		)
		self.client.force_login(admin_user)

	def test_user_add_page_is_available(self):
		response = self.client.get(reverse('admin:accounts_user_add'))

		self.assertEqual(response.status_code, 200)

	def test_user_add_page_hashes_password(self):
		response = self.client.post(
			reverse('admin:accounts_user_add'),
			{
				'email': 'new-user@example.com',
				'first_name': 'New',
				'last_name': 'User',
				'password1': 'Password123!',
				'password2': 'Password123!',
				'_save': 'Save',
			},
		)

		self.assertEqual(response.status_code, 302)
		user = User.objects.get(email='new-user@example.com')
		self.assertTrue(user.check_password('Password123!'))


class RegisterApiTests(APITestCase):
	register_url = '/api/v1/auth/register/'

	def valid_payload(self, **overrides):
		payload = {
			'email': 'parent@example.com',
			'password': 'SecurePass!2026',
			'password_confirm': 'SecurePass!2026',
			'first_name': 'Ngoc',
			'last_name': 'Bich',
		}
		payload.update(overrides)
		return payload

	def test_register_creates_user_and_returns_public_fields(self):
		response = self.client.post(
			self.register_url,
			self.valid_payload(),
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		response_data = response.json()
		user_data = response_data['data']['user']
		self.assertTrue(response_data['success'])
		self.assertEqual(user_data['email'], 'parent@example.com')
		self.assertNotIn('password', user_data)
		self.assertTrue(
			User.objects.get(email='parent@example.com').check_password(
				'SecurePass!2026'
			)
		)

	def test_register_rejects_duplicate_email_case_insensitively(self):
		User.objects.create_user(
			email='parent@example.com',
			password='SecurePass!2026',
		)

		response = self.client.post(
			self.register_url,
			self.valid_payload(email='PARENT@EXAMPLE.COM'),
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertFalse(response.json()['success'])

	def test_register_rejects_mismatched_passwords(self):
		response = self.client.post(
			self.register_url,
			self.valid_payload(password_confirm='DifferentPass!2026'),
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('password_confirm', response.json()['errors'])

	def test_register_requires_names_and_valid_email(self):
		response = self.client.post(
			self.register_url,
			self.valid_payload(
				email='invalid-email',
				first_name='',
				last_name='',
			),
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		errors = response.json()['errors']
		self.assertIn('email', errors)
		self.assertIn('first_name', errors)
		self.assertIn('last_name', errors)


class LoginApiTests(APITestCase):
	login_url = '/api/v1/auth/login/'

	def setUp(self):
		self.password = 'SecurePass!2026'
		User.objects.create_user(
			email='parent@example.com',
			password=self.password,
			first_name='Ngoc',
			last_name='Bich',
		)

	def test_login_returns_tokens_and_public_user(self):
		response = self.client.post(
			self.login_url,
			{
				'email': 'PARENT@EXAMPLE.COM',
				'password': self.password,
			},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		response_data = response.json()
		self.assertTrue(response_data['success'])
		self.assertIn('access', response_data['data'])
		self.assertIn('refresh', response_data['data'])
		self.assertEqual(
			response_data['data']['user']['email'],
			'parent@example.com',
		)
		self.assertNotIn('password', response_data['data']['user'])

	def test_login_rejects_wrong_password(self):
		response = self.client.post(
			self.login_url,
			{
				'email': 'parent@example.com',
				'password': 'WrongPassword!2026',
			},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertFalse(response.json()['success'])

	def test_login_rejects_unknown_email(self):
		response = self.client.post(
			self.login_url,
			{
				'email': 'unknown@example.com',
				'password': self.password,
			},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertFalse(response.json()['success'])

	def test_login_requires_email_and_password(self):
		response = self.client.post(self.login_url, {}, format='json')

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertFalse(response.json()['success'])
		self.assertIn('email', response.json()['errors'])
		self.assertIn('password', response.json()['errors'])


class RefreshTokenApiTests(APITestCase):
	refresh_url = '/api/v1/auth/token/refresh/'

	def setUp(self):
		user = User.objects.create_user(
			email='parent@example.com',
			password='SecurePass!2026',
		)
		self.refresh_token = str(RefreshToken.for_user(user))

	def test_refresh_returns_new_access_token(self):
		response = self.client.post(
			self.refresh_url,
			{'refresh': self.refresh_token},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertTrue(response.json()['success'])
		self.assertIn('access', response.json()['data'])

	def test_refresh_rejects_invalid_token(self):
		response = self.client.post(
			self.refresh_url,
			{'refresh': 'invalid-refresh-token'},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertFalse(response.json()['success'])

	def test_refresh_requires_refresh_token(self):
		response = self.client.post(self.refresh_url, {}, format='json')

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertFalse(response.json()['success'])
		self.assertIn('refresh', response.json()['errors'])


class CurrentUserApiTests(APITestCase):
	me_url = '/api/v1/auth/me/'

	def setUp(self):
		self.user = User.objects.create_user(
			email='parent@example.com',
			password='SecurePass!2026',
			first_name='Ngoc',
			last_name='Bich',
		)
		self.access_token = str(RefreshToken.for_user(self.user).access_token)

	def test_me_returns_current_user_for_valid_access_token(self):
		self.client.credentials(
			HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
		)

		response = self.client.get(self.me_url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		response_data = response.json()
		self.assertTrue(response_data['success'])
		self.assertEqual(
			response_data['data']['email'],
			'parent@example.com',
		)
		self.assertNotIn('password', response_data['data'])

	def test_me_requires_authentication(self):
		response = self.client.get(self.me_url)

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_me_rejects_invalid_access_token(self):
		self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid-access-token')

		response = self.client.get(self.me_url)

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LogoutApiTests(APITestCase):
	logout_url = '/api/v1/auth/logout/'
	refresh_url = '/api/v1/auth/token/refresh/'

	def setUp(self):
		user = User.objects.create_user(
			email='parent@example.com',
			password='SecurePass!2026',
		)
		self.refresh_token = str(RefreshToken.for_user(user))

	def test_logout_blacklists_refresh_token(self):
		logout_response = self.client.post(
			self.logout_url,
			{'refresh': self.refresh_token},
			format='json',
		)

		self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
		self.assertTrue(logout_response.json()['success'])
		self.assertIsNone(logout_response.json()['data'])

		refresh_response = self.client.post(
			self.refresh_url,
			{'refresh': self.refresh_token},
			format='json',
		)
		self.assertEqual(
			refresh_response.status_code,
			status.HTTP_401_UNAUTHORIZED,
		)

	def test_logout_rejects_invalid_refresh_token(self):
		response = self.client.post(
			self.logout_url,
			{'refresh': 'invalid-refresh-token'},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertFalse(response.json()['success'])

	def test_logout_requires_refresh_token(self):
		response = self.client.post(self.logout_url, {}, format='json')

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertFalse(response.json()['success'])
		self.assertIn('refresh', response.json()['errors'])


class SwaggerAuthDocumentationTests(APITestCase):
	def test_auth_endpoints_and_jwt_scheme_are_documented(self):
		response = self.client.get('/api/schema/')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		for path in (
			b'/api/v1/auth/register/',
			b'/api/v1/auth/login/',
			b'/api/v1/auth/token/refresh/',
			b'/api/v1/auth/logout/',
			b'/api/v1/auth/me/',
		):
			self.assertIn(path, response.content)
		self.assertIn(b'jwtAuth', response.content)

