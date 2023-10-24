from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<str:ab_id>/', views.detail, name='detail'),
    path('analysis/<str:song_id>/', views.analysis, name='analysis'),
    path('recommend/', views.recommend, name='recommend'),
    path('genre_albums/', views.recommend, name='genre_albums'),
    path('music_recommend/', views.music_recommend, name='music_recommend'),
]