from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginRequiredView(LoginRequiredMixin, View):
    """ 判断登陆的工具类 """
    pass
