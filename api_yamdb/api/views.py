from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        AllowAny)
from rest_framework.pagination import LimitOffsetPagination

from .serializers import CommentSerializer, ReviewSerializer

# from .permissions import IsOwnerOrReadOnly
from reviews.models import Comment, Review


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AllowAny, )
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        """Список комментариев под определным отзывом."""
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
