from django.db import models


class TimeEntry(models.Model):
    start = models.DateTimeField()
    duration = models.DurationField()
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

    def __str__(self):
        return f'{self.task} {self.rendered_note}'

    @property
    def rendered_note(self):
        return f' {self.note}' if self.note else ''
