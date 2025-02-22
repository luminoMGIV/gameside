# Generated by Django 5.1.5 on 2025-01-29 18:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0007_alter_game_pegi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='cover',
            field=models.ImageField(blank=True, default='covers/default.jpg', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
