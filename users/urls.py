from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import PaymentListAPIView, UserListAPIView, UserCreateAPIView, UserUpdateAPIView, \
    UserRetrieveAPIView, UserDestroyAPIView
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('payment/', PaymentListAPIView.as_view(), name='payment-list'),
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('users/create/', UserCreateAPIView.as_view(), name='user-create'),
    path('users/<int:pk>/update/', UserUpdateAPIView.as_view(), name='user-update'),
    path('users/<int:pk>/retrieve/', UserRetrieveAPIView.as_view(), name='user-retrieve'),
    path('users/<int:pk>/destroy/', UserDestroyAPIView.as_view(), name='user-destroy'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
