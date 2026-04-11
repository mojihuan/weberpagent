# coding: utf-8
import json
from common.base_api import BaseApi
from common.base_params import InitializeParams
from common.import_desc import *
from config.user_info import INFO

color = BaseApi.load_json_file('request_help.json')['color']
parameterList = BaseApi.load_json_file('request_help.json')['parameterList']
templateVOS = BaseApi.load_json_file('request_help.json')['templateVOS']


class N1bdBTU6wm(InitializeParams):
    """帮卖管理|帮卖上架列表"""

    @doc(gHXYe9nXDQKo8k2pCpHF)
    @BaseApi.timing_decorator
    def gHXYe9nXDQKo8k2pCpHF(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='3')
        self.x2Ue8YzUHAdfE5e1ah2B()
        self.vsKRonFDNGzytQja2jna()
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "helpSellTenantId": INFO['main_help_sell_tenant_id'],
            "batchRemark": "备注",
            "settlementType": 1
        }
        return self._make_request('post', 'NE7Tz9kCF', data, 'main', nocheck)

    @doc(iCbN7kUssvEHLZtMSh1V)
    @BaseApi.timing_decorator
    def iCbN7kUssvEHLZtMSh1V(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='3')
        self.x2Ue8YzUHAdfE5e1ah2B()
        self.vsKRonFDNGzytQja2jna()
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "helpSellTenantId": INFO['main_help_sell_tenant_id'],
            "batchRemark": "备注",
            "settlementType": 2
        }
        return self._make_request('post', 'place_an_order', data, 'main', nocheck)

    @doc(iPBfiMFiHxZjY3ZEwdIp)
    @BaseApi.timing_decorator
    def iPBfiMFiHxZjY3ZEwdIp(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='3')
        self.x2Ue8YzUHAdfE5e1ah2B()
        self.vsKRonFDNGzytQja2jna()
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "helpSellTenantId": INFO['main_help_sell_tenant_id'],
            "batchRemark": "备注",
            "settlementType": 3
        }
        return self._make_request('post', 'place_an_order', data, 'main', nocheck)

    @doc(PatKHW4ZM1AOnRz4wYCa)
    @BaseApi.timing_decorator
    def PatKHW4ZM1AOnRz4wYCa(self, nocheck=False):
        res = self.pc.PurkQXBjQXG3tz8hUb1SF()
        data = {
            "batchId": res[0]['helpSellBatchId'],
            "orderIdList": [
                res[0]['orderNo']
            ],
            "batchNo": res[0]['batchNo'],
            "type": 1,
            "recipientName": INFO['vice_sales_customer_name'],
            "recipientPhone": INFO['receiving_phone'],
            "recipientProvinceId": INFO['province_id'],
            "recipientProvinceName": INFO['province_name'],
            "recipientCityId": INFO['city_id'],
            "recipientCityName": INFO['city_name'],
            "recipientCountyId": INFO['county_id'],
            "recipientCountyName": INFO['county_name'],
            "recipientAddress": INFO['detailed_address'],
            "senderName": INFO['customer_name'],
            "senderPhone": INFO['shipping_phone'],
            "senderProvinceId": INFO['province_id'],
            "senderProvinceName": INFO['province_name'],
            "senderCityId": INFO['city_id'],
            "senderCityName": INFO['city_name'],
            "senderCountyId": INFO['county_id'],
            "senderCountyName": INFO['county_name'],
            "senderAddress": INFO['detailed_address'],
            "expressCompanyId": 1,
            "payWay": 1,
            "expressCompanyName": "顺丰",
            "expectPostTimeStart": self.get_formatted_datetime(hours=1),
            "estimateFreight": 10,
            "walletAccountNo": INFO['main_wallet_account_no'],
            "expectPostTimeEnd": self.get_formatted_datetime(hours=2)
        }
        return self._make_request('post', 'bDNwCAp4n', data, 'main', nocheck)

    @doc(x2Ue8YzUHAdfE5e1ah2B)
    @BaseApi.timing_decorator
    def x2Ue8YzUHAdfE5e1ah2B(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='3')
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "helpSellTenantId": INFO['main_help_sell_tenant_id']
        }

        return self._make_request('post', 'QUZxLk9kS', data, 'main', nocheck)

    @doc(YehoAEPuerEeCRCU2qEI)
    @BaseApi.timing_decorator
    def YehoAEPuerEeCRCU2qEI(self, nocheck=False):
        res = self.pc.PurkQXBjQXG3tz8hUb1SF(data='a')
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "helpSellTenantId": INFO['main_help_sell_tenant_id']
        }
        return self._make_request('post', 'vDTNyb76a', data, 'main', nocheck)

    # 帮卖下单保存期望价格
    @BaseApi.timing_decorator
    def vsKRonFDNGzytQja2jna(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='3')
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "expectPrice": "100",
            "helpSellTenantId": INFO['main_help_sell_tenant_id']
        }
        return self._make_request('post', 'IkgcduhSe', data, 'main', nocheck)

    @doc(fBkRLU5PnvGYpBfZdMYx)
    @BaseApi.timing_decorator
    def fBkRLU5PnvGYpBfZdMYx(self, nocheck=False):
        res = self.pc.PurkQXBjQXG3tz8hUb1SF()
        data = {
            "orderNoList": [
                res[0]['orderNo']
            ]
        }
        return self._make_request('post', 'VjS268Bbk', data, 'main', nocheck)

    @doc(fNG49PWF3oUJGnsMAIuf)
    @BaseApi.timing_decorator
    def fNG49PWF3oUJGnsMAIuf(self, nocheck=False):
        res = self.pc.PurkQXBjQXG3tz8hUb1SF()
        data = {
            "orderNo": res[0]['orderNo']
        }
        return self._make_request('post', 't2W0RXX0y', data, 'main', nocheck)

    @doc(EjR5pz1y2L10GHnV2z4v)
    @BaseApi.timing_decorator
    def EjR5pz1y2L10GHnV2z4v(self, nocheck=False):
        res = self.pc.PurkQXBjQXG3tz8hUb1SF()
        data = {
            "orderNo": res[0]['orderNo'],
            "description": "备注"
        }
        return self._make_request('post', 'Upm9s0CAF', data, 'main', nocheck)

    @doc(CtZUckEy9Xr7Q9rhDgM9)
    @BaseApi.timing_decorator
    def CtZUckEy9Xr7Q9rhDgM9(self, nocheck=False):
        res = self.pc.PurkQXBjQXG3tz8hUb1SF(i='wsg')
        data = {
            "type": "2",
            "expressNo": self.sf,
            "expressCompanyName": "顺丰快递",
            "serderPhone": INFO['shipping_phone'],
            "batchId": res[0]['helpSellBatchId'],
            "orderIdList": [
                res[0]['orderNo']
            ],
            "batchNo": res[0]['batchNo'],
            "recipientName": INFO['main_account'],
            "recipientPhone": INFO['receiving_phone'],
            "recipientProvinceId": INFO['province_id'],
            "recipientProvinceName": INFO['province_name'],
            "recipientCityId": INFO['city_id'],
            "recipientCityName": INFO['city_name'],
            "recipientCountyId": INFO['county_id'],
            "recipientCountyName": INFO['county_name'],
            "recipientAddress": INFO['detailed_address']
        }
        return self._make_request('post', 'bDNwCAp4n', data, 'main', nocheck)

    @doc(lUGAPOtEUoXAYtTaa2Jb)
    @BaseApi.timing_decorator
    def lUGAPOtEUoXAYtTaa2Jb(self, nocheck=False):
        res = self.pc.PurkQXBjQXG3tz8hUb1SF(i='wsg')
        data = {
            "batchId": res[0]['helpSellBatchId'],
            "orderIdList": [
                res[0]['orderNo']
            ],
            "batchNo": res[0]['batchNo'],
            "type": "3",
            "recipientName": INFO['vice_sales_customer_name'],
            "recipientPhone": INFO['shipping_phone'],
            "recipientProvinceId": INFO['province_id'],
            "recipientProvinceName": INFO['province_name'],
            "recipientCityId": INFO['city_id'],
            "recipientCityName": INFO['city_name'],
            "recipientCountyId": INFO['county_id'],
            "recipientCountyName": INFO['county_name'],
            "recipientAddress": INFO['detailed_address']
        }
        return self._make_request('post', 'bDNwCAp4n', data, 'main', nocheck)

    @doc(qWL5r2tvJ34XBHF8SvNA)
    @BaseApi.timing_decorator
    def qWL5r2tvJ34XBHF8SvNA(self, nocheck=False):
        res = self.pc.PurkQXBjQXG3tz8hUb1SF()
        data = {
            "orderNoList": [
                res[0]['orderNo']
            ]
        }
        return self._make_request('post', 'fRgdJJtuV', data, 'main', nocheck)

    @doc(xzJ4vjMEgys2mrV0XE7B)
    @BaseApi.timing_decorator
    def xzJ4vjMEgys2mrV0XE7B(self, nocheck=False):
        res = self.pc.PurkQXBjQXG3tz8hUb1SF()
        data = {
            "orderIdList": [
                res[0]['orderNo']
            ]
        }
        return self._make_request('post', 'vsZZTwr4z', data, 'main', nocheck)

    @doc(KWGxLZFsVSdw6Fh5ZbAA)
    @BaseApi.timing_decorator
    def KWGxLZFsVSdw6Fh5ZbAA(self, nocheck=False):
        res = self.pc.PurkQXBjQXG3tz8hUb1SF()
        res_2 = self.pc.Jc9Odo2T6JqvbWDRSsDXy()
        data = {
            "warehouseId": INFO['main_item_warehouse_id'],
            "articlesList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "warehouseId": ""
                }
            ],
            "logisticsNo": res_2[0]['returnExpressNo'],
            "quickOperation": 0,
            "purchaseOrdersArticlesDTO": {
                "articlesNoList": [
                    res[0]['articlesNo']
                ],
                "createBy": "",
                "type": "",
                "userId": "",
                "remark": ""
            }
        }
        return self._make_request('post', 'DYbHAZqxU', data, 'main', nocheck)

    @doc(giHmrq7UpbJoAn7MEMOJ)
    @BaseApi.timing_decorator
    def giHmrq7UpbJoAn7MEMOJ(self, nocheck=False):
        res = self.pc.PurkQXBjQXG3tz8hUb1SF()
        data = {
            "orderNo": res[0]['orderNo']
        }
        return self._make_request('post', 't2W0RXX0y', data, 'main', nocheck)


class KtEAxo6C4B(InitializeParams):
    """帮卖管理|帮卖来货列表"""

    @doc(puhf4ZwCo9hIo0rzm7zd)
    @BaseApi.timing_decorator
    def puhf4ZwCo9hIo0rzm7zd(self, nocheck=False):
        res = self.pc.Jc9Odo2T6JqvbWDRSsDXy()
        data = {
            "type": "2",
            "expressNo": self.sf,
            "expressCompanyName": "顺丰快递",
            "serderPhone": self.phone,
            "batchId": res[0]['helpSellBatchId'],
            "orderIdList": [
                res[0]['orderNo']
            ],
            "batchNo": res[0]['batchNo'],
            "recipientName": INFO['vice_sales_customer_name'],
            "recipientPhone": self.phone,
            "recipientProvinceId": INFO['province_id'],
            "recipientProvinceName": INFO['province_name'],
            "recipientCityId": INFO['city_id'],
            "recipientCityName": INFO['city_name'],
            "recipientCountyId": INFO['county_id'],
            "recipientCountyName": INFO['county_name'],
            "recipientAddress": INFO['detailed_address']
        }
        return self._make_request('post', 'B2Y1BK8tu', data, 'vice', nocheck)

    @doc(UEgbcBjQGEn3BLntI6lb)
    @BaseApi.timing_decorator
    def UEgbcBjQGEn3BLntI6lb(self, nocheck=False):
        res = self.pc.Jc9Odo2T6JqvbWDRSsDXy()
        data = {
            "guaranteeSalePrice": 234,
            "orderNo": res[0]['orderNo'],
            "brandId": res[0]['brandId'],
            "brandName": res[0]['brandName'],
            "modelId": res[0]['modelId'],
            "modelName": res[0]['modelName'],
            "imei": res[0]['imei'],
            "parameters": [
                {
                    "parameterId": res[0]['brandId'],
                    "parameterValue": "brandId",
                    "parameterKey": "品牌",
                    "parameterName": res[0]['brandName'],
                    "parameterList": None
                },
                {
                    "parameterId": res[0]['modelId'],
                    "parameterValue": "modelId",
                    "parameterKey": "型号",
                    "parameterName": res[0]['modelName'],
                    "parameterList": None
                },
                {
                    "parameterId": res[0]['imei'],
                    "parameterValue": "imei",
                    "parameterKey": "IMEI",
                    "parameterName": res[0]['imei'],
                    "parameterList": None
                },
                {
                    "parameterId": 1712,
                    "parameterValue": "colorId",
                    "parameterKey": "颜色",
                    "parameterName": "黑色钛金属",
                    "parameterList": color
                },
                {
                    "parameterId": 41,
                    "parameterValue": "romId",
                    "parameterKey": "存储容量",
                    "parameterName": "256G",
                    "parameterList": [
                        {
                            "id": 36,
                            "title": "8G",
                            "sort": 1
                        },
                        {
                            "id": 37,
                            "title": "16G",
                            "sort": 2
                        },
                        {
                            "id": 38,
                            "title": "32G",
                            "sort": 3
                        },
                        {
                            "id": 39,
                            "title": "64G",
                            "sort": 4
                        },
                        {
                            "id": 40,
                            "title": "128G",
                            "sort": 5
                        },
                        {
                            "id": 41,
                            "title": "256G",
                            "sort": 6
                        },
                        {
                            "id": 99,
                            "title": "512G",
                            "sort": 7
                        },
                        {
                            "id": 105,
                            "title": "1TB",
                            "sort": 9
                        },
                        {
                            "id": 314,
                            "title": "2TB",
                            "sort": 10
                        },
                        {
                            "id": 340,
                            "title": "640G",
                            "sort": 8
                        }
                    ]
                },
                {
                    "parameterId": 72,
                    "parameterValue": "modelParametersId",
                    "parameterKey": "小型号",
                    "parameterName": "其他型号",
                    "parameterList": parameterList
                },
                {
                    "parameterId": 16,
                    "parameterValue": "buyChannelId",
                    "parameterKey": "购买渠道",
                    "parameterName": "国行",
                    "parameterList": [
                        {
                            "id": 16,
                            "title": "国行",
                            "sort": 1
                        },
                        {
                            "id": 42,
                            "title": "港版",
                            "sort": 3
                        },
                        {
                            "id": 43,
                            "title": "美版",
                            "sort": 3
                        },
                        {
                            "id": 44,
                            "title": "韩版",
                            "sort": 4
                        },
                        {
                            "id": 45,
                            "title": "日版",
                            "sort": 5
                        },
                        {
                            "id": 60,
                            "title": "国际版",
                            "sort": 6
                        },
                        {
                            "id": 61,
                            "title": "其他渠道",
                            "sort": 7
                        },
                        {
                            "id": 62,
                            "title": "英版",
                            "sort": 8
                        },
                        {
                            "id": 63,
                            "title": "台版",
                            "sort": 9
                        },
                        {
                            "id": 64,
                            "title": "展示机",
                            "sort": 6
                        },
                        {
                            "id": 65,
                            "title": "国行官换机",
                            "sort": 2
                        },
                        {
                            "id": 66,
                            "title": "工程机",
                            "sort": 12
                        },
                        {
                            "id": 100,
                            "title": "烧卡机",
                            "sort": 13
                        },
                        {
                            "id": 101,
                            "title": "水货有锁",
                            "sort": 5
                        },
                        {
                            "id": 102,
                            "title": "水货无锁",
                            "sort": 4
                        },
                        {
                            "id": 376,
                            "title": "非大陆国行",
                            "sort": 16
                        },
                        {
                            "id": 737,
                            "title": "大陆国行",
                            "sort": 1
                        },
                        {
                            "id": 738,
                            "title": "国行展示机",
                            "sort": 3
                        },
                        {
                            "id": 4090,
                            "title": "国行资源机",
                            "sort": 17
                        },
                        {
                            "id": 4091,
                            "title": "国行权益机",
                            "sort": 18
                        },
                        {
                            "id": 4092,
                            "title": "国行官翻机",
                            "sort": 19
                        },
                        {
                            "id": 4121,
                            "title": "其他版本",
                            "sort": 20
                        }
                    ]
                },
                {
                    "parameterId": None,
                    "parameterValue": "networkStandardId",
                    "parameterKey": "网络制式",
                    "parameterName": None,
                    "parameterList": [
                        {
                            "id": 30,
                            "title": "全网通",
                            "sort": 1
                        },
                        {
                            "id": 31,
                            "title": "双网通",
                            "sort": 2
                        },
                        {
                            "id": 32,
                            "title": "移动版",
                            "sort": 3
                        },
                        {
                            "id": 55,
                            "title": "联通版",
                            "sort": 4
                        },
                        {
                            "id": 56,
                            "title": "电信版",
                            "sort": 5
                        },
                        {
                            "id": 67,
                            "title": "其他",
                            "sort": 6
                        },
                        {
                            "id": 68,
                            "title": "WIFI",
                            "sort": 7
                        },
                        {
                            "id": 69,
                            "title": "WIFI+4G",
                            "sort": 8
                        },
                        {
                            "id": 70,
                            "title": "WIFI+3G",
                            "sort": 9
                        },
                        {
                            "id": 137,
                            "title": "移动版全网通",
                            "sort": 6
                        },
                        {
                            "id": 315,
                            "title": "WIFI+5G",
                            "sort": 10
                        }
                    ]
                },
                {
                    "parameterId": None,
                    "parameterValue": "mobileId",
                    "parameterKey": "移动",
                    "parameterName": None,
                    "parameterList": [
                        {
                            "id": 852,
                            "title": "5G",
                            "sort": 1013
                        },
                        {
                            "id": 853,
                            "title": "4G",
                            "sort": 1014
                        }
                    ]
                },
                {
                    "parameterId": None,
                    "parameterValue": "unicom",
                    "parameterKey": "联通",
                    "parameterName": None,
                    "parameterList": [
                        {
                            "id": 852,
                            "title": "5G",
                            "sort": 1013
                        },
                        {
                            "id": 853,
                            "title": "4G",
                            "sort": 1014
                        }
                    ]
                },
                {
                    "parameterId": None,
                    "parameterValue": "telecom",
                    "parameterKey": "电信",
                    "parameterName": None,
                    "parameterList": [
                        {
                            "id": 854,
                            "title": "4G",
                            "sort": 1014
                        },
                        {
                            "id": 855,
                            "title": "5G",
                            "sort": 1013
                        }
                    ]
                },
                {
                    "parameterId": None,
                    "parameterValue": "machineTypeId",
                    "parameterKey": "机器类型",
                    "parameterName": None,
                    "parameterList": [
                        {
                            "id": 862,
                            "title": "二手优品",
                            "sort": 1019
                        },
                        {
                            "id": 863,
                            "title": "官翻机",
                            "sort": 1020
                        },
                        {
                            "id": 23029,
                            "title": "资源机",
                            "sort": 1046
                        },
                        {
                            "id": 23120,
                            "title": "官换机",
                            "sort": 10000
                        },
                        {
                            "id": 23121,
                            "title": "零售机",
                            "sort": 10001
                        },
                        {
                            "id": 23122,
                            "title": "展示机",
                            "sort": 10002
                        }
                    ]
                },
                {
                    "parameterId": 23012,
                    "parameterValue": "finenessId",
                    "parameterKey": "成色",
                    "parameterName": "靓机",
                    "parameterList": [
                        {
                            "id": 23012,
                            "title": "靓机",
                            "sort": 1029
                        },
                        {
                            "id": 23013,
                            "title": "小花",
                            "sort": 1030
                        },
                        {
                            "id": 23014,
                            "title": "大花",
                            "sort": 1031
                        },
                        {
                            "id": 23015,
                            "title": "外爆",
                            "sort": 1032
                        },
                        {
                            "id": 23016,
                            "title": "内爆",
                            "sort": 1033
                        }
                    ]
                },
                {
                    "parameterId": None,
                    "parameterValue": "warrantyId",
                    "parameterKey": "保修情况",
                    "parameterName": None,
                    "parameterList": [
                        {
                            "id": 23005,
                            "title": "保修时长≥330天",
                            "sort": 1022
                        },
                        {
                            "id": 23006,
                            "title": "180天≤保修时长＜330天",
                            "sort": 1023
                        },
                        {
                            "id": 23007,
                            "title": "30天≤保修时长＜180天",
                            "sort": 1024
                        },
                        {
                            "id": 23008,
                            "title": "保修时长＜30天",
                            "sort": 1025
                        }
                    ]
                },
                {
                    "parameterId": None,
                    "parameterValue": "batteryHealthId",
                    "parameterKey": "电池健康度",
                    "parameterName": None,
                    "parameterList": [
                        {
                            "id": 23024,
                            "title": "电池健康度100%",
                            "sort": 1041
                        },
                        {
                            "id": 23025,
                            "title": "90%＜电池健康度≤99%",
                            "sort": 1042
                        },
                        {
                            "id": 23026,
                            "title": "84%＜电池健康度≤90%",
                            "sort": 1043
                        },
                        {
                            "id": 23027,
                            "title": "81%＜电池健康度≤84%",
                            "sort": 1044
                        },
                        {
                            "id": 23028,
                            "title": "电池健康度≤81%",
                            "sort": 1045
                        }
                    ]
                }
            ],
            "templateVOS": templateVOS,
            "orderId": res[0]['orderNo']
        }
        return self._make_request('post', 'IB3gn1xZs', data, 'vice', nocheck)

    @doc(rE4s2MubKTarhv1LX8Ps)
    @BaseApi.timing_decorator
    def rE4s2MubKTarhv1LX8Ps(self, nocheck=False):
        res = self.pc.Jc9Odo2T6JqvbWDRSsDXy()
        data = {
            "warehouseId": INFO['vice_warehouse_id'],
            "articlesList": [
                {
                    "articlesNo": res[0]['helpSellArticlesNo'],
                    "warehouseId": ""
                }
            ],
            "logisticsNo": res[0]['deliverExpressNo'],
            "quickOperation": 0,
            "purchaseOrdersArticlesDTO": {
                "articlesNoList": [],
                "createBy": "",
                "type": "",
                "userId": "",
                "remark": ""
            }
        }
        return self._make_request('post', 'DYbHAZqxU', data, 'vice', nocheck)

    @doc(s8ZT0XEbPTqi9X6O3C4D)
    @BaseApi.timing_decorator
    def s8ZT0XEbPTqi9X6O3C4D(self, nocheck=False):
        res = self.pc.Jc9Odo2T6JqvbWDRSsDXy()
        data = {
            "warehouseId": INFO['vice_warehouse_id'],
            "articlesList": [
                {
                    "articlesNo": res[0]['helpSellArticlesNo'],
                    "warehouseId": ""
                }
            ],
            "logisticsNo": res[0]['deliverExpressNo'],
            "quickOperation": 0,
            "purchaseOrdersArticlesDTO": {
                "articlesNoList": [],
                "createBy": "",
                "type": "",
                "userId": "",
                "remark": ""
            }
        }
        return self._make_request('post', 'DYbHAZqxU', data, 'vice', nocheck)

    @doc(bpeTVApfqf4ysIlGh0d1)
    @BaseApi.timing_decorator
    def bpeTVApfqf4ysIlGh0d1(self, nocheck=False):
        res = self.pc.Jc9Odo2T6JqvbWDRSsDXy()
        data = {
            "orderIdList": [
                res[0]['orderNo']
            ]
        }
        return self._make_request('post', 'gKmp1GEat', data, 'vice', nocheck)

    @doc(LB9ycxycPTRF4K0JdDw7)
    @BaseApi.timing_decorator
    def LB9ycxycPTRF4K0JdDw7(self, nocheck=False):
        res = self.pc.Jc9Odo2T6JqvbWDRSsDXy()
        data = {
            "guaranteeSalePrice": self.number,
            "orderNo": res[0]['orderIdList'],
            "brandId": res[0]['brandId'],
            "brandName": res[0]['brandName'],
            "modelId": res[0]['modelId'],
            "modelName": res[0]['modelName'],
            "imei": res[0]['imei'],
            "parameters": [
                {
                    "parameterId": res[0]['brandId'],
                    "parameterValue": "brandId",
                    "parameterKey": "品牌",
                    "parameterName": res[0]['brandName'],
                    "parameterList": None
                },
                {
                    "parameterId": res[0]['modelId'],
                    "parameterValue": "modelId",
                    "parameterKey": "型号",
                    "parameterName": res[0]['modelName'],
                    "parameterList": None
                },
                {
                    "parameterId": res[0]['imei'],
                    "parameterValue": "imei",
                    "parameterKey": "IMEI",
                    "parameterName": res[0]['imei'],
                    "parameterList": None
                },
                {
                    "parameterId": 1712,
                    "parameterValue": "colorId",
                    "parameterKey": "颜色",
                    "parameterName": "黑色钛金属",
                    "parameterList": color
                },
                {
                    "parameterId": 41,
                    "parameterValue": "romId",
                    "parameterKey": "存储容量",
                    "parameterName": "256G",
                    "parameterList": [
                        {
                            "id": 36,
                            "title": "8G",
                            "sort": 1
                        },
                        {
                            "id": 37,
                            "title": "16G",
                            "sort": 2
                        },
                        {
                            "id": 38,
                            "title": "32G",
                            "sort": 3
                        },
                        {
                            "id": 39,
                            "title": "64G",
                            "sort": 4
                        },
                        {
                            "id": 40,
                            "title": "128G",
                            "sort": 5
                        },
                        {
                            "id": 41,
                            "title": "256G",
                            "sort": 6
                        },
                        {
                            "id": 99,
                            "title": "512G",
                            "sort": 7
                        },
                        {
                            "id": 105,
                            "title": "1TB",
                            "sort": 9
                        },
                        {
                            "id": 314,
                            "title": "2TB",
                            "sort": 10
                        },
                        {
                            "id": 340,
                            "title": "640G",
                            "sort": 8
                        }
                    ]
                },
                {
                    "parameterId": 72,
                    "parameterValue": "modelParametersId",
                    "parameterKey": "小型号",
                    "parameterName": "其他型号",
                    "parameterList": parameterList
                },
                {
                    "parameterId": 16,
                    "parameterValue": "buyChannelId",
                    "parameterKey": "购买渠道",
                    "parameterName": "国行",
                    "parameterList": [
                        {
                            "id": 16,
                            "title": "国行",
                            "sort": 1
                        },
                        {
                            "id": 42,
                            "title": "港版",
                            "sort": 3
                        },
                        {
                            "id": 43,
                            "title": "美版",
                            "sort": 3
                        },
                        {
                            "id": 44,
                            "title": "韩版",
                            "sort": 4
                        },
                        {
                            "id": 45,
                            "title": "日版",
                            "sort": 5
                        },
                        {
                            "id": 60,
                            "title": "国际版",
                            "sort": 6
                        },
                        {
                            "id": 61,
                            "title": "其他渠道",
                            "sort": 7
                        },
                        {
                            "id": 62,
                            "title": "英版",
                            "sort": 8
                        },
                        {
                            "id": 63,
                            "title": "台版",
                            "sort": 9
                        },
                        {
                            "id": 64,
                            "title": "展示机",
                            "sort": 6
                        },
                        {
                            "id": 65,
                            "title": "国行官换机",
                            "sort": 2
                        },
                        {
                            "id": 66,
                            "title": "工程机",
                            "sort": 12
                        },
                        {
                            "id": 100,
                            "title": "烧卡机",
                            "sort": 13
                        },
                        {
                            "id": 101,
                            "title": "水货有锁",
                            "sort": 5
                        },
                        {
                            "id": 102,
                            "title": "水货无锁",
                            "sort": 4
                        },
                        {
                            "id": 376,
                            "title": "非大陆国行",
                            "sort": 16
                        },
                        {
                            "id": 737,
                            "title": "大陆国行",
                            "sort": 1
                        },
                        {
                            "id": 738,
                            "title": "国行展示机",
                            "sort": 3
                        },
                        {
                            "id": 4090,
                            "title": "国行资源机",
                            "sort": 17
                        },
                        {
                            "id": 4091,
                            "title": "国行权益机",
                            "sort": 18
                        },
                        {
                            "id": 4092,
                            "title": "国行官翻机",
                            "sort": 19
                        },
                        {
                            "id": 4121,
                            "title": "其他版本",
                            "sort": 20
                        }
                    ]
                },
                {
                    "parameterId": 31,
                    "parameterValue": "networkStandardId",
                    "parameterKey": "网络制式",
                    "parameterName": "双网通",
                    "parameterList": [
                        {
                            "id": 30,
                            "title": "全网通",
                            "sort": 1
                        },
                        {
                            "id": 31,
                            "title": "双网通",
                            "sort": 2
                        },
                        {
                            "id": 32,
                            "title": "移动版",
                            "sort": 3
                        },
                        {
                            "id": 55,
                            "title": "联通版",
                            "sort": 4
                        },
                        {
                            "id": 56,
                            "title": "电信版",
                            "sort": 5
                        },
                        {
                            "id": 67,
                            "title": "其他",
                            "sort": 6
                        },
                        {
                            "id": 68,
                            "title": "WIFI",
                            "sort": 7
                        },
                        {
                            "id": 69,
                            "title": "WIFI+4G",
                            "sort": 8
                        },
                        {
                            "id": 70,
                            "title": "WIFI+3G",
                            "sort": 9
                        },
                        {
                            "id": 137,
                            "title": "移动版全网通",
                            "sort": 6
                        },
                        {
                            "id": 315,
                            "title": "WIFI+5G",
                            "sort": 10
                        }
                    ]
                },
                {
                    "parameterId": 852,
                    "parameterValue": "mobileId",
                    "parameterKey": "移动",
                    "parameterName": "5G",
                    "parameterList": [
                        {
                            "id": 852,
                            "title": "5G",
                            "sort": 1013
                        },
                        {
                            "id": 853,
                            "title": "4G",
                            "sort": 1014
                        }
                    ]
                },
                {
                    "parameterId": 852,
                    "parameterValue": "unicom",
                    "parameterKey": "联通",
                    "parameterName": "5G",
                    "parameterList": [
                        {
                            "id": 852,
                            "title": "5G",
                            "sort": 1013
                        },
                        {
                            "id": 853,
                            "title": "4G",
                            "sort": 1014
                        }
                    ]
                },
                {
                    "parameterId": 855,
                    "parameterValue": "telecom",
                    "parameterKey": "电信",
                    "parameterName": "5G",
                    "parameterList": [
                        {
                            "id": 854,
                            "title": "4G",
                            "sort": 1014
                        },
                        {
                            "id": 855,
                            "title": "5G",
                            "sort": 1013
                        }
                    ]
                },
                {
                    "parameterId": 862,
                    "parameterValue": "machineTypeId",
                    "parameterKey": "机器类型",
                    "parameterName": "二手优品",
                    "parameterList": [
                        {
                            "id": 862,
                            "title": "二手优品",
                            "sort": 1019
                        },
                        {
                            "id": 863,
                            "title": "官翻机",
                            "sort": 1020
                        },
                        {
                            "id": 23029,
                            "title": "资源机",
                            "sort": 1046
                        }
                    ]
                },
                {
                    "parameterId": 23014,
                    "parameterValue": "finenessId",
                    "parameterKey": "成色",
                    "parameterName": "大花",
                    "parameterList": [
                        {
                            "id": 23012,
                            "title": "靓机",
                            "sort": 1029
                        },
                        {
                            "id": 23013,
                            "title": "小花",
                            "sort": 1030
                        },
                        {
                            "id": 23014,
                            "title": "大花",
                            "sort": 1031
                        },
                        {
                            "id": 23015,
                            "title": "外爆",
                            "sort": 1032
                        },
                        {
                            "id": 23016,
                            "title": "内爆",
                            "sort": 1033
                        }
                    ]
                },
                {
                    "parameterId": None,
                    "parameterValue": "warrantyId",
                    "parameterKey": "保修情况",
                    "parameterName": None,
                    "parameterList": [
                        {
                            "id": 23005,
                            "title": "保修时长≥330天",
                            "sort": 1022
                        },
                        {
                            "id": 23006,
                            "title": "180天≤保修时长＜330天",
                            "sort": 1023
                        },
                        {
                            "id": 23007,
                            "title": "30天≤保修时长＜180天",
                            "sort": 1024
                        },
                        {
                            "id": 23008,
                            "title": "保修时长＜30天",
                            "sort": 1025
                        }
                    ]
                },
                {
                    "parameterId": None,
                    "parameterValue": "batteryHealthId",
                    "parameterKey": "电池健康度",
                    "parameterName": None,
                    "parameterList": [
                        {
                            "id": 23024,
                            "title": "电池健康度100%",
                            "sort": 1041
                        },
                        {
                            "id": 23025,
                            "title": "90%＜电池健康度≤99%",
                            "sort": 1042
                        },
                        {
                            "id": 23026,
                            "title": "84%＜电池健康度≤90%",
                            "sort": 1043
                        },
                        {
                            "id": 23027,
                            "title": "81%＜电池健康度≤84%",
                            "sort": 1044
                        },
                        {
                            "id": 23028,
                            "title": "电池健康度≤81%",
                            "sort": 1045
                        }
                    ]
                }
            ],
            "templateVOS": templateVOS,
            "orderId": res[0]['orderNo']
        }
        return self._make_request('post', 'IB3gn1xZs', data, 'vice', nocheck)

    @doc(zHbBDAztWlR3wrimNxlj)
    @BaseApi.timing_decorator
    def zHbBDAztWlR3wrimNxlj(self, nocheck=False):
        res = self.pc.Jc9Odo2T6JqvbWDRSsDXy()
        data = {
            "orderNo": res[0]['orderNo'],
            "rejectReason": "屏幕内爆"
        }
        return self._make_request('post', 'F39h78grn', data, 'vice', nocheck)

    @BaseApi.timing_decorator
    def item_number(self, nocheck=False):
        res = self.pc.Jc9Odo2T6JqvbWDRSsDXy()
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'QBZVuqz0S', data, 'vice', nocheck)

    @doc(OKe7y8uCYv26BcVNtvU6)
    @BaseApi.timing_decorator
    def OKe7y8uCYv26BcVNtvU6(self, nocheck=False):
        self.item_number()
        time = self.get_current_timestamp_ms()
        res = self.pc.Jc9Odo2T6JqvbWDRSsDXy()
        res_2 = self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2, j=13, data='a')
        data = {
            "saleTime": self.get_formatted_datetime(),
            "saleType": "1",
            "clientId": INFO['vice_help_sale_supplier_id'],
            "clientName": INFO['vice_help_sale_supplier_name'],
            "accountNo": INFO['vice_sales_customer_name'],
            "accountName": INFO['main_account_name'],
            "userId": INFO['vice_user_id'],
            "deliveryId": INFO['vice_user_id'],
            "deliveryTime": self.get_formatted_datetime(),
            "status": 1,
            "logisticsOrder": self.jd,
            "logisticsNoPrice": 10,
            "isEexpress": "0",
            "offExpressage": "0",
            "orderPayInfoList": [
                {
                    "accountNo": INFO['vice_account_no'],
                    "voucherImg": "",
                    "payPrice": 10,
                    "accountName": INFO['main_account_name']
                }
            ],
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res_2[0]['id'],
                    "imei": res[0]['imei'],
                    "articlesNo": res[0]['helpSellArticlesNo'],
                    "articlesState": 13,
                    "salePrice": 10,
                    "platformArticlesNo": self.serial,
                    "platformOrderNo": None,
                    "remark": None,
                    "finenessId": 1,
                    "articlesInfoId": time,
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1,
                        "id": time
                    },
                    "saleSettlePrice": 1
                }
            ]
        }
        return self._make_request('post', 'JKSmt0DQk', data, 'vice', nocheck)

    @doc(yhsanR53oCT3E0y79Pkt)
    @BaseApi.timing_decorator
    def yhsanR53oCT3E0y79Pkt(self, nocheck=False):
        res = self.pc.Jc9Odo2T6JqvbWDRSsDXy()
        data = {
            "finalSellPrice": res[0]['finalSellPrice'],
            "orderNo": res[0]['orderNo']
        }
        return self._make_request('post', 'lkGutWbef', data, 'vice', nocheck)

    @doc(vCZ8TzDFnPROV6Oo072B)
    @BaseApi.timing_decorator
    def vCZ8TzDFnPROV6Oo072B(self, nocheck=False):
        res = self.pc.Jc9Odo2T6JqvbWDRSsDXy()
        data = {
            "batchId": res[0]['helpSellBatchId'],
            "orderIdList": [
                res[0]['orderNo']
            ],
            "batchNo": res[0]['batchNo'],
            "type": 1,
            "recipientName": INFO['main_account'],
            "recipientPhone": INFO['receiving_phone'],
            "recipientProvinceId": INFO['province_id'],
            "recipientProvinceName": INFO['province_name'],
            "recipientCityId": INFO['city_id'],
            "recipientCityName": INFO['city_name'],
            "recipientCountyId": INFO['county_id'],
            "recipientCountyName": INFO['county_name'],
            "recipientAddress": INFO['detailed_address'],
            "senderName": INFO['address_creator'],
            "senderPhone": INFO['shipping_phone'],
            "senderProvinceId": INFO['province_id'],
            "senderProvinceName": INFO['province_name'],
            "senderCityId": INFO['city_id'],
            "senderCityName": INFO['city_name'],
            "senderCountyId": INFO['county_id'],
            "senderCountyName": INFO['county_name'],
            "senderAddress": INFO['detailed_address'],
            "expressCompanyId": 1,
            "payWay": 1,
            "expressCompanyName": "顺丰",
            "expectPostTimeStart": self.get_formatted_datetime(),
            "estimateFreight": 10,
            "walletAccountNo": INFO['vice_wallet_account_no']
        }
        return self._make_request('post', 'B2Y1BK8tu', data, 'vice', nocheck)

    @doc(v7U6luxQobBYtqeXdMG0)
    @BaseApi.timing_decorator
    def v7U6luxQobBYtqeXdMG0(self, nocheck=False):
        res = self.pc.Jc9Odo2T6JqvbWDRSsDXy()
        data = {
            "batchId": res[0]['helpSellBatchId'],
            "orderIdList": [
                res[0]['orderNo']
            ],
            "batchNo": res[0]['batchNo'],
            "type": 1,
            "recipientName": INFO['main_account'],
            "recipientPhone": INFO['receiving_phone'],
            "recipientProvinceId": INFO['province_id'],
            "recipientProvinceName": INFO['province_name'],
            "recipientCityId": INFO['city_id'],
            "recipientCityName": INFO['city_name'],
            "recipientCountyId": INFO['county_id'],
            "recipientCountyName": INFO['county_name'],
            "recipientAddress": INFO['detailed_address'],
            "senderName": INFO['address_creator'],
            "senderPhone": INFO['shipping_phone'],
            "senderProvinceId": INFO['province_id'],
            "senderProvinceName": INFO['province_name'],
            "senderCityId": INFO['city_id'],
            "senderCityName": INFO['city_name'],
            "senderCountyId": INFO['county_id'],
            "senderCountyName": INFO['county_name'],
            "senderAddress": INFO['detailed_address'],
            "expressCompanyId": 1,
            "payWay": 1,
            "expressCompanyName": "顺丰",
            "expectPostTimeStart": self.get_formatted_datetime(),
            "estimateFreight": 10,
            "walletAccountNo": INFO['vice_wallet_account_no']
        }
        return self._make_request('post', 'B2Y1BK8tu', data, 'vice', nocheck)

    @doc(aR4vvS8nfanSGlBbfKzT)
    @BaseApi.timing_decorator
    def aR4vvS8nfanSGlBbfKzT(self, nocheck=False):
        res = self.pc.Jc9Odo2T6JqvbWDRSsDXy()
        data = {
            "batchId": res[0]['helpSellBatchId'],
            "orderIdList": [
                res[0]['orderNo']
            ],
            "batchNo": res[0]['batchNo'],
            "type": "3",
            "recipientName": INFO['vice_sales_customer_name'],
            "recipientPhone": self.phone,
            "recipientProvinceId": INFO['province_id'],
            "recipientProvinceName": INFO['province_name'],
            "recipientCityId": INFO['city_id'],
            "recipientCityName": INFO['city_name'],
            "recipientCountyId": INFO['county_id'],
            "recipientCountyName": INFO['county_name'],
            "recipientAddress": INFO['detailed_address']
        }
        return self._make_request('post', 'B2Y1BK8tu', data, 'vice', nocheck)


class Z2DMQfvumu(InitializeParams):
    """帮卖管理|帮卖业务配置"""

    @doc(lnEVAUkilhXnv8b0GZtm)
    @BaseApi.timing_decorator
    def lnEVAUkilhXnv8b0GZtm(self, nocheck=False):
        res = self.pc.Ea7Wjr4ctTv69frbEUPZJ()
        data = {
            "id": 91,
            "createTime": res[0]['createTime'],
            "updateTime": res[0]['updateTime'],
            "pageSize": 10,
            "pageNum": 1,
            "orderByColumn": "create_time",
            "isAsc": "desc",
            "merchantCode": INFO['main_help_sell_tenant_id'],
            "merchantName": INFO['main_account'],
            "merchantTypeName": res[0]['merchantTypeName'],
            "orderingMerchantCode": res[0]['orderingMerchantCode'],
            "orderingMerchantName": INFO['main_account'],
            "businessEffectivenessSwitch": "true",
            "helpSellSwitch": "true",
            "buyOutGuaranteeSwitch": "true",
            "guaranteeSharingSwitch": "true",
            "helpSellConfigStr": "10%,封顶111111元",
            "helpSellConfig": {
                "type": "1",
                "configList": [
                    {
                        "percentage": 10,
                        "beginPrice": 0,
                        "cappingPrice": 111111
                    }
                ]
            },
            "guaranteeSharingConfigStr": "20%,封顶222222元",
            "guaranteeSharingConfig": {
                "type": "1",
                "configList": [
                    {
                        "percentage": 20,
                        "beginPrice": 0,
                        "cappingPrice": 222222
                    }
                ]
            },
            "sellTimeoutConfiguration": 10,
            "returnTimeoutConfiguration": 10,
            "automaticSettlementDays": 10,
            "transactionVolume": 4
        }
        return self._make_request('post', 'SGU6BnplE', data, 'vice', nocheck)


if __name__ == '__main__':
    api = ()
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
