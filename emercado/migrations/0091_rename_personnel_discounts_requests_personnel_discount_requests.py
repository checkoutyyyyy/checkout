# Generated by Django 4.1.5 on 2023-03-24 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emercado', '0090_personnel_discounts_requests_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Personnel_Discounts_Requests',
            new_name='Personnel_Discount_Requests',
        ),
    ]
