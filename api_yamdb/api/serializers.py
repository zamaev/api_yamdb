from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import ROLE_CHOICES, User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.IntegerField(required=True)


class AuthSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        max_length=254,
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


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=(
            UniqueValidator(
                queryset=User.objects.all(),
                message='A user with that email already exists.',
            ),
        ),
    )
    role = serializers.ChoiceField(choices=ROLE_CHOICES, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class UserPatchSerializator(UserSerializer):
    role = serializers.ChoiceField(choices=ROLE_CHOICES,
                                   read_only=True)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializerGET(serializers.ModelSerializer):
    genre = GenreSerializer(many=True,)
    category = CategorySerializer()
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('name', 'id', 'year', 'description', 'genre', 'category')


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

    def validate(self, data):
        request = self.context['request']
        title = get_object_or_404(
            Title, pk=self.context['view'].kwargs.get('title_id')
        )
        if request.method == 'POST':
            if (Review.objects.filter(title=title, author=request.user)
                    .exists()):
                raise ValidationError(
                    'Вы уже оставляли отзыв на это произведение'
                )
        return data

    class Meta:
        model = Review
        fields = ('id', 'author', 'title', 'text', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date',)
        model = Comment
