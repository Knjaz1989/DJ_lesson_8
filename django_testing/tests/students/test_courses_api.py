import pytest

from django.urls import reverse
from model_bakery import baker
from rest_framework.exceptions import ValidationError
from _pytest.compat import nullcontext as does_not_raise
from rest_framework.test import APIClient
from students.serializers import CourseSerializer
import django_testing.settings as sett
from students.models import Student, Course


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def settings():
    return sett


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_get_first_course(client):
    course = Course.objects.create(name='python-developer')
    url = reverse('courses-detail', args=[course.id])

    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert course.name == data['name']


@pytest.mark.django_db
def test_get_list(client, course_factory):
    courses = course_factory(_quantity=10)
    url = reverse('courses-list')

    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10


@pytest.mark.django_db
def test_get_list_by_id_filter(client, course_factory):
    courses = course_factory(_quantity=10)
    url = reverse('courses-list')

    response = client.get(f'{url}?id={courses[6].id}')

    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == courses[6].id


@pytest.mark.django_db
def test_get_list_by_name_filter(client, course_factory,):
    courses = course_factory(_quantity=10)
    id_7_name = courses[6].name
    url = reverse('courses-list')

    response = client.get(f'{url}?name={id_7_name}')

    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == id_7_name


@pytest.mark.django_db
def test_create_course(client):
    data = {'name': 'python-developer'}
    url = reverse('courses-list')

    response = client.post(f'{url}', data=data)

    assert response.status_code == 201
    course = Course.objects.first()
    assert course.name == data['name']


@pytest.mark.django_db
def test_patch_course(client, course_factory):
    course = course_factory()
    data = {'name': 'python-developer'}
    url = reverse('courses-detail', args=[course.id])

    response = client.patch(url, data=data)

    assert response.status_code == 200
    course = Course.objects.first()
    assert course.name == data['name']


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory()
    url = reverse('courses-detail', args=[course.id])

    response = client.delete(url)

    assert response.status_code == 204
    assert Course.objects.count() == 0


# Доп. задание
test_values = [
    (1, does_not_raise()),
    (21, pytest.raises(ValidationError))
]


@pytest.mark.django_db
@pytest.mark.parametrize("students_count, expected_result", test_values)
def test_validation(student_factory, students_count, expected_result):
    students_id = [student.id for student in student_factory(_quantity=students_count)]

    with expected_result:
        assert CourseSerializer().validate_students(value=students_id)
