# Generated by Django 4.1.2 on 2022-10-26 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0004_remove_contract_contract_type_contract_contract_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Contract is active'),
        ),
    ]
