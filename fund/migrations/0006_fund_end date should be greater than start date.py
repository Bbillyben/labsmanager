# Generated by Django 4.1.2 on 2023-01-29 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fund', '0005_alter_fund_amount_alter_fund_expense_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='fund',
            constraint=models.CheckConstraint(check=models.Q(('end_date__gt', models.F('start_date'))), name='End Date should be greater than start date'),
        ),
    ]
