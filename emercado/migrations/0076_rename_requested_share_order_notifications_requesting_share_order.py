# Generated by Django 4.1.5 on 2023-03-17 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emercado', '0075_rename_request_share_order_notifications_requested_share_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notifications',
            old_name='requested_share_order',
            new_name='requesting_share_order',
        ),
    ]
