# Generated by Django 4.1.1 on 2023-04-04 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emercado', '0105_alter_store_info_store_address2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumer',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_default.jpg', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='store_info',
            name='profile_pic',
            field=models.CharField(blank=True, default='cart_logo.png', max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='store_info',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_default.jpg', null=True, upload_to=''),
        ),
    ]
