# Generated by Django 4.1.1 on 2023-03-09 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emercado', '0058_alter_product_attributes_product_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='qr_code',
            field=models.ImageField(blank=True, upload_to='qr_codes/'),
        ),
    ]
