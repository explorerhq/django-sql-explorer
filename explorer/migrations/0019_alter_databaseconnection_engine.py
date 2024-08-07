# Generated by Django 5.0.5 on 2024-07-03 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0018_alter_databaseconnection_host_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='databaseconnection',
            name='engine',
            field=models.CharField(choices=[('django.db.backends.sqlite3', 'SQLite3'), ('django.db.backends.postgresql', 'PostgreSQL'), ('django.db.backends.mysql', 'MySQL'), ('django.db.backends.oracle', 'Oracle'), ('django.db.backends.mysql', 'MariaDB'), ('django_cockroachdb', 'CockroachDB'), ('django.db.backends.sqlserver', 'SQL Server (mssql-django)')], max_length=255),
        ),
    ]
