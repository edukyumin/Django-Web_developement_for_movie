from django.db import models
from django.conf import settings
# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    original_title = models.CharField(max_length=100, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    popularity = models.FloatField(blank=True, null=True)
    vote_count = models.IntegerField(blank=True, null=True)
    vote_average = models.FloatField(blank=True, null=True)
    adult = models.BooleanField(blank=True, null=True)
    video = models.BooleanField(blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    original_language = models.CharField(max_length=30, blank=True, null=True)
    poster_path = models.CharField(max_length=255, blank=True, null=True)
    backdrop_path = models.CharField(max_length=255, blank=True, null=True)
    # 원래 genres
    genre_ids = models.ManyToManyField(Genre, related_name='genres_ids')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_users')


class Review(models.Model):
    title = models.CharField(max_length=100)
    rank = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
