# Generated by Django 4.1.5 on 2023-02-02 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emercado', '0010_product_addons'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_variations',
            name='available_flag',
            field=models.IntegerField(default=1),
        ),
    ]
