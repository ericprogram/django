from django.contrib.auth import login
from django.shortcuts import render, redirect
from QQLoginTool.QQtool import OAuthQQ
from django.views import View
from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden, HttpResponseServerError
import logging


from meiduo_mall.utils.response_code import RETCODE
from . models import OAuthQQUser

QQ_CLIENT_ID = '101518219'
QQ_CLIENT_SECRET = '418d84ebdc7241efb79536886ae95224'
QQ_REDIRECT_URI = 'http://www.meiduo.site:8000/oauth_callback'


logger = logging.getLogger('django')

class QQAuthURLView(View):
    """提供QQ登陆URL"""
    def get(self, request):

        # 1.获取查询参数
        next = request.GET.get('next') or '/'

        # 2.创建OAuthQQ工具对象
        # auth_qq = OAuthQQ(client_id='appid',
        #                   client_secret='appkey',
        #                   redirect_uri='QQ登陆成功后的回调地址',
        #                   state='登陆成功重定向时会原样带回')

        # auth_qq = OAuthQQ(client_id='101518219',
        #                   client_secret=‘418d84ebdc7241efb79536886ae95224’,
        #                   redirect_uri='http://www.meiduo.site:8000/oauth_callback',
        #                   state=next)

        auth_qq = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                          client_secret=settings.QQ_CLIENT_SECRET,
                          redirect_uri=settings.QQ_REDIRECT_URI,
                          state=next)

        # 3.调用它里面的get_qq_url 方法，得到拼接好的qq登陆url
        login_url = auth_qq.get_qq_url()

        # 4.响应
        return JsonResponse({'login_url': login_url, 'code': RETCODE.OK, 'errmsg': 'OK'})


class QQAuthView(View):
    """ QQ扫码登陆成功后的回调处理 """
    def get(self, request):

        # 1.获取查询字符串code
        code = request.GET.get('code')

        # 2.校验是否获取到code
        if code is None:
            return HttpResponseForbidden('缺少code')

        # 3.创建QQ登陆辅助工具对象
        auth_qq = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                          client_secret=settings.QQ_CLIENT_SECRET,
                          redirect_uri=settings.QQ_REDIRECT_URI)
        try:
            # 4.调用get_access_token(code) 得到access_token
            access_token = auth_qq.get_access_token(code)

            # 5.调用 get_open_id(access_token) 得到openid
            openid = auth_qq.get_open_id(access_token)
        except Exception as e:
            logger.error(e)
            return HttpResponseServerError('OAUTH 2.0 认证失败')

        # 6.查询openid
        try:
            oAuth_mode = OAuthQQUser.objects.get(openid=openid)
            # 如果能执行到这里说明上面哪行代码查询到了openid
            # 查询到openid 说明此QQ用户已绑定过美多用户，直接代表登陆成功
            # 状态保持
            user = oAuth_mode.user
            login(request, user)

            # 获取查询参数中的state
            next = request.GET.get('state') or '/'

            # 创建响应对象
            response = redirect(next)
            # 向浏览器的cookie中储存username
            response.set_cookie('username', user.username, max_age=settings.SESSION_COOKIE_AGE)

            # 重定向来源界面
            return response
        except OAuthQQUser.DoesNotExist:
            # 说明openid还没有绑定美多用户，渲染一个绑定界面
            return render(request, 'oauth_callback.html', {'openid': openid})

