# Generated by Django 4.1.2 on 2022-10-07 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee_type',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='employee_type',
            name='shortname',
            field=models.CharField(max_length=10),
        ),
    ]
