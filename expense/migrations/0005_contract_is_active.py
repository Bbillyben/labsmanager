# Generated by Django 4.1.2 on 2023-01-31 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0004_remove_contract_is_active_alter_contract_end_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is Active'),
        ),
    ]
