import django.conf
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django_testing.settings import MAX_STUDENTS_PER_COURSE
from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, data):
        if len(data['students']) > MAX_STUDENTS_PER_COURSE:
            raise ValidationError("students can't be more then 20")
        return data

