from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(max_length=150, unique=True,
                              verbose_name='почта')
    username = models.CharField(blank=False, max_length=150, unique=True,
                                verbose_name='имя пользователя')
    first_name = models.CharField(blank=False, max_length=150,
                                  verbose_name='Имя')
    last_name = models.CharField(blank=False, max_length=150,
                                 verbose_name='фамилия')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower',
                             verbose_name='Пользователь-подписчик')
    following = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='following',
                                  verbose_name='пользователь-на кого подписан')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'following'],
                                               name='unique_following')]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
