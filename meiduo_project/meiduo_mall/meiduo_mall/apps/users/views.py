import json
import re
from django import http
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from django_redis import get_redis_connection
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail


from . models import User
from . utils import generate_verify_email_url, get_user_check_token
from meiduo_mall.utils.response_code import RETCODE
from meiduo_mall.utils.views import LoginRequiredView
from celery_tasks.email.tasks import send_verify_email


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
        response = redirect('/')
        response.set_cookie('username', user.username, max_age=settings.SESSION.SESSION_COOKIE_AGE)
        return response


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

        # 获取用户界面来源
        next = request.GET.get('next')

        # 用户登陆成功后，向cookie中存储username
        response = redirect(next or '/')

        # response.set_cookie('username', user.username,
        #                     max_age=None if remembered is None else settings.SESSION_COOKIE_AGE)
        response.set_cookie('username', user.username,
                            max_age=remembered and settings.SESSION_COOKIE_AGE)
        # 重定向到首页
        # return http.HttpResponse("登陆成功，跳转到首页")

        return response


class LogoutView(View):
    """ 登出 """
    def get(self, request):
        # 1.清除状态保持
        logout(request)

        # 创建响应对象
        response = redirect('users:login')
        # 2.清除cookie中的username
        response.delete_cookie('username')

        # 3.重定向到login
        return response


# class InfoView(View):
#     """ 用户中心 """
#     def get(self, request):
#         user = request.user
#         # 如果用户没有登陆就调整到登陆界面
#         if not user.is_authenticated:
#             # return redirect('users:login')
#             return redirect('/login/?next=/info/')
#         else:
#             # 如果用户登陆了，就展示用户中心界面
#             return render(request, 'user_center_info.html')


# 精简代码实现用户中心
class InfoView(LoginRequiredMixin, View):
    """ 用户中心 """
    def get(self, request):
        return render(request, 'user_center_info.html')

# 精简代码实现用户中心第三种方法 装饰器
# @method_decorator(login_required, name='get')
# class InfoView(View):
#     """ 用户中心 """
#     def get(self, request):
#         return render(request, 'user_center_info.html')


class EmailView(LoginRequiredView):
    """ 设置用户邮箱，并发送激活邮箱url """

    def put(self, request):
        # 1.接收请求体非表单数据 body
        json_dict = json.loads(request.body.decode())
        email = json_dict.get('email')

        # 2.校验
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return http.HttpResponseForbidden('邮箱格式有误')

        # 3.修改user模型的email字段
        user = request.user

        # 如果用户没有去设置邮箱再去设置，如果设置过了就不要再设置了
        if user.email != email:
            user.email = email
            user.save()

        # 给当前设置的邮箱发一封激活url
        # send_mail(subject='邮件的标题/主题', message='普通字符串邮件正文', from_email='发件人', recipient_list=['收件人'],
        #           html_message='超文本邮件正文')
        # html_message = '<p> 这是一个激活邮件<a href ="http://www.baidu.com">点我激活</a></p>'
        # 美多商城测试 < chm522 @ 163.com >
        # send_mail(subject='激活邮箱', message='普通字符串邮件正文', from_email=settings.EMAIL_FROM, recipient_list=[email],
        #           html_message=html_message)

        # verify_url = 'http://www.baidu.com'
        verify_url = generate_verify_email_url(user)
        send_verify_email.delay(email, verify_url)

        # 响应
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '添加邮箱成功'})


class EmailVerifyView(View):
    """激活邮箱"""
    def get(self, request):
        # 1.接收查询参数中 token
        token = request.GET.get('token')

        # 2 对token解密，并根据用户信息查询到指定user
        user = get_user_check_token(token)
        if user is None:
            return http.HttpResponseForbidden('邮箱激活失败')

        # 3.修改指定user的email_active字段
        user.email_active = True
        user.save()

        # 4.响应
        return render(request, 'user_center_info.html')


class AddressesView(LoginRequiredView):
    """用户收货地址"""
    def get(self, request):
        return render(request, 'user_center_site.html')
