# coding: utf-8
import json
from common.base_api import BaseApi


class Vssd8T4BpUd8tbwsdelWv(BaseApi):
    """钱包管理|钱包中心"""

    def wgmOemddaPt6(self, headers=None):
        """钱包中心"""
        headers = headers or self.headers['main']
        data = {'orderStatus': 2, **self.get_page_params()}
        response = self.request_handle('post', self.urls['W1m9CQdZU'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def cCEgx5T9KbpZ(self):
        """获取钱包账号id"""
        return self._get_field_copy_value('wgmOemddaPt6', 'main', 'accountNo')

    def rBWq7DI98n6x(self):
        """获取钱包账号id"""
        return self._get_field_copy_value('wgmOemddaPt6', 'vice', 'accountNo')


class R8iWM0wvi9l16aL5WVUbW(BaseApi):
    """钱包管理|钱包订单列表"""

    def oJ5lEbrOf6ug(self, headers=None):
        """钱包订单列表-待付款"""
        headers = headers or self.headers['main']
        data = {'orderStatus': 1, **self.get_page_params()}
        response = self.request_handle('post', self.urls['wMYd9JgAw'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def oS6cf6cv3m8d(self, headers=None):
        """钱包订单列表-确认到款中"""
        headers = headers or self.headers['main']
        data = {'orderStatus': 2, **self.get_page_params()}
        response = self.request_handle('post', self.urls['wMYd9JgAw'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = None
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
