# Generated by Django 5.1.3 on 2024-12-05 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0014_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logo',
            name='logo',
            field=models.FileField(upload_to='logo'),
        ),
    ]
