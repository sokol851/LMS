# Generated by Django 4.2.16 on 2024-10-13 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_alter_payment_paid_courses_alter_payment_paid_lesson_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="link",
            field=models.URLField(
                blank=True, max_length=500, null=True, verbose_name="Cсылка на оплату"
            ),
        ),
        migrations.AddField(
            model_name="payment",
            name="session_id",
            field=models.CharField(
                blank=True, max_length=150, null=True, verbose_name="Сессия"
            ),
        ),
    ]
