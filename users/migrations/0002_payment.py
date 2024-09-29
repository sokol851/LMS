# Generated by Django 4.2.16 on 2024-09-21 19:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("lms", "0005_remove_course_owner_remove_lesson_owner"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "data_payment",
                    models.DateField(auto_now_add=True, verbose_name="дата оплаты"),
                ),
                ("paid_summa", models.IntegerField(verbose_name="Сумма оплаты")),
                (
                    "paid_type",
                    models.CharField(
                        choices=[("Перевод", "Перевод"), ("Наличными", "Наличными")],
                        max_length=150,
                        verbose_name="Тип оплаты",
                    ),
                ),
                (
                    "paid_courses",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="lms.course",
                        verbose_name="Оплаченный курс",
                    ),
                ),
                (
                    "paid_lesson",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="lms.lesson",
                        verbose_name="Оплаченный урок",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
        ),
    ]
