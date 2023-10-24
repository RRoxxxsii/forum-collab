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
    path('mark-answer-solving/<int:pk>/', views.MarkAnswerSolving.as_view(), name='mark-answer-solving'),

    # Комментарии
    path('create-comment/', views.CommentAPIView.as_view(), name='create-comment'),
    path('update-comment/<int:pk>/', views.UpdateCommentAPIView.as_view(), name='update-comment'),
    path('retrieve-comment/<int:pk>/', views.RetrieveCommentAPIView.as_view(), name='detail-comment'),

    path('complain/<str:content_type>/<int:content_id>/', views.ComplainAPIView.as_view(), name='complain')
]

router = DefaultRouter()
router.register(r'likes', views.LikeDislikeViewSet, basename='like-dislike')
router.register(r'questions', views.QuestionViewSet, basename='question')
router.register(r'answers', views.AnswerViewSet, basename='answer')

urlpatterns += router.urls
