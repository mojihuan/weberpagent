# coding: utf-8
import json
from common.base_api import BaseApi


class FuGjIlfCSrJ9s7EnIrE6z(BaseApi):
    """回收商管理|竞价成功订单"""

    def OZxk4qwYiumG(self, headers=None):
        """竞价成功订单"""
        headers = headers or self.headers['main']
        data = {"dateFrom": self.get_the_date(-30), "dateTo": self.get_the_date(), **self.get_page_params(), "bidStatus": "oss"}
        response = self.request_handle('post', self.urls['eiClrHsCQ'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'result.rows', list)
        self.make_pkl_file(res)
        return res


class WY8QLvmYcMdYngaZzAOE7(BaseApi):
    """回收商管理|参与竞价机器"""

    def OURlfeuAdIr8(self, headers=None):
        """参与竞价机器"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['jYu9aGPvE'], data=json.dumps(data),  headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class G3Vidy226qdUxoAgy1xMn(BaseApi):
    """回收商管理|手动竞价列表"""

    def G5Om5tN8OeQh(self, headers=None):
        """手动竞价列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['CTcDSS6w2'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = None
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
