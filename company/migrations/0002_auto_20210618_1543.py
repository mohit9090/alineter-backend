# Generated by Django 3.1.6 on 2021-06-18 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyreview',
            name='rating',
            field=models.PositiveIntegerField(verbose_name='Rating'),
        ),
    ]