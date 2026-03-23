# coding: utf-8
import json
from common.base_api import BaseApi
from common.base_params import InitializeParams


class SellAfterSaleAddArticlesApi(InitializeParams):
    """商品销售|销售售后管理|销售售后处理"""


class SellAfterSalesListApi(BaseApi):
    """商品销售|销售售后管理|销售售后列表"""

    def sales_and_after_sales_are_completed(self, headers=None, num=1, size=1000):
        """销售售后完成"""
        headers = headers or self.headers['main']
        data = {'saleStatus': '5', **self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['sales_aftermarket_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def in_the_after_sales_service(self, headers=None, num=1, size=1000):
        """销售售后中"""
        headers = headers or self.headers['main']
        data = {'saleStatus': '4', **self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['sales_aftermarket_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class SellCustomersManageApi(BaseApi):
    """商品销售|客户管理"""

    def customers_manage(self, headers=None):
        """客户管理"""
        headers = headers or self.headers['main']
        data = {"type": 1, **self.get_page_params()}
        response = self.request_handle('post', self.urls['supplier_manage'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    # 获取id
    def get_id(self):
        return self._get_field_copy_value('customers_manage', 'main', 'id', index=1)

    # 获取id
    def get_id_vice(self):
        return self._get_field_copy_value('customers_manage', 'vice', 'id')


class SellGoodsReceivedApi(BaseApi):
    """商品销售|销售管理|待接收物品"""

    def goods_received_list(self, headers=None):
        """待接收物品列表"""
        headers = headers or self.headers['main']
        data = {"articlesState": 13, "articlesType": "1", **self.get_page_params()}
        response = self.request_handle('post', self.urls['inventory_receive_items'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res

    # 获取物品编号
    def get_list_articles_no(self):
        return self._get_field_copy_value('goods_received_list', 'main', 'articlesNo')


class SellItemsForSaleApi(BaseApi):
    """商品销售|销售管理|待销售物品"""

    def items_for_sale(self, headers=None, num=1, size=1000):
        """待销售物品列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['items_for_sale'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def items_detail(self, headers=None, articles_no=None):
        """待销售物品详情"""
        headers = headers or self.headers['main']
        articles_no = articles_no or self.get_articles_no()
        response = self.request_handle('get', self.urls['items_for_sale_detail'] + articles_no, headers=headers)
        return self.get_response_data(response, 'data', dict)

    # 获取物品编号
    def get_articles_no(self):
        return self._get_field_copy_value('items_for_sale', 'main', 'articlesNo')


class SellListOfItemsForSaleApi(BaseApi):
    """商品销售|销售管理|销售中物品列表"""

    def goods_list_for_sale(self, i=None, j=None, headers=None, num=1, size=1000):
        """销售中物品列表
         i：销售状态 2已销售 3已取消 1销售中
         j：销售类型 1销售 3铺货 5预售
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'saleStatus': i, 'saleType': j}
        response = self.request_handle('post', self.urls['goods_list_for_sale'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def sales_goods_detail(self, headers=None, articles_no=None):
        """销售物品详情"""
        headers = headers or self.headers['main']
        articles_no = articles_no or self.get_articles_no()
        data = {"code": articles_no, "saleType": 2}
        response = self.request_handle('post', self.urls['delisting_details'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)

    def sales_goods_list_delisting_details(self, headers=None, item=None):
        """下架详情"""
        headers = headers or self.headers['main']
        item = item or self.get_articles_no()
        data = {'code': item, 'saleType': 2}
        response = self.request_handle('post', self.urls['delisting_details'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res

    # 获取物品编号
    def get_articles_no(self):
        return self._get_field_copy_value('goods_list_for_sale', 'main', 'articlesNo')


class SellOrderListForSaleApi(BaseApi):
    """商品销售|销售管理|销售中订单列表"""

    def order_list_for_sale(self, headers=None, num=1, size=1000):
        """销售中订单列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['order_list_for_sale'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class SellSaleItemListApi(BaseApi):
    """商品销售|销售管理|已销售物品列表"""

    def sell_sale_item_list(self, headers=None, num=1, size=1000):
        """已销售物品列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['sell_sale_item_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class SellSoldOrderApi(BaseApi):
    """商品销售|销售管理|已销售订单列表"""

    def sold_order_list(self, headers=None, num=1, size=1000):
        """已销售订单列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['list_of_sold_orders'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class SellStaticsApi(BaseApi):
    """商品销售|销售数据统计"""

    def statics(self, headers=None, i=None):
        """统计"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "startTime": self.get_the_date(-30), "endTime": self.get_the_date(), 'saleSupplierId': i}
        response = self.request_handle('post', self.urls['sell_statics'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = SellStaticsApi()
    result = api.statics()
    print(json.dumps(result, indent=4, ensure_ascii=False))
