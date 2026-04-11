# coding: utf-8
import json
from common.base_api import BaseApi
from common.base_params import InitializeParams
from common.file_cache_manager import ParamCache
from common.import_desc import *


class Qca9iy6PVm(InitializeParams):
    """拍机管理|售后管理|售后订单"""

    @doc(hmyGjNG7wkd0bhQUc2TE)
    @BaseApi.timing_decorator
    def hmyGjNG7wkd0bhQUc2TE(self, nocheck=False):
        res = self.pc.ZpUG9P3oxkPb5GFqBrxGQ()
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'hV29HowU2', data, 'camera', nocheck)


class Cb5YB9WqSi(InitializeParams):
    """拍机管理|拍机场次列表"""

    @doc(HX8VkOqbnv1J3lPVSFmm)
    @BaseApi.timing_decorator
    def HX8VkOqbnv1J3lPVSFmm(self, nocheck=False):
        res = self.pc.Z4B1h5YLGNro3dwGrXQhF(data='a')
        res_2 = self.pc.Z4B1h5YLGNro3dwGrXQhF()
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
        return self._make_request('post', 'tPcTx5hqA', data, 'camera', nocheck)

    @doc(lPB3LMDCzxeHLnAzXMs9)
    @BaseApi.timing_decorator
    def lPB3LMDCzxeHLnAzXMs9(self, nocheck=False):
        res = self.pc.Z4B1h5YLGNro3dwGrXQhF(data='a')
        res_2 = self.pc.Z4B1h5YLGNro3dwGrXQhF()
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
        return self._make_request('post', 'tPcTx5hqA', data, 'camera', nocheck)


if __name__ == '__main__':
    api = ()
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
