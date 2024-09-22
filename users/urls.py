from django.urls import path

from users.views import PaymentListAPIView, UserListAPIView
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('payment/', PaymentListAPIView.as_view(), name='payment-list'),
    path('user/', UserListAPIView.as_view(), name='user-list'),
]
