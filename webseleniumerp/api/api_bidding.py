# coding: utf-8
import json
from api.api_platform import BaxRsHzRpoNsTb8fnSa9e, EEdalTouEaLL3VEx3wMnz
from common.base_api import BaseApi


class B1VzuYLyr5G9mdeT7BDwW(BaseApi):
    """拍机小程序|竞拍"""

    def __init__(self):
        super().__init__()
        self.obj = BaxRsHzRpoNsTb8fnSa9e()
        self.obj_2 = EEdalTouEaLL3VEx3wMnz()

    def QwNTfbys2CCL(self, headers=None):
        """竞拍列表 直拍"""
        obj = self.obj.gXHSWafumwCe()
        obj_2 = self.obj.oTwifIq7ER6o()
        headers = headers or self.headers['camera']
        data = {**self.get_page_params(), "marketId": obj[0]['id'], "orderByColumn": "create_time",
                "isAsc": "desc", "modelIdList": [], "finenessIdList": [], "articlesTypeId": "",
                "sessionId": obj_2[0]['id'], "marketCategory": "1", "isBidPrice": None}
        response = self.request_handle('post', self.urls['NDds92Jo6'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def Uf0OesfH65Pq(self, headers=None):
        """竞拍列表 暗拍"""
        obj = self.obj_2.pzCWj3Ksrd4P()
        obj_2 = self.obj_2.i2hsWJeCQxKo()
        headers = headers or self.headers['camera']
        data = {**self.get_page_params(), "marketId": obj[0]['id'], "orderByColumn": "create_time",
                "isAsc": "desc", "modelIdList": [], "finenessIdList": [], "articlesTypeId": "",
                "sessionId": obj_2[0]['id'], "marketCategory": "1", "isBidPrice": None}
        response = self.request_handle('post', self.urls['NDds92Jo6'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class UAPqxpSx1qiMwyQEcIPXb(BaseApi):
    """拍机小程序|我的"""

    def aKHpuJH4LWMe(self, headers=None, i=None):
        """我的购买
        i：订单状态 1待支付 2已支付 3已取消
        """
        headers = headers or self.headers['camera']
        data = {**self.get_page_params(), "orderStatus": i}
        response = self.request_handle('post', self.urls['q58fkMkFf'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def lbnWyhZHxWy3(self, headers=None, i=None):
        """我的包裹
        i：订单状态 1待收货 2已收货
        """
        headers = headers or self.headers['camera']
        data = {"packageState": i, 'sendType': None}
        response = self.request_handle('post', self.urls['gAAnohdPx'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def R0ylvsKYSTRn(self, headers=None, i=None):
        """商品列表
        i：订单状态 1待支付 2待发货 3待收货 4已收货  5已售后 6已取消
        """
        headers = headers or self.headers['camera']
        data = {"articlesStatus": i, **self.get_page_params()}
        response = self.request_handle('post', self.urls['kfM3W7bd1'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def DnyApTb8QiIk(self, headers=None, i=None):
        """退货售后列表
        i: 订单状态
        审核中：[1]线上审核 [11]实物复检 [10]待接收 [4]申诉中
        待处理：[7]待寄回 [6]可补差 [2]待申诉
        售后成功：[5]补差成功 [13]退货成功
        售后失败：[9]主动取消 [8]超时取消 [3]线上拒退 [12]实物拒退
        """
        headers = headers or self.headers['camera']
        data = {"afterStatusList": i, **self.get_page_params()}
        response = self.request_handle('post', self.urls['tkTyS52V5'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = B1VzuYLyr5G9mdeT7BDwW()
    result = api.QwNTfbys2CCL()
    print(json.dumps(result, indent=4, ensure_ascii=False))
