# coding: utf-8
from common.base_api import BaseApi
from common.base_params import InitializeParams
from config.user_info import INFO
from common.import_desc import *

qualityCategoryList = BaseApi.load_json_file('request_quality.json')['qualityCategoryList']
optionIdList = BaseApi.load_json_file('request_quality.json')['optionIdList']
backfillList = BaseApi.load_json_file('request_quality.json')['backfillList']


class ZG6fRe5zTB(InitializeParams):
    """二手通小程序|首页|帮卖"""

    @doc(gSy4Vk4VOP22wEagmKtu)
    def gSy4Vk4VOP22wEagmKtu(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='3')
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "helpSellTenantId": INFO['main_help_sell_tenant_id'],
            "batchRemark": "备注",
            "settlementType": 1
        }
        return self._make_request('post', 'NE7Tz9kCF', data, 'main', nocheck)

    @doc(T7vjIsc0mkOJLNIOlGHR)
    def T7vjIsc0mkOJLNIOlGHR(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='3')
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "batchRemark": "",
            "helpSellTenantId": INFO['main_help_sell_tenant_id'],
            "settlementType": 2
        }

        return self._make_request('post', 'NE7Tz9kCF', data, 'main', nocheck)

    @doc(Q2CD7BU5QG3ce40zfWJ6)
    def Q2CD7BU5QG3ce40zfWJ6(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='3')
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "batchRemark": "",
            "helpSellTenantId": INFO['main_help_sell_tenant_id'],
            "settlementType": 3
        }
        return self._make_request('post', 'NE7Tz9kCF', data, 'main', nocheck)

    @doc(Th8rhqqbFWasw2m5ca09)
    def Th8rhqqbFWasw2m5ca09(self, nocheck=False):
        res = self.pc.PurkQXBjQXG3tz8hUb1SF(i='wsg')
        data = {
            "walletAccountNo": INFO['main_wallet_account_no'],
            "estimateFreight": 10,
            "payWay": "1",
            "expressCompanyId": "1",
            "expressCompanyName": "顺丰",
            "expectPostTimeStart": self.get_formatted_datetime(),
            "senderName": INFO['customer_name'],
            "senderProvinceId": INFO['province_id'],
            "senderProvinceName": INFO['province_name'],
            "senderCityId": INFO['city_id'],
            "senderCityName": INFO['city_name'],
            "senderCountyId": INFO['county_id'],
            "senderCountyName": INFO['county_name'],
            "senderAddress": INFO['detailed_address'],
            "type": 1,
            "batchId": res[0]['helpSellBatchId'],
            "batchNo": res[0]['batchNo'],
            "orderIdList": [
                res[0]['orderNo']
            ],
            "senderPhone": INFO['receiving_phone'],
            "recipientName": INFO['vice_account'],
            "recipientPhone": INFO['shipping_phone'],
            "recipientProvinceId": INFO['province_id'],
            "recipientProvinceName": INFO['province_name'],
            "recipientCityId": INFO['city_id'],
            "recipientCityName": INFO['city_name'],
            "recipientCountyId": INFO['county_id'],
            "recipientCountyName": INFO['county_name'],
            "recipientAddress": INFO['detailed_address']
        }

        return self._make_request('post', 'mstJQUeyv', data, 'main', nocheck)

    @doc(KcQ8VA99jSgpYr00tyLM)
    def KcQ8VA99jSgpYr00tyLM(self, nocheck=False):
        res = self.pc.PurkQXBjQXG3tz8hUb1SF(i='wsg')
        data = {
            "expressCompanyName": "顺丰",
            "expressNo": self.jd,
            "type": "2",
            "batchId": res[0]['helpSellBatchId'],
            "batchNo": res[0]['batchNo'],
            "orderIdList": [
                res[0]['orderNo']
            ],
            "senderPhone": INFO['receiving_phone'],
            "recipientName": INFO['vice_account'],
            "recipientPhone": INFO['shipping_phone'],
            "recipientProvinceId": INFO['province_id'],
            "recipientProvinceName": INFO['province_name'],
            "recipientCityId": INFO['city_id'],
            "recipientCityName": INFO['city_name'],
            "recipientCountyId": INFO['county_id'],
            "recipientCountyName": INFO['county_name'],
            "recipientAddress": INFO['detailed_address']
        }
        return self._make_request('post', 'mstJQUeyv', data, 'main', nocheck)

    @doc(Zng3AfJbx2o0lS97ypXT)
    def Zng3AfJbx2o0lS97ypXT(self, nocheck=False):
        res = self.pc.PurkQXBjQXG3tz8hUb1SF(i='wsg')
        data = {
            "type": "3",
            "batchId": res[0]['helpSellBatchId'],
            "batchNo": res[0]['batchNo'],
            "orderIdList": [
                res[0]['orderNo']
            ],
            "senderPhone": INFO['receiving_phone'],
            "recipientName": INFO['vice_account'],
            "recipientPhone": INFO['shipping_phone'],
            "recipientProvinceId": INFO['province_id'],
            "recipientProvinceName": INFO['province_name'],
            "recipientCityId": INFO['city_id'],
            "recipientCityName": INFO['city_name'],
            "recipientCountyId": INFO['county_id'],
            "recipientCountyName": INFO['county_name'],
            "recipientAddress": INFO['detailed_address']
        }
        return self._make_request('post', 'mstJQUeyv', data, 'main', nocheck)

    @doc(wiM0WjiOzoeKyaTG2PrC)
    def wiM0WjiOzoeKyaTG2PrC(self, nocheck=False):
        res = self.pc.PurkQXBjQXG3tz8hUb1SF(i='wr')
        data = {
            "orderNoList": [
                res[0]['orderNo']
            ]
        }
        return self._make_request('post', 'VjS268Bbk', data, 'main', nocheck)

    @doc(ABD3XVRJTfP5w1yu4jHp)
    def ABD3XVRJTfP5w1yu4jHp(self, nocheck=False):
        res = self.pc.PurkQXBjQXG3tz8hUb1SF(i='wb')
        data = {
            "orderNoList": [
                res[0]['orderNo']
            ]
        }
        return self._make_request('post', 'VjS268Bbk', data, 'main', nocheck)

    @doc(q8V7X7imCb99t9ZvMfo8)
    def q8V7X7imCb99t9ZvMfo8(self, nocheck=False):
        res = self.pc.PurkQXBjQXG3tz8hUb1SF(i='wbi')
        data = {
            "orderNoList": [
                res[0]['orderNo']
            ]
        }
        return self._make_request('post', 'VjS268Bbk', data, 'main', nocheck)

    @doc(LMDMfMzEmvr5s6wtfKmX)
    def LMDMfMzEmvr5s6wtfKmX(self, nocheck=False):
        res = self.pc.PurkQXBjQXG3tz8hUb1SF(i='wsr')
        data = {
            "orderNoList": [
                res[0]['orderNo']
            ]
        }
        return self._make_request('post', 'VjS268Bbk', data, 'main', nocheck)

    @doc(X6ssuFYCjqGxvThVflOf)
    def X6ssuFYCjqGxvThVflOf(self, nocheck=False):
        res = self.pc.PurkQXBjQXG3tz8hUb1SF(i='wb')
        data = {
            "orderNo": res[0]['orderNo'],
            "description": "备注"
        }
        return self._make_request('post', 'Upm9s0CAF', data, 'main', nocheck)

    @doc(bFv5K1H1hfIreNfxq0N7)
    def bFv5K1H1hfIreNfxq0N7(self, nocheck=False):
        res = self.pc.PurkQXBjQXG3tz8hUb1SF(i='wrg')
        data = {
            "orderNoList": [
                res[0]['orderNo']
            ]
        }
        return self._make_request('post', 'GOF01CbL0', data, 'main', nocheck)

    @doc(YmNQXNyn0cgOev94cyUn)
    def YmNQXNyn0cgOev94cyUn(self, nocheck=False):
        res = self.pc.PurkQXBjQXG3tz8hUb1SF(i='rig')
        data = {
            "orderIdList": [
                res[0]['orderNo']
            ]
        }
        return self._make_request('post', 'qqa25IOcj', data, 'main', nocheck)

    @doc(pEdX4tcJCCi2ANETDgLh)
    def pEdX4tcJCCi2ANETDgLh(self, nocheck=False):
        res = self.pc.PurkQXBjQXG3tz8hUb1SF(i='rig')
        res_2 = self.pc.D2grXOWzOv0I5f5rFGf6A()
        data = {
            "logisticsNo": res_2[0]['logisticsNo'],
            "articlesList": [
                {
                    "articlesNo": res[0]['articlesNo']
                }
            ],
            "warehouseId": INFO['main_item_warehouse_id'],
            "quickOperation": 0
        }
        return self._make_request('post', 'oqInLCkEY', data, 'main', nocheck)


class KUHmqHA6mE(InitializeParams):
    """二手通小程序|首页|库存"""

    @doc(individual_item_counting)
    def create_a_new_inventory_count(self, nocheck=False):
        data = {
            'stockUserId': -1
        }
        return self._make_request('post', 'FnNQ9ZVWA', data, 'main', nocheck)

    @doc(individual_item_counting)
    def submit_an_inventory_count(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp()
        res_2 = self.pc.Ux7lF2b6qktEytPTzyaQW()
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "stockNo": res_2[0]['stockNo']
        }
        return self._make_request('post', 'M2mrdmchM', data, 'main', nocheck)

    @doc(FpdSwapLHorzSgUTXzO3)
    def FpdSwapLHorzSgUTXzO3(self, nocheck=False):
        self.create_a_new_inventory_count()
        self.submit_an_inventory_count()
        res = self.pc.Ux7lF2b6qktEytPTzyaQW()
        data = {
            "stockNo": res[0]['stockNo']
        }
        return self._make_request('post', 'fSaKNcmwJ', data, 'main', nocheck)

    @doc(NolDGk9PEn4XYz8LrUgH)
    def NolDGk9PEn4XYz8LrUgH(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='3')
        data = {
            "type": "1",
            "userId": INFO['main_user_id'],
            "remark": "",
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "createBy": INFO['super_admin_account']
        }
        return self._make_request('post', 'Hle0lvsut', data, 'main', nocheck)

    @doc(AHeVie0Oup6y9tNMelfQ)
    def AHeVie0Oup6y9tNMelfQ(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='3')
        data = {
            "type": "2",
            "userId": INFO['main_user_id'],
            "remark": "",
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "createBy": INFO['super_admin_account']
        }
        return self._make_request('post', 'Hle0lvsut', data, 'main', nocheck)

    @doc(cj8y7BldKp6aX4lbkB29)
    def cj8y7BldKp6aX4lbkB29(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='3')
        data = {
            "type": "3",
            "userId": INFO['main_user_id'],
            "remark": "",
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "createBy": INFO['super_admin_account']
        }
        return self._make_request('post', 'Hle0lvsut', data, 'main', nocheck)

    @doc(B0dbkcikzi0su2qFAEqM)
    def B0dbkcikzi0su2qFAEqM(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='3')
        data = {
            "type": "4",
            "userId": INFO['main_user_id'],
            "remark": "",
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "createBy": INFO['super_admin_account']
        }
        return self._make_request('post', 'Hle0lvsut', data, 'main', nocheck)

    @doc(djAbq91arWjnM274GmSY)
    def djAbq91arWjnM274GmSY(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='3')
        data = {
            "type": "5",
            "userId": INFO['main_user_id'],
            "remark": "",
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "createBy": INFO['super_admin_account']
        }
        return self._make_request('post', 'Hle0lvsut', data, 'main', nocheck)

    @doc(wEfefFG7nEo3Kan0I3cY)
    def wEfefFG7nEo3Kan0I3cY(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='3')
        data = {
            "type": "6",
            "userId": INFO['main_user_id'],
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "createBy": INFO['super_admin_account']
        }
        return self._make_request('post', 'Hle0lvsut', data, 'main', nocheck)

    @doc(rOtk4WU5CRaxiuoJLvh6)
    def rOtk4WU5CRaxiuoJLvh6(self, nocheck=False):
        res = self.pc.D2grXOWzOv0I5f5rFGf6A()
        res_2 = self.pc.WbrwTMcyqVsFRjRMcUD9e()
        data = {
            "logisticsNo": res[0]['logisticsNo'],
            "articlesList": [
                {
                    "articlesNo": res_2[0]['articlesNo']
                }
            ],
            "warehouseId": INFO['main_item_warehouse_id'],
            "quickOperation": 0
        }
        return self._make_request('post', 'oqInLCkEY', data, 'main', nocheck)

    @doc(VDDb6S8keIp4qBsOIcxz)
    def VDDb6S8keIp4qBsOIcxz(self, nocheck=False):
        res = self.pc.D2grXOWzOv0I5f5rFGf6A()
        res_2 = self.pc.WbrwTMcyqVsFRjRMcUD9e()
        data = {
            "logisticsNo": res[0]['logisticsNo'],
            "articlesList": [
                {
                    "articlesNo": res_2[0]['articlesNo']
                }
            ],
            "warehouseId": INFO['main_item_warehouse_id'],
            "quickOperation": "1",
            "purchaseOrdersArticlesDTO": {
                "articlesNoList": [
                    res_2[0]['articlesNo']
                ],
                "createBy": f"admin({INFO['main_account']})",
                "userId": INFO['main_user_id'],
                "type": "1",
                "remark": ""
            }
        }
        return self._make_request('post', 'oqInLCkEY', data, 'main', nocheck)

    @doc(PylpYfWMSCO7tb8yWDov)
    def PylpYfWMSCO7tb8yWDov(self, nocheck=False):
        res = self.pc.D2grXOWzOv0I5f5rFGf6A()
        res_2 = self.pc.WbrwTMcyqVsFRjRMcUD9e()
        data = {
            "logisticsNo": res[0]['logisticsNo'],
            "articlesList": [
                {
                    "articlesNo": res_2[0]['articlesNo']
                }
            ],
            "warehouseId": INFO['main_item_warehouse_id'],
            "quickOperation": "1",
            "purchaseOrdersArticlesDTO": {
                "articlesNoList": [
                    res_2[0]['articlesNo']
                ],
                "createBy": f"admin({INFO['main_account']})",
                "userId": INFO['main_user_id'],
                "type": "2",
                "remark": ""
            }
        }
        return self._make_request('post', 'oqInLCkEY', data, 'main', nocheck)

    @doc(Bb6rtOhNILeRK1H3CswE)
    def Bb6rtOhNILeRK1H3CswE(self, nocheck=False):
        res = self.pc.D2grXOWzOv0I5f5rFGf6A()
        res_2 = self.pc.WbrwTMcyqVsFRjRMcUD9e()
        data = {
            "logisticsNo": res[0]['logisticsNo'],
            "articlesList": [
                {
                    "articlesNo": res_2[0]['articlesNo']
                }
            ],
            "warehouseId": INFO['main_item_warehouse_id'],
            "quickOperation": "1",
            "purchaseOrdersArticlesDTO": {
                "articlesNoList": [
                    res_2[0]['articlesNo']
                ],
                "createBy": f"admin({INFO['main_account']})",
                "userId": INFO['main_user_id'],
                "type": "3",
                "remark": ""
            }
        }
        return self._make_request('post', 'oqInLCkEY', data, 'main', nocheck)

    @doc(gwkXCubQ6Kh0UhJCOUp6)
    def gwkXCubQ6Kh0UhJCOUp6(self, nocheck=False):
        res = self.pc.D2grXOWzOv0I5f5rFGf6A()
        res_2 = self.pc.WbrwTMcyqVsFRjRMcUD9e()
        data = {
            "logisticsNo": res[0]['logisticsNo'],
            "articlesList": [
                {
                    "articlesNo": res_2[0]['articlesNo']
                }
            ],
            "warehouseId": INFO['main_item_warehouse_id'],
            "quickOperation": "1",
            "purchaseOrdersArticlesDTO": {
                "articlesNoList": [
                    res_2[0]['articlesNo']
                ],
                "createBy": f"admin({INFO['main_account']})",
                "userId": INFO['main_user_id'],
                "type": "4",
                "remark": ""
            }
        }
        return self._make_request('post', 'oqInLCkEY', data, 'main', nocheck)

    @doc(K9U0fcTlznz9x5lbCPxH)
    def K9U0fcTlznz9x5lbCPxH(self, nocheck=False):
        res = self.pc.D2grXOWzOv0I5f5rFGf6A()
        res_2 = self.pc.WbrwTMcyqVsFRjRMcUD9e()
        data = {
            "logisticsNo": res[0]['logisticsNo'],
            "articlesList": [
                {
                    "articlesNo": res_2[0]['articlesNo']
                }
            ],
            "warehouseId": INFO['main_item_warehouse_id'],
            "quickOperation": "1",
            "purchaseOrdersArticlesDTO": {
                "articlesNoList": [
                    res_2[0]['articlesNo']
                ],
                "createBy": f"admin({INFO['main_account']})",
                "userId": INFO['main_user_id'],
                "type": "5",
                "remark": ""
            }
        }
        return self._make_request('post', 'oqInLCkEY', data, 'main', nocheck)

    @doc(wrfq9qJlYzprjxoG4WmO)
    def wrfq9qJlYzprjxoG4WmO(self, nocheck=False):
        res = self.pc.D2grXOWzOv0I5f5rFGf6A()
        res_2 = self.pc.WbrwTMcyqVsFRjRMcUD9e()
        data = {
            "logisticsNo": res[0]['logisticsNo'],
            "articlesList": [
                {
                    "articlesNo": res_2[0]['articlesNo']
                }
            ],
            "warehouseId": INFO['main_item_warehouse_id'],
            "quickOperation": "1",
            "purchaseOrdersArticlesDTO": {
                "articlesNoList": [
                    res_2[0]['articlesNo']
                ],
                "createBy": f"admin({INFO['main_account']})",
                "userId": INFO['main_user_id'],
                "type": "6",
                "remark": ""
            }
        }
        return self._make_request('post', 'oqInLCkEY', data, 'main', nocheck)

    @doc(AXJg2IWq4WbiLzdWv6RK)
    def AXJg2IWq4WbiLzdWv6RK(self, nocheck=False):
        res = self.pc.Mb5NtymgNZq58BhIE7Umz()
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'CNE12WKlU', data, 'main', nocheck)

    @doc(gUlS03xcTzSc6opuoZXv)
    def gUlS03xcTzSc6opuoZXv(self, nocheck=False):
        res = self.pc.D2grXOWzOv0I5f5rFGf6A()
        res_2 = self.pc.WbrwTMcyqVsFRjRMcUD9e()
        data = {
            "logisticsNo": res[0]['logisticsNo'],
            "articlesList": [
                {
                    "articlesNo": res_2[0]['articlesNo'],
                }
            ],
            "warehouseId": INFO['main_item_warehouse_id'],
            "quickOperation": 0
        }
        return self._make_request('post', 'oqInLCkEY', data, 'main', nocheck)


class Htxslq7CN1(InitializeParams):
    """二手通小程序|首页|采购"""

    @doc(iuU1ZpZnIF2nfnGtBxhK)
    def iuU1ZpZnIF2nfnGtBxhK(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i=1)
        res_2 = self.pc.D2grXOWzOv0I5f5rFGf6A()
        data = {
            "logisticsNo": res_2[0]['logisticsNo'],
            "articlesList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                }
            ],
            "warehouseId": INFO['main_item_warehouse_id'],
            "quickOperation": 0
        }
        return self._make_request('post', 'oqInLCkEY', data, 'main', nocheck)

    @doc(LiiO1y6jvNGLbSiTWHmU)
    def LiiO1y6jvNGLbSiTWHmU(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i=1)
        res_2 = self.pc.D2grXOWzOv0I5f5rFGf6A()
        data = {
            "logisticsNo": res_2[0]['logisticsNo'],
            "articlesList": [
                {
                    "articlesNo": res[0]['articlesNo']
                }
            ],
            "warehouseId": INFO['main_item_warehouse_id'],
            "quickOperation": "1",
            "purchaseOrdersArticlesDTO": {
                "articlesNoList": [
                    res[0]['articlesNo']
                ],
                "createBy": INFO['super_admin_account'],
                "userId": INFO['main_user_id'],
                "type": "1",
                "remark": ""
            }
        }
        return self._make_request('post', 'oqInLCkEY', data, 'main', nocheck)

    @doc(N8ZYbEQ5wRbTFaYhk54m)
    def N8ZYbEQ5wRbTFaYhk54m(self, nocheck=False):
        time = self.get_current_timestamp_ms()
        jd = self.jd
        imei = self.imei
        data = {
            "payState": "2",
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "purchaseTime": self.get_formatted_datetime(),
            "userId": INFO['main_user_id'],
            "remark": self.serial,
            "logisticsPrice": "11",
            "logisticsNo": jd,
            "state": "4",
            "accountName": INFO['main_account_name'],
            "accountNo": INFO['main_account_no'],
            "purchaseOrdersArticlesDTOList": [
                {
                    "imei": imei,
                    "warehouseId": INFO['main_item_warehouse_id'],
                    "articlesRemake": self.serial,
                    "purchasePrice": "11",
                    "platformArticlesNo": self.serial,
                    "logisticsNo": jd,
                    "purchaseArticlesInfoDTO": {
                        "imei": imei,
                        "serialNo": self.serial,
                        "platformOrderNo": self.serial,
                        "num": "",
                        "price": "11",
                        "modelId": "13352",
                        "modelName": "Watch GT 4",
                        "categoryName": "智能手表",
                        "brandName": "华为",
                        "selectList": [],

                        "brandId": "8",
                        "activeType": "5",
                        "reflection": "[2]",
                        "caseMaterialId": "",
                        "connectId": "",
                        "caseSizeId": "",
                        "machineTypeId": "",
                        "finenessId": "",
                        "platform": self.serial,
                        "desc": "235235235",
                        "selectListStr": "",
                        "articlesTypeId": "5",
                        "articlesTypeName": "智能手表",
                        "id": time
                    }
                }
            ],
            "purchaseUserName": INFO['main_purchase_user_name'],
            "orderPayInfoList": [],
            "purchaseOrdersArticlesDTO": {},
            "quickOperation": "0"
        }
        return self._make_request('post', 'dtk8ABnq4', data, 'main', nocheck)

    @doc(KKVgCekmpYe0dXD1TQoP)
    def KKVgCekmpYe0dXD1TQoP(self, nocheck=False):
        ms_time = self.get_current_timestamp_ms()
        jd = self.jd
        imei = self.imei
        data = {
            "payState": "2",
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "purchaseTime": self.get_formatted_datetime(),
            "userId": INFO['main_user_id'],
            "remark": "备注",
            "logisticsPrice": "11",
            "logisticsNo": jd,
            "state": "4",
            "accountName": INFO['main_account_name'],
            "accountNo": INFO['main_account_no'],
            "purchaseOrdersArticlesDTOList": [
                {
                    "imei": imei,
                    "warehouseId": INFO['main_item_warehouse_id'],
                    "articlesRemake": self.serial,
                    "purchasePrice": "16",
                    "platformArticlesNo": self.serial,
                    "logisticsNo": jd,
                    "purchaseArticlesInfoDTO": {
                        "imei": imei,
                        "serialNo": self.serial,
                        "platformOrderNo": self.serial,
                        "num": "",
                        "price": "16",
                        "modelId": "7692",
                        "modelName": "iPhone 5S",
                        "categoryName": "手机",
                        "brandName": "苹果",
                        "selectList": [],
                        "brandId": "1",
                        "activeType": "1",
                        "reflection": "[0]",
                        "smallModelId": "",
                        "buyChannelId": "",
                        "colorId": "",
                        "romId": "",
                        "batteryHealthId": "",
                        "warrantyDurationId": "",
                        "machineTypeId": "",
                        "finenessId": "",
                        "platform": self.serial,
                        "desc": "22222222333333",
                        "selectListStr": "",
                        "articlesTypeId": "1",
                        "articlesTypeName": "手机",
                        "id": ms_time
                    }
                }
            ],
            "purchaseUserName": INFO['main_purchase_user_name'],
            "orderPayInfoList": [],
            "purchaseOrdersArticlesDTO": {
                "createBy": INFO['super_admin_account'],
                "userId": INFO['main_user_id'],
                "type": "2",
                "remark": "22223333"
            },
            "quickOperation": "1"
        }

        return self._make_request('post', 'dtk8ABnq4', data, 'main', nocheck)


class JeJHxqrd7e(InitializeParams):
    """二手通小程序|首页|质检"""

    @doc(GCcaGfhZIx5dmNXOGPoG)
    def GCcaGfhZIx5dmNXOGPoG(self, nocheck=False):
        res = self.pc.UJwDgUZKhNNEKJEIdEAKw()
        data = {
            "presalePrice": "1000",
            "imageUrl": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com//erp-imgfiles/%2Fepbox-erp/20260206/WIehcT%2B7sg/I4FjLToJM%2Bw%3D%3D.jpg",
            "saleImageUrl": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com//erp-imgfiles/%2Fepbox-erp/20260206/WIehcT%2B7sg/I4FjLToJM%2Bw%3D%3D.jpg",
            "receiveId": INFO['special_user_id'],
            "type": "6",
            "deliveryRemark": "移交说明",
            "qualityCategoryList": qualityCategoryList,
            "articlesInfo": {
                "imei": res[0]['imei'],
                "brandName": res[0]['brandName'],
                "modelName": res[0]['modelName'],
                "modelId": res[0]['modelId'],
                "brandId": res[0]['brandId'],
                "serialNo": res[0]['platformArticlesNo'],
                "smallModelId": 72,
                "buyChannelId": 16,
                "colorId": 1712,
                "romId": 41,
                "ramId": None,
                "finenessId": 37,
                "machineTypeId": 862,
                "warrantyDurationId": 23005,
                "batteryHealthId": 23028,
                "finenessName": "充新",
                "colorName": "黑色钛金属",
                "romName": "256G",
                "buyChannelName": "国行",
                "smallModelName": "其他型号",
                "machineTypeName": "二手优品"
            },
            "articlesNo": res[0]['articlesNo'],
            "optionIdList": optionIdList,
            "createBy": INFO['main_account'],
            "templateId": 2,
            "isOther": 1
        }
        return self._make_request('post', 'Wev5hkW8C', data, 'main', nocheck)

    @doc(TIdR7zy3q7gsA97wufMG)
    def TIdR7zy3q7gsA97wufMG(self, nocheck=False):
        res = self.pc.UJwDgUZKhNNEKJEIdEAKw()
        res_2 = self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2, j=5)
        data = {
            "articlesInfo": {
                "imei": res[0]['imei'],
                "brandName": res[0]['brandName'],
                "modelName": res[0]['modelName'],
                "modelId": res[0]['modelId'],
                "brandId": res[0]['brandId'],
            },
            "qualityCategoryList": [
                {
                    "systematicName": "无线功能",
                    "qualityContentList": [
                        {
                            "id": 289,
                            "qualityName": "WiFi功能",
                            "isNormal": 0,
                            "optionList": [
                                {
                                    "id": "475"
                                }
                            ],
                            "selectedValue": "475",
                            "value": "475"
                        }
                    ]
                },
                {
                    "systematicName": "充电功能",
                    "qualityContentList": [
                        {
                            "id": 615,
                            "qualityName": "有线充电",
                            "isNormal": 0,
                            "optionList": [
                                {
                                    "id": "663"
                                }
                            ],
                            "selectedValue": "663",
                            "value": "663"
                        }
                    ]
                },
                {
                    "systematicName": "其他功能",
                    "qualityContentList": [
                        {
                            "id": 607,
                            "qualityName": "数据连接功能",
                            "isNormal": 0,
                            "optionList": [
                                {
                                    "id": "655"
                                }
                            ],
                            "selectedValue": "655",
                            "value": "655"
                        }
                    ]
                },
                {
                    "systematicName": "系统情况",
                    "qualityContentList": [
                        {
                            "id": 391,
                            "qualityName": "开机情况",
                            "isNormal": 0,
                            "optionList": [
                                {
                                    "id": "7395"
                                }
                            ],
                            "selectedValue": "7395",
                            "value": "7395"
                        }
                    ]
                }
            ],
            "optionIdList": [
                "475",
                "663",
                "655",
                "7395"
            ],
            "articlesNo": res_2[0]['articlesNo'],
            "templateId": 2,
            "presalePrice": "11",
            "isOther": 1,
            "imageUrl": "",
            "saleImageUrl": "",
            "saleVideoUrl": "",
            "type": "2",
            "receiveId": INFO['main_user_id'],
            "createBy": ""
        }
        return self._make_request('post', 'Wev5hkW8C', data, 'main', nocheck)

    @doc(fRpQsQhibllGcUnGvL4b)
    def fRpQsQhibllGcUnGvL4b(self, nocheck=False):
        data = {
            "articlesInfo": {
                "imei": self.imei,
                "serialNo": None,
                "colorName": None,
                "romName": None,
                "buyChannelName": None,
                "smallModelName": None,
                "finenessId": 37,
                "finenessName": "充新",
                "machineTypeName": None,
                "articlesTypeId": "1",
                "articlesTypeName": "手机",
                "brandId": "1",
                "brandName": "苹果",
                "modelId": "7694",
                "modelName": "iPhone 6 Plus"
            },
            "qualityCategoryList": qualityCategoryList,
            "optionIdList": optionIdList,
            "templateId": 2,
            "presalePrice": "11",
            "imageUrl": "",
            "saleImageUrl": "",
            "saleVideoUrl": "",
            "isOther": 1,
            "isUpdateReport": False
        }
        return self._make_request('post', 'GTxGeV0Dn', data, 'main', nocheck)

    @doc(frFIFPmzY5aUapx40XDq)
    def frFIFPmzY5aUapx40XDq(self, nocheck=False):
        jd = self.jd
        data = {
            "payState": "1",
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "purchaseTime": self.get_formatted_datetime(),
            "userId": INFO['main_user_id'],
            "remark": "22223333",
            "logisticsPrice": "2",
            "logisticsNo": jd,
            "state": "3",
            "accountName": INFO['main_account_name'],
            "accountNo": INFO['main_account_no'],
            "purchaseOrdersArticlesDTOList": [
                {
                    "imei": self.imei,
                    "warehouseId": "",
                    "purchasePrice": "11",
                    "logisticsNo": jd,
                    "purchaseArticlesInfoDTO": {
                        "id": self.get_current_timestamp_ms(),
                        "otherArticlesNo": "3824438606",
                        "articlesTypeId": 1,
                        "brandId": 1,
                        "brandName": "苹果",
                        "modelId": 7694,
                        "modelName": "iPhone 6 Plus",
                        "serialNo": None,
                        "imei": self.imei,
                        "skuInfo": "苹果 iPhone 6 Plus 充新",
                        "finenessId": 37,
                        "finenessName": "充新",
                        "qualityType": 1,
                        "qualityTypeStr": "人工选择",
                        "qualityNo": "2025092943182",
                        "articlesStatus": 1,
                        "articlesStatusStr": "非库内物品",
                        "userId": INFO['main_account_no'],
                        "userName": INFO['super_admin_account'],
                        "userPhone": INFO['receiving_phone'],
                        "createTime": self.get_formatted_datetime(),
                        "updateTime": self.get_formatted_datetime(),
                        "presalePrice": 11,
                        "activeType": 1,
                        "price": "11",
                        "selectListStr": ""
                    }
                }
            ],
            "purchaseUserName": INFO['main_purchase_user_name'],
            "orderPayInfoList": [
                {
                    "accountNo": INFO['main_account_no'],
                    "accountName": INFO['main_account_name'],
                    "payPrice": "1",
                    "uploadList": []
                }
            ],
            "purchaseOrdersArticlesDTO": {},
            "quickOperation": "0"
        }
        return self._make_request('post', 'Wev5hkW8C', data, 'main', nocheck)


class BGV1dswh7k(InitializeParams):
    """二手通小程序|首页|维修"""

    @doc(qS2uDNdC7LfquknU8HMF)
    def qS2uDNdC7LfquknU8HMF(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='7')
        res_2 = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i='2', j='1', k=1, l='17569')
        res_3 = self.pc.Gv7PVAqUJKoyfROzOacmx(i=1, data='a')
        data = {
            "sendTitle": "1",
            "receiveId": INFO['main_user_id'],
            "repairPrice": 20,
            "repairRemark": "维修详情",
            "salesChannelNo": "",
            "repairItemId": res_3['tableData'][0]['id'],
            "articlesAndAccessoryJoinDTOS": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "accessoryNo": res_2[0]['articlesNo']
                }
            ],
            "articlesNoList": [
                res[0]['articlesNo'],
            ]
        }
        return self._make_request('post', 'rCpZquLEe', data, 'main', nocheck)


class UGpw1VZJZZ(InitializeParams):
    """二手通小程序|首页|销售"""

    @doc(WyGu6Pcc1zlfEZUHYROZ)
    def WyGu6Pcc1zlfEZUHYROZ(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='13')
        time = self.get_current_timestamp_ms()
        jd = self.jd
        data = {
            "saleType": 1,
            "payWay": "1",
            "offExpressage": 0,
            "pickUpType": 1,
            "logisticsCompanyType": "1",
            "userAddressId": "",
            "clientId": INFO['main_sale_supplier_id'],
            "clientName": INFO['vice_sales_customer_name'],
            "pickUpTime": "",
            "status": 1,
            "logisticsOrder": jd,
            "logisticsNoPrice": 11,
            "purchaseOrdersArticlesDTOList": [
                {
                    "saleRecordId": None,
                    "id": res[0]['id'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 1,
                    "salePrice": 34,
                    "saleSettlePrice": 34,
                    "platformArticlesNo": self.serial,
                    "platformOrderNo": "",
                    "purchaseArticlesInfoDTO": {
                        "finenessId": None,
                        "id": time
                    }
                }
            ],
            "accountName": INFO['main_account_name'],
            "accountNo": INFO['main_account_no'],
            "userName": INFO['main_account'],
            "userId": INFO['main_user_id'],
            "orderPayInfoList": [
                {
                    "accountNo": INFO['main_account_no'],
                    "accountName": INFO['main_account_name'],
                    "payPrice": "1",
                    "uploadList": [],
                    "voucherImg": ""
                }
            ],
            "saleTime": self.get_formatted_datetime(),
            "giveAccessoryArticlesNoList": []
        }
        return self._make_request('post', 'BQoAuZBoB', data, 'main', nocheck)

    @doc(I1mqk82QVzJNQKaTV6mz)
    def I1mqk82QVzJNQKaTV6mz(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='13')
        time = self.get_current_timestamp_ms()
        jd = self.jd
        data = {
            "saleType": 1,
            "payWay": "1",
            "offExpressage": 0,
            "pickUpType": 1,
            "logisticsCompanyType": "1",
            "userAddressId": "",
            "clientId": INFO['main_sale_supplier_id'],
            "clientName": INFO['vice_account'],
            "pickUpTime": "",
            "status": 1,
            "logisticsOrder": jd,
            "logisticsNoPrice": 11,
            "purchaseOrdersArticlesDTOList": [
                {
                    "saleRecordId": None,
                    "id": res[0]['id'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 1,
                    "salePrice": 99,
                    "saleSettlePrice": 99,
                    "platformArticlesNo": "",
                    "platformOrderNo": "",
                    "purchaseArticlesInfoDTO": {
                        "finenessId": None,
                        "id": time
                    }
                }
            ],
            "accountName": INFO['main_account_name'],
            "accountNo": INFO['main_account_no'],
            "userName": INFO['main_account'],
            "userId": INFO['main_user_id'],
            "orderPayInfoList": [
                {
                    "accountNo": INFO['main_account_no'],
                    "accountName": INFO['main_account_name'],
                    "payPrice": 99,
                    "uploadList": [],
                    "voucherImg": ""
                }
            ],
            "saleTime": self.get_formatted_datetime(),
            "giveAccessoryArticlesNoList": []
        }
        return self._make_request('post', 'BQoAuZBoB', data, 'main', nocheck)

    @doc(cjzeWBYzVIvAQsaSE5Uv)
    def cjzeWBYzVIvAQsaSE5Uv(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='13')
        res_2 = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i='2')
        time = self.get_current_timestamp_ms()
        jd = self.jd
        data = {
            "saleType": 1,
            "payWay": "1",
            "offExpressage": 0,
            "pickUpType": 1,
            "logisticsCompanyType": "1",
            "userAddressId": "",
            "clientId": INFO['main_sale_supplier_id'],
            "clientName": INFO['vice_sales_customer_name'],
            "pickUpTime": "",
            "status": 1,
            "logisticsOrder": jd,
            "logisticsNoPrice": 11,
            "purchaseOrdersArticlesDTOList": [
                {
                    "saleRecordId": None,
                    "id": res[0]['id'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 1,
                    "salePrice": 63,
                    "saleSettlePrice": 63,
                    "platformArticlesNo": self.serial,
                    "platformOrderNo": "",
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1,
                        "id": time
                    }
                }
            ],
            "accountName": INFO['main_account_name'],
            "accountNo": INFO['main_account_no'],
            "userName": INFO['main_account'],
            "userId": INFO['main_user_id'],
            "orderPayInfoList": [
                {
                    "accountNo": INFO['main_account_no'],
                    "accountName": INFO['main_account_name'],
                    "payPrice": 63,
                    "uploadList": [],
                    "voucherImg": ""
                }
            ],
            "saleTime": self.get_formatted_datetime(),
            "giveAccessoryArticlesNoList": [
                res_2[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'BQoAuZBoB', data, 'main', nocheck)

    @doc(ZuRvUQFLB6nCYNOzrUSt)
    def ZuRvUQFLB6nCYNOzrUSt(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='13')
        time = self.get_current_timestamp_ms()
        jd = self.jd
        data = {
            "saleType": 1,
            "payWay": "1",
            "offExpressage": 0,
            "pickUpType": 1,
            "logisticsCompanyType": "1",
            "userAddressId": "",
            "clientId": INFO['main_sale_supplier_id'],
            "clientName": INFO['vice_sales_customer_name'],
            "pickUpTime": "",
            "status": "2",
            "logisticsOrder": jd,
            "logisticsNoPrice": 11,
            "purchaseOrdersArticlesDTOList": [
                {
                    "saleRecordId": None,
                    "id": res[0]['id'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 1,
                    "salePrice": 234,
                    "saleSettlePrice": 234,
                    "platformArticlesNo": self.serial,
                    "platformOrderNo": "",
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1,
                        "id": time
                    }
                }
            ],
            "accountName": INFO['main_account_name'],
            "accountNo": INFO['main_account_no'],
            "userName": INFO['main_account'],
            "userId": INFO['main_user_id'],
            "orderPayInfoList": [],
            "saleTime": self.get_formatted_datetime(),
            "giveAccessoryArticlesNoList": []
        }
        return self._make_request('post', 'BQoAuZBoB', data, 'main', nocheck)

    @doc(D7cyIB59qNYvDxKX9oXF)
    def D7cyIB59qNYvDxKX9oXF(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='13')
        time = self.get_current_timestamp_ms()
        data = {
            "saleType": 1,
            "payWay": "1",
            "offExpressage": 1,
            "pickUpType": 1,
            "logisticsCompanyType": "1",
            "userAddressId": INFO['main_user_address_id'],
            "clientId": INFO['main_sale_supplier_id'],
            "clientName": INFO['vice_sales_customer_name'],
            "pickUpTime": "",
            "status": "2",
            "logisticsNoPrice": 1,
            "purchaseOrdersArticlesDTOList": [
                {
                    "saleRecordId": None,
                    "id": res[0]['id'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 1,
                    "salePrice": 442,
                    "saleSettlePrice": 442,
                    "platformArticlesNo": "",
                    "platformOrderNo": "",
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 38,
                        "id": time
                    }
                }
            ],
            "accountName": INFO['main_account_name'],
            "accountNo": INFO['main_account_no'],
            "userName": INFO['main_account'],
            "userId": INFO['main_user_id'],
            "orderPayInfoList": [],
            "saleTime": self.get_formatted_datetime(),
            "giveAccessoryArticlesNoList": []
        }
        return self._make_request('post', 'BQoAuZBoB', data, 'main', nocheck)


if __name__ == '__main__':
    api = TraffickerHelpRequest()
    result = api.execute_one_click_help()
    print(result)
