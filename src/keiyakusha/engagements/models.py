from django.conf import settings
from django.db import models
from django.utils import timezone


class EngagementQuerySet(models.QuerySet):

    def with_end(self):
        return self.annotate(end=models.ExpressionWrapper(
            models.F('start') + models.F('duration'),
            output_field=models.DateField(),
        ))

    def active_at(self, when):
        return self \
            .with_end() \
            .filter(start__lte=when, end__gte=when)

    def current(self):
        return self.active_at(timezone.now())


class EngagementManager(models.Manager.from_queryset(EngagementQuerySet)):

    def current_for(self, user=None, client=None):
        filter_kwargs = {}

        if user is not None:
            filter_kwargs['user'] = user

        if client is not None:
            filter_kwargs['client'] = client

        if not filter_kwargs:
            raise ValueError(
                'You must supply at least one of (`user`, `client`)',
            )

        return self.get_queryset() \
            .filter(**filter_kwargs) \
            .current()


class Engagement(models.Model):
    start = models.DateField()
    duration = models.DurationField()
    rate = models.DecimalField(max_digits=18, decimal_places=2)
    currency = models.CharField(max_length=3)
    time_per_week = models.DurationField()
    invoice_period_days = models.PositiveIntegerField()

    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.PROTECT,
        related_name='engagements',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='engagements',
    )

    objects = EngagementManager()

    def __str__(self):
        # TODO: Remove lookups from string methods.
        return (
            f'{self.user.get_full_name()} with {self.client} from'
            f' {self.start} until {self.duration + self.start} at'
            f' {self.currency} {self.rate}/h, for'
            f' {self.time_per_week}/w, billed every'
            f' {self.invoice_period_days} days'
        )
