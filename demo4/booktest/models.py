from datetime import date

from django.db import models

# Create your models here.


# 图书管理器


# 自定义管理器
# 我们可以自定义管理器，并应用到我们的模型类上。
# 注意：一旦为模型类指明自定义的过滤器后，Django不再生成默认管理对象objects。
# 自定义管理器类主要用于两种情况：
# 1. 修改原始查询集，重写all()方法。
#  在管理器类中补充定义新的方法
# class BookInfoManager(models.Manager):
#     """ 自定义模型管理类，就相当于objects """
#
#     def all(self):
#         # 默认查询未删除的图书信息
#         # 调用父类的成员语法为：super().方法名
#         return super().filter(is_delete=False)
#
#     #  创建模型类,接收参数为属性赋值
#     def create_book(self, title, pub_date):
#         # 创建模型类对象self.model可以获得模型类
#         book = self.model()
#         book.btitle = title
#         book.bpub_date = pub_date
#         book.bread = 0
#         book.bcomment = 0
#         book.is_delete = False
#
#         # 将数据插入进数据库
#         book.save()
#         return book

class Bookinfo(models.Model):

    # 自定义模型管理类，如果自定义后，原本objects，就不能用
    # books = BookInfoManager()

    """ 图书模型 """
    btitle = models.CharField(max_length=20, verbose_name="书名")
    bpub_date = models.DateField(verbose_name="发布日期")
    bread = models.IntegerField(default=0, verbose_name="阅读量")
    bcomment = models.IntegerField(default=0, verbose_name="评论")
    is_delete = models.BooleanField(default=False, verbose_name="逻辑删除")
    # 如果模型已经迁移，并且表中已经有数据时，后追加的字段必须给默认值或者可以为空，不然迁移报错
    # 迁移命令: 1. python manage.py makemigrations
    #          2. python manage.py migrate
    image = models.ImageField(upload_to='books', null=True, verbose_name='图片')

    class Meta:
        db_table = "tb_books"  # 自定义表的名字
        verbose_name = "图书"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.btitle

    def bread_unit(self):
        return "%d个" % self.bread
    bread_unit.short_description = "阅读量"  # 自定义显示名字
    bread_unit.admin_order_field = 'bread'  # 此方法依据那个字段进行排序

    def hero_list(self):
        return list(self.heroinfo_set.all())
    hero_list.short_description = "英雄"
    hero_list.admin_order_field = 'heroinfo__id'

    def pub_date(self):
        return self.bpub_date.strftime('%Y-%m-%d')
    pub_date.short_description = '发布日期'
    pub_date.admin_order_field = 'bpub_date'


# 定义英雄模型类HeroInfo
class HeroInfo(models.Model):
    # 枚举
    GENDER_CHOICES = (
        (0, 'female'),
        (1, 'male')
    )
    hname = models.CharField(max_length=20, verbose_name="名称")
    hgender = models.SmallIntegerField(choices=GENDER_CHOICES, default=0, verbose_name="性别")
    hcomment = models.CharField(max_length=200, null=True, verbose_name="描述信息")
    hbook = models.ForeignKey(Bookinfo, on_delete=models.CASCADE, verbose_name="图书")
    is_delete = models.BooleanField(default=False, verbose_name="逻辑删除")

    class Meta:
        db_table = "tb_heros"
        verbose_name = "英雄"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.hname


