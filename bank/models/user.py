from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    cpf = models.CharField(max_length=11, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="bank_users",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="bank_users_permissions",
        blank=True,
    )

    def __str__(self):
        return self.username
