# Generated by Django 4.2.8 on 2024-04-26 13:05

from django.db import migrations, models


def insert_assistant_prompt(apps, schema_editor):

    ExplorerValue = apps.get_model('explorer', 'ExplorerValue')
    ExplorerValue.objects.get_or_create(
        key="ASP",
        value="""You are a data analyst's assistant and will be asked write or modify a SQL query to assist a business
user with their analysis. The user will provide a prompt of what they are looking for help with, and may also
provide SQL they have written so far, relevant table schema, and sample rows from the tables they are querying.

For complex requests, you may use Common Table Expressions (CTEs) to break down the problem into smaller parts.
CTEs are not needed for simpler requests.
"""
    )

def insert_assistant_prompt_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0015_explorervalue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='explorervalue',
            name='key',
            field=models.CharField(choices=[('UUID', 'Install Unique ID'), ('SMLS', 'Startup metric last send'), ('ASP', 'System prompt for SQL Assistant')], max_length=5, unique=True),
        ),
        migrations.RunPython(insert_assistant_prompt, reverse_code=insert_assistant_prompt_reverse),
    ]
