from rest_framework import serializers
from rest_framework.validators import (
    UniqueTogetherValidator, UniqueValidator)

from reviews.models import Comment, Review
from users.models import User, ROLE_CHOICES


class AuthSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=(
            UniqueValidator(
                queryset=User.objects.all(),
                message='A user with that email already exists.'
            ),
        )
    )

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Username cannot be equal "me".')
        return value


class RoleChoiceField(serializers.ChoiceField):
    def to_representation(self, data):
        for key, role in ROLE_CHOICES:
            if key == data:
                return role
        raise serializers.ValidationError(f'Role \'{data}\' is not support')

    def to_internal_value(self, data):
        for key, role in ROLE_CHOICES:
            if role == data:
                return key
        raise serializers.ValidationError('Role is not support')


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=(
            UniqueValidator(
                queryset=User.objects.all(),
                message='A user with that email already exists.',
            ),
        ),
    )
    role = RoleChoiceField(choices=ROLE_CHOICES, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'score', 'pub_date',)
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author'),
                message='Вы уже оставляли отзыв на это произведение'
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'author', 'text', 'cretated',)
        model = Comment
