from random import randint, randrange
from django.core.mail import send_mail
from rest_framework import serializers
from users.models import User


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
        
