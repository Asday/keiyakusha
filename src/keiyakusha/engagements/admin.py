from django.contrib.admin import site

from .models import Engagement


site.register(Engagement)
