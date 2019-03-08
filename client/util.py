import uuid
import datetime

def get_sum_money(cartitems):
    sum_money = 0
    # 计算 选中商品的总价
    for i in cartitems.filter(is_select=True):
        sum_money += (i.num * i.goods.price)
    return round(sum_money, 2)


def get_order_number():
    uuid_str = uuid.uuid4().hex
    now_str = datetime.datetime.now().strftime("%Y%m%d%H%M")
    # 时间加上随机字符
    number = now_str + uuid_str[:20]
    return number
