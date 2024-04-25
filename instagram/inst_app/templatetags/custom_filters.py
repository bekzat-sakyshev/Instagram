from django.utils import timezone
from django import template

register = template.Library()


@register.filter
def pluralize_publications(num):
    if num % 10 == 1 and num != 11:
        return "публикация"
    elif num % 10 in [2, 3, 4] and num not in [12, 13, 14]:
        return "публикации"
    else:
        return "публикаций"


@register.filter
def pluralize_followers(num):
    if num % 10 == 1 and num != 11:
        return "подписчик"
    elif num % 10 in [2, 3, 4] and num not in [12, 13, 14]:
        return "подписчика"
    else:
        return "подписчиков"


@register.filter
def pluralize_followings(num):
    if num % 10 == 1 and num != 11:
        return "подписка"
    elif num % 10 in [2, 3, 4] and num not in [12, 13, 14]:
        return "подписки"
    else:
        return "подписок"


@register.filter
def pluralize_likes(num):
    if num % 10 == 1 and num != 11:
        return "отметка"
    elif num % 10 in [2, 3, 4] and num not in [12, 13, 14]:
        return "отметки"
    else:
        return "отметок"


@register.filter
def pluralize_comments(num):
    if num % 10 == 1 and num != 11:
        return "комментарий"
    elif num % 10 in [2, 3, 4] and num not in [12, 13, 14]:
        return "комментария"
    else:
        return "комментариев"


@register.filter
def custom_timesince(value):
    minute_seconds = 60
    hour_seconds = 60 * 60
    day_seconds = 24 * 60 * 60
    week_seconds = 7 * 24 * 60 * 60

    time_difference = timezone.now() - value

    if time_difference.total_seconds() == 0:
        return 'только что'
    elif time_difference.total_seconds() < minute_seconds:
        return '{} сек.'.format(int(time_difference.total_seconds()))
    elif time_difference.total_seconds() < hour_seconds:
        return '{} мин.'.format(int(time_difference.total_seconds() / 60))
    elif time_difference.total_seconds() < day_seconds:
        return '{} ч.'.format(int(time_difference.total_seconds() / 3600))
    elif time_difference.total_seconds() < week_seconds:
        return '{} дн.'.format(int(time_difference.total_seconds() / 86400))
    else:
        return '{} нед.'.format(int(time_difference.total_seconds() / 604800))


@register.filter
def custom_timesince_back(value):
    minute_seconds = 60
    hour_seconds = 60 * 60
    day_seconds = 24 * 60 * 60
    week_seconds = 7 * 24 * 60 * 60

    time_difference = timezone.now() - value

    if time_difference.total_seconds() == 0:
        return 'только что'
    elif time_difference.total_seconds() < minute_seconds:
        time_difference = int(time_difference.total_seconds())
        if time_difference % 10 == 1 and time_difference != 11:
            time_name = "секунду"
        elif time_difference % 10 in [2, 3, 4] and time_difference not in [12, 13, 14]:
            time_name = "секунды"
        else:
            time_name = "секунд"
        return f'{time_difference} {time_name} назад'
    elif time_difference.total_seconds() < hour_seconds:
        time_difference = int(time_difference.total_seconds() / 60)
        if time_difference % 10 == 1 and time_difference != 11:
            time_name = "минуты"
        elif time_difference % 10 in [2, 3, 4] and time_difference not in [12, 13, 14]:
            time_name = "минуты"
        else:
            time_name = "минут"
        return f'{time_difference} {time_name} назад'
    elif time_difference.total_seconds() < day_seconds:
        time_difference = int(time_difference.total_seconds() / 3600)
        if time_difference % 10 == 1 and time_difference != 11:
            time_name = "час"
        elif time_difference % 10 in [2, 3, 4] and time_difference not in [12, 13, 14]:
            time_name = "часа"
        else:
            time_name = "часов"
        return f'{time_difference} {time_name} назад'
    elif time_difference.total_seconds() < week_seconds:
        time_difference = int(time_difference.total_seconds() / 86400)
        if time_difference % 10 == 1 and time_difference != 11:
            time_name = "день"
        elif time_difference % 10 in [2, 3, 4] and time_difference not in [12, 13, 14]:
            time_name = "дня"
        else:
            time_name = "дней"
        return f'{time_difference} {time_name} назад'
    else:
        time_difference = int(time_difference.total_seconds() / 604800)
        if time_difference % 10 == 1 and time_difference != 11:
            time_name = "неделю"
        elif time_difference % 10 in [2, 3, 4] and time_difference not in [12, 13, 14]:
            time_name = "недели"
        else:
            time_name = "недель"
        return f'{time_difference} {time_name} назад'
