# coding: utf-8
import json
from common.base_api import BaseApi


class AuctionIndexApi(BaseApi):
    """保卖小程序-首页"""

    def item_info_list(self, headers=None):
        """精确发货 物品信息列表"""
        headers = headers or self.headers['main']
        data = {"modelId": 17569}
        response = self.request_handle('post', self.urls['sku'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)

    def list_of_appearance_finishes(self, headers=None):
        """精确发货 外观成色列表"""
        headers = headers or self.headers['main']
        data = {"modelId": 17569, "businessModel": 1}
        response = self.request_handle('post', self.urls['appearance'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)

    # 获取id
    def get_data_id(self):
        return self._get_field_copy_value('list_of_appearance_finishes', 'main', 'id')


class AuctionMyApi(BaseApi):
    """保卖小程序-我的"""

    def sell_order_list(self, i=None, j=None, headers=None, num=1, size=1000):
        """销售订单列表
         i：订单状态 1质检中 2待销售 3销售中 4已销售 5待平台确认 6报价确认 8退货中 9退货已出库 10已退货 7质检完成
         j：类型 1销售服务 2质检服务
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), "businessType": j, 'status': i}
        response = self.request_handle('post', self.urls['sell_order_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def sell_return_details(self, headers=None):
        """退货中 退货详情"""
        res = self.sell_order_list(i=8)
        headers = headers or self.headers['main']
        data = {"id": res[0]['id']}
        response = self.request_handle('post', self.urls['sell_return_details'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)

    def order_details(self, headers=None, i=None):
        """订单详情"""
        res = self.sell_order_list(i=i)
        headers = headers or self.headers['main']
        data = {"id": res[0]['id']}
        response = self.request_handle('post', self.urls['valuation_item_deleted'], data=json.dumps(data),
                                       headers=headers)
        return self.get_response_data(response, 'data', dict)

    def order_list(self, i=None, j=None, headers=None):
        """订单列表
         i：订单状态 1待发货 2待取件 3待收货 4已收货
         j：类型 1销售服务 2质检服务
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "businessType": j}
        if i:
            data['status'] = int(i)
        response = self.request_handle('post', self.urls['order_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    # 获取成色名称
    def get_fineness_name(self):
        return self._get_field_copy_value('order_details', 'main', 'articlesInfoList.finenessName')


if __name__ == '__main__':
    api = AuctionIndexApi()
    result = api.list_of_appearance_finishes()
    print(json.dumps(result, indent=4, ensure_ascii=False))
