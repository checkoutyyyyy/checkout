# Generated by Django 4.1.5 on 2023-01-17 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emercado', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='weight',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='store_owner',
            name='custom_attributes',
            field=models.TextField(default='', null=True),
        ),
        migrations.AddField(
            model_name='store_owner',
            name='custom_category',
            field=models.TextField(default='', null=True),
        ),
    ]