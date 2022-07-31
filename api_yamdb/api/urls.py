from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import send_confirmation_code, obtain_token, UserViewSet
from .views import CategoryViewSet, GenreViewSet, TitleViewSet


router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genre', GenreViewSet, basename='genre')
router_v1.register('title', TitleViewSet, basename='title')


urlpatterns = [
    path('v1/auth/signup/', send_confirmation_code),
    path('v1/auth/token/', obtain_token),
    # path('v1/users/', UserListView.as_view()),
    # path('v1/users/<str:username>/', UserDetailView.as_view()),
    path('v1/', include(router_v1.urls)),
]

