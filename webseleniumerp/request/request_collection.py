# coding: utf-8
import json

from common.base_api import BaseApi
from common.base_params import InitializeParams
from common.file_cache_manager import ParamCache
from common.import_desc import *
from config.user_info import INFO


class L9OPe7bpsb(InitializeParams):
    """bot速收小程序|估价"""

    @doc(NlMCdnlfaAys36F8lpXa)
    @BaseApi.timing_decorator
    def NlMCdnlfaAys36F8lpXa(self, nocheck=False):
        data = {
            "brandId": "1",
            "modelId": "12282",
            "centerId": INFO['merchant_id'],
            "localMachine": 0,
            "skuIdList": [
                "838",
                "16",
                "1712",
                "41"
            ],
            "optionIdList": [
                1045,
                1014,
                741,
                1056,
                750,
                755,
                748,
                1018,
                1048,
                1050
            ],
            "valuationPlatform": 2
        }
        return self._make_request('post', 'pfyHx9Wz2', data, 'collection', nocheck)

    @doc(hFO4xZGpC9IyEEtPv313)
    @BaseApi.timing_decorator
    def hFO4xZGpC9IyEEtPv313(self, nocheck=False):
        obj = self.NlMCdnlfaAys36F8lpXa()
        valuation_no = obj.get('data', {}).get('valuationNo')
        ParamCache.cache_object({"i": valuation_no})
        data = {
            "centerId": INFO['merchant_id'],
            "valuationNoList": [
                valuation_no
            ],
            "isInsured": 0,
            "expressInfo": {
                "senderLongitude": 113.474785,
                "senderLatitude": 23.171635,
                "valuationNoList": [
                    valuation_no
                ],
                "shipmentType": 3,
                "expectPostTimeStart": self.get_formatted_datetime(),
                "expectPostTimeEnd": self.get_formatted_datetime(days=1),
                "cityCenterId": INFO['merchant_id'],
                "cityCenterName": INFO['check_the_center_name'],
                "senderPhone": self.phone
            },
            "insuredExpressInfo": {
                "shipmentType": 3,
                "expectPostTimeStart": self.get_formatted_datetime(),
                "expectPostTimeEnd": self.get_formatted_datetime(days=1)
            }
        }
        return self._make_request('post', 'wswsnqJGr', data, 'collection', nocheck)





if __name__ == '__main__':
    api = CollectionValuedRequest()
    result = api.hFO4xZGpC9IyEEtPv313()
    print(json.dumps(result, indent=4, ensure_ascii=False))
