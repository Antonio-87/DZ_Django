# Generated by Django 4.0.6 on 2022-08-01 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('measurement', '0006_alter_measurement_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='image',
            field=models.ImageField(blank=True, default='ESP32.png', upload_to='media'),
        ),
    ]
