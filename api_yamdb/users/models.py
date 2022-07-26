from django.contrib.auth.models import AbstractUser
from django.db import models


CHOICES = [
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
]


class User(AbstractUser):

    email = models.EmailField(
        'email address',
        unique=True,
        null=False,
        blank=False
    )
    bio = models.TextField('biography', blank=True)
    role = models.CharField(max_length=100, choices=CHOICES, default='user')