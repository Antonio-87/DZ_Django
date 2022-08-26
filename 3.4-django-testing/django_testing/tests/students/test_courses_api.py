import random
import pytest
from django.urls import reverse
from rest_framework.status import is_success


@pytest.mark.django_db
def test_first_course(client, course_factory, student_factory):
    student = student_factory(_quantity=3)
    course = course_factory(students=student)

    response = client.get(reverse('courses-detail', args=[course.id]))

    assert is_success(response.status_code)
    assert  response.json()['id'] == course.id
    assert response.json()['name'] == course.name


@pytest.mark.django_db
def test_list_course(client, course_factory, student_factory):
    student = student_factory(_quantity=3)
    course = course_factory(students=student, _quantity=3)
    courses = [c.id for c in course]

    response = client.get(reverse('courses-list'))
    responses = [resp['id'] for resp in response.json()]
    
    assert is_success(response.status_code)
    assert len(responses) == 3
    assert courses == responses


@pytest.mark.django_db
def test_filter_id(client, course_factory, student_factory):
    student = student_factory(_quantity=3)
    course = course_factory(students=student, _quantity=5)
    random_id = random.choice(course).id

    response = client.get(reverse('courses-list'), {'id': random_id})

    assert is_success(response.status_code)
    assert  response.json()[0]
    assert response.json()[0]['id'] == random_id



@pytest.mark.django_db
def test_filter_name(client, course_factory, student_factory):
    student = student_factory(_quantity=3)
    course = course_factory(students=student, _quantity=5)
    random_name = random.choice(course).name

    response = client.get(reverse('courses-list'), {'name': random_name})

    assert is_success(response.status_code)
    assert  response.json()[0]
    assert response.json()[0]['name'] == random_name


@pytest.mark.django_db
def test_course_create(client):
    new_course = {'name': 'test_course_create'}
    url = reverse('courses-list')

    response = client.post(url, new_course)
    response_get = client.get(url, new_course)

    assert is_success(response.status_code)
    assert response_get.json()[0]
    assert response_get.json()[0]['name'] == new_course['name']


@pytest.mark.django_db
def test_course_update(client, course_factory, student_factory):
    student = student_factory(_quantity=3)
    old_course = course_factory(students=student)
    new_course = course_factory(students=student)

    response = client.patch(reverse('courses-detail', args=[old_course.id]), {'name': new_course.name})
    response_get = client.get(reverse('courses-detail', args=[old_course.id]))

    assert is_success(response.status_code)
    assert response.json()['id'] == old_course.id and response.json()['name'] == new_course.name
    assert response_get.json()['id'] == old_course.id and response_get.json()['name'] == new_course.name  


@pytest.mark.django_db
def test_course_delete(client, course_factory, student_factory):
    student = student_factory(_quantity=3)
    course = course_factory(students=student, _quantity=3)
    random_course = random.choice(course)

    response = client.delete(reverse('courses-detail', args=[random_course.id]))
    response_get = client.get(reverse('courses-list'))
    response_get_list = [course['id'] for course in response_get.json()]

    assert is_success(response.status_code)
    assert  random_course.id not in response_get_list


@pytest.mark.parametrize(
["settings", "expected_status"],
(
    ("19", 201),
    ("20", 201),
    ("21", 400),
)
)
@pytest.mark.django_db
def test_course_validate(client, settings, student_factory, expected_status):
    student = student_factory(_quantity=int(settings))
    course = {'name': 'test_course_create'}
    url = reverse('courses-list')

    response = client.post(url, course, students=student)

    assert response.status_code == expected_status

