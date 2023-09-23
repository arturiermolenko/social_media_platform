import os
import uuid

from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


def user_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    full_name = f"{instance.first_name} {instance.last_name}"
    filename = f"{slugify(full_name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/users/", filename)


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    bio = models.CharField(
        max_length=400,
        blank=True,
    )
    following = models.ManyToManyField("self", blank=True)
    followers = models.ManyToManyField("self", blank=True)
    profile_picture = models.ImageField(null=True, upload_to=user_image_file_path)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
