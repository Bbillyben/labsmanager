# Generated by Django 4.1.2 on 2024-01-14 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infos', '0007_alter_contact_comment_alter_contactinfo_contact'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactinfo',
            options={'verbose_name': 'Contact Info'},
        ),
        migrations.AddField(
            model_name='contactinfotype',
            name='type',
            field=models.CharField(choices=[('none', 'None'), ('tel', 'Phone Number'), ('mail', 'EMail'), ('link', 'Link')], default='none', max_length=4, verbose_name='Type'),
        ),
        migrations.AddField(
            model_name='organizationinfostype',
            name='type',
            field=models.CharField(choices=[('none', 'None'), ('tel', 'Phone Number'), ('mail', 'EMail'), ('link', 'Link')], default='none', max_length=4, verbose_name='Type'),
        ),
    ]