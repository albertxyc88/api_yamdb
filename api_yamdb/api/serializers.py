from genericpath import exists
from sqlite3 import adapt
from rest_framework import serializers

from reviews.models import Comment, Review


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
