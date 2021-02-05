# 导入模板模块
# from django import template
from django.template import Library

# 创建模板注册器
register = Library()

# 定义过滤函数,并添加装饰器把函数变为过滤器
@register.filter
def old_list(list):
    list.reverse()
    return list
