# Generated by Django 4.1.2 on 2022-11-05 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'ordering': ['first_name'], 'verbose_name': 'Employee', 'verbose_name_plural': 'Employee'},
        ),
        migrations.AlterModelOptions(
            name='employee_type',
            options={'ordering': ['name'], 'verbose_name': 'Employee Type'},
        ),
    ]
