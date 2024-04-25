from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models

GENDER_CHOICES = [
    ('мужской', 'Мужской'),
    ('женский', 'Женский'),
    ('не указано', 'Предпочитаю не указывать'),
    ('свой вариант', 'Свой вариант')
]


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    avatar = models.ImageField(null=False, upload_to='avatars', verbose_name='Аватар', default='avatars/no-image.jpeg')
    bio = models.CharField(max_length=150, null=True, verbose_name='Информация о пользователе')
    phone_number = models.CharField(max_length=11, null=True, blank=True, verbose_name='Номер телефона',
                                    validators=[MinLengthValidator(11)])
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, default='не указано', verbose_name='Пол')
    custom_gender = models.CharField(max_length=50, blank=True, null=True, verbose_name='Свой вариант пола')
    publication_count = models.PositiveIntegerField(default=0, verbose_name='Количество публикаций')
    following_count = models.PositiveIntegerField(default=0, verbose_name='Количество подписок')
    followers_count = models.PositiveIntegerField(default=0, verbose_name='Количество подписчиков')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.user
