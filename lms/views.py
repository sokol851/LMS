from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course, Lesson, Subscription
from lms.paginators import CourseLessonPaginator
from users.permissions import IsModerator, IsOwner
from lms.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer


@extend_schema_view(
    list=extend_schema(summary="Получить список курсов",),
    update=extend_schema(summary="Изменение курса",),
    retrieve=extend_schema(summary="Детализация курса",),
    partial_update=extend_schema(summary='Изменение части курса'),
    create=extend_schema(summary="Создание курса",),
    destroy=extend_schema(summary="Удаление курса",),
)
class CourseViewSet(viewsets.ModelViewSet):
    """ ViewSet для работы с курсами """
    queryset = Course.objects.all().order_by('id')
    serializer_class = CourseSerializer
    pagination_class = CourseLessonPaginator

    def perform_create(self, course):
        course.validated_data["owner"] = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [~IsModerator]
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = [IsModerator | IsOwner]
        elif self.action == "destroy":
            self.permission_classes = [~IsModerator | IsOwner]
        return super().get_permissions()


@extend_schema(summary='Создание урока')
class LessonCreateAPIView(generics.CreateAPIView):
    """ Создание урока """
    serializer_class = LessonSerializer
    permission_classes = [~IsModerator, IsAuthenticated]

    def perform_create(self, lesson):
        lesson.validated_data["owner"] = self.request.user
        lesson.save()


@extend_schema(summary='Отображение уроков')
class LessonListAPIView(generics.ListAPIView):
    """ Отображение уроков """
    queryset = Lesson.objects.all().order_by('id')
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    pagination_class = CourseLessonPaginator


@extend_schema(summary='Детализация урока')
class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """ Детализация урока """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


@extend_schema(summary='Обновление урока')
class LessonUpdateAPIView(generics.UpdateAPIView):
    """ Обновление урока """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


@extend_schema(summary='Удаление урока')
class LessonDestroyAPIView(generics.DestroyAPIView):
    """ Удаление урока """
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | ~IsModerator]


class SubscriptionAPIView(APIView):
    """ Подписка на курс """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    @extend_schema(summary='Добавление подписки')
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item, created = Subscription.objects.get_or_create(user=user, course=course_item)

        if created:
            message = 'Подписка добавлена'
        else:
            subs_item.delete()
            message = 'Подписка удалена'
        return Response({"message": message})

    @extend_schema(summary='Список подписок')
    def get(self, request):
        return Response(self.queryset.values())
