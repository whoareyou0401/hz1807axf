from django.contrib.auth.models import AbstractUser
from django.db import models
from .choices import OREDER_STATUS
# Create your models here.
class MyUser(AbstractUser):
    icon = models.ImageField(
        upload_to="icon",
        verbose_name="头像"
    )


class Address(models.Model):
    detail = models.CharField(
        max_length=255,
        verbose_name="详细地址"
    )
    is_delete = models.BooleanField(
        default=False
    )
    is_default = models.BooleanField(
        default=True
    )
    user = models.ForeignKey(
        MyUser,
        null=True
    )
    class Meta:
        unique_together = ["user", "is_default"]
        index_together = ["user", "is_default"]


class BaseData(models.Model):
    img = models.CharField(
        max_length=255
    )
    name = models.CharField(
        max_length=60
    )
    trackid = models.CharField(
        max_length=40
    )
    class Meta:
        abstract = True

class Wheel(BaseData):
    class Meta:
        db_table = "axf_wheel"

class Nav(BaseData):
    class Meta:
        db_table = "axf_nav"

class MustBuy(BaseData):
    class Meta:
        db_table = "axf_mustbuy"

class Shop(BaseData):
    class Meta:
        db_table = 'axf_shop'

class MainShow(BaseData):
    categoryid = models.CharField(
        max_length=255
    )
    brandname = models.CharField(
        max_length=55
    )
    img1 = models.CharField(
        max_length=255
    )
    childcid1 = models.CharField(
        max_length=255
    )
    productid1 = models.CharField(
        max_length=255
    )
    longname1 = models.CharField(
        max_length=255
    )
    price1 = models.CharField(
        max_length=255
    )
    marketprice1 = models.CharField(
        max_length=20
    )

    img2 = models.CharField(
        max_length=255
    )
    childcid2 = models.CharField(
        max_length=255
    )
    productid2 = models.CharField(
        max_length=255
    )
    longname2 = models.CharField(
        max_length=255
    )
    price2 = models.CharField(
        max_length=255
    )
    marketprice2 = models.CharField(
        max_length=20
    )

    img3 = models.CharField(
        max_length=255
    )
    childcid3 = models.CharField(
        max_length=255
    )
    productid3 = models.CharField(
        max_length=255
    )
    longname3 = models.CharField(
        max_length=255
    )
    price3 = models.CharField(
        max_length=255
    )
    marketprice3 = models.CharField(
        max_length=20
    )

    class Meta:
        db_table = "axf_mainshow"

class Goods(models.Model):
    productid = models.CharField(
        max_length=20
    )
    productimg = models.CharField(
        max_length=200
    )
    productname = models.CharField(
        max_length=200,
        null=True
    )
    productlongname = models.CharField(
        max_length=200
    )
    isxf = models.BooleanField(
        default=0
    )
    pmdesc = models.BooleanField(
        default=0
    )
    specifics = models.CharField(
        max_length=20
    )
    price = models.FloatField()
    marketprice = models.FloatField()
    categoryid = models.IntegerField()
    childcid = models.IntegerField()
    childcidname = models.CharField(
        max_length=10
    )
    dealerid = models.CharField(
        max_length=20
    )
    storenums = models.IntegerField()
    productnum = models.IntegerField()

    def __str__(self):
        return str(self.price)

    class Meta:
        db_table = "axf_goods"


class Cart(models.Model):
    user = models.ForeignKey(
        MyUser,
        db_index=True
    )
    goods = models.ForeignKey(
        Goods
    )
    num = models.IntegerField(
        "购买的商品数量"
    )
    is_select = models.BooleanField(
        default=True,
        verbose_name="选中状态"
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="购物车的创建时间"
    )
    update_time = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间"
    )
    def __str__(self):
        return self.goods.productlongname

    __repr__ = __str__


class GoodsTypes(models.Model):
    typeid = models.CharField(
        max_length=40
    )
    typename = models.CharField(
        max_length=50
    )
    childtypenames = models.CharField(
        max_length=255
    )
    typesort = models.IntegerField()

    class Meta:
        db_table = "axf_foodtypes"


class ErrorLog(models.Model):
    msg = models.CharField(
        max_length=255,
        verbose_name="错误信息"
    )
    api_path = models.CharField(
        max_length=255,
        verbose_name="请求路径"
    )
    date = models.DateField(
        auto_now_add=True,
        verbose_name="错误发送时间"
    )

"""
订单表：

		字段：用户 订单号 状态（待付款，待发货， 待收货，待评价，完成）订单创建的时间 收货地址

	

"""
class Order(models.Model):
    user = models.ForeignKey(
        MyUser
    )
    number = models.CharField(
        "订单号",
        max_length=50,
    )
    status = models.IntegerField(
        choices=OREDER_STATUS,
        default=1
    )
    create_time = models.DateTimeField(
        "生成的时间",
        auto_now_add=True
    )
    address = models.ForeignKey(
        Address
    )

"""
订单详情表：
		字段：商品数量 商品 成交价格  订单id 
"""
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order
    )
    goods_num = models.IntegerField(
        "商品数量"
    )
    goods = models.ForeignKey(
        Goods
    )
    price = models.FloatField()
    desc = models.CharField(
        max_length=255,
        null=True
    )

