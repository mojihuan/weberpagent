# coding: utf-8
import json
from common.base_api import BaseApi
from common.base_params import InitializeParams
from common.file_cache_manager import ParamCache
from common.import_desc import *
from config.user_info import INFO


class ONWaZZcZFp(InitializeParams):
    """平台管理|虚拟库存|上拍商品管理"""

    @doc(fSkueYEb8y8LbP6qtAqN)
    @BaseApi.timing_decorator
    def fSkueYEb8y8LbP6qtAqN(self, nocheck=False):
        res = self.pc.HnlUtAPz07JtZRXny3Ogs(i=1)
        res_2 = self.pc.HnlUtAPz07JtZRXny3Ogs(data='a', i=1)
        data = {
            "sessionId": res_2[0]['id'],
            "marketId": res_2[0]['marketId'],
            "articlesNoList": [
                res[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'BCizVyy8z', data, 'super', nocheck)

    @doc(qCFRqyBkOvZyZ960KoJp)
    @BaseApi.timing_decorator
    def qCFRqyBkOvZyZ960KoJp(self, nocheck=False):
        res = self.pc.HnlUtAPz07JtZRXny3Ogs(i=1)
        res_2 = self.pc.HnlUtAPz07JtZRXny3Ogs(data='a', i=2)
        data = {
            "sessionId": res_2[0]['id'],
            "marketId": res_2[0]['marketId'],
            "articlesNoList": [
                res[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'BCizVyy8z', data, 'super', nocheck)

    @doc(vVyPEQRdLSOkYnwvSH3o)
    @BaseApi.timing_decorator
    def vVyPEQRdLSOkYnwvSH3o(self, nocheck=False):
        res = self.pc.HnlUtAPz07JtZRXny3Ogs(i=1)
        obj = res[0]['articlesId']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": res[0]['id']
        }
        return self._make_request('post', 'hWKS7c7Lb', data, 'super', nocheck)

    @doc(sGNrdfZH3A7fxgKXDlng)
    @BaseApi.timing_decorator
    def sGNrdfZH3A7fxgKXDlng(self, nocheck=False):
        res = self.pc.HnlUtAPz07JtZRXny3Ogs(i=1)
        res_2 = self.pc.HnlUtAPz07JtZRXny3Ogs(data='a', i=2)
        data = {
            "sessionId": res_2[0]['id'],
            "marketId": res_2[0]['marketId'],
            "articlesNo": res[0]['articlesNo'],
            "oldSessionId": res_2[1]['id'],
        }
        return self._make_request('post', 'ZQPweThVm', data, 'super', nocheck)

    @doc(HeRVQcjIj8Kd5Ue1KUfT)
    @BaseApi.timing_decorator
    def HeRVQcjIj8Kd5Ue1KUfT(self, nocheck=False):
        res = self.pc.HnlUtAPz07JtZRXny3Ogs(i=2)
        data = {
            "id": res[0]['id']
        }
        return self._make_request('post', 'yvzrZqHUv', data, 'super', nocheck)


class X7hPGKXTGz(InitializeParams):
    """平台管理|运营中心|待指定物品"""

    @doc(cz1GOzhkNTwJrIaMIvqG)
    @BaseApi.timing_decorator
    def cz1GOzhkNTwJrIaMIvqG(self, nocheck=False):
        res = self.pc.YVqIQus8roZWysBseaMP0()
        data = {
            "assignTenantId": INFO['merchant_id'],
            "id": res[-1]['id']
        }
        return self._make_request('post', 'WSN2Czoza', data, 'super', nocheck)

    @doc(TCteXSkve0Oznurlnztw)
    @BaseApi.timing_decorator
    def TCteXSkve0Oznurlnztw(self, nocheck=False):
        res = self.pc.YVqIQus8roZWysBseaMP0()
        data = {
            "assignTenantId": INFO['merchant_id'],
            "id": res[-1]['id']
        }
        return self._make_request('post', 'WSN2Czoza', data, 'super', nocheck)


class G4BNkqhL40(InitializeParams):
    """"平台管理|卖场管理|暗拍卖场列表"""

    @doc(MLwLbgD1GL9V7rRzU5DF)
    def MLwLbgD1GL9V7rRzU5DF(self, nocheck=False):
        data = {
            "name": self.mixed_random(),
            "desc": '卖场描述' + self.mixed_random(),
            "sort": 11,
            "marketCategory": 1,
            "marketType": 1,
            "sessionFrequency": 0,
            "sessionNum": 1,
            "marketActivityList": self.generate_five_minute_sessions(),
            "auctionMarketRuleConfig": {
                "countdownType": 1,
                "merchantLimitList": [
                    3,
                    4
                ],
                "conditionType": 1,
                "lockType": 1,
                "winRuleType": 2,
                "depositType": 1,
                "rangeLimit": 44,
                "failedSessionRule": 2,
                "failedNum": 3,
                "depositPrice": 999,
                "timer": ""
            },
            "auctionMarketArticlesRuleConfig": {
                "minMum": 1,
                "maxMum": 11111,
                "autoAssignType": 1,
                "countdownType": 1,
                "auctionAutoAssignTypeList": [
                    {
                        "categoryId": "",
                        "brandId": "",
                        "modelIdList": [],
                        "finenessIdList": []
                    }
                ]
            },
            "marketTimeType": 2,
            "isEnable": False,
            "activityStartTime": f"{self.get_the_date()} 00:00:00",
            "activityEndTime": f"{self.get_the_date(days=+20)} 00:00:00"
        }
        return self._make_request('post', 'JYN1u44ig', data, 'super', nocheck)

    @doc(oQ4T86fmEaH8KwhBSxP3)
    def oQ4T86fmEaH8KwhBSxP3(self, nocheck=False):
        data = {
            "name": self.mixed_random(),
            "desc": "卖场描述" + self.mixed_random(),
            "sort": 11,
            "marketCategory": 1,
            "marketType": 1,
            "sessionFrequency": 0,
            "sessionNum": 1,
            "marketActivityList": self.generate_hourly_sessions(),
            "auctionMarketRuleConfig": {
                "countdownType": 1,
                "merchantLimitList": [
                    3,
                    4
                ],
                "conditionType": 1,
                "lockType": 1,
                "winRuleType": 2,
                "depositType": 1,
                "rangeLimit": 44,
                "failedSessionRule": 2,
                "failedNum": 3,
                "depositPrice": 999,
                "timer": ""
            },
            "auctionMarketArticlesRuleConfig": {
                "minMum": 1,
                "maxMum": 10000,
                "autoAssignType": 1,
                "countdownType": 1,
                "auctionAutoAssignTypeList": [
                    {
                        "categoryId": 1,
                        "brandId": 1,
                        "modelIdList": [
                            9232
                        ],
                        "finenessIdList": [
                            130
                        ],
                        "minValue": 1,
                        "maxValue": 10000
                    }
                ]
            },
            "marketTimeType": 2,
            "isEnable": True,
            "activityStartTime": f"{self.get_the_date()} 00:00:00",
            "activityEndTime": f"{self.get_the_date(days=+20)} 00:00:00"
        }
        return self._make_request('post', 'JYN1u44ig', data, 'super', nocheck)

    @doc(O4GTsiJ6xj3TEtnNe5vS)
    def O4GTsiJ6xj3TEtnNe5vS(self, nocheck=False):
        sessions = self.generate_five_minute_sessions()
        data = {
            "name": self.mixed_random(),
            "desc": "卖场描述" + self.mixed_random(),
            "marketCategory": 1,
            "marketType": 1,
            "sessionFrequency": 0,
            "sessionNum": len(sessions),
            "marketActivityList": sessions,
            "auctionMarketRuleConfig": {
                "countdownType": 1,
                "merchantLimitList": [
                    3,
                    4
                ],
                "conditionType": 1,
                "lockType": 1,
                "winRuleType": 2,
                "depositType": 1,
                "rangeLimit": 44,
                "failedSessionRule": 2,
                "failedNum": 3,
                "depositPrice": 999,
                "timer": ""
            },
            "auctionMarketArticlesRuleConfig": {
                "autoAssignType": 1,
                "minMum": 1,
                "maxMum": 10000,
                "countdownType": 1,
                "auctionAutoAssignTypeList": [
                    {
                        "categoryId": "",
                        "brandId": "",
                        "modelIdList": [],
                        "finenessIdList": []
                    }
                ]
            },
            "sort": 1,
            "marketTimeType": 1,
            "isEnable": True
        }
        return self._make_request('post', 'JYN1u44ig', data, 'super', nocheck)

    @doc(Bkz45n2kH6kLSep0tdDB)
    def Bkz45n2kH6kLSep0tdDB(self, nocheck=False):
        res = self.pc.YVqIQus8roZWysBseaMP0(i=3)
        data = {
            "name": self.mixed_random(),
            "desc": "卖场描述" + self.mixed_random(),
            "sort": 11,
            "marketCategory": 1,
            "marketType": 1,
            "sessionFrequency": 0,
            "sessionNum": 15,
            "marketActivityList": self.generate_five_minute_sessions(),
            "auctionMarketRuleConfig": {
                "countdownType": 1,
                "merchantLimitList": [
                    3,
                    4
                ],
                "conditionType": 1,
                "lockType": 1,
                "winRuleType": 2,
                "depositType": 1,
                "rangeLimit": 44,
                "failedSessionRule": 2,
                "failedNum": 3,
                "depositPrice": 999,
                "timer": ""
            },
            "auctionMarketArticlesRuleConfig": {
                "minMum": 1,
                "maxMum": 10000,
                "autoAssignType": 1,
                "countdownType": 1,
                "auctionAutoAssignTypeList": [
                    {
                        "categoryId": 1,
                        "brandId": 1,
                        "modelIdList": [
                            9232
                        ],
                        "finenessIdList": [
                            130
                        ],
                        "minValue": 1,
                        "maxValue": 10000
                    }
                ]
            },
            "id": res[0]['id'],
            "marketTimeType": 2,
            "isEnable": True,
            "activityStartTime": f"{self.get_the_date()} 00:00:00",
            "activityEndTime": f"{self.get_the_date(days=+20)} 00:00:00"
        }
        return self._make_request('post', 'DZUkrn3ic', data, 'super', nocheck)

    @doc(Qbf3jYdHG3h4d8NIxgTa)
    def Qbf3jYdHG3h4d8NIxgTa(self, nocheck=False):
        res = self.pc.YVqIQus8roZWysBseaMP0(i=3)
        data = {
            "id": res[0]['id']
        }
        return self._make_request('post', 'bZ7hfuHn9', data, 'super', nocheck)

    @doc(SML4kMf2uJffhQbwtUx6)
    def SML4kMf2uJffhQbwtUx6(self, nocheck=False):
        res = self.pc.YVqIQus8roZWysBseaMP0(i=1)
        data = {
            "id": res[0]["id"]
        }
        return self._make_request('post', 'saEQX2AY1', data, 'super', nocheck)

    @doc(gnlGXVVK4aiBrYlOX6oB)
    def gnlGXVVK4aiBrYlOX6oB(self, nocheck=False):
        res = self.pc.YVqIQus8roZWysBseaMP0(i=1)
        res_2 = self.pc.YVqIQus8roZWysBseaMP0(data='b')
        res_3 = self.pc.YVqIQus8roZWysBseaMP0(data='c')
        data = {
            "sessionId": res_2[0]['id'],
            "marketId": res[0]['id'],
            "articlesNoList": [
                res_3[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'BCizVyy8z', data, 'super', nocheck)

    @doc(ZAkeZYaFKKXvRIOgPLOU)
    def ZAkeZYaFKKXvRIOgPLOU(self, nocheck=False):
        res = self.pc.YVqIQus8roZWysBseaMP0(i=2)
        data = {
            'id': res[0]['id']
        }
        return self._make_request('post', 'oXc5khDp2', data, 'super', nocheck)

    @doc(zWLMV5RXaVG7XxYhtEn2)
    def zWLMV5RXaVG7XxYhtEn2(self, nocheck=False):
        res = self.pc.YVqIQus8roZWysBseaMP0(i=2)
        data = {
            "name": self.mixed_random(),
            "desc": '卖场描述' + self.mixed_random(),
            "sort": 1,
            "marketCategory": 1,
            "marketTimeType": 2,
            "marketType": 1,
            "sessionFrequency": 0,
            "sessionNum": 15,
            "marketActivityList": self.generate_five_minute_sessions(),
            "auctionMarketRuleConfig": {
                "countdownType": 1,
                "merchantLimitList": [
                    3,
                    4
                ],
                "conditionType": 1,
                "lockType": 1,
                "winRuleType": 2,
                "depositType": 1,
                "rangeLimit": 44,
                "failedSessionRule": 2,
                "failedNum": 3,
                "depositPrice": 999,
                "timer": ""
            },
            "auctionMarketArticlesRuleConfig": {
                "minMum": 3,
                "maxMum": 100,
                "autoAssignType": 1,
                "countdownType": 1,
                "auctionAutoAssignTypeList": [
                    {
                        "categoryId": 3,
                        "brandId": 802,
                        "modelIdList": [
                            18031
                        ],
                        "finenessIdList": [
                            108,
                            109
                        ],
                        "minValue": 199
                    }
                ]
            },
            "id": res[0]['id'],
            "isEnable": True,
            "activityStartTime": f"{self.get_the_date()} 00:00:00",
            "activityEndTime": f"{self.get_the_date(days=7)} 00:00:00",
        }
        return self._make_request('post', 'DZUkrn3ic', data, 'super', nocheck)

    @doc(pf1dNwfGdkEBsdL4SZfG)
    def pf1dNwfGdkEBsdL4SZfG(self, nocheck=False):
        res = self.pc.YVqIQus8roZWysBseaMP0(i=2)
        data = {
            "id": res[0]["id"]
        }
        return self._make_request('post', 'yywEPKvG3', data, 'super', nocheck)

    @doc(TcjguVZWjalBPkIgMgk2)
    def TcjguVZWjalBPkIgMgk2(self, nocheck=False):
        res = self.pc.YVqIQus8roZWysBseaMP0(i=3)
        data = {
            "name": self.mixed_random(),
            "desc": '卖场描述' + self.mixed_random(),
            "sort": 1,
            "marketCategory": 1,
            "marketTimeType": 2,
            "marketType": 1,
            "sessionFrequency": 0,
            "sessionNum": 15,
            "marketActivityList": self.generate_five_minute_sessions(),
            "auctionMarketRuleConfig": {
                "countdownType": 1,
                "merchantLimitList": [
                    3,
                    4
                ],
                "conditionType": 1,
                "lockType": 1,
                "winRuleType": 2,
                "depositType": 1,
                "rangeLimit": 44,
                "failedSessionRule": 2,
                "failedNum": 3,
                "depositPrice": 999,
                "timer": ""
            },
            "auctionMarketArticlesRuleConfig": {
                "minMum": 3,
                "maxMum": 100,
                "autoAssignType": 1,
                "countdownType": 1,
                "auctionAutoAssignTypeList": [
                    {
                        "categoryId": 3,
                        "brandId": 802,
                        "modelIdList": [
                            18031
                        ],
                        "finenessIdList": [
                            108,
                            109
                        ],
                        "minValue": 199
                    }
                ]
            },
            "id": res[0]['id'],
            "isEnable": True,
            "activityStartTime": f"{self.get_the_date()} 00:00:00",
            "activityEndTime": f"{self.get_the_date(days=7)} 00:00:00"
        }

        return self._make_request('post', 'DZUkrn3ic', data, 'super', nocheck)


class UVTJ3GwNrM(InitializeParams):
    """平台管理|卖场管理|直拍卖场列表"""

    @doc(dkzcGVBC4f0eOkX7psWu)
    @BaseApi.timing_decorator
    def dkzcGVBC4f0eOkX7psWu(self, nocheck=False):
        sessions = self.generate_five_minute_sessions()
        data = {
            "name": self.mixed_random(),
            "desc": '卖场描述' + self.mixed_random(),
            "marketCategory": 2,
            "marketType": 1,
            "sessionFrequency": 0,
            "sessionNum": len(sessions),
            "marketActivityList": sessions,
            "auctionMarketRuleConfig": {
                "countdownType": 2,
                "merchantLimitList": [
                    3
                ],
                "conditionType": 1,
                "lockType": 1,
                "winRuleType": 2,
                "depositType": 1,
                "rangeLimit": 14,
                "failedSessionRule": 1,
                "failedNum": 15,
                "depositPrice": 0,
                "failedArticlesRule": 1,
                "timer": 4
            },
            "auctionMarketArticlesRuleConfig": {
                "autoAssignType": 1,
                "minMum": 1,
                "maxMum": 100000,
                "countdownType": 2,
                "auctionAutoAssignTypeList": [
                    {
                        "categoryId": 1,
                        "brandId": 1,
                        "modelIdList": [
                            9232
                        ],
                        "finenessIdList": [
                            129
                        ],
                        "minValue": 1,
                        "maxValue": 100000
                    }
                ]
            },
            "sort": 1,
            "marketTimeType": 2,
            "isEnable": True,
            "activityStartTime": self.get_formatted_datetime(),
            "activityEndTime": self.get_formatted_datetime(days=+20),
        }
        return self._make_request('post', 'JYN1u44ig', data, 'super', nocheck)

    @doc(YOZXR96FA6wK0SgiwgLh)
    def YOZXR96FA6wK0SgiwgLh(self, nocheck=False):
        sessions = self.generate_five_minute_sessions()
        data = {
            "name": self.mixed_random(),
            "desc": '卖场描述' + self.mixed_random(),
            "sort": 1,
            "marketCategory": 2,
            "marketType": 1,
            "sessionFrequency": 0,
            "sessionNum": len(sessions),
            "marketActivityList": sessions,
            "auctionMarketRuleConfig": {
                "countdownType": 2,
                "merchantLimitList": [
                    4
                ],
                "conditionType": 1,
                "lockType": 1,
                "winRuleType": 2,
                "depositType": 1,
                "rangeLimit": 14,
                "failedSessionRule": 1,
                "failedNum": 15,
                "depositPrice": 0,
                "failedArticlesRule": 1,
                "timer": 3
            },
            "auctionMarketArticlesRuleConfig": {
                "minMum": 1,
                "maxMum": 1000,
                "autoAssignType": 1,
                "countdownType": 2,
                "auctionAutoAssignTypeList": [
                    {
                        "categoryId": "",
                        "brandId": "",
                        "modelIdList": [],
                        "finenessIdList": []
                    }
                ]
            },
            "marketTimeType": 2,
            "isEnable": False,
            "activityStartTime": self.get_formatted_datetime(),
            "activityEndTime": self.get_formatted_datetime(days=+20),
        }
        return self._make_request('post', 'JYN1u44ig', data, 'super', nocheck)

    @doc(S9rWKvQ89U7Uknx1aXeR)
    @BaseApi.timing_decorator
    def S9rWKvQ89U7Uknx1aXeR(self, nocheck=False):
        res = self.pc.BaxRsHzRpoNsTb8fnSa9e(i=1)
        data = {
            "id": res[0]['id']
        }
        return self._make_request('post', 'saEQX2AY1', data, 'super', nocheck)

    @doc(QfMsQBRWh1m3ZmMdtjh1)
    @BaseApi.timing_decorator
    def QfMsQBRWh1m3ZmMdtjh1(self, nocheck=False):
        res = self.pc.BaxRsHzRpoNsTb8fnSa9e(i=3)
        data = {
            "name": self.mixed_random(),
            "desc": '卖场描述' + self.mixed_random(),
            "sort": 1,
            "marketCategory": 2,
            "marketType": 1,
            "sessionFrequency": 0,
            "sessionNum": 1,
            "marketActivityList": self.generate_five_minute_sessions(),
            "auctionMarketRuleConfig": {
                "countdownType": 2,
                "merchantLimitList": [
                    3
                ],
                "conditionType": 1,
                "lockType": 1,
                "winRuleType": 2,
                "failedArticlesRule": 1,
                "depositType": 1,
                "rangeLimit": 14,
                "failedSessionRule": 1,
                "failedNum": 15,
                "depositPrice": 0,
                "timer": 4
            },
            "auctionMarketArticlesRuleConfig": {
                "minMum": 1,
                "maxMum": 1000,
                "autoAssignType": 1,
                "countdownType": 2,
                "auctionAutoAssignTypeList": [
                    {
                        "categoryId": 1,
                        "brandId": 1,
                        "modelIdList": [
                            7692
                        ],
                        "finenessIdList": [
                            129
                        ],
                        "minValue": 1,
                        "maxValue": 100000
                    }
                ]
            },
            "id": res[0]['id'],
            "marketTimeType": 2,
            "isEnable": True,
            "activityStartTime": self.get_formatted_datetime(),
            "activityEndTime": self.get_formatted_datetime(days=+20),
        }
        return self._make_request('post', 'DZUkrn3ic', data, 'super', nocheck)

    @doc(i2PADX8AIUDmt1eH6XmL)
    @BaseApi.timing_decorator
    def i2PADX8AIUDmt1eH6XmL(self, nocheck=False):
        res = self.pc.BaxRsHzRpoNsTb8fnSa9e(i=1)
        res_2 = self.pc.BaxRsHzRpoNsTb8fnSa9e(data='b')
        res_3 = self.pc.BaxRsHzRpoNsTb8fnSa9e(data='c')
        data = {
            "sessionId": res_2[0]['id'],
            "marketId": res[0]['id'],
            "articlesNoList": [
                res_3[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'BCizVyy8z', data, 'super', nocheck)


class IRgfq9glDm(InitializeParams):
    """平台管理|商户管理"""


class RzBsOiNk4l(InitializeParams):
    """平台管理|同售管理|商品审核"""


class WlAFVePJlH(InitializeParams):
    """平台管理|订单管理|订单审核"""

    @doc(BBiltLX4GA5cpSCyECIP)
    @BaseApi.timing_decorator
    def BBiltLX4GA5cpSCyECIP(self, nocheck=False):
        res = self.pc.V3LpfoN0H354ztNVHPWtf()
        data = {
            "auditStatus": 2,
            "auditRemark": "通过",
            "receipt": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com//erp-imgfiles/%2Fepbox-erp/20250820/WIehcT%2B7sg/I4FjLToJM%2Bw%3D%3D.jpg",
            "businessNo": res[0]['orderNo'],
            "id": res[0]['id']
        }
        return self._make_request('put', 'LjlGQV76c', data, 'platform', nocheck)

    @doc(FMRI6lTSPPbGRqorxtkt)
    @BaseApi.timing_decorator
    def FMRI6lTSPPbGRqorxtkt(self, nocheck=False):
        res = self.pc.V3LpfoN0H354ztNVHPWtf()
        data = {
            "auditStatus": 3,
            "auditRemark": "拒绝",
            "receipt": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com//erp-imgfiles/%2Fepbox-erp/20250820/WIehcT%2B7sg/I4FjLToJM%2Bw%3D%3D.jpg",
            "businessNo": res[0]['orderNo'],
            "id": res[0]['id']
        }
        return self._make_request('put', 'LjlGQV76c', data, 'platform', nocheck)


class SMtCxoJnmP(InitializeParams):
    """平台管理|消息管理|消息发布列表"""

    @doc(G9C97BkpOngHG41cgA0L)
    @BaseApi.timing_decorator
    def G9C97BkpOngHG41cgA0L(self, nocheck=False):
        res = self.pc.IyY9m4jNrW6D0vQNpkgVH()
        data = {
            "auditResult": "1",
            "ids": [
                res[0]['id']
            ],
            "selectType": "1",
            "operationType": 8
        }
        return self._make_request('post', 'UeOgoRjwZ', data, 'platform', nocheck)

    @doc(pj4bj85GPh759JlXB1ir)
    @BaseApi.timing_decorator
    def pj4bj85GPh759JlXB1ir(self, nocheck=False):
        res = self.pc.IyY9m4jNrW6D0vQNpkgVH()
        data = {
            "auditResult": "2",
            "reason": "test1",
            "platformReason": "test1",
            "ids": [
                res[0]['id']
            ],
            "selectType": "1",
            "operationType": 8
        }
        return self._make_request('post', 'UeOgoRjwZ', data, 'platform', nocheck)

    @doc(pdEsg1lHJfR191fcMim5)
    @BaseApi.timing_decorator
    def pdEsg1lHJfR191fcMim5(self, nocheck=False):
        res = self.pc.IyY9m4jNrW6D0vQNpkgVH()
        data = {
            "id": res[0]['id'],
            "selectType": "1",
            "operationType": 6
        }
        return self._make_request('post', 'PDIWnRhr2', data, 'platform', nocheck)


class V35pu3YhqH(InitializeParams):
    """平台管理|壹准拍机|售后管理|申诉管理"""

    @doc(X4Qg6ocEen8r1SwVi5GT)
    @BaseApi.timing_decorator
    def X4Qg6ocEen8r1SwVi5GT(self, nocheck=False):
        res = self.pc.NLUkzWtFzjZSO2vR8Yhhb(i=0)
        data = {
            "id": res[0]['id'],
            "auctionAfterSalesOrderAuditResult": {
                "auditResult": 1,
                "handleMode": 1
            },
            "amount": 1
        }
        return self._make_request('post', 'KLywO7at3', data, 'platform', nocheck)

    @doc(Ms6Xyable2b9S87LhPZd)
    @BaseApi.timing_decorator
    def Ms6Xyable2b9S87LhPZd(self, nocheck=False):
        res = self.pc.NLUkzWtFzjZSO2vR8Yhhb(i=0)
        obj = res[0]['afterOrderNo']
        ParamCache.cache_object({"afterOrderNo": obj}, 'practical.json')
        data = {
            "id": res[0]['id'],
            "auctionAfterSalesOrderAuditResult": {
                "auditResult": 1,
                "handleMode": 2
            },
            "amount": 2
        }
        return self._make_request('post', 'KLywO7at3', data, 'platform', nocheck)

    @doc(Or5VGbcLZ6drxl8wkMSR)
    @BaseApi.timing_decorator
    def Or5VGbcLZ6drxl8wkMSR(self, nocheck=False):
        res = self.pc.NLUkzWtFzjZSO2vR8Yhhb(i=0)
        obj = res[0]['afterOrderNo']
        ParamCache.cache_object({"afterOrderNo": obj}, 'practical.json')
        data = {
            "id": res[0]['id'],
            "auctionAfterSalesOrderAuditResult": {
                "auditResult": 1,
                "handleMode": 3
            }
        }
        return self._make_request('post', 'KLywO7at3', data, 'super', nocheck)


if __name__ == '__main__':
    api = ()
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
