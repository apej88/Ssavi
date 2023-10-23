from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<str:ab_id>/', views.detail, name='detail'),
    path('analysis/<str:song_id>/', views.analysis, name='analysis'),
    path('recommend/', views.recommend, name='recommend'),
    # path('toggle-like-album/', views.toggle_like_album, name='toggle-like-album'),
    
]