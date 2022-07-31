














































from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import UserViewSet, send_confirmation_code


router_v1 = DefaultRouter()
router_v1.register(r'v1/users', UserViewSet)


urlpatterns = [
    path('', include(router_v1.urls)),
    path('v1/auth/signup/', send_confirmation_code),
]
