from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from common.forms import UserForm

# 21.10.1 곽혁 사이트 회원가입기능 구현

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            # 로그인을 바로 하게 만듬
            username = form.cleaned_data.get('username') # 데이터를 개별적으로 따올때
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password) # 인증 정확한지 확인
            login(request, user) # 로그인 요청
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})