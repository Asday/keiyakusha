import os

from django.db import models
from django.utils.functional import cached_property

from slugify import slugify


class Payment(models.Model):
    invoice = models.ForeignKey(
        'invoices.Invoice',
        on_delete=models.PROTECT,
        related_name='payments',
    )
    transaction = models.OneToOneField(
        'bank_accounts.Transaction',
        on_delete=models.CASCADE,
        related_name='payment',
    )

    def __str__(self):
        return f'{self.currency} {self.amount} on {self.date}'

    @cached_property
    def amount(self):
        return self.transaction.native_amount

    @cached_property
    def currency(self):
        return self.transaction.native_currency

    @cached_property
    def date(self):
        return self.transaction.date


def invoice_path(instance, filename):
    """
    Returns a path suitable for saving an invoice to.

    Refers to the client being invoiced.
    """
    # TODO: Test.
    return os.path.join(
        'invoices',
        slugify(instance.client),
        filename,
    )


class Invoice(models.Model):
    date_issued = models.DateField()
    date_due = models.DateField()
    file_sent = models.FileField(upload_to=invoice_path)
    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.PROTECT,
        related_name='invoices',
    )

    def __str__(self):
        return f'Issued to {self.client} on {self.date_issued}'
