from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта")
    first_name = models.CharField(
        max_length=150, default="Не указано", verbose_name="Имя", **NULLABLE
    )
    last_name = models.CharField(
        max_length=150, default="Не указано", verbose_name="Фамилия", **NULLABLE
    )
    phone = models.CharField(
        max_length=35, verbose_name="Телефон", **NULLABLE, default="Не указано"
    )
    city = models.CharField(
        max_length=50, verbose_name="Город", **NULLABLE, default="Не указано"
    )
    avatar = models.ImageField(
        upload_to="users/%Y",
        default="users/non_avatar.png",
        verbose_name="Аватар",
        **NULLABLE,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    REMITTANCE = "Перевод"
    CASH = "Наличными"

    PAID_TYPE = ((REMITTANCE, "Перевод"), (CASH, "Наличными"))

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    data_payment = models.DateField(auto_now_add=True, verbose_name="дата оплаты")
    paid_courses = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name="Оплата курса", **NULLABLE)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, verbose_name="Оплата урока", **NULLABLE)
    paid_summa = models.IntegerField(default=0, verbose_name="Сумма оплаты в рублях", **NULLABLE)
    paid_type = models.CharField(max_length=150, choices=PAID_TYPE, verbose_name="Тип оплаты")
    session_id = models.CharField(max_length=150, verbose_name='Сессия', **NULLABLE)
    link = models.URLField(max_length=500, verbose_name='Cсылка на оплату', **NULLABLE)

    def __str__(self):
        return f"{self.user} - {self.paid_summa} ({self.data_payment})"

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплата"
