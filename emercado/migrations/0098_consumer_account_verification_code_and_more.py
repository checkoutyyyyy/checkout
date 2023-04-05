# Generated by Django 4.1.1 on 2023-03-27 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emercado', '0097_orders_discounted_flag'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumer',
            name='account_verification_code',
            field=models.CharField(max_length=45, null=True),
        ),
        migrations.AddField(
            model_name='consumer',
            name='account_verification_expiry',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='consumer',
            name='account_verification_flag',
            field=models.IntegerField(default=0),
        ),
    ]