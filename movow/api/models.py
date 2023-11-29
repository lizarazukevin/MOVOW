from django.db import models


class ApiGenres(models.Model):
    genre_id = models.IntegerField(primary_key=True)
    genre_name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'api_genres'


class ApiGenresMovies(models.Model):
    id = models.BigAutoField(primary_key=True)
    genres = models.ForeignKey(ApiGenres, models.DO_NOTHING)
    movies = models.ForeignKey('ApiMovies', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_genres_movies'
        unique_together = (('genres', 'movies'),)


class ApiMoviecastingcredits(models.Model):
    credit_id = models.IntegerField(primary_key=True)
    character = models.CharField(max_length=255)
    movie_id = models.ForeignKey('ApiMovies', models.DO_NOTHING)
    person_id = models.ForeignKey('ApiPeople', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_moviecastingcredits'


class ApiMovies(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    tag = models.CharField(unique=True, max_length=255)
    movie_title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255)
    release_date = models.DateField()
    runtime = models.IntegerField()
    status = models.CharField(max_length=255)
    audience_rating = models.FloatField()
    num_ratings = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'api_movies'


class ApiPeople(models.Model):
    person_id = models.IntegerField(primary_key=True)
    tag = models.CharField(unique=True, max_length=255)
    person_name = models.CharField(max_length=255)
    birthday = models.DateField()
    death = models.DateField()
    gender = models.IntegerField()
    department = models.CharField()

    class Meta:
        managed = False
        db_table = 'api_people'


class ApiPeoplealiases(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    person_id = models.ForeignKey(ApiPeople, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_peoplealiases'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Episodes(models.Model):
    episode_id = models.AutoField(primary_key=True)
    season = models.ForeignKey('Seasons', models.DO_NOTHING)
    tag = models.CharField(max_length=255)
    episode_title = models.CharField(max_length=255)
    chron_order = models.IntegerField(blank=True, null=True)
    runtime = models.IntegerField(blank=True, null=True)
    audience_rating = models.FloatField(blank=True, null=True)
    num_ratings = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'episodes'


class Genres(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'genres'


class MovieCastingCredits(models.Model):
    credit_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey('Movies', models.DO_NOTHING)
    person = models.ForeignKey('People', models.DO_NOTHING)
    character = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_casting_credits'


class MovieCrewCredits(models.Model):
    credit_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey('Movies', models.DO_NOTHING)
    person = models.ForeignKey('People', models.DO_NOTHING)
    department = models.CharField(max_length=255, blank=True, null=True)
    job = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_crew_credits'


class MovieGenres(models.Model):
    movie = models.ForeignKey('Movies', models.DO_NOTHING, blank=True, null=True)
    genre = models.ForeignKey(Genres, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_genres'


class MovieReviews(models.Model):
    review_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey('Movies', models.DO_NOTHING)
    tag = models.CharField(unique=True, max_length=255)
    author_name = models.CharField(max_length=255, blank=True, null=True)
    author_username = models.CharField(max_length=255, blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    content = models.CharField(max_length=4095, blank=True, null=True)
    time_created = models.DateTimeField(blank=True, null=True)
    time_updated = models.DateTimeField(blank=True, null=True)
    origin = models.CharField(max_length=255)
    reference = models.CharField(max_length=2047)

    class Meta:
        managed = False
        db_table = 'movie_reviews'


class Movies(models.Model):
    movie_id = models.AutoField(primary_key=True)
    tag = models.CharField(unique=True, max_length=255)
    movie_title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    runtime = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    audience_rating = models.FloatField(blank=True, null=True)
    num_ratings = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movies'


class People(models.Model):
    person_id = models.AutoField(primary_key=True)
    tag = models.CharField(unique=True, max_length=255)
    person_name = models.CharField(max_length=255)
    birthday = models.DateField(blank=True, null=True)
    death = models.DateField(blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people'


class PeopleAliases(models.Model):
    person = models.ForeignKey(People, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people_aliases'


class Providers(models.Model):
    provider_id = models.AutoField(primary_key=True)
    provider_name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'providers'


class RegionProvidedMovies(models.Model):
    movie = models.ForeignKey(Movies, models.DO_NOTHING)
    region = models.ForeignKey('Regions', models.DO_NOTHING)
    provider = models.ForeignKey(Providers, models.DO_NOTHING)
    rent = models.BooleanField()
    rent_price = models.FloatField(blank=True, null=True)
    buy = models.BooleanField()
    buy_price = models.FloatField(blank=True, null=True)
    flatrate = models.BooleanField()
    flatrate_price = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'region_provided_movies'


class RegionProvidedSeasons(models.Model):
    season = models.ForeignKey('Seasons', models.DO_NOTHING)
    region = models.ForeignKey('Regions', models.DO_NOTHING)
    provider = models.ForeignKey(Providers, models.DO_NOTHING)
    rent = models.BooleanField()
    rent_price = models.FloatField(blank=True, null=True)
    buy = models.BooleanField()
    buy_price = models.FloatField(blank=True, null=True)
    flatrate = models.BooleanField()
    flatrate_price = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'region_provided_seasons'


class RegionProvidedShows(models.Model):
    show = models.ForeignKey('Shows', models.DO_NOTHING)
    region = models.ForeignKey('Regions', models.DO_NOTHING)
    provider = models.ForeignKey(Providers, models.DO_NOTHING)
    rent = models.BooleanField()
    rent_price = models.FloatField(blank=True, null=True)
    buy = models.BooleanField()
    buy_price = models.FloatField(blank=True, null=True)
    flatrate = models.BooleanField()
    flatrate_price = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'region_provided_shows'


class Regions(models.Model):
    region_id = models.AutoField(primary_key=True)
    iso = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'regions'


class SeasonCastingCredits(models.Model):
    credit_id = models.AutoField(primary_key=True)
    season = models.ForeignKey('Seasons', models.DO_NOTHING)
    person = models.ForeignKey(People, models.DO_NOTHING)
    character = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'season_casting_credits'


class SeasonCrewCredits(models.Model):
    credit_id = models.AutoField(primary_key=True)
    season = models.ForeignKey('Seasons', models.DO_NOTHING)
    person = models.ForeignKey(People, models.DO_NOTHING)
    department = models.CharField(max_length=255, blank=True, null=True)
    job = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'season_crew_credits'


class Seasons(models.Model):
    season_id = models.AutoField(primary_key=True)
    show = models.ForeignKey('Shows', models.DO_NOTHING)
    tag = models.CharField(max_length=255)
    season_title = models.CharField(max_length=255)
    chron_order = models.IntegerField(blank=True, null=True)
    num_episodes = models.IntegerField(blank=True, null=True)
    audience_rating = models.FloatField(blank=True, null=True)
    num_ratings = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seasons'


class ShowCastingCredits(models.Model):
    credit_id = models.AutoField(primary_key=True)
    show = models.ForeignKey('Shows', models.DO_NOTHING)
    person = models.ForeignKey(People, models.DO_NOTHING)
    character = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'show_casting_credits'


class ShowCrewCredits(models.Model):
    credit_id = models.AutoField(primary_key=True)
    show = models.ForeignKey('Shows', models.DO_NOTHING)
    person = models.ForeignKey(People, models.DO_NOTHING)
    department = models.CharField(max_length=255, blank=True, null=True)
    job = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'show_crew_credits'


class ShowGenres(models.Model):
    show = models.ForeignKey('Shows', models.DO_NOTHING, blank=True, null=True)
    genre = models.ForeignKey(Genres, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'show_genres'


class ShowReviews(models.Model):
    review_id = models.AutoField(primary_key=True)
    show = models.ForeignKey('Shows', models.DO_NOTHING)
    tag = models.CharField(unique=True, max_length=255)
    author_name = models.CharField(max_length=255, blank=True, null=True)
    author_username = models.CharField(max_length=255, blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    content = models.CharField(max_length=4095, blank=True, null=True)
    time_created = models.DateTimeField(blank=True, null=True)
    time_updated = models.DateTimeField(blank=True, null=True)
    origin = models.CharField(max_length=255)
    reference = models.CharField(max_length=2047)

    class Meta:
        managed = False
        db_table = 'show_reviews'


class Shows(models.Model):
    show_id = models.AutoField(primary_key=True)
    tag = models.CharField(unique=True, max_length=255)
    show_title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, blank=True, null=True)
    initial_release = models.DateField(blank=True, null=True)
    final_release = models.DateField(blank=True, null=True)
    num_episodes = models.IntegerField(blank=True, null=True)
    num_seasons = models.IntegerField(blank=True, null=True)
    in_production = models.BooleanField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shows'
