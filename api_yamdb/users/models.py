
from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = (
    ('U', 'user'),
    ('M', 'moderator'),
    ('A', 'admin'),
)


class User(AbstractUser):
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
