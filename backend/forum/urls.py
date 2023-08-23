from django.urls import path

from forum import views

urlpatterns = [
    # Вопросы
    path('ask-question/', views.AskQuestionAPIView.as_view(), name='ask-question'),
    path('update-question/<int:pk>/', views.UpdateQuestionAPIView.as_view(), name='update-question'),

    # Ответы
    path('answer-question/', views.AnswerQuestionAPIView.as_view(), name='answer-question'),
    path('update-answer/<int:pk>/', views.UpdateQuestionAnswerAPIView.as_view(), name='update-answer'),

    # Комментарии
]

