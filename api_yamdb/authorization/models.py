from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель представляющая пользователя."""

    class RoleUser(models.TextChoices):
        USER = 'user'
        ADMIN = 'admin'
        MODERATOR = 'moderator'

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Почта'
    )
    role = models.CharField(
        max_length=50,
        choices=RoleUser.choices,
        default=RoleUser.USER,
        verbose_name='Пользовательские роли'
    )

    bio = models.TextField(blank=True, verbose_name='Биография')
    confirmation_code = models.CharField(
        max_length=100,
        null=True,
        verbose_name='Код подтверждения',
        unique=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def user(self):
        return self.role == self.RoleUser.USER

    @property
    def moderator(self):
        return self.role == self.RoleUser.MODERATOR

    @property
    def admin(self):
        return self.role == self.RoleUser.ADMIN
