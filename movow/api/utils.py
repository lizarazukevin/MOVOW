from rest_framework.response import Response
from .models import *
from .serializers import *

from django.db import DatabaseError

# Movies
def getMoviesList(request):
    try:
        movies = Movies.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    except DatabaseError as e:
        print(f"Movie Database Error: {e}")
        return Response({"error": "Internal Server Error"}, 500)
    
def getMovieDetail(request, pk):
    try:
        movie = Movies.objects.get(movie_id=pk)
        serializer = MovieSerializer(movie, many=False)
        return Response(serializer.data)
    except DatabaseError as e:
        print(f"Movie Database Error: {e}")
        return Response({"error": "Internal Server Error"}, 500)

# Shows
def getShowsList(request):
    try:
        shows = Shows.objects.all()
        serializer = ShowSerializer(shows, many=True)
        return Response(serializer.data)
    except DatabaseError as e:
        print(f"Show Database Error: {e}")
        return Response({"error": "Internal Server Error"}, 500)

def getShowDetail(request, pk):
    try:
        show = Shows.objects.get(show_id=pk)
        serializer = ShowSerializer(show, many=False)
        return Response(serializer.data)
    except DatabaseError as e:
        print(f"Show Database Error: {e}")
        return Response({"error": "Internal Server Error"}, 500)
