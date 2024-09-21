from django.core.management import BaseCommand

from lms.models import Lesson, Course
from users.models import User, Payment


class Command(BaseCommand):

    def handle(self, *args, **options):
        course = {"id": 200, "name": "Backend", "description": "Бекенд-разработчик"}
        Course.objects.create(**course)

        lesson = {"id": 300, "name": "Знакомство с Python", "description": "Познакомимся с основами программирования",
                  "course": Course.objects.get(pk=200)}

        Lesson.objects.create(**lesson)

        user = {"id": 50, "email": "user@test.ru"}

        User.objects.create(**user)

        payment = {"user": User.objects.get(pk=50), "paid_courses": Course.objects.get(pk=200), "paid_lesson": Lesson.objects.get(pk=300),
                   "paid_summa": 10000, "paid_type": "Перевод"}

        Payment.objects.create(**payment)
        print('Объекты успешно созданы.')
