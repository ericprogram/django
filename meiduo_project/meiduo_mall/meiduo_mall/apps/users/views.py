import re

from django import http
from django.shortcuts import render

# Create your views here.
from django.views import View


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

        # 2.校验数据
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

        #TODO 短信验证码校验逻辑


        # 3.创建user并且存储到表中
        # 响应

        pass