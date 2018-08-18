from django.contrib.admin import site

from .models import Client, Project, Task


site.register(Client)
site.register(Project)
site.register(Task)
