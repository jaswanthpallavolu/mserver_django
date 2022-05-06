from django.urls import path
from . import views

urlpatterns = [
    path('info/<str:id>/', views.movie),
    path('search/<str:name>/', views.search),
    path('genres/', views.getGenreMovies),
    path('tags/<str:name>/', views.listMoviesByTags),
    path('tags/', views.listTags),
    path('filter/',views.filtering),
]
