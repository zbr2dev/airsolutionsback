# Generated by Django 2.2.7 on 2019-11-22 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tradeApi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='dailyProfit',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='firstName',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='lastName',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='money',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='region',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
