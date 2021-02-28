import re
from django.contrib.auth.backends import ModelBackend
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData
from django.conf import settings


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


def generate_verify_email_url(user):
    """ 生成用户激活邮箱url """
    # 1.创建加密实例对象
    serializer = Serializer(secret_key=settings.SECRET_KEY, expires_in=3600 * 24)

    # 2.包装要加密字典数据
    data = {'user_id': user.id, 'email': user.email}

    # 3.加密 decode()
    token = serializer.dumps(data).decode()

    # 4.拼接激活url
    verify_url = settings.EMAIL_VERIFY_URL + '?token=' +token

    # 返回url
    return verify_url


def get_user_check_token(token):
    """
    对token进行解密并查询返回到指定user
    @param token: 要解密的用户数据
    @return: user or None
    """
    # 1.创建解密的实例对象
    serializer = Serializer(secret_key=settings.SECRET_KEY, expires_in=3600 * 24)

    # 2.loads
    try:
        date = serializer.loads(token)
        user_id = date.get('user_id')
        email = date.get('email')
        try:
            user = User.objects.get(id=user_id,email=email)
            return user
        except User.DoesNotExist:
            return None
    except BadData:
        return None


