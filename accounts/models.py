from django.db import models
from django.utils import timezone
from users.models import User
from django.shortcuts import get_object_or_404
# Create your models here.

ACCOUNT_TYPE_CHOICES = (
    ('BİRİKİM HESABI','BİRİKİM HESABI'),
    ('KREDİLİ MEVDUAT HESABI','KREDİLİ MEVDUAT HESABI'),
    ('NORMAL HESAP','NORMAL HESAP'),
    ('EMEKLİLİK HESABI','EMEKLİLİK HESABI'),
)

class Currency(models.Model):
    currency_type = models.CharField(max_length=50)

    def __str__(self):
        return self.currency_type


class Accounts(models.Model):

    iban = models.CharField(max_length=60, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPE_CHOICES)
    currency_type = models.ForeignKey(Currency, null=True)
    user = models.ForeignKey(User, null=True, blank=True)
    amount = models.IntegerField()

    def __str__(self):
        return 'with ID : ' +  str(self.id)
        #return 'Account owner is : ' + self.user.first_name + ' IBAN no is : ' + self.iban


class Loan(models.Model):
    account = models.ForeignKey(Accounts)
    interest_rate = models.DecimalField(max_digits=4, decimal_places=2, blank=True, default=0)
    installment = models.IntegerField(default=1)
    start_date = models.DateField()
    finish_date = models.DateField()
    amount = models.IntegerField()
    delay_interest_rate = models.DecimalField(max_digits=4, decimal_places=2, blank=True, default=0)


class LoanAccountPayment(models.Model):
    account = models.ForeignKey(Accounts)
    loan = models.ForeignKey(Loan)
    installment_number = models.IntegerField()
    is_paid = models.BooleanField(default=False)
    finish_date = models.DateField()
    is_active = models.BooleanField(default=True)
    amount = models.IntegerField()

class Transaction(models.Model):

    description = models.CharField(max_length=800)
    amount = models.IntegerField()
    currency_type = models.ForeignKey(Currency)
    sourceaccount = models.ForeignKey(Accounts, related_name='source_account')
    destinationaccount = models.ForeignKey(Accounts, related_name='destination_account')
    sending_date = models.DateField()
    is_done = models.BooleanField(default=False)

    def make_transaction(self):
        source = get_object_or_404(Accounts, pk=self.sourceaccount.id)
        destination = get_object_or_404(Accounts, pk=self.destinationaccount.id)
        source.amount = source.amount - self.amount
        source.save()
        destination.amount = self.amount + self.amount
        destination.save()
        self.is_done = True
        self.save()
        return self

    def validate_transaction(self):
        """
        It validates transaction can be made or not.
        If there is not enough money transaction cannot be made
        :param transaction:
        :return:
        """
        if self.sourceaccount.amount > self.amount:
            return True
        else:
            return False

    def cancel_transaction(self):
        source = get_object_or_404(Accounts, pk=self.sourceaccount.id)
        destination = get_object_or_404(Accounts, pk=self.destinationaccount.id)
        source.amount = source.amount + self.amount
        source.save()
        destination.amount = destination.amount - self.amount
        destination.save()
        self.is_done = False
        self.save()
        return self

    def cancel_validate_transaction(self):
        """
        It validates transaction can be canceled,
        if there is not enough money destination account transaction cannot be cancel
        :param transaction:
        :return:
        """
        if self.destinationaccount.amount > self.amount:
            return True
        else:
            return False




