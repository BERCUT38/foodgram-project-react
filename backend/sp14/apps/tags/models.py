from django.db import models


class Tags(models.Model):
    BLUE = '#0000FF'
    ORANGE = '#FFA500'
    GREEN = '#008000'
    PURPLE = '#800080'
    YELLOW = '#FFFF00'

    COLOR_CHOICES = [
        (BLUE, 'Синий'),
        (ORANGE, 'Оранжевый'),
        (GREEN, 'Зеленый'),
        (PURPLE, 'Фиолетовый'),
        (YELLOW, 'Желтый'),
    ]
    name = models.CharField(
        max_length=200, unique=True, null=False,
        blank=False, verbose_name='название'
        )
    colour = models.CharField(
        max_length=7, unique=True, null=False,
        choices=COLOR_CHOICES,
        blank=False, verbose_name='цвет'
        )
    slug = models.CharField(
        max_length=200, unique=True, null=False,
        blank=False, verbose_name='слаг'
        )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
