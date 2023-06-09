# Generated by Django 4.1.5 on 2023-01-18 07:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emercado', '0006_alter_product_images_product_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_attributes',
            name='product_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='emercado.products'),
        ),
        migrations.AlterField(
            model_name='product_images',
            name='product_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='emercado.products'),
        ),
    ]
