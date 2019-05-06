from datetime import date, timedelta

from freezegun import freeze_time
import pytest

from engagements.models import Engagement

from factories.auth import UserFactory
from factories.clients import ClientFactory
from factories.engagements import EngagementFactory


@freeze_time('2018-08-23 14:00:00', tick=True)
@pytest.mark.django_db
def test_engagement_manager_current_for():
    user_1 = UserFactory()
    user_2 = UserFactory()
    client_1 = ClientFactory()
    client_2 = ClientFactory()

    one_day = timedelta(days=1)
    active_kwargs = {'start': date(2018, 8, 23), 'duration': one_day}
    inactive_kwargs = {'start': date(2018, 8, 20), 'duration': one_day}

    user_1_client_1 = EngagementFactory(
        user=user_1,
        client=client_1,
        **active_kwargs,
    )
    user_2_client_1 = EngagementFactory(
        user=user_2,
        client=client_1,
        **active_kwargs,
    )
    user_1_client_2 = EngagementFactory(
        user=user_1,
        client=client_2,
        **active_kwargs,
    )
    EngagementFactory(user=user_2, client=client_2, **active_kwargs)

    EngagementFactory(user=user_1, client=client_1, **inactive_kwargs)
    EngagementFactory(user=user_2, client=client_1, **inactive_kwargs)
    EngagementFactory(user=user_1, client=client_2, **inactive_kwargs)
    EngagementFactory(user=user_2, client=client_2, **inactive_kwargs)

    with pytest.raises(ValueError):
        Engagement.objects.current_for()

    user_and_client = Engagement.objects.current_for(
        user=user_1,
        client=client_1,
    )

    assert user_and_client.count() == 1
    assert user_1_client_1 in user_and_client

    user_only = Engagement.objects.current_for(user=user_1)

    assert user_only.count() == 2
    assert user_1_client_1 in user_only
    assert user_1_client_2 in user_only

    client_only = Engagement.objects.current_for(client=client_1)

    assert client_only.count() == 2
    assert user_1_client_1 in client_only
    assert user_2_client_1 in client_only
