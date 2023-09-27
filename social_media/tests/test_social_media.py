from random import choices
from string import ascii_lowercase

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from social_media.models import Post, Comment
from social_media.serializers import PostListSerializer

POSTS_URL = reverse("social-media:posts-list")
POSTS_CREATE_URL = reverse("social_media:posts-create")


def sample_post(**params):
    suffix = "".join(choices(ascii_lowercase, k=5))
    author_id = get_user_model().objects.first().id

    defaults = {
        "title": f"test_title_{suffix}",
        "content": f"test_content_{suffix * 10}",
        "author_id": author_id,
    }
    defaults.update(params)

    return Post.objects.create(**defaults)


def get_detail_post_url(post_id):
    return reverse("social_media:posts-detail", args=[post_id])


def get_like_unlike_post_url(post_id):
    return reverse("social_media:posts-like-unlike", args=[post_id])


def get_url_for_add_comment(post_id):
    return reverse("social-media:comment-create", args=[post_id])


def get_detail_comment_url(post_id, comment_id):
    return reverse("social_media:comment-detail", args=[post_id, comment_id])


def get_url_for_like_unlike_comment(post_id, comment_id):
    return reverse("social-media:comment-like-unlike", args=[post_id, comment_id])


class UnauthenticatedSocialMediaApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(POSTS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedSocialMediaApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_posts(self):
        sample_post()
        sample_post()
        sample_post()

        response = self.client.get(POSTS_URL)
        data = response.data["results"]
        for post in data:
            del post["like_count"]

        posts = Post.objects.order_by("-updated_at")
        serializer = PostListSerializer(posts, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, serializer.data)

    def test_create_post(self):
        suffix = "".join(choices(ascii_lowercase, k=5))
        author_id = get_user_model().objects.first().id
        data = {
            "title": f"test_title_{suffix}",
            "content": f"test_content_{suffix * 10}",
            "author_id": author_id,
        }

        response = self.client.post(POSTS_CREATE_URL, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_post(self):
        post = sample_post(author_id=1)
        data = {
            "title": "test_title",
            "content": "test_content",
            "author_id": 1,
        }
        url = get_detail_post_url(post_id=post.id)
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_post(self):
        post = sample_post(author_id=1)
        data = {
            "content": "test_content",
        }
        url = get_detail_post_url(post_id=post.id)
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_post(self):
        post = sample_post(author_id=1)

        url = get_detail_post_url(post_id=post.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_like_unlike_post(self):
        post = sample_post()

        url = get_detail_post_url(post_id=post.id)
        first_response = self.client.get(url)
        likes_count_before = len(first_response.data["liked_by"])

        like_url = get_like_unlike_post_url(post_id=post.id)
        self.client.post(like_url)
        second_response = self.client.get(url)
        likes_count_after_like = len(second_response.data["liked_by"])

        self.assertEqual(likes_count_before + 1, likes_count_after_like)

        self.client.post(like_url)
        third_response = self.client.get(url)
        likes_count_after_unlike = len(third_response.data["liked_by"])

        self.assertEqual(likes_count_after_unlike, likes_count_after_like - 1)

    def test_add_comment(self):
        post = sample_post()
        data = {
            "content": "test comment"
        }

        url = get_url_for_add_comment(post_id=post.id)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_like_unlike_comment(self):
        post = sample_post()
        comment = Comment.objects.create(
            content="test content",
            post_id=post.id,
            author=self.user
        )

        like_count = Comment.objects.get(id=comment.id).liked_by.count()

        like_url = get_url_for_like_unlike_comment(
            post_id=post.id,
            comment_id=comment.id
        )
        self.client.post(like_url)
        comment_url = get_detail_comment_url(
            post_id=post.id,
            comment_id=comment.id
        )
        response = self.client.get(comment_url)

        like_count_after = len(response.data["liked_by"])

        self.assertEqual(like_count, like_count_after - 1)
