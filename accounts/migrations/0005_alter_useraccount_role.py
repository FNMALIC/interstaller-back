# Generated by Django 5.0.7 on 2024-08-13 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_rename_interrest_useraccount_interest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='role',
            field=models.CharField(choices=[('agent_manager', 'Chief_Agent'), ('agent', 'Agent'), ('client', 'Client')], default=None, max_length=15, null=True),
        ),
    ]
