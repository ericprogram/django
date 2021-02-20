from django.shortcuts import render
from QQLoginTool.QQtool import OAuthQQ
from django.views import View
from django.conf import settings
from django.http import JsonResponse, HttpResponse

from meiduo_mall.utils.response_code import RETCODE

QQ_CLIENT_ID = '101518219'
QQ_CLIENT_SECRET = '418d84ebdc7241efb79536886ae95224'
QQ_REDIRECT_URI = 'http://www.meiduo.site:8000/oauth_callback'


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

