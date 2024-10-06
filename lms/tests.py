from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from lms.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    """Тестирует CRUD занятий курса"""

    def setUp(self):
        self.user = User.objects.create(email="test@test.ru", password="12345")
        self.moderator = User.objects.create(
            email="moderator@test.ru", password="12345"
        )
        moderators_group = Group.objects.create(name="moderators")
        moderators_group.user_set.add(self.moderator)
        self.course = Course.objects.create(name="Test course", owner=self.user)
        self.lesson = Lesson.objects.create(name="Test lesson 1", course=self.course, owner=self.user)

    def test_lesson_list(self):
        url = reverse("lms:lesson-list")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data.get("results")), Lesson.objects.count())
        self.assertEqual(data.get("results"),
                         [{'id': 1,
                           'name': 'Test lesson 1',
                           'description': None,
                           'preview': 'http://testserver/lesson/non_lesson.png',
                           'url_video': None,
                           'course': 1,
                           'owner': 1}]
                         )

    def test_lesson_create(self):
        url = reverse("lms:lesson-create")
        self.client.force_authenticate(user=self.user)
        data = {"name": "Test lesson 2", "course": self.course.id, "owner": self.user.id}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertEqual(data.get("name"), data.get("name"))

    def test_lesson_create_with_youtube(self):
        url = reverse("lms:lesson-create")
        self.client.force_authenticate(user=self.user)
        data = {"name": "Test lesson 3", "course": self.course.id, "url_video": "https://www.youtube.com/",
                "owner": self.user.id}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertEqual(data.get("name"), "Test lesson 3")

    def test_lesson_create_with_not_youtube(self):
        url = reverse("lms:lesson-create")
        self.client.force_authenticate(user=self.user)
        data = {"name": "Test lesson 4", "course": self.course.id, "url_video": "https://www.yandex.com/",
                "owner": self.user.id}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_lesson_update(self):
        url = reverse("lms:lesson-update", args=(self.lesson.pk,))
        self.client.force_authenticate(user=self.user)
        data = {
            'name': 'Test lesson 5',
            'description': 'test desc 5',
            'course': self.course.pk,
            'owner': self.user.pk
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), 'Test lesson 5')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_delete(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('lms:lesson-delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_delete_as_moderator(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse('lms:lesson-delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('lms:subscription')
        self.user = User.objects.create(email="test@test.ru", password="12345")
        self.course = Course.objects.create(name="Test course", owner=self.user)
        self.subscription = Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        Subscription.objects.all().delete()
        data = {'course': self.course.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')

    def test_subscription_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        data = response.json()
        self.assertEqual(data[0].get('id'), self.course.id)
        self.assertEqual(data[0], {'id': 1, 'user_id': 1, 'course_id': 1})

    def test_subscribe_course_is_none(self):
        Subscription.objects.all().delete()
        data = {'course_id': ''}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_subscribe_not_is_auth(self):
        Subscription.objects.all().delete()
        self.client.force_authenticate(user='')
        data = {'course_id': self.course.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
