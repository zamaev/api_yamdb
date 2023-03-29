from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import datetime as dt

from users.models import User


class Category(models.Model):
    """Категории."""

    name = models.CharField(verbose_name='Категория',
                            max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры."""

    name = models.CharField(verbose_name='Название жанра',
                            max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Жанры произведений."""

    genre = models.ForeignKey(
        Genre,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        'Title',
        null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведений'
        ordering = ('id',)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Title(models.Model):
    """Произведения."""

    name = models.CharField(verbose_name='Произведение',
                            max_length=256)
    year = models.IntegerField(verbose_name='Год произведения',
                               validators=[
                                MaxValueValidator(
                                    dt.date.today().year,
                                    'Максимальный год равен текущему году'
                                )
                               ])
    description = models.TextField(verbose_name='Описание', blank=True)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )
    genre = models.ManyToManyField(
        Genre,
        through=GenreTitle
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг',
        null=True,
        default=None
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Review(models.Model):
    """Отзывы."""

    text = models.TextField(
        verbose_name='Текст',
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1, 'Минимальная оценка 1'),
            MaxValueValidator(10, 'Максимальная оценка 10')
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['pub_date']
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),
        )

    def __str__(self):
        return self.text[:30]


class Comment(models.Model):
    """Комментарии."""

    text = models.TextField(
        verbose_name='Текст',
    )
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['pub_date']

    def __str__(self):
        return self.text[:30]
