from django.urls import path

from forum import views

urlpatterns = [
    path('ask-question/', views.AskQuestionAPIView.as_view(), name='ask-question'),
    path('answer-question/', views.AnswerQuestionAPIView.as_view(), name='answer-question'),
    path('update-answer/', views.UpdateAnswerAPIView.as_view(), name='update-answer'),

]

