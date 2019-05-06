import factory

from django.apps import apps
from django.conf import settings


User = apps.get_model(settings.AUTH_USER_MODEL)


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: f'user-{n}')

    class Meta:
        model = User
