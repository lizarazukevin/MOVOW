from django.shortcuts import render

from django.db import DatabaseError

from .models import *
from .serializers import *

from rest_framework.response import Response
from rest_framework.decorators import api_view

# Default routes
@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/movies/',
            'method': 'GET',
            'body': None,
            'description': 'Return a list of all the movies'
        },
        {
            'Endpoint': '/shows/',
            'method': 'GET',
            'body': None,
            'description': 'Return a list of all the shows'  
        }
    ]

    return Response(routes)

@api_view(['GET'])
def getMovies(request):
    try:
        movies = Movies.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    except DatabaseError as e:
        print(f"Database Error: {e}")
        return Response({"error": "Internal Server Error"}, 500)
    

@api_view(['GET'])
def getShows(request):
    try:
        shows = Shows.objects.all()
        serializer = ShowSerializer(shows, many=True)
        return Response(serializer.data)
    except DatabaseError as e:
        print(f"Database Error: {e}")
        return Response({"error": "Internal Server Error"}, 500)