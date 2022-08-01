from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, GenreViewSet, TitleViewSet, UserViewSet,
                    send_confirmation_code, obtain_token)

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genre')
router.register('titles', TitleViewSet, basename='title')

urlpatterns = [
    path('v1/auth/signup/', send_confirmation_code, name='signup'),
    path('v1/auth/token/', obtain_token, name='token'),
    path('v1/', include(router.urls)),
]
