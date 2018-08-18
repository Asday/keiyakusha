from django.conf import settings
from django.db import models


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

    def __str__(self):
        return (
            f'With {self.client} from {self.start} for {self.duration}'
            f' at {self.currency} {self.rate}/h, for'
            f' {self.time_per_week}/w, billed every'
            f' {self.invoice_period_days} days'
        )
