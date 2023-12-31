from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import login, logout
from .models import User, UsersAppUser
from .forms import UserForm

# Create your views here.

# 로그인 폼을 띄우고 로그인 진행한다
def sign_in(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
    else:
        form = AuthenticationForm()

    return render(request, 'users_app/sign_in.html', {'form':form})

def sign_out(request):
    logout(request)
    return redirect('index')

# 회원가입 폼을 띄우고 가입 진행한다
def sign_up(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user_name = request.POST['user_name']
        user_genre = ','.join(request.POST.getlist('genre_list'))

        user = User.objects.create_user(username, email, password)
        user.user_name = user_name
        user.user_genre = user_genre

        user.save()
        return redirect('sign_in')

    else:
        form = UserForm()

    return render(request, 'users_app/sign_up.html', {'form':form})

# 작성하다 만 아이디 체크
def id_check(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username', None)
            if username:
                if UsersAppUser.objects.filter(username=username).exists():
                    return JsonResponse({'is_taken':True})
                else:
                    return JsonResponse({'is_taken':False})
        except IntegrityError:
            return redirect('sign_up')

    else:
        return JsonResponse({'error':'올바르지 않은 형식입니다'})

@login_required
def user_update(request):
    user = request.user
    if request.method == 'POST':
        user.user_name = request.POST['user_name']
        user.email = request.POST['email']

        user_genre = ','.join(request.POST.getlist('genre_list'))
        user.user_genre = user_genre

        new_password = request.POST['new_password']
        if new_password:
            user.set_password(new_password)

        user.save()
        messages.success(request, '회원정보 수정이 완료되었습니다.')

        return redirect('sign_in')
    else:
        return render(request, 'users_app/user_update.html')
    
@login_required
def password_check(request):
    if request.method == 'POST':
        password_check = request.POST.get('password', None)

        if password_check is not None:
            user = request.user
            if user.check_password(password_check):
                return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})

    return render(request, 'users_app/password_check.html')