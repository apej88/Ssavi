from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):

    # 이메일은 기본적으로 묻는 관계로 초기 생성 시 필요 없음
    # 이름, 선호장르 필드
    user_name = models.CharField(max_length=100)
    user_genre = models.CharField(max_length=50)