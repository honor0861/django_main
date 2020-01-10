# 파일명 : seralizers.py => 직렬화

from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('no','name','price','regdate')