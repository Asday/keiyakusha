from datetime import date, timedelta
from decimal import Decimal

import factory

from engagements.models import Engagement

from .clients import ClientFactory
from .auth import UserFactory


class EngagementFactory(factory.django.DjangoModelFactory):
    start = date(2018, 8, 23)
    duration = timedelta(days=1)
    rate = Decimal('10.00')
    currency = 'GBP'
    time_per_week = timedelta(hours=35)
    invoice_period_days = 14
    client = factory.SubFactory(ClientFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Engagement
