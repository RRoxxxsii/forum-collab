from django.urls import path
from rest_framework.routers import DefaultRouter

from forum import views

urlpatterns = [
    # Вопросы
    path('ask-question/', views.AskQuestionAPIView.as_view(), name='ask-question'),
    path('update-question/<int:pk>/', views.UpdateQuestionAPIView.as_view(), name='update-question'),

    # Ответы
    path('answer-question/', views.AnswerQuestionAPIView.as_view(), name='answer-question'),
    path('update-answer/<int:pk>/', views.UpdateQuestionAnswerAPIView.as_view(), name='update-answer'),

    # Комментарии
    path('create-comment/', views.CommentAPIView.as_view(), name='create-comment'),
    path('update-comment/<int:pk>/', views.UpdateCommentAPIView.as_view(), name='update-comment'),

]

router = DefaultRouter()
router.register(r'likes', views.LikeDislikeViewSet, basename='like-dislike')
router.register(r'questions', views.QuestionViewSet)
router.register(r'answers', views.AnswerViewSet, basename='answer')

urlpatterns += router.urls
