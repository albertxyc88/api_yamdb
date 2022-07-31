from rest_framework import serializers

from reviews.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    # Если не автор, доступно только для чтения
    author = serializers.SlugRelatedField(
        # почему оказывается slug_field='username'?
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate_score(self, value):
        if 1 <= value[1] <= 10:
            return value
        raise serializers.ValidationError (
            'Оценка произведения должна быть в диапазоне от 1 до 10'
        )


class CommentSerializer(serializers.ModelSerializer):
    # Если не автор, доступно только для чтения
    author = serializers.SlugRelatedField(
        # почему указывается slug_field='username'?
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Comment
        fields = '__all__'     
