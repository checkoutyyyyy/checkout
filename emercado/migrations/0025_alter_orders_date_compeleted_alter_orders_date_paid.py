# Generated by Django 4.1.5 on 2023-02-26 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emercado', '0024_merge_20230224_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='date_compeleted',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='date_paid',
            field=models.DateTimeField(null=True),
        ),
    ]
