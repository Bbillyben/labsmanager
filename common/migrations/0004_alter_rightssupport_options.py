# Generated by Django 4.1.2 on 2023-11-30 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_rightssupport'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rightssupport',
            options={'default_permissions': 'view', 'managed': False, 'permissions': (('employee_list', 'Permission to see employee list'), ('team_list', 'Permission to see team list'), ('project_list', 'Permission to see project list'), ('display_calendar', 'Permission to see main calendar'), ('display_dashboard', 'Permission to see dasgboard'))},
        ),
    ]
