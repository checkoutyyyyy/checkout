# Generated by Django 4.1.1 on 2023-03-09 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emercado', '0062_alter_line_items_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='line_items',
            name='order_id',
            field=models.CharField(max_length=45),
        ),
    ]