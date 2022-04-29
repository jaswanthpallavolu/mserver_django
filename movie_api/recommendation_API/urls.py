from django.urls import path
from . import views

urlpatterns = [
    path('contentbased/<str:movieId>/', views.contentBased),
    path('collaborative/', views.collaborativeFilter)
]
