# Generated by Django 4.1.5 on 2023-02-26 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emercado', '0025_alter_orders_date_compeleted_alter_orders_date_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='service_fee',
            field=models.FloatField(default=0),
        ),
    ]
