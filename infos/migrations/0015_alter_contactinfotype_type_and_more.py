# Generated by Django 4.2.13 on 2024-08-29 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infos', '0014_alter_genericnote_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactinfotype',
            name='type',
            field=models.CharField(choices=[('none', 'None'), ('tel', 'Phone Number'), ('mail', 'EMail'), ('link', 'Link'), ('addr', 'Address')], default='none', max_length=4, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='organizationinfostype',
            name='type',
            field=models.CharField(choices=[('none', 'None'), ('tel', 'Phone Number'), ('mail', 'EMail'), ('link', 'Link'), ('addr', 'Address')], default='none', max_length=4, verbose_name='Type'),
        ),
    ]
