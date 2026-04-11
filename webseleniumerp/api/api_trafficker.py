# coding: utf-8
import json
from common.base_api import BaseApi


class VfTkevwpodNhL42zHU3dx(BaseApi):
    """二手通小程序|首页"""

    def D2k1drVu2N1e(self, headers=None):
        """帮卖列表 帮卖上架列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "listType": 0, "entryType": 1}
        response = self.request_handle('post', self.urls['R9KURc37p'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def uPKv8yuxu7KE(self, headers=None):
        """一键帮卖 帮卖清单"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['Ol7sHS12i'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def SMw7DJm83xsG(self, headers=None):
        """库存盘点 库存盘点列表"""
        headers = headers or self.headers['main']
        data = {"stockNo": "", "maxBehotTime": "", "startTime": "", "endTime": ""}
        response = self.request_handle('post', self.urls['eIaBtZRsg'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)

    def lYg2j57m1KBq(self, headers=None):
        """物流列表 物流列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['VRAiYmFWf'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def FOKJDIottLep(self, headers=None):
        """采购订单 采购订单列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['ES1m5P2yR'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def cc9d3eoQODGd(self, headers=None):
        """物品质检 物品质检列表"""
        headers = headers or self.headers['main']
        data = {"imeiOrNo": ""}
        response = self.request_handle('post', self.urls['mtwBAziua'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def t6NP6wsidTkw(self, headers=None):
        """物品维修 物品维修列表"""
        headers = headers or self.headers['main']
        data = {"imeiOrNo": ""}
        response = self.request_handle('post', self.urls['ftMaom67y'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res

    def afgFyCfi7BYQ(self, headers=None):
        """维修记录 维修记录列表"""
        headers = headers or self.headers['main']
        data = {"imeiOrNo": ""}
        response = self.request_handle('post', self.urls['FyUjIjfix'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res

    def xAQc5dlPVSjv(self, headers=None):
        """销售订单 销售订单列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['oMg0yCVbP'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class SMuBZZVIBpz3FpTfyxc5X(BaseApi):
    """二手通小程序|统计"""

    def xCTpclrHollM(self, headers=None):
        """业务统计"""
        headers = headers or self.headers['main']
        response = self.request_handle('get', self.urls['BT72VcbCF'], headers=headers)
        return self.get_response_data(response, 'data', dict)

    def TVCgbuZkcjep(self, headers=None):
        """采购统计"""
        headers = headers or self.headers['main']
        today = self.get_the_date()
        data = {"startTime": today, "endTime": today}
        response = self.request_handle('post', self.urls['yR6YDXTh8'], data=json.dumps(data),       headers=headers)
        return self.get_response_data(response, 'data', dict)

    def FqssvItwBC9O(self, headers=None):
        """销售统计"""
        headers = headers or self.headers['main']
        today = self.get_the_date()
        data = {"startTime": today, "endTime": today}
        response = self.request_handle('post', self.urls['tkkORJo11'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)


if __name__ == '__main__':
    api = ()
    res = api
    print(res)
