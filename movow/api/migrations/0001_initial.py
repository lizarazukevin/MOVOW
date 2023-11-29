# Generated by Django 4.2.7 on 2023-11-29 00:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Movies",
            fields=[
                ("movie_id", models.IntegerField(primary_key=True, serialize=False)),
                ("tag", models.CharField(max_length=255, unique=True)),
                ("movie_title", models.CharField(max_length=255)),
                ("original_title", models.CharField(max_length=255)),
                ("release_date", models.DateField()),
                ("runtime", models.IntegerField()),
                ("status", models.CharField(max_length=255)),
                ("audience_rating", models.FloatField()),
                ("num_ratings", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="People",
            fields=[
                ("person_id", models.IntegerField(primary_key=True, serialize=False)),
                ("tag", models.CharField(max_length=255, unique=True)),
                ("person_name", models.CharField(max_length=255)),
                ("birthday", models.DateField()),
                ("death", models.DateField()),
                ("gender", models.IntegerField()),
                ("department", models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name="PeopleAliases",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "person_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.people"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MovieCastingCredits",
            fields=[
                ("credit_id", models.IntegerField(primary_key=True, serialize=False)),
                ("character", models.CharField(max_length=255)),
                (
                    "movie_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.movies"
                    ),
                ),
                (
                    "person_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.people"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Genres",
            fields=[
                ("genre_id", models.IntegerField(primary_key=True, serialize=False)),
                ("genre_name", models.CharField(max_length=255, unique=True)),
                ("movies", models.ManyToManyField(to="api.movies")),
            ],
        ),
    ]