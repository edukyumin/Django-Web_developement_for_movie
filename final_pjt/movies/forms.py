from django import forms
from .models import Review, Comment, Movie, Genre, Recommand


class MovieForm(forms.ModelForm):
    # 
    genre_ids = forms.ModelMultipleChoiceField(
        label = 'Genre',
        queryset = Genre.objects.all(),
        widget = forms.CheckboxSelectMultiple,
    )
    # release_date 를 달력으로 고르기
    release_date = forms.DateField(
        widget=forms.widgets.DateInput(attrs={'type': 'date'})
    )
    class Meta:
        model = Movie
        fields = ["title", "original_title", "release_date", "popularity", "vote_count", "vote_average", "adult", "video", "overview", "original_language", "poster_path", "backdrop_path", "genre_ids",]

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["title", "rank", "content",]


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label = '댓글달기'
    )
    class Meta:
        model = Comment
        fields = ["content",]


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'


class RecommandForm(forms.ModelForm):
    genre_recommand = forms.ModelMultipleChoiceField(
        label = '원하시는 장르를 고르시오.',
        queryset = Genre.objects.all(),
        widget = forms.CheckboxSelectMultiple,
    )
    release_date = forms.DateField(
        widget=forms.widgets.DateInput(attrs={'type': 'date'})
        )
    class Meta:
        model = Recommand
        fields = ["genre_recommand", "popularity", "vote_average", "release_date", "adult",] 