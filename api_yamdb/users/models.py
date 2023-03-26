
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db import models

ROLE_CHOICES = (
    ('U', 'user'),
    ('M', 'moderator'),
    ('A', 'admin'),
)


def username_is_not_me_validators(username):
    if username == 'me':
        raise ValidationError('Username cannot be \'me\'')


class User(AbstractUser):
    username = models.CharField(
        'username',
        max_length=150,
        blank=True,
        unique=True,
        validators=(
            UnicodeUsernameValidator(),
            username_is_not_me_validators,
        )
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=1,
        choices=ROLE_CHOICES,
        default='U',
    )
    confirmation_code = models.IntegerField(
        'Код подтверждения',
        blank=True,
        null=True,
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('email',),
                name='unique_email',
            ),
        )
