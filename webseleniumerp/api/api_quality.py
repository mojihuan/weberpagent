# coding: utf-8
import json
from common.base_api import BaseApi


class UJwDgUZKhNNEKJEIdEAKw(BaseApi):
    """质检管理|质检中物品"""

    def diFPISdg6WyC(self, headers=None, num=1, size=1000):
        """质检中物品"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['h0fUFo3xb'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class TzjKXVa7hC8j6pmsPJQvk(BaseApi):
    """质检管理|质检内容模版"""

    def WY9tdqjthqMp(self, headers=None):
        """质检内容模版"""
        headers = headers or self.headers['idle']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['zwgM8CxaW'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class Et8Xdyxf5FU41xsPtI5u4(BaseApi):
    """质检管理|质检统计数据"""

    def sT5RyqQrIQR6(self, headers=None):
        """质检统计数据"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "erpStartTime": self.get_the_date(-14), "erpEndTime": self.get_the_date()}
        response = self.request_handle('post', self.urls['quality_count'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class QyKIiWECv2ppl2UxZhwh3(BaseApi):
    """质检管理|质检记录列表"""

    def vAUM2VniBdJP(self, headers=None):
        """质检记录列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['ihdSAgrDn'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class LA8iNKfD36vwyHje5H9wF(BaseApi):
    """质检管理|质检统计数据"""

    def DKb7kmr8N1de(self, headers=None):
        """质检统计数据"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['fmrJZQngD'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class LNkpjm7bSdFieVvrwYNga(BaseApi):
    """质检管理|先质检后入库"""

    def rvPD6y5UvbdO(self, headers=None, i=None, num=1, size=1000):
        """非库内物品列表
        i: 1人工选择 2壹准验机app
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'type': i}
        response = self.request_handle('post', self.urls['VGVzFz3wR'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def i5eQu4jjL9ji(self, headers=None, num=1, size=1000):
        """非库内质检记录列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['GRw5uTFoq'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class DWK5kgL9TSp4zG8JsQVHs(BaseApi):
    """质检管理|质检模版管理"""

    def hSMikT30kdRk(self, headers=None):
        """质检模版管理"""
        headers = headers or self.headers['idle']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['r6W7daQiq'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class H7kEGXdRmBdMQh2h54JJr(BaseApi):
    """质检管理|待接收物品"""

    def PiUPtHf3A9kk(self, headers=None):
        """待接收物品列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "articlesState": 4, "articlesType": "1"}
        response = self.request_handle('post', self.urls['aLG4SFltS'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res

    def WvhOq9x8mCSL(self):
        """获取物品编号"""
        return self._get_field_copy_value('wait_turn_over_list', 'main', 'articlesNo')


class PYi7eKoJOr5suysXpCFvf(BaseApi):
    """质检管理|待移交物品"""

    def eJitQXxutgtJ(self, headers=None, num=1, size=1000):
        """待移交物品列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['aLG4SFltS'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = None
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
