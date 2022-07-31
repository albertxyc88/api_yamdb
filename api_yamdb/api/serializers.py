

















































































































from random import randint, randrange
from django.core.mail import send_mail
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

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


class CodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'role',
            'email'
        )
    
    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError('использовать имя "me" запрещено!')
        return data
