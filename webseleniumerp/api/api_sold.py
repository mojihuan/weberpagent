# coding: utf-8
import json
from common.base_api import BaseApi


class MJx9y5FhH7uORtcUnKq9n(BaseApi):
    """同售管理|闲鱼严选|闲鱼订单列表"""

    def V3i4khEjsgpN(self, headers=None):
        """闲鱼订单列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['S8W01P7pW'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class U2ksfnNMVlCR1wSX0oSaK(BaseApi):
    """同售管理|闲鱼严选|闲鱼商品列表"""

    def q7kbPkQI6isS(self, headers=None):
        """闲鱼商品列表"""
        headers = headers or self.headers['main']
        data = {'platformType': 1, **self.get_page_params()}
        response = self.request_handle('post', self.urls['RKlPU68TX'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class YojCy7cNjPbvgLorVzofY(BaseApi):
    """同售管理|闲鱼严选|闲鱼售后列表"""

    def B5jsRmeuozvP(self, headers=None):
        """闲鱼售后列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "platformType": 1}
        response = self.request_handle('post', self.urls['VgC5IF64v'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class IoioQDiVvRYIs7babfELd(BaseApi):
    """同售管理|得物95分|95商品列表"""

    def cc4GJBAYY1cI(self, i=None, headers=None):
        """95商品列表
         i：物品状态 3已发布 2发布失败
        """
        headers = headers or self.headers['main']
        data = {'platformType': 2, **self.get_page_params(), "goodsStatus": i}
        response = self.request_handle('post', self.urls['RKlPU68TX'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class N76dJG67fEenMyyntUYj1(BaseApi):
    """同售管理|得物95分|订单列表"""

    def xuW99SzDwFia(self, headers=None):
        """95订单列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['ZKaV2J73s'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class C0Y7dl9PySZXOEwQmgSYI(BaseApi):
    """同售管理|得物95分|回退列表"""

    def uLGPDLGbQRqt(self, headers=None):
        """95回退列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['QiTxMEtLA'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class ZL8TGRq6O328uDu1xYGAT(BaseApi):
    """同售管理|得物95分|售后列表"""

    def MxNZ29OziHdP(self, headers=None):
        """95售后列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "platformType": 2}
        response = self.request_handle('post', self.urls['VgC5IF64v'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = None
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
