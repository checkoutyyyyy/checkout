# Generated by Django 4.1.1 on 2023-03-02 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emercado', '0038_rename_date_compeleted_orders_date_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='profile_picture',
            field=models.CharField(max_length=120, null=True),
        ),
    ]
