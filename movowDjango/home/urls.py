from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("question/", views.QuestionView.as_view(), name="question"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("signin/", views.SignInView.as_view(), name="signin"),
    path("list/", views.ListView.as_view(), name="list"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("movie/", views.MovieView.as_view(), name="movieinfo"),
    path("show/", views.ShowView.as_view(), name="showinfo"),
    path("actor/", views.HomeView.as_view(), name="actor"),
]