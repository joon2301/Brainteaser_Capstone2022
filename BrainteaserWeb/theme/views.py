from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def list(request):
    return render(request, 'list.html')

def write(request):
    return render(request, 'write.html')

def view(request):
    return render(request, 'view.html')