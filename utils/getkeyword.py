import jsonpath

"""
    获取json响应数据的关键字的值
"""


class GetKeyWord:
    @staticmethod
    def get_key_word(source_data, keyword):  # 获取首次出现的关键字的数据
        try:
            return jsonpath.jsonpath(source_data, f"$..{keyword}")[0]
        except Exception as e:
            print(f"关键字{keyword}不存在")
            print(e)
            return False

    @staticmethod
    def get_key_words(source_data, keyword):  # 获取所有的关键字的数据
        try:
            return jsonpath.jsonpath(source_data, f"$..{keyword}")
        except Exception as e:
            print(f"关键字{keyword}不存在")
            print(e)
            return False


if __name__ == '__main__':
    data = {'status_code': 200,
            'headers': {'Vary': 'Origin, Access-Control-Request-Method, Access-Control-Request-Headers',
                        'X-Content-Type-Options': 'nosniff', 'X-XSS-Protection': '1; mode=block',
                        'Cache-Control': 'no-cache, no-store, max-age=0, must-revalidate', 'Pragma': 'no-cache',
                        'Expires': '0', 'X-Frame-Options': 'DENY', 'Content-Type': 'application/json',
                        'Transfer-Encoding': 'chunked', 'Date': 'Sun, 12 Jun 2022 01:07:23 GMT',
                        'Keep-Alive': 'timeout=60', 'Connection': 'keep-alive'},
            'json': {'code': 200, 'message': '下单成功', 'data': {'orderItemList': [
                {'orderId': 236, 'orderSn': '202206120100000006', 'productId': 29,
                 'productPic': 'http://macro-oss.oss-cn-shenzhen.aliyuncs.com/mall/images/20180615/5acc5248N6a5f81cd.jpg',
                 'productName': 'Apple iPhone 8 Plus 64GB 红色特别版 移动联通电信4G手机', 'productBrand': '苹果',
                 'productSn': '7437799', 'productPrice': 6299.0, 'productQuantity': 1, 'productSkuId': 107,
                 'productSkuCode': '201808270029002', 'productCategoryId': 19, 'promotionName': '无优惠',
                 'promotionAmount': 0, 'couponAmount': 0, 'integrationAmount': 0, 'realAmount': 6299.0,
                 'giftIntegration': 5499, 'giftGrowth': 5499,
                 'productAttr': '[{"key":"颜色","value":"金色"},{"key":"容量","value":"64G"}]'}],
                                                              'order': {'id': 236, 'memberId': 19,
                                                                        'orderSn': '202206120100000006',
                                                                        'createTime': '2022-06-12T01:07:23.418+00:00',
                                                                        'memberUsername': 'yang', 'totalAmount': 6299.0,
                                                                        'payAmount': 6299.0, 'freightAmount': 0,
                                                                        'promotionAmount': 0, 'integrationAmount': 0,
                                                                        'couponAmount': 0, 'discountAmount': 0,
                                                                        'payType': 0, 'sourceType': 1, 'status': 0,
                                                                        'orderType': 0, 'autoConfirmDay': 15,
                                                                        'integration': 5499, 'growth': 5499,
                                                                        'promotionInfo': '无优惠', 'receiverName': '杨睿文',
                                                                        'receiverPhone': '13277968935',
                                                                        'receiverPostCode': '433100',
                                                                        'receiverProvince': '湖北省',
                                                                        'receiverCity': '武汉市', 'receiverRegion': '洪山区',
                                                                        'receiverDetailAddress': '保利时代3栋',
                                                                        'confirmStatus': 0, 'deleteStatus': 0}}},
            'time': 55.607}
    print((GetKeyWord.get_key_word(data, "orderSn")))
