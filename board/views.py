from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# 경로를 못찾을때에는 앞에 마침표를 찍어 같은 경로라는걸을 알려준다.
from django.http import HttpResponse
# Create your views here.

# 주석달기
# 언제 누가 뭘 위해서 작성하는지
# 메인 페이지 작성
# 질문 목록 출력
#21.09.17 곽혁 작성
def index(request):
    # Question.objects.order_by('-create_date')
    # Question 모델에서 객체를 참조하는데 / -가 붙어있으면 해당 객체를 기준으로 역순정렬
    # 역순으로 정렬해올것 (객체는 create_date)

    # 페이징처리 추가 21.09.24 곽혁

    # 페이징 처리 관련 템플릿 태그 속성. (템플릿단 페이징 처리 속성)
    # .count : 전체 게시물 개수
    # .per_page : 페이지당 보여줄 게시물 개수
    # .page_range : 페이지 범위
    # number : 현재 페이지 번호
    # previous_page_number : 이전 페이지 번호
    # previous_page_number : 다음 페이지 번호
    # has_previous : 이전 페이지 유무
    # has_next : 다음 페이지 유무
    # start_index :  현재 페이지 시작 인덱스
    # end_index :  현재 페이지 끝 인덱스

    # 페이지의 입력 파라미터 추가.

    page = request.GET.get('page', '1')

    # 조회
    question_list = Question.objects.order_by('-create_date')

    # 페이징 처리 기능 구현
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩
    page_obj = paginator.get_page(page)
    context ={'question_list': page_obj}
    # 템플릿단에 던짐 / 변수에 담지않고 던져도 상관 X
    return render(request, 'question_list.html', context) # render는 조회성


def detail(request, question_id):
    # 글의 제목과 내용 출력
    question = Question.objects.get(id=question_id)
    return render(request, 'question_detail.html', {'question': question})

def test(request):
    return render(request, 'index.html')

# 21.09.23 답변 등록하기
# 작성자: 곽혁
# get_object_or_404 : 사용자에게 보여지는 에러 메세지 제어 함수
#                     데이터의 유츌을 막기 위한 방법.
# redirect : 페이지의 재 요청 데이터를 전송 후 페이지를 새로고침하기 위함

# def answer_create(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     # 다음과 같은 방식이 가능했던 이유는 question, answer 모델이 외래키로 연결되어 있기 때문
#     # question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
#     # answer 모델을 직접 사용하는 방법.
#     answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
#     answer.save()
#     return redirect('board:detail', question_id=question.id)

# 21.09.26 곽혁 질문답변기능 수정
@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.create_date = timezone.now()
            answer.save()
            return redirect('board:detail', question_id=question.id)
    else:
        form = AnswerForm()
    return render(request, 'question_detail.html', {'question': question, 'form': form})

# 21.09.24 곽혁 질문등록 기능 구현

@login_required(login_url='common:login') # 해당함수를 실행하기전에 로그인유무를 확인 로그인을 안했을시 해당 url로 이동
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            # 21.10.01 곽혁 글쓴이 추가
            question.author = request.user # request.user 현재 로그인한 계정의 User모델 객체
            question.create_date = timezone.now()
            question.save()
            return redirect('board:index')
    else:
        form = QuestionForm()
    return render(request, 'board/question_form.html', {'form': form})