# Generated by Django 4.2.13 on 2024-07-30 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0006_alter_lmprojectsetting_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lmprojectsetting',
            old_name='user',
            new_name='project',
        ),
    ]
