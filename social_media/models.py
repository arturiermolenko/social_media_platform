import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify

from user.models import User


def post_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    post_title = instance.created_at
    filename = f"{slugify(post_title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/posts/", filename)


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    liked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="liked_posts"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        null=True,
        upload_to=post_image_file_path,
        blank=True,
        default=None
    )

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    content = models.CharField(max_length=300)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    liked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="liked_comments"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.content
