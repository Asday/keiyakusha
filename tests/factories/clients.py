import factory

from clients.models import Client


class ClientFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'client-{n}')

    class Meta:
        model = Client
