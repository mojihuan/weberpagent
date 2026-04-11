# coding: utf-8
import json
from common.base_api import BaseApi


class ZpUG9P3oxkPb5GFqBrxGQ(BaseApi):
    """拍机管理|售后管理|售后订单"""

    def Hz8EMlxg5WBm(self, headers=None):
        """售后订单列表"""
        headers = headers or self.headers['camera']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['wngYpEYbo'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class Z4B1h5YLGNro3dwGrXQhF(BaseApi):
    """拍机管理|拍机场次列表"""

    def ZuIQQpaDevaL(self, headers=None):
        """拍机场次列表"""
        headers = headers or self.headers['camera']
        data = {**self.get_page_params(), 'listType': "1"}
        response = self.request_handle('post', self.urls['Q1sdcYxeD'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def nOhPEhCFHgIT(self, headers=None):
        """查看场次商品"""
        obj = self.m80jkwjQfMFY()
        headers = headers or self.headers['camera']
        data = {**self.get_page_params(), 'sessionId': obj}
        response = self.request_handle('post', self.urls['gOqcWJomd'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)

    def m80jkwjQfMFY(self):
        """获取id"""
        return self._get_field_copy_value('ZuIQQpaDevaL', 'camera', 'id')


if __name__ == '__main__':
    api = ()
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
