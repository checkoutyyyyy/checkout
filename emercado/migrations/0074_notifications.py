# Generated by Django 4.1.5 on 2023-03-17 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emercado', '0073_orders_shared_to'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('consumer_id', models.IntegerField(null=True)),
                ('consumer_id_format', models.CharField(max_length=45, null=True)),
                ('request_share_order', models.IntegerField(null=True)),
                ('merchant_id', models.IntegerField(null=True)),
                ('order_id', models.IntegerField(null=True)),
                ('order_id_format', models.CharField(max_length=45, null=True)),
                ('merchant_id_format', models.CharField(max_length=45, null=True)),
                ('content', models.TextField(null=True)),
                ('images', models.TextField(null=True)),
                ('notif_type', models.CharField(max_length=50)),
                ('date_time', models.DateTimeField()),
                ('url', models.CharField(max_length=120)),
            ],
            options={
                'db_table': 'emcdo_notification',
            },
        ),
    ]