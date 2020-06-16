from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Review, Comment, Movie, Genre
from .forms import ReviewForm, CommentForm, MovieForm, GenreForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
import random
import requests


def index(request):
    movies = Movie.objects.order_by('-release_date') # 영화 개봉일 순으로 정렬하기
    genres = Genre.objects.all()
    paginator = Paginator(movies, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'movies' : movies,
        'genres' : genres,
    }
    return render(request, 'movies/index.html', context)


@login_required
def movie_create(request):
    # superuser만 movie_create할 수 있음
    if not request.user.is_superuser:
        return redirect('movies:index')
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save()
            # movie.user = request.user
            # movie.save()
            return redirect('movies:index')
    else:
        form = MovieForm()
    context = {
        'form': form,
    }
    return render(request, 'movies/movie_form.html', context)


@login_required
def movie_update(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    # superuser만 movie_update할 수 있음
    if not request.user.is_superuser:
        return redirect('movies:index')
    # if request.user == movie.user:
    if request.user.is_superuser:
        if request.method == 'POST':
            form = MovieForm(request.POST, instance=movie)
            if form.is_valid():
                movie = form.save()
                # movie = form.save(commit=False)
                # movie.user = request.user
                # movie.save()
                return redirect('movies:index')
        else:
            form = MovieForm(instance=movie)
        context = {
            'form': form,
            'movie': movie,
        }
        return render(request, 'movies/movie_form.html', context)

@login_required
@require_POST
def movie_delete(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    # superuser만 movie_delete할 수 있음
    if not request.user.is_superuser:
        return redirect('movies:index')
    # if request.user == movie.user:
    if request.user.is_superuser:
        movie.delete()
    return redirect('movies:index')

################################################
# Review #

@login_required
def create(request, movie_pk):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            movie = get_object_or_404(Movie, pk=movie_pk)
            review.movie = movie
            review.save()
            return redirect('movies:detail', movie_pk)
    else:
        form = ReviewForm()
    context = {
        'form': form,
    }
    return render(request, 'movies/form.html', context)


def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = movie.review_set.all()
    # genre 뽑기
    genres = movie.genre_ids.all()
    # youtube에서 트레일러 가져오기
    # API_KEY : kyumin_api
    
    # const API_KEY = process.env.VUE_APP_YOUTUBE_API_KEY
    # const API_URL = 'https://www.googleapis.com/youtube/v3/search'
    # VUE_APP_YOUTUBE_API_KEY=AIzaSyC1tQrciIigfPf2s0Acn9xsYsNgagaWT5g

    YOUTUBE_API_KEY='AIzaSyBzP1Nq0VtqllvL8V2vag0H7nLfXCNAtKY'
    # AIzaSyDU-_eW6fNS1ThG4DjvDS10G00OjsrnzgE
    YOUTUBE_URL = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'key': YOUTUBE_API_KEY,
        'part': 'snippet',
        'type': 'video',
        'q': movie.title + 'trailer'
    }
    response = requests.get(YOUTUBE_URL, params=params).json()
    # print(response)
    video_id = response['items'][3]['id']['videoId']
    # print(video_id)
    video = f'https://www.youtube.com/embed/{video_id}'
    # print(video)
    context = {
        'movie': movie,
        'reviews': reviews,
        'genres': genres,
        'video': video
    }
    return render(request, 'movies/detail.html', context)


def review_detail(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)
    comments = review.comment_set.all()
    comment_form = CommentForm()
    context = {
        'movie': movie,
        'review': review,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'movies/review_detail.html', context)


@login_required
def update(request, movie_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user == review.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.save()
                # return redirect('movies:index')
                return redirect('movies:review_detail', movie_pk, review.pk)
        else:
            form = ReviewForm(instance=review)
        context = {
            'form': form,
            'review': review,
        }
        return render(request, 'movies/form.html', context)


@login_required
@require_POST
def delete(request,movie_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user == review.user:
        review.delete()
    return redirect('movies:detail', movie_pk)

#######################################################
# comment #

@login_required
def comments_create(request, movie_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.review = review
            comment.save()
    return redirect('movies:review_detail', movie_pk, review.pk)


@require_POST
@login_required
def comments_delete(request, movie_pk, review_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.user != request.user:
        return redirect('movies:review_detail', movie_pk, review_pk)
    comment.delete()
    return redirect('movies:review_detail', movie_pk, review_pk)


@login_required
def like(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)

    # 좋아요 취소
    if movie.like_users.filter(pk=user.pk).exists():
        movie.like_users.remove(user)
        liked = False

    # 좋아요
    else:
        movie.like_users.add(user)
        liked = True

    context = {
        'count': movie.like_users.count(),
        'liked': liked,
    }
    return JsonResponse(context)


##############################################################################################
# Genre 생성, 수정, 삭제

# @login_required
# def genre_create(request):
#     if request.method == 'POST':
#         form = GenreForm(request.POST)
#         if form.is_valid():
#             genre = form.save(commit=False)
#             genre.user = request.user
#             genre.save()
#             return redirect('movies:index')
#     else:
#         form = GenreForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'movies/genre_form.html', context)


# @login_required
# def genre_update(request, genre_pk):
#     genre = get_object_or_404(Genre, pk=genre_pk)
#     if request.user == genre.user:
#         if request.method == 'POST':
#             form = GenreForm(request.POST, instance=genre)
#             if form.is_valid():
#                 genre = form.save(commit=False)
#                 genre.user = request.user
#                 genre.save()
#                 return redirect('movies:index')
#         else:
#             form = GenreForm(instance=genre)
#         context = {
#             'form': form,
#             'genre': genre,
#         }
#         return render(request, 'movies/genre_form.html', context)


# @login_required
# @require_POST
# def genre_delete(request, genre_pk):
#     genre = get_object_or_404(Genre, pk=genre_pk)
#     if request.user == genre.user:
#         genre.delete()
#     return redirect('movies:index')

#######################################################################
# 영화추천
@login_required
def recommand(request):
    movies = Movie.objects.order_by('-vote_average') #괜찮은 영화 순서대로 뽑기 위해서 -voteaverage로 정렬
    result = []
    if request.user.id != None: # 로그인한 유저라면
        like_movies = request.user.like_users # 로그인한 사람의 정보 저장
        if len(like_movies.all()) != 0: # 좋아요 한게 있어 그러면?
            choice_genres = [] # 비어있는 리스트 만들기
            for favorite_movie in like_movies.all(): # 이사람이 좋아한 영화를 하나씩 꺼내
                for favorite_genre in favorite_movie.genre_ids.all(): # 좋아한 영화의 장르를 모두 꺼내
                    if favorite_genre not in choice_genres: # 중복되지 않게 넣기
                        choice_genres.append(favorite_genre)
            random.shuffle(choice_genres) # 리스트가 순서가 일정하면 같은 장르를 추천하기에 리스트를 한번 섞어준다.

            for movie in movies:
                count = 1
                for genre in choice_genres:
                    if genre in movie.genre_ids.all():
                        if movie not in result: # 중복되지 않게 넣기
                            result.append(movie)
                        # 영화 20개 될때 까지
                        if len(result) >= 20:
                            count = 0
                            break
                if count == 0:
                        break
            # 매번 같은 영화를 추천하면 심심하기 때문에 20개의 영화를 리스트에 넣고 그 중에서 랜덤으로 10개를 뽑기
            results = random.sample(result, 10)
        else:  # 좋아요를 누른 영화(장르)가 없다면
            for k in range(15): # 평점 좋은 영화 15개 중에 10개 랜덤!
                result.append(movies[k])
            results = random.sample(result,10)
    context = {
        'results': results,
    }
    return render(request, 'movies/recommand.html', context)