from django.urls import path
from forum import views
from rest_framework.routers import DefaultRouter

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

    path('top-tags/', views.ThemeTagsAPIView.as_view(), name='top-tags'),

    path('complain/<str:content_type>/<int:content_id>/', views.ComplainAPIView.as_view(), name='complain')
]

router = DefaultRouter()
router.register(r'likes', views.LikeDislikeViewSet, basename='like-dislike')
router.register(r'questions', views.QuestionViewSet, basename='question')
router.register(r'answers', views.AnswerViewSet, basename='answer')

urlpatterns += router.urls
