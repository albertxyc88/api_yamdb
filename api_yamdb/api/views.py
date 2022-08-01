from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import (IsAuthenticatedOrReadOnly, IsAuthenticated,
                                        AllowAny)
from rest_framework.pagination import LimitOffsetPagination

from .serializers import CommentSerializer, ReviewSerializer

from .permissions import Is_AuthorAdminModeratorCreate_Or_ReadOnly
from reviews.models import Review, Title


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (Is_AuthorAdminModeratorCreate_Or_ReadOnly, )

    def get_queryset(self):
        """Список отзывов под определёным произведением."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        """
        Добавить новый отзыв. 
        Пользователь может оставить только один отзыв на произведение.
        Права доступа: Аутентифицированные пользователи.
        """
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (Is_AuthorAdminModeratorCreate_Or_ReadOnly, )

    def get_queryset(self):
        """Список комментариев под определёным отзывом."""
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        """Добавление комментария к отзыву."""
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
