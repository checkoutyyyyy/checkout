# Generated by Django 4.1.5 on 2023-03-17 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emercado', '0074_notifications'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notifications',
            old_name='request_share_order',
            new_name='requested_share_order',
        ),
    ]