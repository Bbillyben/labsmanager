# Generated by Django 4.2.13 on 2024-07-28 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_remove_institution_adress'),
        ('settings', '0005_lmprojectsetting_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lmprojectsetting',
            name='user',
            field=models.ForeignKey(blank=True, help_text='Fund', null=True, on_delete=django.db.models.deletion.CASCADE, to='project.project', verbose_name='Fund'),
        ),
    ]