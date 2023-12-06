from rest_framework.serializers import ModelSerializer
from .models import *

class MovieSerializer(ModelSerializer):
    class Meta:
        model = Movies
        fields = '__all__'

class ShowSerializer(ModelSerializer):
    class Meta:
        model = Shows
        fields = '__all__'
        
class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genres
        fields = '__all__'

class PeopleSerializer(ModelSerializer):
    class Meta:
        model = People
        fields = '__all__'

class PeopleAliasesSerializer(ModelSerializer):
    class Meta:
        model = PeopleAliases
        fields = '__all__'

class CastingSerializer(ModelSerializer):
    class Meta:
        model = MovieCastingCredits
        fields = '__all__'