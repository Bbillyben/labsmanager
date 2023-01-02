# Generated by Django 4.1.2 on 2023-01-02 11:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0002_alter_expense_fund_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='quotity',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)], verbose_name='Time quotity'),
        ),
    ]
