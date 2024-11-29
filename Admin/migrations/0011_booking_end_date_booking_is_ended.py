# Generated by Django 4.2.14 on 2024-11-29 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0010_remove_booking_advance_rent'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='is_ended',
            field=models.BooleanField(default=False),
        ),
    ]
