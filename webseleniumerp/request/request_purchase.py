# coding: utf-8
import json
from common.file_cache_manager import ParamCache
from config.user_info import INFO
from common.base_api import BaseApi
from common.base_params import InitializeParams
from common.import_desc import *


class ZTKvMx4gs4(InitializeParams):
    """商品采购|采购管理|新增采购单"""

    @doc(Iv2a1sAnyG1YRbkyU84V)
    @BaseApi.timing_decorator
    def Iv2a1sAnyG1YRbkyU84V(self, nocheck=False):
        time = self.get_current_timestamp_ms()
        sf = self.sf
        data = {
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "state": "4",
            "purchaseUserId": INFO['main_purchase_user_id'],
            "purchaseUserName": INFO['main_purchase_user_name'],
            "logisticsNo": sf,
            "payState": "1",
            "purchaseSource": "2",
            "logisticsPrice": "11",
            "userId": INFO['main_user_id'],
            "purchaseTime": self.get_formatted_datetime(),
            "warehouseId": 490,
            "remark": "备注",
            "quickOperation": 0,
            "orderPayInfoList": [
                {
                    "accountNo": INFO['main_account_no'],
                    "voucherImg": "",
                    "payPrice": 10,
                    "accountName": INFO['main_account_name']
                }
            ],
            "purchaseOrdersArticlesDTO": {
                "articlesNoList": [
                    None,
                    None
                ],
                "createBy": "",
                "type": "",
                "userId": "",
                "remark": ""
            },
            "purchaseOrdersArticlesDTOList": [
                {
                    "imei": self.imei,
                    "articlesRemake": "描述",
                    "purchasePrice": "100",
                    "logisticsNo": sf,
                    "warehouseId": 490,
                    "supplyType": 1,
                    "supplyTypeDesc": "A",
                    "purchaseArticlesInfoDTO": {
                        "brandId": 1,
                        "brandName": "苹果",
                        "modelId": 17569,
                        "modelName": "iPhone 16 Pro Max",
                        "articlesTypeId": 1,
                        "articlesTypeName": "手机",
                        "imei": self.imei,
                        "articlesRemake": "描述",
                        "purchasePrice": "100",
                        "romId": 41,
                        "romName": "256G",
                        "ramId": "",
                        "ramName": "",
                        "colorId": 1712,
                        "colorName": "黑色钛金属",
                        "num": "10",
                        "skuInfo": "苹果小型号:A3297;购买渠道:国行;颜色:黑色钛金属;ROM容量:256G;电池健康度:电池健康度100%;苹果保修情况:保修时长≥330天;商品来源:二手优品;成色:99新;",
                        "smallModelId": 1743,
                        "smallModelName": "A3297",
                        "buyChannelId": 16,
                        "buyChannelName": "国行",
                        "batteryHealthId": 23024,
                        "batteryHealthName": "电池健康度100%",
                        "warrantyDurationId": 23005,
                        "warrantyDurationName": "保修时长≥330天",
                        "machineTypeId": 862,
                        "machineTypeName": "二手优品",
                        "finenessId": 2,
                        "finenessName": "99新",
                        "id": time,
                        "_X_ROW_KEY": "row_43"
                    }
                },
                {
                    "imei": self.imei,
                    "articlesRemake": "描述",
                    "purchasePrice": "100",
                    "logisticsNo": sf,
                    "warehouseId": 490,
                    "supplyType": 1,
                    "supplyTypeDesc": "A",
                    "purchaseArticlesInfoDTO": {
                        "brandId": 1,
                        "brandName": "苹果",
                        "modelId": 17569,
                        "modelName": "iPhone 16 Pro Max",
                        "articlesTypeId": 1,
                        "articlesTypeName": "手机",
                        "imei": self.imei,
                        "articlesRemake": "描述",
                        "purchasePrice": "100",
                        "romId": 41,
                        "romName": "256G",
                        "ramId": "",
                        "ramName": "",
                        "colorId": 1712,
                        "colorName": "黑色钛金属",
                        "num": "10",
                        "skuInfo": "苹果小型号:A3297;购买渠道:国行;颜色:黑色钛金属;ROM容量:256G;电池健康度:电池健康度100%;苹果保修情况:保修时长≥330天;商品来源:二手优品;成色:99新;",
                        "smallModelId": 1743,
                        "smallModelName": "A3297",
                        "buyChannelId": 16,
                        "buyChannelName": "国行",
                        "batteryHealthId": 23024,
                        "batteryHealthName": "电池健康度100%",
                        "warrantyDurationId": 23005,
                        "warrantyDurationName": "保修时长≥330天",
                        "machineTypeId": 862,
                        "machineTypeName": "二手优品",
                        "finenessId": 2,
                        "finenessName": "99新",
                        "id": time,
                        "_X_ROW_KEY": "row_44"
                    }
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'km9X0jSmr', data, 'main', nocheck)

    @doc(W8Tva7jFU0AkEqegXRnE)
    @BaseApi.timing_decorator
    def W8Tva7jFU0AkEqegXRnE(self, nocheck=False):
        time = self.get_current_timestamp_ms()
        sf = self.sf
        data = {
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "state": "4",
            "purchaseUserId": INFO['main_purchase_user_id'],
            "purchaseUserName": INFO['main_purchase_user_name'],
            "logisticsNo": sf,
            "payState": "1",
            "purchaseSource": "2",
            "logisticsPrice": "11",
            "userId": INFO['main_user_id'],
            "purchaseTime": self.get_formatted_datetime(),
            "warehouseId": 490,
            "remark": "备注",
            "quickOperation": 0,
            "orderPayInfoList": [
                {
                    "accountNo": INFO['main_account_no'],
                    "voucherImg": "",
                    "payPrice": 100,
                    "accountName": INFO['main_account_name']
                }
            ],
            "purchaseOrdersArticlesDTO": {
                "articlesNoList": [
                    None,
                    None
                ],
                "createBy": "",
                "type": "",
                "userId": "",
                "remark": ""
            },
            "purchaseOrdersArticlesDTOList": [
                {
                    "imei": self.imei,
                    "articlesRemake": "描述",
                    "purchasePrice": "100",
                    "logisticsNo": sf,
                    "warehouseId": 490,
                    "supplyType": 1,
                    "supplyTypeDesc": "A",
                    "purchaseArticlesInfoDTO": {
                        "brandId": 1,
                        "brandName": "苹果",
                        "modelId": 17569,
                        "modelName": "iPhone 16 Pro Max",
                        "articlesTypeId": 1,
                        "articlesTypeName": "手机",
                        "imei": self.imei,
                        "articlesRemake": "描述",
                        "purchasePrice": "100",
                        "romId": 41,
                        "romName": "256G",
                        "ramId": "",
                        "ramName": "",
                        "colorId": 1712,
                        "colorName": "黑色钛金属",
                        "num": "10",
                        "skuInfo": "苹果小型号:A3297;购买渠道:国行;颜色:黑色钛金属;ROM容量:256G;电池健康度:电池健康度100%;苹果保修情况:保修时长≥330天;商品来源:二手优品;成色:99新;",
                        "smallModelId": 1743,
                        "smallModelName": "A3297",
                        "buyChannelId": 16,
                        "buyChannelName": "国行",
                        "batteryHealthId": 23024,
                        "batteryHealthName": "电池健康度100%",
                        "warrantyDurationId": 23005,
                        "warrantyDurationName": "保修时长≥330天",
                        "machineTypeId": 862,
                        "machineTypeName": "二手优品",
                        "finenessId": 2,
                        "finenessName": "99新",
                        "id": time,
                        "_X_ROW_KEY": "row_43"
                    }
                },
                {
                    "imei": self.imei,
                    "articlesRemake": "描述",
                    "purchasePrice": "100",
                    "logisticsNo": sf,
                    "warehouseId": 490,
                    "supplyType": 1,
                    "supplyTypeDesc": "A",
                    "purchaseArticlesInfoDTO": {
                        "brandId": 1,
                        "brandName": "苹果",
                        "modelId": 17569,
                        "modelName": "iPhone 16 Pro Max",
                        "articlesTypeId": 1,
                        "articlesTypeName": "手机",
                        "imei": self.imei,
                        "articlesRemake": "描述",
                        "purchasePrice": "100",
                        "romId": 41,
                        "romName": "256G",
                        "ramId": "",
                        "ramName": "",
                        "colorId": 1712,
                        "colorName": "黑色钛金属",
                        "num": "10",
                        "skuInfo": "苹果小型号:A3297;购买渠道:国行;颜色:黑色钛金属;ROM容量:256G;电池健康度:电池健康度100%;苹果保修情况:保修时长≥330天;商品来源:二手优品;成色:99新;",
                        "smallModelId": 1743,
                        "smallModelName": "A3297",
                        "buyChannelId": 16,
                        "buyChannelName": "国行",
                        "batteryHealthId": 23024,
                        "batteryHealthName": "电池健康度100%",
                        "warrantyDurationId": 23005,
                        "warrantyDurationName": "保修时长≥330天",
                        "machineTypeId": 862,
                        "machineTypeName": "二手优品",
                        "finenessId": 2,
                        "finenessName": "99新",
                        "id": time,
                        "_X_ROW_KEY": "row_44"
                    }
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'km9X0jSmr', data, 'main', nocheck)

    @doc(UXWWtbpIHPQ9A7QMbtc9)
    @BaseApi.timing_decorator
    def UXWWtbpIHPQ9A7QMbtc9(self, nocheck=False):
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
                    "serialNo": self.mixed_random(),
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
                        "serialNo": self.mixed_random(),
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
        self.validate_request_data(data)
        return self._make_request('post', 'km9X0jSmr', data, 'main', nocheck)

    @doc(LTMkAl3mr9wdiYoATjak)
    @BaseApi.timing_decorator
    def LTMkAl3mr9wdiYoATjak(self, nocheck=False):
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
        self.validate_request_data(data)
        return self._make_request('post', 'km9X0jSmr', data, 'main', nocheck)

    @doc(N4CQUFEbAhA6O3SqB3ap)
    @BaseApi.timing_decorator
    def N4CQUFEbAhA6O3SqB3ap(self, nocheck=False):
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
                    "serialNo": self.mixed_random(),
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
                        "serialNo": self.mixed_random(),
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
        self.validate_request_data(data)
        return self._make_request('post', 'km9X0jSmr', data, 'main', nocheck)

    @doc(K2g9gJbSU76WxYKMFL1A)
    @BaseApi.timing_decorator
    def K2g9gJbSU76WxYKMFL1A(self, nocheck=False):
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
        self.validate_request_data(data)
        return self._make_request('post', 'km9X0jSmr', data, 'main', nocheck)


class GVdV4FYYC3(InitializeParams):
    """商品采购|采购管理|未发货订单列表"""

    @doc(uXCn7JV8wWVKBqpjkPz1)
    @BaseApi.timing_decorator
    def uXCn7JV8wWVKBqpjkPz1(self, nocheck=False):
        obj = self.pc.Y6hDdvp1tY9uk0H51cn91()
        ParamCache.cache_object({'i': obj[0]['purchaseNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "supplierId": INFO['main_supplier_id']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'NQuaSyCwg', data, 'main', nocheck)

    @doc(NApBGCWJXaD8TCr8oG0O)
    @BaseApi.timing_decorator
    def NApBGCWJXaD8TCr8oG0O(self, nocheck=False):
        obj = self.pc.Y6hDdvp1tY9uk0H51cn91()
        ParamCache.cache_object({'i': obj[0]['platformOrderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "platformOrderNo": obj[0]['platformOrderNo']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'NQuaSyCwg', data, 'main', nocheck)

    @doc(gEvHUJODc2blQ0T3B8vs)
    @BaseApi.timing_decorator
    def gEvHUJODc2blQ0T3B8vs(self, nocheck=False):
        obj = self.pc.Y6hDdvp1tY9uk0H51cn91()
        ParamCache.cache_object({'i': obj[0]['platformArticlesNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "platformArticlesNo": obj[0]['platformArticlesNo']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'NQuaSyCwg', data, 'main', nocheck)

    @doc(tg0itP0B1fKeUwbew3bL)
    @BaseApi.timing_decorator
    def tg0itP0B1fKeUwbew3bL(self, nocheck=False):
        obj = self.pc.Y6hDdvp1tY9uk0H51cn91()
        ParamCache.cache_object({'i': obj[0]['imei']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "imei": obj[0]['imei']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'NQuaSyCwg', data, 'main', nocheck)

    @doc(DntxwTAfuSnkVqrNwSV9)
    @BaseApi.timing_decorator
    def DntxwTAfuSnkVqrNwSV9(self, nocheck=False):
        obj = self.pc.Y6hDdvp1tY9uk0H51cn91()
        ParamCache.cache_object({'i': obj[0]['imei']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "dateFrom": self.get_the_date(),
            "dateTo": self.get_the_date(days=1),
        }
        self.validate_request_data(data)
        return self._make_request('post', 'NQuaSyCwg', data, 'main', nocheck)


class HMBSFfGhqc(InitializeParams):
    """商品采购|采购管理|到货通知单列表"""

    @doc(EY8ajeO8hDESQhWV9p4d)
    @BaseApi.timing_decorator
    def EY8ajeO8hDESQhWV9p4d(self, nocheck=False):
        obj = self.pc.THtT7YW545kAG73W2gHDj()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        data = {
            "stateList": [
                2,
                3
            ],
            "orderNo": obj[0]['orderNo'],
            "pageNum": 1,
            "pageSize": 10
        }
        self.validate_request_data(data)
        return self._make_request('post', 'LDvQ06cIg', data, 'main', nocheck)

    @doc(yUfJVOWNNm8e1oZ0AOli)
    @BaseApi.timing_decorator
    def yUfJVOWNNm8e1oZ0AOli(self, nocheck=False):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP()
        ParamCache.cache_object({'i': obj[0]['logisticsNoList'][0]})
        data = {
            "stateList": [
                2,
                3
            ],
            "logisticsNo": obj[0]['logisticsNoList'][0],
            "pageNum": 1,
            "pageSize": 10
        }
        self.validate_request_data(data)
        return self._make_request('post', 'LDvQ06cIg', data, 'main', nocheck)

    @doc(KbYnHWYarqIZt0JaCFuZ)
    @BaseApi.timing_decorator
    def KbYnHWYarqIZt0JaCFuZ(self, nocheck=False):
        obj = self.pc.THtT7YW545kAG73W2gHDj()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        data = {
            "stateList": [
                2,
                3
            ],
            "supplierId": INFO['main_supplier_id'],
            "pageNum": 1,
            "pageSize": 10
        }
        self.validate_request_data(data)
        return self._make_request('post', 'LDvQ06cIg', data, 'main', nocheck)

    @doc(W62QpkNGF7aGdL8UtHlh)
    @BaseApi.timing_decorator
    def W62QpkNGF7aGdL8UtHlh(self, nocheck=False):
        obj = self.pc.THtT7YW545kAG73W2gHDj()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        data = {
            "stateList": [
                2,
                3
            ],
            "creatTimeStart": self.get_the_date(),
            "creatTimeEnd": self.get_the_date(days=1),
            "pageNum": 1,
            "pageSize": 10
        }
        self.validate_request_data(data)
        return self._make_request('post', 'LDvQ06cIg', data, 'main', nocheck)


class N47ymrezM8(InitializeParams):
    """商品采购|采购售后管理|采购售后列表"""

    @doc(phfsqPqFesHVfgjiWNer)
    @BaseApi.timing_decorator
    def phfsqPqFesHVfgjiWNer(self, nocheck=False):
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=2)
        ParamCache.cache_object({"i": obj[0]['id']})
        data = {
            "ids": [
                obj[0]['id']
            ],
            "saleState": 1,
            "receiveState": 1,
            "purchaseDeliveryTime": self.get_formatted_datetime(),
            "payState": "2",
            "remark": "备注"
        }
        self.validate_request_data(data)
        return self._make_request('put', 'xGS6K1sGm', data, 'main', nocheck)

    @doc(jVgd53LQsvnwXfUXRRgq)
    @BaseApi.timing_decorator
    def jVgd53LQsvnwXfUXRRgq(self, nocheck=False):
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=2)
        ParamCache.cache_object({"i": obj[0]['id']})
        data = {
            "ids": [
                obj[0]['id']
            ],
            "saleState": 1,
            "receiveState": 1,
            "purchaseDeliveryTime": self.get_formatted_datetime(),
            "payState": "1",
            "accountNo": INFO['main_account_no'],
            "accountName": "系统默认账户",
            "remark": "备注"
        }
        self.validate_request_data(data)
        return self._make_request('put', 'xGS6K1sGm', data, 'main', nocheck)

    @doc(Z4SuqHs6Y2LaV2QZa5Ir)
    @BaseApi.timing_decorator
    def Z4SuqHs6Y2LaV2QZa5Ir(self, nocheck=False):
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=2)
        ParamCache.cache_object({"i": obj[0]['id']})
        data = {
            "ids": [
                obj[0]['id']
            ],
            "saleState": 2,
            "receiveState": 1,
            "purchaseDeliveryTime": self.get_formatted_datetime(),
            "remark": "备注",
            "logisticsNo": self.jd
        }
        self.validate_request_data(data)
        return self._make_request('put', 'xGS6K1sGm', data, 'main', nocheck)

    @doc(pHj61cDnzOd8FgCqMVW5)
    @BaseApi.timing_decorator
    def pHj61cDnzOd8FgCqMVW5(self, nocheck=False):
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=2)
        ParamCache.cache_object({"i": obj[0]['id']})
        data = {
            "ids": [
                obj[0]['id']
            ],
            "saleState": 2,
            "receiveState": 2,
            "purchaseDeliveryTime": self.get_formatted_datetime(),
            "warehouseId": INFO['main_item_in_warehouse_id']
        }
        self.validate_request_data(data)
        return self._make_request('put', 'xGS6K1sGm', data, 'main', nocheck)

    @doc(tTRW133mzbKPeCd8m40H)
    @BaseApi.timing_decorator
    def tTRW133mzbKPeCd8m40H(self, nocheck=False):
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=2)
        ParamCache.cache_object({"i": obj[0]['id']})
        imei = self.imei
        data = {
            "ids": [
                obj[0]['id'],
            ],
            "saleState": 3,
            "receiveState": 1,
            "purchaseDeliveryTime": self.get_formatted_datetime(),
            "remark": "备注",
            "logisticsNo": self.jd,
            "buildExchangeList": [
                {
                    "saleArticlesRelevanceId": obj[0]['id'],
                    "skuInfo": obj[0]['skuInfo'],
                    "purchaseArticlesInfoDTO": {
                        "articlesTypeId": 1,
                        "brandId": 1,
                        "modelId": 17569,
                        "imei": imei,
                        "purchasePrice": "299",
                        "articlesRemake": "",
                        "remark": "",
                        "sourcePurchasePrice": 200,
                        "modelName": "iPhone 16 Pro Max",
                        "colorId": 1712,
                        "colorName": "黑色钛金属",
                        "finenessId": 2,
                        "finenessName": "99新"
                    },
                    "imei": imei,
                    "purchasePrice": "299",
                    "articlesRemake": "",
                    "supplyType": 2,
                    "supplyTypeDesc": "C"
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('put', 'xGS6K1sGm', data, 'main', nocheck)

    @doc(J5gqPGgMCU66iUGcjVkX)
    @BaseApi.timing_decorator
    def J5gqPGgMCU66iUGcjVkX(self, nocheck=False):
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=2)
        ParamCache.cache_object({"i": obj[0]['id']})
        imei = self.imei
        data = {
            "ids": [
                obj[0]['id']
            ],
            "saleState": 3,
            "receiveState": 2,
            "purchaseDeliveryTime": self.get_formatted_datetime(),
            "remark": "备注",
            "warehouseId": INFO['main_item_warehouse_id'],
            "buildExchangeList": [
                {
                    "saleArticlesRelevanceId": obj[0]['id'],
                    "skuInfo": obj[0]['skuInfo'],
                    "purchaseArticlesInfoDTO": {
                        "articlesTypeId": 1,
                        "brandId": 1,
                        "modelId": 17569,
                        "imei": imei,
                        "purchasePrice": "828",
                        "articlesRemake": "",
                        "remark": "",
                        "sourcePurchasePrice": obj[0]['purchasePrice'],
                        "modelName": "iPhone 16 Pro Max",
                        "finenessId": 2,
                        "finenessName": "99新"
                    },
                    "imei": imei,
                    "purchasePrice": "828",
                    "articlesRemake": "",
                    "supplyType": 2,
                    "supplyTypeDesc": "C"
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('put', 'xGS6K1sGm', data, 'main', nocheck)

    @doc(Bht5FveIIJwsO1nzrSou)
    @BaseApi.timing_decorator
    def Bht5FveIIJwsO1nzrSou(self, nocheck=False):
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=1)
        ParamCache.cache_object({"i": obj[0]['imei']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "imei": obj[0]['imei'],
            "type": "1"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'y03duzqXb', data, 'main', nocheck)

    @doc(CfF5rsovr6q1eXvK89E3)
    @BaseApi.timing_decorator
    def CfF5rsovr6q1eXvK89E3(self, nocheck=False):
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=2)
        ParamCache.cache_object({"i": obj[0]['imei']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "imei": obj[0]['imei'],
            "type": "2"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'y03duzqXb', data, 'main', nocheck)

    @doc(k39WRkcNXmAaALC0Vslr)
    @BaseApi.timing_decorator
    def k39WRkcNXmAaALC0Vslr(self, nocheck=False):
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=1)
        ParamCache.cache_object({"i": obj[0]['imei']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "supplierId": ['main_supplier_id'],
            "type": "1"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'y03duzqXb', data, 'main', nocheck)

    @doc(NqFHiIZhsGNUUdvC6h2P)
    @BaseApi.timing_decorator
    def NqFHiIZhsGNUUdvC6h2P(self, nocheck=False):
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=2)
        ParamCache.cache_object({"i": obj[0]['imei']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "supplierId": ['main_supplier_id'],
            "type": "2"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'y03duzqXb', data, 'main', nocheck)

    @doc(WGIFhMXGjLDYNdHFNmZ6)
    @BaseApi.timing_decorator
    def WGIFhMXGjLDYNdHFNmZ6(self, nocheck=False):
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=1)
        ParamCache.cache_object({"i": obj[0]['platformArticlesNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "platformArticlesNo": obj[0]['platformArticlesNo'],
            "type": "1"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'y03duzqXb', data, 'main', nocheck)

    @doc(nwM5r4G3gxMKFkY7vCkS)
    @BaseApi.timing_decorator
    def nwM5r4G3gxMKFkY7vCkS(self, nocheck=False):
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=2)
        ParamCache.cache_object({"i": obj[0]['platformArticlesNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "platformArticlesNo": obj[0]['platformArticlesNo'],
            "type": "2"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'y03duzqXb', data, 'main', nocheck)

    @doc(SdxPSZvsxDBQFJmoq0sn)
    @BaseApi.timing_decorator
    def SdxPSZvsxDBQFJmoq0sn(self, nocheck=False):
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=1)
        ParamCache.cache_object({"i": obj[0]['billNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "saleNo": obj[0]['billNo'],
            "type": "1"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'y03duzqXb', data, 'main', nocheck)

    @doc(xKOkW569Bn2xL0RXmnEZ)
    @BaseApi.timing_decorator
    def xKOkW569Bn2xL0RXmnEZ(self, nocheck=False):
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=2)
        ParamCache.cache_object({"i": obj[0]['saleNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "saleNo": obj[0]['saleNo'],
            "type": "2"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'y03duzqXb', data, 'main', nocheck)

    @doc(XEQ3tAQnMxJ6mC5Z3zSu)
    @BaseApi.timing_decorator
    def XEQ3tAQnMxJ6mC5Z3zSu(self, nocheck=False):
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=1)
        ParamCache.cache_object({"i": obj[0]['billNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "type": "1",
            "erpStartTime": self.get_the_date(),
            "erpEndTime": self.get_the_date()
        }
        self.validate_request_data(data)
        return self._make_request('post', 'y03duzqXb', data, 'main', nocheck)

    @doc(PhchxOyoBh6ZBZxAR8B5)
    @BaseApi.timing_decorator
    def PhchxOyoBh6ZBZxAR8B5(self, nocheck=False):
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=2)
        ParamCache.cache_object({"i": obj[0]['saleNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "type": "2",
            "erpStartTime": self.get_the_date(),
            "erpEndTime": self.get_the_date()
        }
        self.validate_request_data(data)
        return self._make_request('post', 'y03duzqXb', data, 'main', nocheck)

    @doc(cJyOkQvyQsMExyu5Vt45)
    @BaseApi.timing_decorator
    def cJyOkQvyQsMExyu5Vt45(self, nocheck=False):
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=1)
        ParamCache.cache_object({"i": obj[0]['logisticsNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "type": "1",
            "warehouseLogisticsOrderNo": obj[0]['logisticsNo']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'y03duzqXb', data, 'main', nocheck)

    @doc(y4THlC3ekhRh4iae3DtD)
    @BaseApi.timing_decorator
    def y4THlC3ekhRh4iae3DtD(self, nocheck=False):
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=2)
        ParamCache.cache_object({"i": obj[0]['logisticsNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "type": "2",
            "warehouseLogisticsOrderNo": obj[0]['logisticsNo']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'y03duzqXb', data, 'main', nocheck)

    @doc(dhBbO6TlYXaCCyMti4Sf)
    @BaseApi.timing_decorator
    def dhBbO6TlYXaCCyMti4Sf(self, nocheck=False, status=None):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "type": "2",
            "saleState": status
        }
        self.validate_request_data(data)
        return self._make_request('post', 'y03duzqXb', data, 'main', nocheck)


class WdU75jpBUw(InitializeParams):
    """商品采购|采购售后管理|待售后列表"""

    @doc(iWItsJtwj5CLc0GYimGA)
    @BaseApi.timing_decorator
    def iWItsJtwj5CLc0GYimGA(self, nocheck=False):
        obj = self.pc.XHVW0IhQgPnb63fnaqTdN()
        ParamCache.cache_object({"i": obj[1]['articlesNo']})
        data = {
            "payState": "2",
            "purchaseArticlesSaleInfoList": [
                {
                    "saleState": "7",
                    "articlesNo": obj[0]['articlesNo'],
                    "newPurchasePrice": 20,
                    "supplierName": INFO['main_supplier_name'],
                    "supplierId": INFO['main_supplier_id']
                },
                {
                    "saleState": "7",
                    "articlesNo": obj[1]['articlesNo'],
                    "newPurchasePrice": 20,
                    "supplierName": INFO['main_supplier_name'],
                    "supplierId": INFO['main_supplier_id']
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'MgU31VbHk', data, 'main', nocheck)

    @doc(Zd7znz6pdWwciZ4zhv18)
    @BaseApi.timing_decorator
    def Zd7znz6pdWwciZ4zhv18(self, nocheck=False):
        obj = self.pc.XHVW0IhQgPnb63fnaqTdN()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "payState": "2",
            "purchaseArticlesSaleInfoList": [
                {
                    "saleState": "7",
                    "articlesNo": obj[0]['articlesNo'],
                    "newPurchasePrice": 20,
                    "supplierName": INFO['main_supplier_name'],
                    "supplierId": INFO['main_supplier_id']
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'MgU31VbHk', data, 'main', nocheck)

    @doc(Mlllk8zWuMbryTvo07YA)
    @BaseApi.timing_decorator
    def Mlllk8zWuMbryTvo07YA(self, nocheck=False):
        obj = self.pc.XHVW0IhQgPnb63fnaqTdN()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "payState": "1",
            "accountNo": INFO['main_account_no'],
            "accountName": INFO['main_account_name'],
            "purchaseArticlesSaleInfoList": [
                {
                    "saleState": "7",
                    "articlesNo": obj[0]['articlesNo'],
                    "newPurchasePrice": 50,
                    "supplierName": INFO['main_supplier_name'],
                    "supplierId": INFO['main_supplier_id']
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'MgU31VbHk', data, 'main', nocheck)

    @doc(mtmZ9ns5g8nanblESlTR)
    @BaseApi.timing_decorator
    def mtmZ9ns5g8nanblESlTR(self, nocheck=False):
        obj = self.pc.XHVW0IhQgPnb63fnaqTdN()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "saleState": 5,
            "offExpressage": "0",
            "logisticsNoPrice": 11,
            "logisticsOrder": self.jd,
            "supplierName": INFO['main_supplier_name'],
            "supplierId": INFO['main_supplier_id'],
            "purchaseOrdersArticlesDTOList": [
                {
                    "purchaseNo": obj[0]['purchaseNo'],
                    "articlesNo": obj[0]['articlesNo'],
                    "id": obj[0]['id'],
                    "purchasePrice": 10,
                    "saleRemake": "备注"
                }
            ],
            "deliveryTime": self.get_formatted_datetime(),
            "purchaseOrdersSaleInfoDTO": {
                "ids": [
                    obj[0]['id']
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
        self.validate_request_data(data)
        return self._make_request('post', 'TDNsMZDYJ', data, 'main', nocheck)

    @doc(gXtFuS2Icw1FTTfLvWC0)
    @BaseApi.timing_decorator
    def gXtFuS2Icw1FTTfLvWC0(self, nocheck=False):
        obj = self.pc.XHVW0IhQgPnb63fnaqTdN()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "saleState": 5,
            "offExpressage": "1",
            "logisticsNoPrice": 10,
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "purchaseOrdersArticlesDTOList": [
                {
                    "purchaseNo": obj[0]['purchaseNo'],
                    "articlesNo": obj[0]['articlesNo'],
                    "id": obj[0]['id'],
                    "purchasePrice": 10,
                    "saleRemake": "备注"
                }
            ],
            "deliveryTime": self.get_formatted_datetime(),
            "walletAccountNo": INFO['main_wallet_account_no'],
            "payWay": 2,
            "pickUpType": 1,
            "logisticsCompanyType": 1,
            "userAddressId": 559,
            "purchaseOrdersSaleInfoDTO": {
                "ids": [
                    obj[0]['id']
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
        self.validate_request_data(data)
        return self._make_request('post', 'TDNsMZDYJ', data, 'main', nocheck)

    @doc(nFSWCuNM4gli2yRB2dwD)
    @BaseApi.timing_decorator
    def nFSWCuNM4gli2yRB2dwD(self, nocheck=False):
        obj = self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2, j=3)
        data = {
            "queryNo": obj[0]['articlesNo']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'RoVc0CTIT', data, 'main', nocheck)

    @doc(uq01dOZeO9ByThGMfj4w)
    @BaseApi.timing_decorator
    def uq01dOZeO9ByThGMfj4w(self, nocheck=False):
        obj = self.pc.XHVW0IhQgPnb63fnaqTdN()
        ParamCache.cache_object({"i": obj[1]['articlesNo']})
        data = {
            "saleState": 5,
            "offExpressage": "0",
            "logisticsNoPrice": 11,
            "logisticsOrder": self.jd,
            "supplierName": INFO['main_supplier_name'],
            "supplierId": INFO['main_supplier_id'],
            "purchaseOrdersArticlesDTOList": [
                {
                    "purchaseNo": obj[0]['purchaseNo'],
                    "articlesNo": obj[0]['articlesNo'],
                    "id": obj[0]['id'],
                    "purchasePrice": 10,
                    "saleRemake": "备注"
                },
                {
                    "purchaseNo": obj[1]['purchaseNo'],
                    "articlesNo": obj[1]['articlesNo'],
                    "id": obj[1]['id'],
                    "purchasePrice": 10,
                    "saleRemake": "备注"
                }
            ],
            "deliveryTime": self.get_formatted_datetime(),
            "purchaseOrdersSaleInfoDTO": {
                "ids": [
                    obj[0]['id'],
                    obj[1]['id']
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
        self.validate_request_data(data)
        return self._make_request('post', 'TDNsMZDYJ', data, 'main', nocheck)

    @doc(EXJN6Kfs99I6kkD0lNX2)
    @BaseApi.timing_decorator
    def EXJN6Kfs99I6kkD0lNX2(self, nocheck=False):
        obj = self.pc.XHVW0IhQgPnb63fnaqTdN()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "saleState": 5,
            "offExpressage": "0",
            "logisticsNoPrice": 11,
            "logisticsOrder": self.jd,
            "supplierName": INFO['main_supplier_name'],
            "supplierId": INFO['main_supplier_id'],
            "purchaseOrdersArticlesDTOList": [
                {
                    "purchaseNo": obj[0]['purchaseNo'],
                    "articlesNo": obj[0]['articlesNo'],
                    "id": obj[0]['id'],
                    "purchasePrice": 10,
                    "saleRemake": "备注"
                }
            ],
            "deliveryTime": self.get_formatted_datetime(),
            "purchaseOrdersSaleInfoDTO": {
                "ids": [
                    obj[0]['id']
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
        self.validate_request_data(data)
        return self._make_request('post', 'TDNsMZDYJ', data, 'main', nocheck)

    @doc(r3no6VL2SjqT3qCMSXsF)
    @BaseApi.timing_decorator
    def r3no6VL2SjqT3qCMSXsF(self, nocheck=False):
        obj = self.pc.XHVW0IhQgPnb63fnaqTdN()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "saleState": 5,
            "offExpressage": "0",
            "logisticsNoPrice": 0,
            "supplierName": INFO['main_supplier_name'],
            "supplierId": INFO['main_supplier_id'],
            "purchaseOrdersArticlesDTOList": [
                {
                    "purchaseNo": obj[0]['purchaseNo'],
                    "articlesNo": obj[0]['articlesNo'],
                    "id": obj[0]['id'],
                    "purchasePrice": 10,
                    "saleRemake": "备注"
                }
            ],
            "deliveryTime": self.get_formatted_datetime(),
            "purchaseOrdersSaleInfoDTO": {
                "ids": [
                    obj[0]['id']
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
        self.validate_request_data(data)
        return self._make_request('post', 'TDNsMZDYJ', data, 'main', nocheck)

    @doc(WCIspC62VSOcHhuvk6oH)
    @BaseApi.timing_decorator
    def WCIspC62VSOcHhuvk6oH(self, nocheck=False):
        obj = self.pc.XHVW0IhQgPnb63fnaqTdN()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "saleState": 5,
            "offExpressage": "0",
            "logisticsNoPrice": 0,
            "supplierName": INFO['main_supplier_name'],
            "supplierId": INFO['main_supplier_id'],
            "purchaseOrdersArticlesDTOList": [
                {
                    "purchaseNo": obj[0]['purchaseNo'],
                    "articlesNo": obj[0]['articlesNo'],
                    "id": obj[0]['id'],
                    "purchasePrice": 10,
                    "saleRemake": "备注"
                }
            ],
            "deliveryTime": self.get_formatted_datetime(),
            "purchaseOrdersSaleInfoDTO": {
                "ids": [
                    obj[0]['id']
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
        self.validate_request_data(data)
        return self._make_request('post', 'TDNsMZDYJ', data, 'main', nocheck)

    @doc(bRT8qBZ1qzcsOegIVUiL)
    @BaseApi.timing_decorator
    def bRT8qBZ1qzcsOegIVUiL(self, nocheck=False):
        obj = self.pc.XHVW0IhQgPnb63fnaqTdN()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "saleState": 5,
            "offExpressage": "0",
            "logisticsNoPrice": 0,
            "supplierName": INFO['main_supplier_name'],
            "supplierId": INFO['main_supplier_id'],
            "purchaseOrdersArticlesDTOList": [
                {
                    "purchaseNo": obj[0]['purchaseNo'],
                    "articlesNo": obj[0]['articlesNo'],
                    "id": obj[0]['id'],
                    "purchasePrice": 10,
                    "saleRemake": "备注"
                }
            ],
            "deliveryTime": self.get_formatted_datetime(),
            "purchaseOrdersSaleInfoDTO": {
                "ids": [
                    obj[0]['id']
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
        self.validate_request_data(data)
        return self._make_request('post', 'TDNsMZDYJ', data, 'main', nocheck)

    @doc(p2NxayPBZqnmytlhtjEy)
    @BaseApi.timing_decorator
    def p2NxayPBZqnmytlhtjEy(self, nocheck=False):
        obj = self.pc.XHVW0IhQgPnb63fnaqTdN()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
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
                    "purchaseNo": obj[0]['purchaseNo'],
                    "articlesNo": obj[0]['articlesNo'],
                    "id": obj[0]['id'],
                    "purchasePrice": obj[0]['purchasePrice'],
                    "saleRemake": "备注"
                }
            ],
            "deliveryTime": self.get_formatted_datetime(),
            "purchaseOrdersSaleInfoDTO": {
                "ids": [
                    obj[0]['id']
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
                        "saleArticlesRelevanceId": obj[0]['id'],
                        "skuInfo": obj[0]['skuInfo'],
                        "purchaseArticlesInfoDTO": {
                            "articlesTypeId": 1,
                            "brandId": obj[0]['brandId'],
                            "modelId": obj[0]['modelId'],
                            "imei": imei,
                            "purchasePrice": "100",
                            "articlesRemake": "",
                            "remark": "",
                            "sourcePurchasePrice": obj[0]['purchasePrice'],
                            "modelName": obj[0]['modelName'],
                        },
                        "imei": imei,
                        "purchasePrice": "100",
                        "articlesRemake": ""
                    }
                ]
            }
        }
        self.validate_request_data(data)
        return self._make_request('post', 'TDNsMZDYJ', data, 'main', nocheck)

    @doc(HR074UMjBJ9KgEckp0hD)
    @BaseApi.timing_decorator
    def HR074UMjBJ9KgEckp0hD(self, nocheck=False):
        obj = self.pc.XHVW0IhQgPnb63fnaqTdN()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        imei = self.imei
        data = {
            "saleState": 5,
            "offExpressage": "0",
            "logisticsNoPrice": 0,
            "supplierName": INFO['main_supplier_name'],
            "supplierId": INFO['main_supplier_id'],
            "purchaseOrdersArticlesDTOList": [
                {
                    "purchaseNo": obj[0]['purchaseNo'],
                    "articlesNo": obj[0]['articlesNo'],
                    "id": obj[0]['id'],
                    "purchasePrice": obj[0]['purchasePrice'],
                    "saleRemake": "备注"
                }
            ],
            "deliveryTime": self.get_formatted_datetime(),
            "purchaseOrdersSaleInfoDTO": {
                "ids": [
                    obj[0]['id']
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
                        "saleArticlesRelevanceId": obj[0]['id'],
                        "skuInfo": obj[0]['skuInfo'],
                        "purchaseArticlesInfoDTO": {
                            "articlesTypeId": 1,
                            "brandId": obj[0]['brandId'],
                            "modelId": obj[0]['modelId'],
                            "imei": imei,
                            "purchasePrice": "100",
                            "articlesRemake": "",
                            "remark": "",
                            "sourcePurchasePrice": obj[0]['purchasePrice'],
                            "modelName": obj[0]['modelName'],
                        },
                        "imei": imei,
                        "purchasePrice": "100",
                        "articlesRemake": ""
                    }
                ]
            }
        }
        self.validate_request_data(data)
        return self._make_request('post', 'TDNsMZDYJ', data, 'main', nocheck)

    @doc(AObSRgmEGYVIgbuCw6h4)
    @BaseApi.timing_decorator
    def AObSRgmEGYVIgbuCw6h4(self, nocheck=False):
        obj = self.pc.XHVW0IhQgPnb63fnaqTdN()
        data = {
            "remark": "备注",
            "articlesNo": obj[0]['articlesNo']
        }
        self.validate_request_data(data)
        return self._make_request('put', 'BegcMvuP1', data, 'main', nocheck)


class LZnv9DokCX(InitializeParams):
    """商品采购|采购售后管理|待接收物品"""

    @doc(kDYL6B67bVRYqDohXGBm)
    @BaseApi.timing_decorator
    def kDYL6B67bVRYqDohXGBm(self, nocheck=False):
        obj = self.pc.Rwpqef340gYUd4Hgkbq8l()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "articlesNoList": [
                obj[0]['articlesNo']
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'WpZgDxZLH', data, 'main', nocheck)

    @doc(gXbPXTa8tODEWzcuCWKK)
    @BaseApi.timing_decorator
    def gXbPXTa8tODEWzcuCWKK(self, nocheck=False):
        obj = self.pc.Rwpqef340gYUd4Hgkbq8l()
        ParamCache.cache_object({"i": obj[0]['imei']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesNo": obj[0]['imei'],
            "articlesState": 10,
            "articlesType": 1
        }
        self.validate_request_data(data)
        return self._make_request('post', 'BbtJmNsWL', data, 'main', nocheck)

    @doc(GK9UcuLcY440l6QirME6)
    @BaseApi.timing_decorator
    def GK9UcuLcY440l6QirME6(self, nocheck=False):
        obj = self.pc.Rwpqef340gYUd4Hgkbq8l()
        ParamCache.cache_object({"i": obj[0]['imei']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesState": 10,
            "erpStartTime": self.get_the_date(),
            "erpEndTime": self.get_the_date(),
            "articlesType": 1
        }
        self.validate_request_data(data)
        return self._make_request('post', 'BbtJmNsWL', data, 'main', nocheck)


class G4EaCouJoJ(InitializeParams):
    """商品采购|采购管理|采购订单列表"""

    @doc(V3OaBTTJgYrJQyoMmypY)
    @BaseApi.timing_decorator
    def V3OaBTTJgYrJQyoMmypY(self, nocheck=False):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP()
        ParamCache.cache_object({"i": obj[0]['articlesNoList'][0]})
        data = {
            "articlesNo": obj[0]['articlesNoList'][0],
            "remark": "备注"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'R7HA7rwAV', data, 'main', nocheck)

    @doc(FxIuRXAgm25KpkG1vYdL)
    @BaseApi.timing_decorator
    def FxIuRXAgm25KpkG1vYdL(self, nocheck=False):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP()
        ParamCache.cache_object({"i": obj[0]['articlesNoList'][0]})
        data = {
            "logisticsNo": self.jd,
            "purchaseOrdersArticlesDTOList": [
                {
                    "purchaseNo": obj[0]['orderNo'],
                    "articlesNo": obj[0]['articlesNoList'][0],
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'iUOg847fP', data, 'main', nocheck)

    @doc(X9AzyILbQOMXUGnTTHIW)
    @BaseApi.timing_decorator
    def X9AzyILbQOMXUGnTTHIW(self, nocheck=False):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP()
        ParamCache.cache_object({"i": obj[0]['articlesNoList'][0]})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesNoOrImei": obj[0]['articlesNoList'][0],
            "articlesType": 1
        }
        self.validate_request_data(data)
        return self._make_request('post', 'k90OkSeBm', data, 'main', nocheck)

    @doc(UBQunveHStNfKk7VC1MY)
    @BaseApi.timing_decorator
    def UBQunveHStNfKk7VC1MY(self, nocheck=False):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "orderNo": obj[0]['orderNo'],
            "articlesType": 1
        }
        self.validate_request_data(data)
        return self._make_request('post', 'k90OkSeBm', data, 'main', nocheck)

    @doc(CIlgrf4csxjqTWz7KBW8)
    @BaseApi.timing_decorator
    def CIlgrf4csxjqTWz7KBW8(self, nocheck=False):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "supplierId": INFO['main_supplier_id'],
            "articlesType": 1
        }
        self.validate_request_data(data)
        return self._make_request('post', 'k90OkSeBm', data, 'main', nocheck)

    @doc(SEQRfhZPQLSks8OIHSUp)
    @BaseApi.timing_decorator
    def SEQRfhZPQLSks8OIHSUp(self, nocheck=False, status=None):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "state": status,
            "articlesType": 1
        }
        self.validate_request_data(data)
        return self._make_request('post', 'k90OkSeBm', data, 'main', nocheck)

    @doc(RHW76Y60nHIiwxzfeZNR)
    @BaseApi.timing_decorator
    def RHW76Y60nHIiwxzfeZNR(self, nocheck=False):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP()
        ParamCache.cache_object({"i": obj[0]['logisticsNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "logisticsNo": obj[0]['logisticsNo'],
            "articlesType": 1
        }
        self.validate_request_data(data)
        return self._make_request('post', 'k90OkSeBm', data, 'main', nocheck)

    @doc(ZQ8ruPTDvW7q2hXTRV77)
    @BaseApi.timing_decorator
    def ZQ8ruPTDvW7q2hXTRV77(self, nocheck=False, status=None):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "payState": status,
            "articlesType": 1
        }
        self.validate_request_data(data)
        return self._make_request('post', 'k90OkSeBm', data, 'main', nocheck)

    @doc(gwoujeJsaB3onqINz3vL)
    @BaseApi.timing_decorator
    def gwoujeJsaB3onqINz3vL(self, nocheck=False):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesType": 1,
            "erpStartTime": self.get_the_date(),
            "erpEndTime": self.get_the_date()
        }
        self.validate_request_data(data)
        return self._make_request('post', 'k90OkSeBm', data, 'main', nocheck)

    @doc(JB7S4POKRpjesx1Q32J0)
    @BaseApi.timing_decorator
    def JB7S4POKRpjesx1Q32J0(self, nocheck=False):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesType": 1,
            "userId": INFO['main_user_id'],
        }
        self.validate_request_data(data)
        return self._make_request('post', 'k90OkSeBm', data, 'main', nocheck)

    @doc(FysimTUmjHi3FisKVbsM)
    @BaseApi.timing_decorator
    def FysimTUmjHi3FisKVbsM(self, nocheck=False):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP()
        obj_2 = self.pc.Z6BEKs3GvdIWf6a1Dj2uP(data='a')
        ParamCache.cache_object({"i": obj_2[0]['platformArticlesNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "purchaseNo": obj[0]['orderNo'],
            "platformArticlesNo": obj_2[0]['platformArticlesNo']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'k90OkSeBm', data, 'main', nocheck)

    @doc(KjmhjLfM7YrFQNE6NiZG)
    @BaseApi.timing_decorator
    def KjmhjLfM7YrFQNE6NiZG(self, nocheck=False):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP(data='a')
        ParamCache.cache_object({"i": obj[0]['imei']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "purchaseNo": obj[0]['orderNo'],
            "articlesNoOrImei": obj[0]['imei']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'k90OkSeBm', data, 'main', nocheck)

    @doc(D1M3VTxNoTROnlErwIkd)
    @BaseApi.timing_decorator
    def D1M3VTxNoTROnlErwIkd(self, nocheck=False):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP(data='a')
        ParamCache.cache_object({"i": obj[0]['platformOrderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "purchaseNo": obj[0]['orderNo'],
            "platformOrderNo": obj[0]['platformOrderNo']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'k90OkSeBm', data, 'main', nocheck)

    @doc(Nu2xob41mVQX0Uwyv77c)
    @BaseApi.timing_decorator
    def Nu2xob41mVQX0Uwyv77c(self, nocheck=False):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP()
        obj_2 = self.pc.Z6BEKs3GvdIWf6a1Dj2uP(data='a')
        ParamCache.cache_object({"i": obj_2[0]['serialNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "purchaseNo": obj[0]['orderNo'],
            "serialNo": obj_2[0]['serialNo']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'k90OkSeBm', data, 'main', nocheck)


class FYDICk4EbP(InitializeParams):
    """商品采购|供应商管理"""

    @doc(h0V1zMfjLKSd4odY9NU2)
    @BaseApi.timing_decorator
    def h0V1zMfjLKSd4odY9NU2(self, nocheck=False):
        data = {
            "supplierName": '供应商' + self.serial,
            "phone": self.phone,
            "accountNo": INFO['idle_account_sno'],
            "level": 1,
            "provinceName": "北京",
            "provinceId": 1100,
            "cityName": "北京市",
            "cityId": 11010,
            "countyName": "崇文区",
            "countyId": 1105,
            "address": "爱心路" + self.serial,
            "userId": 953,
            "supplierType": 1,
            "defaultStatus": 0,
            "supplyType": 1,
            "type": 2,
            "supplyTypeDesc": "A"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'Gw9nFt0kw', data, 'idle', nocheck)

    @doc(VUZzvXlURvWP4b43uTRg)
    @BaseApi.timing_decorator
    def VUZzvXlURvWP4b43uTRg(self, nocheck=False):
        data = {
            "supplierName": '供应商' + self.serial,
            "phone": self.phone,
            "accountNo": INFO['idle_account_sno'],
            "level": 1,
            "provinceName": "北京",
            "provinceId": 1100,
            "cityName": "北京市",
            "cityId": 11010,
            "countyName": "崇文区",
            "countyId": 1105,
            "address": "爱心路" + self.serial,
            "userId": 953,
            "supplierType": 2,
            "defaultStatus": 1,
            "supplyType": 1,
            "type": 2,
            "supplyTypeDesc": "A"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'Gw9nFt0kw', data, 'idle', nocheck)

    @doc(ZwXnGe8s67ZogrbVkpxf)
    @BaseApi.timing_decorator
    def ZwXnGe8s67ZogrbVkpxf(self, nocheck=False):
        obj = self.pc.UCpwX0dlRXRmKVzfDX5dd()
        data = {
            "createTime": obj[0]['createTime'],
            "updateBy": obj[0]['updateBy'],
            "updateTime": self.get_formatted_datetime(),
            "pageSize": 10,
            "pageNum": 1,
            "orderByColumn": "create_time",
            "isAsc": obj[0]['isAsc'],
            "id": obj[0]['id'],
            "supplierName": '供应商' + self.serial,
            "phone": self.phone,
            "accountNo": INFO['idle_account_sno'],
            "level": 0,
            "provinceId": 2900,
            "provinceName": "广东",
            "cityId": 29020,
            "cityName": "广州市",
            "countyId": 54386,
            "countyName": "黄埔区",
            "address": "开创大道2565号生生广场",
            "userId": INFO['idle_user_id'],
            "tenantId": obj[0]['tenantId'],
            "isInit": 1,
            "isDelete": 0,
            "supplierType": 1,
            "defaultStatus": 0,
            "type": 2,
            "businessType": 1,
            "supplyType": 2,
            "supplyTypeDesc": "C"
        }
        self.validate_request_data(data)
        return self._make_request('put', 'qYK5c6Rpi', data, 'idle', nocheck)

    @doc(AO2AZxYBELIUmcGqLQlG)
    @BaseApi.timing_decorator
    def AO2AZxYBELIUmcGqLQlG(self, nocheck=False):
        data = {
            "supplierName": INFO['main_supplier_name'],
            "type": 2,
            "pageNum": 1,
            "pageSize": 10
        }
        self.validate_request_data(data)
        return self._make_request('post', 'jj0Esnp8n', data, 'idle', nocheck)


class EE20RTANF9(InitializeParams):
    """商品采购|采购管理|采购工单"""

    @doc(rfP03M51AR6P1V5a2zV9)
    @BaseApi.timing_decorator
    def rfP03M51AR6P1V5a2zV9(self, nocheck=False):
        obj = self.pc.WziJGBshZjou10L8PleRe()
        obj_2 = self.pc.WziJGBshZjou10L8PleRe(data='a', i='工序')
        data = {
            "workNum": 1,
            "workStartTime": self.get_formatted_datetime(),
            "workEndTime": self.get_formatted_datetime(days=1),
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "processList": [
                {
                    "processId": obj_2[0]['id'],
                    "processNum": 1,
                    "callType": 1,
                    "processStartTime": self.get_formatted_datetime(),
                    "processEndTime": self.get_formatted_datetime(days=1),
                    "processUserIdList": [
                        INFO['main_user_id']
                    ],
                    "defectIdList": [
                        obj[0]['id'],
                        obj[1]['id']
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
        self.validate_request_data(data)
        return self._make_request('post', 'IMz1mtWm1', data, 'main', nocheck)

    @doc(plgZg761v9pgtz1l53NY)
    @BaseApi.timing_decorator
    def plgZg761v9pgtz1l53NY(self, nocheck=False):
        obj = self.pc.WziJGBshZjou10L8PleRe()
        obj_2 = self.pc.WziJGBshZjou10L8PleRe(data='a', i='工序')
        data = {
            "workNum": 1,
            "workStartTime": self.get_formatted_datetime(),
            "workEndTime": self.get_formatted_datetime(days=1),
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "processList": [
                {
                    "processId": obj_2[0]['id'],
                    "processNum": 1,
                    "callType": 2,
                    "processStartTime": self.get_formatted_datetime(),
                    "processEndTime": self.get_formatted_datetime(days=1),
                    "processUserIdList": [
                        INFO['main_user_id']
                    ],
                    "defectIdList": [
                        obj[0]['id'],
                        obj[1]['id']
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
        self.validate_request_data(data)
        return self._make_request('post', 'IMz1mtWm1', data, 'main', nocheck)

    @doc(H7QZrgxeJPrgyVASQvUy)
    @BaseApi.timing_decorator
    def H7QZrgxeJPrgyVASQvUy(self, nocheck=False):
        obj = self.pc.WziJGBshZjou10L8PleRe()
        obj_2 = self.pc.WziJGBshZjou10L8PleRe(data='a', i='工序')
        obj_3 = self.pc.WziJGBshZjou10L8PleRe(data='a', i='报价')
        obj_4 = self.pc.WmKG9OkI9OlJlOENUzgNu()
        ParamCache.cache_object({'i': obj_4[0]['orderNo']})
        data = {
            "id": obj_4[0]['id'],
            "workNum": 1,
            "workStartTime": self.get_formatted_datetime(),
            "workEndTime": self.get_formatted_datetime(days=1),
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "processList": [
                {
                    "processId": obj_2[0]['id'],
                    "processNum": 1,
                    "callType": 1,
                    "processStartTime": self.get_formatted_datetime(),
                    "processEndTime": self.get_formatted_datetime(days=1),
                    "processUserIdList": [
                        INFO['main_user_id']
                    ],
                    "defectIdList": [
                        obj[0]['id'],
                        obj[1]['id']
                    ],
                    "remark": None,
                    "id": obj_4[0]['taskProgressList'][0]['id'],
                    "sort": 1
                },
                {
                    "processId": obj_3[0]['id'],
                    "processNum": "",
                    "callType": 2,
                    "processStartTime": self.get_formatted_datetime(),
                    "processEndTime": self.get_formatted_datetime(days=1),
                    "processUserIdList": [
                        INFO['main_user_id']
                    ],
                    "defectIdList": [
                        obj[0]['id'],
                        obj[1]['id']
                    ],
                    "remark": None,
                    "id": None,
                    "sort": 2
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('put', 'Evx1QWKUp', data, 'main', nocheck)

    @doc(hsFfIhIFCLXHb4x2J1CC)
    @BaseApi.timing_decorator
    def hsFfIhIFCLXHb4x2J1CC(self, nocheck=False):
        obj = self.pc.WziJGBshZjou10L8PleRe()
        obj_2 = self.pc.WziJGBshZjou10L8PleRe(data='a', i='工序')
        obj_3 = self.pc.WziJGBshZjou10L8PleRe(data='a', i='报价')
        obj_4 = self.pc.WmKG9OkI9OlJlOENUzgNu()
        obj_5 = self.pc.WziJGBshZjou10L8PleRe(data='a', i='退货')
        ParamCache.cache_object({'i': obj_4[0]['orderNo']})
        data = {
            "id": obj_4[0]['id'],
            "workNum": 1,
            "workStartTime": self.get_formatted_datetime(),
            "workEndTime": self.get_formatted_datetime(days=1),
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "processList": [
                {
                    "processId": obj_2[0]['id'],
                    "processNum": 1,
                    "callType": 1,
                    "processStartTime": self.get_formatted_datetime(),
                    "processEndTime": self.get_formatted_datetime(days=1),
                    "processUserIdList": [
                        INFO['main_user_id']
                    ],
                    "defectIdList": [
                        obj[0]['id'],
                        obj[1]['id']
                    ],
                    "remark": None,
                    "id": obj_4[0]['taskProgressList'][0]['id'],
                    "sort": 1
                },
                {
                    "processId": obj_3[0]['id'],
                    "processNum": "",
                    "callType": 2,
                    "processStartTime": self.get_formatted_datetime(),
                    "processEndTime": self.get_formatted_datetime(days=1),
                    "processUserIdList": [
                        INFO['main_user_id']
                    ],
                    "defectIdList": [
                        obj[0]['id'],
                        obj[1]['id']
                    ],
                    "remark": None,
                    "id": obj_4[0]['taskProgressList'][1]['id'],
                    "sort": 2
                },
                {
                    "processId": obj_5[0]['id'],
                    "processNum": "",
                    "callType": 2,
                    "processStartTime": self.get_formatted_datetime(),
                    "processEndTime": self.get_formatted_datetime(days=1),
                    "processUserIdList": [
                        INFO['main_user_id']
                    ],
                    "defectIdList": [
                        obj[0]['id'],
                        obj[1]['id']
                    ],
                    "remark": None,
                    "id": None,
                    "sort": 3
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('put', 'Evx1QWKUp', data, 'main', nocheck)

    @doc(LrMhNar9BE7bRoEWOGFt)
    @BaseApi.timing_decorator
    def LrMhNar9BE7bRoEWOGFt(self, nocheck=False):
        obj = self.pc.WziJGBshZjou10L8PleRe()
        obj_2 = self.pc.WziJGBshZjou10L8PleRe(data='a', i='工序')
        obj_3 = self.pc.WziJGBshZjou10L8PleRe(data='a', i='报价')
        obj_4 = self.pc.WmKG9OkI9OlJlOENUzgNu()
        obj_5 = self.pc.WziJGBshZjou10L8PleRe(data='a', i='退货')
        obj_6 = self.pc.WziJGBshZjou10L8PleRe(data='a', i='付款')
        ParamCache.cache_object({'i': obj_4[0]['orderNo']})
        data = {
            "id": obj_4[0]['id'],
            "workNum": 1,
            "workStartTime": self.get_formatted_datetime(),
            "workEndTime": self.get_formatted_datetime(days=1),
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "processList": [
                {
                    "processId": obj_2[0]['id'],
                    "processNum": 1,
                    "callType": 1,
                    "processStartTime": self.get_formatted_datetime(),
                    "processEndTime": self.get_formatted_datetime(days=1),
                    "processUserIdList": [
                        INFO['main_user_id']
                    ],
                    "defectIdList": [
                        obj[0]['id'],
                        obj[1]['id']
                    ],
                    "remark": None,
                    "id": obj_4[0]['taskProgressList'][0]['id'],
                    "sort": 1
                },
                {
                    "processId": obj_3[0]['id'],
                    "processNum": "",
                    "callType": 2,
                    "processStartTime": self.get_formatted_datetime(),
                    "processEndTime": self.get_formatted_datetime(days=1),
                    "processUserIdList": [
                        INFO['main_user_id']
                    ],
                    "defectIdList": [
                        obj[0]['id'],
                        obj[1]['id']
                    ],
                    "remark": None,
                    "id": obj_4[0]['taskProgressList'][1]['id'],
                    "sort": 2
                },
                {
                    "processId": obj_5[0]['id'],
                    "processNum": "",
                    "callType": 2,
                    "processStartTime": self.get_formatted_datetime(),
                    "processEndTime": self.get_formatted_datetime(days=1),
                    "processUserIdList": [
                        INFO['main_user_id']
                    ],
                    "defectIdList": [
                        obj[0]['id'],
                        obj[1]['id']
                    ],
                    "remark": None,
                    "id": obj_4[0]['taskProgressList'][2]['id'],
                    "sort": 3
                },
                {
                    "processId": obj_6[0]['id'],
                    "processNum": "",
                    "callType": 2,
                    "processStartTime": self.get_formatted_datetime(),
                    "processEndTime": self.get_formatted_datetime(days=1),
                    "processUserIdList": [
                        INFO['main_user_id']
                    ],
                    "defectIdList": [
                        obj[0]['id'],
                        obj[1]['id']
                    ],
                    "remark": None,
                    "id": None,
                    "sort": 4
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('put', 'Evx1QWKUp', data, 'main', nocheck)

    @doc(v7dp0gZaBk5c5dnae7G3)
    @BaseApi.timing_decorator
    def v7dp0gZaBk5c5dnae7G3(self, nocheck=False):
        obj = self.pc.WmKG9OkI9OlJlOENUzgNu()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        data = [
            obj[0]['id']
        ]
        self.validate_request_data(data)
        return self._make_request('post', 'ZlYpQhYLf', data, 'main', nocheck)

    @doc(RB3GNQ8IJqAeegDYmA32)
    @BaseApi.timing_decorator
    def RB3GNQ8IJqAeegDYmA32(self, nocheck=False):
        obj = self.pc.WmKG9OkI9OlJlOENUzgNu()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        data = [
            obj[0]['id']
        ]
        self.validate_request_data(data)
        return self._make_request('post', 'ZlYpQhYLf', data, 'main', nocheck)

    @doc(FNyrgjsFJzK3B4902iHy)
    @BaseApi.timing_decorator
    def FNyrgjsFJzK3B4902iHy(self, nocheck=False):
        obj = self.pc.WmKG9OkI9OlJlOENUzgNu()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        data = [
            obj[0]['id']
        ]
        self.validate_request_data(data)
        return self._make_request('post', 'ZlYpQhYLf', data, 'main', nocheck)

    @doc(q7pI3tL3zRqZ67pGHnxf)
    @BaseApi.timing_decorator
    def q7pI3tL3zRqZ67pGHnxf(self, nocheck=False):
        obj = self.pc.WmKG9OkI9OlJlOENUzgNu()
        data = [
            obj[0]['id'],
        ]
        self.validate_request_data(data)
        return self._make_request('post', 'NSoJocsGm', data, 'main', nocheck)

    @doc(HTjf6RsIbsSIfYSwsXzv)
    @BaseApi.timing_decorator
    def HTjf6RsIbsSIfYSwsXzv(self, nocheck=False):
        obj = self.pc.WmKG9OkI9OlJlOENUzgNu()
        obj_2 = self.pc.WziJGBshZjou10L8PleRe()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        data = {
            "orderNo": obj[0]['orderNo'],
            "processId": obj[0]['taskProgressList'][0]['id'],
            "state": "2",
            "workDuration": 24,
            "userId": INFO['main_user_id'],
            "workQualifiedNum": 100,
            "workDefectsNum": 0,
            "remark": "备注",
            "workId": obj[0]['id'],
            "workDefectList": [
                {
                    "num": 0,
                    "defectId": obj_2[0]['id']
                },
                {
                    "num": 0,
                    "defectId": obj_2[1]['id']
                }
            ],
            "workStartTime": self.get_formatted_datetime(),
            "workEndTime": self.get_formatted_datetime(days=1),
        }
        self.validate_request_data(data)
        return self._make_request('post', 'p3u6vvLZS', data, 'main', nocheck)

    @doc(sruAfwpM3knh3URDgVTd)
    @BaseApi.timing_decorator
    def sruAfwpM3knh3URDgVTd(self, nocheck=False):
        obj = self.pc.WmKG9OkI9OlJlOENUzgNu()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        data = {
            "orderNo": obj[0]['orderNo'],
            "processId": obj[0]['taskProgressList'][1]['id'],
            "state": "2",
            "workDuration": 24,
            "userId": INFO['main_user_id'],
            "workQualifiedNum": 0,
            "workDefectsNum": 0,
            "remark": "备注",
            "price": 88.88,
            "workId": obj[0]['id'],
            "workStartTime": self.get_formatted_datetime(),
            "workEndTime": self.get_formatted_datetime(days=1),
        }
        self.validate_request_data(data)
        return self._make_request('post', 'p3u6vvLZS', data, 'main', nocheck)

    @doc(IBx6SkNmcqoSeAqgrxkF)
    @BaseApi.timing_decorator
    def IBx6SkNmcqoSeAqgrxkF(self, nocheck=False):
        obj = self.pc.WmKG9OkI9OlJlOENUzgNu()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        data = {
            "orderNo": obj[0]['orderNo'],
            "processId": obj[0]['taskProgressList'][2]['id'],
            "state": "2",
            "workDuration": 24,
            "userId": INFO['main_user_id'],
            "workQualifiedNum": 5,
            "workDefectsNum": 0,
            "remark": "备注",
            "workNum": 5,
            "workId": obj[0]['id'],
            "workStartTime": self.get_formatted_datetime(),
            "workEndTime": self.get_formatted_datetime(days=1),
        }
        self.validate_request_data(data)
        return self._make_request('post', 'p3u6vvLZS', data, 'main', nocheck)

    @doc(vkKizyCO3AYcLb15f5j2)
    @BaseApi.timing_decorator
    def vkKizyCO3AYcLb15f5j2(self, nocheck=False):
        obj = self.pc.WmKG9OkI9OlJlOENUzgNu()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        data = {
            "orderNo": obj[0]['orderNo'],
            "processId": obj[0]['taskProgressList'][3]['id'],
            "state": "2",
            "workDuration": 24,
            "userId": INFO['main_user_id'],
            "workQualifiedNum": 0,
            "workDefectsNum": 0,
            "remark": "备注",
            "price": 23.43,
            "workId": obj[0]['id'],
            "workStartTime": self.get_formatted_datetime(),
            "workEndTime": self.get_formatted_datetime(days=1),
        }
        self.validate_request_data(data)
        return self._make_request('post', 'p3u6vvLZS', data, 'main', nocheck)

    @doc(pQejvS83KhwLmhztGkIZ)
    @BaseApi.timing_decorator
    def pQejvS83KhwLmhztGkIZ(self, nocheck=False):
        obj = self.pc.WmKG9OkI9OlJlOENUzgNu()
        obj_2 = self.pc.WziJGBshZjou10L8PleRe()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        data = {
            "id": obj[0]['id'],
            "workNum": 1,
            "workStartTime": obj[0]['workStartTime'],
            "workEndTime": obj[0]['workEndTime'],
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "processList": [
                {
                    "processId": obj[0]['taskProgressList'][0]['processId'],
                    "processNum": 1,
                    "callType": 1,
                    "processStartTime": obj[0]['workStartTime'],
                    "processEndTime": obj[0]['workEndTime'],
                    "processUserIdList": [
                        INFO['main_user_id']
                    ],
                    "defectIdList": [
                        obj_2[0]['id'],
                        obj_2[1]['id'],
                    ],
                    "remark": None,
                    "id": obj[0]['taskProgressList'][0]['id'],
                    "sort": 1
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('put', 'Evx1QWKUp', data, 'main', nocheck)

    @doc(KOF9RCucwpiZtv3KYptu)
    @BaseApi.timing_decorator
    def KOF9RCucwpiZtv3KYptu(self, nocheck=False):
        obj = self.pc.WmKG9OkI9OlJlOENUzgNu()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        data = {
            "orderNo": obj[0]['orderNo'],
            "pageNum": 1,
            "pageSize": 10
        }
        self.validate_request_data(data)
        return self._make_request('post', 'zaz3DUWFs', data, 'main', nocheck)

    @doc(D198Z7vIR4WbkTl36hHI)
    @BaseApi.timing_decorator
    def D198Z7vIR4WbkTl36hHI(self, nocheck=False):
        obj = self.pc.WmKG9OkI9OlJlOENUzgNu()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "workStartTime": self.get_formatted_datetime(),
            "workEndTime": self.get_formatted_datetime(days=1),
        }
        self.validate_request_data(data)
        return self._make_request('post', 'zaz3DUWFs', data, 'main', nocheck)

    @doc(GlZThKYcHMLtYtD6WFjf)
    @BaseApi.timing_decorator
    def GlZThKYcHMLtYtD6WFjf(self, nocheck=False):
        obj = self.pc.WmKG9OkI9OlJlOENUzgNu()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        data = {
            "supplierId": INFO['main_supplier_id'],
            "pageNum": 1,
            "pageSize": 10
        }
        self.validate_request_data(data)
        return self._make_request('post', 'zaz3DUWFs', data, 'main', nocheck)

    @doc(ZfNPiUkcpGxXUTMsfG0n)
    @BaseApi.timing_decorator
    def ZfNPiUkcpGxXUTMsfG0n(self, nocheck=False, state=None):
        data = {
            "state": state,
            "pageNum": 1,
            "pageSize": 10
        }
        self.validate_request_data(data)
        return self._make_request('post', 'zaz3DUWFs', data, 'main', nocheck)


class SDhYvjpFxu(InitializeParams):
    """商品采购|采购任务"""

    @doc(tuGormTpYPA2aELsOzkM)
    @BaseApi.timing_decorator
    def tuGormTpYPA2aELsOzkM(self, nocheck=False):
        data = {
            "name": "采购任务" + self.serial,
            "userId": INFO['main_user_id'],
            "startTime": self.get_the_date(),
            "endTime": self.get_the_date(days=1),
            "remark": "备注",
            "taskSuppliers": [
                {
                    "supplierId": INFO['main_supplier_id'],
                    "supplierName": INFO['main_supplier_name']
                }
            ],
            "infos": [
                {
                    "articlesTypeId": 1,
                    "articlesTypeName": "手机",
                    "brandId": 1,
                    "brandName": "苹果",
                    "modelId": 7692,
                    "modelName": "iPhone 5S",
                    "taskNum": 1,
                    "skuJsonObject": {
                        "articlesTypeId": 1,
                        "articlesTypeName": "手机",
                        "brandName": "苹果",
                        "brandId": 1,
                        "modelId": 7692,
                        "modelName": "iPhone 5S",
                        "skuInfo": "苹果小型号:A1530;购买渠道:国行;颜色:金色;ROM容量:16G;电池健康度:电池健康度100%;苹果保修情况:保修时长≥330天;商品来源:二手优品;成色:全新仅拆封;",
                        "smallModelId": 94,
                        "smallModelName": "A1530",
                        "buyChannelId": 16,
                        "buyChannelName": "国行",
                        "colorId": 49,
                        "colorName": "金色",
                        "romId": 37,
                        "romName": "16G",
                        "batteryHealthId": 23024,
                        "batteryHealthName": "电池健康度100%",
                        "warrantyDurationId": 23005,
                        "warrantyDurationName": "保修时长≥330天",
                        "machineTypeId": 862,
                        "machineTypeName": "二手优品",
                        "finenessId": 1,
                        "finenessName": "全新仅拆封"
                    },
                    "successNum": 0
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'OeEzn1U3T', data, 'main', nocheck)

    @doc(Vax4XBiddBZJvUZ7eKdV)
    @BaseApi.timing_decorator
    def Vax4XBiddBZJvUZ7eKdV(self, nocheck=False):
        data = {
            "name": "采购任务" + self.serial,
            "userId": INFO['main_user_id'],
            "startTime": self.get_the_date(),
            "endTime": self.get_the_date(days=1),
            "remark": "备注",
            "taskSuppliers": [
                {
                    "supplierId": INFO['main_supplier_id'],
                    "supplierName": INFO['main_supplier_name']
                }
            ],
            "infos": [
                {
                    "articlesTypeId": 3,
                    "articlesTypeName": "平板电脑",
                    "brandId": 8,
                    "brandName": "华为",
                    "modelId": 17792,
                    "modelName": "Hi MatePad 11.5寸 2024款 柔光版",
                    "taskNum": 1,
                    "skuJsonObject": {
                        "articlesTypeId": 3,
                        "articlesTypeName": "平板电脑",
                        "brandName": "华为",
                        "brandId": 8,
                        "modelId": 17792,
                        "modelName": "Hi MatePad 11.5寸 2024款 柔光版",
                        "skuInfo": "购买渠道:国行;RAM（运存）:8G;ROM容量:128G;网络制式:WIFI;商品来源:二手优品;成色:全新仅拆封;",
                        "buyChannelId": 16,
                        "buyChannelName": "国行",
                        "ramId": 35,
                        "ramName": "8G",
                        "romId": 40,
                        "romName": "128G",
                        "networkStandardId": 68,
                        "networkStandardName": "WIFI",
                        "machineTypeId": 862,
                        "machineTypeName": "二手优品",
                        "finenessId": 1,
                        "finenessName": "全新仅拆封"
                    },
                    "successNum": 0
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'OeEzn1U3T', data, 'main', nocheck)

    @doc(XBHUgvj186aUw4Sixsaa)
    @BaseApi.timing_decorator
    def XBHUgvj186aUw4Sixsaa(self, nocheck=False):
        data = {
            "name": "采购任务" + self.serial,
            "userId": INFO['main_user_id'],
            "startTime": self.get_the_date(),
            "endTime": self.get_the_date(days=1),
            "remark": "备注",
            "taskSuppliers": [
                {
                    "supplierId": INFO['main_supplier_id'],
                    "supplierName": INFO['main_supplier_name']
                }
            ],
            "infos": [
                {
                    "articlesTypeId": 4,
                    "articlesTypeName": "笔记本电脑",
                    "brandId": 8,
                    "brandName": "华为",
                    "modelId": 12612,
                    "modelName": "MateBook D 14 SE 2023款",
                    "taskNum": 1,
                    "skuJsonObject": {
                        "articlesTypeId": 4,
                        "articlesTypeName": "笔记本电脑",
                        "brandName": "华为",
                        "brandId": 8,
                        "modelId": 12612,
                        "modelName": "MateBook D 14 SE 2023款",
                        "skuInfo": "RAM（运存）:16GB;固态硬盘:不含固态硬盘;机械硬盘:不含机械硬盘;显卡:核芯/集成显卡;处理器:Intel Core i5 12代;商品来源:二手优品;成色:全新仅拆封;",
                        "ramId": 812,
                        "ramName": "16GB",
                        "ssdId": 526,
                        "ssdName": "不含固态硬盘",
                        "mechanicalHardDriveId": 514,
                        "mechanicalHardDriveName": "不含机械硬盘",
                        "graphicsCardModelId": 712,
                        "graphicsCardModelName": "核芯/集成显卡",
                        "processorId": 842,
                        "processorName": "Intel Core i5 12代",
                        "machineTypeId": 862,
                        "machineTypeName": "二手优品",
                        "finenessId": 1,
                        "finenessName": "全新仅拆封"
                    },
                    "successNum": 0
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'OeEzn1U3T', data, 'main', nocheck)

    @doc(IlyTw4WbHlrGhJIXjQNt)
    @BaseApi.timing_decorator
    def IlyTw4WbHlrGhJIXjQNt(self, nocheck=False):
        data = {
            "name": "采购任务" + self.serial,
            "userId": INFO['main_user_id'],
            "startTime": self.get_the_date(),
            "endTime": self.get_the_date(days=1),
            "remark": "备注",
            "taskSuppliers": [
                {
                    "supplierId": INFO['main_supplier_id'],
                    "supplierName": INFO['main_supplier_name']
                }
            ],
            "infos": [
                {
                    "articlesTypeId": 5,
                    "articlesTypeName": "智能手表",
                    "brandId": 8,
                    "brandName": "华为",
                    "modelId": 13352,
                    "modelName": "Watch GT 4",
                    "taskNum": 1,
                    "skuJsonObject": {
                        "articlesTypeId": 5,
                        "articlesTypeName": "智能手表",
                        "brandName": "华为",
                        "brandId": 8,
                        "modelId": 13352,
                        "modelName": "Watch GT 4",
                        "skuInfo": "表壳材质:不锈钢+高分子纤维复合材料;连接:GPS;购买渠道:国行;表壳尺寸:41毫米;商品来源:二手优品;成色:全新仅拆封;",
                        "caseMaterialId": 1790,
                        "caseMaterialName": "不锈钢+高分子纤维复合材料",
                        "connectId": 374,
                        "connectName": "GPS",
                        "buyChannelId": 16,
                        "buyChannelName": "国行",
                        "caseSizeId": 368,
                        "caseSizeName": "41毫米",
                        "machineTypeId": 862,
                        "machineTypeName": "二手优品",
                        "finenessId": 1,
                        "finenessName": "全新仅拆封"
                    },
                    "successNum": 0
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'OeEzn1U3T', data, 'main', nocheck)

    @doc(Jo3v4QXhq0GyXeDDjAG8)
    @BaseApi.timing_decorator
    def Jo3v4QXhq0GyXeDDjAG8(self, nocheck=False):
        obj = self.pc.ZzpxfXbO9fEmLG1gxxzjP(data='a')
        ParamCache.cache_object({'i': obj[0]['taskOrderNo']})
        data = {
            "purchaseTaskInfoList": [
                {
                    "id": obj[0]['id'],
                    "ids": None,
                    "taskOrderNo": obj[0]['taskOrderNo'],
                    "supplierId": INFO['main_supplier_id'],
                    "supplierIds": None,
                    "supplierName": INFO['main_supplier_name'],
                    "articlesTypeId": obj[0]['articlesTypeId'],
                    "articlesTypeName": obj[0]['articlesTypeName'],
                    "brandId": obj[0]['brandId'],
                    "brandName": obj[0]['brandName'],
                    "modelId": obj[0]['modelId'],
                    "modelName": obj[0]['modelName'],
                    "skuJsonObject": {
                        "createBy": None,
                        "createTime": None,
                        "updateBy": None,
                        "updateTime": None,
                        "remark": None,
                        "pageSize": 10,
                        "pageNum": 1,
                        "orderByColumn": "create_time",
                        "isAsc": "desc",
                        "erpStartTime": None,
                        "erpEndTime": None,
                        "id": None,
                        "articlesNo": None,
                        "articlesNoList": None,
                        "imei": None,
                        "articlesTypeId": obj[0]['skuJsonObject']['articlesTypeId'],
                        "articlesTypeName": obj[0]['skuJsonObject']['articlesTypeName'],
                        "brandId": obj[0]['skuJsonObject']['brandId'],
                        "brandName": obj[0]['skuJsonObject']['brandName'],
                        "modelId": obj[0]['skuJsonObject']['modelId'],
                        "modelName": obj[0]['skuJsonObject']['modelName'],
                        "romId": obj[0]['skuJsonObject']['romId'],
                        "romName": obj[0]['skuJsonObject']['romName'],
                        "ramId": None,
                        "ramName": None,
                        "colorId": obj[0]['skuJsonObject']['colorId'],
                        "colorName": obj[0]['skuJsonObject']['colorName'],
                        "buyChannelId": obj[0]['skuJsonObject']['buyChannelId'],
                        "buyChannelName": obj[0]['skuJsonObject']['buyChannelName'],
                        "smallModelId": obj[0]['skuJsonObject']['smallModelId'],
                        "smallModelName": obj[0]['skuJsonObject']['smallModelName'],
                        "serialNo": None,
                        "detailId": None,
                        "warrantyDurationId": obj[0]['skuJsonObject']['warrantyDurationId'],
                        "warrantyDurationName": obj[0]['skuJsonObject']['warrantyDurationName'],
                        "machineTypeId": obj[0]['skuJsonObject']['machineTypeId'],
                        "machineTypeName": obj[0]['skuJsonObject']['machineTypeName'],
                        "batteryHealthId": obj[0]['skuJsonObject']['batteryHealthId'],
                        "batteryHealthName": obj[0]['skuJsonObject']['batteryHealthName'],
                        "finenessId": obj[0]['skuJsonObject']['finenessId'],
                        "finenessName": obj[0]['skuJsonObject']['finenessName'],
                        "networkStandardId": None,
                        "networkStandardName": None,
                        "mobileNetworkId": None,
                        "mobileNetworkName": None,
                        "unicomNetworkId": None,
                        "unicomNetworkName": None,
                        "telecomNetworkId": None,
                        "telecomNetworkName": None,
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
                        "isDelete": None,
                        "assessParam": None,
                        "assessTitle": None,
                        "warehouseId": None
                    },
                    "skuJson": obj[0]['skuJson'],
                    "skuInfo": obj[0]['skuInfo'],
                    "taskNum": 1,
                    "deliveryNum": 30,
                    "qualifiedNum": 10,
                    "successNum": 0,
                    "remark": "备注",
                    "skuTaskNum": None,
                    "purchaseNum": None
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'qJGogY0tt', data, 'main', nocheck)

    @doc(e65OsVYsAZfUdtju3ktx)
    @BaseApi.timing_decorator
    def e65OsVYsAZfUdtju3ktx(self, nocheck=False):
        obj = self.pc.ZzpxfXbO9fEmLG1gxxzjP(data='b')
        ParamCache.cache_object({'i': obj[0]['taskOrderNo']})
        data = {
            "payState": "2",
            "taskOrderNo": obj[0]['taskOrderNo'],
            "purchaseTime": self.get_formatted_datetime(),
            "supplierName": INFO['main_supplier_name'],
            "supplierId": INFO['main_supplier_id'],
            "userId": INFO['main_user_id'],
            "userName": INFO['main_manager'],
            "warehouseId": INFO['main_item_warehouse_id'],
            "purchaseOrdersArticlesDTOList": [
                {
                    "imei": self.imei,
                    "warehouseId": INFO['main_item_warehouse_id'],
                    "purchasePrice": 500,
                    "purchaseArticlesInfoDTO": {
                        "createBy": None,
                        "createTime": None,
                        "updateBy": None,
                        "updateTime": None,
                        "remark": None,
                        "pageSize": 10,
                        "pageNum": 1,
                        "orderByColumn": "create_time",
                        "isAsc": "desc",
                        "erpStartTime": None,
                        "erpEndTime": None,
                        "id": None,
                        "articlesNo": None,
                        "articlesNoList": None,
                        "imei": None,
                        "articlesTypeId": obj[0]['skuJsonObject']['articlesTypeId'],
                        "articlesTypeName": obj[0]['skuJsonObject']['articlesTypeName'],
                        "brandId": obj[0]['skuJsonObject']['brandId'],
                        "brandName": obj[0]['skuJsonObject']['brandName'],
                        "modelId": obj[0]['skuJsonObject']['modelId'],
                        "modelName": obj[0]['skuJsonObject']['modelName'],
                        "romId": obj[0]['skuJsonObject']['romId'],
                        "romName": obj[0]['skuJsonObject']['romName'],
                        "ramId": None,
                        "ramName": None,
                        "colorId": obj[0]['skuJsonObject']['colorId'],
                        "colorName": obj[0]['skuJsonObject']['colorName'],
                        "buyChannelId": obj[0]['skuJsonObject']['buyChannelId'],
                        "buyChannelName": obj[0]['skuJsonObject']['buyChannelName'],
                        "smallModelId": obj[0]['skuJsonObject']['smallModelId'],
                        "smallModelName": obj[0]['skuJsonObject']['smallModelName'],
                        "serialNo": None,
                        "detailId": None,
                        "warrantyDurationId": obj[0]['skuJsonObject']['warrantyDurationId'],
                        "warrantyDurationName": obj[0]['skuJsonObject']['warrantyDurationName'],
                        "machineTypeId": obj[0]['skuJsonObject']['machineTypeId'],
                        "machineTypeName": obj[0]['skuJsonObject']['machineTypeName'],
                        "batteryHealthId": obj[0]['skuJsonObject']['batteryHealthId'],
                        "batteryHealthName": obj[0]['skuJsonObject']['batteryHealthName'],
                        "finenessId": obj[0]['skuJsonObject']['finenessId'],
                        "finenessName": obj[0]['skuJsonObject']['finenessName'],
                        "networkStandardId": None,
                        "networkStandardName": None,
                        "mobileNetworkId": None,
                        "mobileNetworkName": None,
                        "unicomNetworkId": None,
                        "unicomNetworkName": None,
                        "telecomNetworkId": None,
                        "telecomNetworkName": None,
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
                        "isDelete": None,
                        "assessParam": None,
                        "assessTitle": None,
                        "warehouseId": None
                    },
                    "infoId": "2039639142114267137",
                    "supplyType": 2,
                    "supplyTypeDesc": "C"
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'CSwjLDWyD', data, 'main', nocheck)

    @doc(QlWxSfpR4xrTDauwyHLD)
    @BaseApi.timing_decorator
    def QlWxSfpR4xrTDauwyHLD(self, nocheck=False):
        obj = self.pc.ZzpxfXbO9fEmLG1gxxzjP()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        data = {
            "supplierId": INFO['main_supplier_id'],
            "returnNum": 1,
            "logisticsNo": self.sf,
            "isLogistics": 0,
            "returnTime": self.get_formatted_datetime(),
            "supplierName": "壹站收",
            "taskOrderNo": obj[0]['orderNo']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'IZyPme0A0', data, 'main', nocheck)

    @doc(WYBiBGE7VdR3njn7NPom)
    @BaseApi.timing_decorator
    def WYBiBGE7VdR3njn7NPom(self, nocheck=False):
        obj = self.pc.ZzpxfXbO9fEmLG1gxxzjP()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        data = {
            "supplierId": INFO['main_supplier_id'],
            "returnNum": 1,
            "logisticsNo": self.sf,
            "isLogistics": 0,
            "returnTime": self.get_formatted_datetime(),
            "supplierName": "壹站收",
            "taskOrderNo": obj[0]['orderNo']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'IZyPme0A0', data, 'main', nocheck)


if __name__ == '__main__':
    api = ()
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
