# coding: utf-8
import json
from common.file_cache_manager import ParamCache
from config.user_info import INFO
from common.base_api import BaseApi
from common.base_params import InitializeParams
from common.import_desc import *

class PurchaseAddRequest(InitializeParams):
    """商品采购|采购管理|新增采购单"""

    @doc(p_new_purchase_order_paid_warehouse)
    @BaseApi.timing_decorator
    def new_purchase_order_paid_warehouse(self, nocheck=False):
        time = self.get_current_timestamp_ms()
        jd = self.jd
        imei = self.imei
        data = {
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "state": "4",
            "purchaseUserId": INFO['main_purchase_user_id'],
            "purchaseUserName": INFO['main_purchase_user_name'],
            "logisticsNo": jd,
            "payState": "1",
            "purchaseSource": "2",
            "logisticsPrice": "11",
            "userId": INFO['main_user_id'],
            "purchaseTime": self.get_formatted_datetime(),
            "warehouseId": INFO['main_item_warehouse_id'],
            "remark": "备注",
            "quickOperation": 0,
            "orderPayInfoList": [
                {
                    "accountNo": INFO['main_account_no'],
                    "voucherImg": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com//erp-imgfiles/%2Fepbox-erp/20250821/WIehcT%2B7sg/I4FjLToJM%2Bw%3D%3D.jpg",
                    "payPrice": 10,
                    "accountName": INFO['main_account_name'],
                }
            ],
            "purchaseOrdersArticlesDTO": {
                "articlesNoList": [
                    None
                ],
                "createBy": "",
                "type": "",
                "userId": "",
                "remark": ""
            },
            "purchaseOrdersArticlesDTOList": [
                {
                    "imei": imei,
                    "serialNo": self.serial_number,
                    "articlesRemake": self.serial,
                    "purchasePrice": 10,
                    "platformArticlesNo": self.serial,
                    "logisticsNo": jd,
                    "warehouseId": INFO['main_item_warehouse_id'],
                    "platformOrderNo": self.serial,
                    "purchaseArticlesInfoDTO": {
                        "brandId": 1,
                        "brandName": "苹果",
                        "modelId": 7695,
                        "modelName": "iPhone 6S Plus",
                        "articlesTypeId": 1,
                        "articlesTypeName": "手机",
                        "imei": imei,
                        "articlesRemake": self.serial,
                        "purchasePrice": 11,
                        "romId": "",
                        "romName": "",
                        "ramId": "",
                        "ramName": "",
                        "colorId": "",
                        "colorName": "",
                        "num": "",
                        "platformArticlesNo": self.serial,
                        "platformOrderNo": self.serial,
                        "serialNo": self.serial_number,
                        "skuInfo": "",
                        "smallModelId": "",
                        "smallModelName": "",
                        "buyChannelId": "",
                        "buyChannelName": "",
                        "batteryHealthId": "",
                        "batteryHealthName": "",
                        "warrantyDurationId": "",
                        "warrantyDurationName": "",
                        "machineTypeId": "",
                        "machineTypeName": "",
                        "finenessId": "",
                        "finenessName": "",
                        "id": time
                    }
                }
            ]
        }

        return self._make_request('post', 'item_new_purchase_order', data, 'main', nocheck)

    @doc(p_new_purchase_order_has_not_been_shipped)
    @BaseApi.timing_decorator
    def new_purchase_order_has_not_been_shipped(self, nocheck=False):
        time = self.get_current_timestamp_ms()
        imei = self.imei
        data = {
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "state": "1",
            "purchaseUserId": INFO['main_purchase_user_id'],
            "purchaseUserName": INFO['main_purchase_user_name'],
            "payState": "2",
            "purchaseSource": "2",
            "userId": INFO['main_user_id'],
            "purchaseTime": self.get_formatted_datetime(),
            "remark": "备注",
            "purchaseOrdersArticlesDTO": {
                "articlesNoList": [
                    None
                ]
            },
            "purchaseOrdersArticlesDTOList": [
                {
                    "imei": imei,
                    "serialNo": self.serial_number,
                    "articlesRemake": self.serial,
                    "purchasePrice": "11",
                    "platformArticlesNo": self.serial,
                    "logisticsNo": "",
                    "warehouseId": "",
                    "platformOrderNo": self.serial,
                    "purchaseArticlesInfoDTO": {
                        "brandId": 1,
                        "brandName": "苹果",
                        "modelId": 7692,
                        "modelName": "iPhone 5S",
                        "articlesTypeId": 1,
                        "articlesTypeName": "手机",
                        "imei": imei,
                        "articlesRemake": self.serial,
                        "purchasePrice": "11",
                        "romId": "",
                        "romName": "",
                        "ramId": "",
                        "ramName": "",
                        "colorId": "",
                        "colorName": "",
                        "num": "",
                        "platformArticlesNo": self.serial,
                        "platformOrderNo": self.serial,
                        "serialNo": self.serial_number,
                        "skuInfo": "",
                        "smallModelId": "",
                        "smallModelName": "",
                        "buyChannelId": "",
                        "buyChannelName": "",
                        "batteryHealthId": "",
                        "batteryHealthName": "",
                        "warrantyDurationId": "",
                        "warrantyDurationName": "",
                        "machineTypeId": "",
                        "machineTypeName": "",
                        "finenessId": "",
                        "finenessName": "",
                        "id": time,
                        "_X_ROW_KEY": "row_21"
                    }
                }
            ]
        }

        return self._make_request('post', 'item_new_purchase_order', data, 'main', nocheck)

    @doc(p_new_purchase_order_unpaid_journey)
    @BaseApi.timing_decorator
    def new_purchase_order_unpaid_journey(self, nocheck=False):
        time = self.get_current_timestamp_ms()
        jd = self.jd
        imei = self.imei
        data = {
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "state": "3",
            "purchaseUserId": INFO['main_purchase_user_id'],
            "purchaseUserName": INFO['main_purchase_user_name'],
            "logisticsNo": jd,
            "payState": "2",
            "purchaseSource": "2",
            "logisticsPrice": "11",
            "userId": INFO['main_user_id'],
            "purchaseTime": self.get_formatted_datetime(),
            "purchaseOrdersArticlesDTO": {
                "articlesNoList": [
                    None
                ]
            },
            "purchaseOrdersArticlesDTOList": [
                {
                    "imei": imei,
                    "platformArticlesNo": self.serial,
                    "articlesRemake": "",
                    "purchasePrice": "11",
                    "logisticsNo": jd,
                    "warehouseId": "",
                    "purchaseArticlesInfoDTO": {
                        "brandId": 1,
                        "brandName": "苹果",
                        "modelId": 7692,
                        "modelName": "iPhone 5S",
                        "articlesTypeId": 1,
                        "articlesTypeName": "手机",
                        "imei": imei,
                        "articlesRemake": "",
                        "purchasePrice": "11",
                        "romId": "",
                        "romName": "",
                        "ramId": "",
                        "ramName": "",
                        "colorId": "",
                        "colorName": "",
                        "num": "",
                        "skuInfo": "",
                        "smallModelId": "",
                        "smallModelName": "",
                        "buyChannelId": "",
                        "buyChannelName": "",
                        "batteryHealthId": "",
                        "batteryHealthName": "",
                        "warrantyDurationId": "",
                        "warrantyDurationName": "",
                        "machineTypeId": "",
                        "machineTypeName": "",
                        "finenessId": "",
                        "finenessName": "",
                        "id": time,
                        "_X_ROW_KEY": "row_22"
                    }
                }
            ]
        }
        return self._make_request('post', 'item_new_purchase_order', data, 'main', nocheck)

    @doc(p_new_purchase_order_unpaid_warehouse)
    @BaseApi.timing_decorator
    def new_purchase_order_unpaid_warehouse(self, nocheck=False):
        time = self.get_current_timestamp_ms()
        jd = self.jd
        imei = self.imei
        data = {
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "state": "4",
            "purchaseUserId": INFO['main_purchase_user_id'],
            "purchaseUserName": INFO['main_purchase_user_name'],
            "logisticsNo": jd,
            "payState": "2",
            "purchaseSource": "2",
            "logisticsPrice": '10',
            "userId": INFO['main_user_id'],
            "purchaseTime": self.get_formatted_datetime(),
            "warehouseId": INFO['main_item_warehouse_id'],
            "remark": self.serial,
            "quickOperation": 0,
            "purchaseOrdersArticlesDTO": {
                "articlesNoList": [
                    None
                ],
                "createBy": "",
                "type": "",
                "userId": "",
                "remark": ""
            },
            "purchaseOrdersArticlesDTOList": [
                {
                    "imei": imei,
                    "serialNo": self.serial_number,
                    "articlesRemake": self.serial,
                    "purchasePrice": '200',
                    "platformArticlesNo": self.serial,
                    "logisticsNo": jd,
                    "warehouseId": INFO['main_item_warehouse_id'],
                    "platformOrderNo": self.serial,
                    "purchaseArticlesInfoDTO": {
                        "brandId": 1,
                        "brandName": "苹果",
                        "modelId": 17569,
                        "modelName": "iPhone 16 Pro Max",
                        "articlesTypeId": 1,
                        "articlesTypeName": "手机",
                        "imei": imei,
                        "articlesRemake": self.serial,
                        "purchasePrice": '200',
                        "romId": 41,
                        "romName": "256G",
                        "ramId": "",
                        "ramName": "",
                        "colorId": 1712,
                        "colorName": "黑色钛金属",
                        "num": "",
                        "platformArticlesNo": self.serial,
                        "platformOrderNo": self.serial,
                        "serialNo": self.serial_number,
                        "skuInfo": "苹果小型号:其他型号;购买渠道:国行;颜色:黑色钛金属;ROM容量:256G;电池健康度:电池健康度≤81%;苹果保修情况:保修时长≥330天;商品来源:二手优品;成色:全新仅拆封;",
                        "smallModelId": 72,
                        "smallModelName": "其他型号",
                        "buyChannelId": 16,
                        "buyChannelName": "国行",
                        "batteryHealthId": 23028,
                        "batteryHealthName": "电池健康度≤81%",
                        "warrantyDurationId": 23005,
                        "warrantyDurationName": "保修时长≥330天",
                        "machineTypeId": 862,
                        "machineTypeName": "二手优品",
                        "finenessId": 1,
                        "finenessName": "全新仅拆封",
                        "id": time,
                    }
                }
            ]
        }
        return self._make_request('post', 'item_new_purchase_order', data, 'main', nocheck)

    @doc(p_create_and_transfer_order)
    @BaseApi.timing_decorator
    def create_and_transfer_order(self, nocheck=False):
        time = self.get_current_timestamp_ms()
        jd = self.jd
        imei = self.imei
        data = {
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "state": "4",
            "purchaseUserId": INFO['main_purchase_user_id'],
            "purchaseUserName": INFO['main_purchase_user_name'],
            "logisticsNo": jd,
            "payState": "1",
            "purchaseSource": "2",
            "logisticsPrice": "11",
            "userId": INFO['main_user_id'],
            "purchaseTime": self.get_formatted_datetime(),
            "warehouseId": INFO['main_item_warehouse_id'],
            "remark": "备注",
            "quickOperation": 1,
            "orderPayInfoList": [
                {
                    "accountNo": INFO['main_account_no'],
                    "voucherImg": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com//erp-imgfiles/%2Fepbox-erp/20250821/WIehcT%2B7sg/I4FjLToJM%2Bw%3D%3D.jpg",
                    "payPrice": 10,
                    "accountName": INFO['main_account_name']
                }
            ],
            "purchaseOrdersArticlesDTO": {
                "articlesNoList": [
                    None
                ],
                "createBy": INFO['special_account_name'],
                "type": "1",
                "userId": INFO['special_user_id'],
                "remark": "移交说明"
            },
            "purchaseOrdersArticlesDTOList": [
                {
                    "imei": imei,
                    "serialNo": self.serial,
                    "articlesRemake": self.serial,
                    "purchasePrice": 10,
                    "platformArticlesNo": self.serial,
                    "logisticsNo": jd,
                    "warehouseId": INFO['main_item_warehouse_id'],
                    "platformOrderNo": self.serial,
                    "purchaseArticlesInfoDTO": {
                        "brandId": 1,
                        "brandName": "苹果",
                        "modelId": 7692,
                        "modelName": "iPhone 5S",
                        "articlesTypeId": 1,
                        "articlesTypeName": "手机",
                        "imei": imei,
                        "articlesRemake": self.serial,
                        "purchasePrice": 10,
                        "romId": 38,
                        "romName": "32G",
                        "ramId": "",
                        "ramName": "",
                        "colorId": 49,
                        "colorName": "金色",
                        "num": "",
                        "platformArticlesNo": self.serial,
                        "platformOrderNo": self.serial,
                        "serialNo": self.serial,
                        "skuInfo": "苹果小型号:A1530;购买渠道:国行;颜色:金色;ROM容量:32G;电池健康度:电池健康度100%;苹果保修情况:保修时长≥330天;商品来源:官翻机;成色:全新仅拆封;",
                        "smallModelId": 94,
                        "smallModelName": "A1530",
                        "buyChannelId": 16,
                        "buyChannelName": "国行",
                        "batteryHealthId": 23024,
                        "batteryHealthName": "电池健康度100%",
                        "warrantyDurationId": 23005,
                        "warrantyDurationName": "保修时长≥330天",
                        "machineTypeId": 863,
                        "machineTypeName": "官翻机",
                        "finenessId": 1,
                        "finenessName": "全新仅拆封",
                        "id": time
                    }
                }
            ]
        }

        return self._make_request('post', 'item_new_purchase_order', data, 'main', nocheck)


class PurchaseUnsendListRequest(InitializeParams):
    """商品采购|采购管理|未发货订单列表"""

    @doc(p_unsend_order_by_supplier)
    @BaseApi.timing_decorator
    def unsend_order_by_supplier(self):
        ParamCache.cache_object({"supplierId": INFO['main_supplier_id']}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "supplierId": INFO['main_supplier_id'],
        }
        return self._make_request('post', 'un_shipped_order', data, 'main')

    @doc(p_unsend_order_by_platform_order_no)
    @BaseApi.timing_decorator
    def unsend_order_by_platform_order_no(self):
        res = self.pc.purchase_unsend_order_list()
        obj = res[0]['platformOrderNo']
        ParamCache.cache_object({"platformOrderNo": obj}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "platformOrderNo": obj,
        }
        return self._make_request('post', 'un_shipped_order', data, 'main')

    @doc(p_unsend_order_by_platform_articles_no)
    @BaseApi.timing_decorator
    def unsend_order_by_platform_articles_no(self):
        res = self.pc.purchase_unsend_order_list()
        obj = res[0]['platformArticlesNo']
        ParamCache.cache_object({"platformArticlesNo": obj}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "platformArticlesNo": obj,
        }
        return self._make_request('post', 'un_shipped_order', data, 'main')

    @doc(p_unsend_order_by_platform_imei)
    @BaseApi.timing_decorator
    def unsend_order_by_platform_imei(self):
        res = self.pc.purchase_unsend_order_list()
        obj = res[0]['imei']
        ParamCache.cache_object({"imei": obj}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "imei": obj,
        }
        return self._make_request('post', 'un_shipped_order', data, 'main')

    @doc(p_unsend_order_by_platform_date)
    @BaseApi.timing_decorator
    def unsend_order_by_platform_date(self):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "dateFrom": self.get_the_date(-1),
            "dateTo": self.get_the_date()
        }
        return self._make_request('post', 'un_shipped_order', data, 'main')


class PurchaseArrivalListRequest(InitializeParams):
    """商品采购|采购管理|到货通知单列表"""

    @doc(p_arrival_list_by_supplier)
    @BaseApi.timing_decorator
    def arrival_list_by_supplier(self):
        ParamCache.cache_object({"supplierId": INFO['main_supplier_id']}, 'practical.json')
        data = {
            "stateList": [
                2,
                3
            ],
            "supplierId": INFO['main_supplier_id'],
            "pageNum": 1,
            "pageSize": 10
        }
        return self._make_request('post', 'arrival_notices', data, 'main')

    @doc(p_arrival_list_by_platform_logistics_no)
    @BaseApi.timing_decorator
    def arrival_list_by_platform_logistics_no(self):
        res = self.pc.purchase_arrival_list()
        obj = res[0]['logisticsNo']
        ParamCache.cache_object({"logisticsNo": obj}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "logisticsNo": obj,
        }
        return self._make_request('post', 'arrival_notices', data, 'main')

    @doc(p_arrival_list_by_platform_order_no)
    @BaseApi.timing_decorator
    def arrival_list_by_platform_order_no(self):
        res = self.pc.purchase_arrival_list()
        obj = res[0]['orderNo']
        ParamCache.cache_object({"orderNo": obj}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "orderNo": obj,
        }
        return self._make_request('post', 'arrival_notices', data, 'main')

    @doc(p_arrival_list_by_platform_date)
    @BaseApi.timing_decorator
    def arrival_list_by_platform_date(self):
        data = {
            "stateList": [
                2,
                3
            ],
            "supplierId": INFO['main_supplier_id'],
            "pageNum": 1,
            "pageSize": 10,
            "creatTimeStart": self.get_the_date(-1),
            "creatTimeEnd": self.get_the_date()
        }
        return self._make_request('post', 'arrival_notices', data, 'main')


class PurchaseAfterSaleListRequest(InitializeParams):
    """商品采购|采购售后管理|采购售后列表"""

    @doc(p_purchase_refund_single)
    @BaseApi.timing_decorator
    def purchase_refund_single(self, nocheck=False):
        res = self.pc.purchase_after_sales_list_data()
        data = {
            "ids": [
                res[0]['id']
            ],
            "saleState": 1,
            "receiveState": 1,
            "purchaseDeliveryTime": self.get_formatted_datetime(),
            "payState": "2",
            "remark": "备注"
        }

        return self._make_request('put', 'purchase_aftermarket_order_details', data, 'main', nocheck)

    @doc(p_purchase_refuse_route)
    @BaseApi.timing_decorator
    def purchase_refuse_route(self, nocheck=False):
        res = self.pc.purchase_after_sales_list_data()
        data = {
            "ids": [
                res[0]['id']
            ],
            "saleState": 2,
            "receiveState": 1,
            "purchaseDeliveryTime": self.get_formatted_datetime(),
            "remark": "备注",
            "logisticsNo": self.jd
        }

        return self._make_request('put', 'purchase_aftermarket_order_details', data, 'main', nocheck)

    @doc(p_purchase_refuse_warehousing)
    @BaseApi.timing_decorator
    def purchase_refuse_warehousing(self, nocheck=False):
        res = self.pc.purchase_after_sales_list_data()
        data = {
            "ids": [
                res[0]['id']
            ],
            "saleState": 2,
            "receiveState": 2,
            "purchaseDeliveryTime": self.get_formatted_datetime(),
            "warehouseId": INFO['main_item_in_warehouse_id']
        }

        return self._make_request('put', 'purchase_aftermarket_order_details', data, 'main', nocheck)

    @doc(p_purchase_after_list_search_by_imei)
    @BaseApi.timing_decorator
    def purchase_after_list_search_by_imei(self):
        res = self.pc.purchase_after_sales_list_data()
        imei = res[0]['imei']
        ParamCache.cache_object({"imei": imei}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "imei": imei,
            "type": "1"
        }
        return self._make_request('post', 'purchase_after_sales_list', data, 'main')

    @doc(p_purchase_after_list_search_by_supplier_id)
    @BaseApi.timing_decorator
    def purchase_after_list_search_by_supplier_id(self):
        ParamCache.cache_object({"supplierId": INFO['main_supplier_id']}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "supplierId": INFO['main_supplier_id'],
            "type": "1"
        }
        return self._make_request('post', 'purchase_after_sales_list', data, 'main')

    @doc(p_purchase_after_list_search_by_platform_articles_no)
    @BaseApi.timing_decorator
    def purchase_after_list_search_by_platform_articles_no(self):
        res = self.pc.purchase_after_sales_list_data()
        ParamCache.cache_object({"platformArticlesNo": res[0]['platformArticlesNo']}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "supplierId": res[0]['platformArticlesNo'],
            "type": "1"
        }
        return self._make_request('post', 'purchase_after_sales_list', data, 'main')

    @doc(p_purchase_after_list_search_by_sale_state)
    @BaseApi.timing_decorator
    def purchase_after_list_search_by_sale_state(self):
        res = self.pc.purchase_after_sales_list_data()
        ParamCache.cache_object({"saleState": res[0]['saleState']}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "saleState": res[0]['saleState'],
            "type": "1"
        }
        return self._make_request('post', 'purchase_after_sales_list', data, 'main')

    @doc(p_purchase_after_list_search_by_sale_no)
    @BaseApi.timing_decorator
    def purchase_after_list_search_by_sale_no(self):
        res = self.pc.purchase_after_sales_list_data()
        ParamCache.cache_object({"saleNo": res[0]['saleNo']}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "saleNo": res[0]['saleNo'],
            "type": "1"
        }
        return self._make_request('post', 'purchase_after_sales_list', data, 'main')

    @doc(p_purchase_after_list_search_by_logistics_no)
    @BaseApi.timing_decorator
    def purchase_after_list_search_by_logistics_no(self):
        res = self.pc.purchase_after_sales_list_data()
        ParamCache.cache_object({"logisticsNo": res[0]['logisticsNo']}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "warehouseLogisticsOrderNo": res[0]['logisticsNo'],
            "type": "1"
        }
        return self._make_request('post', 'purchase_after_sales_list', data, 'main')

    @doc(p_purchase_after_list_search_by_date)
    @BaseApi.timing_decorator
    def purchase_after_list_search_by_date(self):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "type": "1",
            "erpStartTime": self.get_the_date(-1),
            "erpEndTime": self.get_the_date()
        }
        return self._make_request('post', 'purchase_after_sales_list', data, 'main')

    @doc(p_purchase_barter_route)
    @BaseApi.timing_decorator
    def purchase_barter_route(self, nocheck=False):
        res = self.pc.purchase_after_sales_list_data()
        imei = self.imei
        data = {
            "ids": [
                res[0]['id']
            ],
            "saleState": 3,
            "receiveState": 1,
            "purchaseDeliveryTime": self.get_formatted_datetime(),
            "remark": "备注",
            "logisticsNo": self.jd,
            "buildExchangeList": [
                {
                    "saleArticlesRelevanceId": res[0]['id'],
                    "skuInfo": res[0]['skuInfo'],
                    "purchaseArticlesInfoDTO": {
                        "articlesTypeId": 1,
                        "brandId": res[0]['brandId'],
                        "modelId": res[0]['modelId'],
                        "imei": imei,
                        "purchasePrice": "100",
                        "articlesRemake": "",
                        "remark": "",
                        "sourcePurchasePrice": res[0]['purchasePrice'],
                        "modelName": res[0]['modelName'],
                    },
                    "imei": imei,
                    "purchasePrice": "100",
                    "articlesRemake": ""
                }
            ]
        }

        return self._make_request('put', 'purchase_aftermarket_order_details', data, 'main', nocheck)

    @doc(p_purchase_barter_warehousing)
    @BaseApi.timing_decorator
    def purchase_barter_warehousing(self, nocheck=False):
        res = self.pc.purchase_after_sales_list_data()
        imei = self.imei
        data = {
            "ids": [
                res[0]['id']
            ],
            "saleState": 3,
            "receiveState": 2,
            "purchaseDeliveryTime": self.get_formatted_datetime(),
            "remark": "备注",
            "warehouseId": INFO['main_item_warehouse_id'],
            "buildExchangeList": [
                {
                    "saleArticlesRelevanceId": res[0]['id'],
                    "skuInfo": res[0]['skuInfo'],
                    "purchaseArticlesInfoDTO": {
                        "articlesTypeId": 1,
                        "brandId": res[0]['brandId'],
                        "modelId": res[0]['modelId'],
                        "imei": imei,
                        "purchasePrice": "100",
                        "articlesRemake": "",
                        "remark": "",
                        "sourcePurchasePrice": res[0]['purchasePrice'],
                        "modelName": res[0]['modelName'],
                    },
                    "imei": imei,
                    "purchasePrice": "100",
                    "articlesRemake": ""
                }
            ]
        }

        return self._make_request('put', 'purchase_aftermarket_order_details', data, 'main', nocheck)


class PurchaseAwaitAfterSaleListRequest(InitializeParams):
    """商品采购|采购售后管理|待售后列表"""

    @doc(p_purchase_refund_difference_not_settled)
    @BaseApi.timing_decorator
    def purchase_refund_difference_not_settled(self, nocheck=False):
        res = self.pc.purchase_post_sale_list_data()
        data = {
            "payState": "2",
            "purchaseArticlesSaleInfoList": [
                {
                    "saleState": "7",
                    "articlesNo": res[0]['articlesNo'],
                    "newPurchasePrice": 20,
                    "supplierName": INFO['main_supplier_name'],
                    "supplierId": INFO['main_supplier_id']
                }
            ]
        }
        return self._make_request('post', 'after_sale_operate', data, 'main', nocheck)

    @doc(p_purchase_refund_difference_settled)
    @BaseApi.timing_decorator
    def purchase_refund_difference_settled(self, nocheck=False):
        res = self.pc.purchase_post_sale_list_data()
        data = {
            "payState": "1",
            "accountNo": INFO['main_account_no'],
            "accountName": INFO['main_account_name'],
            "purchaseArticlesSaleInfoList": [
                {
                    "saleState": "7",
                    "articlesNo": res[0]['articlesNo'],
                    "newPurchasePrice": 50,
                    "supplierName": INFO['main_supplier_name'],
                    "supplierId": INFO['main_supplier_id']
                }
            ]
        }
        return self._make_request('post', 'after_sale_operate', data, 'main', nocheck)

    @doc(p_after_sales_delivery)
    @BaseApi.timing_decorator
    def after_sales_delivery(self, nocheck=False):
        res = self.pc.purchase_post_sale_list_data()
        data = {
            "saleState": 5,
            "offExpressage": "0",
            "logisticsNoPrice": 11,
            "logisticsOrder": self.jd,
            "supplierName": INFO['main_supplier_name'],
            "supplierId": INFO['main_supplier_id'],
            "purchaseOrdersArticlesDTOList": [
                {
                    "purchaseNo": res[0]['purchaseNo'],
                    "articlesNo": res[0]['articlesNo'],
                    "id": res[0]['id'],
                    "purchasePrice": 10,
                    "saleRemake": "备注"
                }
            ],
            "deliveryTime": self.get_formatted_datetime(),
            "purchaseOrdersSaleInfoDTO": {
                "ids": [
                    res[0]['id']
                ],
                "saleState": 0,
                "receiveState": 1,
                "purchaseDeliveryTime": self.get_formatted_datetime(),
                "payState": "",
                "accountNo": "",
                "accountName": "",
                "remark": "",
                "warehouseId": "",
                "logisticsNo": ""
            }
        }
        return self._make_request('post', 'purchase_after_sales_warehouse', data, 'main', nocheck)

    @doc(p_after_sales_outbound_return_refund_unsettled)
    @BaseApi.timing_decorator
    def after_sales_outbound_return_refund_unsettled(self, nocheck=False):
        res = self.pc.purchase_post_sale_list_data()
        data = {
            "saleState": 5,
            "offExpressage": "0",
            "logisticsNoPrice": 11,
            "logisticsOrder": self.jd,
            "supplierName": INFO['main_supplier_name'],
            "supplierId": INFO['main_supplier_id'],
            "purchaseOrdersArticlesDTOList": [
                {
                    "purchaseNo": res[0]['purchaseNo'],
                    "articlesNo": res[0]['articlesNo'],
                    "id": res[0]['id'],
                    "purchasePrice": 10,
                    "saleRemake": "备注"
                }
            ],
            "deliveryTime": self.get_formatted_datetime(),
            "purchaseOrdersSaleInfoDTO": {
                "ids": [
                    res[0]['id']
                ],
                "saleState": 1,
                "receiveState": 1,
                "purchaseDeliveryTime": self.get_formatted_datetime(),
                "payState": "2",
                "accountNo": "",
                "accountName": "",
                "remark": "test",
                "warehouseId": "",
                "logisticsNo": ""
            }
        }
        return self._make_request('post', 'purchase_after_sales_warehouse', data, 'main', nocheck)

    @doc(p_after_sales_outbound_return_refund_settled)
    @BaseApi.timing_decorator
    def after_sales_outbound_return_refund_settled(self, nocheck=False):
        res = self.pc.purchase_post_sale_list_data()
        data = {
            "saleState": 5,
            "offExpressage": "0",
            "logisticsNoPrice": 0,
            "supplierName": INFO['main_supplier_name'],
            "supplierId": INFO['main_supplier_id'],
            "purchaseOrdersArticlesDTOList": [
                {
                    "purchaseNo": res[0]['purchaseNo'],
                    "articlesNo": res[0]['articlesNo'],
                    "id": res[0]['id'],
                    "purchasePrice": 10,
                    "saleRemake": "备注"
                }
            ],
            "deliveryTime": self.get_formatted_datetime(),
            "purchaseOrdersSaleInfoDTO": {
                "ids": [
                    res[0]['id']
                ],
                "saleState": 1,
                "receiveState": 1,
                "purchaseDeliveryTime": self.get_formatted_datetime(),
                "payState": "1",
                "accountNo": INFO['main_account_no'],
                "accountName": INFO['main_account_name'],
                "remark": "test",
                "warehouseId": "",
                "logisticsNo": ""
            }
        }
        return self._make_request('post', 'purchase_after_sales_warehouse', data, 'main', nocheck)

    @doc(p_after_sales_delivery_refusal_to_return_in_transit)
    @BaseApi.timing_decorator
    def after_sales_delivery_refusal_to_return_in_transit(self, nocheck=False):
        res = self.pc.purchase_post_sale_list_data()
        data = {
            "saleState": 5,
            "offExpressage": "0",
            "logisticsNoPrice": 0,
            "supplierName": INFO['main_supplier_name'],
            "supplierId": INFO['main_supplier_id'],
            "purchaseOrdersArticlesDTOList": [
                {
                    "purchaseNo": res[0]['purchaseNo'],
                    "articlesNo": res[0]['articlesNo'],
                    "id": res[0]['id'],
                    "purchasePrice": 10,
                    "saleRemake": "备注"
                }
            ],
            "deliveryTime": self.get_formatted_datetime(),
            "purchaseOrdersSaleInfoDTO": {
                "ids": [
                    res[0]['id']
                ],
                "saleState": 2,
                "receiveState": 1,
                "purchaseDeliveryTime": self.get_formatted_datetime(),
                "payState": "",
                "accountNo": "",
                "accountName": "",
                "remark": "test",
                "warehouseId": "",
                "logisticsNo": self.jd
            }
        }
        return self._make_request('post', 'purchase_after_sales_warehouse', data, 'main', nocheck)

    @doc(p_after_sales_outbound_refuse_to_return_warehousing)
    @BaseApi.timing_decorator
    def after_sales_outbound_refuse_to_return_warehousing(self, nocheck=False):
        res = self.pc.purchase_post_sale_list_data()
        data = {
            "saleState": 5,
            "offExpressage": "0",
            "logisticsNoPrice": 0,
            "supplierName": INFO['main_supplier_name'],
            "supplierId": INFO['main_supplier_id'],
            "purchaseOrdersArticlesDTOList": [
                {
                    "purchaseNo": res[0]['purchaseNo'],
                    "articlesNo": res[0]['articlesNo'],
                    "id": res[0]['id'],
                    "purchasePrice": 10,
                    "saleRemake": "备注"
                }
            ],
            "deliveryTime": self.get_formatted_datetime(),
            "purchaseOrdersSaleInfoDTO": {
                "ids": [
                    res[0]['id']
                ],
                "saleState": 2,
                "receiveState": 2,
                "purchaseDeliveryTime": self.get_formatted_datetime(),
                "payState": "",
                "accountNo": "",
                "accountName": "",
                "remark": "test",
                "warehouseId": INFO['main_item_in_warehouse_id'],
                "logisticsNo": ""
            }
        }
        return self._make_request('post', 'purchase_after_sales_warehouse', data, 'main', nocheck)

    @doc(p_after_sales_delivery_exchange_in_transit)
    @BaseApi.timing_decorator
    def after_sales_delivery_exchange_in_transit(self, nocheck=False):
        res = self.pc.purchase_post_sale_list_data()
        imei = self.imei
        data = {
            "saleState": 5,
            "offExpressage": "0",
            "logisticsNoPrice": 11,
            "logisticsOrder": self.jd,
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "purchaseOrdersArticlesDTOList": [
                {
                    "purchaseNo": res[0]['purchaseNo'],
                    "articlesNo": res[0]['articlesNo'],
                    "id": res[0]['id'],
                    "purchasePrice": res[0]['purchasePrice'],
                    "saleRemake": "备注"
                }
            ],
            "deliveryTime": self.get_formatted_datetime(),
            "purchaseOrdersSaleInfoDTO": {
                "ids": [
                    res[0]['id']
                ],
                "saleState": 3,
                "receiveState": 2,
                "purchaseDeliveryTime": self.get_formatted_datetime(),
                "payState": "",
                "accountNo": "",
                "accountName": "",
                "remark": "备注",
                "warehouseId": INFO['main_item_warehouse_id'],
                "logisticsNo": "",
                "buildExchangeList": [
                    {
                        "saleArticlesRelevanceId": res[0]['id'],
                        "skuInfo": res[0]['skuInfo'],
                        "purchaseArticlesInfoDTO": {
                            "articlesTypeId": 1,
                            "brandId": res[0]['brandId'],
                            "modelId": res[0]['modelId'],
                            "imei": imei,
                            "purchasePrice": "100",
                            "articlesRemake": "",
                            "remark": "",
                            "sourcePurchasePrice": res[0]['purchasePrice'],
                            "modelName": res[0]['modelName'],
                        },
                        "imei": imei,
                        "purchasePrice": "100",
                        "articlesRemake": ""
                    }
                ]
            }
        }
        return self._make_request('post', 'purchase_after_sales_warehouse', data, 'main', nocheck)

    @doc(p_after_sales_outbound_replacement_warehousing)
    @BaseApi.timing_decorator
    def after_sales_outbound_replacement_warehousing(self, nocheck=False):
        res = self.pc.purchase_post_sale_list_data()
        imei = self.imei
        data = {
            "saleState": 5,
            "offExpressage": "0",
            "logisticsNoPrice": 0,
            "supplierName": INFO['main_supplier_name'],
            "supplierId": INFO['main_supplier_id'],
            "purchaseOrdersArticlesDTOList": [
                {
                    "purchaseNo": res[0]['purchaseNo'],
                    "articlesNo": res[0]['articlesNo'],
                    "id": res[0]['id'],
                    "purchasePrice": res[0]['purchasePrice'],
                    "saleRemake": "备注"
                }
            ],
            "deliveryTime": self.get_formatted_datetime(),
            "purchaseOrdersSaleInfoDTO": {
                "ids": [
                    res[0]['id']
                ],
                "saleState": 3,
                "receiveState": 2,
                "purchaseDeliveryTime": self.get_formatted_datetime(),
                "payState": "",
                "accountNo": "",
                "accountName": "",
                "remark": "",
                "warehouseId": INFO['main_item_in_warehouse_id'],
                "logisticsNo": "",
                "buildExchangeList": [
                    {
                        "saleArticlesRelevanceId": res[0]['id'],
                        "skuInfo": res[0]['skuInfo'],
                        "purchaseArticlesInfoDTO": {
                            "articlesTypeId": 1,
                            "brandId": res[0]['brandId'],
                            "modelId": res[0]['modelId'],
                            "imei": imei,
                            "purchasePrice": "100",
                            "articlesRemake": "",
                            "remark": "",
                            "sourcePurchasePrice": res[0]['purchasePrice'],
                            "modelName": res[0]['modelName'],
                        },
                        "imei": imei,
                        "purchasePrice": "100",
                        "articlesRemake": ""
                    }
                ]
            }
        }
        return self._make_request('post', 'purchase_after_sales_warehouse', data, 'main', nocheck)

    @doc(p_search_by_imei)
    @BaseApi.timing_decorator
    def search_by_imei(self, nocheck=False):
        res = self.pc.purchase_post_sale_list_data()
        data = {
            "remark": "test",
            "articlesNo": res[0]['articlesNo']
        }
        return self._make_request('put', 'after_sale_cancel', data, 'main', nocheck)

    @doc(p_cancel_purchase_after_sale)
    @BaseApi.timing_decorator
    def cancel_purchase_after_sale(self, nocheck=False):
        res = self.pc.purchase_post_sale_list_data()
        data = {
            "remark": "test",
            "articlesNo": res[0]['articlesNo']
        }
        return self._make_request('put', 'after_sale_cancel', data, 'main', nocheck)


class PurchaseGoodsReceivedRequest(InitializeParams):
    """商品采购|采购售后管理|待接收物品"""

    @doc(p_goods_received)
    @BaseApi.timing_decorator
    def goods_received(self, nocheck=False):
        res = self.pc.purchase_items_to_be_received_data()
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'receive_item_receive', data, 'main', nocheck)

    @doc(p_search_by_imei)
    @BaseApi.timing_decorator
    def search_by_imei(self):
        res = self.pc.purchase_items_to_be_received_data()
        obj = res[0]['imei']
        ParamCache.cache_object({"imei": obj}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesNo": obj,
            "articlesState": 10,
            "articlesType": 1
        }
        return self._make_request('post', 'inventory_receive_items', data, 'main')

    @doc(p_search_by_date)
    @BaseApi.timing_decorator
    def search_by_date(self):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesState": 10,
            "articlesType": 1,
            "erpStartTime": self.get_the_date(-1),
            "erpEndTime": self.get_the_date(),
        }
        return self._make_request('post', 'inventory_receive_items', data, 'main')


class PurchaseOrderListRequest(InitializeParams):
    """商品采购|采购管理|采购订单列表"""

    @doc(p_new_purchase_order_refund)
    @BaseApi.timing_decorator
    def new_purchase_order_refund(self, nocheck=False):
        res = self.pc.purchase_order_list_data()
        data = {
            "articlesNo": res[0]['articlesNoList'][0],
            "remark": "备注"
        }

        return self._make_request('post', 'purchases_are_refundable_only', data, 'main', nocheck)

    @doc(p_logistics_delivery)
    @BaseApi.timing_decorator
    def logistics_delivery(self, nocheck=False):
        res = self.pc.purchase_order_list_data()
        data = {
            "logisticsNo": self.jd,
            "purchaseOrdersArticlesDTOList": [
                {
                    "purchaseNo": res[0]['orderNo'],
                    "articlesNo": res[0]['articlesNoList'][0],
                }
            ]
        }

        return self._make_request('post', 'logistics_delivery', data, 'main', nocheck)

    @doc(p_order_list_search_by_purchase_number)
    @BaseApi.timing_decorator
    def order_list_search_by_purchase_number(self):
        res = self.pc.purchase_order_list_data()
        obj = res[0]['orderNo']
        ParamCache.cache_object({"orderNo": obj}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "orderNo": obj,
            "articlesType": 1,
        }
        return self._make_request('post', 'purchase_order_list', data, 'main')

    @doc(p_order_list_search_by_supplier)
    @BaseApi.timing_decorator
    def order_list_search_by_supplier(self):
        ParamCache.cache_object({"supplierId": INFO['main_supplier_id']}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "supplierId": INFO['main_supplier_id'],
            "articlesType": 1,
        }
        return self._make_request('post', 'purchase_order_list', data, 'main')


    @doc(p_order_list_search_by_order_state)
    @BaseApi.timing_decorator
    def order_list_search_by_order_state(self, state_str, state_str_):
        ParamCache.cache_object({"stateStr": state_str_}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "state": state_str,
            "articlesType": 1,
        }
        return self._make_request('post', 'purchase_order_list', data, 'main')

    @doc(p_order_list_search_by_imei)
    @BaseApi.timing_decorator
    def order_list_search_by_imei(self):
        res = self.pc.purchase_order_list_data()
        obj = res[0]['articlesNoList'][0]
        ParamCache.cache_object({"articlesNoList": obj}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesNoOrImei": obj,
            "articlesType": 1,
        }
        return self._make_request('post', 'purchase_order_list', data, 'main')

    @doc(p_order_list_search_by_logistics_no)
    @BaseApi.timing_decorator
    def order_list_search_by_logistics_no(self):
        res = self.pc.purchase_order_list_data()
        obj = res[0]['logisticsNo'][0]
        ParamCache.cache_object({"logisticsNo": obj}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "logisticsNo": obj,
            "articlesType": 1,
        }
        return self._make_request('post', 'purchase_order_list', data, 'main')

    @doc(p_order_list_search_by_pay_state)
    @BaseApi.timing_decorator
    def order_list_search_by_pay_state(self):
        ParamCache.cache_object({"payStateStr": '未付款'}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "payState": 2,
            "articlesType": 1,
        }
        return self._make_request('post', 'purchase_order_list', data, 'main')

    @doc(p_order_list_search_by_purchase_uid)
    @BaseApi.timing_decorator
    def order_list_search_by_purchase_uid(self):
        ParamCache.cache_object({"purchaseUserId": INFO['main_purchase_user_id']}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "purchaseUserId": INFO['main_purchase_user_id'],
            "supplierId": INFO['main_supplier_id'],
            "articlesType": 1,
        }
        return self._make_request('post', 'purchase_order_list', data, 'main')

    @doc(p_order_list_search_by_uid)
    @BaseApi.timing_decorator
    def order_list_search_by_uid(self):
        ParamCache.cache_object({"userId": INFO['main_user_id']}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "userId": INFO['main_user_id'],
            "articlesType": 1,
        }
        return self._make_request('post', 'purchase_order_list', data, 'main')

    @doc(p_order_list_search_by_date)
    @BaseApi.timing_decorator
    def order_list_search_by_date(self):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "erpEndTime": self.get_the_date(),
            "erpStartTime": self.get_the_date(-1),
            "articlesType": 1,
        }
        return self._make_request('post', 'purchase_order_list', data, 'main')


class PurchaseSupplierManageRequest(InitializeParams):
    """商品采购|供应商管理"""

    @doc(p_new_supplier)
    @BaseApi.timing_decorator
    def new_supplier(self, nocheck=False):
        data = {
            "createTime": self.get_formatted_datetime(),
            "pageSize": 10,
            "pageNum": 1,
            "orderByColumn": "create_time",
            "isAsc": "desc",
            "id": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "phone": INFO['receiving_phone'],
            "accountNo": INFO['main_account_no'],
            "level": 0,
            "provinceId": INFO['shipping_province_id'],
            "provinceName": INFO['shipping_province_name'],
            "cityId": INFO['shipping_city_id'],
            "cityName": INFO['shipping_city_name'],
            "countyId": INFO['shipping_county_id'],
            "countyName": INFO['shipping_county_name'],
            "address": INFO['shipping_detailed_address'],
            "userId": INFO['main_user_id'],
            "tenantId": INFO['merchant_id'],
            "isInit": 1,
            "isDelete": 0,
            "supplierType": 1,
            "defaultStatus": 0,
            "type": 2,
            "businessType": 1,
            "supplyType": "1"
        }

        return self._make_request('post', 'supplier_add', data, 'idle', nocheck)

    @doc(p_edit_supplier)
    @BaseApi.timing_decorator
    def edit_supplier(self, nocheck=False):
        res = self.pc.purchase_supplier_manage_data()
        data = {
            "createTime": res[0]['createTime'],
            "updateBy": res[0]['updateBy'],
            "updateTime": self.get_formatted_datetime(),
            "pageSize": 10,
            "pageNum": 1,
            "orderByColumn": "create_time",
            "isAsc": res[0]['isAsc'],
            "id": res[0]['id'],
            "supplierName": res[0]['supplierName'],
            "phone": self.phone,
            "accountNo": res[0]['accountNo'],
            "level": res[0]['level'],
            "provinceId": INFO['province_id'],
            "provinceName": INFO['province_name'],
            "cityId": INFO['city_id'],
            "cityName": INFO['city_name'],
            "countyId": INFO['county_id'],
            "countyName": INFO['county_name'],
            "address": INFO['detailed_address'],
            "userId": res[0]['userId'],
            "tenantId": res[0]['tenantId'],
            "isInit": 1,
            "isDelete": 0,
            "supplierType": 1,
            "defaultStatus": 0,
            "type": 2,
            "businessType": 1,
            "supplyType": "2"
        }

        return self._make_request('put', 'supplier_edit', data, 'idle', nocheck)


class PurchaseWorkOrderRequest(InitializeParams):
    """商品采购|采购管理|采购工单"""

    @doc(p_work_order_add)
    @BaseApi.timing_decorator
    def work_order_add(self, nocheck=False):
        res = self.pc.system_work_order_setting_data()
        res_2 = self.pc.system_work_order_setting_data(data='a')
        start_time = self.get_formatted_datetime()
        end_time = self.get_formatted_datetime(days=1)
        data = {
            "workNum": 1,
            "workStartTime": start_time,
            "workEndTime": end_time,
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "processList": [
                {
                    "processId": res_2[0]['id'],
                    "processNum": 1,
                    "callType": 1,
                    "processStartTime": start_time,
                    "processEndTime": end_time,
                    "processUserIdList": [
                        INFO['main_user_id']
                    ],
                    "defectIdList": [
                        res[0]['id']
                    ],
                    "remark": None,
                    "id": None,
                    "sort": 1
                }
            ],
            "articlesTypeId": 1,
            "articlesTypeName": "手机",
            "brandId": 1,
            "brandName": "苹果",
            "modelId": 7692,
            "modelName": "iPhone 5S",
            "skuInfo": "苹果 iPhone 5S "
        }

        return self._make_request('post', 'work_order_add', data, 'main', nocheck)

    @doc(p_work_order_edit)
    @BaseApi.timing_decorator
    def work_order_edit(self, nocheck=False):
        res = self.pc.purchase_work_order_data()
        res_2 = self.pc.system_work_order_setting_data()
        res_3 = self.pc.system_work_order_setting_data(data='a')
        res_4 = self.post_api.purchase_work_order.get_task_id()
        start_time = self.get_formatted_datetime()
        end_time = self.get_formatted_datetime(days=1)
        data = {
            "id": res[0]['id'],
            "workNum": 2,
            "workStartTime": start_time,
            "workEndTime": end_time,
            "supplierId": INFO['main_supplier_id'],
            "supplierName": "壹站收",
            "processList": [
                {
                    "processId": res_3[0]['id'],
                    "processNum": 2,
                    "callType": 1,
                    "processStartTime": start_time,
                    "processEndTime": end_time,
                    "processUserIdList": [
                        INFO['main_user_id']
                    ],
                    "defectIdList": [
                        res_2[0]['id'],
                    ],
                    "remark": None,
                    "id": res_4,
                    "sort": 1
                }
            ]
        }

        return self._make_request('put', 'work_order_add', data, 'main', nocheck)

    @doc(p_work_order_to_start_the_task)
    @BaseApi.timing_decorator
    def work_order_to_start_the_task(self, nocheck=False):
        res = self.pc.purchase_work_order_data()
        data = [
            res[0]['id']
        ]
        return self._make_request('post', 'the_work_order_starts_the_task', data, 'main', nocheck)

    @doc(p_work_order_ends_the_task)
    @BaseApi.timing_decorator
    def work_order_ends_the_task(self):
        self.work_order_to_start_the_task()

    @doc(p_work_order_resumes_tasks)
    @BaseApi.timing_decorator
    def work_order_resumes_tasks(self):
        self.work_order_to_start_the_task()

    @doc(p_work_order_del)
    @BaseApi.timing_decorator
    def work_order_del(self, nocheck=False):
        res = self.pc.purchase_work_order_data()
        data = [
            res[0]['id'],
        ]

        return self._make_request('put', 'work_order_del', data, 'main', nocheck)


if __name__ == '__main__':
    api = PurchaseAddRequest()
    result = api.new_purchase_order_paid_warehouse()
    # print(json.dumps(result, indent=4, ensure_ascii=False))

