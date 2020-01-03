from django.db import models

# Create your models here.

class Table1(models.Model):
    objects = models.Manager() # vs code 오류 제거용
    
    no      = models.AutoField(primary_key=True)      # 자동 입력, 기본 키
    title   = models.CharField(max_length=200)        # 문자타입, 최대 200글자
    content = models.TextField()                      # 길이 제한이 없는 문자열
    writer  = models.CharField(max_length=50)         # 최대 15글자
    hit     = models.IntegerField()                   # 32비트 정수형 필드
    img     = models.BinaryField(null=True)           # 바이너리 필드
    regdate = models.DateTimeField(auto_now_add=True) # 날짜와 시간을 갖는 필드, 자동 생성
    