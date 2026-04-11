# coding: utf-8
import json
from common.base_api import BaseApi


class LaWjPQE8xRiQHRII3i9Bt(BaseApi):
    """商城管理|售后列表"""

    def KhRsCcqqbnRu(self, headers=None):
        """售后列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['qY7baS5Sq'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class BoKPsGPfTNvMGy8lEDfDK(BaseApi):
    """商城管理|网点管理"""

    def nNxpGKdNDGBb(self, headers=None):
        """网点管理"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['mnKICekG6'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class Eyfry1kHW3Ok17IyqXd1d(BaseApi):
    """商城管理|商品管理"""

    def W76ARi8VSxeK(self, headers=None):
        """商品管理 1上架中 2已销售 3已下架 4已退回"""
        headers = headers or self.headers['main']
        data = {'articlesState': 1, **self.get_page_params(), 'statusList': ['3', '4']}
        response = self.request_handle('post', self.urls['a7V6pHGg8'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = None
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
