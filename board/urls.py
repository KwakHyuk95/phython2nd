from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    # path('url명', 뷰에서.가져올 함수)
    path('', views.index, name='index'),
    path('<int:question_id>', views.detail, name='detail'),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('question/create/', views.question_create, name='question_create'),
    # path('testpage/', views.test),
]