# coding: utf-8
import json
from common.base_api import BaseApi
from common.base_params import InitializeParams, is_performance_close
from common.file_cache_manager import ParamCache
from common.import_desc import *
from config.user_info import INFO


class CameraAfterSalesOrdersRequest(InitializeParams):
    """拍机管理|售后管理|售后订单"""

    @doc(c_pending_end_of_after_sales)
    @BaseApi.timing_decorator
    def pending_end_of_after_sales(self, nocheck=False):
        res = self.pc.camera_after_sales_order_data()
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'pending_end_of_after_sales', data, 'camera', nocheck)


class AListOfAirportVisitsRequest(InitializeParams):
    """拍机管理|拍机场次列表"""

    @doc(c_direct_auction_bidding_modify_the_price)
    @BaseApi.timing_decorator
    def direct_auction_bidding_modify_the_price(self, nocheck=False):
        res = self.pc.camera_list_of_airport_visits_data(data='a')
        res_2 = self.pc.camera_list_of_airport_visits_data()
        obj = res[0]['articlesNo']
        obj_2 = 8888
        ParamCache.cache_object({"articlesNo": obj}, {"bidPrice": obj_2}, 'practical.json')
        data = {
            "articlesNo": obj,
            "bidPrice": obj_2,
            "id": res[0]['id'],
            "marketCategory": 2,
            "marketId": res[0]['marketId'],
            "sessionId": res_2[0]['id']
        }
        return self._make_request('post', 'modify_the_direct_sale_price', data, 'camera', nocheck)

    @doc(c_secret_shot_bidding_modify_the_price)
    @BaseApi.timing_decorator
    def secret_shot_bidding_modify_the_price(self, nocheck=False):
        res = self.pc.camera_list_of_airport_visits_data(data='a')
        res_2 = self.pc.camera_list_of_airport_visits_data()
        obj = res[0]['articlesNo']
        obj_2 = 8888
        ParamCache.cache_object({"articlesNo": obj}, {"bidPrice": obj_2}, 'practical.json')
        data = {
            "articlesNo": obj,
            "bidPrice": obj_2,
            "id": res[0]['id'],
            "marketCategory": 2,
            "marketId": res[0]['marketId'],
            "sessionId": res_2[0]['id']
        }
        return self._make_request('post', 'modify_the_direct_sale_price', data, 'camera', nocheck)


if __name__ == '__main__':
    api = CameraAfterSalesOrdersRequest()
    result = api.pending_end_of_after_sales()
    print(json.dumps(result, indent=4, ensure_ascii=False))
