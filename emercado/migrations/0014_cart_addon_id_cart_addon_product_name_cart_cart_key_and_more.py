# Generated by Django 4.1.5 on 2023-02-09 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emercado', '0013_cart_cart_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='addon_id',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='addon_product_name',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='cart_key',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='cart',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='cart',
            name='total',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='cart',
            name='variation_id',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='variation_name',
            field=models.CharField(max_length=120, null=True),
        ),
    ]