# coding: utf-8
import json
from common.base_api import BaseApi


class SoldListOfXianYuOrdersApi(BaseApi):
    """同售管理|闲鱼严选|闲鱼订单列表"""

    def get_list_of_xian_yu_orders(self, headers=None):
        """闲鱼订单列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['same_sale_xy_orders_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class SoldListOfXianYuProductsApi(BaseApi):
    """同售管理|闲鱼严选|闲鱼商品列表"""

    def get_list_of_xian_yu_products(self, headers=None):
        """闲鱼商品列表"""
        headers = headers or self.headers['main']
        data = {'platformType': 1, **self.get_page_params()}
        response = self.request_handle('post', self.urls['same_sale_xy_goods_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class SoldListOfXianYuSalesApi(BaseApi):
    """同售管理|闲鱼严选|闲鱼售后列表"""

    def get_list_of_xian_yu_sales(self, headers=None):
        """闲鱼售后列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "platformType": 1}
        response = self.request_handle('post', self.urls['same_sale_de_wu_sales_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class SoldNinetyFiveItemListApi(BaseApi):
    """同售管理|得物95分|95商品列表"""

    def get_ninety_five_item_list(self, i=None, headers=None):
        """95商品列表
         i：物品状态 3已发布 2发布失败

        """
        headers = headers or self.headers['main']
        data = {'platformType': 2, **self.get_page_params(), "goodsStatus": i}
        response = self.request_handle('post', self.urls['same_sale_xy_goods_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class SoldNinetyFiveOrdersListApi(BaseApi):
    """同售管理|得物95分|订单列表"""

    def get_ninety_five_orders_list(self, headers=None):
        """95订单列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['same_sale_de_wu_orders_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class SoldNinetyFiveRebackListApi(BaseApi):
    """同售管理|得物95分|回退列表"""

    def get_ninety_five_orders_list(self, headers=None):
        """95回退列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['same_sale_de_wu_re_back'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class SoldNinetyFiveSalesListApi(BaseApi):
    """同售管理|得物95分|售后列表"""

    def get_ninety_five_orders_list(self, headers=None):
        """95售后列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "platformType": 2}
        response = self.request_handle('post', self.urls['same_sale_de_wu_sales_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = None
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
