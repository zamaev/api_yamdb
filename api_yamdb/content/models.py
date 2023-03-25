from django.db import models


class Category(models.Model):
    name = models.CharField(verbose_name='Category name',
                            max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(verbose_name='Genre name',
                            max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    title = models.ForeignKey(
        'Title',
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.genre


class Title(models.Model):
    name = models.CharField(verbose_name='Title',
                            max_length=256)
    year = models.IntegerField(verbose_name='Title year')
    description = models.TextField(verbose_name='Description', blank=True)
    category = models.ForeignKey(
        Category,
        verbose_name='category',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )
    genre = models.ManyToManyField(
        Genre,
        through=GenreTitle
    )

    def __str__(self):
        return self.name
