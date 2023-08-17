from django.urls import path

from forum import views

urlpatterns = [
    path('ask_question/', views.AskQuestionAPIView.as_view(), name='ask-question'),

]

