from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator


# 装饰器
def my_decorator(func1):

    def wrapper(request,*args,**kwargs):
        print("装饰器被调用了")
        print("本次请求的路径:%s" % request.path)
        return func1(request,*args,**kwargs)
    return wrapper

# @method_decorator(my_decorator,name='dispatch') # 相当于装饰了所有方法
# 为特定请求方法添加装饰器
# @method_decorator(my_decorator,name='get')
class DemoView(View):

    """ 类视图"""

    # 装饰器直接放方法之上，也可以调用修饰器
    # @method_decorator(my_decorator)
    def get(self,request):
        return HttpResponse("get")

    # @my_decorator 可以实现，不推荐
    def post(self, request):
        return HttpResponse("post")

    def put(self, request):
        return HttpResponse("put")

    def delete(self, request):
        return HttpResponse("delete")