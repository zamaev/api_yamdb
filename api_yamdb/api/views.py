from rest_framework import viewsets

from .mixins import CreateListDestroyViewSet
from content.models import Category, Title, Genre
from .serializers import (
    CategorySerializer,
    TitleSerializer,
    GenreSerializer,
    TitleSerializerGET
)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializerGET
        return TitleSerializer


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
