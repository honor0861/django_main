from django.shortcuts import render
from django.http import HttpResponse

# insert1
from .models import Item

# select1
from .serializers import ItemSerializer
from rest_framework.renderers import JSONRenderer
import json

# 127.0.0.1:8000/api/select1?key=abc
# {"id":"a"} => 물품 1개
def select1(request):
    key = request.GET.get("key","")
    num = int(request.GET.get("num","1"))
    search = request.GET.get("search","")
    data = json.dumps({"ret":'key error'})
    # DB에서 확인
    
    if key == 'abc': 
        obj = Item.objects.filter(name__contains = search)[:num] # name 속성이 search 값을 가지고 있는 것
        serializer = ItemSerializer(obj, many=True)
        data = JSONRenderer().render(serializer.data)
        return HttpResponse(data)

# [{"id":"a"}, {"id":"b"}]
def select2(request):
    obj = Item.objects.all()
    serializer = ItemSerializer(obj, many=True)
    data = JSONRenderer().render(serializer.data)
    return HttpResponse(data)

# 127.0.0.1:8000/api/insert1
def insert1(request):
    for i in range(1,31,1):
        obj = Item()
        obj.name = '도서'+str(i)
        obj.price = 4000+i
        obj.save()

    return HttpResponse("insert1")
