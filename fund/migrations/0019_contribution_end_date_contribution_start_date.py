# Generated by Django 4.1.2 on 2023-04-05 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fund', '0018_alter_budget_amount_contribution'),
    ]

    operations = [
        migrations.AddField(
            model_name='contribution',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='End Date'),
        ),
        migrations.AddField(
            model_name='contribution',
            name='start_date',
            field=models.DateField(blank=True, null=True, verbose_name='Start Date'),
        ),
    ]
