# $ python manage.py check
# $ python manage.py makemigrations member
# $ python manage.py migrate member

# 1. 회원을 20명 추가하시오
# ex) 101 102 506 409
from django.db import models

class Table2(models.Model):
    objects = models.Manager() # vs code 오류 제거용
    
    no          = models.AutoField(primary_key=True)
    name        = models.CharField(max_length=30)
    kor         = models.IntegerField()
    eng         = models.IntegerField()
    math        = models.IntegerField()
    classroom   = models.CharField(max_length=3)
    regdate     = models.DateTimeField(auto_now_add=True)