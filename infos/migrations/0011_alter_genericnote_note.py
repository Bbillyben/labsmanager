# Generated by Django 4.2.13 on 2024-07-11 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infos', '0010_alter_contactinfotype_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genericnote',
            name='note',
            field=models.TextField(blank=True, null=True, verbose_name='note'),
        ),
    ]
