# 파일명 : board
# urls.py는 상위 url
# 하위 url은 member, board 등에서 만듦
from django.urls import path
from . import views

urlpatterns = [
    path('list',views.list, name="list"),
    path('write', views.write, name="write"),
    path('content', views.content, name="content"),
    path('edit', views.edit, name="edit"),
    path('delete', views.delete, name="delete")
]