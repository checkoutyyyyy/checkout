# Generated by Django 4.1.1 on 2023-02-24 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emercado', '0021_alter_consumer_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumer',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_default.jpg', null=True, upload_to='profile/img'),
        ),
    ]
