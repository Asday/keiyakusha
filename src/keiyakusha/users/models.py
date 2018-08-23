from django.conf import settings
from django.db import models

from annoying.fields import AutoOneToOneField
from pytz import all_timezones


class UserProfile(models.Model):
    week_start_on_monday = models.BooleanField(default=True)
    timezone = models.CharField(
        max_length=max((len(timezone) for timezone in all_timezones)),
        choices=((timezone, timezone) for timezone in all_timezones),
        default='UTC',
    )

    user = AutoOneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )

    def __str__(self):
        return str(self.user)
