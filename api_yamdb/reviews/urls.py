from django.urls import path

from . import views

app_name = 'review'

urlpatterns = [
    # Получение списка всех отзывов/Добавление нового отзыва
    path(
        'titles/<int:title_id>/reviews/',
        views.titles_reviews,
        name='title_reviews'
    ),

    # Полуение отзыва по id/Частичное обновление отзыва по id/Удаление отзыва по id
    path(
        'titles/<int:title_id>/reviews/<int:review_id>/',
        views.titles_review_id,
        name='title_review_id'
    ),

    # Получение списка всех комментариев к отзыву/Добавление комментария к отзыву
    path(
        'titles/<int:title_id>/reviews/<int:review_id>/comments/',
        views.titles_reviews_comments,
        name='title_review_comments'
    ),

    # Получение комментария к отзыву/Частичное обновление комментария к отзыву/Удаление комментария к отзыву
    path(
        'titles/<int:title_id>/reviews/<int:review_id>/comments/<int:comment_id>',
        views.title_review_comment_id,
        name='title_review_comment_id'
    ),
]
