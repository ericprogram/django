from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment


""" Jinja2模板引擎环境配置 """


def jinja2_environment(**options):
    """
    确保可以使用模板引擎中的{{ url('') }} {{ static('') }}这类语句
    """
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,

    })
    return env
