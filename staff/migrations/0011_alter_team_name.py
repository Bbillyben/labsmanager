# Generated by Django 4.1.2 on 2023-09-07 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0010_alter_employee_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=70, unique=True, verbose_name='Team Name'),
        ),
    ]
