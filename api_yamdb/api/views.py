from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets

from reviews.models import Review, Title
from .serializers import (CommentSerializer,
                          ReviewSerializer,)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели Review."""
    serializer_class = ReviewSerializer
    permission_classes = (permissions.AllowAny,) # пока поставил этот пермишн

    def object(self):
        """Возвращает title по pk."""
        return get_object_or_404(Title, pk=self.kwargs.get("title_id"))

    def get_queryset(self):
        """Возвращает queryset c review для выбранного title."""
        return self.object().reviews.all()

    def perform_create(self, serializer):
        """Создает review для текущего title,
        автор == текущий пользователь."""
        serializer.save(author=self.request.user, title=self.object())


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = (permissions.AllowAny,) # пока поставил этот пермишн

    def object(self):
        """Возвращает review по pk."""
        return get_object_or_404(Review, pk=self.kwargs.get("review_id"))

    def get_queryset(self):
        """Возвращает queryset c comments для выбранного review."""
        return self.object.comments.all()

    def perform_create(self, serializer):
        """Создает comments для текущего review,
        автор == текущий пользователь."""
        serializer.save(author=self.request.user, review=self.object())

        # есть у меня сомнения по поводу перформ-креэйт, сделал пока как в предыдущем задании
