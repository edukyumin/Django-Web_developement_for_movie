from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    # INDEX #
    path('', views.index, name='index'),
    ## GENRE #
    # path('genre_create/', views.genre_create, name='genre_create'),
    # path('<int:genre_pk>/genre_update/', views.genre_update, name='genre_update'),
    # path('<int:genre_pk>/genre_delete/', views.genre_delete, name='genre_delete'),

    # MOVIE #
    path('movie_create/', views.movie_create, name='movie_create'),
    path('<int:movie_pk>/update/', views.movie_update, name='movie_update'),
    path('<int:movie_pk>/delete/', views.movie_delete, name='movie_delete'),
    path('<int:movie_pk>/detail', views.detail, name='detail'),
    # REVIEW #
    path('<int:movie_pk>/create/', views.create, name='create'),
    path('<int:movie_pk>/review_detail/<int:review_pk>/', views.review_detail, name='review_detail'),
    path('<int:movie_pk>/<int:review_pk>/update/', views.update, name='update'),
    path('<int:movie_pk>/<int:review_pk>/delete/', views.delete, name='delete'),
    # COMMENT #
    path('<int:movie_pk>/<int:review_pk>/comments', views.comments_create, name='comments_create'),
    path('<int:movie_pk>/<int:review_pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),
    path('<int:movie_pk>/like/', views.like, name='like'),
    # RECOMMEND #
    path('recommend/', views.recommend, name='recommend'),
    path('choice_create/', views.choice_create, name='choice_create'),
]
