# coding: utf-8
import json
from common.base_api import BaseApi


class Bp2sy8RGkznaP23ykw4u0(BaseApi):
    """报价管理|基础保价单"""

    def cZW5rexDrdV1(self, headers=None):
        """基础保价单"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['ZVeik6IID'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PHz1OOo3hU4WlsQVRPNdh(BaseApi):
    """报价管理|报价配置"""

    def riwuSwQ4o1tZ(self, headers=None):
        """报价配置"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['f9IDq1oH0'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class L853Yd28M6920mhkQf4PO(BaseApi):
    """报价管理|我的保价单"""

    def jrTYCZYoFYrx(self, headers=None):
        """我的保价单"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['AZNOjF7sK'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class Ip8MdffmRDeC08DW107an(BaseApi):
    """报价管理|报价记录"""

    def Cz6fNwj9NZkN(self, headers=None):
        """报价记录"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['SrR29G5El'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = None
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
