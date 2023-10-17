from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
def index(request):
    return render(request, 'Ssavi_app/index.html')

def detail(request):
    return render(request, 'Ssavi_app/detail.html')