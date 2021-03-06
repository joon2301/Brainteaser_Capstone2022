import numpy as np
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Community,Board,BoardContents,FinalComment, Comment
from .forms import commentForm, commentChildForm
from django.core.paginator import Paginator

import datetime

from django.db.models import Max
from sentence_transformers import util

# Create your views here.


# 게시글 리스트 보기
def list(request,t):
    boards = Board.objects
    category = {'case':'category4','free':'category5'}
    print(category[t])
    boardList = Community.objects.filter(Category=category[t]).order_by('-Date')
    paginator = Paginator(boardList, '5')
    page = request.GET.get('page', 1)
    posts = paginator.page(page)
    print(boardList.values())
    return render(request, 'list2.html', {
        "posts": posts
    })


# 게시글 보기
def view(request, t, p):
    # 게시글 내용 가져오기
    boardContents = BoardContents.objects.get(PostID=p)
    contents = str(boardContents).split(',')
    # 게시글 댓글 가져오기
    try:
        comments = FinalComment.objects.filter(PostID=p).order_by('-Likes')
    except:
        print('댓글이 없는데요?')
        comments = None
    # 조회수 +1
    clickedUp(contents, p)

    return render(request, 'view2.html', {
        "boardContents": boardContents,
        'teaserAns': comments,
        'answerForm': commentForm,
        'answerChildForm': commentChildForm,
    })


def childAns(request,t,p,c):
    print('child:',c)
    if request.method == 'POST':
        form = commentChildForm(request.POST)
        userAns = request.POST.get('Comment')
    print(userAns)
    addComment(request.session.get('username'), p, userAns, c)
    return redirect(reverse('view2',args=[t,p]))


def parentAns(request,t,p):
    print('parent')
    userAns = request.POST.get('Comment')
    print(userAns)
    addComment(request.session.get('username'), p, userAns, 0)
    return redirect(reverse('view2',args=[t,p]))


def edit(request, t, p):
        board_Contents = BoardContents.objects.get(PostID=p)
        if request.method == "POST":
            board_Contents.Title = request.POST['title']
            board_Contents.Contents = request.POST['text']
            board_Contents.save()
            return redirect('/community/'+t+'/post=' + str(p))

        else:
            return render(request, 'edit2.html', {'bdc': board_Contents, 'category':t})

# 삭제
def delete(request,t,p):
    print('post:', p)
    with connection.cursor() as cursor:
        try:
            cursor.execute("delete from Comment_User_Likes where CommentID in (select CommentID from comment where PostID = %d);" % p)
            cursor.execute("delete from comment where PostID = %d;" % p)
            cursor.execute("delete from community where PostID = %d;" % p)
        except:
            print('error')
    return redirect('list',t)


def write(request,t):
    category = {'case':'category4','free':'category5'}
    key = Board.objects.aggregate(PostID =Max('PostID'))
    if key['PostID'] == None:
        key['PostID'] = int(0)
    print(key['PostID'])
    if request.method == 'POST':
        board_Contents = Board()

        board_Contents.PostID = key['PostID'] + 1
        board_Contents.Title = request.POST['title']
        board_Contents.Category = category[t]
        board_Contents.Contents = request.POST.get('text1', True)
        board_Contents.AccID = request.session.get('username')
        board_Contents.Date = datetime.datetime.now()
        board_Contents.Clicked = int(0)
        board_Contents.save()
        return redirect('/community/' + t + '/')
    else:
        return render(request, 'write2.html', {'category': t})


def titleTest(request, t, test):
    result = titleSearch(test)
    print(result)
    return render(request, 'titleTest2.html', {'contents': result})


#이름 검색 (검색 할거면 주석 제거)
def titleSearch(input):
    from .apps import CommunityConfig
    from .models import Question
    # 변수 설정
    corpusLabel = []
    corpus = []
    top_k = 3
    teaserObjects = Board.objects.all().values()
    QuesObjects = Question.objects.all().values()
    for i in [teaserObjects,QuesObjects]:
        for j in i:
            corpusLabel.append([j['Title'],j['Category']])
            corpus.append(j['Title'])

    # KoBert 모델을 사용하여 문장 수치화
    queryEmbedding = CommunityConfig.embedder.encode(input, convert_to_tensor=True)
    corpusEmbeddings = CommunityConfig.embedder.encode(corpus, convert_to_tensor=True)

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
            cursor.execute("update community set Clicked = %d where PostID = %d" % (clicked, p))
        except:
            print('error')


# 댓글 추가
def addComment(AccID, TeaserID, Answer, PID):
    with connection.cursor() as cursor:
        cursor.execute("select MAX(CommentID) from comment")
        CommentID = cursor.fetchall()[0][0]
        if CommentID == None:
            CommentID = 0
        CommentID += 1
        now = datetime.datetime.now()
        try:
            cursor.execute('insert into comment values(%d,"%s",%d,"%s","%s", "%d")' % (
            CommentID, AccID, TeaserID, Answer, now.strftime('%Y-%m-%d %H:%M:%S'), PID ))

        except:
            print('error')

# 댓글 제거
def delComment(request, t, p, c):
    print('post:', p, 'commentID:', c)
    with connection.cursor() as cursor:
        try:
            cursor.execute("delete from comment where PostID = %d AND ParentID = %d;" % (p, c))
            cursor.execute("delete from Comment_User_Likes where CommentID = %d;" % (c))
            cursor.execute("delete from comment where PostID = %d AND CommentID = %d;"%(p,c))
        except:
            print('error')
    return redirect('view2',t,p)

# 댓글 수정
def editComment(request,t,p,c):
    print('post:', p, 'commentID:', c)
    try:
        comments = Comment.objects.filter(PostID=p,CommentID=c)
    except:
        print('댓글이 없는데요?')
    if request.method == 'POST':
        updateComment = request.POST['comment']
        print(updateComment)
        with connection.cursor() as cursor:
            try:
                cursor.execute("update comment set comment='%s' where PostID = %d AND CommentID = %d;"%(updateComment,p,c))
                return HttpResponse('<script>window.close()</script>')
            except:
                print('error')
    return render(request, 'comEdit2.html',{
        'ans':comments[0],
    })

# 댓글 좋아요
def likeComment(request,t,p,c):
    username = request.session.get('username')
    print(request.session.get('username'),c)
    with connection.cursor() as cursor:
        try:
            cursor.execute("select * from Comment_User_Likes where CommentID=%d AND AccID='%s';"%(c,username))
            temp = cursor.fetchall()
            print(len(temp))
            if len(temp) > 0:
                cursor.execute("delete from Comment_User_Likes where CommentID=%d AND AccID='%s';" % (c, username))
            else:
                cursor.execute("insert into Comment_User_Likes values('%s',%d)"%(username,c))
        except:
            print('error')

    return redirect('view2',t,p)


#댓글 유사도 페이즈
def simAnswer(request,t,p,c):
    print(c)
    try:
        sim = []
        unsim = []
        answers = FinalComment.objects.filter(CommentID=c,ParentID=0).values('Comment')[0]
        simTmp,unsimTmp = commentSearch(answers['Comment'], p)
        for i in simTmp:
            sim.append(FinalComment.objects.filter(Comment=i).values('AccID','Comment')[0])
        for i in unsimTmp:
            unsim.append(FinalComment.objects.filter(Comment=i).values('AccID','Comment')[0])
    except:
        print('error')

    return render(request, 'simAns2.html' , {
        'sim':sim,
        'unsim':unsim
    })


#댓글 유사도
def commentSearch(input,p):
    from .apps import CommunityConfig
    from .models import FinalComment
    # 변수 설정
    corpus = []
    top_k = 2
    comObjects = FinalComment.objects.filter(PostID=p,ParentID=0).exclude(Comment=input).values('CommentID','Comment')
    for i in comObjects:
        corpus.append(i['Comment'])
    # KoBert 모델을 사용하여 문장 수치화
    queryEmbedding = CommunityConfig.embedder.encode(input, convert_to_tensor=True)
    corpusEmbeddings = CommunityConfig.embedder.encode(corpus, convert_to_tensor=True)
    # 코사인 유사도 검사
    cos_scores = util.pytorch_cos_sim(queryEmbedding, corpusEmbeddings)[0]
    cos_scores = cos_scores.cpu()
    # score 높은 순으로 정렬
    top_results = np.argpartition(-cos_scores, range(len(corpus)))[0:len(corpus)]
    simResult = []
    unsimResult = []
    print('=========')
    print(corpus)
    print(cos_scores)
    print(top_results)
    print('=========')
    # 전달용 배열 생성
    if len(corpus)<top_k:
        top_k = len(corpus)
    for idx in top_results[1:top_k+1]:
        simResult.append(corpus[idx])
    for idx in top_results[len(corpus)-top_k:len(corpus)]:
        unsimResult.append(corpus[idx])
    print(simResult)
    print(unsimResult)
    return simResult, unsimResult