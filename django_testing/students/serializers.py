import django.conf
from rest_framework import serializers

from django_testing.settings import MAX_STUDENTS_PER_COURSE
from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate_students(self, value):
        """
        Check that the blog post is about Django.
        """
        if len(value) > MAX_STUDENTS_PER_COURSE:
            raise serializers.ValidationError("Max students in the course can't be more then 20")
        return value

