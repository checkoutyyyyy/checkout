# Generated by Django 4.1.5 on 2023-03-09 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emercado', '0065_merge_20230309_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='date_created',
            field=models.DateTimeField(null=True),
        ),
    ]
