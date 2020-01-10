from django.db import models

# python manage.py check
# python manage.py makemigrations api
# python manage.py migrate api

class Item(models.Model):
    objects = models.Manager() # vs code 오류 제거용
    
    no      = models.AutoField(primary_key=True)      # 자동 입력, 기본 키
    name    = models.CharField(max_length=30)        # 문자타입, 최대 200글자
    price   = models.IntegerField()                   # 32비트 정수형 필드
    regdate = models.DateTimeField(auto_now_add=True) # 날짜와 시간을 갖는 필드, 자동 생성