# Generated by Django 4.1.5 on 2023-03-15 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emercado', '0068_role_remove_system_user_add_user_access_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='display_flag',
            field=models.IntegerField(default=1),
        ),
    ]