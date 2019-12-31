from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

cursor = connection.cursor()

@csrf_exempt # post로 값을 전달받는 곳은 필수
def join1(request):
    if request.method == 'GET':
        return render(request, 'member/join1.html')

def list(request):
    # ID 기준으로 오름차순
    sql = "SELECT * FROM MEMBER ORDER BY ID ASC"
    cursor.execute(sql) # SQL문 실행
    data = cursor.fetchall() # 결과값을 가져옴
    print(type(data)) # list
    print(data) # [ (1,2,3,4,5), ( ), ( )]

    #list.html을 표시하기 이전에 list변수에 data 값을, title변수에 "회원목록" 문자를
    return render(request, 'member/list.html',
        {"list":data, "title":"회원목록"})

def index(request):
    # return HttpResponse("index n page <hr />")
    return render(request, 'member/index.html')

@csrf_exempt
def login(request):
    if request.method == 'GET':
        return render(request, 'member/login.html')
    elif request.method == 'POST':
        idnum = request.POST['id']
        passw = request.POST['pw']
        ar2 = [idnum, passw] # 리스트로 만듦
        print(ar2)
        # DB에 추가함
        # 크롬에서 127.0.0.1:8000/member/index
        return redirect('/member/index')

@csrf_exempt # post로 값을 전달받는 곳은 필수로 해야함
def join(request):
    if request.method == 'GET':
        return render(request, 'member/join.html')
    elif request.method == 'POST':
        id = request.POST['id']
        na = request.POST['name']
        ag = request.POST['age']
        pw = request.POST['pw']

        ar = [id,na,ag,pw] # list로 만듦
        print(ar)
        # DB에 추가함

        sql = """
            INSERT INTO MEMBER(ID,NAME,AGE,PW,JOINDATE)
            VALUES (%s, %s, %s, %s, SYSDATE)
            """
        cursor.execute(sql,ar)

        # 크롬에서 127.0.0.1:8000/member/index
        return redirect('/member/index')