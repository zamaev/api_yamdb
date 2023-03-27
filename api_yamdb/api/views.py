import random

from django.db.models import Avg

from rest_framework import permissions, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.mixins import CreateListDestroyViewSet
from api.permissions import isAdmin, isOwner, IsAdminOrReadOnly
from api.serializers import (
    AuthSerializer,
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    TitleSerializerGET,
    TokenSerializer,
    UserSerializer,
)
from reviews.models import Review, Title, Category, Genre
from users.models import User


class AuthViewSet(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    @action(detail=False, methods=('post',))
    def token(self, request):
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
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (isAdmin,)

    def get_object(self):
        username = self.kwargs.get('pk')
        if username == 'me':
            username = self.request.user.username
        return get_object_or_404(User, username=username)

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'partial_update':
            return (isOwner(),)
        return super().get_permissions()


class CategoryViewSet(CreateListDestroyViewSet):
    """Вьюсет для обьектов модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели Title."""

    permission_classes = (IsAdminOrReadOnly,)
    queryset = Title.objects.all().annotate(
        Avg("reviews__score")
    )

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


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели Review."""
    serializer_class = ReviewSerializer
    permission_classes = (permissions.AllowAny,)  # пока поставил этот пермишн

    def get_object(self):
        """Возвращает title по pk."""
        return get_object_or_404(Title, pk=self.kwargs.get("title_id"))

    def get_queryset(self):
        """Возвращает queryset c review для выбранного title."""
        return self.get_object().reviews.all()

    def perform_create(self, serializer):
        """Создает review для текущего title,
        автор == текущий пользователь."""
        serializer.save(author=self.request.user, title=self.get_object())


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = (permissions.AllowAny,)  # пока поставил этот пермишн

    def get_object(self):
        """Возвращает review по pk."""
        return get_object_or_404(Review, pk=self.kwargs.get("review_id"))

    def get_queryset(self):
        """Возвращает queryset c comments для выбранного review."""
        return self.get_object.comments.all()

    def perform_create(self, serializer):
        """Создает comments для текущего review,
        автор == текущий пользователь."""
        serializer.save(author=self.request.user, review=self.get_object())

        # есть у меня сомнения по поводу перформ-креэйт,
        # сделал пока как в предыдущем задании
