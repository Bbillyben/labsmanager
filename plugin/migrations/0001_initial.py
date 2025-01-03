# Generated by Django 4.2.13 on 2024-09-21 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PluginConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, help_text='Key of plugin', max_length=255, unique=True, verbose_name='Key')),
                ('name', models.CharField(blank=True, help_text='PluginName of the plugin', max_length=255, null=True, verbose_name='Name')),
                ('active', models.BooleanField(default=False, help_text='Is the plugin active', verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Plugin Configuration',
                'verbose_name_plural': 'Plugin Configurations',
            },
        ),
        migrations.CreateModel(
            name='PluginSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(help_text='Settings key (must be unique - case insensitive)', max_length=50)),
                ('value', models.CharField(blank=True, help_text='Settings value', max_length=200)),
                ('plugin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='settings', to='plugin.pluginconfig', verbose_name='Plugin')),
            ],
            options={
                'unique_together': {('plugin', 'key')},
            },
        ),
    ]
