from random import randint, randrange
from django.core.mail import send_mail
from rest_framework import permissions
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer
from rest_framework import viewsets
from users.models import User
from .serializers import LoginSerializer
from .permissions import AdminOnlyPermission
from .pagination import UserPagination
from rest_framework import filters


# Create your views here.
class LoginAPIView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_mail(
            'subject',
            'text',
            'yamdb@gmail.com',
            ['artouralty.jesus@gmail.com'],
            fail_silently=False
        )
        return Response(serializer.data)
        # serializer = self.serializer_class(data=user)
        # return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [AdminOnlyPermission]
    pagination_class = UserPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ('username',) 

    def perform_create(self, serializer):
        serializer.save(role='user')

