# Generated by Django 3.1.7 on 2022-03-24 18:26

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20220324_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='photo',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='category',
            name='photo',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='Image'),
        ),
    ]
