from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    return render(request, 'index.html')

def list(request):
    return render(request, 'list.html')

def write(request):
    return render(request, 'write.html')

def view(request):
    return render(request, 'view.html')

def logout(request):
    print(request.session.get('username'), "로그아웃")
    request.session.flush()
    return redirect('/')

