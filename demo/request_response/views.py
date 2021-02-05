<<<<<<< HEAD
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
=======
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
import json

# Create your views here.

"""Django中的视图函数不需要指定请求方法,只要路由匹配成功都可以调用, 查询字符串无论是get请求还是post请求都可以有,但一般都是get请求带查询字符串"""


# /weather/beijing/2018
def weather1(request, city, year):
    """演示获取url路径数据"""
    print(city)
    print(year)

    return HttpResponse('weather1')


# /weather/beijing/2018
def weather2(request, year, city):
    """演示获取url路径数据"""
    print(city)
    print(year)

    return HttpResponse('weather1')


# GET /get_query_params/
def get_query_params(request):
    """演示获取url查询字符串数据"""
    # request.GET 后面大写的GET只是一个请求对象的属性而已,和请求方法无关 QueryDict类型对象
    query_dict = request.GET
    # query_dict.get()  取单个值
    # query_dict.getlist() 取某个的多个值,返回列表
    return HttpResponse('get_query_params')


# request.POST 用来获取请求体中的表单数据, 大写的POST只是一个属性而已,和请求方法无关, QueryDict类型对象
# POST /get_form_data/
def get_form_data(request):
    """演示获取请求体表单数据"""

    query_dict = request.POST
    print(query_dict.get('a'))
    print(query_dict.getlist('like'))

    return HttpResponse('get_form_data')


# POST /get_json/
def get_json(request):
    """演示获取请求体中的非表单数据:json"""
    # 获取请求体非表单数据用body属性,得到bytes类型的数据
    json_bytes = request.body
    json_str = json_bytes.decode()
    dict = json.loads(json_str)  # 将json字符串转换成json字典或json列表
    # json.dumps()  # 把字典或列表转换成json字符串
    print(dict)
    return HttpResponse('get_json')


def get_user(request):
    """演示获取当前请求对象"""
    # 当前如果没有登录获取 request.user 会是一个匿名用户AnonymousUser
    # 如果当前登录了,request.user 获取到当前登录的用户对象 zhangsan
    print(request.user)
    return HttpResponse('get_user')






# GET /response_demo/
def response_demo(request):
    """演示响应对象的基本操作"""
    # return HttpResponse(content='hello', content_type='text/html', status=200)
    # return HttpResponse(content='hello', content_type='text/plain', status=201)
    response = HttpResponse('hello')
    response['itcast'] = 'hello world'  # 自定义响应头
    # return HttpResponse(content='hello')
    return response


# GET /json_response_demo/
def json_response_demo(request):
    """演示响应json数据"""
    # data = {'name': 'zs', 'age': 12}
    data = [{'name': 'zs', 'age': 12}, 'hahaha']
    dict = {'dict1': data}
    # 如果响应的json数据不是字典面是列表 要么 多指定safe=False 或者把列表包装成字典格式
    return JsonResponse(dict)


# GET /redirect_demo/
def redirect_demo(request):

    """演示重定向"""
    # if 判断当前是不是登录用户,如果是 返回用户中心界面数据
    #     else:

    # print(reverse('index')) # /json_response_demo_xxxx/  没有设置命名空间时,可以用路由别名进行反向解析,它是全局查找
    # 如果设置了命名空间后,那么这个子应用中进行反向解析时 写法 (命名空间:路由别名)
    print(reverse('request_response:index')) # json_response_demo_xxxx

    # 在路由最前面加/ 代表从根路由进行重定向,如果没有加/ 那么就是从当前路由拼接后面的路由再进行定向
    # return redirect('/users/index/')
    # return HttpResponse('redirect_demo')
    return redirect(reverse('users:index'))


# GET /cookie_demo/
def cookie_demo(request):
    """演示cookie读写操作"""

    response = HttpResponse('ok')
    response.set_cookie('name', 'ww', max_age=3600)  # 设置cookie
    # response.delete_cookie('name')  # 删除cookie

    print(request.COOKIES.get('name'))  # None  zs
    return response

# GET /session_demo/
def session_demo(request):
    """演示session读写操作"""
    # session依赖于cookie
    # 当代码执行到这行时,会将session设置到redis数据
    # 同时,生成了一个唯一session_id的东西,把session_id 通过后期的响应对象设置到浏览器的cookie中
    # request.session['name'] = 'zhangsan'  # 设置session

    # 先通过请求对象读取到cookie中的session_id, 然后通过session_id再读取出redis中session记录, 再通过name key获取value
    print(request.session.get('name'))  # 读取session
    return HttpResponse('session_demo')

>>>>>>> e11c1fb91caeb86092f06f789fd5f2a5c8e240c7
