from django.shortcuts import render, redirect
from .models import ITBoard

# Create your views here.
def index(request):
    return render(request, 'index.html')

def list(request):
    boards = ITBoard.objects.all()
    return render(request, 'list.html',{"boards":boards})

def write(request):
    return render(request, 'write.html')

def view(request):
    return render(request, 'view.html')

def logout(request):
    print(request.session.get('username'), "로그아웃")
    request.session.flush()
    return redirect('/')

