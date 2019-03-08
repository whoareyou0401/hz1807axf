from django.contrib.auth import authenticate, login
from django.http import JsonResponse, QueryDict
from django.urls import reverse
from django.views import View
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CartSerializer
from .authentications import LoginAuthentication
from .util import get_sum_money

from .models import *


class LoginAPI(View):

    def post(self, req):
        # 解析参数
        u_name = req.POST.get("uname")
        pwd = req.POST.get("pwd")
        # 校验数据
        if u_name and len(u_name)>=3:
            # 校验用户
            user = authenticate(username=u_name, password=pwd)
            #进行登录
            if user:
                login(req, user)
                # 返回跳转位置
                data = {
                    "code": 0,
                    "msg": "ok",
                    "data": reverse("axf:mine")
                }
                return JsonResponse(data)
            else:
                data = {
                    "code": 1,
                    "msg": "用户名或密码错误"
                }
                return JsonResponse(data)
        else:
            data = {
                "code": 1,
                "msg": "用户名过短"
            }
            return JsonResponse(data)


class RegisterAPI(View):

    def post(self, req):
        # 解析参数
        username = req.POST.get("username")
        pwd = req.POST.get("pwd")
        confirm_pwd = req.POST.get("confirm_pwd")
        email = req.POST.get("email")
        icon = req.FILES.get("icon")
        #校验数据的合法性
        if username and len(username) >= 3 and pwd and pwd == confirm_pwd:
            # 校验用户名是否可用
            if MyUser.objects.filter(username=username).exists():
                data = {
                    "code": 1,
                    "msg": "此账户已经被注册"
                }
                return JsonResponse(data)
            # 创建用户
            user = MyUser.objects.create_user(
                username=username,
                email=email,
                is_active=False,
                password=pwd,
                icon=icon
            )
        # 发送激活邮件  自己写 激活连接
        #     send_verify_mail(user)
        # 跳转到登录页面
            data = {
                "code": 0,
                "data": reverse("axf:login")
            }
            return JsonResponse(data)

"""
           1 要知道是谁

			2 事件（加操作） 哪个商品 数量（我们这里是一个）

			3 在加购物车要判断库存

			4 添加购物车的数据

"""

class ItemCartAPI(CreateAPIView, UpdateAPIView):
    queryset = Cart.objects.all()
    authentication_classes = [LoginAuthentication]
    serializer_class = CartSerializer
    def post(self, request, *args, **kwargs):
        # 允许修改我们的请求参数


        user = request.user
        # 判断用户时候登录
        if not user:
            res = {
                "msg": "not login",
                "code": 1,
                "data": reverse("axf:login")
            }
            return Response(res)
        request.data._mutable = True
        # 为了满足我们序列化器的字段需求
        request.data["user"] = user.id
        request.data._mutable = False
        # 获取商品
        goods_id = request.data.get("goods")
        goods = Goods.objects.get(pk=goods_id)
        num = int(request.data.get("num"))
        # 判断库存
        if num > goods.storenums:
            res = {
                "code": 2,
                "msg": "商品库存不足",
                "data": None
            }
            return Response(res)
        cart_items = Cart.objects.filter(
            user=user,
            goods_id=goods_id
        )
        # 如果不是第一次添加 那就修改对应的数据的商品数量
        if cart_items.exists():
            cart_item = cart_items.first()
            cart_item.num += int(num)
            cart_item.save()
            res = {
                "code": 0,
                "msg": "OK",
                "data": self.get_serializer(cart_item).data
            }
            return Response(res)
        else:
            serializer = self.get_serializer(data=request.data)

            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            res = {
                "code": 0,
                "msg": "OK",
                "data": serializer.data
            }
            return Response(res, status=status.HTTP_201_CREATED, headers=headers)

    def put(self, request, *args, **kwargs):
        user = request.user
        # 判断用户时候登录
        if not user:
            res = {
                "msg": "not login",
                "code": 1,
                "data": reverse("axf:login")
            }
            return Response(res)
        request.data._mutable = True
        num = int(request.data.get("num"))
        if num < 1:
            res = {
                "code": 1,
                "msg": "数量不合法",
                "data":""
            }
            return Response(res)
        cart_data = Cart.objects.get(user_id=user.id, goods_id=request.data.get("goods"))
        cart_num = 0
        # 修改商品的数量
        cart_data.num -= num
        # 判断数量是不是等于0了
        if cart_data.num == 0:
            cart_data.delete()
        else:
            # 如果没减到0就保存数据
            cart_data.save()
            cart_num = cart_data.num
        res = {
            "code": 0,
            "msg": "ok",
            "data": cart_num
        }
        return Response(res)


class CartItemStatusAPI(View):

    def put(self, request):
        """
        1 解析参数（用户， 购物车的ID）

		2 将购物车数据的选中状态置反

		3 判断全选状态

		4 计算总价

		5 返回结果

        :param request:
        :return:
        """
        params = QueryDict(request.body)
        user = request.user
        cart_id = params.get("cid")
        cart_item = Cart.objects.get(pk=cart_id)
        # 2 将购物车数据的选中状态置反
        cart_item.is_select = not cart_item.is_select
        cart_item.save()

        #  3 判断全选状态
        is_select_all= True
        cart_items = Cart.objects.filter(user=user)
        if cart_items.filter(is_select=False).exists():
            is_select_all = False
#         算钱
        money = get_sum_money(cart_items)
#         返回结果
        res = {
            "code": 0,
            "msg": "ok",
            "data":{
                "current_item_status": cart_item.is_select,
                "is_select_all": is_select_all,
                "money": money
            }
        }
        return JsonResponse(res)


def cart_data_status_api(request):
#     获取用户
    user = request.user
    if not user.is_authenticated:
        raise Exception("您未登录")
#     判断操作的动作
    carts = Cart.objects.filter(user_id=user.id)
    # 保证购物车有数据
    if not carts.exists():
        raise Exception("您购物车暂无商品，请去购物")
    # 判断我们的操作
    is_select_all = carts.filter(is_select=False).exists()

    # 存在没选中的数据------>将商品全都选中
    carts.update(is_select=is_select_all)

#     算钱
    sum_money = get_sum_money(carts) if is_select_all else 0
    res = {
        "code":0,
        "msg":"OK",
        "data": {
            "is_select_all":is_select_all,
            "sum_money": sum_money
        }
    }
    return JsonResponse(res)


class CartDataOptionAPI(View):
    """
    1 校验登录 获取购物车数据ID

	2 拿到这个ID对应的购物车数据

	3 更新数量

	4 计算总价

	5 返回结果

    """
    def put(self, req):
        params = QueryDict(req.body)
        user = req.user
        if not user.is_authenticated:
            raise Exception("请先登录")
        # 拿到这个ID对应的购物车数据
        cart_data = Cart.objects.get(pk=params.get("cid"))
        # 判断操作 加 还是 减
        option = params.get("option")
        if option == "add":
        #     执行加操作
            cart_data.num += 1
            cart_data.save()

        else:
            # 执行减操作
            cart_data.num -= 1
            if cart_data.num == 0:
                cart_data.delete()
            else:
                cart_data.save()

        # 算总价
        cart_items = Cart.objects.filter(user=user)
        sum_money = get_sum_money(cart_items)

        is_select_all = (not cart_items.filter(is_select=False).exists()) and cart_items.exists()


        # 返回结果
        res = {
            "code": 0,
            "msg": "OK",
            "data": {
                "sum_money": sum_money,
                "current_num": cart_data.num,
                "is_select_all": is_select_all
            }
        }
        return JsonResponse(res)


class OrderItemAPI(DestroyAPIView):
    queryset = OrderItem.objects.filter(order__status=1)
    authentication_classes = [LoginAuthentication]
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        # 计算总价
        order_id = request.data.get("order_id")
        order_items = self.queryset.filter(order__number=order_id)
        sum_money = 0
        for i in order_items:
            sum_money += (i.goods_num * i.price)
        res = {
            "code": 0,
            "msg": "OK",
            "data": {
                "sum_money": sum_money
            }
        }
        return Response(res)
