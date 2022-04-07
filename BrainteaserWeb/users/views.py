from django.shortcuts import render, redirect
from django.db import connection


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
            print(request.session.get('username'),"성공")
            return redirect('index')
        else:
            return render(request, "users/main.html")


def login(username, password):
    cur = connection.cursor()
    sql = "select Password from users where AccID =%s AND Password = %s"

    cur.execute(sql, (username, password))
    users = cur.fetchall()
    if len(users) == 1:
        # 성공
        return True
    else:
        # 실패
        print("실패")
        return False


def save_session(request, username, password):
    request.session['username'] = username
    request.session['password'] = password
