# 파일명 : api/urls.py 직접 생성
# urls.py는 상위 url
# 하위 url은 member, board 등에서 만듦
from django.urls import path
from . import views

urlpatterns = [
    path('select1', views.select1, name="select1"),
    path('select2', views.select2, name="select2"),
    path('insert1', views.insert1, name="insert1"),
]