
from django.shortcuts import render

# Create your views here.
from django.template.defaultfilters import date
from django.db.models import F, Q, Sum, Avg, Max, Min
from booktest.models import Bookinfo, HeroInfo
import logging


"""  新增 
1）save
通过创建模型类对象，执行对象的save()方法保存到数据库中。
2）create
通过模型类.objects.create()保存。
"""

# 新增 1
# book = Bookinfo()
# book.btitle = "三国"
# book.bpub_date = "1999-9-9"
# book.save()


# 新增 2
# book = Bookinfo(
#     btitle="三国志",
#     bpub_date="1909-9-9"
# )
# book.save()

# 新增 3
# book = Bookinfo.objects.create(
#     btitle="三国战纪",
#     bpub_date = "1909-9-9"
# )

# 外键新增
# hero = HeroInfo.objects.create(
#     hname = '马超',
#     # hbook= book  #  给外键直接赋值时，要赋外键表示的模型对象
#     hbook_id=book.id  #  如果给外键id赋值,必须赋关联模型对象的id
#
# )

"""
基本查询:
get,all,count

get 查询单一结果，如果不存在会抛出模型类.DoesNotExist异常。
all 查询多个结果。
count 查询结果数量。
"""
# get 查询单一
# book = Bookinfo.objects.get(id=1)
# try:
#     book = Bookinfo.objects.get(btitle='笑傲江湖')
# except Bookinfo.DoesNotExist:
#     pass
# logging.error(book)


# all 查询多个结果,QuerySet查询集
# book = Bookinfo.objects.all()
# logging.error(book)

# count 查询结果数量
# book = Bookinfo.objects.count()
# logging.error(book)


"""
过滤查询：

filter ,exclude ,get

exclude  查询满足条件之外的

字段名__运算符

"""
# 1.查询id为1的书籍


# book = Bookinfo.objects.get(id=1)
# exact：表示判等。
# book = Bookinfo.objects.filter(id__exact=1)
# book = Bookinfo.objects.filter(id=1)
# logging.error(book)


# 2.查询书名包含”湖“的书籍，like %湖%
# contains：是否包含。
# book = Bookinfo.objects.filter(btitle__contains='湖')
# logging.error(book)
#
# # 3.查询书名以’部‘结尾的书籍（endwith ,startswith） like %部
# startswith、endswith：以指定值开头或结尾。
# book = Bookinfo.objects.filter(btitle__endswith='部')
# logging.error(book)


# 4.查询书名不为空的书籍
# isnull：是否为null。
# book = Bookinfo.objects.filter(btitle__isnull=False)
# logging.error(book)
#
# # 5.查询id编号为2和4的书籍
# book = Bookinfo.objects.filter(id__in=[2,4])
# logging.error(book)
#
# # 6.查询编号大于2的书籍（id__gt,id__lt,id__gtd,id__lte）
# gt 大于 (greater then)
# gte 大于等于 (greater then equal)
# lt 小于 (less then)
# lte 小于等于 (less then equal)

# book = Bookinfo.objects.filter(id__gt=2)
# logging.error(book)

# # 7.查询id不等于3的书籍
# 不等于的运算符，使用exclude()过滤器。
# book = Bookinfo.objects.exclude(id=3)
# logging.error(book)
#
# # 8.查询1980年发布的书籍
# year、month、day、week_day、hour、minute、second：对日期时间类型的属性进行运算。
# book = Bookinfo.objects.filter(bpub_date__year=1980)
# logging.error(book)
#
# # 9.查询1990年1月1日后发表的书籍
# book = Bookinfo.objects.filter(bpub_date__gt='1990-1-1')
# logging.error(book)
#

""" F对象 """
# F对象: 实现两个字段之间的比较也支持运算
# # 1.查询阅读量大于评论量的书籍
# book = Bookinfo.objects.filter(bread__gte=F('bcomment'))
# logging.error(book)
#
# # 2.查询阅读量大于2倍评论量的书籍
# book = Bookinfo.objects.filter(bread__gt=F('bcomment') * 2)
# logging.error(book)

""" Q对象 """
# # 1.查询阅读量大于20，或编号小于3的图书
# book1 = Bookinfo.objects.filter(bread__gt='20', id__lt='3')
# logging.error(book1)
#
# book2 = Bookinfo.objects.filter(bread__gt='20').filter(id__lt='3')
# logging.error(book2)
#
# # Q对象可以使用&、|连接，&表示逻辑与，|表示逻辑或
# book3 = Bookinfo.objects.filter(Q(bread__gt='20') & Q(id__lt='3'))
# logging.error(book3)
#
#
# book4 = Bookinfo.objects.filter(Q(bread__gt=20) | Q(pk__lt=3))
# logging.error(book4)
#
#
#
# # 2.查询编号不等于3的书籍
# book = Bookinfo.objects.exclude(id=3)
# logging.error(book)
#
# # Q对象前可以使用~操作符，表示非not。
# book = Bookinfo.objects.filter(~Q(pk=3))
# logging.error(book)


"""聚合函数"""
# 使用aggregate()过滤器调用聚合函数。聚合函数包括：Avg 平均，Count 数量，Max 最大，Min 最小，Sum 求和，被定义在django.db.models中
# 1.统计总的阅读量
# 注意aggregate的返回值是一个字典类型
# book = Bookinfo.objects.aggregate(Sum('bread'))
# logging.error(book)
#
# # 查询图书总数
# # 使用count时一般不使用aggregate()过滤器 ,count函数的返回值是一个数字。
# book = Bookinfo.objects.count()
# logging.error(book)

# book_avg = Bookinfo.objects.aggregate(Avg('bread'))
# logging.error(book_avg)
#
# book_max = Bookinfo.objects.aggregate(Max('bread'))
# logging.error(book_max)
#
# book_min = Bookinfo.objects.aggregate(Min('bread'))
# logging.error(book_min)


""" 排序 """
# 使用order_by对结果进行排序
# book = Bookinfo.objects.all().order_by('bread')  # 升序
# logging.error(book)
# book = Bookinfo.objects.all().order_by('-bread')  # 降序
# logging.error(book)


""" 
基础关联查询

由一到多的访问语法： 一对应的模型类对象.多对应的模型类名小写_set 例

由多到一的访问语法: 多对应的模型类对象.多对应的模型类中的关系类属性名
 """

# 1.一查多：查询编号为1的图书中所有人物信息
# book = Bookinfo.objects.get(id=1)
# heros = book.heroinfo_set.all()
# logging.error(heros)
#
# # 2.多查一：查询编号为1的英雄出自的书籍
# hero = HeroInfo.objects.get(id=1)
# book = hero.hbook
# logging.error(book)


"""  关联过滤查询
 
由多模型类条件查询一模型类数据:
语法如下：
关联模型类名小写__属性名__条件运算符=值

"""
# 1.多查一：查询书籍中人物的描述包含"降龙"的书籍
# book = Bookinfo.objects.filter(heroinfo__hcomment__contains='降龙')
# logging.error(book)

# 2.一查多：查询书名为"天龙八部"的所有人物信息
# hero = HeroInfo.objects.filter(hbook__btitle__contains='天龙八部')
# logging.error(hero)
#
# # 注意：如果没有"__运算符"部分，表示等于
# hero = HeroInfo.objects.filter(hbook__btitle='天龙八部')
# logging.error(hero)
#
# # 查询图书阅读量大于30的所有英雄
#
# hero = HeroInfo.objects.filter(hbook__bread__gt='30')
# logging.error(hero)


""" 
查询集 QuerySet 

查询集，也称查询结果集、QuerySet，表示从数据库中获取的对象集合。
当调用如下过滤器方法时，Django会返回查询集（而不是简单的列表）：
all()：返回所有数据。
filter()：返回满足条件的数据。
exclude()：返回满足条件之外的数据。
order_by()：对结果进行排序。
"""

# 对查询集可以再次调用过滤器进行过滤
# book = Bookinfo.objects.filter(bread__gt=30).order_by('bpub_date')
# logging.error(book)


# exists()：判断查询集中是否有数据，如果有则返回True，没有则返回False。


# 1）惰性执行
# 创建查询集不会访问数据库，直到调用数据时，才会访问数据库，调用数据的情况包括迭代、序列化、与if合用
# 例如，当执行如下语句时，并未进行数据库查询，只是创建了一个查询集qs
# qs = Bookinfo.objects.all()
# 继续执行遍历迭代操作后，才真正的进行了数据库的查询
# for book in qs:
#     print(book.btitle)

# 2）缓存
# 使用同一个查询集，第一次使用时会发生数据库的查询，然后Django会把结果缓存下来，
# 再次使用这个查询集时会使用缓存的数据，减少了数据库的查询次数。

# 情况一：如下是两个查询集，无法重用缓存，每次查询都会与数据库进行一次交互，增加了数据库的负载。
# [book.id for book in Bookinfo.objects.all()]
# [book.id for book in Bookinfo.objects.all()]

# 情况二：经过存储后，可以重用查询集，第二次使用缓存中的数据。
# qs=BookInfo.objects.all()
# [book.id for book in qs]
# [book.id for book in qs]


# 3 限制查询集
# 可以对查询集进行取下标或切片操作，等同于sql中的limit和offset子句。
# 注意：不支持负数索引。
# 对查询集进行切片后返回一个新的查询集，不会立即执行查询。
# 如果获取一个对象，直接使用[0]，等同于[0:1].get()，但是如果没有数据，[0]引发IndexError异常，[0:1].get()如果没有数据引发DoesNotExist异常。

# 示例：获取第1、2项，运行查看。
# qs = Bookinfo.objects.all()[0:3]
# logging.error(qs)




""" 修改 """
# book = Bookinfo.objects.get(btitle='三国志', id=8)
# book.btitle = '三国志2'
# book.save()

# Bookinfo.objects.filter(btitle='三国志', id=10).update(btitle='三国志3')


""" 删除 """
# book = Bookinfo.objects.get(id=12)
# book.delete()

# Bookinfo.objects.filter(id=7).delete()


# 定义管理器
# qs = Bookinfo.books.all()
# logging.error(qs)
#
# book = Bookinfo.books.create_book("测试书籍ABCD", '1980-1-2')
# logging.error(book)