from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<str:ab_id>/', views.detail, name='detail'),
    path('recommend/', views.recommend, name='recommend'),
    
]