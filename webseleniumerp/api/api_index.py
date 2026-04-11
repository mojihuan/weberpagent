# coding: utf-8
import json
from common.base_api import BaseApi


class L0sVKV0pYqiMgKqqjdRDv(BaseApi):
    """首页|待办物品"""

    def w6HTj34LlvdB(self, headers=None):
        """待办物品"""
        headers = headers or self.headers['main']
        response = self.request_handle('post', self.urls['SGWQ5u9Os'], data=json.dumps({}), headers=headers)
        return self.get_response_data(response, 'data', dict)

    def tDRq1x0ViY4u(self, headers=None):
        """今日数据"""
        headers = headers or self.headers['main']
        response = self.request_handle('post', self.urls['HrrU6KAEV'], data=json.dumps({}), headers=headers)
        return self.get_response_data(response, 'data', dict)

    def QcM91hDHTaD0(self, headers=None):
        """预估物品到货时效"""
        headers = headers or self.headers['main']
        response = self.request_handle('post', self.urls['TAy2kTtNx'], data=json.dumps({}), headers=headers)
        return self.get_response_data(response, 'data', dict)


class INBsa7uXWvRflmozMyZ7Y(BaseApi):
    """首页|个人中心"""

    def rI0La6FxSuFu(self, headers=None):
        """个人中心"""
        headers = headers or self.headers['main']
        response = self.request_handle('get', self.urls['qKbwUThei'], headers=headers)
        return self.get_response_data(response, 'user', dict)

    def GpbSEHCemdpy(self):
        return self._get_field_copy_value('rI0La6FxSuFu', 'main', 'nickName')


if __name__ == '__main__':
    api = None
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
