from interface.MemberInterface import MemberInterface
from utils.Mysql import Mysql
from utils.sendmethod import SendMethod


class ShoppingInterface:
    def __init__(self):
        self.url = "http://47.108.206.100:8085"
        self.headers = MemberInterface().get_member_token("yang", "123456")

    # 添加购物车
    def add_shopping_cart(self, body):
        method = "post"
        url = self.url + "/cart/add"
        return SendMethod.send_method(method, url, json=body, headers=self.headers)

    # 确认订单
    def confirm_order(self, data):
        method = "post"
        url = self.url + "/order/generateConfirmOrder"
        return SendMethod.send_method(method, url, json=data, headers=self.headers)

    # 生成订单
    def generate_order(self, data):
        method = "post"
        ulr = self.url + "/order/generateOrder"
        return SendMethod.send_method(method, ulr, json=data, headers=self.headers)

    # 添加地址
    def add_address(self, data):
        method = "post"
        ulr = self.url + "/member/address/add"
        return SendMethod.send_method(method, ulr, json=data, headers=self.headers)

    # 支付成功回调
    def paySuccess(self, orderid, paytype):
        method = "post"
        url = self.url + "/order/paySuccess"
        data = {
            "orderId": orderid,
            "payType": paytype,
        }
        return SendMethod.send_method(method, url, data=data, headers=self.headers)


if __name__ == '__main__':
    sql = Mysql.extract_mysql("SELECT id FROM oms_cart_item WHERE member_id= 19;")
    shopping_cart_id = sql[-1][0]  # 获取最新的 订单ID
    data = [
        shopping_cart_id
    ]
    print(shopping_cart_id)
    print(data)