from django.conf import settings
from django.db import models
from django.utils.functional import cached_property


class Account(models.Model):
    name = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255)
    currency = models.CharField(max_length=3)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='accounts',
    )

    def __str__(self):
        return f'{self.name} at {self.bank_name} in {self.currency}'


class Transaction(models.Model):
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    target = models.CharField(max_length=255, help_text='creditor or debtor')
    date = models.DateField()

    account = models.ForeignKey(
        'bank_accounts.Account',
        on_delete=models.PROTECT,
        related_name='transactions',
    )
    foreign_transaction = models.OneToOneField(
        'bank_accounts.ForeignTransaction',
        on_delete=models.PROTECT,
        related_name='transaction',
        blank=True,
        null=True,
    )

    def __str__(self):
        return (
            f'{abs(self.amount)} {"to" if self.amount < 0 else "from"}'
            f' {self.target}'
        )

    @cached_property
    def is_foreign(self):
        return self.foreign_transaction is not None

    @cached_property
    def native_amount(self):
        # TODO: Test.
        if self.is_foreign:
            return self.foreign_transaction.gross_amount
        else:
            return self.amount

    @cached_property
    def native_currency(self):
        # TODO: Test.
        if self.is_foreign:
            return self.foreign_transaction.currency
        else:
            return self.account.currency


class ForeignTransaction(models.Model):
    exchange_rate = models.DecimalField(max_digits=18, decimal_places=5)
    currency = models.CharField(max_length=3)
    fee = models.DecimalField(max_digits=18, decimal_places=2)

    def __str__(self):
        return (
            f'{self.currency} {self.net_amount} received, at'
            f' {self.exchange_rate}:1, with a {self.fee} fee'
        )

    @cached_property
    def gross_amount(self):
        # TODO: Test.
        return (self.transaction.amount + self.fee) * self.exchange_rate
