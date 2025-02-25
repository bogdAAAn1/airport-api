from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class CreateUserViewTests(APITestCase):
    def test_create_user(self):
        url = reverse("user:create")
        data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(email="test@example.com")
        self.assertEqual(user.email, "test@example.com")
        self.assertNotEqual(user.password, "testpass123")
        self.assertTrue(user.check_password("testpass123"))

    def test_create_user_with_short_password(self):
        url = reverse("user:create")
        data = {
            "email": "test@example.com",
            "password": "123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_create_user_with_existing_email(self):
        User.objects.create_user(email="test@example.com", password="testpass123")
        url = reverse("user:create")
        data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)


class JWTAuthenticationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )
        self.url = reverse("user:manage")

    def test_jwt_authentication(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)