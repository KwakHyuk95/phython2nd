from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# ORM
# 데이터베이스의 데이터를 조회하거나 저장하기위해 원래는
# 퀘리(SQL)을 사용했지만 Django에서는
# 데이터베이스 테이블을 '모델화'해서 사용하고 쿼리들을
# Django 기준 python 코드로 처리하는 방법.

# ORM의 특징
# 개발자만의 쿼리(SQL)을 만들기가 어렵다.
# 쿼리를 잘못 작성할 가능성이 낮아진다(간단한 명령에 한해서)
# DBMS를 변경(이관)할때 쿼리를 바꿀 필요가 없다.

# 모델 작성
# 질문, 답변 모델을 생성
# 질문모델
# subject : 질문의 제목
# content : 질문의 내용
# create_date : 질문을 작성한 일시

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200) # CharField 문자의 길이를 제한
    content = models.TextField() # TextField 제한없이 문자를 입력받고 싶을때 씀
    create_date = models.DateTimeField() # 날짜나 시간은 상황에 맞게 TextField나 DateTimeField 사용

    def __str__(self):
        return self.subject

# 답변모델
# question : 질문
# content : 답변의 내용
# create_date : e답변 작성 일시.
# 컬럼에 null을 허용하고 싶다면 null=True를 추가

# 21.10.01 곽혁 글쓴이 추가
class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # on_delete=models.CASCADE는 답변에 연결된 질문이 삭제되면 답변도 함께 삭제하라는 의미
    content = models.TextField()
    create_date = models.DateTimeField()

