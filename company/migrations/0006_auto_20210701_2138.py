# Generated by Django 3.1.6 on 2021-07-01 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_auto_20210701_2130'),
    ]

    operations = [
        migrations.RenameField(
            model_name='companyinfo',
            old_name='company_mode',
            new_name='mode',
        ),
        migrations.AddField(
            model_name='companyfounder',
            name='email',
            field=models.EmailField(default='m@m.com', max_length=254, verbose_name='Email'),
            preserve_default=False,
        ),
    ]
