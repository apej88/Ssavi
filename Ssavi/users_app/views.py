from django.shortcuts import render

# Create your views here.

# 로그인 폼을 띄우고 로그인 진행한다
def sign_in(request):
    return render(request, 'users_app/sign_in.html')

# 회원가입 폼을 띄우고 가입 진행한다
def sign_up(request):
    return render(request, 'users_app/sign_up.html')