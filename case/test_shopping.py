"""
购物车流程
"""
from interface.Shoppinginterface import ShoppingInterface
from utils.Mysql import Mysql
from utils.getkeyword import GetKeyWord
import pytest


class TestShopping:
    # 添加购物车
    def test_add_shopping_cart(self):
        body = {
            "createDate": "2022-06-11T04:42:44.785Z",  # 创建时间
            "deleteStatus": 0,  # 是否删除
            "id": 0,  # 购物车记录id
            "memberId": 19,  # 会员id
            "memberNickname": "yang",  # 会员username
            "modifyDate": "2022-06-11T04:42:44.785Z",  # 修改时间
            "price": 6299,  # 商品价格
            "productAttr": '[{"key":"颜色","value":"金色"},{"key":"容量","value":"64G"}]',  # 商品属性  # 商品库存表(pms_sku_stock)
            "productBrand": "苹果",  # 商品品牌 # 商品表中 (pms_product)
            "productCategoryId": 19,  # 产品类别ID # 商品表中 (pms_product)
            "productId": 29,  # 产品ID # 商品库存表(pms_sku_stock)
            "productName": "Apple iPhone 8 Plus 64GB 红色特别版 移动联通电信4G手机",  # 产品名称 # 商品表中 (pms_product)
            "productPic": "http://macro-oss.oss-cn-shenzhen.aliyuncs.com/mall/images/20180615/5acc5248N6a5f81cd.jpg",
            # 商品的pic
            "productSkuCode": "201808270029002",
            "productSkuId": 107,
            "productSn": "7437799",
            "productSubTitle": "【限时限量抢购】Apple产品年中狂欢节，好物尽享，美在智慧！速来 >> 勾选[保障服务][原厂保2年]，获得AppleCare+全方位服务计划，原厂延保售后无忧。",
            "quantity": 1
        }
        # 发送请求
        ShoppingInterface().add_shopping_cart(body)
        # 断言最新的 购物车 信息是否为空
        pytest.assume(Mysql.extract_mysql("SELECT id FROM oms_cart_item WHERE member_id= 19 ;")[-1] is not None)

    # 确认订单
    def test_confirm_order(self):
        data = [
            # 获取最新的 订单ID
            Mysql.extract_mysql("SELECT id FROM oms_cart_item WHERE member_id= 19;")[-1][0]
        ]
        rqs = ShoppingInterface().confirm_order(data)  # 发送请求
        num1 = int(GetKeyWord.get_key_word(rqs, 'payAmount'))  # 实付金额
        num2 = int(GetKeyWord.get_key_word(rqs, 'promotionAmount'))  # 优惠金额
        num3 = int(GetKeyWord.get_key_word(rqs, 'freightAmount'))  # 运费
        num4 = int(GetKeyWord.get_key_word(rqs, 'price'))  # 商品单价
        num5 = int(GetKeyWord.get_key_word(rqs, 'quantity'))  # 件数
        # 实付金额= 商品单价 * 件数 + 运费 - 优惠金额
        assert num4 * num5 + num3 - num2 == num1
        # 断言 总金额 是否和 返回数据一致
        pytest.assume(num4 * num5 + num3 - num2 == num1)
        # 断言 商品列表是否为空
        commodity_list = GetKeyWord.get_key_word(rqs, "cartPromotionItemList")
        pytest.assume(commodity_list is not None)
        # 断言 地址是否为空
        address = GetKeyWord.get_key_word(rqs, "memberReceiveAddressList")
        pytest.assume(address is not None)

    # 生成订单
    def test_generate_order(self):
        data = {
            "cartIds": [
                # 获取最新的 订单ID
                str(Mysql.extract_mysql("SELECT id,delete_status FROM oms_cart_item WHERE member_id= 19;")[-1][0])
            ],
            "memberReceiveAddressId": 24,  # 快递 ID
            "payType": 0,
        }
        rqs = ShoppingInterface().generate_order(data)  # 发送请求
        # 断言 SQL最新的订单号 是否和 返回的订单号相等
        sql_02 = Mysql.extract_mysql("SELECT id,order_sn,status FROM oms_order WHERE member_id= 19 ;")
        newest_order = sql_02[-1][1]  # 获取最新的 订单号
        pytest.assume(int(GetKeyWord.get_key_word(rqs, "orderSn")) == int(newest_order))  # 断言最新的订单号是否和返回的订单号相等
        # 断言 订单SQL里面的 status 是否等于0
        newest_status = sql_02[-1][2]  # 获取最新订单号的 status
        pytest.assume(newest_status == 0)
        # 断言 delete_status 是否等于 1
        newest_delete_status = Mysql.extract_mysql("SELECT id,delete_status FROM oms_cart_item WHERE member_id= 19;")[-1][1]  # 获取最新的 delete_status
        pytest.assume(newest_delete_status == 1)

    # 支付成功回调
    def test_paySuccess(self):
        stock = Mysql.extract_mysql("SELECT stock FROM pms_sku_stock WHERE id= 107;")[-1][0]  # 获取最新的 库存数值
        # 返回为 int 数据  获取最新的订单 ID
        shopping_id = int(Mysql.extract_mysql("SELECT id FROM oms_order WHERE member_id= 19 ;")[-1][0])
        # 发送响应
        rqs = (ShoppingInterface().paySuccess(str(shopping_id), '1'))
        # 断言 返回数据是否是支付成功
        assert GetKeyWord.get_key_word(rqs, "message") == "支付成功"
        # 获取 status 数据 断言
        assert Mysql.extract_mysql("SELECT id,status FROM oms_order WHERE member_id= 19 ;")[-1][1] == 1
        # 断言 支付完成后库存是否会减少
        newest_stock = Mysql.extract_mysql("SELECT stock FROM pms_sku_stock WHERE id= 107;")[-1][0]  # 获取支付完成后的库存数值
        assert stock == newest_stock + 1
