# Generated by Django 4.1.2 on 2023-01-18 16:05

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0002_leave_color_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leave',
            name='color',
        ),
        migrations.AddField(
            model_name='leave_type',
            name='color',
            field=colorfield.fields.ColorField(default='#FF0000', image_field=None, max_length=18, samples=None),
        ),
    ]
