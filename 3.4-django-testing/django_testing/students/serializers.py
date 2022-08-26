from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from students.models import Course, Student
from django.conf import settings


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, attrs):
        """Метод для валидации. Вызывается при создании и обновлении."""

        stud_count = Student.objects.count()
        if stud_count > settings.MAX_STUDENTS_PER_COURSE:
            raise ValidationError('Колличество студентов на курсе  превышено')
        return super().validate(attrs)