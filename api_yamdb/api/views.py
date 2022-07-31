from django.core.mail import send_mail
from rest_framework import permissions
from django.shortcuts import render
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer, UserSerializer, UserEmailSerializer, CodeSerializer
from rest_framework import viewsets
from .permissions import AdminPermission, ModeratorPermission, UserPermission, OwnerPermission, IsAdminOrReadOnly, IsAdminOrSuperUser
from .pagination import UserPagination
from rest_framework import filters, viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets

from reviews.models import Category, Genre, Title
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer)


User = get_user_model()


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [AdminPermission|IsAdminUser]
#     lookup_field = 'username'
#     filter_backends = [filters.SearchFilter]
#     search_fields = ('username',) 

#     @action(methods=['patch', 'get'], detail=False,
#             permission_classes=[IsAuthenticated],
#             url_path='me', url_name='me')
#     def me(self, request, *args, **kwargs):
#         instance = self.request.user
#         serializer = self.get_serializer(instance)
#         if self.request.method == 'PATCH':
#             serializer = self.get_serializer(
#                 instance, data=request.data, partial=True)
#             serializer.is_valid()
#             serializer.save()
#         return Response(serializer.data)


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     permission_classes = [IsAdminUser | AdminPermission]
#     serializer_class = UserSerializer
#     lookup_field = 'username'
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['username', ]

#     @action(methods=['patch', 'get'], detail=False,
#             permission_classes=[IsAuthenticated],
#             url_path='me', url_name='me')
#     def me(self, request, *args, **kwargs):
#         instance = self.request.user
#         serializer = self.get_serializer(instance)
#         if self.request.method == 'PATCH':
#             serializer = self.get_serializer(
#                 instance, data=request.data, partial=True)
#             serializer.is_valid()
#             serializer.save()
#         return Response(serializer.data)

# class UserViewSet(viewsets.ModelViewSet):
#     """API для модели пользователя"""
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     pagination_class = UserPagination
#     permission_classes = [IsAdminOrSuperUser]
#     lookup_field = 'username'

#     @action(detail=False, methods=['get', 'patch'],
#             permission_classes=[IsAuthenticated])
#     def me(self, request):
#         """API для получения и редактирования
#         текущим пользователем своих данных"""
#         user = request.user
#         if request.method == 'GET':
#             serializer = self.get_serializer(user)
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         serializer = self.get_serializer(user, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(role=user.role, partial=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminPermission,)
    lookup_field = 'username'
    lookup_value_regex = r'[\w\@\.\+\-]+'
    filter_backends = (filters.SearchFilter)
    search_fields = ('username',)

    @action(
        methods=('get', 'patch'),
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,),
        serializer_class=UserSerializer
    )
    def user_info(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_confirmation_code(request):
    serializer = UserEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    if not User.objects.filter(email=email).exists():
        User.objects.create(
            username=email, email=email
        )
    user = User.objects.filter(email=email).first()
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения Yamdb',
        f'Ваш код подтверждения: {confirmation_code}',
        'yamdb@yamdb.com',
        [email],
        fail_silently=False
    )
    return Response(
        {'result': 'Код подтверждения успешно отправлен!'},
        status=status.HTTP_200_OK
    )

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def send_code(request):
#     username = request.data.get('username')
#     email = request.data.get('email')
#     serializer = UserEmailSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     if username is None or email is None:
#         if username is None:
#             return Response(
#                 {'Error': 'Незаполненное поле username!'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         if email is None:
#             return Response(
#                 {'Error': 'Незаполненное поле email!'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#     if not User.objects.filter(username=username, email=email).exists():
#         User.objects.create_user(username=username, email=email)
#     user = get_object_or_404(User, username=username, email=email)
#     confirmation_code = 123
#     subject = 'Code Confirmation'
#     content = f'Your confirmation code is: {confirmation_code}'
#     send_mail(
#         subject=subject,
#         message=content,
#         from_email='yamdb@yamdb.com',
#         recipient_list=[user.email],
#         fail_silently=False
#     )
#     return Response(serializer.data, status=status.HTTP_200_OK)


# class UserSignupView(APIView):
#     def post(self, request):
#         serializer = UserEmailSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             username = serializer.data.get('username')
#             user = get_object_or_404(User, username=username)
#             confirmation_code = 49325230
#             user.confirmation_code = confirmation_code
#             user.save()

#             send_mail(
#                 'subj',
#                 'content',
#                 'yamdb@yamdb.com',
#                 [user.email],
#                 fail_silently=False
#             )

#             return Response(serializer.data, status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# def confirmation_generator(username):
#     '''Generate confirmation codes'''

#     user = get_object_or_404(User, username=username)
#     confirmation_code = ''.join(
#         [random.choice(settings.CONF_GEN) for x in range(15)]
#     )
#     user.confirmation_code = confirmation_code
#     user.save()

#     send_mail(
#         settings.MAIL_SUBJECT,
#         confirmation_code,
#         settings.FROM_EMAIL,
#         [user.email],
#         fail_silently=False
#     )


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
