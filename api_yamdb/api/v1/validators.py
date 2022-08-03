from django.contrib.auth import get_user_model
from django.forms import ValidationError
from rest_framework import serializers
from django.core.validators import validate_email

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
    try:
        validate_email(email)
    except ValidationError:
        raise serializers.ValidationError('Please enter a valid email')
    return email
