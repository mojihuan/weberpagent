# coding: utf-8
import json
from common.base_api import BaseApi


class J2Dfh2036O8m8ti5cojOh(BaseApi):
    """消息管理|消息中心"""

    def LGKmg1HSVZPu(self, headers=None):
        """回收商发布"""
        headers = headers or self.headers['main']
        data = {"messageParentClass": "1", **self.get_page_params()}
        response = self.request_handle('post', self.urls['GP4arTtYi'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def GdYOuX4yaIlv(self, headers=None):
        """商品交易"""
        headers = headers or self.headers['main']
        data = {"messageParentClass": "2", **self.get_page_params()}
        response = self.request_handle('post', self.urls['GP4arTtYi'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def HF2jlp9c9WKD(self, headers=None):
        """推送公告"""
        headers = headers or self.headers['main']
        data = {"messageParentClass": "3", **self.get_page_params()}
        response = self.request_handle('post', self.urls['GP4arTtYi'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class KxO3PKRgVuNDVjQUSHVcl(BaseApi):
    """消息管理|消息发布列表"""

    def qTd9V34NC3MZ(self, headers=None):
        """消息发布列表"""
        headers = headers or self.headers['main']
        data = {"selectType": "2", **self.get_page_params()}
        response = self.request_handle('post', self.urls['W6umEZcEP'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def XCsOUJ3AgR1a(self, headers=None):
        """消息发送记录"""
        headers = headers or self.headers['main']
        data = {"selectType": "1", **self.get_page_params()}
        response = self.request_handle('post', self.urls['HZMOLhjZL'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = None
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
