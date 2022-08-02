from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = [
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    ]

    email = models.EmailField(max_length=80, unique=True, blank=False)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=20, choices=ROLES, default=USER)
    password = models.CharField(max_length=128, blank=True, null=True)
    confirmation_code = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
