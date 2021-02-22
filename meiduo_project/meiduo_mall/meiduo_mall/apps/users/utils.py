import re
from django.contrib.auth.backends import ModelBackend


from . models import User


def get_user_by_account(account):
    """
    通过账号获取用户模型对象
    @param account: mobile / username
    @return: user or None
    """
    try:
        if re.match(r'1[3-9]\d{9}', account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
        return user
    except User.DoesNotExist:
        return None


class UsernameMobileAuthBackend(ModelBackend):
    """ 自定义认证后端类实现多账号登陆 """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 1.根据用户名或者手机号 查询user
        user = get_user_by_account(username)

        # 2.校验用户密码
        if user and user.check_password(password) and user.is_active:
            # 3.返回user or Nore
            return user
