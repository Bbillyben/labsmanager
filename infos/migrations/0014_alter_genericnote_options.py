# Generated by Django 4.2.13 on 2024-07-28 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('infos', '0013_alter_genericnote_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='genericnote',
            options={'ordering': ['created_at'], 'verbose_name': 'Generic Notes'},
        ),
    ]
