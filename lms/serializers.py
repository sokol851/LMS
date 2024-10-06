from rest_framework import serializers

from lms.models import Course, Lesson, Subscription
from lms.validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [UrlValidator(field='url_video')]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    course_subscribe = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            "name",
            "preview",
            "description",
            "lesson_count",
            "lessons",
            "owner",
            "course_subscribe",
        )

    @staticmethod
    def get_lesson_count(instance):
        lesson_count = instance.lessons.count()
        return lesson_count

    def get_course_subscribe(self, instance):
        user = self.context['request'].user
        if Subscription.objects.filter(user=user, course=instance).exists():
            return True
        return False


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
