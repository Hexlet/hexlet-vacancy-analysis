
from asgiref.sync import sync_to_async
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from app.telegram_bot.models import TgUser, UserSubscriptionSettings


@sync_to_async
def get_or_create_user(username, user_id, is_subscribed):
    user = TgUser.objects.get_or_create(
        username=username,
        user_id=user_id,
        is_subscribed=is_subscribed
        )
    return user


@sync_to_async
def get_user(username):
    try:
        user = TgUser.objects.get(username=username)
        return user
    except TgUser.DoesNotExist:
        return None


@sync_to_async
def get_user_subscription(user_id):
    try:
        subscription = UserSubscriptionSettings.objects.get(user=user_id)
        return subscription
    except UserSubscriptionSettings.DoesNotExist:
        return None


@sync_to_async
def save_subscription_settings_to_db(username, filters, interval_choice):
    """
    Сохраняет или обновляет настройки подписки пользователя с нужным crontab-расписанием.
    выбор интервала: 'minute', 'day', 'week'
    """
    user = TgUser.objects.get(username=username)
    match interval_choice:
        case 'minute':
            crontab, _ = CrontabSchedule.objects.get_or_create(
                minute='*', hour='*', day_of_week='*',
                day_of_month='*', month_of_year='*'
            )
        case 'day':
            crontab, _ = CrontabSchedule.objects.get_or_create(
                minute='0', hour='9', day_of_week='*',
                day_of_month='*', month_of_year='*'
            )
        case 'week':
            crontab, _ = CrontabSchedule.objects.get_or_create(
                minute='0', hour='10', day_of_week='1',
                day_of_month='*', month_of_year='*'
            )
        case _:
            raise ValueError('Unknown interval')

    subscription, _ = UserSubscriptionSettings.objects.update_or_create(
        user=user,
        filters=filters,
        crontab=crontab,
    )


@sync_to_async
def get_periodic_task(username):
    try:
        task = PeriodicTask.objects.get(name=username)
        return task
    except PeriodicTask.DoesNotExist:
        return None
        



