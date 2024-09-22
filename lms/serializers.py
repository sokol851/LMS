from rest_framework import serializers

from lms.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Course
        fields = ('name', 'preview', 'description', 'lesson_count', 'lessons',)

    @staticmethod
    def get_lesson_count(instance):
        lesson_count = instance.lessons.count()
        return lesson_count
