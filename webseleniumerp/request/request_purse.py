# coding: utf-8
import json
from common.base_api import BaseApi
from common.base_params import InitializeParams
from common.import_desc import *


class PNng2wLCAK(InitializeParams):
    """钱包管理|钱包中心"""

    @doc(JxIyyg72fjeXbmTdyUr7)
    @BaseApi.timing_decorator
    def JxIyyg72fjeXbmTdyUr7(self, nocheck=False):
        data = {
            "giftBalance": 0,
            "type": 4,
            "refillPrice": int(self.number),
            "payType": 1,
            "receipt": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com//erp-imgfiles/%2Fepbox-erp/20250820/WIehcT%2B7sg/I4FjLToJM%2Bw%3D%3D.jpg",
            "receiveAccountNo": "1"
        }
        return self._make_request('post', 'MeGvzXuEL', data, 'main', nocheck)


if __name__ == '__main__':
    api = ()
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
