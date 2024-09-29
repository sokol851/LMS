from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from lms.models import Course, Lesson
from users.models import Payment, User
from django.contrib.auth.models import Group


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Создаём группу модераторов
        Group.objects.get_or_create(id=1, name='Moderator')

        # Создаём пользователей
        user1 = {"id": 50, "email": "user@pow.ru", }
        user2 = {"id": 51, "email": "user2@pow.ru", }
        [User.objects.create(**user) for user in (user1, user2)]

        user_1 = User.objects.get(id=50)
        user_1.set_password("12345")
        user_1.save()

        user_2 = User.objects.get(id=51)
        user_2.set_password("12345")
        user_2.save()

        # Создаём курсы
        course = {"id": 200, "name": "Backend", "description": "Бекенд-разработчик", "owner": User.objects.get(id=50), }
        Course.objects.create(**course)

        # Создаём уроки
        lesson1 = {
            "id": 300,
            "name": "Знакомство с Python",
            "description": "Познакомимся с основами программирования",
            "course": Course.objects.get(pk=200),
            "owner": User.objects.get(id=50),
        }

        lesson2 = {
            "id": 301,
            "name": "Погружение в профессию",
            "description": "Изучение",
            "course": Course.objects.get(pk=200),
            "owner": User.objects.get(id=51),
        }

        [Lesson.objects.create(**lesson) for lesson in (lesson1, lesson2)]

        # Создаём оплаты
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
        print("Объекты успешно созданы.\n"
              "Пользователи:\n"
              "user@pow.ru - 12345\n"
              "user2@pow.ru - 12345")
