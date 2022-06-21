from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
import firebase_admin
from firebase_admin import auth


class RegisterSerializer(serializers.ModelSerializer):
    """сериализватор для регистрации юзера"""
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True,
                                     validators=[validate_password])

    class Meta:
        model = User
        fields = ('email', 'password', 'username')

    def create(self, validated_data):
        """метод для создания объекта модели User
        + создание в Firebase"""
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
        )

        user.set_password(validated_data['password'])
        user.save()

        default_app = firebase_admin.initialize_app()
        firebase_user = auth.create_user(
            email=validated_data["email"],
            password=validated_data["password"]
        )

        return user

