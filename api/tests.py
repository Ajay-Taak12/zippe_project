from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthenticationTests(APITestCase):
    def test_user_can_register_and_login(self):
        register_url = reverse("register")
        login_url = reverse("token_obtain_pair")

        payload = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "strong-password",
            "password2": "strong-password",
        }

        register_response = self.client.post(register_url, payload, format="json")
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())

        login_payload = {
            "username": "testuser",
            "password": "strong-password",
        }
        login_response = self.client.post(login_url, login_payload, format="json")
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", login_response.data)
        self.assertIn("refresh", login_response.data)


class TaskTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="taskuser", email="task@example.com", password="task-pass"
        )
        login_url = reverse("token_obtain_pair")
        response = self.client.post(
            login_url,
            {"username": "taskuser", "password": "task-pass"},
            format="json",
        )
        self.access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_create_and_list_tasks(self):
        list_url = reverse("task-list")

        create_payload = {
            "title": "My first task",
            "description": "Test description",
            "completed": False,
        }
        create_response = self.client.post(list_url, create_payload, format="json")
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        list_response = self.client.get(list_url)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(list_response.data["count"], 1)
        self.assertEqual(list_response.data["results"][0]["title"], "My first task")
