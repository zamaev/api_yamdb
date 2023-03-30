from rest_framework import mixins
from rest_framework import viewsets


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    lookup_field = 'slug'
