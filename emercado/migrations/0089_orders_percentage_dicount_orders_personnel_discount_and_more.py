# Generated by Django 4.1.5 on 2023-03-23 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emercado', '0088_discount_personnel'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='percentage_dicount',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='orders',
            name='personnel_discount',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='orders',
            name='total_personnel_discount',
            field=models.FloatField(default=0),
        ),
    ]
