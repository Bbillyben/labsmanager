# Generated by Django 4.1.2 on 2023-01-31 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fund', '0006_fund_end date should be greater than start date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fund',
            name='is_active',
        ),
        migrations.AlterField(
            model_name='fund',
            name='start_date',
            field=models.DateField(blank=True, null=True, verbose_name='Start Date'),
        ),
    ]
