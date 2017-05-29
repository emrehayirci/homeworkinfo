from django.contrib import admin
from .models import Accounts, Currency, Transaction
# Register your models here.
admin.site.register(Accounts)
admin.site.register(Currency)
admin.site.register(Transaction)
