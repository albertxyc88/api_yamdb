from django.forms import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model
from reviews.models import Category, Genre, Title
from .validators import is_correct_username, is_correct_email

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Genre
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()



class EmailSerializer(serializers.Serializer):
    """Email serializer"""

    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    def validate_username(self, username):
        return is_correct_username(username)

    def validate_email(self, email):
        return is_correct_email(email)

    class Meta:
        model = User
        fields = ('username', 'email',)


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""

    def validate_username(self, username):
        return is_correct_username(username)

    def validate_email(self, email):
        return is_correct_email(email)

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
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]


class RoleSerializer(UserSerializer):
    """Role Serializer"""

    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'bio', 'role'
        )

    def validate(self, data):
        if data.get('role') == 'user':
            raise ValidationError('User cannot change his role')
        return data


class ConfirmationCodeSerializer(serializers.Serializer):
    """Confirmation code serializer"""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


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
