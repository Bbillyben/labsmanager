# Generated by Django 4.1.2 on 2023-06-27 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0008_employee_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='first_name',
            field=models.CharField(max_length=40, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='last_name',
            field=models.CharField(max_length=40, verbose_name='Last Name'),
        ),
    ]
