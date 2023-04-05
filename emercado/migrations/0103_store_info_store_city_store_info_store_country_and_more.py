# Generated by Django 4.1.1 on 2023-03-31 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emercado', '0102_merge_20230331_0756'),
    ]

    operations = [
        migrations.AddField(
            model_name='store_info',
            name='store_city',
            field=models.CharField(default='', max_length=120),
        ),
        migrations.AddField(
            model_name='store_info',
            name='store_country',
            field=models.CharField(default='', max_length=120),
        ),
        migrations.AddField(
            model_name='store_info',
            name='store_postal_code',
            field=models.CharField(default='', max_length=120),
        ),
        migrations.AddField(
            model_name='store_info',
            name='store_state',
            field=models.CharField(default='', max_length=120),
        ),
        migrations.AddField(
            model_name='store_info',
            name='store_street',
            field=models.CharField(default='', max_length=120),
        ),
        migrations.AlterField(
            model_name='store_info',
            name='store_address2',
            field=models.CharField(default='', max_length=120),
        ),
    ]