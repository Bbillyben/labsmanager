# Generated by Django 4.1.2 on 2023-02-16 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0007_alter_genericinfotype_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email'),
        ),
    ]
