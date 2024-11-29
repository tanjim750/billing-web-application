# Generated by Django 4.2.14 on 2024-11-27 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0008_booking_advance_rent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='payment_status',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='total_due',
        ),
        migrations.AddField(
            model_name='monthlypayment',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
    ]