# coding: utf-8
import json
from api.api_platform import PlatformListOfDirectAuctionHousesApi, PlatformListOfDarkAuctionHousesApi
from common.base_api import BaseApi


class BiddingCameraApi(BaseApi):
    """拍机小程序-竞拍"""

    def __init__(self):
        super().__init__()
        self.straight_shot = PlatformListOfDirectAuctionHousesApi()
        self.secret_shot = PlatformListOfDarkAuctionHousesApi()

    def zhi_auction_list(self, headers=None):
        """竞拍列表"""
        result = self.straight_shot.list_of_stores()
        result_2 = self.straight_shot.view_session_details()
        headers = headers or self.headers['camera']
        data = {**self.get_page_params(), "marketId": result[0]['id'], "orderByColumn": "create_time",
                "isAsc": "desc", "modelIdList": [], "finenessIdList": [], "articlesTypeId": "",
                "sessionId": result_2[0]['id'], "marketCategory": "1", "isBidPrice": None}
        response = self.request_handle('post', self.urls['auction_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def an_auction_list(self, headers=None):
        """竞拍列表"""
        result = self.secret_shot.list_of_dark_auction_houses()
        result_2 = self.secret_shot.view_session_details()
        headers = headers or self.headers['camera']
        data = {**self.get_page_params(), "marketId": result[0]['id'], "orderByColumn": "create_time",
                "isAsc": "desc", "modelIdList": [], "finenessIdList": [], "articlesTypeId": "",
                "sessionId": result_2[0]['id'], "marketCategory": "1", "isBidPrice": None}
        response = self.request_handle('post', self.urls['auction_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class BiddingMyApi(BaseApi):
    """拍机小程序-我的"""

    def auction_my_purchase_list(self, headers=None, i=None):
        """我的购买
        i：订单状态 1待支付 2已支付 3已取消
        """
        headers = headers or self.headers['camera']
        data = {**self.get_page_params(), "orderStatus": i}
        response = self.request_handle('post', self.urls['my_purchase'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def camera_my_package_list(self, headers=None, i=None):
        """我的包裹
        i：订单状态 1待收货 2已收货
        """
        headers = headers or self.headers['camera']
        data = {"packageState": i, 'sendType': None}
        response = self.request_handle('post', self.urls['camera_my_package'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def racket_product_list(self, headers=None, i=None):
        """商品列表
        i：订单状态 1待支付 2待发货 3待收货 4已收货  5已售后 6已取消
        """
        headers = headers or self.headers['camera']
        data = {"articlesStatus": i, **self.get_page_params()}
        response = self.request_handle('post', self.urls['racket_product_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def pat_machine_return_after_sales_list(self, headers=None, i=None):
        """退货售后列表
        i: 订单状态
        审核中：[1]线上审核 [11]实物复检 [10]待接收 [4]申诉中
        待处理：[7]待寄回 [6]可补差 [2]待申诉
        售后成功：[5]补差成功 [13]退货成功
        售后失败：[9]主动取消 [8]超时取消 [3]线上拒退 [12]实物拒退
        """
        headers = headers or self.headers['camera']
        data = {"afterStatusList": i, **self.get_page_params()}
        response = self.request_handle('post', self.urls['pat_machine_return_after_sales'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = BiddingCameraApi()
    result = api.an_auction_list()
    print(json.dumps(result, indent=4, ensure_ascii=False))
