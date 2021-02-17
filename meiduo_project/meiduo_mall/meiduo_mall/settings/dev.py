""" 开发环境配置文件 """
import os
import sys

"""
Django settings for meiduo_mall project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path


# print('sys path :', sys.path)

# 用Pycharm 直接打开导 文件直接会被加入sys.path中作为导包路径
# Python解释器会将项目启动文件所在的目录，也自动加入sys.path中作为导包路径

# ['E:\\eric\\py_django\\django\\meiduo_project\\meiduo_mall',
# 'E:\\eric\\py_django\\django\\meiduo_project',
# 'C:\\Program Files\\JetBrains\\PyCharm 2020.2\\plugins\\python\\helpers\\pycharm_display',
# 'D:\\Programs\\Python\\Python38\\python38.zip',
# 'D:\\Programs\\Python\\Python38\\DLLs',
# 'D:\\Programs\\Python\\Python38\\lib',
# 'D:\\Programs\\Python\\Python38',
# 'C:\\Users\\NING MEI\\AppData\\Roaming\\Python\\Python38\\site-packages',
# 'D:\\Programs\\Python\\Python38\\lib\\site-packages',
# 'C:\\Program Files\\JetBrains\\PyCharm 2020.2\\plugins\\python\\helpers\\pycharm_matplotlib_backend']


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 追加项目导包路径
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# print('sys path :', sys.path)

# ['E:\\eric\\py_django\\django\\meiduo_project\\meiduo_mall\\meiduo_mall\\apps',
# 'E:\\eric\\py_django\\django\\meiduo_project\\meiduo_mall',
# 'E:\\eric\\py_django\\django\\meiduo_project',
# 'C:\\Program Files\\JetBrains\\PyCharm 2020.2\\plugins\\python\\helpers\\pycharm_display',
# 'D:\\Programs\\Python\\Python38\\python38.zip', 'D:\\Programs\\Python\\Python38\\DLLs',
# 'D:\\Programs\\Python\\Python38\\lib', 'D:\\Programs\\Python\\Python38',
# 'C:\\Users\\NING MEI\\AppData\\Roaming\\Python\\Python38\\site-packages',
# 'D:\\Programs\\Python\\Python38\\lib\\site-packages',
# 'C:\\Program Files\\JetBrains\\PyCharm 2020.2\\plugins\\python\\helpers\\pycharm_matplotlib_backend']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bkn#swmx%(q6-6t&a#b-5#98$po+2-dx6dkra$t@m*m1a-u%$o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'meiduo_mall.apps.users.apps.UsersConfig'
    'users.apps.UsersConfig'
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'meiduo_mall.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',  # jinja2模板引擎
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            # 补充Jinja2模板引擎环境
            'environment': 'meiduo_mall.utils.jinja2_env.jinja2_environment',
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],

        },

    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'meiduo_mall.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
        'HOST': '127.0.0.1',  # 数据库主机
        'PORT': 3306,  # 数据库端口
        'USER': 'root',  # 数据库用户名
        'PASSWORD': '123456',  # 数据库用户密码
        'NAME': 'meiduo'  # 数据库名字
    }
}

# 配置项目缓存为Redis缓存
CACHES = {
    #  默认的Redis配置项，采用0号Redis库
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    #  状态保持的Redis配置项，采用1号Redis库
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
# session 缓存配置
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"


# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), 'logs/meiduo.log'),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  # 日志器
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'   # 使用中国语言

TIME_ZONE = 'Asia/Shanghai'  # 使用中国上海时间


USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# 静态文件访问路由前缀
STATIC_URL = '/static/'

# 配置静态文件加载路径
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
