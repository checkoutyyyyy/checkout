# Generated by Django 4.1.1 on 2023-03-31 03:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emercado', '0103_store_info_store_city_store_info_store_country_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store_info',
            name='store_city',
        ),
        migrations.RemoveField(
            model_name='store_info',
            name='store_country',
        ),
        migrations.RemoveField(
            model_name='store_info',
            name='store_postal_code',
        ),
        migrations.RemoveField(
            model_name='store_info',
            name='store_state',
        ),
        migrations.RemoveField(
            model_name='store_info',
            name='store_street',
        ),
    ]
