from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Review, Comment, Movie, Genre, Recommand
from .forms import ReviewForm, CommentForm, MovieForm, GenreForm, RecommandForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
import random, requests, datetime


def index(request):
    movies = Movie.objects.order_by('-release_date') # 영화 개봉일 순으로 정렬하기
    genres = Genre.objects.all()
    paginator = Paginator(movies, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    # YOUTUBE_API_KEY='AIzaSyARmKeLqm3doSnkEbYhGjRkxXj-25YuYd8'
    
    # YOUTUBE_URL = 'https://www.googleapis.com/youtube/v3/search'
    # random_number = range(0, 9)
    # top_movies = movies[int(random.choice(random_number))]
    
    # params = {
    #     'key': YOUTUBE_API_KEY,
    #     'part': 'snippet',
    #     'type': 'video',
    #     'q': top_movies.title + 'trailer'
    # }
    # response = requests.get(YOUTUBE_URL, params=params).json()
    # video_id = response['items'][0]['id']['videoId']
    # video = f'https://www.youtube.com/embed/{video_id}?autoplay=1'

    context = {
        'page_obj': page_obj,
        'movies' : movies,
        'genres' : genres,
        # 'video' : video,
        # 'my_movie': movies[0],
        # 'top_movies' : top_movies
    }
    return render(request, 'movies/index.html', context)

####################################################################################
## MOVIE ##

@login_required
def movie_create(request):
    ## superuser만 movie_create할 수 있음
    if not request.user.is_superuser:
        return redirect('movies:index')
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save()
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
    if not request.user.is_superuser:
        return redirect('movies:index')
    if request.user.is_superuser:
        if request.method == 'POST':
            form = MovieForm(request.POST, instance=movie)
            if form.is_valid():
                movie = form.save()
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
    if not request.user.is_superuser:
        return redirect('movies:index')
    if request.user.is_superuser:
        movie.delete()
    return redirect('movies:index')

##################################################################################
## REVIEW ##

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
    genres = movie.genre_ids.all()
    ## youtube에서 트레일러 가져오기

    # YOUTUBE_API_KEY='AIzaSyARmKeLqm3doSnkEbYhGjRkxXj-25YuYd8'
    # YOUTUBE_URL = 'https://www.googleapis.com/youtube/v3/search'
    # params = {
    #     'key': YOUTUBE_API_KEY,
    #     'part': 'snippet',
    #     'type': 'video',
    #     'q': movie.title + 'trailer'
    # }
    # response = requests.get(YOUTUBE_URL, params=params).json()
    # video_id = response['items'][3]['id']['videoId']
    # video = f'https://www.youtube.com/embed/{video_id}'
    context = {
        'movie': movie,
        'reviews': reviews,
        'genres': genres,
        # 'video': video
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

#######################################################################################
## COMMENT ##

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

    ## 좋아요 취소
    if movie.like_users.filter(pk=user.pk).exists():
        movie.like_users.remove(user)
        liked = False

    ## 좋아요
    else:
        movie.like_users.add(user)
        liked = True

    context = {
        'count': movie.like_users.count(),
        'liked': liked,
    }
    return JsonResponse(context)


#################################################################################
## 아래는 장르를 생성하는 관리자용 기능. (사용하지 않았음)
## Genre ##

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

#########################이 위=의 기능은 사용하지 않았음(장르생성, 장르수정)##################################################################
## RECOMMEND ##

@login_required
def choice_create(request):
    recommand = get_object_or_404(Recommand)
    if request.method == 'POST':
        form = RecommandForm(request.POST, instance=recommand)
        if form.is_valid():
            recommand = form.save()
            return redirect('movies:recommend')
    else:
        form = RecommandForm(instance=recommand)
    context = {
        'form': form,
    }
    return render(request, 'movies/recommand_form.html', context)


@login_required
def recommend(request):
    movies = Movie.objects.order_by('-vote_average') #괜찮은 영화 순서대로 뽑기 위해서 -voteaverage로 정렬
    genres = Genre.objects.all()
    # 추천요청 데이터 전부
    recommands = Recommand.objects.all()
    # 추천요청 중 장르만 뽑은 것
    genre_recommands = Recommand.objects.values('genre_recommand')
    choices = []
    if request.user.id != None: # 로그인한 유저라면
        # 이하는 추천 알고리즘
        # form에 들어간 genre 에 따라
        choice_genres = []
        check = 1
        for favorite_genre in genre_recommands:
            choice_genres.append(favorite_genre['genre_recommand'])
            check = check * favorite_genre['genre_recommand']
##########################################################################################
        for movie in movies:
            compare = 1
            compare2 = []
            for movie_genre in movie.genre_ids.all():
                compare = compare * movie_genre.id
                compare2.append(movie_genre.id)
            ####아닌것들 제외하기 위한 조건
            if compare % check == 0:
                flag = True
                for x in choice_genres:
                    if x not in compare2:
                        flag = False
                if flag == True:
                    if Recommand.objects.values('adult').get()['adult'] == movie.adult:
                        # form에 들어간 popularity 에 따라
                        if Recommand.objects.values('popularity').get()['popularity'] <= movie.popularity:
                             # form에 들어간 vote_average 에 따라
                            if Recommand.objects.values('vote_average').get()['vote_average'] <= movie.vote_average:
                                # form에 입력한 release_date에 따라
                                # 값이 작을수록 최신에 개봉한 영화입니다.
                                if datetime.datetime.strptime(str(Recommand.objects.values('release_date').get()['release_date']), "%Y-%m-%d") <= datetime.datetime.strptime(str(movie.release_date), "%Y-%m-%d"):
                                    choices.append(movie)
 
    context = {
        'movies' : movies,
        'choices' : choices,
        'genres': genres,
        'recommands' : recommands,
        'genre_recommands' : genre_recommands,
        
    }
    return render(request, 'movies/recommand.html', context)


