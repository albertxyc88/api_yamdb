from django.contrib.auth import get_user_model
from django.forms import ValidationError
from rest_framework import serializers
from reviews.models import Category, Genre, Title, Comment, Review

from .validators import is_correct_email, is_correct_username

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
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title', )

    def validate(self, value):
        if self.context['request'].method == 'POST':
            author = self.context.get('request').user
            title_id = self.context['view'].kwargs['title_id']
            if Review.objects.filter(author=author, title_id=title_id).exists():
                raise serializers.ValidationError (
                'У Вас уже есть отзыв на данное произведение. Выберите другое'
            )
        return value

    def validate_score(self, value):
        if 1 <= value <= 10:
            return value
        raise serializers.ValidationError (
            'Оценка произведения должна быть в диапазоне от 1 до 10'
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = '__all__'
