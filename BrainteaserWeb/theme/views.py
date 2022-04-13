from django.shortcuts import render, redirect
from .models import Board,BoardContents
from django.core.paginator import Paginator
# Create your views here.
def index(request):
    return render(request, 'index.html')

def list(request,idx = 0):
    # IT 게시판
    if idx != 0 :
        idx = idx
    boards = Board.objects.filter(Category='Category1')
    boardList = []
    for i in boards:
        boardList.append(str(i).split(','))

    print(len(boards))
    return render(request, 'list.html',{"boards":boardList,'index':idx})

def list2(request):
    boards = Board.objects
    boardList = Board.objects.filter(Category='Category1')
    paginator = Paginator(boardList,'5')
    page = request.GET.get('page',1)
    posts = paginator.page(page)
    return render(request, 'list.html',{"boards":boards,"posts":posts})

def write(request):
    return render(request, 'write.html')

def view(request):
    # TeaserID가 자동적으로 수정되면서 다수의 URL을 사용할 수 있도록 해야함.
    boardContents = BoardContents.objects.get(TeaserID = 1)
    contents = str(boardContents).split(',')
    print(contents)
    return render(request, 'view.html', {"boardContents":contents})

def logout(request):
    print(request.session.get('username'), "로그아웃")
    request.session.flush()
    return redirect('/')

def next(request):

    return list(request,1)



