# Generated by Django 4.1.5 on 2023-02-26 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emercado', '0028_alter_cart_product_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='account_id',
            field=models.CharField(max_length=45, null=True),
        ),
    ]
