# Generated by Django 5.1.1 on 2024-09-14 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_review_is_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='is_achieved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='booking',
            name='is_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
