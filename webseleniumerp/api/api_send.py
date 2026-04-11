# coding: utf-8
import json
from common.base_api import BaseApi


class QM4hD6LNhqKxZAitqFFJl(BaseApi):
    """送修管理|已送修物品"""

    def bkXQFPd3Pz5I(self, headers=None, num=1, size=1000):
        """已送修物品"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['plS4Pvb1M'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class MMuymWgzUDbCSdlZPeMMY(BaseApi):
    """送修管理|送修单列表"""

    def FaEsPLDSYo0I(self, headers=None, num=1, size=1000):
        """送修单列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['lrBhSwDJ0'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res



class O4WRo0dJF2emvqwRnFzMf(BaseApi):
    """送修管理|待接收物品"""

    def YqVnVVK1SIQq(self, headers=None):
        """待接收物品"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['BbtJmNsWL'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)

    def CPCfLFUgmSVV(self):
        """获取物品编号"""
        return self._get_field_copy_value('YqVnVVK1SIQq', 'main', 'articlesNo')


if __name__ == '__main__':
    api = ()
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
