# Generated by Django 4.1.2 on 2023-03-20 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fund', '0016_alter_fund_item_fund'),
    ]

    operations = [
        migrations.AddField(
            model_name='cost_type',
            name='in_focus',
            field=models.BooleanField(default=True, verbose_name='In Focus'),
        ),
        migrations.AddField(
            model_name='fund',
            name='amount_f',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True, verbose_name='Focus Amount'),
        ),
        migrations.AddField(
            model_name='fund',
            name='expense_f',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True, verbose_name='Focus Expense'),
        ),
    ]