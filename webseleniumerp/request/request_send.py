# coding: utf-8
import json
from common.base_api import BaseApi
from common.base_params import InitializeParams,is_performance_close
from common.import_desc import *
from config.user_info import INFO


class SendBeenSentRepairRequest(InitializeParams):
    """送修管理|已送修物品"""

    @doc(s_repair_completed_route)
    @BaseApi.timing_decorator
    def repair_completed_route(self, nocheck=False):
        res = self.pc.send_been_sent_repair_data()
        data = {
            "returnSuccessType": 1,
            "repairCompletedArticleList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "id": res[0]['id'],
                    "orderNo": res[0]['orderNo'],
                    "repairAmount": 0,
                    "accessoryPrice": 0,
                    "articlesType": 1
                }
            ]
        }
        return self._make_request('post', 'sent_for_repair', data, 'main', nocheck)


class SendRepairListRequest(InitializeParams):
    """送修管理|送修单列表"""

    @doc(s_repair_fee_settlement_paid)
    @BaseApi.timing_decorator
    def repair_fee_settlement_paid(self, nocheck=False):
        res = self.pc.send_list_of_repair_orders_data()
        data = {
            "id": res[0]['id'],
            "payStatus": "1",
            "payAccount": INFO['main_account_no']
        }
        return self._make_request('post', 'send_the_repair_cost_settlement', data, 'main', nocheck)

    @doc(s_repair_fee_settlement_non_payment)
    @BaseApi.timing_decorator
    def repair_fee_settlement_non_payment(self, nocheck=False):
        res = self.pc.send_list_of_repair_orders_data()
        data = {
            "id": res[0]['id'],
            "payStatus": "0"
        }
        return self._make_request('post', 'send_the_repair_cost_settlement', data, 'main', nocheck)


class SendStayRepairRequest(InitializeParams):
    """送修管理|待送修物品"""

    @doc(s_send_out_for_repair)
    @BaseApi.timing_decorator
    def send_out_for_repair(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='16')
        data = {
            "saleState": 13,
            "offExpressage": "0",
            "logisticsNoPrice": 11,
            "logisticsNo": self.sf,
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "purchaseOrdersArticlesDTOList": [
                {
                    "purchaseNo": res[0]['purchaseNo'],
                    "articlesNo": res[0]['articlesNo'],
                    "id": res[0]['id'],
                    "purchasePrice": res[0]['purchasePrice'],
                    "saleRemake": "备注",
                    "imei": res[0]['imei'],
                    "articlesType": 1,
                    "platformArticlesNo": res[0]['platformArticlesNo'],
                    "articlesTypeId": 1,
                    "articlesTypeName": res[0]['articlesTypeName']
                }
            ],
            "deliveryTime": self.get_formatted_datetime(),
        }
        return self._make_request('post', 'send_out_the_warehouse', data, 'main', nocheck)


if __name__ == '__main__':
    api = SendBeenSentRepairRequest()
    result = api.repair_completed_route()
    print(json.dumps(result, indent=4, ensure_ascii=False))
