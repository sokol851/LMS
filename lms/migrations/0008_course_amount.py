# Generated by Django 4.2.16 on 2024-10-13 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lms", "0007_subscription"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="amount",
            field=models.IntegerField(default=0, verbose_name="Стоимость курса"),
        ),
    ]
