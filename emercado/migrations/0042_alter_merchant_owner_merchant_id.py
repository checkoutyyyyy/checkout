# Generated by Django 4.1.1 on 2023-03-02 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emercado', '0041_merchant_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchant_owner',
            name='merchant_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]