# Generated by Django 4.1.5 on 2023-02-24 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emercado', '0022_orders_service_instructions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='account_id',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
