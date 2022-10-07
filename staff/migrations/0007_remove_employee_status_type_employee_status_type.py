# Generated by Django 4.1.2 on 2022-10-07 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0006_remove_employee_status_employee_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee_status',
            name='type',
        ),
        migrations.AddField(
            model_name='employee_status',
            name='type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='staff.employee_type'),
            preserve_default=False,
        ),
    ]
