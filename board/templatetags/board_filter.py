from django import template

# 21.09.27 곽혁 템플릿 태그 커스터마이징
# 파이썬관련된 파일 건드릴때는 재시작해보는게 좋음

register = template.Library()

@register.filter
def sub(value, arg):
    return value - arg