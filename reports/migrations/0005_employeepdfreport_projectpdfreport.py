# Generated by Django 4.1.2 on 2023-07-25 14:56

import django.core.validators
from django.db import migrations, models
import reports.models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_projectwordreport'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeePDFReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Template name', max_length=100, verbose_name='Name')),
                ('description', models.CharField(help_text='Report template description', max_length=250, verbose_name='Description')),
                ('revision', models.PositiveIntegerField(default=1, editable=False, help_text='Report revision number (auto-increments)', verbose_name='Revision')),
                ('filename_pattern', models.CharField(default='report.docx', help_text='Pattern for generating report filenames', max_length=100, verbose_name='Filename Pattern')),
                ('enabled', models.BooleanField(default=True, help_text='Report template is enabled', verbose_name='Enabled')),
                ('template', models.FileField(help_text='Report template file', upload_to=reports.models.rename_template, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['doc', 'docx'])], verbose_name='Template')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectPDFReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Template name', max_length=100, verbose_name='Name')),
                ('description', models.CharField(help_text='Report template description', max_length=250, verbose_name='Description')),
                ('revision', models.PositiveIntegerField(default=1, editable=False, help_text='Report revision number (auto-increments)', verbose_name='Revision')),
                ('filename_pattern', models.CharField(default='report.docx', help_text='Pattern for generating report filenames', max_length=100, verbose_name='Filename Pattern')),
                ('enabled', models.BooleanField(default=True, help_text='Report template is enabled', verbose_name='Enabled')),
                ('template', models.FileField(help_text='Report template file', upload_to=reports.models.rename_template, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['doc', 'docx'])], verbose_name='Template')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
