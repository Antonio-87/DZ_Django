# Generated by Django 4.0.6 on 2022-08-01 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('measurement', '0003_alter_measurement_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]