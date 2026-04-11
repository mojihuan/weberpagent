# coding: utf-8
from common.base_api import BaseApi
from common.base_params import InitializeParams
from common.file_cache_manager import ParamCache
from common.import_desc import *
from config.user_info import INFO


class DuLudPwrAY(InitializeParams):
    """拍机小程序|竞拍"""

    @doc(ooh8smtEbSrtOuUNqjJa)
    @BaseApi.timing_decorator
    def ooh8smtEbSrtOuUNqjJa(self, nocheck=False):
        self.wait_default()
        res = self.pc.HnlUtAPz07JtZRXny3Ogs(i=2)
        res_2 = self.pc.YVqIQus8roZWysBseaMP0(i=1)
        res_3 = self.pc.YVqIQus8roZWysBseaMP0(data='b')
        obj = res[0]['articlesNo']
        obj_2 = '8888'
        ParamCache.cache_object({"articlesNo": obj}, {"bidPrice": obj_2}, 'practical.json')
        data = {
            "sessionId": res_3[0]['id'],
            "marketId": res_2[0]['id'],
            "articlesNo": obj,
            "bidPrice": obj_2,
            "marketCategory": "1"
        }
        return self._make_request('post', 'Uv26Jy6GJ', data, 'camera', nocheck)

    @doc(SAnRSrq1160pZali4yIf)
    @BaseApi.timing_decorator
    def SAnRSrq1160pZali4yIf(self, nocheck=False):
        self.wait_default()
        res = self.pc.HnlUtAPz07JtZRXny3Ogs(i=2)
        res_2 = self.pc.BaxRsHzRpoNsTb8fnSa9e()
        res_3 = self.pc.BaxRsHzRpoNsTb8fnSa9e(data='b')
        obj = res[0]['articlesNo']
        obj_2 = '9999'
        ParamCache.cache_object({"articlesNo": obj}, {"bidPrice": obj_2}, 'practical.json')
        data = {
            "sessionId": res_3[0]['id'],
            "marketId": res_2[0]['id'],
            "articlesNo": obj,
            "bidPrice": obj_2,
            "marketCategory": "2"
        }
        return self._make_request('post', 'Uv26Jy6GJ', data, 'camera', nocheck)

    @doc(YvnI8JFogJKDJyevymIw)
    @BaseApi.timing_decorator
    def YvnI8JFogJKDJyevymIw(self, nocheck=False):
        res = self.pc.HnlUtAPz07JtZRXny3Ogs(i=2)
        res_2 = self.pc.YVqIQus8roZWysBseaMP0()
        res_3 = self.pc.YVqIQus8roZWysBseaMP0(data='b')
        res_4 = self.pc.B1VzuYLyr5G9mdeT7BDwW(data='a')
        obj = res[0]['articlesNo']
        obj_2 = '5555'
        ParamCache.cache_object({"articlesNo": obj}, {"bidPrice": obj_2}, 'practical.json')
        data = {
            "sessionId": res_3[0]['id'],
            "marketId": res_2[0]['id'],
            "articlesNo": obj,
            "bidPrice": obj_2,
            "id": res_4[0]['bidPriceId']
        }
        return self._make_request('post', 'S8PjmEPm5', data, 'camera', nocheck)

    @doc(MdM1073dpYo2D4xRtbN4)
    @BaseApi.timing_decorator
    def MdM1073dpYo2D4xRtbN4(self, nocheck=False):
        res = self.pc.HnlUtAPz07JtZRXny3Ogs(i=2)
        res_2 = self.pc.YVqIQus8roZWysBseaMP0()
        res_3 = self.pc.YVqIQus8roZWysBseaMP0(data='b')
        res_4 = self.pc.B1VzuYLyr5G9mdeT7BDwW()
        obj = res[0]['articlesNo']
        obj_2 = '5555'
        ParamCache.cache_object({"articlesNo": obj}, {"bidPrice": obj_2}, 'practical.json')
        data = {
            "sessionId": res_3[0]['id'],
            "marketId": res_2[0]['id'],
            "articlesNo": obj,
            "bidPrice": obj_2,
            "id": res_4[0]['bidPriceId']
        }
        return self._make_request('post', 'S8PjmEPm5', data, 'camera', nocheck)


class RQTYlCj2X9(InitializeParams):
    """拍机小程序|我的"""

    @doc(Ly41cUm9R4N75FqquckG)
    @BaseApi.timing_decorator
    def Ly41cUm9R4N75FqquckG(self, nocheck=False):
        res = self.pc.UAPqxpSx1qiMwyQEcIPXb(i=2)
        obj = res[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj}, 'practical.json')
        data = {
            "orderNo": res[0]['saleOrderNo'],
            "articlesNo": obj
        }
        return self._make_request('post', 'dgzXMTa7e', data, 'camera', nocheck)

    @doc(wOMYzQailIlwneqp3YqQ)
    @BaseApi.timing_decorator
    def wOMYzQailIlwneqp3YqQ(self, nocheck=False):
        res = self.pc.KmxOWBECeMnMqtP1qACyx(data='b')
        obj = res[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj}, 'practical.json')
        data = {
            "orderNo": res[0]['saleOrderNo'],
            "articlesNo": obj
        }
        return self._make_request('post', 'dgzXMTa7e', data, 'camera', nocheck)

    @doc(c71cLTyRLuY4tAw5OBlV)
    @BaseApi.timing_decorator
    def c71cLTyRLuY4tAw5OBlV(self, nocheck=False):
        res = self.pc.UAPqxpSx1qiMwyQEcIPXb(i=3)
        obj = res[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj}, 'practical.json')
        data = {
            "orderNo": res[0]['saleOrderNo'],
            "articlesNo": obj
        }
        return self._make_request('post', 'U3aqRLh23', data, 'camera', nocheck)

    @doc(aVXdmJVbK9wjjXJCBjst)
    @BaseApi.timing_decorator
    def aVXdmJVbK9wjjXJCBjst(self, nocheck=False):
        res = self.pc.UAPqxpSx1qiMwyQEcIPXb(i=4)
        data = {
            "articlesNo": res[0]['articlesNo'],
            "auctionAfterSalesOrderReason": {
                "afterReason": "4",
                "afterDesc": "售后",
                "imageUrl": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com//erp-imgfiles/%2Fepbox-erp/20260203/Cky5EnqksaGALjZuTUQMkA%3D%3D.png",
                "videoUrl": "",
                "qualityInspectionReportList": [

                ]
            }
        }
        return self._make_request('post', 'lT1CRJl4T', data, 'camera', nocheck)

    @doc(BPBCQmGYcAgtwQuFgbaO)
    @BaseApi.timing_decorator
    def BPBCQmGYcAgtwQuFgbaO(self, nocheck=False):
        res = self.pc.UAPqxpSx1qiMwyQEcIPXb(data='a', i=[6])
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'sO1Sva4AY', data, 'camera', nocheck)

    @doc(J62o1YNEgyQUVrUfzEs3)
    @BaseApi.timing_decorator
    def J62o1YNEgyQUVrUfzEs3(self, nocheck=False):
        res = self.pc.UAPqxpSx1qiMwyQEcIPXb(data='a', i=[6])
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'sO1Sva4AY', data, 'camera', nocheck)

    @doc(zd1jfkpdiIAy1G9RVrIq)
    @BaseApi.timing_decorator
    def zd1jfkpdiIAy1G9RVrIq(self, nocheck=False):
        res = self.pc.UAPqxpSx1qiMwyQEcIPXb(data='a', i=[6])
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'EDIy8SBwR', data, 'camera', nocheck)

    @doc(HOPKwhJtyDRx8zxTdh7S)
    @BaseApi.timing_decorator
    def HOPKwhJtyDRx8zxTdh7S(self, nocheck=False):
        res = self.pc.UAPqxpSx1qiMwyQEcIPXb(data='a', i=[6])
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'EDIy8SBwR', data, 'camera', nocheck)

    @doc(XFuplSfvhfY3pPN3q60t)
    @BaseApi.timing_decorator
    def XFuplSfvhfY3pPN3q60t(self, nocheck=False):
        res = self.pc.UAPqxpSx1qiMwyQEcIPXb(data='a', i=[6])
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'EDIy8SBwR', data, 'camera', nocheck)

    @doc(jw92LPqmCSgtAgFxlGVO)
    @BaseApi.timing_decorator
    def jw92LPqmCSgtAgFxlGVO(self, nocheck=False):
        res = self.pc.UAPqxpSx1qiMwyQEcIPXb(data='a', i=[6])
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'pd3YAYXZg', data, 'camera', nocheck)

    @doc(G8mzJPJPK9gNaeIm9U7P)
    @BaseApi.timing_decorator
    def G8mzJPJPK9gNaeIm9U7P(self, nocheck=False):
        res = self.pc.UAPqxpSx1qiMwyQEcIPXb(data='a', i=[2])
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'pd3YAYXZg', data, 'camera', nocheck)

    @doc(SXKFMEeSoPN01IP9Lwlp)
    @BaseApi.timing_decorator
    def SXKFMEeSoPN01IP9Lwlp(self, nocheck=False):
        res = self.pc.UAPqxpSx1qiMwyQEcIPXb(data='a', i=[6])
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'pd3YAYXZg', data, 'camera', nocheck)

    @doc(UfKqlNZ2jFR6rFZUiH8v)
    @BaseApi.timing_decorator
    def UfKqlNZ2jFR6rFZUiH8v(self, nocheck=False):
        res = self.pc.UAPqxpSx1qiMwyQEcIPXb(data='a', i=[7])
        res_2 = self.pc.B63gyanXogW9NpUu1Gr1K()
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "sendType": 1,
            "expressCompanyId": "1",
            "expressCompanyName": "顺丰物流",
            "expectPostTimeStart": self.get_formatted_datetime(),
            "expressType": 1,
            "express": {
                "senderName": INFO['camera_name'],
                "senderPhone": INFO['camera_phone'],
                "senderProvinceId": INFO['province_id'],
                "senderProvinceName": INFO['province_name'],
                "senderCityId": INFO['city_id'],
                "senderCityName": INFO['city_name'],
                "senderCountyId": INFO['county_id'],
                "senderCountyName": INFO['county_name'],
                "senderAddress": INFO['detailed_address']
            },
            "id": obj,
            "centerId": res_2[0]['id']
        }
        return self._make_request('post', 'Q2KtOpnyw', data, 'camera', nocheck)

    @doc(fujEfOlXIMCY3oXrDNVd)
    @BaseApi.timing_decorator
    def fujEfOlXIMCY3oXrDNVd(self, nocheck=False):
        res = self.pc.UAPqxpSx1qiMwyQEcIPXb(data='a', i=[7])
        res_2 = self.pc.B63gyanXogW9NpUu1Gr1K()
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "expressNo": self.sf,
            "expressCompanyId": INFO['sf_express_logo'],
            "expressCompanyName": "顺丰快运",
            "id": obj,
            "centerId": res_2[0]['id'],
            "sendType": 2
        }
        return self._make_request('post', 'Q2KtOpnyw', data, 'camera', nocheck)

    @doc(nKqLT6q8XX9QYiJ26jms)
    @BaseApi.timing_decorator
    def nKqLT6q8XX9QYiJ26jms(self, nocheck=False):
        res = self.pc.UAPqxpSx1qiMwyQEcIPXb(data='a', i=[7])
        res_2 = self.pc.B63gyanXogW9NpUu1Gr1K()
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "expressNo": self.sf,
            "expressCompanyId": INFO['sf_express_logo'],
            "expressCompanyName": "顺丰快运",
            "id": obj,
            "centerId": res_2[0]['id'],
            "sendType": 2
        }
        return self._make_request('post', 'Q2KtOpnyw', data, 'camera', nocheck)

    @doc(ZLMjQKplgxx6Krvopxg7)
    @BaseApi.timing_decorator
    def ZLMjQKplgxx6Krvopxg7(self, nocheck=False):
        res = self.pc.UAPqxpSx1qiMwyQEcIPXb(data='a', i=[7])
        res_2 = self.pc.B63gyanXogW9NpUu1Gr1K()
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj,
            "centerId": res_2[0]['id'],
            "sendType": 3
        }
        return self._make_request('post', 'Q2KtOpnyw', data, 'camera', nocheck)

    @doc(FFK90vpcso9aPNnQyAWS)
    @BaseApi.timing_decorator
    def FFK90vpcso9aPNnQyAWS(self, nocheck=False):
        res = self.pc.UAPqxpSx1qiMwyQEcIPXb(data='a', i=[7])
        res_2 = self.pc.B63gyanXogW9NpUu1Gr1K()
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj,
            "centerId": res_2[0]['id'],
            "sendType": 3
        }
        return self._make_request('post', 'Q2KtOpnyw', data, 'camera', nocheck)

    @doc(xYF6VMP7gVBubHHeRksW)
    @BaseApi.timing_decorator
    def xYF6VMP7gVBubHHeRksW(self, nocheck=False):
        res = self.pc.UAPqxpSx1qiMwyQEcIPXb(data='a', i=[2])
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj,
            "auctionAfterSalesOrderAppeal": {
                "afterDesc": "申诉",
                "imageUrl": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com//erp-imgfiles/%2Fepbox-erp/20260206/Cky5EnqksaGALjZuTUQMkA%3D%3D.png",
                "videoUrl": "",
                "appealType": "0"
            }
        }
        return self._make_request('post', 'JOdnj8tkF', data, 'camera', nocheck)

    @doc(qy2BOyYcjRZCMRxmI1HJ)
    @BaseApi.timing_decorator
    def qy2BOyYcjRZCMRxmI1HJ(self, nocheck=False):
        res = self.pc.UAPqxpSx1qiMwyQEcIPXb(data='a', i=[2])
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj,
            "auctionAfterSalesOrderAppeal": {
                "afterDesc": "申诉",
                "imageUrl": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com//erp-imgfiles/%2Fepbox-erp/20260206/Cky5EnqksaGALjZuTUQMkA%3D%3D.png",
                "videoUrl": "",
                "appealType": "0"
            }
        }
        return self._make_request('post', 'JOdnj8tkF', data, 'camera', nocheck)

    @doc(GUCbnylR1i5xvkHG84Lq)
    @BaseApi.timing_decorator
    def GUCbnylR1i5xvkHG84Lq(self, nocheck=False):
        res = self.pc.UAPqxpSx1qiMwyQEcIPXb(data='a', i=[6])
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'sO1Sva4AY', data, 'camera', nocheck)

    @doc(aSUFM1IQg6Qn99K4na0b)
    @BaseApi.timing_decorator
    def aSUFM1IQg6Qn99K4na0b(self, nocheck=False):
        res = self.pc.UAPqxpSx1qiMwyQEcIPXb(data='a', i=[7])
        res_2 = self.pc.B63gyanXogW9NpUu1Gr1K()
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "sendType": 1,
            "expressCompanyId": "1",
            "expressCompanyName": "顺丰物流",
            "expectPostTimeStart": self.get_formatted_datetime(),
            "expressType": 1,
            "express": {
                "senderName": INFO['camera_name'],
                "senderPhone": INFO['camera_phone'],
                "senderProvinceId": INFO['province_id'],
                "senderProvinceName": INFO['province_name'],
                "senderCityId": INFO['city_id'],
                "senderCityName": INFO['city_name'],
                "senderCountyId": INFO['county_id'],
                "senderCountyName": INFO['county_name'],
                "senderAddress": INFO['detailed_address']
            },
            "id": obj,
            "centerId": res_2[0]['id']
        }
        return self._make_request('post', 'Q2KtOpnyw', data, 'camera', nocheck)


if __name__ == '__main__':
    api = ()
    result = api
    print(result)
