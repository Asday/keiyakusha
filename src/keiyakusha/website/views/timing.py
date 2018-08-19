from collections import defaultdict
from datetime import timedelta
from decimal import Decimal

from django.views.generic import TemplateView

import attr


# Will likely move closer to where the data comes from when the
# time comes.  For now it can be here to fill with test data.
@attr.s
class TimerData(object):
    duration = attr.ib()
    totals = attr.ib()

    def render_totals(self):
        # TODO: Test.
        totals = defaultdict(Decimal)
        for total in self.totals:
            totals[total.currency] += total.amount

        ordered_totals = sorted(
            totals.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        rendered_totals = (
            ''.join((str(total_item) for total_item in total))
            for total in ordered_totals
        )

        return ' '.join(rendered_totals)


@attr.s
class Total(object):
    amount = attr.ib()
    currency = attr.ib()


# TODO: Should this subclass `ListView` instead?
class TimingView(LoginRequiredMixin, TemplateView):
    template_name = 'timing/index.html'

    def get_uninvoiced_data(self):
        # TODO: Get real data.
        return TimerData(
            duration=timedelta(hours=73, minutes=20, seconds=3),
            totals=[
                Total(amount=Decimal('10.00'), currency='AUD'),
                Total(amount=Decimal('15.00'), currency='AUD'),
                Total(amount=Decimal('20.00'), currency='GBP'),
            ]
        )

    def get_this_week_data(self):
        # TODO: Get real data.
        return TimerData(
            duration=timedelta(hours=12, minutes=10),
            totals=[
                Total(amount=Decimal('15.00'), currency='AUD'),
                Total(amount=Decimal('20.00'), currency='GBP'),
            ]
        )

    def get_today_data(self):
        # TODO: Get real data.
        return TimerData(
            duration=timedelta(hours=3, minutes=40, seconds=35),
            totals=[
                Total(amount=Decimal('15.00'), currency='AUD'),
                Total(amount=Decimal('20.00'), currency='GBP'),
            ]
        )

    def get_current_task_data(self):
        # TODO: Get real data.
        # return None
        return TimerData(
            duration=timedelta(hours=1),
            totals=[
                Total(amount=Decimal('5.00'), currency='GBP'),
            ]
        )
