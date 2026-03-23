# coding: utf-8
import json
from common.base_api import BaseApi


class IndexStaticsApi(BaseApi):
    """首页|待办物品"""

    def index_statics(self, headers=None):
        """首页-待办物品"""
        headers = headers or self.headers['main']
        response = self.request_handle('post', self.urls['index_statics'], data=json.dumps({}), headers=headers)
        return self.get_response_data(response, 'data', dict)

    def index_today(self, headers=None):
        """首页-今日数据"""
        headers = headers or self.headers['main']
        response = self.request_handle('post', self.urls['index_today'], data=json.dumps({}), headers=headers)
        return self.get_response_data(response, 'data', dict)

    def logistics_data(self, headers=None):
        """首页-预估物品到货时效"""
        headers = headers or self.headers['main']
        response = self.request_handle('post', self.urls['logistics_data'], data=json.dumps({}), headers=headers)
        return self.get_response_data(response, 'data', dict)


class UserInfoApi(BaseApi):
    """首页|个人中心"""

    def user_center(self, headers=None):
        """个人中心"""
        headers = headers or self.headers['main']
        response = self.request_handle('get', self.urls['user_center'], headers=headers)
        return self.get_response_data(response, 'user', dict)

    def get_(self):
        return self._get_field_copy_value('user_center', 'main', 'nickName')


if __name__ == '__main__':
    api = None
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
