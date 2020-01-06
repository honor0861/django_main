# 파일명 : board/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from base64 import b64encode # byte배열을 base64(이미지를 출력해줄 수 있는 포맷)로 변경함
import pandas as pd
cursor = connection.cursor() # sql문 수행을 하기 위한 cursor 객체

##########################################################################################
from .models import Table2   # models.py 파일의 Table2 클래스

# setting.py
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # 디렉토리 이름 추출

@csrf_exempt
def t2_update_all(request):
    if request.method == 'GET':
        n = request.session['no'] # 8, 5, 3
        print(n)
        # SELECT * FROM BOARD_TABLE2 WHERE NO=8 or NO=5 or NO=3
        # SELECT * FROM BOARD_TABLE2 WHERE NO IN (8,5,3)
        rows = Table2.objects.filter(no__in=n)
        return render(request, 'board/t2_update_all.html',{"list":rows})
    elif request.method == 'POST':  # 체크박스 클릭하고 나서 수정을 누르면 POST를 먼저 실행- > GET으로 -> POST 실행
        menu = request.POST['menu']
        print(menu)
        if menu == '1':
            no=request.POST.getlist("chk[]")
            request.session['no'] = no
            print(no)
            return redirect("/board/t2_update_all")
        elif menu == '2':
            no=request.POST.getlist("no[]")
            name=request.POST.getlist("name[]")
            kor=request.POST.getlist("kor[]")
            eng=request.POST.getlist("eng[]")
            math=request.POST.getlist("math[]")
            objs = []
            for i in range(0, len(no),1):
                obj = Table2.objects.get(no=no[i])
                obj.name = name[i]
                obj.kor = kor[i]
                obj.eng = eng[i]
                obj.math = math[i]
                objs.append(obj)
            Table2.objects.bulk_update(objs, ["name","kor","eng","math"])
            return redirect("/board/t2_list")

def t2_insert_all(request):
    if request.method =='GET':
        return render(request, 'board/t2_insert_all.html',{"cnt":range(5)})
    elif request.method == 'POST':
        na = request.POST.getlist('name[]')
        ko = request.POST.getlist('kor[]')
        en = request.POST.getlist('eng[]')
        ma = request.POST.getlist('math[]')
        
        """
        하나 할 때는 가능하나 동시에 수행할 때는 이렇게 쓰면 안됨
        반복문 수행하다가 중간에 끊기면 다 날아감
        """

        objs = []

        for i in range(0, len(na),1):
            obj = Table2()
            obj.name = na[i]
            obj.kor = ko[i]
            obj.eng = en[i]
            obj.math = ma[i]
            objs.append(obj)

        # 일괄 추가
        Table2.objects.bulk_create(objs)
        return redirect("/board/t2_list")

@csrf_exempt
def t2_update(request):
    if request.method == 'GET':
        n = request.GET.get("no",0)
        # SELECT * FROM BOARD_TABLE2 WHERE NO=%s
        row = Table2.objects.get(no=n)
        return render(request,'board/t2_update.html',{"one":row})
    elif request.method == 'POST':
        n = request.POST['no']
        obj = Table2.objects.get(no=n) # obj 객체 생성
        obj.name = request.POST['name']  # 변수에 값
        obj.kor  = request.POST['kor']
        obj.eng  = request.POST['eng']
        obj.math = request.POST['math']
        obj.save()
        # UPDATE BOARD_TABLE2 SET
        # NAME=%s, KOR=%s, ENG=%s, MATH=%s
        # WHERE NO=%s
        return redirect("/board/t2_list")

@csrf_exempt
def t2_delete(request):
    if request.method == 'GET':
        n = request.GET.get("no",0)

        # SELECT * FROM BOARD_TABLE2 WHERE NO = %s
        row = Table2.objects.get(no=n)

        # DELETE FROM BOARD_TABLE2 WHERE NO=%s
        row.delete() # 삭제

        return redirect("/board/t2_list")

@csrf_exempt
def t2_list(request):
    if request.method == 'GET':
        rows = Table2.objects.all()                                 # SQL : SELECT * FROM BOARD_TABLE2
        print(rows)                                                 # 결과 확인
        print(type(rows))                                           # 타입 확인
        return render(request, 'board/t2_list.html', {"list":rows}) # html 표시

@csrf_exempt
def t2_insert(request):
    if request.method == 'GET':
        return render(request, 'board/t2_insert.html')              # 템플릿을 불러옴
    elif request.method == 'POST':
        obj = Table2() # obj 객체 생성
        obj.name = request.POST['name']  # 변수에 값
        obj.kor  = request.POST['kor']
        obj.eng  = request.POST['eng']
        obj.math = request.POST['math']
        obj.save()                       # 저장하기 수행

        return redirect("/board/t2_insert")

def dataframe(request):
    if request.method == 'GET':
        df = pd.read_sql(
            """
            SELECT NO, WRITER, HIT, REGDATE
            FROM BOARD_TABLE1
            """, con=connection)
        print(df)
        print(df['NO'])
        return render(request, 'board/dataframe.html',{"df":df.to_html(classes="table")})

@csrf_exempt
def edit(request):
    if request.method == 'GET':
        no = request.GET.get("no", 0)
        sql = """
            SELECT NO, TITLE, CONTENT
            FROM BOARD_TABLE1
            WHERE NO=%s
        """
        cursor.execute(sql, [no])
        data = cursor.fetchone()
        return render(request, 'board/edit.html', {"one":data})
    elif request.method == 'POST':
        no = request.POST['no']
        ti = request.POST['title']
        co = request.POST['content']
        arr = [ti,co,no]
        sql = """
            UPDATE BOARD_TABLE1 SET TITLE=%s, CONTENT=%s WHERE NO = %s
        """
        cursor.execute(sql, arr)
        return redirect("/board/content?no="+ no)

@csrf_exempt
def delete(request):
    if request.method == 'GET':
        no = request.GET.get("no",0)
        sql = """
            DELETE FROM BOARD_TABLE1
            WHERE NO=%s
        """
        cursor.execute(sql, [no])
        return redirect("/board/list")

@csrf_exempt
def content(request):
    if request.method =='GET':
        no = request.GET.get('no',0)
        # 127.0.0.1:8000/board/content?no=34
        # 127.0.0.1:8000/board/content     ?no=0 => 오류발생
        # # If와 Else의 개념 : ? 기준으로 no= 가 있는지 없는지 여부 확인
        # if no=34라는 값이 들어가게 되면 no에다가 34를 대입, no에 값이 없을 경우 no에다가 0를 대입
        # request.GET['no']
        if no == 0 :
            return redirect("/board/list") # <a href와 같음>
        if request.session['hit']==1:
            sql = """
                UPDATE BOARD_TABLE1 SET HIT = HIT+1 
                WHERE NO = %s
            """ # 조회 수 1 증가시킴
            cursor.execute(sql,[no])
            request.session['hit'] = 0

        # 이전글 번호 가져오기
        sql ="""
            SELECT NVL(MAX(NO),0) 
            FROM BOARD_TABLE1
            WHERE NO < %s
        """ # NVL은 첫 번째 인자값이 없으면 0으로 출력
        cursor.execute(sql,[no])
        prev = cursor.fetchone()

        # 다음글 번호 가져오기
        sql ="""
            SELECT NVL(MIN(NO),0)
            FROM BOARD_TABLE1
            WHERE NO > %s
        """
        cursor.execute(sql,[no])
        next = cursor.fetchone()

        # 가져오기
        sql = """
            SELECT
                NO, TITLE, CONTENT, WRITER, HIT,
                TO_CHAR(REGDATE, 'YYYY-MM-DD HH:MI:SS')
                , IMG
            FROM
                BOARD_TABLE1
            WHERE
                NO = %s
        """
        cursor.execute(sql,[no])
        data = cursor.fetchone()   # (1,2,3,4,5,6)

        if data[6] : # DB에 BLOB에 있는 경우
            img = data[6].read() # 바이트 배열을 img에 넣음
            img64 = b64encode(img).decode("utf-8")
        else : # 없는 경우
            file = open('./static/img/default.jpg','rb')
            img = file.read()
            img64 = b64encode(img).decode("utf-8")

        # print(type([no]))        # list
        # print(type(data))        # tuple
        return render(request, 'board/content.html',
         {"one":data, "image":img64, "prev": prev[0], "next":next[0]})

@csrf_exempt
def list(request):
    if request.method =='GET':
        request.session['hit'] = 1 # 세션에 hit=1
        sql = """
            SELECT NO, TITLE, CONTENT, WRITER, HIT, TO_CHAR(REGDATE, 'YYYY-MM-DD HH:MI:SS')
            FROM BOARD_TABLE1
            ORDER BY NO DESC
        """
        cursor.execute(sql)
        data = cursor.fetchall() # 한 번에 모든 Row를 읽기 위해서 사용
        # print(type(data))      # list
        # print(data)            # [ ( ), ( ) ]
        return render(request, 'board/list.html',{"abc":data}) # "abc"는 KEY
    

@csrf_exempt
def write(request):
    if request.method =='GET':
        return render(request, 'board/write.html')
    elif request.method == 'POST':
        tmp = None        
        if 'img' in request.FILES:
            img = request.FILES['img'] # name값 img
            tmp = img.read() # 이미지를 byte[]로 변경  
        arr = [
            request.POST['title'],
            request.POST['content'],
            request.POST['writer'],
            tmp
        ]
        try :
            # print(arr)
            sql = """
                INSERT INTO BOARD_TABLE1
                (TITLE, CONTENT, WRITER, IMG, HIT, REGDATE)
                VALUES(%s, %s, %s, %s, 234, SYSDATE)
            """
            cursor.execute(sql, arr)
        except Exception as e:
            print(e)
        return redirect("/board/list") # a href와 같음