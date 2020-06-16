from django.contrib import admin
from. models import Genre, Movie, Recommand

# Register your models here.
admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Recommand)