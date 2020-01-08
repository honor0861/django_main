from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.conf.locale import ar

cursor = connection.cursor()

# django에서 제공하는 User 모델
from django.contrib.auth.models import User
from django.contrib.auth import login as login1
from django.contrib.auth import logout as logout1
from django.contrib.auth import authenticate as auth1

from .models import Table2 # 실습과제
from django.db.models import Sum, Max, Min, Count, Avg

def js_chart(request):
    str =[100, 200,300,400 , 500, 600]
    return render(request, 'member/js_chart.html')

def js_index(request):
    return render(request, 'member/js_index.html')

def exam_select(request):
    txt = request.GET.get("txt","")
    page = int(request.GET.get("page",1)) # 페이지가 안 들어오면 1페이지가 표시되도록 함
    
    if txt == "": # 검색어가 없는 경우 전체 출력
        # page nummber 1 => 0, 10
        # page nummber 2 => 11, 20
        # page nummber 3 => 21, 30
        
        # SELECT * FROM MEMBER_TABLE2
        list = Table2.objects.all()[(page*10)-10:page*10]

        # SELECT COUNT(*) FROM MEMBER_TABLE2
        cnt  = Table2.objects.all().count()
        tot = (cnt-1)//10 + 1
        # 10 => 1
        # 13 => 2
        # 20 => 2
        # 31 => 4
    else:
        # SELECT * FROM MT2 WHERE name LIKE '%가%'
        list = Table2.objects.filter(name__contains=txt)[page*10-10:page*10]

        # SELECT COUNT(*) FROM MT2 WHERE name LIKE '%가%'
        cnt = Table2.objects.filter(name__contains=txt).count()
        tot = (cnt-1)//10 +1

    return render(request, 'member/exam_select.html',{"list":list, "pages":range(1,tot+1,1)})

    """
    sum = Table2.objects.raw("SELECT  1 as no, SUM(math) smath FROM MEMBER_TABLE2")
    print(type(sum))
    print(sum.columns)
    print(sum[0].smath)
    
    # SELECT SUM(math) FROM MEMBER_TABLE2 WHERE CLASS_ROOM=101
    list = Table2.objects.aggregate(Sum('math'))

    # SELECT NO, NAME FROM MEMBER_TABLE2
    list = Table2.objects.all().values('no','name')

    # SELECT * FROM MEMBER_TABLE2 ORDER BY name ASC
    list = Table2.objects.all().order_by('name')
    #list = Table2.objects.raw("SELECT * FROM MEMBER_TABLE2 ORDER BY name ASC")

    # 반별 국어, 영어, 수학 합계
    # SELECT SUM(kor) AS kor, SUM(eng) AS eng, SUM(math) AS math FROM MEMBER_TABLE2 GROUP BY CLASSROOM
    list = Table2.objects.values('classroom').annotate(kor=Sum('kor'),eng=Sum('eng'),math=Sum('math'))   
    
    return render(request, 'member/exam_select.html',{"list":list}) 
    """
    
@csrf_exempt
def exam_list(request):
    if request.method == 'GET':
        rows = Table2.objects.all()
        print(rows)
        return render(request, 'member/exam_list.html', {"list":rows})

@csrf_exempt
def exam_insert(request):
    if request.method == 'GET':
        return render(request, 'member/exam_insert.html',{"cnt":range(5)})
    elif request.method == 'POST':
        na = request.POST.getlist('name')
        ko = request.POST.getlist('kor')
        en = request.POST.getlist('eng')
        ma = request.POST.getlist('math')
        cl = request.POST.getlist('classroom')

        objs = []

        for i in range(0, len(na)):
            obj=Table2()
            obj.name=na[i]
            obj.kor=ko[i]
            obj.eng=en[i]
            obj.math=ma[i]
            objs.append(obj)

        Table2.objects.bulk_create(objs)
        return redirect("/member/exam_list")


###############################################################################

@csrf_exempt
def auth_join(request):
    if request.method == 'GET':
        return render(request, 'member/auth_join.html')
    elif request.method == "POST":
        id = request.POST['username']
        pw = request.POST['password']
        na = request.POST['first_name']
        em = request.POST['email']

        # 회원가입
        obj = User.objects.create_user(             # create_user가 함수명
            username=id,
            password=pw,
            first_name=na,
            email=em
        )
        obj.save()

        return redirect("/member/auth_index")

def auth_index(request):
    if request.method == 'GET':
        return render(request, 'member/auth_index.html')

@csrf_exempt
def auth_login(request):
    if request.method == 'GET':
        return render(request, 'member/auth_login.html')
    elif request.method == 'POST':
        id = request.POST['username']
        pw = request.POST['password']

        obj = auth1(request, username=id, password=pw) # DB에 인증

        if obj is not None:
            login1(request, obj)                       # 세션에 추가
            return redirect("/member/auth_index")                     
        return redirect('/member/auth_login')

@csrf_exempt
def auth_logout(request):
    if request.method=='GET' or request.method=='POST':
        logout1(request) # 세션 초기화
        return redirect("/member/auth_index")

def auth_edit(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect("/member/auth_login")

        obj = User.objects.get(username=request.user)
        return render(request, 'member/auth_edit.html',{"obj":obj})
    elif request.method == 'POST':
        id = request.POST['username']
        na = request.POST['first_name']
        em = request.POST['email']

        obj=User.objects.get(username=id)
        obj.first_name=na
        obj.email=em
        obj.save()
        return redirect("/member/auth_index")

def auth_pw(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect("/member/auth_login")

        return render(request, 'member/auth_pw.html')
    elif request.method == 'POST':
        pw = request.POST['pw']                         # 기존 암호
        pw1 = request.POST['pw1']                        # 바꿀 암호
        # 바꾸기 전에 인증
        obj = auth1(request, username=request.user, password=pw)
        if obj:
            obj.set_password(pw1)                       # pw1으로 암호 변경
            obj.save()
            return redirect("/member/auth_index")
        
        return redirect("/member/auth_pw")

#####################################################################

@csrf_exempt # post로 값을 전달받는 곳은 필수로 해야함
def delete(request):
    if request.method == 'GET' or request.method == 'POST':
        ar = [request.session['userid']]
        sql = "DELETE FROM MEMBER WHERE ID=%s"
        cursor.execute(sql, ar)
        return redirect("/member/logout")

@csrf_exempt
def edit(request) :
    if request.method =='GET':
        ar = [request.session['userid']]
        sql = "SELECT * FROM MEMBER WHERE ID=%s"
        cursor.execute(sql, ar) # sql문 실행
        data = cursor.fetchone() # 일치하는 단일 행을 꺼냄
        print(data)
        return render(request, 'member/edit.html', {"one":data})
    elif request.method == 'POST':
        ar = [request.POST['name'], request.POST['age'], request.POST['id']]
        sql = "UPDATE MEMBER SET NAME = %s, AGE = %s WHERE ID = %s"
        cursor.execute(sql, ar)
        return redirect("/member/index")

@csrf_exempt # post로 값을 전달받는 곳은 필수
def join1(request):
    if request.method == 'GET':
        return render(request, 'member/join1.html')

def list(request):
    sql = "SELECT * FROM MEMBER ORDER BY ID ASC"  # ID 기준으로 오름차순
    cursor.execute(sql)                           # SQL문 실행
    data = cursor.fetchall()       # 일치하는 행의 리스트 결과값을 가져옴
    print(type(data)) # list
    print(data)                    # [ (1,2,3,4,5), ( ), ( )]
    #list.html을 표시하기 이전에 list 변수에 data 값을, title 변수에 "회원목록" 문자를
    return render(request, 'member/list.html', {"list":data, "title":"회원목록"})

def index(request):
    # return HttpResponse("index n page <hr />")
    return render(request, 'member/index.html')

@csrf_exempt
def login(request):
    if request.method == 'GET':
        return render(request, 'member/login.html')
    elif request.method == 'POST':
        ar = [request.POST['id'], request.POST['pw']]    # 리스트로 만듦
        sql = "SELECT ID, NAME FROM MEMBER WHERE ID=%s AND PW=%s"
        cursor.execute(sql, ar)
        data=cursor.fetchone()                           # 한 줄 가져오기
        print(type(data))
        print(data)                                           # ('a','b')
        if data:
            request.session['userid'] = data[0]
            request.session['username'] = data[1]
            return redirect('/member/index')
        return redirect('/member/login')

@csrf_exempt
def logout(request):
    if request.method=='GET' or request.method=='POST':
        del request.session['userid']
        del request.session['username']
        return redirect('/member/index')

@csrf_exempt 
def join(request):
    if request.method == 'GET':
        return render(request, 'member/join.html')
    elif request.method == 'POST':
        id = request.POST['id']
        na = request.POST['name']
        ag = request.POST['age']
        pw = request.POST['pw']

        ar = [id,na,ag,pw]     # list로 만듦
        print(ar)              # DB에 추가함
        sql = "INSERT INTO MEMBER(ID,NAME,AGE,PW,JOINDATE) VALUES (%s, %s, %s, %s, SYSDATE)"
        cursor.execute(sql,ar) # 크롬에서 127.0.0.1:8000/member/index
        return redirect('/member/index')