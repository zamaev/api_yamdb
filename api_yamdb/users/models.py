
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
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
