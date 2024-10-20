from datetime import timedelta, date

from celery import shared_task
from django.core.mail import send_mail

from django.conf import settings
from lms.models import Course, Subscription
from users.models import User


@shared_task
def sending_mail(course):
    email_list = []
    course = Course.objects.get(pk=course)
    subscriptions = Subscription.objects.filter(course=course)
    for subscription in subscriptions:
        email_list.append(subscription.user.email)
    subject_mail = f'Обновление материала в {course.name}!'
    text_mail = f'Оповещаем Вас, что в курсе {course.name} внесены изменения.'
    send_mail(subject_mail, text_mail, settings.EMAIL_HOST_USER, email_list, fail_silently=True)


@shared_task
def check_last_login():
    users = User.objects.filter(is_active=True, is_staff=False, is_superuser=False, last_login__isnull=False)
    date_delta = timedelta(30)
    for user in users:
        date_block = date.today() - date_delta
        if user.last_login.date() <= date_block:
            subject_mail = f'Аккаунт заблокирован!'
            text_mail = f'Оповещаем Вас, что аккаунт {user.email} заблокирован так как нет активности более 30 дней.'
            send_mail(subject_mail, text_mail, settings.EMAIL_HOST_USER, (user.email,), fail_silently=True)
            user.is_active = False
            user.save()
