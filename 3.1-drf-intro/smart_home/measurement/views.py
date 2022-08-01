from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Sensor, Measurement
from .serializers import MeasurementSerializer, SensorSerialiser, SensorDetailSerializer

class SensorView_add(ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerialiser


class SensorRUD(RetrieveUpdateDestroyAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer


class MeasurementView_add(ListCreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
