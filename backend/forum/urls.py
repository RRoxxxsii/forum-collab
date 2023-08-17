from django.urls import path

from forum import views

urlpatterns = [
    path('ask-question/', views.AskQuestionAPIView.as_view(), name='ask-question'),

]

