# Generated by Django 4.1.5 on 2023-03-24 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emercado', '0091_rename_personnel_discounts_requests_personnel_discount_requests'),
    ]

    operations = [
        migrations.AddField(
            model_name='personnel_discount_requests',
            name='file',
            field=models.CharField(max_length=120, null=True),
        ),
    ]
