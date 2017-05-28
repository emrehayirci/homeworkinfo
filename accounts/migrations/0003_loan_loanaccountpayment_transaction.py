# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-28 19:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20170525_0835'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interest_rate', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=4)),
                ('installment', models.IntegerField(default=1)),
                ('start_date', models.DateField()),
                ('finish_date', models.DateField()),
                ('amount', models.IntegerField()),
                ('delay_interest_rate', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=4)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Accounts')),
            ],
        ),
        migrations.CreateModel(
            name='LoanAccountPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('installment_number', models.IntegerField()),
                ('is_paid', models.BooleanField(default=False)),
                ('finish_date', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Accounts')),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Loan')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=800)),
                ('amount', models.IntegerField()),
                ('sending_date', models.DateField()),
                ('currency_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Currency')),
                ('destinationaccount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_account', to='accounts.Accounts')),
                ('sourceaccount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_account', to='accounts.Accounts')),
            ],
        ),
    ]
