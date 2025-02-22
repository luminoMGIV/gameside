# Generated by Django 5.1.5 on 2025-01-28 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platform',
            name='logo',
            field=models.ImageField(blank=True, default='/logos/default.jpg', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='platform',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
