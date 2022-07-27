from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLES = (
        ('USER', 'USER'),
        ('MODERATOR', 'MODERATOR'),
        ('ADMIN', 'ADMIN'),
    )

    email = models.EmailField('email address', unique=True, blank=False)
    bio = models.TextField('biography', blank=True)
    role = models.CharField(max_length=20, choices=ROLES, default=ROLES[0][0])
    confirmation_code = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username