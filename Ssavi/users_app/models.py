from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):

    # 이메일은 기본적으로 묻는 관계로 초기 생성 시 필요 없음
    # 이름, 선호장르 필드
    user_name = models.CharField(max_length=100)
    user_genre = models.CharField(max_length=200)

class UsersAppUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    user_name = models.CharField(max_length=100)
    user_genre = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'users_app_user'