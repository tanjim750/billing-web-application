# Generated by Django 4.2.14 on 2024-11-27 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0007_booking_rent_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='advance_rent',
            field=models.FloatField(default=0),
        ),
    ]
