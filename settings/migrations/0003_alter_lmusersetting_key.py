# Generated by Django 4.1.2 on 2023-01-02 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0002_alter_lmusersetting_options_lmusersetting_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lmusersetting',
            name='key',
            field=models.CharField(help_text='Settings key (must be unique - case insensitive)', max_length=50),
        ),
    ]
