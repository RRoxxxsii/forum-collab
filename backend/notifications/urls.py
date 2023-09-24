from django.urls import path

from notifications import views

urlpatterns = [
    path('', views.UserNotificationListAPIView.as_view(), name='notifications')
]

