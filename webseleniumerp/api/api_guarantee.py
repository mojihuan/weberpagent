# coding: utf-8
import json
from common.base_api import BaseApi


class BAc7o7mzTE8oACvyeArJW(BaseApi):
    """保卖管理|订单列表"""

    def PoY7iA7QafwP(self, i=None, headers=None):
        """订单列表
         i：订单状态 1待发货 2待取件 3待收货 4已收货 5已完成 6已取消 7已退货
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'status': i}
        response = self.request_handle('post', self.urls['iKeQQFmFF'], data=json.dumps(data),    headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def v6lgcdrrB6rn(self, headers=None):
        """物品列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['wKFkRVWzm'], data=json.dumps(data),      headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class TD9Y1EebwgkWWw4gbKGII(BaseApi):
    """保卖管理|退货管理"""

    def MTU290s6GvCd(self, i=None, headers=None):
        """物品明细列表
         i：订单状态 1待退货 2待取货 3退货已出库 4已退货 5已取消
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'status': i}
        response = self.request_handle('post', self.urls['J7GarZ0Mm'], data=json.dumps(data),  headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def BxBcWC50E2qm(self, i=None, headers=None):
        """批次明细列表
         i：订单状态 1待退货 2待取货 3退货已出库 4已退货 5已取消
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'status': i}
        response = self.request_handle('post', self.urls['gR4uLU4p7'], data=json.dumps(data),   headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class Krj5gFvH88BTJJo3iWzJX(BaseApi):
    """保卖管理|商品管理"""

    def G1RYa7qCCi7R(self, i=None, headers=None):
        """商品管理列表
         i：订单状态 1质检中 2待销售 3销售中
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'status': i}
        response = self.request_handle('post', self.urls['p513Ph2Gz'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = ()
    result = api
    print(result)
    print(json.dumps(result, indent=4, ensure_ascii=False))
