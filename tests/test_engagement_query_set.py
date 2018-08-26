from datetime import date, timedelta

import pytest

from engagements.models import Engagement
from factories.auth import UserFactory
from factories.clients import ClientFactory
from factories.engagements import EngagementFactory


@pytest.mark.django_db
def test_active_at():
    user = UserFactory()

    client_a = ClientFactory()
    client_b = ClientFactory()

    engagement_a_active = EngagementFactory(
        start=date(2018, 8, 23),
        duration=timedelta(days=1),
        user=user,
        client=client_a,
    )
    EngagementFactory(
        start=date(2018, 8, 21),
        duration=timedelta(days=1),
        user=user,
        client=client_a,
    )
    EngagementFactory(
        start=date(2018, 8, 23),
        duration=timedelta(days=1),
        user=user,
        client=client_b,
    )

    assert Engagement.objects.all().count() == 3  # Just checkin'.

    active_at = Engagement.objects \
        .filter(client=client_a) \
        .active_at(date(2018, 8, 23))

    assert engagement_a_active in active_at
    assert active_at.count() == 1
