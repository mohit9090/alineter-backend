# Generated by Django 3.1.6 on 2021-06-07 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_page', '0002_auto_20210607_1411'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='username',
        ),
    ]
