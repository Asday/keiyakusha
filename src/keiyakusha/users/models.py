from django.conf import settings
from django.db import models

from annoying.fields import AutoOneToOneField


class UserProfile(models.Model):
    week_start_on_monday = models.BooleanField(default=True)

    user = AutoOneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )

    def __str__(self):
        return str(self.user)
