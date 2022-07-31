import email
import uuid
from django.core.mail import send_mail
from rest_framework import permissions
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .permissions import IsAdminOnly, ModeratorPermission, UserPermission, OwnerPermission, IsAdminOrReadOnly, IsAdminOrSuperUser
from .pagination import UserPagination
from rest_framework import filters, viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import generics

from reviews.models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer, EmailSerializer, UserSerializer, ConfirmationCodeSerializer, RoleSerializer
from .utils import send_code


User = get_user_model()


# class UserListView(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     filter_backends = (filters.SearchFilter,)
#     permission_classes = (IsAdminOnly,)
#     search_fields = ('username',)
#     lookup_field = 'username'

#     def perform_create(self, serializer):
#         if serializer.is_valid():
#             serializer.save()
#         return super().perform_create(serializer)
    

# class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = UserSerializer
#     permission_classes = (IsAdminOnly,)
#     lookup_field = 'username'

#     def get_queryset(self):
#         user = User.objects.filter(username=self.kwargs['username'])
#         return user


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOnly,)
    lookup_field = 'username'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)

    @action(
        methods=('GET', 'PATCH'),
        detail=False,
        url_path='me/',
        permission_classes=(OwnerPermission,),
        serializer_class=RoleSerializer
    )
    def self_user(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_paginated_response(self, data):
        return Response({
            'results': data
        })
    
# Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjYwMTUwNjg2LCJpYXQiOjE2NTkyODY2ODYsImp0aSI6IjA0NTUwYTMzMzg4MTQzMDM5ZmU2NTczODlkOGQ5YTJlIiwidXNlcl9pZCI6Mn0.JAaO-fGkv2us6e45kkJ14DpPcwY_MMIbmtc6_p2YIRg

    # def get_permissions(self):
    #     if self.action == 'POST':
    #         permission_classes = IsAdminOnly
    #         return [permission_classes()]
    #     return super().get_permissions()

    # def get_permissions(self):
    #     if self.action == 'create':
    #         composed_perm = IsAuthenticated & IsAdminOnly
    #         return [composed_perm()]
    #     return super().get_permissions()

    # @api_view(['POST'])
    # def perform_create(self, serializer):
    #     self.permission_classes = [IsAdminOnly]
        
    #     if email_serializer.is_valid():
    #         # email_serializer.is_valid(raise_exception=True)
    #         username = serializer.validated_data.get('username')
    #         email = serializer.validated_data.get('email')
    #         if User.objects.filter(username=username).exists() is False:
    #             user = User.objects.create_user(username=username, email=email)
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_200_OK)
    #         user = get_object_or_404(User, username=username, email=email)
    #         user.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_confirmation_code(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    if User.objects.filter(username=username).exists() is False:
        user = User.objects.create_user(username=username, email=email)
        send_code(email, user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    user = get_object_or_404(User, username=username, email=email)
    send_code(email, user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def obtain_token(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    confirmation_code = serializer.validated_data['confirmation_code']
    if confirmation_code == user.confirmation_code:
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (permissions.AllowAny,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (permissions.AllowAny,)
