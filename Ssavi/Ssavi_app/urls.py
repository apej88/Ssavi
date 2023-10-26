from django.urls import path
from . import views

urlpatterns = [
    path('', views.album_list, name='index'),
    path('detail/<str:ab_id>/', views.detail, name='detail'),
    path('analysis/<str:song_id>/', views.analysis, name='analysis'),
    path('genre_albums/', views.recommend, name='genre_albums'),
    
    path('music_recommend/', views.music_recommend, name='music_recommend'),
    path('like_track/', views.like_track, name='like_track'),
    path('like_album/', views.like_album, name='like_album'),
    path('album/search/', views.album_search, name='album_search'),

    path('mypage/', views.mypage, name='mypage'),
    path('playlist/', views.playlist, name='playlist'),
    path('liked_album/', views.liked_album, name='liked_album'),
    path('liked_track/', views.liked_track, name='liked_track'),
    path('delPlayList/<str:pk>', views.delPlayList, name='delete'),
]