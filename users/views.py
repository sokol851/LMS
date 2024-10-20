from django.core.exceptions import ValidationError
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
    """ Список оплат """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = (
        "paid_courses",
        "paid_lesson",
        "paid_type",
    )
    ordering_fields = ("data_payment",)


@extend_schema(summary='Создание оплаты')
class PaymentCreateAPIView(generics.CreateAPIView):
    """ Создание оплаты """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        if payment.paid_lesson:
            product = Lesson.objects.get(id=payment.paid_lesson.id)
        elif payment.paid_courses:
            product = Course.objects.get(id=payment.paid_courses.id)
        else:
            raise ValidationError('Course or Lesson needed')

        if payment.paid_type == 'Перевод':
            stripe_product = create_product(product=product.name)
            stripe_price = create_price(stripe_product, product.amount)
            payment.paid_summa = product.amount
            session_id, payment_link = create_session(stripe_price)
            payment.session_id = session_id
            payment.link = payment_link
            payment.save()
        else:
            payment.paid_summa = product.amount
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
