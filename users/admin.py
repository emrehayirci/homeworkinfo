from django.contrib import admin
from .models import User, Address
# Register your models here.
admin.site.register(Address)
admin.site.register(User)