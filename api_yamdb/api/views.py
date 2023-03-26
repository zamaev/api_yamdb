import random

from rest_framework import permissions, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.serializers import AuthSerializer, UserSerializer
from users.models import User


class AuthViewSet(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    @action(detail=False, methods=('post',))
    def token(self, request):
        if not request.data:
            return Response(
                {'message': 'The body cannot be empty.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = get_object_or_404(User, username=request.data['username'])
        if not request.data.get('confirmation_code'):
            return Response(
                {'message': 'Confirmation_code are required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        confirmation_code = request.data.get('confirmation_code')
        if (not user or user.confirmation_code != int(confirmation_code)):
            return Response(
                {'message': 'Invalid confirmation_code.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {'token': str(RefreshToken.for_user(user).access_token)},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=('post',))
    def signup(self, request):
        if not request.data:
            return Response(
                {'message': 'The body cannot be empty.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not request.data.get('email') or not request.data.get('username'):
            return Response(
                {'message': 'Email and username are required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = User.objects.filter(**request.data).first()
        if not user:
            serializer = AuthSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user = serializer.save()
        serializer = AuthSerializer(user)
        confirmation_code = random.randint(1111, 9999)
        user.confirmation_code = confirmation_code
        user.save()
        user.email_user(
            'Код подтверждения',
            f'Ваш код подтверждения: {confirmation_code}.',
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        username = self.kwargs.get('pk')
        if username == 'me':
            username = self.request.user.username
        return get_object_or_404(User, username=username)
