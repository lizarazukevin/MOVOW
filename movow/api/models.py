from django.db import models


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

    def __str__(self):
        return f"{self.movie_title} {self.movie_id} {self.release_date}"

class Genres(models.Model):
    genre_id = models.IntegerField(primary_key=True)
    genre_name = models.CharField(max_length=255, unique=True, null=False)
    movies = models.ManyToManyField(Movies)

    def __str__(self):
        return f"{self.genre_name} {self.genre_id}"


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

    def __str__(self):
        return f"{self.person_name} {self.person_id} {self.gender}"


class PeopleAliases(models.Model):
    person_id = models.ForeignKey(People, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} {self.person_id}"


class MovieCastingCredits(models.Model):
    credit_id = models.IntegerField(primary_key=True)
    movie_id = models.ForeignKey(Movies, on_delete=models.CASCADE)
    person_id = models.ForeignKey(People, on_delete=models.CASCADE)
    character = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.character} {self.credit_id}"
