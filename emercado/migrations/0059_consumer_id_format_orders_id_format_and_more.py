# Generated by Django 4.1.5 on 2023-03-09 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emercado', '0058_alter_product_attributes_product_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumer',
            name='id_format',
            field=models.CharField(default='', max_length=45),
        ),
        migrations.AddField(
            model_name='orders',
            name='id_format',
            field=models.CharField(default='', max_length=45),
        ),
        migrations.AddField(
            model_name='products',
            name='id_format',
            field=models.CharField(default='', max_length=45),
        ),
        migrations.AddField(
            model_name='store_info',
            name='id_format',
            field=models.CharField(default='', max_length=45),
        ),
    ]