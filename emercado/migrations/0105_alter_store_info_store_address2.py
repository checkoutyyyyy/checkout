# Generated by Django 4.1.1 on 2023-04-03 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emercado', '0104_remove_store_info_store_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store_info',
            name='store_address2',
            field=models.CharField(default='', max_length=300),
        ),
    ]
