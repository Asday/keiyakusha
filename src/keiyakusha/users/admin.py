from django.contrib.admin import site

from .models import UserProfile


site.register(UserProfile)
