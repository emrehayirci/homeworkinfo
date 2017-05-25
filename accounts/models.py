from django.db import models
from django.utils import timezone
from users.models import User
# Create your models here.

class Currency(models.Model):
    currency_type = models.CharField(max_length=50)

    def __str__(self):
        return self.currency_type

class Accounts(models.Model):

    iban = models.CharField(max_length=60, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    account_type = models.CharField(max_length=50)
    currency_type = models.ForeignKey(Currency, null=True)
    user = models.ForeignKey(User, null=True, blank=True)
    amount = models.IntegerField()

    def __str__(self):
        return 'Account owner is : ' + self.user.first_name  + ' IBAN no is : ' + self.iban
