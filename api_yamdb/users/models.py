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
    confirmation_code = models.CharField(max_length=255, blank=True, null=True)

    @property
    def is_moderator(self):
        return self.role == (self.MODERATOR or self.ADMIN or self.is_superuser)

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_user(self):
        return self.role == self.USER

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
