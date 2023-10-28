from django.urls import path
from . import views

urlpatterns = [
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('id_check/', views.id_check, name='id_check'),
    path('user_update/', views.user_update, name='user_update'),
    path('user_pwd_check/', views.password_check, name='pwd_check')
]