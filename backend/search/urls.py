from django.urls import path

from . import views

urlpatterns = [
    path('search', views.SearchResultAPIView.as_view(), name='search-list'),
]
