from audioop import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
import pymysql


# Create your views here.
def main(request):
    if request.method == 'GET':
        print(request.session.get('username'))
        if request.session.get('username') == None:
            return render(request, "users/main.html")
        else:
            return redirect('index')

    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if login(username, password):
            save_session(request, username, password)
            return redirect('index')
        else:
            return render(request, "users/main.html")


def login(username, password):
    conn = pymysql.connect(host='34.146.163.3', user='root', password='1q2w3e4r!', db='mydb', charset='utf8')
    cur = conn.cursor()
    sql = "select Password from users where AccID =%s AND Password = %s"

    cur.execute(sql, (username, password))
    users = cur.fetchall()
    conn.close()
    if len(users) == 1:
        # 성공
        print("성공")

        return True
    else:
        # 실패
        print("실패")
        return False


def save_session(request, username, password):
    request.session['username'] = username
    request.session['password'] = password
