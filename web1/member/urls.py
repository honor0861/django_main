# member/urls.py : 하위 url에 속함, 사전에 파일 생성해야 함 
from django.urls import path # path 호출 추가
from . import views # 현재 패키지에서 views 모듈을 가져옴

# 127.0.0.1:8000/member/index => index 함수 동작
# 127.0.0.1:8000/member/login
# 127.0.0.1:8000/member/join
# 127.0.0.1:8000/board/write
# 127.0.0.1:8000/board/list

urlpatterns = [
    path('index', views.index, name="index"), # path가 index일 때 views
    path('join', views.join, name="join"),
    path('login', views.login, name="login"),
    path('logout',views.logout, name="logout"),
    path('list1', views.list1, name="list1"),
    path('edit', views.edit, name="edit"),
    path('delete', views.delete, name="delete"),
    path('join1', views.join1, name="join1"),  # ur1 만들기용 -> join1

    path('auth_join', views.auth_join, name="auth_join"),
    path('auth_login', views.auth_login, name="auth_login"),
    path('auth_logout', views.auth_logout, name="auth_logout"),
    path('auth_edit', views.auth_edit, name="auth_edit"),
    path('auth_pw', views.auth_pw, name="auth_pw"),
    path('auth_index', views.auth_index, name="auth_index"),

    path('exam_insert',views.exam_insert, name="exam_insert"),
    path('exam_list',views.exam_list, name="exam_list"),
    #path('exam_update',views.exam_update, name="exam_update"),
    #path('exam_delete',views.exam_delete, name="exam_delete"),
    path('exam_select',views.exam_select, name="exam_select"),

    path('js_index', views.js_index, name="js_index"),
    path('js_chart', views.js_chart, name="js_chart"),
    
    path('dataframe', views.dataframe, name="dataframe"),
    path('graph', views.graph, name="graph"),
    path('graph2', views.graph2, name="graph2")
    ]