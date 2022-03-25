# Generated by Django 3.1.7 on 2022-03-24 18:20

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='logo',
        ),
        migrations.AddField(
            model_name='brand',
            name='photo',
            field=cloudinary.models.CloudinaryField(default=1, max_length=255, verbose_name='Image'),
            preserve_default=False,
        ),
    ]
