# Generated by Django 4.1.2 on 2023-02-14 15:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fund', '0014_alter_amounthistory_value_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='fund_item',
            name='entry_date',
            field=models.DateField(default=datetime.date.today, verbose_name='Entry Date'),
        ),
        migrations.AddField(
            model_name='fund_item',
            name='value_date',
            field=models.DateField(default=datetime.date.today, verbose_name='value Date'),
        ),
    ]