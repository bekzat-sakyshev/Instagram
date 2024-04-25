from django.db import models
from django.contrib.auth import get_user_model


class Publication(models.Model):
    image = models.ImageField(null=False, upload_to='posts', verbose_name='Публикация')
    text = models.TextField(
        null=False, blank=False, verbose_name='Описание',
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='publications', verbose_name='Пользователи'
    )
    like = models.IntegerField(default=0, verbose_name='лайк')
    comment = models.IntegerField(default=0, verbose_name='комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикация'

    def __str__(self):
        return f'{self.text}'


class Comments(models.Model):
    publication = models.ForeignKey(
        'inst_app.Publication',
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Публикация'
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='comments', verbose_name='Пользователи'
    )
    text = models.TextField(
        null=False, blank=False, verbose_name='Описание',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'комментарии'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return f'{self.text}'


class Like(models.Model):
    publication = models.ForeignKey(
        'inst_app.Publication',
        related_name='likes',
        on_delete=models.CASCADE,
        verbose_name='Публикация'
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='likes', verbose_name='Пользователи'
    )

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайк'


class Follower(models.Model):
    subscriber = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='subscribers', verbose_name='Подписчик'
    )
    followed = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='followers', verbose_name='Пользователь для подписки'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписка'

