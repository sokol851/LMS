# Generated by Django 4.2.16 on 2024-09-21 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lms", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="lesson",
            options={"verbose_name": "Урок", "verbose_name_plural": "Уроки"},
        ),
        migrations.AlterField(
            model_name="lesson",
            name="url_video",
            field=models.URLField(
                blank=True, null=True, verbose_name="Ссылка на видео"
            ),
        ),
    ]
