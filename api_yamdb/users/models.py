
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db import models

ROLE_CHOICES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


def username_is_not_me_validators(username):
    if username == 'me':
        raise ValidationError('Username cannot be \'me\'')


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
    confirmation_code = models.IntegerField(
        'Код подтверждения',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('username',)
        constraints = (
            models.UniqueConstraint(
                fields=('email',),
                name='unique_email',
            ),
        )

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'admin'
        if self.role == 'admin':
            self.is_staff = True
        super().save(*args, **kwargs)
