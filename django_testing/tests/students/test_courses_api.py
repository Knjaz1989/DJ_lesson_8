import pytest
from model_bakery import baker
from rest_framework.test import APIClient

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
    Course.objects.create(name='python-developer')
    first = Course.objects.first()

    response = client.get('/courses/1/')

    assert response.status_code == 200
    data = response.json()
    assert first.name == data['name']


@pytest.mark.django_db
def test_get_list(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get('/courses/')

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10


@pytest.mark.django_db
def test_get_list_by_id_filter(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get('/courses/?id=7')

    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == courses[6].id


@pytest.mark.django_db
def test_get_list_by_name_filter(client, course_factory,):
    courses = course_factory(_quantity=10)
    id_7_name = courses[6].name

    response = client.get(f'/courses/?name={id_7_name}')

    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == id_7_name


@pytest.mark.django_db
def test_create_course(client):
    data = {'name': 'python-developer'}

    response = client.post('/courses/', data=data)

    assert response.status_code == 201
    course = Course.objects.first()
    assert course.name == data['name']


@pytest.mark.django_db
def test_patch_course(client, course_factory):
    course = course_factory()
    data = {'name': 'python-developer'}

    response = client.patch('/courses/1/', data=data)

    assert response.status_code == 200
    course = Course.objects.first()
    assert course.name == data['name']


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory()

    response = client.delete('/courses/1/')

    assert response.status_code == 204
    assert Course.objects.count() == 0


# Доп. задание
@pytest.mark.parametrize("student_count, expected_result", [(1, True), (21, False)])
def test_validation(settings, student_count, expected_result):

    assert (settings.MAX_STUDENTS_PER_COURSE >= student_count) == expected_result
