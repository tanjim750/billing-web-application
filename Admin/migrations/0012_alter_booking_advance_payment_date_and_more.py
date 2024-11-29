# Generated by Django 4.2.14 on 2024-11-29 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0011_booking_end_date_booking_is_ended'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='advance_payment_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='date_created',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='last_payment_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='rent_start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]