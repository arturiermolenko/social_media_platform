import random
import string

from celery import shared_task
from django.contrib.auth import get_user_model

from social_media.models import Post


@shared_task
def create_post_at_scheduled_time():
    if get_user_model().objects.first():
        author_id = get_user_model().objects.first().id
        letters = string.ascii_lowercase
        title = "".join(random.choice(letters) for _ in range(50))
        content = "".join(random.choice(letters) for _ in range(150))
        Post.objects.create(title=title, content=content, author_id=author_id)
    else:
        print("You need to create a user!")
