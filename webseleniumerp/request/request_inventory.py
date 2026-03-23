# coding: utf-8
import json
from common.base_api import BaseApi
from common.base_params import InitializeParams, is_performance_close
from common.file_cache_manager import ParamCache
from common.import_desc import *
from config.user_info import INFO


class InventoryAddressManageRequest(InitializeParams):
    """库存管理|出库管理|地址管理"""

    @doc(i_add_address)
    @BaseApi.timing_decorator
    def add_address(self, nocheck=False):
        data = {
            "detailMsg": "和平路" + self.serial + "号",
            "deliverName": "杰克" + self.serial,
            "phone": self.phone,
            "type": "1",
            "provinceId": 1100,
            "cityId": 11010,
            "countyId": 1104,
            "offDefault": 0
        }
        return self._make_request('post', 'address_manage_add', data, 'idle', nocheck)

    @doc(i_edit_address)
    @BaseApi.timing_decorator
    def edit_address(self, nocheck=False):
        res = self.pc.inventory_address_manage_data()
        data = {
            "createBy": res[0]['createBy'],
            "createTime": res[0]['createTime'],
            "pageSize": 10,
            "pageNum": 1,
            "orderByColumn": "create_time",
            "isAsc": "desc",
            "id": res[0]['id'],
            "type": "1",
            "typeName": "通用业务",
            "provinceId": INFO['province_id'],
            "provinceName": INFO['province_name'],
            "cityId": INFO['city_id'],
            "cityName": INFO['city_name'],
            "countyId": INFO['county_id'],
            "countyName": INFO['county_name'],
            "detailMsg": INFO['detailed_address'],
            "deliverName": INFO['address_creator'],
            "phone": INFO['receiving_phone'],
            "userId": INFO['main_user_id'],
            "isDelete": 0,
            "tenantId": res[0]['tenantId'],
            "editBool": "false",
            "offDefault": 0
        }
        return self._make_request('put', 'address_manage_add', data, 'idle', nocheck)

    @doc(i_delete_address)
    @BaseApi.timing_decorator
    def delete_address(self, nocheck=False):
        res = self.pc.inventory_address_manage_data()
        data = [
            res[0]['id']
        ]
        return self._make_request('post', 'address_manage_delete', data, 'idle', nocheck)


class InventoryHandOverGoodsRecordsRequest(InitializeParams):
    """库存管理|移交接收管理|移交记录"""

    @doc(i_hand_over_records_search_by_imei)
    @BaseApi.timing_decorator
    def hand_over_records_search_by_imei(self):
        res = self.pc.inventory_receive_records_data(data='a')
        imei = res[0]['imei']
        ParamCache.cache_object({"imei": imei}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesNo": imei,
            "articlesType": 1
        }
        return self._make_request('post', 'handover_records_list', data, 'main')

    @doc(i_hand_over_records_search_by_order_no)
    @BaseApi.timing_decorator
    def hand_over_records_search_by_order_no(self):
        res = self.pc.inventory_receive_records_data()
        order_no = res[0]['orderNo']
        ParamCache.cache_object({"orderNo": order_no}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "orderNo": order_no,
            "articlesType": 1
        }
        return self._make_request('post', 'handover_records_list', data, 'main')

    @doc(i_hand_over_records_search_by_status)
    @BaseApi.timing_decorator
    def hand_over_records_search_by_status(self, status=None):
        if status is None:
            res = self.pc.inventory_receive_records_data(data='a')
            status = res[0]['status']
        ParamCache.cache_object({"status": status}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "status": status,
            "articlesType": 1
        }
        return self._make_request('post', 'handover_records_list', data, 'main')

    @doc(i_hand_over_records_search_by_reason_type)
    @BaseApi.timing_decorator
    def hand_over_records_search_by_reason_type(self, reason_type=None):
        if reason_type is None:
            res = self.pc.inventory_receive_records_data(data='a')
            reason_type = res[0]['reasonType']
        ParamCache.cache_object({"reasonType": reason_type}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "reasonType": reason_type,
            "articlesType": 1
        }
        return self._make_request('post', 'handover_records_list', data, 'main')

    @doc(i_hand_over_records_search_by_person)
    @BaseApi.timing_decorator
    def hand_over_records_search_by_person(self):
        ParamCache.cache_object({"distributorId": INFO['main_user_id']}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "distributorId": INFO['main_user_id'],
            "articlesType": 1
        }
        return self._make_request('post', 'handover_records_list', data, 'main')

    @doc(i_hand_over_records_search_by_receive_id)
    @BaseApi.timing_decorator
    def hand_over_records_search_by_receive_id(self):
        ParamCache.cache_object({"receiveId": INFO['main_user_id']}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "userId": INFO['main_user_id'],
            "articlesType": 1
        }
        return self._make_request('post', 'handover_records_list', data, 'main')


class InventoryHandOverGoodsRequest(InitializeParams):
    """库存管理|移交接收管理|移交物品"""

    @doc(i_hand_over_goods)
    @BaseApi.timing_decorator
    def hand_over_goods(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='3')
        data = {
            "type": "6",
            "userId": INFO['main_user_id'],
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "createBy": INFO['super_admin_account']
        }
        return self._make_request('post', 'item_inventory_transfer', data, 'main', nocheck)


class InventoryItemSignWarehousingRequest(InitializeParams):
    """库存管理|入库管理|物品签收入库"""

    @doc(i_sign_for_receipt)
    @BaseApi.timing_decorator
    def sign_for_receipt(self, nocheck=False):
        res = self.pc.inventory_list_data(i='1')
        data = {
            "warehouseId": INFO['main_item_warehouse_id'],
            "articlesList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "logisticsNo": res[0]['logisticsNo']
                }
            ],
            "quickOperation": 0,
            "purchaseOrdersArticlesDTO": {
                "articlesNoList": [
                    res[0]['articlesNo']
                ],
                "createBy": "",
                "type": "",
                "userId": ""
            }
        }
        return self._make_request('post', 'not_hand_over', data, 'main', nocheck)


class InventoryListRequest(InitializeParams):
    """库存管理|库存列表"""

    @doc(i_inventory_transfer_sell_special)
    @BaseApi.timing_decorator
    def inventory_transfer_sell_special(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='3')
        data = {
            "type": "4",
            "userId": INFO['special_user_id'],
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "remark": "备注",
            "createBy": INFO['special_account_name']
        }
        return self._make_request('post', 'item_inventory_transfer', data, 'main', nocheck)

    @doc(i_inventory_transfer_repair_special)
    @BaseApi.timing_decorator
    def inventory_transfer_repair_special(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='3')
        data = {
            "type": "2",
            "userId": INFO['special_user_id'],
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "remark": "备注",
            "createBy": INFO['special_account_name']
        }
        return self._make_request('post', 'item_inventory_transfer', data, 'main', nocheck)

    @doc(i_inventory_transfer_purchase_special)
    @BaseApi.timing_decorator
    def inventory_transfer_purchase_special(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='3')
        data = {
            "type": "5",
            "userId": INFO['special_user_id'],
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "remark": "备注",
            "createBy": INFO['special_account_name']
        }
        return self._make_request('post', 'item_inventory_transfer', data, 'main', nocheck)

    @doc(i_inventory_transfer_quality_special)
    @BaseApi.timing_decorator
    def inventory_transfer_quality_special(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='3')
        data = {
            "type": "1",
            "userId": INFO['special_user_id'],
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "remark": "备注",
            "createBy": INFO['special_account_name']
        }
        return self._make_request('post', 'item_inventory_transfer', data, 'main', nocheck)

    @doc(i_inventory_transfer_send_special)
    @BaseApi.timing_decorator
    def inventory_transfer_send_special(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='3')
        data = {
            "type": "3",
            "userId": INFO['special_user_id'],
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "remark": "备注",
            "createBy": INFO['special_account_name']
        }
        return self._make_request('post', 'item_inventory_transfer', data, 'main', nocheck)

    @doc(i_inventory_transfer_purchase_main)
    @BaseApi.timing_decorator
    def inventory_transfer_purchase_main(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='3')
        data = {
            "type": "5",
            "userId": INFO['main_user_id'],
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "remark": "备注",
            "createBy": INFO['main_account']
        }
        return self._make_request('post', 'item_inventory_transfer', data, 'main', nocheck)

    @doc(i_inventory_transfer_sell_main)
    @BaseApi.timing_decorator
    def inventory_transfer_sell_main(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='3')
        data = {
            "type": "4",
            "userId": INFO['main_user_id'],
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "remark": "备注",
            "createBy": INFO['main_account']
        }
        return self._make_request('post', 'item_inventory_transfer', data, 'main', nocheck)

    @doc(i_inventory_transfer_quality_main)
    @BaseApi.timing_decorator
    def inventory_transfer_quality_main(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='3')
        data = {
            "type": "1",
            "userId": INFO['main_user_id'],
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "remark": "备注",
            "createBy": INFO['main_account']
        }
        return self._make_request('post', 'item_inventory_transfer', data, 'main', nocheck)

    @doc(i_inventory_transfer_repair_main)
    @BaseApi.timing_decorator
    def inventory_transfer_repair_main(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='3')
        data = {
            "type": "2",
            "userId": INFO['main_user_id'],
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "remark": "备注",
            "createBy": INFO['main_account']
        }
        return self._make_request('post', 'item_inventory_transfer', data, 'main', nocheck)

    @doc(i_inventory_transfer_send_main)
    @BaseApi.timing_decorator
    def inventory_transfer_send_main(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='13')
        data = {
            "type": "3",
            "userId": INFO['main_user_id'],
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "remark": "备注",
            "createBy": INFO['main_account']
        }
        return self._make_request('post', 'item_inventory_transfer', data, 'main', nocheck)

    @doc(i_inventory_list_search_by_imei)
    @BaseApi.timing_decorator
    def inventory_list_search_by_imei(self):
        res = self.pc.inventory_list_data(i='2', j='3')
        imei = res[0]['imei']
        ParamCache.cache_object({"imei": imei}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "inventoryStatus": "2",
            "articlesNoOrImei": imei
        }
        return self._make_request('post', 'item_inventory_list', data, 'main')

    @doc(i_inventory_list_search_by_supplier)
    @BaseApi.timing_decorator
    def inventory_list_search_by_supplier(self):
        ParamCache.cache_object({"supplierId": INFO['main_supplier_id']}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "supplierId": INFO['main_supplier_id'],
            "inventoryStatus": "2"
        }
        return self._make_request('post', 'item_inventory_list', data, 'main')

    @doc(i_inventory_list_search_by_purchaser)
    @BaseApi.timing_decorator
    def inventory_list_search_by_purchaser(self):
        ParamCache.cache_object({"purchaseId": INFO['main_user_id']}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "purchaseId": INFO['main_user_id'],
            "inventoryStatus": "2"
        }
        return self._make_request('post', 'item_inventory_list', data, 'main')

    @doc(i_inventory_list_search_by_type_id)
    @BaseApi.timing_decorator
    def inventory_list_search_by_type_id(self, articles_type_id):
        ParamCache.cache_object({"articlesTypeId": articles_type_id}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesTypeId": articles_type_id
        }
        return self._make_request('post', 'item_inventory_list', data, 'main')

    @doc(i_inventory_list_search_by_purchase_date)
    @BaseApi.timing_decorator
    def inventory_list_search_by_purchase_date(self):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "inventoryStatus": "2",
            "purchaseStartTime": self.get_the_date(),
            "purchaseEndTime": self.get_the_date()
        }
        return self._make_request('post', 'item_inventory_list', data, 'main')

    @doc(i_inventory_list_search_by_saler)
    @BaseApi.timing_decorator
    def inventory_list_search_by_saler(self):
        ParamCache.cache_object({"belongId": INFO['main_user_id']}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "salesId": INFO['main_user_id'],
            "inventoryStatus": "2"
        }
        return self._make_request('post', 'item_inventory_list', data, 'main')

    @doc(i_inventory_list_search_by_sale_custom)
    @BaseApi.timing_decorator
    def inventory_list_search_by_sale_custom(self):
        ParamCache.cache_object({"salesChannelNo": INFO['main_sale_supplier_id']}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "salesChannelNo": INFO['main_sale_supplier_id'],
            "inventoryStatus": "2"
        }
        return self._make_request('post', 'item_inventory_list', data, 'main')

    @doc(i_inventory_list_search_by_articles_state)
    @BaseApi.timing_decorator
    def inventory_list_search_by_articles_state(self, articles_state):
        ParamCache.cache_object({"articlesState": articles_state}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesState": articles_state,
        }
        return self._make_request('post', 'item_inventory_list', data, 'main')

    @doc(i_inventory_list_search_by_inventory_status)
    @BaseApi.timing_decorator
    def inventory_list_search_by_inventory_status(self, inventory_status):
        ParamCache.cache_object({"inventoryStatus": inventory_status}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "inventoryStatus": inventory_status
        }
        return self._make_request('post', 'item_inventory_list', data, 'main')

    @doc(i_inventory_list_search_by_warehouse_id)
    @BaseApi.timing_decorator
    def inventory_list_search_by_warehouse_id(self):
        ParamCache.cache_object({"warehouseId": INFO['main_item_warehouse_id']}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "warehouseId": INFO['main_item_warehouse_id'],
            "inventoryStatus": "2",
        }
        return self._make_request('post', 'item_inventory_list', data, 'main')

    @doc(i_sale_out_of_warehouse_has)
    @BaseApi.timing_decorator
    def sale_out_of_warehouse_has(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='13')
        data = {
            "offExpressage": "0",
            "saleType": "1",
            "deliveryTime": self.get_formatted_datetime(),
            "clientName": INFO['vice_help_sale_supplier_name'],
            "salePrice": "10",
            "refundMethod": 1,
            "receiveState": 1,
            "status": 1,
            "buyReturn": 1,
            "newSalePrice": 0,
            "newPurchasePrice": 0,
            "saleTime": self.get_formatted_datetime(),
            "userId": INFO['main_user_id'],
            "clientId": INFO['vice_help_sale_supplier_id'],
            "accountNo": INFO['main_account_no'],
            "logisticsOrder": self.jd,
            "logisticsNoPrice": "10",
            "platformArticlesNo": self.serial,
            "platformOrderNo": self.serial,
            "purchaseOrdersArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 3,
                    "id": res[0]['id'],
                    "imei": res[0]['imei'],
                    "platformArticlesNo": self.serial,
                    "platformOrderNo": self.serial,
                    "salePrice": "10",
                    "saleSettlePrice": "10",
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1
                    }
                }
            ]
        }
        return self._make_request('post', 'item_inventory_sell', data, 'main', nocheck)

    @doc(i_sale_out_of_warehouse_not)
    @BaseApi.timing_decorator
    def sale_out_of_warehouse_not(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='13')
        data = {
            "offExpressage": "0",
            "saleType": "1",
            "deliveryTime": self.get_formatted_datetime(),
            "clientName": INFO['vice_help_sale_supplier_name'],
            "salePrice": "10",
            "refundMethod": 1,
            "receiveState": 1,
            "status": 2,
            "buyReturn": 1,
            "newSalePrice": 0,
            "newPurchasePrice": 0,
            "saleTime": self.get_formatted_datetime(),
            "userId": INFO['main_user_id'],
            "clientId": INFO['vice_help_sale_supplier_id'],
            "accountNo": INFO['main_account_no'],
            "logisticsOrder": self.jd,
            "logisticsNoPrice": "10",
            "platformArticlesNo": self.serial,
            "platformOrderNo": self.serial,
            "purchaseOrdersArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 3,
                    "id": res[0]['id'],
                    "imei": res[0]['imei'],
                    "platformArticlesNo": self.serial,
                    "platformOrderNo": self.serial,
                    "salePrice": "10",
                    "saleSettlePrice": "10",
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1
                    }
                }
            ]
        }
        return self._make_request('post', 'item_inventory_sell', data, 'main', nocheck)

    @doc(i_return_after_sale_has)
    @BaseApi.timing_decorator
    def return_after_sale_has(self, nocheck=False):
        res = self.pc.inventory_list_data(i='3', j='9')
        res_2 = self.pc.inventory_list_data(data='b')
        data = {
            "status": 2,
            "newSalePrice": 0,
            "warehouseId": INFO['main_item_warehouse_id'],
            "saleType": "1",
            "returnType": 1,
            "sellSaleOrderArticlesDTOList": [
                {
                    "accessoryNoList": [],
                    "articlesNo": res[0]['articlesNo'],
                    "newSalePrice": 0,
                    "imei": res[0]['imei'],
                    "saleOrderNo": res[0]['salesOrder'],
                    "saleSettlePrice": res_2[0]['saleOrderInfo']['salePrice'],
                }
            ]
        }
        return self._make_request('post', 'sales_after_sales_list', data, 'main', nocheck)

    @doc(i_return_after_sale_not)
    @BaseApi.timing_decorator
    def return_after_sale_not(self, nocheck=False):
        res = self.pc.inventory_list_data(i='3', j='9')
        res_2 = self.pc.inventory_list_data(data='b')
        data = {
            "status": 1,
            "newSalePrice": 0,
            "logisticsNo": self.jd,
            "saleType": "1",
            "returnType": 1,
            "remark": "test",
            "sellSaleOrderArticlesDTOList": [
                {
                    "accessoryNoList": [],
                    "articlesNo": res[0]['articlesNo'],
                    "newSalePrice": 0,
                    "imei": res[0]['imei'],
                    "saleOrderNo": res[0]['salesOrder'],
                    "saleSettlePrice": res_2[0]['saleOrderInfo']['salePrice'],
                }
            ]
        }
        return self._make_request('post', 'sales_after_sales_list', data, 'main', nocheck)

    @doc(i_return_only_parts_has)
    @BaseApi.timing_decorator
    def return_only_parts_has(self, nocheck=False):
        res = self.pc.inventory_list_data(i='3', j='9')
        res_2 = self.pc.inventory_list_data(data='b')
        data = {
            "status": 2,
            "newSalePrice": 20,
            "warehouseId": INFO['main_in_warehouse_id'],
            "accessoryType": 3,
            "accessoryNo": "PJ0140",
            "saleType": "2",
            "returnType": 1,
            "sellSaleOrderArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "platformArticlesNo": self.serial,
                    "newSalePrice": 20,
                    "saleOrderNo": res[0]['salesOrder'],
                    "saleSettlePrice": res_2[0]['saleOrderInfo']['salePrice'],
                    "accessoryNoList": [
                        {
                            "brandId": 2,
                            "brandName": "三星",
                            "modelId": 7792,
                            "modelName": "W2015",
                            "accessoryType": 3,
                            "accessoryNo": "PJ0140",
                            "accessoryQuality": 3,
                            "accessoryPrice": 20,
                            "articlesTypeId": 1,
                            "articlesTypeName": "手机",
                            "channelType": 1,
                            "purchasePrice": 20
                        }
                    ]
                }
            ]
        }
        return self._make_request('post', 'sales_after_sales_list', data, 'main', nocheck)

    @doc(i_return_only_parts_not)
    @BaseApi.timing_decorator
    def return_only_parts_not(self, nocheck=False):
        res = self.pc.inventory_list_data(i='3', j='9')
        res_2 = self.pc.inventory_list_data(data='b')
        data = {
            "status": 1,
            "newSalePrice": 30,
            "logisticsNo": self.jd,
            "accessoryType": 3,
            "accessoryNo": "PJ0170",
            "saleType": "2",
            "returnType": 1,
            "remark": "test",
            "sellSaleOrderArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "platformArticlesNo": "16200143",
                    "newSalePrice": 30,
                    "saleOrderNo": res[0]['salesOrder'],
                    "saleSettlePrice": res_2[0]['saleOrderInfo']['salePrice'],
                    "accessoryNoList": [
                        {
                            "brandId": 313,
                            "brandName": "VIVO",
                            "modelId": 6668,
                            "modelName": "Y67",
                            "accessoryType": 3,
                            "accessoryNo": "PJ0170",
                            "accessoryQuality": 3,
                            "accessoryPrice": 40,
                            "articlesTypeId": 1,
                            "articlesTypeName": "手机",
                            "channelType": 1,
                            "purchasePrice": 40
                        }
                    ]
                }
            ]
        }
        return self._make_request('post', 'sales_after_sales_list', data, 'main', nocheck)

    @doc(i_price_adjustment_after_sales)
    @BaseApi.timing_decorator
    def price_adjustment_after_sales(self, nocheck=False):
        res = self.pc.inventory_list_data(i='3', j='9')
        res_2 = self.pc.inventory_list_data(data='b')
        data = {
            "status": 2,
            "newSalePrice": 50,
            "saleType": "5",
            "returnType": 1,
            "remark": "备注",
            "sellSaleOrderArticlesDTOList": [
                {
                    "accessoryNoList": [],
                    "articlesNo": res[0]['articlesNo'],
                    "newSalePrice": 50,
                    "imei": res[0]['imei'],
                    "saleOrderNo": res[0]['salesOrder'],
                    "saleSettlePrice": res_2[0]['saleOrderInfo']['salePrice']
                }
            ]
        }
        return self._make_request('post', 'sales_after_sales_list', data, 'main', nocheck)

    @doc(i_refund_only_after_purchase)
    @BaseApi.timing_decorator
    def refund_only_after_purchase(self, nocheck=False):
        res = self.pc.inventory_list_data(i='1')
        data = {
            "articlesNo": res[0]['articlesNo'],
            "remark": "备注"
        }
        return self._make_request('post', 'purchases_are_refundable_only', data, 'main', nocheck)

    @doc(i_item_info_edit)
    @BaseApi.timing_decorator
    def item_info_edit(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='3')
        data = {
            "id": res[0]['id'],
            "articlesNo": res[0]['articlesNo'],
            "purchaseArticlesInfoDTO": {
                "id": res[0]['id'],
                "articlesNo": res[0]['articlesNo'],
                "articlesTypeName": res[0]['articlesTypeName'],
                "brandId": res[0]['brandId'],
                "brandName": res[0]['brandName'],
                "modelId": res[0]['modelId'],
                "modelName": res[0]['modelName'],
                "smallModelId": 75,
                "smallModelName": "A1699",
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
            }
        }
        return self._make_request('post', 'inventory_list_edit', data, 'main', nocheck)


class InventoryLogisticsListRequest(InitializeParams):
    """库存管理|入库管理|物流列表"""

    @doc(i_logistics_list_search_by_logistics_no)
    @BaseApi.timing_decorator
    def logistics_list_search_by_logistics_no(self):
        res = self.pc.inventory_logistics_list_data()
        logistics_no = res[0]['logisticsNo']
        ParamCache.cache_object({"logisticsNo": logistics_no}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "logisticsNo": logistics_no
        }
        return self._make_request('post', 'material_flow_list', data, 'main')

    @doc(i_logistics_list_search_by_imei)
    @BaseApi.timing_decorator
    def logistics_list_search_by_imei(self):
        res = self.pc.inventory_logistics_list_data(data='a')
        articlesNo = res[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": articlesNo}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesNoOrImei": articlesNo
        }
        return self._make_request('post', 'material_flow_list', data, 'main')

    @doc(i_logistics_list_search_by_platform_articles_no)
    @BaseApi.timing_decorator
    def logistics_list_search_by_platform_articles_no(self):
        res = self.pc.inventory_logistics_list_data(data='a')
        platformArticlesNo = res[0]['platformArticlesNo']
        logisticsNo = res[0]['logisticsNo']
        ParamCache.cache_object({"platformArticlesNo": platformArticlesNo}, 'practical.json')
        ParamCache.cache_object({"logisticsNo": logisticsNo}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "platformArticlesNo": platformArticlesNo
        }
        return self._make_request('post', 'material_flow_list', data, 'main')

    @doc(i_logistics_list_search_by_business_no)
    @BaseApi.timing_decorator
    def logistics_list_search_by_business_no(self):
        res = self.pc.inventory_logistics_list_data(data='a')
        businessNo = res[0]['businessNo']
        ParamCache.cache_object({"businessNo": businessNo}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "businessNo": businessNo
        }
        return self._make_request('post', 'material_flow_list', data, 'main')

    @doc(i_logistics_list_search_by_sortation_status)
    @BaseApi.timing_decorator
    def logistics_list_search_by_sortation_status(self, status=None):
        res = self.pc.inventory_logistics_list_data(k=status)
        status = res[0]['status']
        ParamCache.cache_object({"status": status}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "sortationStatus": status
        }
        return self._make_request('post', 'material_flow_list', data, 'main')

    @doc(i_logistics_list_search_by_sortation_id)
    @BaseApi.timing_decorator
    def logistics_list_search_by_sortation_id(self):
        userName = INFO['customer_name']
        ParamCache.cache_object({"userName": userName}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "sortationId": INFO['main_user_id']
        }
        return self._make_request('post', 'material_flow_list', data, 'main')

    @doc(i_logistics_list_search_by_date)
    @BaseApi.timing_decorator
    def logistics_list_search_by_date(self):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "sortationStartTime": self.get_the_date(),
            "sortationEndTime": self.get_the_date()
        }
        return self._make_request('post', 'material_flow_list', data, 'main')


class InventoryNewItemRequest(InitializeParams):
    """库存管理|入库管理|物流签收入库"""

    @doc(i_logistics_signature_for_receipt)
    @BaseApi.timing_decorator
    def logistics_signature_for_receipt(self, nocheck=False):
        res = self.pc.inventory_list_data(i='1')
        data = {
            "warehouseId": INFO['main_item_warehouse_id'],
            "articlesList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "warehouseId": ""
                }
            ],
            "logisticsNo": res[0]['logisticsNo'],
            "quickOperation": 0,
            "purchaseOrdersArticlesDTO": {
                "articlesNoList": [
                    res[0]['articlesNo'],
                ],
                "createBy": "",
                "type": "",
                "userId": "",
                "remark": ""
            }
        }
        return self._make_request('post', 'sign_receipt_store', data, 'main', nocheck)

    @doc(i_help_sell_logistics_signature_for_receipt)
    @BaseApi.timing_decorator
    def help_sell_logistics_signature_for_receipt(self, nocheck=False):
        res = self.pc.help_sell_the_list_of_goods_data()
        data = {
            "warehouseId": INFO['main_item_warehouse_id'],
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
        return self._make_request('post', 'sign_receipt_store', data, 'vice', nocheck)


class InventoryOutboundOrdersListRequest(InitializeParams):
    """库存管理|出库管理|仅出库订单列表"""

    @doc(i_return_outgoing_items_warehousing)
    @BaseApi.timing_decorator
    def return_outgoing_items_warehousing(self, nocheck=False):
        res = self.pc.inventory_outbound_orders_list_data()
        res_2 = self.pc.inventory_outbound_orders_list_data(data='a')
        data = {
            "returnMethod": "1",
            "logisticsOrder": self.jd,
            "returnTime": self.get_formatted_datetime(),
            "warehouseId": INFO['main_in_warehouse_id'],
            "articlesList": [
                {
                    "articlesNo": res_2[0]['articlesNo'],
                    "orderNo": res[0]['orderNo']
                }
            ]
        }
        return self._make_request('post', 'out_warehouse_back', data, 'main', nocheck)

    @doc(i_return_outgoing_items_route)
    @BaseApi.timing_decorator
    def return_outgoing_items_route(self, nocheck=False):
        res = self.pc.inventory_outbound_orders_list_data()
        res_2 = self.pc.inventory_outbound_orders_list_data(data='a')
        data = {
            "returnMethod": "2",
            "logisticsOrder": self.jd,
            "returnTime": self.get_formatted_datetime(),
            "articlesList": [
                {
                    "articlesNo": res_2[0]['articlesNo'],
                    "orderNo": res[0]['orderNo']
                }
            ]
        }
        return self._make_request('post', 'out_warehouse_back', data, 'main', nocheck)

    @doc(i_outbound_sales_only_received)
    @BaseApi.timing_decorator
    def outbound_sales_only_received(self, nocheck=False):
        res = self.pc.inventory_outbound_orders_list_data()
        res_2 = self.pc.inventory_outbound_orders_list_data(data='a')
        res_3 = self.pc.inventory_list_data(i='3', j='18')
        data = {
            "saleType": "1",
            "clientId": INFO['main_sale_supplier_id'],
            "clientName": INFO['vice_sales_customer_name'],
            "status": "1",
            "accountNo": INFO['main_account_no'],
            "accountName": INFO['main_account_name'],
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res_3[0]['id'],
                    "articlesNo": res_2[0]['articlesNo'],
                    "articlesState": 18,
                    "salePrice": 11,
                    "platformOrderNo": self.serial,
                    "remark": "仅出库备注",
                    "saleSettlePrice": 11,
                    "outboundOrderNo": res[0]['orderNo']
                }
            ]
        }
        return self._make_request('post', 'out_warehouse_sell', data, 'main', nocheck)

    @doc(i_outbound_sales_only_uncollected)
    @BaseApi.timing_decorator
    def outbound_sales_only_uncollected(self, nocheck=False):
        res = self.pc.inventory_outbound_orders_list_data()
        res_2 = self.pc.inventory_outbound_orders_list_data(data='a')
        res_3 = self.pc.inventory_list_data(i='3', j='18')
        data = {
            "saleType": "1",
            "clientId": INFO['main_sale_supplier_id'],
            "clientName": INFO['vice_sales_customer_name'],
            "status": "2",
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res_3[0]['id'],
                    "articlesNo": res_2[0]['articlesNo'],
                    "articlesState": 18,
                    "salePrice": 120,
                    "platformOrderNo": self.serial,
                    "remark": "备注1",
                    "saleSettlePrice": 120,
                    "outboundOrderNo": res[0]['orderNo']
                }
            ]
        }
        return self._make_request('post', 'out_warehouse_sell', data, 'main', nocheck)

    @doc(i_create_an_outbound_only_order)
    @BaseApi.timing_decorator
    def create_an_outbound_only_order(self, nocheck=False):
        time = self.get_current_timestamp_ms()
        res = self.pc.inventory_list_data()
        data = {
            "saleTime": self.get_formatted_datetime(),
            "saleType": "4",
            "clientId": INFO['main_sale_supplier_id'],
            "clientName": INFO['vice_sales_customer_name'],
            "accountNo": INFO['main_account_no'],
            "accountName": INFO['main_account_name'],
            "userId": INFO['main_user_id'],
            "deliveryId": INFO['main_user_id'],
            "deliveryTime": self.get_formatted_datetime(),
            "status": 1,
            "logisticsOrder": self.jd,
            "logisticsNoPrice": 11,
            "remark": "备注",
            "isEexpress": "0",
            "offExpressage": "0",
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res[0]['id'],
                    "imei": res[0]['imei'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 3,
                    "salePrice": None,
                    "platformArticlesNo": res[0]['platformArticlesNo'],
                    "platformOrderNo": None,
                    "remark": "备注",
                    "finenessId": None,
                    "articlesInfoId": time,
                    "purchaseArticlesInfoDTO": {
                        "finenessId": None,
                        "id": time
                    },
                    "saleSettlePrice": ""
                }
            ]
        }
        return self._make_request('post', 'create_a_new_order', data, 'main', nocheck)


class InventoryPurchaseAndSellOutRequest(InitializeParams):
    """库存管理|出库管理|采购售后出库"""

    @doc(i_purchase_after_sales_warehouse)
    @BaseApi.timing_decorator
    def purchase_after_sales_warehouse(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='10')
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
        }
        return self._make_request('post', 'purchase_after_sales_warehouse', data, 'main', nocheck)


class InventoryReceiveItemRequest(InitializeParams):
    """库存管理|移交接收管理|接收物品"""

    @doc(i_item_acceptance_repair_status)
    def item_acceptance_repair_status(self, nocheck=False):
        res = self.pc.inventory_receive_items_data(i='6')
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'receive_item_receive', data, 'main', nocheck)

    @doc(i_inventory_receive_item_search_by_imei)
    @BaseApi.timing_decorator
    def inventory_receive_item_search_by_imei(self):
        res = self.pc.inventory_receive_items_data()
        imei = res[0]['imei']
        ParamCache.cache_object({"imei": imei}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesNo": imei,
            "articlesType": 1
        }
        return self._make_request('post', 'inventory_receive_items', data, 'main')

    @doc(i_inventory_receive_item_search_by_articles_type_id)
    @BaseApi.timing_decorator
    def inventory_receive_item_search_by_articles_type_id(self, articles_type_id):
        ParamCache.cache_object({"articlesType": articles_type_id}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesTypeId": articles_type_id,
        }
        return self._make_request('post', 'inventory_receive_items', data, 'main')

    @doc(i_inventory_receive_item_search_by_brand_id)
    @BaseApi.timing_decorator
    def inventory_receive_item_search_by_brand_id(self):
        ParamCache.cache_object({"brandName": '苹果'}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesTypeId": "1",
            "brandId": 1,
            "articlesType": 1
        }
        return self._make_request('post', 'inventory_receive_items', data, 'main')

    @doc(i_inventory_receive_item_search_by_model_name)
    @BaseApi.timing_decorator
    def inventory_receive_item_search_by_model_name(self):
        ParamCache.cache_object({"modelName": 'iPhone 16 Pro Max'}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesTypeId": "1",
            "brandId": 1,
            "modelId": 17569,
            "articlesType": 1
        }
        return self._make_request('post', 'inventory_receive_items', data, 'main')

    @doc(i_inventory_receive_item_search_by_articles_state)
    @BaseApi.timing_decorator
    def inventory_receive_item_search_by_articles_state(self, articles_state, articles_state_str):
        ParamCache.cache_object({"articlesStateStr": articles_state_str}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesState": articles_state,
            "articlesType": 1
        }
        return self._make_request('post', 'inventory_receive_items', data, 'main')

    @doc(i_inventory_receive_item_search_by_hand_over_person)
    @BaseApi.timing_decorator
    def inventory_receive_item_search_by_hand_over_person(self):
        ParamCache.cache_object({"operateName": INFO['customer_name']}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "distributorId": INFO['main_user_id'],
            "articlesType": 1
        }
        return self._make_request('post', 'inventory_receive_items', data, 'main')

    @doc(i_inventory_receive_item_search_by_receive_person)
    @BaseApi.timing_decorator
    def inventory_receive_item_search_by_receive_person(self):
        ParamCache.cache_object({"reUserName": INFO['special_account_name']}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "userId": INFO['special_user_id'],
            "articlesType": 1
        }
        return self._make_request('post', 'inventory_receive_items', data, 'main')

    @doc(i_inventory_receive_item_search_by_reason_type)
    @BaseApi.timing_decorator
    def inventory_receive_item_search_by_reason_type(self, reason_type):
        ParamCache.cache_object({"reasonType": reason_type}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "reasonType": reason_type,
            "articlesType": 1
        }
        return self._make_request('post', 'inventory_receive_items', data, 'main')

    @doc(i_inventory_receive_item_search_by_reason_time)
    @BaseApi.timing_decorator
    def inventory_receive_item_search_by_reason_time(self):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "erpStartTime": self.get_the_date(-1),
            "erpEndTime": self.get_the_date(),
            "articlesType": 1
        }
        return self._make_request('post', 'inventory_receive_items', data, 'main')

    @doc(i_inventory_receive_item_search_by_receive_order_no)
    @BaseApi.timing_decorator
    def inventory_receive_item_search_by_receive_order_no(self):
        res = self.pc.inventory_receive_items_data()
        order_no = res[0]['orderNo']
        ParamCache.cache_object({"orderNo": order_no}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "orderNo": order_no,
            "articlesType": 1
        }
        return self._make_request('post', 'inventory_receive_items', data, 'main')

    @doc(i_inventory_receive_order_no_search_by_imei)
    @BaseApi.timing_decorator
    def inventory_receive_order_no_search_by_imei(self):
        res = self.pc.inventory_receive_items_data(data='b')
        order_no = res[0]['orderNo']
        ParamCache.cache_object({"imei": res[0]['imei']}, 'practical.json')
        data = {
            "orderNo": order_no,
            "articlesType": 1
        }
        return self._make_request('post', 'receive_items', data, 'main')

    @doc(i_inventory_receive_order_no_search_by_order_no)
    @BaseApi.timing_decorator
    def inventory_receive_order_no_search_by_order_no(self):
        res = self.pc.inventory_receive_items_data(data='a')
        order_no = res[0]['orderNo']
        ParamCache.cache_object({"orderNo": order_no}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "orderNo": order_no,
            "articlesType": 1
        }
        return self._make_request('post', 'receive_items', data, 'main')

    @doc(i_inventory_receive_order_no_search_by_status)
    @BaseApi.timing_decorator
    def inventory_receive_order_no_search_by_status(self):
        ParamCache.cache_object({"status": 1}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "status": "1",
            "articlesType": 1
        }
        return self._make_request('post', 'receive_items', data, 'main')

    @doc(i_inventory_receive_order_no_search_by_reason_type)
    @BaseApi.timing_decorator
    def inventory_receive_order_no_search_by_reason_type(self, reason_type):
        ParamCache.cache_object({"reasonType": reason_type}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "reasonType": reason_type,
            "articlesType": 1
        }
        return self._make_request('post', 'receive_items', data, 'main')

    @doc(i_inventory_receive_order_no_search_by_distributor)
    @BaseApi.timing_decorator
    def inventory_receive_order_no_search_by_distributor(self):
        ParamCache.cache_object({"distributorId": INFO['main_user_id']}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "distributorId": INFO['main_user_id'],
            "articlesType": 1
        }
        return self._make_request('post', 'receive_items', data, 'main')

    @doc(i_inventory_receive_order_no_search_by_user_id)
    @BaseApi.timing_decorator
    def inventory_receive_order_no_search_by_user_id(self):
        ParamCache.cache_object({"receiveId": INFO['special_user_id']}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "userId": INFO['special_user_id'],
            "articlesType": 1
        }
        return self._make_request('post', 'receive_items', data, 'main')

    @doc(i_inventory_receive_order_no_search_by_date)
    @BaseApi.timing_decorator
    def inventory_receive_order_no_search_by_date(self):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "erpStartTime": self.get_the_date(),
            "erpEndTime": self.get_the_date(),
            "articlesType": 1
        }
        return self._make_request('post', 'receive_items', data, 'main')


class InventorySaleOutWarehouseRequest(InitializeParams):
    """库存管理|出库管理|销售出库"""

    def item_number(self, nocheck=False):
        res = self.pc.sell_items_for_sale_data()
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'set_articles_no', data, 'main', nocheck)

    @doc(i_sales_out_warehouse_received)
    def sales_out_warehouse_received(self, nocheck=False):
        time = self.get_current_timestamp_ms()
        res = self.pc.inventory_list_data(i='2', j='13')
        data = {
            "saleTime": self.get_formatted_datetime(),
            "saleType": "1",
            "clientId": INFO['main_sale_supplier_id'],
            "clientName": INFO['vice_sales_customer_name'],
            "accountNo": INFO['main_account_no'],
            "accountName": INFO['main_account_name'],
            "userId": INFO['main_user_id'],
            "deliveryId": INFO['main_user_id'],
            "deliveryTime": self.get_formatted_datetime(),
            "status": 1,
            "logisticsOrder": self.jd,
            "logisticsNoPrice": 10,
            "isEexpress": "0",
            "offExpressage": "0",
            "orderPayInfoList": [
                {
                    "accountNo": INFO['main_account_no'],
                    "voucherImg": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com//erp-imgfiles/%2Fepbox-erp/20250820/WIehcT%2B7sg/I4FjLToJM%2Bw%3D%3D.jpg",
                    "payPrice": 10,
                    "accountName": INFO['main_account_name'],
                }
            ],
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res[0]['id'],
                    "imei": res[0]['imei'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 13,
                    "salePrice": 10,
                    "platformArticlesNo": self.serial,
                    "platformOrderNo": self.serial,
                    "remark": self.serial,
                    "finenessId": 1,
                    "articlesInfoId": time,
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1,
                        "id": time
                    },
                    "saleSettlePrice": 10
                }
            ]
        }
        return self._make_request('post', 'item_inventory_sell', data, 'main', nocheck)

    @doc(i_sales_out_warehouse_not_received)
    def sales_out_warehouse_not_received(self, nocheck=False):
        time = self.get_current_timestamp_ms()
        res = self.pc.inventory_list_data(i='2', j='13')
        data = {
            "saleTime": self.get_formatted_datetime(),
            "saleType": "1",
            "clientId": INFO['main_sale_supplier_id'],
            "clientName": INFO['vice_sales_customer_name'],
            "accountNo": INFO['main_account_no'],
            "accountName": INFO['main_account_name'],
            "userId": INFO['main_user_id'],
            "deliveryId": INFO['main_user_id'],
            "deliveryTime": self.get_formatted_datetime(),
            "status": 2,
            "logisticsOrder": self.jd,
            "logisticsNoPrice": 10,
            "isEexpress": "0",
            "offExpressage": "0",
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res[0]['id'],
                    "imei": res[0]['imei'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 13,
                    "salePrice": 501,
                    "platformArticlesNo": self.serial,
                    "platformOrderNo": self.serial,
                    "remark": self.serial,
                    "finenessId": None,
                    "articlesInfoId": time,
                    "purchaseArticlesInfoDTO": {
                        "finenessId": None,
                        "id": time
                    },
                    "saleSettlePrice": 501
                }
            ]
        }
        return self._make_request('post', 'item_inventory_sell', data, 'main', nocheck)

    @doc(i_sales_out_warehouse_help_sell)
    def sales_out_warehouse_help_sell(self, nocheck=False):
        time = self.get_current_timestamp_ms()
        res = self.pc.inventory_list_data(data='a', i='2', j='13')
        res_2 = self.pc.help_sell_the_list_of_goods_data()
        data = {
            "saleTime": self.get_formatted_datetime(),
            "saleType": "1",
            "clientId": INFO['vice_help_sale_supplier_id'],
            "clientName": INFO['vice_help_sale_supplier_name'],
            "accountNo": INFO['vice_account_no'],
            "accountName": INFO['main_account_name'],
            "userId": INFO['vice_user_id'],
            "deliveryId": INFO['vice_user_id'],
            "deliveryTime": self.get_formatted_datetime(),
            "status": 1,
            "logisticsOrder": self.jd,
            "logisticsNoPrice": 11,
            "isEexpress": "0",
            "offExpressage": "0",
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res[0]['id'],
                    "imei": res_2[0]['imei'],
                    "articlesNo": res_2[0]['helpSellArticlesNo'],
                    "articlesState": 13,
                    "salePrice": 11,
                    "platformArticlesNo": self.serial,
                    "platformOrderNo": self.serial,
                    "remark": self.serial,
                    "finenessId": 1,
                    "articlesInfoId": time,
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1,
                        "id": time
                    },
                    "saleSettlePrice": 11
                }
            ]
        }
        return self._make_request('post', 'item_inventory_sell', data, 'vice', nocheck)

    @doc(i_sell_distribution)
    def sell_distribution(self, nocheck=False):
        self.item_number()
        time = self.get_current_timestamp_ms()
        res = self.pc.inventory_list_data(i='2', j='13')
        data = {
            "saleTime": self.get_formatted_datetime(),
            "saleType": "3",
            "clientId": INFO['main_sale_supplier_id'],
            "clientName": INFO['vice_sales_customer_name'],
            "accountNo": INFO['main_account_no'],
            "accountName": INFO['main_account_name'],
            "userId": INFO['main_user_id'],
            "deliveryId": INFO['main_user_id'],
            "deliveryTime": self.get_formatted_datetime(),
            "status": 1,
            "logisticsOrder": self.jd,
            "logisticsNoPrice": 11,
            "isEexpress": "0",
            "offExpressage": "0",
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res[0]['id'],
                    "imei": res[0]['imei'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 13,
                    "salePrice": 11,
                    "platformArticlesNo": self.serial,
                    "platformOrderNo": self.serial,
                    "remark": self.serial,
                    "finenessId": 1,
                    "articlesInfoId": time,
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1,
                        "id": time
                    },
                    "saleSettlePrice": ""
                }
            ]
        }
        return self._make_request('post', 'item_inventory_sell', data, 'main', nocheck)

    @doc(i_sell_advance_sale)
    def sell_advance_sale(self, nocheck=False):
        time = self.get_current_timestamp_ms()
        res = self.pc.inventory_list_data(i='2', j='13')
        data = {
            "saleTime": self.get_formatted_datetime(),
            "saleType": "5",
            "clientId": INFO['main_sale_supplier_id'],
            "clientName": INFO['vice_sales_customer_name'],
            "accountNo": INFO['main_account_no'],
            "accountName": INFO['main_account_name'],
            "userId": INFO['main_user_id'],
            "deliveryId": INFO['main_user_id'],
            "deliveryTime": self.get_formatted_datetime(),
            "status": 1,
            "logisticsOrder": self.jd,
            "logisticsNoPrice": 11,
            "isEexpress": "0",
            "offExpressage": "0",
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res[0]['id'],
                    "imei": res[0]['imei'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 3,
                    "salePrice": None,
                    "platformArticlesNo": self.serial,
                    "platformOrderNo": None,
                    "remark": "备注",
                    "finenessId": 1,
                    "articlesInfoId": time,
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1,
                        "id": time
                    },
                    "saleSettlePrice": ""
                }
            ]
        }
        return self._make_request('post', 'item_inventory_sell', data, 'main', nocheck)

    @doc(i_sell_outbound_accessories)
    def sell_outbound_accessories(self, nocheck=False):
        time = self.get_current_timestamp_ms()
        res = self.pc.inventory_list_data(i='2', j='13')
        res_2 = self.pc.attachment_inventory_list_data(i='2')
        data = {
            "saleTime": self.get_formatted_datetime(),
            "saleType": "1",
            "clientId": INFO['main_sale_supplier_id'],
            "clientName": INFO['vice_sales_customer_name'],
            "accountNo": INFO['main_account_no'],
            "accountName": INFO['main_account_name'],
            "userId": INFO['main_user_id'],
            "deliveryId": INFO['main_user_id'],
            "deliveryTime": self.get_formatted_datetime(),
            "status": 2,
            "logisticsOrder": self.jd,
            "logisticsNoPrice": 11,
            "isEexpress": "0",
            "offExpressage": "0",
            "giveAccessoryArticlesNoList": [
                res_2[0]['articlesNo']
            ],
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res[0]['id'],
                    "imei": res[0]['imei'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 3,
                    "salePrice": 100,
                    "platformArticlesNo": self.serial,
                    "platformOrderNo": self.serial,
                    "remark": "备注",
                    "finenessId": 1,
                    "articlesInfoId": time,
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1,
                        "id": time
                    },
                    "saleSettlePrice": 100
                }
            ]
        }
        return self._make_request('post', 'item_inventory_sell', data, 'main', nocheck)


class InventorySellAfterSaleDeliveryRequest(InitializeParams):
    """库存管理|出库管理|销售售后出库"""

    @BaseApi.timing_decorator
    def item_number(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='15')
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'set_articles_no', data, 'main', nocheck)

    @doc(i_sell_get_out)
    @BaseApi.timing_decorator
    def sell_get_out(self, nocheck=False):
        self.item_number()
        res = self.pc.inventory_list_data(i='2', j='15')
        res_2 = self.pc.inventory_list_data(i='2', j='3')
        data = {
            "saleUserId": INFO['main_sale_supplier_id'],
            "offExpressage": "0",
            "logisticsNo": self.jd,
            "logisticsPrice": "11",
            "saleType": "7",
            "purchaseOrdersArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "remark": self.serial,
                    "saleSettlePrice": res[0]['totalRevenue']
                }
            ],
            "newPurchaseOrdersArticlesDTO": {
                "articlesNo": res_2[0]['articlesNo'],
                "imei": res_2[0]['imei'],
                "newSalePrice": 11,
                "platformArticlesNo": res_2[0]['platformArticlesNo'],
                "platformOrderNo": self.serial,
                "remark": self.serial,
                "costPrice": res_2[0]['sumCost']
            },
            "isSaleType": True
        }
        return self._make_request('post', 'sell_after_sale_out_stock', data, 'main', nocheck)

    @doc(i_sell_after_sale_refusal_return)
    @BaseApi.timing_decorator
    def sell_after_sale_refusal_return(self, nocheck=False):
        self.item_number()
        res = self.pc.inventory_list_data(i='2', j='15')
        data = {
            "saleUserId": INFO['main_sale_supplier_id'],
            "logisticsNo": self.jd,
            "logisticsPrice": "11",
            "saleType": "6",
            "purchaseOrdersArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "remark": None,
                    "saleSettlePrice": 40
                }
            ],
            "newPurchaseOrdersArticlesDTO": {
                "articlesNo": "",
                "imei": "",
                "newSalePrice": "",
                "platformArticlesNo": "",
                "platformOrderNo": "",
                "remark": "",
                "costPrice": 0
            },
            "isSaleType": True
        }
        return self._make_request('post', 'sell_after_sale_out_stock', data, 'main', nocheck)

    @doc(i_sell_after_sale_repair)
    @BaseApi.timing_decorator
    def sell_after_sale_repair(self, nocheck=False):
        self.item_number()
        res = self.pc.inventory_list_data(i='2', j='15')
        data = {
            "logisticsNo": self.jd,
            "logisticsPrice": "40",
            "saleUserId": INFO['main_sale_supplier_id'],
            "saleType": "3",
            "purchaseOrdersArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "remark": None,
                    "saleSettlePrice": 42
                }
            ],
            "newPurchaseOrdersArticlesDTO": {
                "articlesNo": "",
                "imei": "",
                "newSalePrice": "",
                "platformArticlesNo": "",
                "platformOrderNo": "",
                "remark": "",
                "costPrice": 0
            },
            "isSaleType": True
        }
        return self._make_request('post', 'sell_after_sale_out_stock', data, 'main', nocheck)


class InventorySendOutRepairRequest(InitializeParams):
    """库存管理|出库管理|送修出库"""

    @doc(i_send_out_the_warehouse)
    @BaseApi.timing_decorator
    def send_out_the_warehouse(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='16')
        data = {
            "saleState": 13,
            "offExpressage": "0",
            "logisticsNoPrice": 11,
            "logisticsNo": self.sf,
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "purchaseOrdersArticlesDTOList": [
                {
                    "purchaseNo": res[0]['purchaseNo'],
                    "articlesNo": res[0]['articlesNo'],
                    "id": res[0]['id'],
                    "purchasePrice": res[0]['purchasePrice'],
                    "saleRemake": "备注",
                    "imei": res[0]['imei'],
                    "articlesType": 1,
                    "platformArticlesNo": res[0]['platformArticlesNo'],
                    "articlesTypeId": 1,
                    "articlesTypeName": res[0]['articlesTypeName']
                }
            ],
            "deliveryTime": self.get_formatted_datetime(),
        }
        return self._make_request('post', 'send_out_the_warehouse', data, 'main', nocheck)


class InventoryStockCountRequest(InitializeParams):
    """库存管理|库存盘点"""

    @doc(i_completed_inventory_count)
    @BaseApi.timing_decorator
    def add_inventory_count(self, nocheck=False):
        data = {
            "stockUserId": INFO['main_user_id']
        }
        return self._make_request('post', 'add_inventory_count', data, 'main', nocheck)

    @doc(i_completed_inventory_count)
    @BaseApi.timing_decorator
    def submit_inventory_count(self, nocheck=False):
        res = self.pc.inventory_count_data()
        res_2 = self.pc.inventory_list_data(i=2)
        data = {
            "stockNo": res[0]['stockNo'],
            "articlesNoList": [
                res_2[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'submit_inventory_count', data, 'main', nocheck)

    @doc(i_completed_inventory_count)
    @BaseApi.timing_decorator
    def completed_inventory_count(self, nocheck=False):
        self.add_inventory_count()
        self.submit_inventory_count()
        res = self.pc.inventory_count_data()
        data = {
            "stockNo": res[0]['stockNo'],
            "remark": "备注"
        }
        return self._make_request('post', 'completed_inventory_count', data, 'main', nocheck)


class InventoryStoreTransferRequest(InitializeParams):
    """库存管理|库存调拨"""

    @doc(i_new_allocation)
    @BaseApi.timing_decorator
    def new_allocation(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='3')
        data = {
            "outWarehouseId": INFO['main_item_warehouse_id'],
            "inWarehouseId": INFO['main_item_in_warehouse_id'],
            "remark": "备注",
            "articlesType": "1",
            "articles": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei']
                }
            ],
            "expressInfo": {
                "walletAccountNo": INFO['main_wallet_account_no'],
                "isEexpress": 0,
                "estimateFreight": None,
                "expressNo": self.jd
            }
        }
        return self._make_request('post', 'item_new_allocation', data, 'main', nocheck)

    @doc(i_receive)
    @BaseApi.timing_decorator
    def receive(self, nocheck=False):
        res = self.pc.inventory_warehouse_allocation_data()
        res_2 = self.pc.inventory_warehouse_allocation_data(data='a')
        data = {
            "id": res[0]['id'],
            "quickOperation": 0,
            "purchaseOrdersArticlesDTO": {
                "articlesNoList": [
                    res_2['itemList'][0]['articlesNo']
                ],
                "userId": None,
                "type": None,
                "remark": None
            }
        }
        return self._make_request('post', 'item_allocation_receive', data, 'main', nocheck)

    @doc(i_cancel)
    @BaseApi.timing_decorator
    def cancel(self, nocheck=False):
        res = self.pc.inventory_warehouse_allocation_data()
        res_2 = self.pc.inventory_warehouse_allocation_data(data='a')
        data = {
            "id": res[0]['id'],
            "articlesNoList": [
                res_2['itemList'][0]['articlesNo']
            ]
        }
        return self._make_request('post', 'item_allocation_revoke', data, 'main', nocheck)


if __name__ == '__main__':
    api = InventoryListRequest()
    result = api.inventory_transfer_purchase_special()
    print(json.dumps(result, indent=4, ensure_ascii=False))
