# pyrefly: ignore [missing-import]
from django.shortcuts import render

# Create your views here.
def home(req):
    return render(req, 'home.html')

def about(req, data):
    return render(req, 'about.html', {'data': data})