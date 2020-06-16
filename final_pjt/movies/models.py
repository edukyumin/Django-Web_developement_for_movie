from django.db import models
from django.conf import settings
# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=100)
    # genre가 숫자로 들어 가있는 것을 글자로 보여주기 위해서~
    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=100)
    original_title = models.CharField(max_length=100)
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    adult = models.BooleanField()
    video = models.BooleanField()
    overview = models.TextField()
    original_language = models.CharField(max_length=30)
    poster_path = models.CharField(max_length=255, null=True)
    backdrop_path = models.CharField(max_length=255, null=True)
    # 원래 genres
    genre_ids = models.ManyToManyField(Genre, related_name='genre_ids')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='like_users')



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


class Recommand(models.Model):
    genre_recommand = models.ManyToManyField(Genre, null=True,  related_name='genre_recommand')
    adult = models.BooleanField(null=True)
    popularity = models.FloatField(null=True)
    vote_average = models.FloatField(null=True)
    release_date = models.DateField(null=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)