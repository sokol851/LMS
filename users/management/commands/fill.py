from django.core.management import BaseCommand

from lms.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):

    def handle(self, *args, **options):
        course = {"id": 200, "name": "Backend", "description": "Бекенд-разработчик"}
        Course.objects.create(**course)

        lesson1 = {
            "id": 300,
            "name": "Знакомство с Python",
            "description": "Познакомимся с основами программирования",
            "course": Course.objects.get(pk=200),
        }

        lesson2 = {
            "id": 301,
            "name": "Погружение в профессию",
            "description": "Изучение",
            "course": Course.objects.get(pk=200),
        }

        [Lesson.objects.create(**lesson) for lesson in (lesson1, lesson2)]

        user1 = {"id": 50, "email": "user@test.ru"}
        user2 = {"id": 51, "email": "user2@test2.ru"}

        [User.objects.create(**user) for user in (user1, user2)]

        payment1 = {
            "user": User.objects.get(pk=50),
            "paid_courses": Course.objects.get(pk=200),
            "paid_lesson": Lesson.objects.get(pk=300),
            "paid_summa": 10000,
            "paid_type": "Перевод",
        }
        payment2 = {
            "user": User.objects.get(pk=50),
            "paid_courses": Course.objects.get(pk=200),
            "paid_lesson": Lesson.objects.get(pk=301),
            "paid_summa": 50000,
            "paid_type": "Наличными",
        }
        payment3 = {
            "user": User.objects.get(pk=51),
            "paid_courses": Course.objects.get(pk=200),
            "paid_lesson": Lesson.objects.get(pk=300),
            "paid_summa": 11000,
            "paid_type": "Наличными",
        }

        [
            Payment.objects.create(**payment)
            for payment in (payment1, payment2, payment3)
        ]
        print("Объекты успешно созданы.")
