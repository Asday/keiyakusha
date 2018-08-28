from datetime import date, timedelta

from freezegun import freeze_time
import pytest

from clients.models import Project, Task
from timing_website.forms import AddTimeForm

from factories.auth import UserFactory
from factories.clients import ClientFactory, ProjectFactory, TaskFactory
from factories.engagements import EngagementFactory


def client_and_user_with_engagement():
    client = ClientFactory(name='client')
    user = UserFactory()
    EngagementFactory(
        user=user,
        client=client,
        start=date(2018, 8, 23),
        duration=timedelta(days=1),
    )

    return client, user


@freeze_time('2018-08-23 14:00:00', tick=True)
@pytest.mark.django_db
def test_add_time_form_creates_objects():
    client, user = client_and_user_with_engagement()

    form = AddTimeForm(
        data={
            'start': '1300',
            'task': 'task',
            'project': 'project',
            'client': client.name,
        },
        user=user,
    )

    form.is_valid()
    assert form.errors == {}

    time_entry = form.save()
    task = Task.objects.get(external_reference='task')
    project = Project.objects.get(name='project')

    assert project.client == client
    assert task.project == project
    assert time_entry.task == task
    assert time_entry.pk is not None


@freeze_time('2018-08-23 14:00:00', tick=True)
@pytest.mark.django_db
def test_add_time_form_uses_existing_projects():
    client, user = client_and_user_with_engagement()
    project = ProjectFactory(name='project', client=client)

    form = AddTimeForm(
        data={
            'start': '1300',
            'task': 'task',
            'project': project.name,
            'client': client.name,
        },
        user=user,
    )

    form.is_valid()
    assert form.errors == {}
    assert Project.objects.count() == 1


@freeze_time('2018-08-23 14:00:00', tick=True)
@pytest.mark.django_db
def test_add_time_form_uses_existing_tasks():
    client, user = client_and_user_with_engagement()
    project = ProjectFactory(name='project', client=client)
    task = TaskFactory(external_reference='task', project=project)

    form = AddTimeForm(
        data={
            'start': '1300',
            'task': task.external_reference,
            'project': project.name,
            'client': client.name,
        },
        user=user,
    )

    form.is_valid()
    assert form.errors == {}
    assert Task.objects.count() == 1


@freeze_time('2018-08-23 14:00:00', tick=True)
@pytest.mark.django_db
def test_add_time_form_handles_duration():
    client, user = client_and_user_with_engagement()

    form = AddTimeForm(
        data={
            'start': '1300',
            'end': '1330',
            'task': 'task',
            'project': 'project',
            'client': client.name,
        },
        user=user,
    )

    form.is_valid()
    assert form.errors == {}

    time_entry = form.save()

    assert time_entry.duration == timedelta(minutes=30)
