from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny

from lms.models import Course, Lesson
from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer
from users.services import create_product, create_price, create_session


@extend_schema(summary='Список оплат')
class PaymentListAPIView(generics.ListAPIView):
    """ Список оплат курсов """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = (
        "paid_courses",
        "paid_lesson",
        "paid_type",
    )
    ordering_fields = ("data_payment",)


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        if payment.paid_type == 'Перевод':
            if payment.paid_lesson:
                lesson = Lesson.objects.get(id=payment.paid_lesson.id)
                product = create_product(product=lesson.name)
                price = create_price(product, lesson.amount)
                payment.paid_summa = lesson.amount
                session_id, payment_link = create_session(price)
                payment.session_id = session_id
                payment.link = payment_link
                payment.save()

            elif payment.paid_courses:
                course = Course.objects.get(id=payment.paid_courses.id)
                product = create_product(product=course.name)
                price = create_price(product, course.amount)
                payment.paid_summa = course.amount
                session_id, payment_link = create_session(price)
                payment.session_id = session_id
                payment.link = payment_link
                payment.save()
        else:
            if payment.paid_lesson:
                lesson = Lesson.objects.get(id=payment.paid_lesson.id)
                payment.paid_summa = lesson.amount
                payment.save()

            elif payment.paid_courses:
                course = Course.objects.get(id=payment.paid_courses.id)
                payment.paid_summa = course.amount
                payment.save()


@extend_schema(summary='Список пользователей')
class UserListAPIView(generics.ListAPIView):
    """ Список пользователей """
    serializer_class = UserSerializer
    queryset = User.objects.all()


@extend_schema(summary='Создание пользователя')
class UserCreateAPIView(generics.CreateAPIView):
    """ Создание пользователя """
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


@extend_schema(summary='Редактирование пользователя')
class UserUpdateAPIView(generics.UpdateAPIView):
    """ Редактирование пользователя """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_update(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


@extend_schema(summary='Удаление пользователя')
class UserDestroyAPIView(generics.DestroyAPIView):
    """ Удаление пользователя """
    queryset = User.objects.all()


@extend_schema(summary='Детализация пользователя')
class UserRetrieveAPIView(generics.RetrieveAPIView):
    """ Детализация пользователя """
    serializer_class = UserSerializer
    queryset = User.objects.all()
