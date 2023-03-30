from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from users.validators import username_is_not_me_validators

ROLE_CHOICES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


class User(AbstractUser):
    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text=('Required. 150 characters or fewer. '
                   'Letters, digits and @/./+/-/_ only.'),
        validators=(
            UnicodeUsernameValidator(),
            username_is_not_me_validators,
        ),
        error_messages={
            'unique': 'A user with that username already exists.',
        },
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=30,
        choices=ROLE_CHOICES,
        default='user',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)
        constraints = (
            models.UniqueConstraint(
                fields=('email',),
                name='unique_email',
            ),
        )

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'admin'

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'admin'
        if self.is_admin:
            self.is_staff = True
        super().save(*args, **kwargs)
