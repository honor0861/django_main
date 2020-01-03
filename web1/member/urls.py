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
    path('list', views.list, name="list"),
    path('edit', views.edit, name="edit"),
    path('delete', views.delete, name="delete"),
    path('join1', views.join1, name="join1")  # ur1 만들기용 -> join1
    ]