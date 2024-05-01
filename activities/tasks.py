from celery import shared_task
from django.contrib.auth import get_user_model

from activities.models import Post


@shared_task
def create_scheduled_post(content, image, user_id):
    author = get_user_model().objects.get(pk=user_id)
    Post.objects.create(
        content=content,
        image=image,
        user=author
    )
