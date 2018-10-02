from django.shortcuts import render
from django.http.response import HttpResponse
# import for file upload
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOADE_DIR = os.path.join(BASE_DIR, 'static/seminar/uploaded')

# Create your views here.
def index(request):
    return render(request, 'index.html')
