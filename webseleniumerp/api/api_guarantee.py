# coding: utf-8
import json
from common.base_api import BaseApi


class GuaranteeOrderManageApi(BaseApi):
    """保卖管理|订单列表"""

    def order_list(self, i=None, headers=None):
        """订单列表
         i：订单状态 1待发货 2待取件 3待收货 4已收货 5已完成 6已取消 7已退货

        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'status': i}
        response = self.request_handle('post', self.urls['warranted_order_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def item_list(self, headers=None):
        """物品列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['warranted_order_list_item'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class GuaranteeReturnsManageApi(BaseApi):
    """保卖管理|退货管理"""

    def item_detail_list(self, i=None, headers=None):
        """物品明细列表
         i：订单状态 1待退货 2待取货 3退货已出库 4已退货 5已取消

        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'status': i}
        response = self.request_handle('post', self.urls['warranted_item_detail_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def batch_detail_list(self, i=None, headers=None):
        """批次明细列表
         i：订单状态 1待退货 2待取货 3退货已出库 4已退货 5已取消

        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'status': i}
        response = self.request_handle('post', self.urls['warranted_batch_detail_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class GuaranteeGoodsManageApi(BaseApi):
    """保卖管理|商品管理"""

    def order_list(self, i=None, headers=None):
        """商品管理列表
         i：订单状态 1质检中 2待销售 3销售中
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'status': i}
        response = self.request_handle('post', self.urls['warranted_goods_manage'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = GuaranteeGoodsManageApi()
    result = api.order_list(i=2)
    print(result)
    print(json.dumps(result, indent=4, ensure_ascii=False))
