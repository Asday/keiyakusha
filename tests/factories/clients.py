import factory

from clients.models import Client, Project, Task


class ClientFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'client-{n}')

    class Meta:
        model = Client


class ProjectFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'project-{n}')
    client = factory.SubFactory(ClientFactory)

    class Meta:
        model = Project


class TaskFactory(factory.django.DjangoModelFactory):
    external_reference = factory.Sequence(lambda n: f'task-{n}')
    project = factory.SubFactory(ProjectFactory)

    class Meta:
        model = Task
