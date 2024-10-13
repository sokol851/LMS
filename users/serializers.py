from rest_framework import serializers

from users.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    """ Сериализатор оплат """
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор пользователей """
    class Meta:
        model = User
        fields = "__all__"
