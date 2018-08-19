from calendar import weekday
from collections import defaultdict
from datetime import timedelta
from decimal import Decimal

from django.db import models
from django.utils import timezone

import attr


@attr.s
class TimerData(object):
    duration = attr.ib()
    totals = attr.ib()

    @classmethod
    def from_queryset(cls, qs):
        # TODO: Test.
        return cls(
            duration=qs.total_duration(),
            totals=[
                Total(amount=amount, currency=currency)
                for currency, amount in qs.total_amounts().items()
            ],
        )

    @classmethod
    def from_instance(cls, time_entry):
        # TODO: Test.
        return cls(
            duration=time_entry.duration_so_far,
            totals=[
                Total(amount=time_entry.amount, currency=time_entry.currency)
            ],
        )

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
            ''.join((currency, str(amount.quantize(Decimal('0.01')))))
            for currency, amount in ordered_totals
        )

        return ' '.join(rendered_totals)


@attr.s
class Total(object):
    amount = attr.ib()
    currency = attr.ib()


class TimeEntryQuerySet(models.QuerySet):

    def uninvoiced(self):
        return self.filter(invoice=None)

    def running_tasks(self):
        return self.filter(duration=None)

    def from_this_week(self, user=None):
        # TODO: Test.
        # TODO: Might not be the best place for getting week start.
        # TODO: Might not be the best place for getting last Monday.
        week_start_on_monday = True
        if user is not None and user.profile is not None:
            week_start_on_monday = user.profile.week_start_on_monday

        today = timezone.now().date()
        current_weekday = weekday(today.year, today.month, today.day)

        if not week_start_on_monday:
            # We're going to subtract the weekday from the current date
            # to get the start of the week's date.  If the user has for
            # some bizarre reason decided that Sunday is the start of
            # the week, shift `current_weekday` such that 0 == Sunday
            # instead of Monday.
            current_weekday += 1
            current_weekday %= 7

        last_monday = today - timedelta(days=current_weekday)

        return self.filter(
            start__day__gte=last_monday.day,
            start__month__gte=last_monday.month,
            start__year__gte=last_monday.year,
        )

    def from_today(self):
        today = timezone.now().date()

        return self.filter(
            start__day__gte=today.day,
            start__month__gte=today.month,
            start__year__gte=today.year,
        )

    def total_duration(self):
        # TODO: Test.
        return self.aggregate(models.Sum('duration'))['duration__sum']

    def total_amounts(self):
        # TODO: Test.
        totals = defaultdict(Decimal)
        for time_entry in self:
            totals[time_entry.engagement.currency] += time_entry.amount

        return totals

    def data(self):
        return TimerData.from_queryset(self)


class TimeEntryManager(models.Manager.from_queryset(TimeEntryQuerySet)):

    def current_task(self, user):
        try:
            return self.running_tasks().filter(engagement__user=user).get()
        except self.model.DoesNotExist:
            return None


class TimeEntry(models.Model):
    start = models.DateTimeField()
    duration = models.DurationField(blank=True, null=True)
    note = models.CharField(max_length=255, blank=True)

    task = models.ForeignKey(
        'clients.Task',
        on_delete=models.PROTECT,
        related_name='time_entries',
    )
    invoice = models.ForeignKey(
        'invoices.Invoice',
        on_delete=models.SET_NULL,
        related_name='time_entries',
        blank=True,
        null=True,
    )
    engagement = models.ForeignKey(
        'engagements.Engagement',
        on_delete=models.PROTECT,
        related_name='time_entries',
    )

    objects = TimeEntryManager()

    class Meta:
        verbose_name_plural = 'time entries'

    def __str__(self):
        return f'{self.duration} on {self.task} {self.rendered_note}'

    @property
    def rendered_note(self):
        return f' {self.note}' if self.note else ''

    @property
    def duration_so_far(self):
        return timezone.now() - self.start

    @property
    def amount(self):
        # TODO: Test.
        duration = self.duration or self.duration_so_far
        secondly_rate = self.engagement.rate / 60 / 60

        return duration.seconds * secondly_rate

    @property
    def currency(self):
        return self.engagement.currency

    def as_data(self):
        return TimerData.from_instance(self)

    @property
    def start_date(self):
        return self.start.date()

    @property
    def start_time(self):
        return self.start.time()

    @property
    def end_time(self):
        # TODO: Test.
        return (self.start + self.duration).time()
