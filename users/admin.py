from django.contrib import admin

from users.models import Payment, User


@admin.register(User)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "phone",
        "city",
        "is_active",
    )
    list_filter = (
        "is_active",
        "city",
    )
    search_fields = (
        "email",
        "first_name",
        "last_name",
        "phone",
        "city",
    )


@admin.register(Payment)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "data_payment",
        "paid_courses",
        "paid_lesson",
        "paid_summa",
        "paid_type",
    )
    list_filter = (
        "user",
        "data_payment",
        "paid_type",
    )
    search_fields = (
        "user",
        "data_payment",
    )
