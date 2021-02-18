from django import http
from django.contrib.auth import login
from django.shortcuts import render
from django.views import View
import re


from .models import User
from meiduo_mall.utils.response_code import RETCODE

class RegisterView(View):
    """ 用户注册 """
    def get(self, request):
        """
         提供注册界面
         :param request: 请求对象
         :return: 注册界面
        """
        return render(request, 'register.html')

    def post(self, request):
        # 1.接收请求体表单数据 POST
        query_dict = request.POST
        username = query_dict.get('username')
        password = query_dict.get('password')
        password2 = query_dict.get('password2')
        mobile = query_dict.get('mobile')
        sms_code = query_dict.get('sms_code')
        allow = query_dict.get('allow')  # 如果表单中的复选框没有指定value时勾选，传入的是'on'，反之None.

        # 2.校验数据  ‘’, {} , [],False, None
        # all([]) 返回 True, False
        if all([username, password, password2, mobile, sms_code, allow]) is False:
            # 前台有非空校验，校验是防止用户在非前台页面注册的情况
            return http.HttpResponseForbidden('缺少必传参数')

        # 正则校验用户名
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')

        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')

        if password != password2:
            return http.HttpResponseForbidden('两次输入的密码不一致')

        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号码')

        # TODO 短信验证码校验逻辑

        # 3.创建user并且存储到表中
        # user = User.objects.create(
        #     username = username,
        #     password = password,
        #     mobile = mobile
        #
        # )
        # user.set_password(password)
        # user.save()

        # 最简单的方法,创建并且保存用户
        # def create_user(self, username, email=None, password=None, **extra_fields):
        # 传参的第一个为位置参数，后面都为关键字参数所以需要password=password
        user = User.objects.create_user(username, password=password, mobile=mobile)

        # 注册成功，即代表登陆成功 (状态保持)
        # request.session['id'] = user.id
        # user_id = request.session['id']

        # django 自带的状态保持
        login(request, user)

        # 4.响应()

        return http.HttpResponse('注册成功，登陆到首页')


class UsernameCountView(View):
    """ 判断用户名是否重复"""
    def get(self, request, username):

        # 查询user表，查询username的数量
        count = User.objects.filter(username=username).count()

        # 包装响应数据
        data = {
            'count': count,
            'code': 'RETCODE.OK',  # 自定义状态码
            'errmsg': "OK"

        }
        # 响应
        return http.JsonResponse(data)


class MobileCountView(View):
    """ 判断手机号是否重复 """
    def get(self, request, mobile):
        # 查询user表，查询mobile的数量
        count = User.objects.filter(mobile=mobile).count()
        date = {
            'count': count,
            'code': 'RETCODE.OK',  # 自定义状态码
            'errmsg': "OK"
        }
        return http.JsonResponse(date)
