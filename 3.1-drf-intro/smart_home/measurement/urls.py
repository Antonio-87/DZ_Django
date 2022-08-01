from django.urls import path
from .views import MeasurementView_add, SensorRUD, SensorView_add

urlpatterns = [
    path('sensors/', SensorView_add.as_view()),
    path('sensors/<pk>/', SensorRUD.as_view()),
    path('measurements/', MeasurementView_add.as_view()),
]
