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


@freeze_time('2018-08-23 14:00:00', tick=True)
@pytest.mark.django_db
def test_add_time_form_client_related_properties():
    user = UserFactory()
    other_user = UserFactory()
    client_active_1 = ClientFactory()
    client_active_2 = ClientFactory()
    client_inactive = ClientFactory()
    client_active_other_user = ClientFactory()
    client_inactive_other_user = ClientFactory()
    ClientFactory()  # never had an engagement

    one_day = timedelta(days=1)
    active_kwargs = {'start': date(2018, 8, 23), 'duration': one_day}
    inactive_kwargs = {'start': date(2018, 8, 20), 'duration': one_day}

    EngagementFactory(user=user, client=client_active_1, **active_kwargs)
    EngagementFactory(user=user, client=client_active_2, **active_kwargs)
    EngagementFactory(user=user, client=client_inactive, **inactive_kwargs)
    EngagementFactory(
        user=other_user,
        client=client_active_other_user,
        **active_kwargs,
    )
    EngagementFactory(
        user=other_user,
        client=client_inactive_other_user,
        **inactive_kwargs,
    )

    form = AddTimeForm(user=user)

    clients = form.user_clients

    assert clients.count() == 2
    assert client_active_1 in clients
    assert client_active_2 in clients

    project_client_1 = ProjectFactory(client=client_active_1)
    project_client_2 = ProjectFactory(client=client_active_2)
    project_other_user = ProjectFactory(client=client_active_other_user)

    projects = form.user_projects

    assert projects.count() == 2
    assert project_client_1 in projects
    assert project_client_2 in projects

    task_client_1 = TaskFactory(project=project_client_1)
    task_client_2 = TaskFactory(project=project_client_2)
    TaskFactory(project=project_other_user)

    tasks = form.user_tasks

    assert tasks.count() == 2
    assert task_client_1 in tasks
    assert task_client_2 in tasks
