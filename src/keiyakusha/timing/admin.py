from django.contrib.admin import site

from .models import TimeEntry


site.register(TimeEntry)
