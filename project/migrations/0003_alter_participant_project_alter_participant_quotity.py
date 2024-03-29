# Generated by Django 4.1.2 on 2023-01-02 11:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_alter_institution_options_alter_project_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participant_project', to='project.project', verbose_name='Project'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='quotity',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)], verbose_name='Time quotity'),
        ),
    ]
