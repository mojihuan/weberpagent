# coding: utf-8
import json
from common.base_api import BaseApi
from config.user_info import INFO


class CameraAfterSalesOrderApi(BaseApi):
    """拍机管理|售后管理|售后订单"""

    def after_sales_list(self, headers=None):
        """售后订单列表"""
        headers = headers or self.headers['camera']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['after_sales_order_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class CameraListOfAirportVisitsApi(BaseApi):
    """拍机管理|拍机场次列表"""

    def list_of_airport_visits(self, headers=None):
        """拍机场次列表"""
        headers = headers or self.headers['camera']
        data = {**self.get_page_params(), 'listType': "1"}
        response = self.request_handle('post', self.urls['list_of_airport_visits'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def view_the_products_of_the_session(self, headers=None):
        """查看场次商品"""
        see_id = self.get_id()
        headers = headers or self.headers['camera']
        data = {**self.get_page_params(), 'sessionId': see_id}
        response = self.request_handle('post', self.urls['view_the_products_of_the_session'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)

    # 获取id
    def get_id(self):
        return self._get_field_copy_value('list_of_airport_visits', 'camera', 'id')


if __name__ == '__main__':
    api = CameraListOfAirportVisitsApi()
    result = api.list_of_airport_visits()
    print(json.dumps(result, indent=4, ensure_ascii=False))
