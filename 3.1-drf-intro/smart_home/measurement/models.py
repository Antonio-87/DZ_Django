from django.db import models

class Sensor(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')
    temperature = models.DecimalField(max_digits=3, decimal_places=1)
    created_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='media', blank=True, default='ESP32.png')

    def __str__(self):
        return self.id_sensor

    class Meta:
        ordering = ['-created_at']