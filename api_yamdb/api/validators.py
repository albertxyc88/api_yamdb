from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


def is_correct_username(username):
    if User.objects.filter(username=username).exists():
        raise serializers.ValidationError('This username is already taken')
    if username == 'me':
        raise serializers.ValidationError('username "me" is forbidden')
    if username is None or username == '':
        raise serializers.ValidationError('Username field is required')
    return username


def is_correct_email(email):
    if User.objects.filter(email=email).exists():
        raise serializers.ValidationError('This email is already taken')
    if email is None or email == '':
        raise serializers.ValidationError('Email field is required')
    return email
