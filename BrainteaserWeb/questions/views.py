import numpy as np
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Board, BoardContents, TeaserAnswer, FinalAnswer
from django.core.paginator import Paginator
from .forms import answerForm
import datetime

from django.db.models import Max
from sentence_transformers import util

# Create your views here.


# 게시글 리스트 보기
def list(request,t):
    boards = Board.objects
    category = {'it':'category1','economics':'category2','casual':'category3'}
    print(category[t])
    boardList = Board.objects.filter(Category=category[t]).order_by('-Date')
    paginator = Paginator(boardList, '5')
    page = request.GET.get('page', 1)
    posts = paginator.page(page)
    return render(request, 'list.html', {
        "boards": boards,
        "posts": posts
    })


# 게시글 보기
def view(request, t, p):
    # 게시글 내용 가져오기
    boardContents = BoardContents.objects.get(TeaserID=p)
    contents = str(boardContents).split(',')
    # 게시글 댓글 가져오기
    try:
        answers = FinalAnswer.objects.filter(TeaserID=p).order_by('-Likes')
    except:
        print('댓글이 없는데요?')
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


def edit(request, t, p):
        print(p)
        board_Contents = BoardContents.objects.get(TeaserID=p)

        if request.method == "POST":
            board_Contents.Title = request.POST['title']
            board_Contents.Teaser = request.POST['text']
            board_Contents.save()
            return redirect('/questions/'+t+'/post=' + str(p))

        else:
            return render(request, 'edit.html', {'bdc': board_Contents, 'category':t})

# 삭제
def delete(request,t,p):
    print('post:', p)
    with connection.cursor() as cursor:
        try:
            cursor.execute("delete from Answer_User_Likes where AnswerID in (select AnswerID from teaserAnswer where TeaserID = %d);" % p)
            cursor.execute("delete from teaserAnswer where TeaserID = %d;" % p)
            cursor.execute("delete from brainTeaser where TeaserID = %d;" % p)
        except:
            print('error')
    return list(request,t)


def write(request,t):
    category = {'it': 'category1', 'economics': 'category2', 'casual': 'category3'}
    key = Board.objects.aggregate(TeaserID =Max('TeaserID'))
    print(key['TeaserID'])
    if request.method == 'POST':
        board_Contents = Board()
        board_Contents.TeaserID = key['TeaserID'] + 1
        board_Contents.Title = request.POST['title']
        board_Contents.Category = category[t]
        board_Contents.Teaser = request.POST.get('text1', True)
        board_Contents.AccID = request.session.get('username')
        board_Contents.Date = datetime.datetime.now()
        board_Contents.Clicked = int(0)
        board_Contents.save()
        return redirect('/questions/' + t + '/')
    else:
        return render(request, 'write.html', {'category': t})


def titleTest(request, t, test):
    result = titleSearch(test)
    print(result)
    return render(request, 'titleTest.html', {'contents': result})


#이름 검색 (검색 할거면 주석 제거)
def titleSearch(input):
    from .apps import ThemeConfig
    from .models import Community
    # 변수 설정
    corpusLabel = []
    corpus = []
    top_k = 3
    teaserObjects = Board.objects.all().values()
    commObjects = Community.objects.all().values()
    for i in [teaserObjects,commObjects]:
        for j in i:
            corpusLabel.append([j['Title'],j['Category']])
            corpus.append(j['Title'])

    # KoBert 모델을 사용하여 문장 수치화
    queryEmbedding = ThemeConfig.embedder.encode(input, convert_to_tensor=True)
    corpusEmbeddings = ThemeConfig.embedder.encode(corpus, convert_to_tensor=True)

    # 코사인 유사도 검사
    cos_scores = util.pytorch_cos_sim(queryEmbedding, corpusEmbeddings)[0]
    cos_scores = cos_scores.cpu()
    # score 높은 순으로 정렬
    top_results = np.argpartition(-cos_scores, range(top_k))[0:top_k]
    searchResult = []
    # 전달용 배열 생성
    for idx in top_results[0:top_k]:
        searchResult.append([corpus[idx].strip(),corpusLabel[idx][1]])
    return searchResult


# 조회수 +1
def clickedUp(contents, p):
    with connection.cursor() as cursor:
        clicked = int(contents[4]) + 1
        try:
            cursor.execute("update brainTeaser set Clicked = %d where teaserID = %d" % (clicked, p))
        except:
            print('error')
            print(1)


# 댓글 추가
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

# 댓글 제거
def delComment(request, t, p, c):
    print('post:', p, 'answerID:', c)
    with connection.cursor() as cursor:
        try:
            cursor.execute("delete from teaserAnswer where TeaserID = %d AND AnswerID = %d;"%(p,c))
        except:
            print('error')
    return view(request,p)

# 댓글 수정
def editComment(request,t,p,c):
    print('post:', p, 'answerID:', c)
    try:
        answers = TeaserAnswer.objects.filter(TeaserID=p,AnswerID=c)
    except:
        print('댓글이 없는데요?')
        answers = None
    if request.method == 'POST':
        updateAnswer = request.POST['comment']
        print(updateAnswer)
        with connection.cursor() as cursor:
            try:
                cursor.execute("update teaserAnswer set Answer='%s' where TeaserID = %d AND AnswerID = %d;"%(updateAnswer,p,c))
                return HttpResponse('<script>window.close()</script>')
            except:
                print('error')
    return render(request, 'comEdit.html',{
        'ans':answers[0],
    })

# 댓글 좋아요
def likeAnswer(request,t,p,c):
    username = request.session.get('username')
    print(request.session.get('username'),c)
    with connection.cursor() as cursor:
        try:
            cursor.execute("select * from Answer_User_Likes where AnswerID=%d AND AccID='%s';"%(c,username))
            temp = cursor.fetchall()
            print(len(temp))
            if len(temp)>0:
                cursor.execute("delete from Answer_User_Likes where AnswerID=%d AND AccID='%s';" % (c, username))
            else:
                cursor.execute("insert into Answer_User_Likes values('%s',%d)"%(username,c))
        except:
            print('error')

    return redirect('view',t,p)
