# Generated by Django 3.1.6 on 2021-07-01 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0006_auto_20210701_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyemailhelpline',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company'),
        ),
        migrations.AlterField(
            model_name='companyfounder',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company'),
        ),
        migrations.AlterField(
            model_name='companytelephonehelpline',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company'),
        ),
    ]
