# Generated by Django 4.1.2 on 2022-10-07 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0005_remove_employee_status_employee_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee_status',
            name='employee',
        ),
        migrations.AddField(
            model_name='employee_status',
            name='employee',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='staff.employee'),
            preserve_default=False,
        ),
    ]
