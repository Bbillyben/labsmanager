# Generated by Django 4.1.2 on 2022-10-11 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=150)),
                ('adress', models.CharField(blank=True, max_length=150, null=True)),
            ],
            options={
                'verbose_name': 'Lab Institution',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Project Name')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End Date')),
                ('status', models.BooleanField(default=True, verbose_name='Project Status')),
            ],
            options={
                'verbose_name': 'project',
            },
        ),
        migrations.CreateModel(
            name='Institution_Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('c', 'Coordinator'), ('p', 'Participant')], default='p', max_length=1, verbose_name='Status')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.institution', verbose_name='Institution')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.project', verbose_name='Project')),
            ],
            options={
                'verbose_name': 'Partner Institution',
            },
        ),
    ]
