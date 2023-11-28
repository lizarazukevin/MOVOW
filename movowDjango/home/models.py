from django.db import models
import pymongo


class Movies(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    tag = models.CharField(max_length=255, unique=True, null=False)
    movie_title = models.CharField(max_length=255, null=False)
    original_title = models.CharField(max_length=255)
    release_date = models.DateField()
    runtime = models.IntegerField()
    status = models.CharField(max_length=255)
    audience_rating = models.FloatField()
    num_ratings = models.IntegerField()


class Genres(models.Model):
    genre_id = models.IntegerField(primary_key=True)
    genre_name = models.CharField(max_length=255, unique=True, null=False)
    movies = models.ManyToManyField(Movies)


# class MovieGenres(models.Model):
#     movie_id = models.ForeignKey()


class People(models.Model):
    person_id = models.IntegerField(primary_key=True)
    tag = models.CharField(max_length=255, unique=True, null=False)
    person_name = models.CharField(max_length=255, null=False)
    birthday = models.DateField()
    death = models.DateField()
    gender = models.IntegerField()
    department = models.CharField()


class PeopleAliases(models.Model):
    person_id = models.ForeignKey(People, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)


class MovieCastingCredits(models.Model):
    credit_id = models.IntegerField(primary_key=True)
    movie_id = models.ForeignKey(Movies, on_delete=models.CASCADE)
    person_id = models.ForeignKey(People, on_delete=models.CASCADE)
    character = models.CharField(max_length=255)

