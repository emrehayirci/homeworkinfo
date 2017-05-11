from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
class Accounts(models.Model):

    iban = models.CharField(max_length=60, blank=True)
    created_at = models.DateTimeField(default=timezone.now())
    account_type = models.CharField(max_length=50)
    currency_type = models.CharField(max_length=50)
    user = models.ForeignKey(User)
    amount = models.IntegerField()
