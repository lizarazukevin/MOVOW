from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes, name="routes"),
    path('movies/', views.getMovies, name="movies"),
    path('movies/<str:pk>/', views.getMovie, name="movie"),
    path('shows/', views.getShows, name="shows"),
    path('shows/<str:pk>/', views.getShow, name="movie"),
]