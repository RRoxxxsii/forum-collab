from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from accounts import views

urlpatterns = [
    path('create-account/', views.CustomUserRegisterAPIView.as_view(), name='create-account'),

    # Подтверждение почты при регистрации
    path('confirm-email/', views.RequestEmailToConfirmAPIView.as_view(), name='confirm-email-request'),
    path('email-confirmation-result/', views.ConfirmEmailAPIView.as_view(), name='email-confirmation-result'),

    # Смена почты
    path('change-email-confirm/', views.ChangeEmailAddressAPIView.as_view(), name='change-email-confirm'),
    path('new-email-confirmation-result/', views.ConfirmNewEmailAPIView.as_view(),
         name='new-email-confirmation-result'),

    # Аутентификация по JWT-токенам
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
