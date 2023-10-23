from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User

        fields = (
            'username',
            'password',
            'email',
            'user_name',
            'user_genre'
        )

        labels = {
            'username':'ID',
            'password':'비밀번호',
            'email':'이메일',
            'user_name':'성명',
            'user_genre':'선호 장르'
        }