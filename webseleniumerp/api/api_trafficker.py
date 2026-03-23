# coding: utf-8
import json
from common.base_api import BaseApi


class TraffickerIndexApi(BaseApi):
    """首页"""

    def help_sell_listings_list(self, headers=None):
        """帮卖列表 帮卖上架列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "listType": 0, "entryType": 1}
        response = self.request_handle('post', self.urls['help_sell_listings_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def help_sell_list(self, headers=None):
        """一键帮卖 帮卖清单"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['help_sell_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def inventory_count_list(self, headers=None):
        """库存盘点 库存盘点列表"""
        headers = headers or self.headers['main']
        data = {"stockNo": "", "maxBehotTime": "", "startTime": "", "endTime": ""}
        response = self.request_handle('post', self.urls['mg_inventory_count'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)

    def logistics_list_list(self, headers=None):
        """物流列表 物流列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['logistics_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def purchase_order_list(self, headers=None):
        """采购订单 采购订单列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['purchase_order'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def quality_inspection_list(self, headers=None):
        """物品质检 物品质检列表"""
        headers = headers or self.headers['main']
        data = {"imeiOrNo": ""}
        response = self.request_handle('post', self.urls['quality_inspection'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def item_repair_list(self, headers=None):
        """物品维修 物品维修列表"""
        headers = headers or self.headers['main']
        data = {"imeiOrNo": ""}
        response = self.request_handle('post', self.urls['item_repair'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res

    def repair_record_list(self, headers=None):
        """维修记录 维修记录列表"""
        headers = headers or self.headers['main']
        data = {"imeiOrNo": ""}
        response = self.request_handle('post', self.urls['mg_repair_record'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res

    def sell_order_list(self, headers=None):
        """销售订单 销售订单列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['sell_order'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class TraffickerStaticsApi(BaseApi):
    """首页|统计"""

    def business_statics(self, headers=None):
        """业务统计"""
        headers = headers or self.headers['main']
        response = self.request_handle('get', self.urls['business_statistics'], headers=headers)
        return self.get_response_data(response, 'data', dict)

    def purchase_statistics(self, headers=None):
        """采购统计"""
        headers = headers or self.headers['main']
        today = self.get_the_date()
        data = {"startTime": today, "endTime": today}
        response = self.request_handle('post', self.urls['purchase_statistics'], data=json.dumps(data),
                                       headers=headers)
        return self.get_response_data(response, 'data', dict)

    def sell_statistics(self, headers=None):
        """销售统计"""
        headers = headers or self.headers['main']
        today = self.get_the_date()
        data = {"startTime": today, "endTime": today}
        response = self.request_handle('post', self.urls['sell_statistics'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)


if __name__ == '__main__':
    api = TraffickerStaticsApi()
    res = api.business_statics()
    print(res)
