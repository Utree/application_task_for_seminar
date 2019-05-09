from django.shortcuts import render
from django.http.response import HttpResponse
# import for file upload
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOADE_DIR = os.path.join(BASE_DIR, 'static/seminar/uploaded')

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'seminar/login.html')

def register(request):
    return render(request, 'seminar/register.html')

def home(request):
    return render(request, 'seminar/home.html')

def add(request):
    return render(request, 'seminar/add.html')

def style_transfer(request):
    return render(request, 'seminar/style_transfer.html')

def manifest(request):
    return render(request, 'seminar/manifest.json')
