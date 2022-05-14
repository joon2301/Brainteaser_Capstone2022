from sentence_transformers import SentenceTransformer, util
import numpy as np
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .apps import HomepageConfig
from .models import Board,Community


# Create your views here.
def index(request):
    return render(request, 'homeindex.html')

def index2(request):
    return render(request, 'index.html')

def logout(request):
    print(request.session.get('username'), "로그아웃")
    request.session.flush()
    return redirect('/')

def search(request,input):
    # 혹시나 본문 검색을 대비해서 만들어둔 함수형 검색
    searchResult = titleSearch(input)
    print(searchResult)
    # 검색 결과로 나오는 데이터 추출
    showResult = []
    for title,category in searchResult:
        if category == 'category1' or category == 'category2' or category == 'category3':
            showResult.append(Board.objects.filter(Title = title).values()[0])
        else:
            showResult.append(Community.objects.filter(Title = title).values()[0])
    print(showResult)
    # HTML 출력을 위한 변수들 지정, 게시판 형식으로 위한 페이징 설정
    boardList = showResult
    paginator = Paginator(boardList, '5')
    page = request.GET.get('page', 1)
    posts = paginator.page(page)
    return render(request, 'searchlist.html', {
        "posts": posts
    })


#이름 검색 (검색 할거면 주석 제거)
def titleSearch(input):
    # 변수 설정
    corpusLabel = []
    corpus = []
    top_k = 0
    teaserObjects = Board.objects.all().values()
    commObjects = Community.objects.all().values()
    for i in [teaserObjects,commObjects]:
        for j in i:
            corpusLabel.append([j['Title'],j['Category']])
            corpus.append(j['Title'])

    # KoBert 모델을 사용하여 문장 수치화
    queryEmbedding = HomepageConfig.embedder.encode(input, convert_to_tensor=True)
    corpusEmbeddings = HomepageConfig.embedder.encode(corpus, convert_to_tensor=True)

    # 코사인 유사도 검사
    cos_scores = util.pytorch_cos_sim(queryEmbedding, corpusEmbeddings)[0]
    cos_scores = cos_scores.cpu()
    # 아래 숫자 수정해서 거르기
    for i in cos_scores:
        if i > 0.32:
            top_k += 1
    # score 높은 순으로 정렬
    top_results = np.argpartition(-cos_scores, range(top_k))[0:top_k]
    searchResult = []
    # 전달용 배열 생성
    for idx in top_results[0:top_k]:
        searchResult.append([corpus[idx].strip(),corpusLabel[idx][1]])
    return searchResult
