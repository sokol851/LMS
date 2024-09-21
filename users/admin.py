from django.contrib import admin

from users.models import User


@admin.register(User)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone', 'city', 'is_active',)
    list_filter = ('is_active', 'city',)
    search_fields = ('email', 'first_name', 'last_name', 'phone', 'city',)
