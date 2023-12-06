from django.shortcuts import render

from django.db import DatabaseError

from .models import *
from .serializers import *
from .utils import *

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
    if request.method == 'GET':
        return getMoviesList(request)
    
@api_view(['GET'])
def getMovie(request, pk):
    if request.method == 'GET':
        return getMovieDetail(request, pk)
    

@api_view(['GET'])
def getShows(request):
    if request.method == 'GET':
        return getShowsList(request)
    
@api_view(['GET'])
def getShow(request, pk):
    if request.method == 'GET':
        return getShowDetail(request, pk)