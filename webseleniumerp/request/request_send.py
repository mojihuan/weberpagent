# coding: utf-8
import json
from common.base_api import BaseApi
from common.base_params import InitializeParams
from common.import_desc import *
from config.user_info import INFO


class FU9FBZt4ek(InitializeParams):
    """送修管理|已送修物品"""

    @doc(oaxztsMnbnAXzAxWj6JK)
    @BaseApi.timing_decorator
    def oaxztsMnbnAXzAxWj6JK(self, nocheck=False):
        res = self.pc.QM4hD6LNhqKxZAitqFFJl()
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
        return self._make_request('post', 'kVBioewfn', data, 'main', nocheck)


class KNGJBF1SxK(InitializeParams):
    """送修管理|送修单列表"""

    @doc(woND08hYZ9lwms8Lse0i)
    @BaseApi.timing_decorator
    def woND08hYZ9lwms8Lse0i(self, nocheck=False):
        res = self.pc.MMuymWgzUDbCSdlZPeMMY()
        data = {
            "id": res[0]['id'],
            "payStatus": "1",
            "payAccount": INFO['main_account_no']
        }
        return self._make_request('post', 'ic1tjRLFM', data, 'main', nocheck)

    @doc(k42ezJisaBTjBTBWBoXd)
    @BaseApi.timing_decorator
    def k42ezJisaBTjBTBWBoXd(self, nocheck=False):
        res = self.pc.MMuymWgzUDbCSdlZPeMMY()
        data = {
            "id": res[0]['id'],
            "payStatus": "0"
        }
        return self._make_request('post', 'ic1tjRLFM', data, 'main', nocheck)


class DImzEKD7BR(InitializeParams):
    """送修管理|待送修物品"""

    @doc(FDe96kyUKHRoCJ6I7nfE)
    @BaseApi.timing_decorator
    def FDe96kyUKHRoCJ6I7nfE(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='16')
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
        return self._make_request('post', 'MQ0HvcES5', data, 'main', nocheck)


if __name__ == '__main__':
    api = ()
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
