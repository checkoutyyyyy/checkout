# Generated by Django 4.1.1 on 2023-03-29 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emercado', '0098_consumer_account_verification_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='store_info',
            name='latitude',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='store_info',
            name='longitude',
            field=models.FloatField(default=0.0),
        ),
    ]
