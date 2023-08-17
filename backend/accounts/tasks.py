# from datetime import timedelta
#
# from celery import shared_task
# from django.utils import timezone
#
# from .models import NewUser
#
#
# @shared_task
# def delete_inactive_accounts():
#     # Вычисляем дату, которая будет представлять "сегодня минус time_subtract"
#     time_subtract = 180
#     six_months_ago = timezone.now() - timedelta(days=time_subtract)
#
#     # Получаем список неактивных аккаунтов, которые неактивны более 6 месяцев
#     inactive_accounts = NewUser.objects.filter(is_active=False, time_deleted__lte=six_months_ago)
#
#     # Удаляем неактивные аккаунты
#     for account in inactive_accounts:
#         account.delete()
