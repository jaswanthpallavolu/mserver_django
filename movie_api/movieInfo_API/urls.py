from django.urls import path
from . import views

urlpatterns = [
    path('info/<str:id>/', views.movie),

    path('search/matches/<str:name>/', views.searchMatches),
    path('search/<str:name>/', views.search),

    path('genres/', views.getGenreMovies),
    path('filter/', views.filtering),

    path('tags/<str:name>/', views.listMoviesByTags),
    path('tags/', views.listTags),

]
