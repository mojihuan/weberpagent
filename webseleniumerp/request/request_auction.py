# coding: utf-8
import json
from common.base_api import BaseApi
from common.base_params import InitializeParams
from common.file_cache_manager import ParamCache
from config.user_info import INFO
from common.import_desc import *

class AuctionIndexRequest(InitializeParams):
    """首页"""

    @doc(a_fast_submit_new_order)
    def fast_submit_new_order(self, nocheck=False):
        data = {
            "childBusinessType": "2",
            "deliverNum": 1,
            "inspectionCenterId": INFO['check_the_center_id'],
            "inspectionCenterCode": INFO['merchant_id'],
            "expectationTotalPrice": "5555"
        }
        return self._make_request('post', 'submit_new_order', data, 'main', nocheck)

    @doc(a_large_quantity_fast_submit_new_order)
    def large_quantity_fast_submit_new_order(self, nocheck=False):
        res = self.pc.platform_inspection_center_manage_data()
        data = {
            "childBusinessType": "2",
            "deliverNum": 5,
            "inspectionCenterId": INFO['check_the_center_id'],
            "inspectionCenterCode": INFO['merchant_id'],
            "expectationTotalPrice": "4567"
        }
        return self._make_request('post', 'submit_new_order', data, 'main', nocheck)

    @doc(a_max_quantity_fast_submit_new_order)
    def max_quantity_fast_submit_new_order(self, nocheck=False):
        res = self.pc.platform_inspection_center_manage_data()
        data = {
            "childBusinessType": "2",
            "deliverNum": 1000,
            "inspectionCenterId": INFO['check_the_center_id'],
            "inspectionCenterCode": INFO['merchant_id'],
            "expectationTotalPrice": "2734"
        }
        return self._make_request('post', 'submit_new_order', data, 'main', nocheck)

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
        return self._make_request('post', 'valuation', data, 'main', nocheck)


    @doc(a_auto_submit_new_order)
    @BaseApi.timing_decorator
    def auto_submit_new_order(self, nocheck=False):
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
        return self._make_request('post', 'submit_new_order', data, 'main', nocheck)

    @doc(a_quality_inspection_service_create_an_order)
    @BaseApi.timing_decorator
    def quality_inspection_service_create_an_order(self, nocheck=False):
        data = {
            "childBusinessType": "3",
            "deliverNum": 1,
            "inspectionCenterId": INFO['check_the_center_id'],
            "inspectionCenterCode": INFO['merchant_id']
        }
        return self._make_request('post', 'submit_new_order', data, 'main', nocheck)


class AuctionMyRequest(InitializeParams):
    """我的"""

    @doc(a_sales_out_warehouse)
    def sales_out_warehouse(self,nocheck=False):
        res = self.pc.auction_my_data(j=1, i=2)
        data = [
            {
                "id": res[0]['id'],
                "saleType": 1,
                "salePricingType": 1
            }
        ]
        return self._make_request('post', 'sales_out_warehouse', data, 'main', nocheck)


    @doc(a_self_pricing_selling_items)
    def self_pricing_selling_items(self, nocheck=False):
        res = self.pc.auction_my_data(j=1, i=2)
        data = [
            {
                "id": res[0]['id'],
                "upbeatPrice": 5900,
                "saleType": 1,
                "salePricingType": "2"
            }
        ]
        return self._make_request('post', 'sales_out_warehouse', data, 'main', nocheck)

    @doc(a_together_xy_sell_items)
    def together_xy_sell_items(self, nocheck=False):
        res = self.pc.auction_my_data(j=1, i=2)
        data = [
            {
                "id": res[0]['id'],
                "saleType": 1,
                "salePricingType": "3"
            }
        ]
        return self._make_request('post', 'sales_out_warehouse', data, 'main', nocheck)

    @doc(a_express_easy_return)
    def express_easy_return(self, nocheck=False):
        res = self.pc.auction_my_data(j=1, i=2)
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
        return self._make_request('post', 'returnable', data, 'main', nocheck)

    @doc(a_sell_no_quality_check_return)
    def sell_no_quality_check_return(self, nocheck=False):
        res = self.pc.auction_my_data(j=1, i=2)
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
        return self._make_request('post', 'returnable', data, 'main', nocheck)

    @doc(a_self_pickup_returns)
    def self_pickup_returns(self, nocheck=False):
        res = self.pc.auction_my_data(j=1, i=2)
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
        return self._make_request('post', 'returnable', data, 'main', nocheck)

    @doc(a_cancel_the_sale)
    def cancel_the_sale(self, nocheck=False):
        res = self.pc.auction_my_data(j=1, i=3)
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'bm_cancel_the_sale', data, 'main', nocheck)

    @doc(a_price_change_during_sales)
    def price_change_during_sales(self, nocheck=False):
        res = self.pc.auction_my_data(j=1, i=3)
        obj = res[0]['id']
        obj_2 = '5900'
        ParamCache.cache_object({"id": obj, "upbeatPrice": obj_2}, 'practical.json')
        data = {
            "id": obj,
            "upbeatPrice": obj_2
        }
        return self._make_request('post', 'price_change', data, 'main', nocheck)

    @doc(a_platform_cancel_the_sale)
    def platform_cancel_the_sale(self, nocheck=False):
        res = self.pc.auction_my_data(j=1, i=5)
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'bm_cancel_the_sale', data, 'main', nocheck)

    @doc(a_sales_re_inspection)
    def sales_re_inspection(self, nocheck=False):
        res = self.pc.auction_my_data(j=1, i=2)
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
        return self._make_request('post', 'reinspection', data, 'main', nocheck)

    @doc(a_change_the_return_method)
    def change_the_return_method(self, nocheck=False):
        res = self.pc.auction_my_data(j=1, i=8)
        data = {
            "articlesNo": res[0]['articlesNo'],
            "addressId": INFO['main_user_address_yz_id'],
            "logisticsType": "1"
        }
        return self._make_request('post', 'bm_change_the_return_method', data, 'main', nocheck)

    @doc(a_cancel_the_return)
    def cancel_the_return(self, nocheck=False):
        res = self.pc.auction_my_data(j=1, i=8)
        data = {
            "articlesNo": res[0]['articlesNo'],
        }
        return self._make_request('post', 'cancel_the_return', data, 'main', nocheck)

    @doc(a_confirm_receipt)
    def confirm_receipt(self, nocheck=False):
        res = self.pc.auction_my_data(j=1, i=9)
        data = {
            "articlesNo": res[0]['articlesNo'],
        }
        return self._make_request('post', 'bm_confirm_receipt', data, 'main', nocheck)

    @doc(a_offer_confirms_sale)
    def offer_confirms_sale(self, nocheck=False):
        res = self.pc.auction_my_data(j=1, i=6)
        data = [
            {
                "id": res[0]['id'],
                "saleType": 3
            }
        ]
        return self._make_request('post', 'sales_out_warehouse', data, 'main', nocheck)

    @doc(a_shipped_immediately_sf)
    def shipped_immediately_sf(self, nocheck=False):
        res = self.pc.auction_my_data(data='b', i=1, j=1)
        res_2 = self.pc.platform_inspection_center_manage_data()
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
        return self._make_request('post', 'delivery_goods', data, 'main', nocheck)

    @doc(a_shipped_immediately_own)
    def shipped_immediately_own(self, nocheck=False, headers_type='main'):
        res = self.pc.auction_my_data(data='b', i=1, j=1)
        res_2 = self.pc.platform_inspection_center_manage_data()
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
        return self._make_request('post', 'delivery_goods', data, headers_type, nocheck)

    @doc(a_deliver_it_yourself)
    def deliver_it_yourself(self, nocheck=False):
        res = self.pc.auction_my_data(data='b', i=1, j=1)
        res_2 = self.pc.platform_inspection_center_manage_data()
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
        return self._make_request('post', 'delivery_goods', data, 'main', nocheck)

    @doc(a_pending_pickup_cancel_the_order)
    def pending_pickup_cancel_the_order(self, nocheck=False):
        res = self.pc.auction_my_data(data='b', i=2, j=1)
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'bm_cancel_the_order', data, 'main', nocheck)

    @doc(a_pending_receipt_cancel_the_order)
    def pending_receipt_cancel_the_order(self, nocheck=False):
        res = self.pc.auction_my_data(data='b', i=3, j=1)
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'bm_cancel_the_order', data, 'main', nocheck)

    @doc(a_pending_receipt_of_reshipment_by_sf_logistics)
    def pending_receipt_of_reshipment_by_sf_logistics(self, nocheck=False):
        res = self.pc.auction_my_data(data='b', i=3, j=1)
        res_2 = self.pc.platform_inspection_center_manage_data()
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
        return self._make_request('post', 'bm_reship', data, 'main', nocheck)

    @doc(a_pending_receipt_reshipment_self_mailing)
    def pending_receipt_reshipment_self_mailing(self, nocheck=False):
        res = self.pc.auction_my_data(data='b', i=3, j=1)
        res_2 = self.pc.platform_inspection_center_manage_data()
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
        return self._make_request('post', 'bm_reship', data, 'main', nocheck)

    @doc(a_pending_receipt_reshipment_deliver_it_yourself)
    def pending_receipt_reshipment_deliver_it_yourself(self, nocheck=False):
        res = self.pc.auction_my_data(data='b', i=3, j=1)
        res_2 = self.pc.platform_inspection_center_manage_data()
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
        return self._make_request('post', 'bm_reship', data, 'main', nocheck)

    @doc(a_shipped_immediately_no_shipping_address)
    def shipped_immediately_no_shipping_address(self, nocheck=False):
        res = self.pc.auction_my_data(data='b', i=1, j=1)
        res_2 = self.pc.platform_inspection_center_manage_data()
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

        return self._make_request('post', 'delivery_goods', data, 'main', nocheck)

    @doc(a_shipped_immediately_sf_the_next_day)
    def shipped_immediately_sf_the_next_day(self, nocheck=False):
        res = self.pc.auction_my_data(data='b', i=1, j=1)
        res_2 = self.pc.platform_inspection_center_manage_data()
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
        return self._make_request('post', 'delivery_goods', data, 'main', nocheck)

    @doc(a_cancel_the_order)
    def cancel_the_order(self, nocheck=False):
        res = self.pc.auction_my_data(data='b', i=1, j=1)
        data = {
            "id": res[0]['id']
        }
        return self._make_request('post', 'bm_cancel_the_order', data, 'main', nocheck)

    @doc(a_quality_self_pickup_returns)
    def quality_self_pickup_returns(self, nocheck=False):
        res = self.pc.auction_my_data(j=2, i=7)
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
        return self._make_request('post', 'returnable', data, 'main', nocheck)

    @doc(a_quality_shipped_immediately_sf)
    def quality_shipped_immediately_sf(self, nocheck=None):
        res = self.pc.auction_my_data(data='b', i=1, j=2)
        res_2 = self.pc.platform_inspection_center_manage_data()
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
        return self._make_request('post', 'delivery_goods', data, 'main', nocheck)

    @doc(a_quality_shipped_immediately_own)
    def quality_shipped_immediately_own(self, nocheck=False):
        res = self.pc.auction_my_data(data='b', i=1, j=2)
        res_2 = self.pc.platform_inspection_center_manage_data()
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
        return self._make_request('post', 'delivery_goods', data, 'main', nocheck)

    @doc(a_quality_deliver_it_yourself)
    def quality_deliver_it_yourself(self, nocheck=False):
        res = self.pc.auction_my_data(data='b', i=1, j=2)
        res_2 = self.pc.platform_inspection_center_manage_data()
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
        return self._make_request('post', 'delivery_goods', data, 'main', nocheck)

    @doc(a_quality_shipped_immediately_sf_the_next_day)
    def quality_shipped_immediately_sf_the_next_day(self, nocheck=False):
        res = self.pc.auction_my_data(data='b', i=1, j=2)
        res_2 = self.pc.platform_inspection_center_manage_data()
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
        return self._make_request('post', 'delivery_goods', data, 'main', nocheck)

    @doc(a_quality_shipped_immediately_no_address)
    def quality_shipped_immediately_no_address(self, nocheck=False):
        res = self.pc.auction_my_data(data='b', i=1, j=2)
        res_2 = self.pc.platform_inspection_center_manage_data()
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
        return self._make_request('post', 'delivery_goods', data, 'main', nocheck)

    @doc(a_quality_shipped_immediately_no_shipping_address)
    def quality_shipped_immediately_no_shipping_address(self, nocheck=False):
        res = self.pc.auction_my_data(data='b', i=1, j=2)
        res_2 = self.pc.platform_inspection_center_manage_data()
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

        return self._make_request('post', 'delivery_goods', data, 'main', nocheck)

    @doc(a_quality_cancel_the_order)
    def quality_cancel_the_order(self, nocheck=False):
        res = self.pc.auction_my_data(data='b', i=1, j=2)
        data = {
            "id": res[0]['id']
        }
        return self._make_request('post', 'bm_cancel_the_order', data, 'main', nocheck)

    @doc(a_quality_pending_pickup_cancel_the_order)
    def quality_pending_pickup_cancel_the_order(self, nocheck=False):
        res = self.pc.auction_my_data(data='b', i=2, j=2)
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'bm_cancel_the_order', data, 'main', nocheck)

    @doc(a_quality_pending_receipt_cancel_the_order)
    def quality_pending_receipt_cancel_the_order(self, nocheck=False):
        res = self.pc.auction_my_data(data='b', i=3, j=2)
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'bm_cancel_the_order', data, 'main', nocheck)

    @doc(a_quality_pending_receipt_of_reshipment_by_sf_logistics)
    def quality_pending_receipt_of_reshipment_by_sf_logistics(self, nocheck=False):
        res = self.pc.auction_my_data(data='b', i=3, j=2)
        res_2 = self.pc.platform_inspection_center_manage_data()
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
        return self._make_request('post', 'bm_reship', data, 'main', nocheck)

    @doc(a_quality_pending_receipt_reshipment_self_mailing)
    def quality_pending_receipt_reshipment_self_mailing(self, nocheck=False):
        res = self.pc.auction_my_data(data='b', i=3, j=2)
        res_2 = self.pc.platform_inspection_center_manage_data()
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
        return self._make_request('post', 'bm_reship', data, 'main', nocheck)

    @doc(a_quality_pending_receipt_reshipment_deliver_it_yourself)
    def quality_pending_receipt_reshipment_deliver_it_yourself(self, nocheck=False):
        res = self.pc.auction_my_data(data='b', i=3, j=2)
        res_2 = self.pc.platform_inspection_center_manage_data()
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
        return self._make_request('post', 'bm_reship', data, 'main', nocheck)

    @doc(a_quality_inspection_completed_express_return)
    def quality_inspection_completed_express_return(self, nocheck=False):
        res = self.pc.auction_my_data(j=2, i=7)
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
        return self._make_request('post', 'returnable', data, 'main', nocheck)

    @doc(a_quality_sales_re_inspection)
    def quality_sales_re_inspection(self, nocheck=False):
        res = self.pc.auction_my_data(j=2, i=7)
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
        return self._make_request('post', 'reinspection', data, 'main', nocheck)


if __name__ == '__main__':
    api = AuctionIndexRequest()
    result = api.auto_submit_new_order()
    # print(result)
    # fast_submit_new_order
    # precise_shipment_estimate
    # auto_submit_new_order