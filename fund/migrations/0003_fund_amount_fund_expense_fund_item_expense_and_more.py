# Generated by Django 4.1.2 on 2022-11-25 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fund', '0002_alter_fund_options_alter_fund_institution_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='fund',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True, verbose_name='Amount'),
        ),
        migrations.AddField(
            model_name='fund',
            name='expense',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True, verbose_name='Expense'),
        ),
        migrations.AddField(
            model_name='fund_item',
            name='expense',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True, verbose_name='Expense'),
        ),
        migrations.AlterField(
            model_name='fund_item',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True, verbose_name='Amount'),
        ),
    ]
