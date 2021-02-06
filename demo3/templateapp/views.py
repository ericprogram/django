from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

# 模板


class TempView(View):

    def get(self,request):
        date = {"name":"程序员",
                'alist':[1,2,3,3,4],
                # 'alist': None,
                'adict':{'name':'张三','age':18},
                "a":40
        }

        # return render(request,'index.html',context="此参数必须传入字典")
        return render(request,'index.html',context=date)


class TempBaseView(View):
    def get(self,request):
        return render(request,'base.html')


class TempChildView(View):
    def get(self,request):
        return render(request,'child.html')


class Jinja2View(View):
    def get(self, request):
        date = {
            'jinja2_list' : ["a", "b", "c"],
            'abc': "B"
        }
        return render(request,'jinja2_test.html',context=date)