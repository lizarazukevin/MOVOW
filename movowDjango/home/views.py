from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

# Create your views here.
class HomeView(generic.ListView):
    template_name = "home/home.html"

    def get_queryset(self):
        return HttpResponse("200")
    
class QuestionView(generic.ListView):
    template_name = "home/question.html"

    def get_queryset(self):
        return HttpResponse("200")

class ProfileView(generic.ListView):
    template_name = "home/profile.html"

    def get_queryset(self):
        return HttpResponse("200")
    
class SignInView(generic.ListView):
    template_name = "home/signin.html"

    def get_queryset(self):
        return HttpResponse("200")
    
class ListView(generic.ListView):
    template_name = "home/list.html"

    def get_queryset(self):
        return HttpResponse("200")
    
class SearchView(generic.ListView):
    template_name = "home/search.html"

    def get_queryset(self):
        return HttpResponse("200")

# These need to eventually be Detailed view with a slug
class MovieView(generic.ListView):
    template_name = "home/movie_info.html"

    def get_queryset(self):
        return HttpResponse("200")
    
class ShowView(generic.ListView):
    template_name = "home/show_info.html"

    def get_queryset(self):
        return HttpResponse("200")
    
class ActorView(generic.ListView):
    template_name = "home/actor.html"

    def get_queryset(self):
        return HttpResponse("200")