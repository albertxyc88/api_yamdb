from django.urls import include, path
from .views import LoginAPIView
from rest_framework.routers import DefaultRouter
from .views import UserViewSet


router_v1 = DefaultRouter()
router_v1.register(r'v1/users', UserViewSet)


urlpatterns = [
    path('', include(router_v1.urls)),
    path('v1/auth/signup/', LoginAPIView.as_view()),
    path('v1/users/', LoginAPIView.as_view()),
]
