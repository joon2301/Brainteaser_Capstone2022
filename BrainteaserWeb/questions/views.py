from django.db import connection
from django.shortcuts import render
from .models import Board, BoardContents, TeaserAnswer
from django.core.paginator import Paginator
from .forms import answerForm
import datetime


# Create your views here.

# 게시글 리스트 보기
def list(request):
    boards = Board.objects
    boardList = Board.objects.filter(Category='Category1')
    paginator = Paginator(boardList, '5')
    page = request.GET.get('page', 1)
    posts = paginator.page(page)
    return render(request, 'list.html', {
        "boards": boards,
        "posts": posts
    })


def write(request):
    return render(request, 'write.html')


# 게시글 보기
def view(request, p):
    # 게시글 내용 가져오기
    boardContents = BoardContents.objects.get(TeaserID=p)
    contents = str(boardContents).split(',')
    # 게시글 댓글 가져오기
    try:
        answers = TeaserAnswer.objects.filter(TeaserID=p)
    except:
        print(' 댓글이 없는데요?')
        answers = None
    # 조회수 +1
    clickedUp(contents, p)
    # 댓글 달기
    if request.method == 'POST':
        comment = answerForm(request.POST)
        if comment.is_valid():
            userAns = comment.cleaned_data['Answer']
            addComment(request.session.get('username'), p, userAns)

    return render(request, 'view.html', {
        "boardContents": contents,
        'teaserAns': answers,
        'answerForm': answerForm,
    })


# 조회수 +1
def clickedUp(contents, p):
    with connection.cursor() as cursor:
        clicked = int(contents[4]) + 1
        cursor.execute("update brainTeaser set Clicked = %d where teaserID = %d" % (clicked, p))


def addComment(AccID, TeaserID, Answer):
    with connection.cursor() as cursor:
        cursor.execute("select MAX(AnswerID) from teaserAnswer")
        AnwerID = cursor.fetchall()[0][0] + 1
        now = datetime.datetime.now()
        try:
            cursor.execute('insert into teaserAnswer values(%d,"%s",%d,"%s","%s")' % (
            AnwerID, AccID, TeaserID, Answer, now.strftime('%Y-%m-%d %H:%M:%S') ))
        except:
            print('error')


def edit(request, p):
    print(p)
    return render(request, 'edit.html')
