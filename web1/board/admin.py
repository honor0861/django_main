from django.contrib import admin

from board.models import Table1
admin.site.register(Table1)

# conda list => django 버전 확인
# pip install django == 2.25
# python manage.py createsuperuser
# admin => 아이디
# 1234 => 암호
# 1234
# y