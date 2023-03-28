import random

from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import TitleFilter
from api.mixins import CreateListDestroyViewSet
from api.permissions import (IsAdminOrReadOnly, IsAnyRoleOrReadOnly, isAdmin,
                             isOwner)
from api.serializers import (AuthSerializer, CategorySerializer,
                             CommentSerializer, GenreSerializer,
                             ReviewSerializer, TitleSerializer,
                             TitleSerializerGET, TokenSerializer,
                             UserPatchSerializator, UserSerializer)
from reviews.models import Category, Genre, Review, Title
from users.models import User


class AuthViewSet(viewsets.ViewSet):
    """Вьюсет для авторизации."""

    permission_classes = (permissions.AllowAny,)

    @action(detail=False, methods=('post',))
    def token(self, request):
        """Получение токена по email и коду подтверждения."""
        serializer = TokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        user = get_object_or_404(User, username=request.data.get('username'))
        confirmation_code = request.data.get('confirmation_code')
        if (not user or user.confirmation_code != int(confirmation_code)):
            return Response(
                {'message': 'Invalid confirmation_code.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {'token': str(AccessToken.for_user(user))},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=('post',))
    def signup(self, request):
        """Регистрация по email и username."""
        user = None
        if request.data.get('username') and request.data.get('email'):
            user = User.objects.filter(
                username=request.data.get('username'),
                email=request.data.get('email'),
            ).first()
        serializer = AuthSerializer(user, data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not user:
            user = serializer.save()
        confirmation_code = random.randint(1111, 9999)
        user.confirmation_code = confirmation_code
        user.save()
        user.email_user(
            'Код подтверждения',
            f'{confirmation_code}',
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели User."""

    queryset = User.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def get_object(self):
        username = self.kwargs.get('pk')
        if username == 'me':
            username = self.request.user.username
        return get_object_or_404(User, username=username)

    def get_serializer_class(self):
        if (self.kwargs.get('pk') == 'me'
                and self.action == 'partial_update'):
            return UserPatchSerializator
        return UserSerializer

    def get_permissions(self):
        if (self.kwargs.get('pk') == 'me'
            and (self.action == 'retrieve'
                 or self.action == 'partial_update'
                 or self.action == 'destroy')):
            return (isOwner(),)
        return (isAdmin(),)

    def destroy(self, request, pk=None):
        if self.kwargs.get('pk') == 'me':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, pk)

    def update(self, request, *args, **kwargs):
        if self.action == 'update':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, args, **kwargs)


class CategoryViewSet(CreateListDestroyViewSet):
    """Вьюсет для обьектов модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели Title."""

    permission_classes = (IsAdminOrReadOnly,)
    queryset = Title.objects.annotate(Avg('reviews__score')).order_by('name')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """Использует один из сериалайзеров в зависимости от запроса."""
        if self.request.method == 'GET':
            return TitleSerializerGET
        return TitleSerializer


class GenreViewSet(CreateListDestroyViewSet):
    """Вьюсет для обьектов модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели Review."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAnyRoleOrReadOnly,)

    def get_title(self):
        """Возвращает title по pk."""
        return get_object_or_404(Title, pk=self.kwargs.get("title_id"))

    def get_queryset(self):
        """Возвращает queryset c review для выбранного title."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """Создает review для текущего title,
        автор == текущий пользователь."""
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = (IsAnyRoleOrReadOnly,)

    def get_review(self):
        """Возвращает review по pk."""
        return get_object_or_404(Review, pk=self.kwargs.get("review_id"))

    def get_queryset(self):
        """Возвращает queryset c comments для выбранного review."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """Создает comments для текущего review,
        автор == текущий пользователь."""
        serializer.save(author=self.request.user, review=self.get_review())
