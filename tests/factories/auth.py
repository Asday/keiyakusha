import factory

from django.apps import apps
from django.conf import settings


User = apps.get_model(settings.AUTH_USER_MODEL)


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User
