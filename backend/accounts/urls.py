from django.urls import include, path
from rest_framework.routers import DefaultRouter
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

    # Удаление аккаунта
    path('delete-account/', views.DeleteAccountAPIView.as_view(), name='delete-account'),

    # Восстановление аккаунта
    path('restore-account/', views.RestoreAccountAPIView.as_view(), name='restore-account'),
    path('restore-account-email-confirm/', views.RestoreAccountFromEmailAPIView.as_view(),
         name='restore-account-email-confirm'),

    # Смена пароля
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    # Аутентификация по JWT-токенам
    path("token/", views.EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

router = DefaultRouter()
router.register('users', views.UserViewSet)

urlpatterns += router.urls
