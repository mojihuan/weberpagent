# coding: utf-8
from common.base_api import BaseApi
from common.base_params import InitializeParams
from common.file_cache_manager import ParamCache
from config.user_info import INFO
from common.import_desc import *


class ZTIxIMcZz7(InitializeParams):
    """保卖小程序|首页"""

    @doc(BipQkv2GeGlQ96IF4MWs)
    def BipQkv2GeGlQ96IF4MWs(self, nocheck=False):
        data = {
            "childBusinessType": "2",
            "deliverNum": 1,
            "inspectionCenterId": INFO['check_the_center_id'],
            "inspectionCenterCode": INFO['merchant_id'],
            "expectationTotalPrice": "5555"
        }
        return self._make_request('post', 'BvpLVs5Te', data, 'main', nocheck)

    @doc(large_quantity_fast_submit_new_order)
    def large_quantity_fast_submit_new_order(self, nocheck=False):
        self.pc.B63gyanXogW9NpUu1Gr1K()
        data = {
            "childBusinessType": "2",
            "deliverNum": 5,
            "inspectionCenterId": INFO['check_the_center_id'],
            "inspectionCenterCode": INFO['merchant_id'],
            "expectationTotalPrice": "4567"
        }
        return self._make_request('post', 'BvpLVs5Te', data, 'main', nocheck)

    @doc(Ggf9HFpxeJakOskwG6Fo)
    def Ggf9HFpxeJakOskwG6Fo(self, nocheck=False):
        self.pc.B63gyanXogW9NpUu1Gr1K()
        data = {
            "childBusinessType": "2",
            "deliverNum": 1000,
            "inspectionCenterId": INFO['check_the_center_id'],
            "inspectionCenterCode": INFO['merchant_id'],
            "expectationTotalPrice": "2734"
        }
        return self._make_request('post', 'BvpLVs5Te', data, 'main', nocheck)

    # 精确发货估价
    @BaseApi.timing_decorator
    def precise_shipment_estimate(self, nocheck=False):
        data = {
            "brandId": 1,
            "modelId": "17569",
            "skuIdList": [
                "1743",
                "16",
                "1712",
                "41"
            ],
            "optionIdList": [
                1041,
                963,
                998,
                828,
                837,
                971,
                969,
                845,
                979,
                967,
                834
            ],
            "tenantId": 888888
        }
        return self._make_request('post', 'wwzSduh7x', data, 'main', nocheck)

    @doc(Cb5TwEFeOGRjQqpsPYhX)
    @BaseApi.timing_decorator
    def Cb5TwEFeOGRjQqpsPYhX(self, nocheck=False):
        # res = self.precise_shipment_estimate()
        data = {
            "childBusinessType": 1,
            "deliverNum": 1,
            # "inspectionCenterId": INFO['check_the_center_id'],
            # "inspectionCenterCode": INFO['merchant_id'],
            # "detailId": res['data']['detailId'],
            # "finenessId": res['data']['finenessId'],
            "inspectionCenterId": 13,
            "inspectionCenterCode": 560981,
            "detailId": 4678206,
            "finenessId": 130,
            "imei": "",
            "report": {
                "report": [
                    {
                        "questionOptionList": [
                            {
                                "questionId": 368,
                                "questionName": "折叠屏保护膜情况",
                                "optionList": [
                                    {
                                        "optionId": 969,
                                        "optionName": "有保护膜"
                                    }
                                ]
                            },
                            {
                                "questionId": 304,
                                "questionName": "机身外观",
                                "optionList": [
                                    {
                                        "optionId": 834,
                                        "optionName": "正常"
                                    }
                                ]
                            },
                            {
                                "questionId": 369,
                                "questionName": "副屏-液晶显示",
                                "optionList": [
                                    {
                                        "optionId": 979,
                                        "optionName": "副屏显示完美"
                                    }
                                ]
                            },
                            {
                                "questionId": 305,
                                "questionName": "屏幕外观",
                                "optionList": [
                                    {
                                        "optionId": 837,
                                        "optionName": "屏外观完美"
                                    }
                                ]
                            },
                            {
                                "questionId": 306,
                                "questionName": "液晶显示",
                                "optionList": [
                                    {
                                        "optionId": 845,
                                        "optionName": "显示完美"
                                    }
                                ]
                            },
                            {
                                "questionId": 374,
                                "questionName": "保修情况",
                                "optionList": [
                                    {
                                        "optionId": 998,
                                        "optionName": "保修≥331天"
                                    }
                                ]
                            },
                            {
                                "questionId": 300,
                                "questionName": "开机情况",
                                "optionList": [
                                    {
                                        "optionId": 1041,
                                        "optionName": "全新未拆封"
                                    }
                                ]
                            },
                            {
                                "questionId": 364,
                                "questionName": "iCloud账户锁",
                                "optionList": [
                                    {
                                        "optionId": 963,
                                        "optionName": "已解除"
                                    }
                                ]
                            },
                            {
                                "questionId": 366,
                                "questionName": "转轴状况",
                                "optionList": [
                                    {
                                        "optionId": 967,
                                        "optionName": "正常"
                                    }
                                ]
                            },
                            {
                                "questionId": 367,
                                "questionName": "副屏-屏幕外观",
                                "optionList": [
                                    {
                                        "optionId": 971,
                                        "optionName": "副屏外观完美"
                                    }
                                ]
                            },
                            {
                                "questionId": 303,
                                "questionName": "边框背板",
                                "optionList": [
                                    {
                                        "optionId": 828,
                                        "optionName": "外壳完美"
                                    }
                                ]
                            }
                        ],
                        "questionTypeName": "成色情况"
                    },
                    {
                        "questionOptionList": [

                        ],
                        "questionTypeName": "功能情况"
                    }
                ]
            },
            # "todayReferencePrice": res['data']['price'],
            "todayReferencePrice": 6240,
            "skuInfo": "A3297 国行 黑色钛金属 256G",
            "optionIdList": [
                1041,
                963,
                998,
                828,
                837,
                971,
                969,
                845,
                979,
                967,
                834
            ],
            "expectationTotalPrice": 6240
            # "expectationTotalPrice": res['data']['price']
        }
        return self._make_request('post', 'BvpLVs5Te', data, 'main', nocheck)

    @doc(Sx6ZHoGa30GK1xH2QbdF)
    @BaseApi.timing_decorator
    def Sx6ZHoGa30GK1xH2QbdF(self, nocheck=False):
        data = {
            "childBusinessType": "3",
            "deliverNum": 1,
            "inspectionCenterId": INFO['check_the_center_id'],
            "inspectionCenterCode": INFO['merchant_id']
        }
        return self._make_request('post', 'BvpLVs5Te', data, 'main', nocheck)


class FoIA7X707t(InitializeParams):
    """保卖小程序|我的"""

    @doc(IXznmT0bw7FbeHeJCKo6)
    def IXznmT0bw7FbeHeJCKo6(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(j=1, i=2)
        data = [
            {
                "id": res[0]['id'],
                "saleType": 1,
                "salePricingType": 1
            }
        ]
        return self._make_request('post', 'K2GwqIXJR', data, 'main', nocheck)

    @doc(fCa9uV4NiZ8jEqmYeUCb)
    def fCa9uV4NiZ8jEqmYeUCb(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(j=1, i=2)
        data = [
            {
                "id": res[0]['id'],
                "upbeatPrice": 5900,
                "saleType": 1,
                "salePricingType": "2"
            }
        ]
        return self._make_request('post', 'K2GwqIXJR', data, 'main', nocheck)

    @doc(yFYRFwLu0JNJimcMK5sd)
    def yFYRFwLu0JNJimcMK5sd(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(j=1, i=2)
        data = [
            {
                "id": res[0]['id'],
                "saleType": 1,
                "salePricingType": "3"
            }
        ]
        return self._make_request('post', 'K2GwqIXJR', data, 'main', nocheck)

    @doc(vSYI2uUTSCpcmhYjD9PL)
    def vSYI2uUTSCpcmhYjD9PL(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(j=1, i=2)
        data = {
            "returnReason": "1",
            "returnWay": "1",
            "returnAddressId": INFO['main_user_address_yz_id'],
            "returnArticlesInfoList": [
                {
                    "orderId": res[0]['orderId'],
                    "orderNo": res[0]['consignmentOrderNo'],
                    "articleNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                }
            ]
        }
        return self._make_request('post', 'S4kwZF2CW', data, 'main', nocheck)

    @doc(iGivKV5TSvAIvnbdwJRr)
    def iGivKV5TSvAIvnbdwJRr(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(j=1, i=2)
        data = {
            "returnReason": "1",
            "returnWay": "1",
            "returnAddressId": INFO['main_user_address_yz_id'],
            "returnArticlesInfoList": [
                {
                    "orderId": res[0]['orderId'],
                    "orderNo": res[0]['consignmentOrderNo'],
                    "articleNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                }
            ]
        }
        return self._make_request('post', 'S4kwZF2CW', data, 'main', nocheck)

    @doc(opIdDf5eKi5IeleUQBrA)
    def opIdDf5eKi5IeleUQBrA(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(j=1, i=2)
        data = {
            "returnReason": "1",
            "returnWay": "2",
            "returnAddressId": INFO['main_user_address_yz_id'],
            "returnArticlesInfoList": [
                {
                    "orderId": res[0]['orderId'],
                    "orderNo": res[0]['consignmentOrderNo'],
                    "articleNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                }
            ]
        }
        return self._make_request('post', 'S4kwZF2CW', data, 'main', nocheck)

    @doc(nFqNMqf4dIPEGjrwj8SB)
    def nFqNMqf4dIPEGjrwj8SB(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(j=1, i=3)
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'S9ROIFFJh', data, 'main', nocheck)

    @doc(c6MpT8xfZmLs5uZMq385)
    def c6MpT8xfZmLs5uZMq385(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(j=1, i=3)
        obj = res[0]['id']
        obj_2 = '5900'
        ParamCache.cache_object({"id": obj, "upbeatPrice": obj_2}, 'practical.json')
        data = {
            "id": obj,
            "upbeatPrice": obj_2
        }
        return self._make_request('post', 'yrXPibstn', data, 'main', nocheck)

    @doc(O9TSVizVMFbBHj4PSQi5)
    def O9TSVizVMFbBHj4PSQi5(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(j=1, i=5)
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'S9ROIFFJh', data, 'main', nocheck)

    @doc(D1O3SOVl05gD2Lts19A9)
    def D1O3SOVl05gD2Lts19A9(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(j=1, i=2)
        data = {
            "articlesNo": res[0]['articlesNo'],
            "applyReason": "复检理由",
            "recheckItemInfoList": [
                {
                    "itemId": 52,
                    "itemName": "触摸功能"
                },
                {
                    "itemId": 260,
                    "itemName": "前置摄像头(多选)"
                },
                {
                    "itemId": 85,
                    "itemName": "后置摄像头(多选)"
                },
                {
                    "itemId": 94,
                    "itemName": "闪光灯/手电筒"
                }
            ]
        }
        return self._make_request('post', 'fRmPOvphI', data, 'main', nocheck)

    @doc(zYQJNPRNzQr7xEmj3Xov)
    def zYQJNPRNzQr7xEmj3Xov(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(j=1, i=8)
        data = {
            "articlesNo": res[0]['articlesNo'],
            "addressId": INFO['main_user_address_yz_id'],
            "logisticsType": "1"
        }
        return self._make_request('post', 'pd7yf7Nck', data, 'main', nocheck)

    @doc(Np66pyiMQJz6zbkMLvGH)
    def Np66pyiMQJz6zbkMLvGH(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(j=1, i=8)
        data = {
            "articlesNo": res[0]['articlesNo'],
        }
        return self._make_request('post', 'm4CTVwFIs', data, 'main', nocheck)

    @doc(CPBlWzLFLVwb7oz15BxA)
    def CPBlWzLFLVwb7oz15BxA(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(j=1, i=9)
        data = {
            "articlesNo": res[0]['articlesNo'],
        }
        return self._make_request('post', 'fQDMwXL16', data, 'main', nocheck)

    @doc(ONNJvxBz8YiF5nJbXEx9)
    def ONNJvxBz8YiF5nJbXEx9(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(j=1, i=6)
        data = [
            {
                "id": res[0]['id'],
                "saleType": 3
            }
        ]
        return self._make_request('post', 'K2GwqIXJR', data, 'main', nocheck)

    @doc(cWki4FW4tSlwK63nwMDm)
    def cWki4FW4tSlwK63nwMDm(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(data='b', i=1, j=1)
        res_2 = self.pc.B63gyanXogW9NpUu1Gr1K()
        data = {
            "businessNo": res[0]['orderNo'],
            "childType": 1,
            "recipientPhone": res_2[0]['phone'],
            "recipientName": res_2[0]['operationCenterName'],
            "recipientProvinceId": res_2[0]['provinceId'],
            "recipientProvinceName": res_2[0]['provinceName'],
            "recipientCityId": res_2[0]['cityId'],
            "recipientCityName": res_2[0]['cityName'],
            "recipientCountyId": res_2[0]['countyId'],
            "recipientCountyName": res_2[0]['countyName'],
            "recipientAddress": res_2[0]['address'],
            "senderPhone": INFO['receiving_phone'],
            "senderName": INFO['customer_name'],
            "senderProvinceId": INFO['province_id'],
            "senderProvinceName": INFO['province_name'],
            "senderCityId": INFO['city_id'],
            "senderCityName": INFO['city_name'],
            "senderCountyId": INFO['county_id'],
            "senderCountyName": INFO['county_name'],
            "senderAddress": INFO['detailed_address'],
            "inspectionCenterId": INFO['check_the_center_id'],
            "inspectionCenterCode": INFO['merchant_id'],
            "inspectionCenterName": INFO['check_the_center_name'],
            "expressType": 1,
            "expectPostTimeStart": self.get_formatted_datetime(days=-1)
        }
        return self._make_request('post', 'RPab3Ale0', data, 'main', nocheck)

    @doc(GWIqOqgj1k2cLGBWcfJP)
    def GWIqOqgj1k2cLGBWcfJP(self, nocheck=False, headers_type='main'):
        res = self.pc.D7NTmTMqMuHicClYboqMC(data='b', i=1, j=1)
        res_2 = self.pc.B63gyanXogW9NpUu1Gr1K()
        data = {
            "businessNo": res[0]['orderNo'],
            "childType": 2,
            "recipientPhone": res_2[0]['phone'],
            "recipientName": res_2[0]['operationCenterName'],
            "recipientProvinceId": res_2[0]['provinceId'],
            "recipientProvinceName": res_2[0]['provinceName'],
            "recipientCityId": res_2[0]['cityId'],
            "recipientCityName": res_2[0]['cityName'],
            "recipientCountyId": res_2[0]['countyId'],
            "recipientCountyName": res_2[0]['countyName'],
            "recipientAddress": res_2[0]['address'],
            "senderPhone": INFO['receiving_phone'],
            "senderName": INFO['customer_name'],
            "senderProvinceId": INFO['province_id'],
            "senderProvinceName": INFO['province_name'],
            "senderCityId": INFO['city_id'],
            "senderCityName": INFO['city_name'],
            "senderCountyId": INFO['county_id'],
            "senderCountyName": INFO['county_name'],
            "senderAddress": INFO['detailed_address'],
            "inspectionCenterId": INFO['check_the_center_id'],
            "inspectionCenterCode": INFO['merchant_id'],
            "inspectionCenterName": INFO['check_the_center_name'],
            "expressNo": self.sf,
            "expressCompanyName": "顺丰快运"
        }
        return self._make_request('post', 'RPab3Ale0', data, headers_type, nocheck)

    @doc(fK0PREFRv2Msvl2flpXO)
    def fK0PREFRv2Msvl2flpXO(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(data='b', i=1, j=1)
        res_2 = self.pc.B63gyanXogW9NpUu1Gr1K(i=INFO['camera_merchant_id'])
        data = {
            "businessNo": res[0]['orderNo'],
            "childType": 3,
            "recipientPhone": res_2[0]['phone'],
            "recipientName": res_2[0]['operationCenterName'],
            "recipientProvinceId": res_2[0]['provinceId'],
            "recipientProvinceName": res_2[0]['provinceName'],
            "recipientCityId": res_2[0]['cityId'],
            "recipientCityName": res_2[0]['cityName'],
            "recipientCountyId": res_2[0]['countyId'],
            "recipientCountyName": res_2[0]['countyName'],
            "recipientAddress": res_2[0]['address'],
            "senderPhone": INFO['receiving_phone'],
            "senderName": INFO['customer_name'],
            "senderProvinceId": INFO['province_id'],
            "senderProvinceName": INFO['province_name'],
            "senderCityId": INFO['city_id'],
            "senderCityName": INFO['city_name'],
            "senderCountyId": INFO['county_id'],
            "senderCountyName": INFO['county_name'],
            "senderAddress": INFO['detailed_address'],
            "inspectionCenterId": INFO['camera_check_the_center_id'],
            "inspectionCenterCode": INFO['camera_merchant_id'],
            "inspectionCenterName": INFO['camera_check_the_center_name'],
        }
        return self._make_request('post', 'RPab3Ale0', data, 'main', nocheck)

    @doc(JnMqTWMbAzexR3HQWbXB)
    def JnMqTWMbAzexR3HQWbXB(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(data='b', i=1, j=1)
        res_2 = self.pc.B63gyanXogW9NpUu1Gr1K()
        data = {
            "businessNo": res[0]['orderNo'],
            "childType": 3,
            "recipientPhone": res_2[0]['phone'],
            "recipientName": res_2[0]['operationCenterName'],
            "recipientProvinceId": res_2[0]['provinceId'],
            "recipientProvinceName": res_2[0]['provinceName'],
            "recipientCityId": res_2[0]['cityId'],
            "recipientCityName": res_2[0]['cityName'],
            "recipientCountyId": res_2[0]['countyId'],
            "recipientCountyName": res_2[0]['countyName'],
            "recipientAddress": res_2[0]['address'],
            "senderPhone": INFO['receiving_phone'],
            "senderName": INFO['customer_name'],
            "senderProvinceId": INFO['province_id'],
            "senderProvinceName": INFO['province_name'],
            "senderCityId": INFO['city_id'],
            "senderCityName": INFO['city_name'],
            "senderCountyId": INFO['county_id'],
            "senderCountyName": INFO['county_name'],
            "senderAddress": INFO['detailed_address'],
            "inspectionCenterId": INFO['check_the_center_id'],
            "inspectionCenterCode": INFO['merchant_id'],
            "inspectionCenterName": INFO['check_the_center_name'],
        }
        return self._make_request('post', 'RPab3Ale0', data, 'main', nocheck)

    @doc(DE8blhh3n53JAyeZSU0m)
    def DE8blhh3n53JAyeZSU0m(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(data='b', i=2, j=1)
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'SQVuifMNd', data, 'main', nocheck)

    @doc(h6mvvkdQDZSeUdSoNi8W)
    def h6mvvkdQDZSeUdSoNi8W(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(data='b', i=3, j=1)
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'SQVuifMNd', data, 'main', nocheck)

    @doc(dUwWvkoALcS9DZVO0Ldg)
    def dUwWvkoALcS9DZVO0Ldg(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(data='b', i=3, j=1)
        res_2 = self.pc.B63gyanXogW9NpUu1Gr1K()
        data = {
            "businessNo": res[0]['orderNo'],
            "childType": 1,
            "recipientPhone": res_2[0]['phone'],
            "recipientName": res_2[0]['operationCenterName'],
            "recipientProvinceId": res_2[0]['provinceId'],
            "recipientProvinceName": res_2[0]['provinceName'],
            "recipientCityId": res_2[0]['cityId'],
            "recipientCityName": res_2[0]['cityName'],
            "recipientCountyId": res_2[0]['countyId'],
            "recipientCountyName": res_2[0]['countyName'],
            "recipientAddress": res_2[0]['address'],
            "senderPhone": INFO['receiving_phone'],
            "senderName": INFO['customer_name'],
            "senderProvinceId": INFO['province_id'],
            "senderProvinceName": INFO['province_name'],
            "senderCityId": INFO['city_id'],
            "senderCityName": INFO['city_name'],
            "senderCountyId": INFO['county_id'],
            "senderCountyName": INFO['county_name'],
            "senderAddress": INFO['detailed_address'],
            "inspectionCenterId": INFO['check_the_center_id'],
            "inspectionCenterCode": INFO['merchant_id'],
            "inspectionCenterName": INFO['check_the_center_name'],
            "expressType": 1,
            "expectPostTimeStart": self.get_formatted_datetime(days=-1)
        }
        return self._make_request('post', 'BD4RR09HW', data, 'main', nocheck)

    @doc(POJtV9lZxRzUvoZMBNQB)
    def POJtV9lZxRzUvoZMBNQB(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(data='b', i=3, j=1)
        res_2 = self.pc.B63gyanXogW9NpUu1Gr1K()
        data = {
            "businessNo": res[0]['orderNo'],
            "childType": 2,
            "recipientPhone": res_2[0]['phone'],
            "recipientName": res_2[0]['operationCenterName'],
            "recipientProvinceId": res_2[0]['provinceId'],
            "recipientProvinceName": res_2[0]['provinceName'],
            "recipientCityId": res_2[0]['cityId'],
            "recipientCityName": res_2[0]['cityName'],
            "recipientCountyId": res_2[0]['countyId'],
            "recipientCountyName": res_2[0]['countyName'],
            "recipientAddress": res_2[0]['address'],
            "senderPhone": INFO['receiving_phone'],
            "senderName": INFO['customer_name'],
            "senderProvinceId": INFO['province_id'],
            "senderProvinceName": INFO['province_name'],
            "senderCityId": INFO['city_id'],
            "senderCityName": INFO['city_name'],
            "senderCountyId": INFO['county_id'],
            "senderCountyName": INFO['county_name'],
            "senderAddress": INFO['detailed_address'],
            "inspectionCenterId": INFO['check_the_center_id'],
            "inspectionCenterCode": INFO['merchant_id'],
            "inspectionCenterName": INFO['check_the_center_name'],
            "expressNo": self.sf,
            "expressCompanyName": "中通快递"
        }
        return self._make_request('post', 'BD4RR09HW', data, 'main', nocheck)

    @doc(jHgDbDirasYNbKdklnIY)
    def jHgDbDirasYNbKdklnIY(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(data='b', i=3, j=1)
        res_2 = self.pc.B63gyanXogW9NpUu1Gr1K()
        data = {
            "businessNo": res[0]['orderNo'],
            "childType": 3,
            "recipientPhone": res_2[0]['phone'],
            "recipientName": res_2[0]['operationCenterName'],
            "recipientProvinceId": res_2[0]['provinceId'],
            "recipientProvinceName": res_2[0]['provinceName'],
            "recipientCityId": res_2[0]['cityId'],
            "recipientCityName": res_2[0]['cityName'],
            "recipientCountyId": res_2[0]['countyId'],
            "recipientCountyName": res_2[0]['countyName'],
            "recipientAddress": res_2[0]['address'],
            "senderPhone": INFO['receiving_phone'],
            "senderName": INFO['customer_name'],
            "senderProvinceId": INFO['province_id'],
            "senderProvinceName": INFO['province_name'],
            "senderCityId": INFO['city_id'],
            "senderCityName": INFO['city_name'],
            "senderCountyId": INFO['county_id'],
            "senderCountyName": INFO['county_name'],
            "senderAddress": INFO['detailed_address'],
            "inspectionCenterId": INFO['check_the_center_id'],
            "inspectionCenterCode": INFO['merchant_id'],
            "inspectionCenterName": INFO['check_the_center_name'],
        }
        return self._make_request('post', 'BD4RR09HW', data, 'main', nocheck)

    @doc(axbH6Gue6hxYBUT7LOr0)
    def axbH6Gue6hxYBUT7LOr0(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(data='b', i=1, j=1)
        data = {
            "businessNo": res[0]['orderNo'],
            "childType": 1,
            "recipientPhone": "",
            "recipientName": "",
            "recipientProvinceId": "",
            "recipientProvinceName": "",
            "recipientCityId": "",
            "recipientCityName": "",
            "recipientCountyId": "",
            "recipientCountyName": "",
            "recipientAddress": "",
            "senderPhone": INFO['receiving_phone'],
            "senderName": INFO['customer_name'],
            "senderProvinceId": INFO['province_id'],
            "senderProvinceName": INFO['province_name'],
            "senderCityId": INFO['city_id'],
            "senderCityName": INFO['city_name'],
            "senderCountyId": INFO['county_id'],
            "senderCountyName": INFO['county_name'],
            "senderAddress": INFO['detailed_address'],
            "inspectionCenterId": INFO['check_the_center_id'],
            "inspectionCenterCode": INFO['merchant_id'],
            "inspectionCenterName": INFO['check_the_center_name'],
            "expressType": 1,
            "expectPostTimeStart": self.get_formatted_datetime()
        }

        return self._make_request('post', 'RPab3Ale0', data, 'main', nocheck)

    @doc(jC7q178S4xk9JOlI2EUW)
    def jC7q178S4xk9JOlI2EUW(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(data='b', i=1, j=1)
        res_2 = self.pc.B63gyanXogW9NpUu1Gr1K()
        data = {
            "businessNo": res[0]['orderNo'],
            "childType": 1,
            "recipientPhone": res_2[0]['phone'],
            "recipientName": res_2[0]['operationCenterName'],
            "recipientProvinceId": res_2[0]['provinceId'],
            "recipientProvinceName": res_2[0]['provinceName'],
            "recipientCityId": res_2[0]['cityId'],
            "recipientCityName": res_2[0]['cityName'],
            "recipientCountyId": res_2[0]['countyId'],
            "recipientCountyName": res_2[0]['countyName'],
            "recipientAddress": res_2[0]['address'],
            "senderPhone": INFO['receiving_phone'],
            "senderName": INFO['customer_name'],
            "senderProvinceId": INFO['province_id'],
            "senderProvinceName": INFO['province_name'],
            "senderCityId": INFO['city_id'],
            "senderCityName": INFO['city_name'],
            "senderCountyId": INFO['county_id'],
            "senderCountyName": INFO['county_name'],
            "senderAddress": INFO['detailed_address'],
            "inspectionCenterId": INFO['check_the_center_id'],
            "inspectionCenterCode": INFO['merchant_id'],
            "inspectionCenterName": INFO['check_the_center_name'],
            "expressType": 1,
            "expectPostTimeStart": self.get_formatted_datetime(days=2)
        }
        return self._make_request('post', 'RPab3Ale0', data, 'main', nocheck)

    @doc(QVxsGMaLD5ww9O6KQQSe)
    def QVxsGMaLD5ww9O6KQQSe(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(data='b', i=1, j=1)
        data = {
            "id": res[0]['id']
        }
        return self._make_request('post', 'SQVuifMNd', data, 'main', nocheck)

    @doc(tLLsyo9wcWyBHK8e8y0v)
    def tLLsyo9wcWyBHK8e8y0v(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(j=2, i=7)
        data = {
            "returnReason": "",
            "returnWay": "2",
            "returnAddressId": INFO['main_user_address_yz_id'],
            "returnArticlesInfoList": [
                {
                    "orderId": res[0]['orderId'],
                    "orderNo": res[0]['consignmentOrderNo'],
                    "articleNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                }
            ]
        }
        return self._make_request('post', 'S4kwZF2CW', data, 'main', nocheck)

    @doc(dkzE7aNehgS9qMzBIRzf)
    def dkzE7aNehgS9qMzBIRzf(self, nocheck=None):
        res = self.pc.D7NTmTMqMuHicClYboqMC(data='b', i=1, j=2)
        res_2 = self.pc.B63gyanXogW9NpUu1Gr1K()
        data = {
            "businessNo": res[0]['orderNo'],
            "childType": 1,
            "recipientPhone": res_2[0]['phone'],
            "recipientName": res_2[0]['operationCenterName'],
            "recipientProvinceId": res_2[0]['provinceId'],
            "recipientProvinceName": res_2[0]['provinceName'],
            "recipientCityId": res_2[0]['cityId'],
            "recipientCityName": res_2[0]['cityName'],
            "recipientCountyId": res_2[0]['countyId'],
            "recipientCountyName": res_2[0]['countyName'],
            "recipientAddress": res_2[0]['address'],
            "senderPhone": INFO['receiving_phone'],
            "senderName": INFO['customer_name'],
            "senderProvinceId": INFO['province_id'],
            "senderProvinceName": INFO['province_name'],
            "senderCityId": INFO['city_id'],
            "senderCityName": INFO['city_name'],
            "senderCountyId": INFO['county_id'],
            "senderCountyName": INFO['county_name'],
            "senderAddress": INFO['detailed_address'],
            "inspectionCenterId": INFO['check_the_center_id'],
            "inspectionCenterCode": INFO['merchant_id'],
            "inspectionCenterName": INFO['check_the_center_name'],
            "expressType": 1,
            "expectPostTimeStart": self.get_formatted_datetime(days=-1)
        }
        return self._make_request('post', 'RPab3Ale0', data, 'main', nocheck)

    @doc(oOoG2Yvd9naVzPCCZOBU)
    def oOoG2Yvd9naVzPCCZOBU(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(data='b', i=1, j=2)
        res_2 = self.pc.B63gyanXogW9NpUu1Gr1K()
        data = {
            "businessNo": res[0]['orderNo'],
            "childType": 2,
            "recipientPhone": res_2[0]['phone'],
            "recipientName": res_2[0]['operationCenterName'],
            "recipientProvinceId": res_2[0]['provinceId'],
            "recipientProvinceName": res_2[0]['provinceName'],
            "recipientCityId": res_2[0]['cityId'],
            "recipientCityName": res_2[0]['cityName'],
            "recipientCountyId": res_2[0]['countyId'],
            "recipientCountyName": res_2[0]['countyName'],
            "recipientAddress": res_2[0]['address'],
            "senderPhone": INFO['receiving_phone'],
            "senderName": INFO['customer_name'],
            "senderProvinceId": INFO['province_id'],
            "senderProvinceName": INFO['province_name'],
            "senderCityId": INFO['city_id'],
            "senderCityName": INFO['city_name'],
            "senderCountyId": INFO['county_id'],
            "senderCountyName": INFO['county_name'],
            "senderAddress": INFO['detailed_address'],
            "inspectionCenterId": INFO['check_the_center_id'],
            "inspectionCenterCode": INFO['merchant_id'],
            "inspectionCenterName": INFO['check_the_center_name'],
            "expressNo": self.sf,
            "expressCompanyName": "顺丰快运"
        }
        return self._make_request('post', 'RPab3Ale0', data, 'main', nocheck)

    @doc(KDByBY1AXyw9jWoR1wVN)
    def KDByBY1AXyw9jWoR1wVN(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(data='b', i=1, j=2)
        res_2 = self.pc.B63gyanXogW9NpUu1Gr1K()
        data = {
            "businessNo": res[0]['orderNo'],
            "childType": 3,
            "recipientPhone": res_2[0]['phone'],
            "recipientName": res_2[0]['operationCenterName'],
            "recipientProvinceId": res_2[0]['provinceId'],
            "recipientProvinceName": res_2[0]['provinceName'],
            "recipientCityId": res_2[0]['cityId'],
            "recipientCityName": res_2[0]['cityName'],
            "recipientCountyId": res_2[0]['countyId'],
            "recipientCountyName": res_2[0]['countyName'],
            "recipientAddress": res_2[0]['address'],
            "senderPhone": INFO['receiving_phone'],
            "senderName": INFO['customer_name'],
            "senderProvinceId": INFO['province_id'],
            "senderProvinceName": INFO['province_name'],
            "senderCityId": INFO['city_id'],
            "senderCityName": INFO['city_name'],
            "senderCountyId": INFO['county_id'],
            "senderCountyName": INFO['county_name'],
            "senderAddress": INFO['detailed_address'],
            "inspectionCenterId": INFO['check_the_center_id'],
            "inspectionCenterCode": INFO['merchant_id'],
            "inspectionCenterName": INFO['check_the_center_name'],
        }
        return self._make_request('post', 'RPab3Ale0', data, 'main', nocheck)

    @doc(E0ZBM1bZ77yxxR0xKw5r)
    def E0ZBM1bZ77yxxR0xKw5r(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(data='b', i=1, j=2)
        res_2 = self.pc.B63gyanXogW9NpUu1Gr1K()
        data = {
            "businessNo": res[0]['orderNo'],
            "childType": 1,
            "recipientPhone": res_2[0]['phone'],
            "recipientName": res_2[0]['operationCenterName'],
            "recipientProvinceId": res_2[0]['provinceId'],
            "recipientProvinceName": res_2[0]['provinceName'],
            "recipientCityId": res_2[0]['cityId'],
            "recipientCityName": res_2[0]['cityName'],
            "recipientCountyId": res_2[0]['countyId'],
            "recipientCountyName": res_2[0]['countyName'],
            "recipientAddress": res_2[0]['address'],
            "senderPhone": INFO['receiving_phone'],
            "senderName": INFO['customer_name'],
            "senderProvinceId": INFO['province_id'],
            "senderProvinceName": INFO['province_name'],
            "senderCityId": INFO['city_id'],
            "senderCityName": INFO['city_name'],
            "senderCountyId": INFO['county_id'],
            "senderCountyName": INFO['county_name'],
            "senderAddress": INFO['detailed_address'],
            "inspectionCenterId": INFO['check_the_center_id'],
            "inspectionCenterCode": INFO['merchant_id'],
            "inspectionCenterName": INFO['check_the_center_name'],
            "expressType": 1,
            "expectPostTimeStart": self.get_formatted_datetime(days=2)
        }
        return self._make_request('post', 'RPab3Ale0', data, 'main', nocheck)

    @doc(HU0PCydYlVIqdfWaGMjN)
    def HU0PCydYlVIqdfWaGMjN(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(data='b', i=1, j=2)
        res_2 = self.pc.B63gyanXogW9NpUu1Gr1K()
        data = {
            "businessNo": res[0]['orderNo'],
            "childType": 2,
            "recipientPhone": res_2[0]['phone'],
            "recipientName": res_2[0]['operationCenterName'],
            "recipientProvinceId": res_2[0]['provinceId'],
            "recipientProvinceName": res_2[0]['provinceName'],
            "recipientCityId": res_2[0]['cityId'],
            "recipientCityName": res_2[0]['cityName'],
            "recipientCountyId": res_2[0]['countyId'],
            "recipientCountyName": res_2[0]['countyName'],
            "recipientAddress": res_2[0]['address'],
            "senderPhone": '',
            "senderName": '',
            "senderProvinceId": '',
            "senderProvinceName": '',
            "senderCityId": '',
            "senderCityName": '',
            "senderCountyId": '',
            "senderCountyName": '',
            "senderAddress": '',
            "inspectionCenterId": INFO['check_the_center_id'],
            "inspectionCenterCode": INFO['merchant_id'],
            "inspectionCenterName": INFO['check_the_center_name'],
            "expressNo": self.sf,
            "expressCompanyName": "顺丰速递"
        }
        return self._make_request('post', 'RPab3Ale0', data, 'main', nocheck)

    @doc(PviYbAYqWAHOvqa557i4)
    def PviYbAYqWAHOvqa557i4(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(data='b', i=1, j=2)
        data = {
            "businessNo": res[0]['orderNo'],
            "childType": 1,
            "recipientPhone": "",
            "recipientName": "",
            "recipientProvinceId": "",
            "recipientProvinceName": "",
            "recipientCityId": "",
            "recipientCityName": "",
            "recipientCountyId": "",
            "recipientCountyName": "",
            "recipientAddress": "",
            "senderPhone": INFO['receiving_phone'],
            "senderName": INFO['customer_name'],
            "senderProvinceId": INFO['province_id'],
            "senderProvinceName": INFO['province_name'],
            "senderCityId": INFO['city_id'],
            "senderCityName": INFO['city_name'],
            "senderCountyId": INFO['county_id'],
            "senderCountyName": INFO['county_name'],
            "senderAddress": INFO['detailed_address'],
            "inspectionCenterId": INFO['check_the_center_id'],
            "inspectionCenterCode": INFO['merchant_id'],
            "inspectionCenterName": INFO['check_the_center_name'],
            "expressType": 1,
            "expectPostTimeStart": self.get_formatted_datetime()
        }

        return self._make_request('post', 'RPab3Ale0', data, 'main', nocheck)

    @doc(GG02SXVJvvxVfIaz5KPi)
    def GG02SXVJvvxVfIaz5KPi(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(data='b', i=1, j=2)
        data = {
            "id": res[0]['id']
        }
        return self._make_request('post', 'SQVuifMNd', data, 'main', nocheck)

    @doc(dnH26r9vPAzxPhrGlF4V)
    def dnH26r9vPAzxPhrGlF4V(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(data='b', i=2, j=2)
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'SQVuifMNd', data, 'main', nocheck)

    @doc(t944F3rbr3phQU1rks2g)
    def t944F3rbr3phQU1rks2g(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(data='b', i=3, j=2)
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'SQVuifMNd', data, 'main', nocheck)

    @doc(N77Kx6zXsaGkusHouXhf)
    def N77Kx6zXsaGkusHouXhf(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(data='b', i=3, j=2)
        res_2 = self.pc.B63gyanXogW9NpUu1Gr1K()
        data = {
            "businessNo": res[0]['orderNo'],
            "childType": 3,
            "recipientPhone": res_2[0]['phone'],
            "recipientName": res_2[0]['operationCenterName'],
            "recipientProvinceId": res_2[0]['provinceId'],
            "recipientProvinceName": res_2[0]['provinceName'],
            "recipientCityId": res_2[0]['cityId'],
            "recipientCityName": res_2[0]['cityName'],
            "recipientCountyId": res_2[0]['countyId'],
            "recipientCountyName": res_2[0]['countyName'],
            "recipientAddress": res_2[0]['address'],
            "senderPhone": INFO['receiving_phone'],
            "senderName": INFO['customer_name'],
            "senderProvinceId": INFO['province_id'],
            "senderProvinceName": INFO['province_name'],
            "senderCityId": INFO['city_id'],
            "senderCityName": INFO['city_name'],
            "senderCountyId": INFO['county_id'],
            "senderCountyName": INFO['county_name'],
            "senderAddress": INFO['detailed_address'],
            "inspectionCenterId": INFO['check_the_center_id'],
            "inspectionCenterCode": INFO['merchant_id'],
            "inspectionCenterName": INFO['check_the_center_name'],
            "expressType": 1,
            "expectPostTimeStart": self.get_formatted_datetime(days=-1)
        }
        return self._make_request('post', 'BD4RR09HW', data, 'main', nocheck)

    @doc(P4olp9T5viFuNTxwILbU)
    def P4olp9T5viFuNTxwILbU(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(data='b', i=3, j=2)
        res_2 = self.pc.B63gyanXogW9NpUu1Gr1K()
        data = {
            "businessNo": res[0]['orderNo'],
            "childType": 2,
            "recipientPhone": res_2[0]['phone'],
            "recipientName": res_2[0]['operationCenterName'],
            "recipientProvinceId": res_2[0]['provinceId'],
            "recipientProvinceName": res_2[0]['provinceName'],
            "recipientCityId": res_2[0]['cityId'],
            "recipientCityName": res_2[0]['cityName'],
            "recipientCountyId": res_2[0]['countyId'],
            "recipientCountyName": res_2[0]['countyName'],
            "recipientAddress": res_2[0]['address'],
            "senderPhone": INFO['receiving_phone'],
            "senderName": INFO['customer_name'],
            "senderProvinceId": INFO['province_id'],
            "senderProvinceName": INFO['province_name'],
            "senderCityId": INFO['city_id'],
            "senderCityName": INFO['city_name'],
            "senderCountyId": INFO['county_id'],
            "senderCountyName": INFO['county_name'],
            "senderAddress": INFO['detailed_address'],
            "inspectionCenterId": INFO['check_the_center_id'],
            "inspectionCenterCode": INFO['merchant_id'],
            "inspectionCenterName": INFO['check_the_center_name'],
            "expressNo": self.sf,
            "expressCompanyName": "中通快递"
        }
        return self._make_request('post', 'BD4RR09HW', data, 'main', nocheck)

    @doc(RZQfpgsxpRx4JZVtCxnq)
    def RZQfpgsxpRx4JZVtCxnq(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(data='b', i=3, j=2)
        res_2 = self.pc.B63gyanXogW9NpUu1Gr1K()
        data = {
            "businessNo": res[0]['orderNo'],
            "childType": 3,
            "recipientPhone": res_2[0]['phone'],
            "recipientName": res_2[0]['operationCenterName'],
            "recipientProvinceId": res_2[0]['provinceId'],
            "recipientProvinceName": res_2[0]['provinceName'],
            "recipientCityId": res_2[0]['cityId'],
            "recipientCityName": res_2[0]['cityName'],
            "recipientCountyId": res_2[0]['countyId'],
            "recipientCountyName": res_2[0]['countyName'],
            "recipientAddress": res_2[0]['address'],
            "senderPhone": INFO['receiving_phone'],
            "senderName": INFO['customer_name'],
            "senderProvinceId": INFO['province_id'],
            "senderProvinceName": INFO['province_name'],
            "senderCityId": INFO['city_id'],
            "senderCityName": INFO['city_name'],
            "senderCountyId": INFO['county_id'],
            "senderCountyName": INFO['county_name'],
            "senderAddress": INFO['detailed_address'],
            "inspectionCenterId": INFO['check_the_center_id'],
            "inspectionCenterCode": INFO['merchant_id'],
            "inspectionCenterName": INFO['check_the_center_name'],
        }
        return self._make_request('post', 'BD4RR09HW', data, 'main', nocheck)

    @doc(GgObI3IHddbUmzzKy0Ur)
    def GgObI3IHddbUmzzKy0Ur(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(j=2, i=7)
        data = {
            "returnReason": "",
            "returnWay": "1",
            "returnAddressId": INFO['main_user_address_yz_id'],
            "returnArticlesInfoList": [
                {
                    "orderId": res[0]['orderId'],
                    "orderNo": res[0]['consignmentOrderNo'],
                    "articleNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                }
            ]
        }
        return self._make_request('post', 'S4kwZF2CW', data, 'main', nocheck)

    @doc(bfGgREVaLQ1o2fmtJMrE)
    def bfGgREVaLQ1o2fmtJMrE(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(j=2, i=7)
        data = {
            "articlesNo": res[0]['articlesNo'],
            "applyReason": "",
            "recheckItemInfoList": [
                {
                    "itemId": 0,
                    "itemName": "物品信息"
                }
            ]
        }
        return self._make_request('post', 'fRmPOvphI', data, 'main', nocheck)


if __name__ == '__main__':
    api = ()
    result = api
    # print(result)
    # fast_submit_new_order
    # precise_shipment_estimate
    # auto_submit_new_order
