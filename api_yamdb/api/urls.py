from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import CategoryViewSet, GenreViewSet, TitleViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genre', GenreViewSet, basename='genre')
router.register('title', TitleViewSet, basename='title')

urlpatterns = [
    path('v1/', include(router.urls)),
]
