# coding: utf-8
import json
from common.base_api import BaseApi
from api.api_login import LoginApi
from common.base_url import URL


class RecyclerBidSuccessOrderApi(BaseApi):
    """回收商管理|竞价成功订单"""

    def bid_success_order_list(self, headers=None):
        """竞价成功订单"""
        headers = headers or self.headers['main']
        data = {"dateFrom": self.get_the_date(-30), "dateTo": self.get_the_date(), **self.get_page_params(),
                "bidStatus": "oss"}
        response = self.request_handle('post', self.urls['bid_success_order'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'result.rows', list)
        self.make_pkl_file(res)
        return res


class RecyclerJoinMachineApi(BaseApi):
    """回收商管理|参与竞价机器"""

    def join_bidding_machine_list(self, headers=None):
        """参与竞价机器"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['join_bidding_machine'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class RecyclerManualBiddingApi(BaseApi):
    """回收商管理|手动竞价列表"""

    def manual_bidding_list(self, headers=None):
        """手动竞价列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['manual_bidding'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = None
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
