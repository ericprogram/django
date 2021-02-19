from django import http
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views import View
import re

from django_redis import get_redis_connection

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

        # 短信验证码校验逻辑
        # 创建redis连接对象
        redis_conn = get_redis_connection('verify_codes')

        # 获取redis数据库中当前用户短信验证码
        sms_code_server_bytes = redis_conn.get('sms_%s' % mobile)

        # 删除已经取出的短信验证码,让它只能被使用一次
        redis_conn.delete('sms_%s' % mobile)

        # 判断redis中短信验证码是否过期
        if sms_code_server_bytes is None:
            return http.JsonResponse({'code': RETCODE.SMSCODERR, 'errmsg': '短信验证码已过期'})

        # 将bytes类型转换为字符串类型
        sms_code_server = sms_code_server_bytes.decode()

        # 用户填写的和redis中的短信验证码是否一致
        if sms_code != sms_code_server:
            return http.JsonResponse({'code': RETCODE.SMSCODERR, 'errmsg': '短信验证码填写错误'})

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
        # return http.HttpResponse('注册成功，登陆到首页')
        return redirect('/')


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


class LoginView(View):
    """ 登陆 """
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        # 接收请求表单数据
        query_dict = request.POST
        print(query_dict.dict().keys())
        username = query_dict.get('username')
        password = query_dict.get('password')
        remembered = query_dict.get('remembered')

        # 校验
        if all([username,password]) is False:
            return http.HttpResponseForbidden("缺少必传参数")

        # 登陆验证
        # if 如果是手机登陆:
        #     user = User.objects.get(mobile=username)
        # elif 如果是邮箱登陆：
        #     user = User.objects.get(email=username)
        # else:
        #     user = User.objects.get(username=username)
        # user.check_password(password)
        # 以上两句代码相当于  authenticate(request, username=username, password=password)

        # authenticate 默认配置读取的是username ，如果需要用手机号登陆，需要重写authenticate
        user = authenticate(request, username=username, password=password)

        # 判断用户是否通过身份认证
        if user is None:
            return render(request, 'login.html', {'account_errmsg': '用户名或密码错误'})
        # 状态保持
        login(request, user)

        # 如果用户没有勾选记住登陆，设置session过期时间为会话结束
        # if remembered is None:
        #     # 设置过期时间
        #     request.session.set_expiry(0)
        # else:
        #     request.session.set_expiry(3600 * 24 * 7)

        # 三目运算
        # request.session.set_expiry(0 if remembered is None else (3600 * 24 * 7))

        # 如果勾选记住密码设置为None,默认两周，否则设置会话时间为结束
        request.session.set_expiry(None if remembered else 0)

        # 重定向到首页
        # return http.HttpResponse("登陆成功，跳转到首页")
        return redirect('/')