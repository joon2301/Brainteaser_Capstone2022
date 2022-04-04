from audioop import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
import pymysql
# Create your views here.
def main(request):
    if request.method == 'GET':
        return render(request, "users/main.html")
    
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #이거 if문에 True/False 박고 해주세요! 디비는 저한테만 있어서..
        if login(username,password):
            #이거 도와주세요!! 페이지 이동 실패만 자꾸 뜨네요
            return render(request, 'index.html')
        else:
            return render(request, "users/main.html")

    # if user is not None:
    #     login(request, user)
    #     #
    #     return render(request, )
    #
    # else:
    #     return render(request, 'users/main.html')

def login(username,password):
    conn = pymysql.connect(host='localhost', user='root2',password='1q2w3e4r!',db='mydb',charset='utf8')
    cur = conn.cursor()
    sql = "select Password from users where AccID =%s AND Password = %s"

    cur.execute(sql,(username,password))
    users = cur.fetchall()
    conn.close()
    if len(users) == 1:
        #성공
        print("성공")
        return True
    else:
        #실패
        print("실패")
        return False
