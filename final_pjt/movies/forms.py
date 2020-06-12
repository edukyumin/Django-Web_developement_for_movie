from django import forms
from .models import Review, Comment, Movie, Genre


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["title", "rank", "content",]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content",]


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'