# Generated by Django 2.2.7 on 2019-11-23 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tradeApi', '0003_package_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='recipient',
            field=models.CharField(max_length=128),
        ),
    ]
