from django.urls import path

from favourites import views


urlpatterns = [
    path('favourites-add/', views.AddToFavouritesAPIView.as_view(), name='add-to-favourites'),
    path('favourites/', views.FavouritesListAPIView.as_view(), name='favourites')
]

