from random import randint, randrange
from django.core.mail import send_mail
from rest_framework import serializers
from django.contrib.auth import get_user_model
from reviews.models import Category, Genre, Title
from .validators import is_correct_username, is_correct_email

User = get_user_model()


class EmailSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email',)
    
    def validate_username(self, username):
        return is_correct_username(username)
    
    def validate_email(self, email):
        return is_correct_email(email)


class UserSerializer(serializers.ModelSerializer):
    
    def validate_username(self, username):
        return is_correct_username(username)
    
    def validate_email(self, email):
        return is_correct_email(email)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'bio', 'role', 'email')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]


class RoleSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'bio', 'role'
        )


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

# class UserEmailSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = (
#             'username', 'first_name', 'last_name', 'email', 'bio', 'role'
#         )
    
#     def validate(self, data):
#         if data.get('username') == 'me':
#             raise serializers.ValidationError('использовать имя "me" запрещено!')
#         return data



class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        if data.get('username') is None:
            raise serializers.ValidationError('username is required')
        if data.get('username') == 'me':
            raise serializers.ValidationError('cannot login with username "me"')
        if data.get('email') is None:
            raise serializers.ValidationError('email is required')
        return data



class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Title
