# Generated by Django 4.2.13 on 2024-08-01 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fund', '0020_budget_desc_contribution_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='cost_type',
            name='is_hr',
            field=models.BooleanField(default=False, verbose_name='Is Human Resources'),
        ),
    ]