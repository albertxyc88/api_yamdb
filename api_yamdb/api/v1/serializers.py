from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from .validators import is_correct_email, is_correct_username

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer."""

    class Meta:
        exclude = ('id',)
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Genre serializer."""

    class Meta:
        exclude = ('id',)
        model = Genre
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    """Title Serializer."""

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
    """ReadOnlyTitle Serializer."""

    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


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


class ReviewSerializer(serializers.ModelSerializer):
    """Review serializer."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        exclude = ('title',)

    def validate(self, value):
        if self.context['request'].method == 'POST':
            author = self.context.get('request').user
            title_id = self.context['view'].kwargs['title_id']
            title = get_object_or_404(Title, pk=title_id)
            if Review.objects.filter(
                author=author,
                title=title
            ).exists():
                raise serializers.ValidationError(
                    'У Вас уже есть отзыв на данное произведение.'
                    'Выберите другое'
                )
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Comment serializer."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        exclude = ('review', )
