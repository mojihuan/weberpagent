# coding: utf-8
import json
from common.base_api import BaseApi
from common.base_params import InitializeParams, is_performance_close
from common.file_cache_manager import ParamCache
from common.import_desc import *
from config.user_info import INFO


class GuaranteeReturnsManageRequest(InitializeParams):
    """保卖管理|退货管理"""

    @doc(g_cancel_returns_by_mail)
    @BaseApi.timing_decorator
    def cancel_returns_by_mail(self, nocheck=False):
        res = self.pc.guarantee_returns_manage_data(i=1)
        data = {
            "articlesNo": res[0]['articlesNo']
        }
        return self._make_request('post', 'cancel_a_return', data, 'main', nocheck)

    @doc(g_self_lifted_cancel_a_return)
    @BaseApi.timing_decorator
    def self_lifted_cancel_a_return(self, nocheck=False):
        res = self.pc.guarantee_returns_manage_data(i=2)
        data = {
            "articlesNo": res[0]['articlesNo']
        }
        return self._make_request('post', 'cancel_a_return', data, 'main', nocheck)

    @doc(g_change_the_return_method)
    @BaseApi.timing_decorator
    def change_the_return_method(self, nocheck=False):
        res = self.pc.guarantee_returns_manage_data(i=2)
        data = {
            "articlesNo": res[0]['articlesNo'],
            "logisticsType": 1,
            "addressId": INFO['main_user_address_id']
        }
        return self._make_request('post', 'change_the_return_method', data, 'main', nocheck)

    @doc(g_change_the_return_method_by_mail)
    @BaseApi.timing_decorator
    def change_the_return_method_by_mail(self, nocheck=False):
        res = self.pc.guarantee_returns_manage_data(i=1)
        data = {
            "articlesNo": res[0]['articlesNo'],
            "logisticsType": 2,
            "addressId": 100
        }
        return self._make_request('post', 'change_the_return_method', data, 'main', nocheck)

    @doc(g_confirm_receipt)
    @BaseApi.timing_decorator
    def confirm_receipt(self, nocheck=False):
        res = self.pc.guarantee_returns_manage_data(i=3)
        data = {
            "articlesNo": res[0]['articlesNo'],
        }
        return self._make_request('post', 'confirm_receipt', data, 'main', nocheck)


class GuaranteeOrderManageRequest(InitializeParams):
    """保卖管理|订单列表"""

    @doc(g_quick_guarantee_item_submission)
    @BaseApi.timing_decorator
    def quick_guarantee_item_submission(self, nocheck=False):
        res = self.pc.guarantee_order_manage_data(data='a')
        data = {
            "quickList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "articlesTypeName": res[0]['articlesTypeName'],
                    "brandName": res[0]['brandName'],
                    "modelName": res[0]['modelName'],
                    "skuInfo": res[0]['skuInfo'],
                    "finenessId": res[0]['finenessId'],
                    "finenessName": res[0]['finenessName'],
                    "supplierName": INFO['main_supplier_name'],
                    "warehouseId": INFO['main_item_warehouse_id'],
                    "warehouseName": INFO['main_item_warehouse_name'],
                    "articlesState": res[0]['articlesState'],
                    "inventoryStatus": res[0]['inventoryStatus'],
                    "articlesInfo": {
                        "createBy": res[0]['articlesInfo']['createBy'],
                        "createTime": res[0]['articlesInfo']['createTime'],
                        "updateBy": None,
                        "updateTime": None,
                        "remark": None,
                        "pageSize": 10,
                        "pageNum": 1,
                        "orderByColumn": "create_time",
                        "isAsc": "desc",
                        "erpStartTime": None,
                        "erpEndTime": None,
                        "id": res[0]['articlesInfo']['id'],
                        "articlesNo": res[0]['articlesInfo']['articlesNo'],
                        "articlesTypeId": res[0]['articlesInfo']['articlesTypeId'],
                        "articlesTypeName": res[0]['articlesInfo']['articlesTypeName'],
                        "brandId": res[0]['articlesInfo']['brandId'],
                        "brandName": res[0]['articlesInfo']['brandName'],
                        "modelId": res[0]['articlesInfo']['modelId'],
                        "modelName": res[0]['articlesInfo']['modelName'],
                        "romId": res[0]['articlesInfo']['romId'],
                        "romName": res[0]['articlesInfo']['romName'],
                        "ramId": None,
                        "ramName": "",
                        "colorId": res[0]['articlesInfo']['colorId'],
                        "colorName": res[0]['articlesInfo']['colorName'],
                        "buyChannelId": res[0]['articlesInfo']['buyChannelId'],
                        "buyChannelName": res[0]['articlesInfo']['buyChannelName'],
                        "smallModelId": res[0]['articlesInfo']['smallModelId'],
                        "smallModelName": res[0]['articlesInfo']['smallModelName'],
                        "warrantyDurationId": res[0]['articlesInfo']['warrantyDurationId'],
                        "warrantyDurationName": res[0]['articlesInfo']['warrantyDurationName'],
                        "batteryHealthId": res[0]['articlesInfo']['batteryHealthId'],
                        "batteryHealthName": res[0]['articlesInfo']['batteryHealthName'],
                        "finenessId": res[0]['articlesInfo']['finenessId'],
                        "finenessName": res[0]['articlesInfo']['finenessName'],
                        "networkStandardId": None,
                        "networkStandardName": None,
                        "machineTypeId": res[0]['articlesInfo']['machineTypeId'],
                        "machineTypeName": res[0]['articlesInfo']['machineTypeName'],
                        "mobileNetworkId": None,
                        "mobileNetworkName": None,
                        "unicomNetworkId": None,
                        "unicomNetworkName": None,
                        "telecomNetworkId": None,
                        "telecomNetworkName": None,
                        "lockedId": None,
                        "lockedName": None,
                        "ssdId": None,
                        "ssdName": None,
                        "caseSizeId": None,
                        "caseSizeName": None,
                        "mechanicalHardDriveId": None,
                        "mechanicalHardDriveName": None,
                        "processorId": None,
                        "processorName": None,
                        "graphicsCardModelId": None,
                        "graphicsCardModelName": None,
                        "caseMaterialId": None,
                        "caseMaterialName": None,
                        "connectId": None,
                        "connectName": None,
                        "isDelete": 0,
                        "assessParam": None,
                        "assessTitle": None,
                        "detailId": None,
                        "serialNo": res[0]['articlesInfo']['serialNo'],
                    },
                    "isQualityReport": False,
                    "expectationPrice": 800
                }
            ]
        }
        return self._make_request('post', 'quick_guarantee', data, 'main', nocheck)

    @doc(g_ship_now_by_express_sf)
    @BaseApi.timing_decorator
    def ship_now_by_express_sf(self, nocheck=False):
        res = self.pc.guarantee_order_manage_data(i=1)
        res_2 = self.pc.platform_inspection_center_manage_data()
        data = {
            "businessNo": res[0]['orderNo'],
            "type": 1,
            "childType": 1,
            "expectPostTimeStart": self.get_formatted_datetime(),
            "expressType": 1,
            "senderProvinceName": INFO['province_name'],
            "senderCityName": INFO['city_name'],
            "senderCountyName": INFO['county_name'],
            "senderProvinceId": INFO['province_id'],
            "senderCityId": INFO['city_id'],
            "senderCountyId": INFO['county_id'],
            "senderAddress": INFO['detailed_address'],
            "senderName": res_2[0]['name'],
            "senderPhone": res_2[0]['phone'],
            "recipientProvinceName": res_2[0]['provinceName'],
            "recipientCityName": res_2[0]['cityName'],
            "recipientCountyName": res_2[0]['countyName'],
            "recipientProvinceId": res_2[0]['provinceId'],
            "recipientCityId": res_2[0]['cityId'],
            "recipientCountyId": res_2[0]['countyId'],
            "recipientAddress": res_2[0]['address'],
            "recipientName": INFO['customer_name'],
            "recipientPhone": INFO['receiving_phone'],
            "expectPostTimeStartEnd": self.get_formatted_datetime(),
            "inspectionCenterId": INFO['check_the_center_id'],
        }
        return self._make_request('post', 'confirm_the_order', data, 'main', nocheck)

    @doc(g_ship_now_by_express_jd)
    @BaseApi.timing_decorator
    def ship_now_by_express_jd(self, nocheck=False):
        res = self.pc.guarantee_order_manage_data(i=1)
        res_2 = self.pc.platform_inspection_center_manage_data()
        data = {
            "businessNo": res[0]['orderNo'],
            "type": 1,
            "childType": 2,
            "expectPostTimeStart": self.get_formatted_datetime(),
            "expressType": 2,
            "senderProvinceName": INFO['province_name'],
            "senderCityName": INFO['city_name'],
            "senderCountyName": INFO['county_name'],
            "senderProvinceId": INFO['province_id'],
            "senderCityId": INFO['city_id'],
            "senderCountyId": INFO['county_id'],
            "senderAddress": INFO['detailed_address'],
            "senderName": res_2[0]['name'],
            "senderPhone": res_2[0]['phone'],
            "recipientProvinceName": res_2[0]['provinceName'],
            "recipientCityName": res_2[0]['cityName'],
            "recipientCountyName": res_2[0]['countyName'],
            "recipientProvinceId": res_2[0]['provinceId'],
            "recipientCityId": res_2[0]['cityId'],
            "recipientCountyId": res_2[0]['countyId'],
            "recipientAddress": res_2[0]['address'],
            "recipientName": INFO['customer_name'],
            "recipientPhone": INFO['receiving_phone'],
            "expectPostTimeStartEnd": self.get_formatted_datetime(),
            "inspectionCenterId": INFO['check_the_center_id'],
        }
        return self._make_request('post', 'confirm_the_order', data, 'main', nocheck)

    @doc(g_ship_now_by_express_self_mail)
    @BaseApi.timing_decorator
    def ship_now_by_express_self_mail(self, nocheck=False):
        res = self.pc.guarantee_order_manage_data(i=1)
        res_2 = self.pc.platform_inspection_center_manage_data()
        data = {
            "businessNo": res[0]['orderNo'],
            "type": 1,
            "childType": 3,
            "expectPostTimeStart": self.get_formatted_datetime(),
            "expressCompanyId": "shunfeng",
            "expressNo": self.sf,
            "expressCompanyName": "顺丰速运",
            "inspectionCenterId": INFO['check_the_center_id'],
        }
        return self._make_request('post', 'confirm_the_order', data, 'main', nocheck)

    @doc(g_ship_now_by_express_send_it_yourself)
    @BaseApi.timing_decorator
    def ship_now_by_express_send_it_yourself(self, nocheck=False):
        res = self.pc.guarantee_order_manage_data(i=1)
        res_2 = self.pc.platform_inspection_center_manage_data()
        data = {
            "businessNo": res[0]['orderNo'],
            "type": "2",
            "childType": 3,
            "inspectionCenterId": INFO['check_the_center_id'],
        }
        return self._make_request('post', 'confirm_the_order', data, 'main', nocheck)

    @doc(g_quick_guarantee_cancel_the_order)
    @BaseApi.timing_decorator
    def quick_guarantee_cancel_the_order(self, nocheck=False):
        res = self.pc.guarantee_order_manage_data(i=2)
        data = {
            "id": res[0]['id']
        }
        return self._make_request('post', 'cancel_the_order', data, 'main', nocheck)

    @doc(g_fast_guarantee_reshipment)
    @BaseApi.timing_decorator
    def fast_guarantee_reshipment(self, nocheck=False):
        res = self.pc.guarantee_order_manage_data(i=3)
        res_2 = self.pc.platform_inspection_center_manage_data()
        data = {
            "businessNo": res[0]['orderNo'],
            "type": "1",
            "childType": 1,
            "expectPostTimeStart": self.get_formatted_datetime(),
            "expressType": 1,
            "senderProvinceName": INFO['province_name'],
            "senderCityName": INFO['city_name'],
            "senderCountyName": INFO['county_name'],
            "senderProvinceId": INFO['province_id'],
            "senderCityId": INFO['city_id'],
            "senderCountyId": INFO['county_id'],
            "senderAddress": INFO['detailed_address'],
            "senderName": res_2[0]['name'],
            "senderPhone": res_2[0]['phone'],
            "recipientProvinceName": res_2[0]['provinceName'],
            "recipientCityName": res_2[0]['cityName'],
            "recipientCountyName": res_2[0]['countyName'],
            "recipientProvinceId": res_2[0]['provinceId'],
            "recipientCityId": res_2[0]['cityId'],
            "recipientCountyId": res_2[0]['countyId'],
            "recipientAddress": res_2[0]['address'],
            "recipientName": INFO['customer_name'],
            "recipientPhone": INFO['receiving_phone'],
            "expectPostTimeStartEnd": self.get_formatted_datetime(),
            "inspectionCenterId": INFO['check_the_center_id'],
        }
        return self._make_request('post', 'reship', data, 'main', nocheck)


class GuaranteeGoodsManageRequest(InitializeParams):
    """保卖管理|商品管理"""

    @doc(g_sell_bid_reference_price)
    @BaseApi.timing_decorator
    def sell_bid_reference_price(self, nocheck=False):
        res = self.pc.guarantee_goods_manage_data(i=2)
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = [
            {
                "id": obj,
                "saleType": "1",
                "salePricingType": 1,
                "upbeatPrice": 0
            }
        ]
        return self._make_request('post', 'sales_goods', data, 'main', nocheck)

    @doc(g_sell_bid_self_pricing)
    @BaseApi.timing_decorator
    def sell_bid_self_pricing(self, nocheck=False):
        res = self.pc.guarantee_goods_manage_data(i=2)
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = [
            {
                "id": obj,
                "saleType": "1",
                "salePricingType": 2,
                "upbeatPrice": 50
            }
        ]
        return self._make_request('post', 'sales_goods', data, 'main', nocheck)

    @doc(g_sell_bid_platform_pricing)
    @BaseApi.timing_decorator
    def sell_bid_platform_pricing(self, nocheck=False):
        res = self.pc.guarantee_goods_manage_data(i=2)
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = [
            {
                "id": obj,
                "saleType": "1",
                "salePricingType": 3
            }
        ]
        return self._make_request('post', 'sales_goods', data, 'main', nocheck)

    @doc(g_sell_same_sale_reference_price)
    @BaseApi.timing_decorator
    def sell_same_sale_reference_price(self, nocheck=False):
        res = self.pc.guarantee_goods_manage_data(i=2)
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = [
            {
                "id": obj,
                "saleType": "2",
                "salePricingType": 1,
                "upbeatPrice": 0
            }
        ]
        return self._make_request('post', 'sales_goods', data, 'main', nocheck)

    @doc(g_sell_self_same_sale_pricing)
    @BaseApi.timing_decorator
    def sell_self_same_sale_pricing(self, nocheck=False):
        res = self.pc.guarantee_goods_manage_data(i=2)
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = [
            {
                "id": obj,
                "saleType": "2",
                "salePricingType": 2,
                "upbeatPrice": 50
            }
        ]
        return self._make_request('post', 'sales_goods', data, 'main', nocheck)

    @doc(g_sell_same_sale_platform_pricing)
    @BaseApi.timing_decorator
    def sell_same_sale_platform_pricing(self, nocheck=False):
        res = self.pc.guarantee_goods_manage_data(i=2)
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = [
            {
                "id": obj,
                "saleType": "2",
                "salePricingType": 3
            }
        ]
        return self._make_request('post', 'sales_goods', data, 'main', nocheck)


    @doc(g_cancel_the_sale)
    @BaseApi.timing_decorator
    def cancel_the_sale(self, nocheck=False):
        res = self.pc.guarantee_goods_manage_data(i=3)
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'cancel_sales', data, 'main', nocheck)

    @doc(g_update_price)
    @BaseApi.timing_decorator
    def update_price(self, nocheck=False):
        res = self.pc.guarantee_goods_manage_data(i=3)
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id":obj,
            "upbeatPrice": "50"
        }
        return self._make_request('post', 'update_sales', data, 'main', nocheck)


if __name__ == '__main__':
    api = GuaranteeGoodsManageRequest()
    result = api.cancel_the_sale()
    print(json.dumps(result, indent=4, ensure_ascii=False))
