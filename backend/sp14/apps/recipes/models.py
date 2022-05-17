from apps.ingredients.models import Ingredient
from apps.tags.models import Tags
from apps.user.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Recipes(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False,
                            verbose_name='Название')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор')
    text = models.TextField(blank=False, null=False,
                            verbose_name='Описание')
    tags = models.ManyToManyField(Tags, through='Rtags')
    ingredients = models.ManyToManyField(Ingredient, through='Ringredients')
    cooking_time = models.PositiveIntegerField(
    					validators=[MinValueValidator(1)],
					verbose_name='Время готовки'
					)
    image = models.ImageField(upload_to='recipes/', 
    			      blank=False, null=False,
                              verbose_name='Фото рецепта')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Rtags(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Тэги'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return 'Тэг рецепта'


class Ringredients(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.PROTECT,
                                   verbose_name='Ингридиент'
                                   )
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)],
                                         verbose_name='количество'
                                         )

    class Meta:
        verbose_name = 'Ингридиенты'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return 'Ингридиент в рецепте'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorite',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE,
                               related_name='in_favorite',
                               verbose_name='Рецепт')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'recipe'],
                       name='unique_recipe_in_user_favor')]
        ordering = ('-id',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='shlist',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE,
                               verbose_name='Рецепт')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'recipe'],
                       name='unique_recipe_in_user_shopping_list')]
        ordering = ('-id',)
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'

