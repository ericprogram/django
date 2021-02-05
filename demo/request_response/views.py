import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
from django.urls import reverse


def weather(request,year,city):
    print(city,year)
    return HttpResponse("OK")




# 获取url中的查询字符串数据
# request.GET GET只是一个属性而已和请求方式无关，得到QueryDict类型对象
# QueryDict  get 只能取一键一值 getlist;获取一键多值，返回的是一个列表
# http://127.0.0.1:8003/get_query_params/?a=100&b=200&a=300
def get_query_params(request):
    query_dict = request.GET
    a = query_dict.get('a')
    alist = query_dict.getlist('a')
    print('a=',a)
    print("alist=",alist)
    return HttpResponse("get_query_params")


# 演示获取请求体中的表单数据
#request.POST
# 在Django非get请求都要进行CSRF认证
def get_form_date(request):
    query_post = request.POST
    print('query_post',query_post)
    return HttpResponse('get_from_date')

# 演示获取请求体的非表单数据 json: [],b'{}'
# bytes_date = request.body       bytes
# json_date_str = bytes_date.decode()
# data = json.loads(json_date_str)
# date = json.loads(request.body.decode())

def get_json(requset):
    json_dict = json.loads(requset.body.decode())
    print('json_dict=',json_dict)
    return  HttpResponse("get_json")


# 响应对象的基本使用
def response_test(requset):
    # return HttpResponse(content="hello",content_type='text/html',status=200)
    # return HttpResponse(content="hello2",content_type='text/pan',status=200)

    response = HttpResponse("hello 3")
    # response['eric'] = 'hmchen' 自定义

    # date = {"name":"eric", "age":18}
    date1 =[1,2,3,4]
    # response = JsonResponse(date1, safe=False)
    date = {'alist':date1}
    response = JsonResponse(date)

    return response

# 重定向的使用
def redirect_test(request):
    print("重定向")
    # 如果重定向时，路由最前面不加 / 就是基于当前url拼接要生定向的路径  http://127.0.0.1:8003/response_test/
    # return redirect('/get_query_params/')   不推荐写死路由
    # 反向解析
    # return redirect(get_query_params)
    # 加路由别名
    # return redirect('query_par')
    # 主url加命名空间
    print(reverse('users:query_par'))
    # return redirect(reverse('users:query_par'))
    return redirect('users:query_par')

# cookie读写操作
def cookie_test(request):
    response = HttpResponse("cookie test")
    # 设置cookie
    response.set_cookie('name','eric',max_age=3600)
    response.set_cookie('age', '18', max_age=3600)

    # 读取cookie ,这一次设置的cookie，下一次访问才能读取到
    name = request.COOKIES.get('name')
    print("name=",name)
    return response
