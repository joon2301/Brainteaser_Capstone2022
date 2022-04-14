from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    return render(request, 'homeindex.html')

def index2(request):
    return render(request, 'index.html')

def logout(request):
    print(request.session.get('username'), "로그아웃")
    request.session.flush()
    return redirect('/')