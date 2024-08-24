# Generated by Django 4.2.13 on 2024-07-28 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fund', '0020_budget_desc_contribution_desc'),
        ('settings', '0004_labsmanagersetting'),
    ]

    operations = [
        migrations.CreateModel(
            name='LMProjectSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(blank=True, help_text='Settings value', max_length=200)),
                ('key', models.CharField(help_text='Settings key (must be unique - case insensitive)', max_length=50)),
                ('user', models.ForeignKey(blank=True, help_text='Fund', null=True, on_delete=django.db.models.deletion.CASCADE, to='fund.fund', verbose_name='Fund')),
            ],
            options={
                'verbose_name': 'LabsManager Project Setting',
                'verbose_name_plural': 'LabsManager Project Settings',
            },
        ),
        migrations.AddConstraint(
            model_name='lmprojectsetting',
            constraint=models.UniqueConstraint(fields=('key', 'user'), name='unique key and fund'),
        ),
    ]