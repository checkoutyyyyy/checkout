# Generated by Django 4.1.1 on 2023-03-17 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emercado', '0073_store_info_store_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store_info',
            name='store_address2',
            field=models.CharField(default='', max_length=120),
        ),
    ]
