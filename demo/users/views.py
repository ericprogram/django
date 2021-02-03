from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

"""
定义视图函数:
1.至少要有一个函数，用来接收函数请求对象
2.在函数最后必须要要返回一个响应对戏

"""
# http://127.0.0.1:8000/users/index/
def index(request):
    # 省略了业务逻辑处理代码
    return HttpResponse("hello")


