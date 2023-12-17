from django.urls import path
from notifications import views

urlpatterns = [
    path('', views.UserNotificationListAPIView.as_view(), name='notifications'),
    path('mark-as-read', views.MarkNotificationsAsReadAPIView.as_view(), name='mark-as-read')
]
