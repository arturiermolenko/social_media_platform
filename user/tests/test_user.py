from random import choices
from string import ascii_lowercase

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

USER_FOLLOW_UNFOLLOW_URL = reverse("user:follow_unfollow")


class UserModelTests(TestCase):
    def test_user_creation_with_email(self):
        email = "test@email.com"
        password = "testpass123"
        user = get_user_model().objects.create(email=email, password=password)
        self.assertEqual(user.pk, user.id)
        self.assertEqual(user.email, email)

    def test_cannot_create_user_with_username(self):
        username = "test@email.com"
        password = "testpass123"
        with self.assertRaises(TypeError):
            get_user_model().objects.create(username=username, password=password)


def create_user():
    suffix = "".join(choices(ascii_lowercase, k=10))
    email = f"{suffix}@social.com"
    password = reversed(suffix)
    return get_user_model().objects.create(email=email, password=password)


class UserAPITEsts(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@cosial.com", "password"
        )
        self.client.force_authenticate(self.user)

    def test_follow_unfollow(self):
        user = create_user()
        data = {"type": "follow", "id": user.id}

        self.client.post(USER_FOLLOW_UNFOLLOW_URL, data)

        self.assertEqual(self.user.following.count(), 1)
        self.assertEqual(user.followers.first(), self.user)

        data = {"type": "unfollow", "id": user.id}

        self.client.post(USER_FOLLOW_UNFOLLOW_URL, data)

        self.assertEqual(self.user.following.count(), 0)
        self.assertNotEqual(user.followers.first(), self.user)
