# coding: utf-8
import json
from common.base_api import BaseApi
from common.base_params import InitializeParams, is_performance_close
from common.file_cache_manager import ParamCache
from common.import_desc import *
from config.user_info import INFO


class AttachmentGoodsReceivedRequest(InitializeParams):
    """配件管理|入库管理|待接收物品"""

    @doc(a_goods_received)
    @BaseApi.timing_decorator
    def goods_received(self, nocheck=False):
        res = (self.pc.attachment_goods_received_data()
               if is_performance_close else self.get_list_data('list_of_items_to_be_received'))
        data = {
            "accessoryList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "oao": "123"
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'accessory_receive_items', data, 'special', nocheck)

    @doc(a_goods_received_search_item)
    @BaseApi.timing_decorator
    def goods_received_search_item(self, nocheck=False):
        res = self.pc.attachment_goods_received_data()
        obj = res[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesNo": obj
        }
        self.validate_request_data(data)
        return self._make_request('post', 'items_to_be_received', data, 'special', nocheck)

    @doc(a_goods_received_search_time)
    @BaseApi.timing_decorator
    def goods_received_search_time(self, nocheck=False):
        res = self.pc.attachment_goods_received_data()
        obj = res[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "deliveryStartTime": self.get_the_date(),
            "deliveryEndTime": self.get_the_date(days=1),
        }
        self.validate_request_data(data)
        return self._make_request('post', 'items_to_be_received', data, 'special', nocheck)


class AttachmentHandOverItemsRequest(InitializeParams):
    """配件管理|移交接收管理|移交物品"""

    @doc(a_hand_over_items_to_inventory)
    @BaseApi.timing_decorator
    def hand_over_items_to_inventory(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data(i=2)
        data = {
            "accessoryList": [
                {
                    "articlesNo": res[0]['articlesNo']
                }
            ],
            "deliveryType": "6",
            "userId": INFO['main_user_id'],
            "deliveryRemark": "备注"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'inventory_transfer', data, 'main', nocheck)

    @doc(a_hand_over_items_to_purchase)
    @BaseApi.timing_decorator
    def hand_over_items_to_purchase(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data(i=2)
        data = {
            "accessoryList": [
                {
                    "articlesNo": res[0]['articlesNo']
                }
            ],
            "deliveryType": "5",
            "userId": INFO['main_user_id'],
            "deliveryRemark": "备注"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'inventory_transfer', data, 'main', nocheck)

    @doc(a_hand_over_items_to_sell)
    @BaseApi.timing_decorator
    def hand_over_items_to_sell(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data(i=2)
        data = {
            "accessoryList": [
                {
                    "articlesNo": res[0]['articlesNo']
                }
            ],
            "deliveryType": "4",
            "userId": INFO['main_user_id'],
            "deliveryRemark": "备注"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'inventory_transfer', data, 'main', nocheck)

    @doc(a_hand_over_items_to_send)
    @BaseApi.timing_decorator
    def hand_over_items_to_send(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data(i=2)
        data = {
            "accessoryList": [
                {
                    "articlesNo": res[0]['articlesNo']
                }
            ],
            "deliveryType": "3",
            "userId": INFO['main_user_id'],
            "deliveryRemark": "备注"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'inventory_transfer', data, 'main', nocheck)

    @doc(a_hand_over_items_to_repair)
    @BaseApi.timing_decorator
    def hand_over_items_to_repair(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data(i=2)
        data = {
            "accessoryList": [
                {
                    "articlesNo": res[0]['articlesNo']
                }
            ],
            "deliveryType": "2",
            "userId": INFO['main_user_id'],
            "deliveryRemark": "备注"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'inventory_transfer', data, 'main', nocheck)

    @doc(a_hand_over_items_to_quality)
    @BaseApi.timing_decorator
    def hand_over_items_to_quality(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data(i=2)
        data = {
            "accessoryList": [
                {
                    "articlesNo": res[0]['articlesNo']
                }
            ],
            "deliveryType": "1",
            "userId": INFO['main_user_id'],
            "deliveryRemark": "备注"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'inventory_transfer', data, 'main', nocheck)

    @doc(a_hand_over_different_recipients)
    @BaseApi.timing_decorator
    def hand_over_different_recipients(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data(i=2)
        data = {
            "accessoryList": [
                {
                    "articlesNo": res[0]['articlesNo']
                }
            ],
            "deliveryType": "1",
            "userId": INFO['special_user_id'],
            "deliveryRemark": "备注"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'inventory_transfer', data, 'main', nocheck)

    @doc(a_hand_over_items_search_item)
    @BaseApi.timing_decorator
    def hand_over_items_search_item(self, nocheck=False):
        res = self.pc.attachment_goods_received_data()
        obj = res[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj})
        data = {
            "articlesNo": obj
        }
        self.validate_request_data(data)
        return self._make_request('post', 'accessories_search_items', data, 'main', nocheck)


class AttachmentHandOverRecordsRequest(InitializeParams):
    """配件管理|移交接收管理|移交记录"""

    @doc(a_bulk_cancel_handovers)
    @BaseApi.timing_decorator
    def bulk_cancel_handovers(self, nocheck=False):
        res = self.pc.attachment_handover_records_data(data='a')
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'bulk_cancel_handovers', data, 'main', nocheck)

    @doc(a_hand_over_items_search_item_no)
    @BaseApi.timing_decorator
    def hand_over_items_search_item_no(self, nocheck=False):
        res = self.pc.attachment_handover_records_data(data='a')
        obj = res[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesNo": obj,
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'handover_records', data, 'main', nocheck)

    @doc(a_hand_over_items_search_order)
    @BaseApi.timing_decorator
    def hand_over_items_search_order(self, nocheck=False):
        res = self.pc.attachment_handover_records_data()
        obj = res[0]['orderNo']
        ParamCache.cache_object({"orderNo": obj})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "orderNo": obj,
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'handover_records', data, 'main', nocheck)

    @doc(a_hand_over_items_search_name)
    @BaseApi.timing_decorator
    def hand_over_items_search_name(self, nocheck=False):
        res = self.pc.attachment_handover_records_data()
        ParamCache.cache_object({"orderNo": res[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "distributorId": INFO['main_user_id'],
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'handover_records', data, 'main', nocheck)

    @doc(a_hand_over_items_search_receive)
    @BaseApi.timing_decorator
    def hand_over_items_search_receive(self, nocheck=False):
        res = self.pc.attachment_handover_records_data()
        ParamCache.cache_object({"orderNo": res[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "userId": INFO['special_user_id'],
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'handover_records', data, 'main', nocheck)

    @doc(a_hand_over_items_search_time)
    @BaseApi.timing_decorator
    def hand_over_items_search_time(self, nocheck=False):
        res = self.pc.attachment_handover_records_data()
        ParamCache.cache_object({"orderNo": res[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "userId": INFO['special_user_id'],
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'handover_records', data, 'main', nocheck)

    @doc(a_hand_over_items_search_status)
    @BaseApi.timing_decorator
    def hand_over_items_search_status(self, nocheck=False, status=None):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "status": status,
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'handover_records', data, 'main', nocheck)


class AttachmentInventoryListRequest(InitializeParams):
    """配件管理|配件库存|库存列表"""

    @doc(a_item_details_modify_item_information)
    @BaseApi.timing_decorator
    def item_details_modify_item_information(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data(i=2)
        data = {
            "id": res[0]['id'],
            "articlesNo": res[0]['articlesNo'],
            "skuInfo": res[0]['skuInfo'],
            "accessoryType": 1,
            "channelType": 1,
            "baseAccessoryDTO": {
                "accessoryNo": "PJ0216",
                "accessoryName": "铁片",
                "brandId": 8,
                "modelId": 18107,
                "accessoryType": 1,
                "modelName": "Pura 80 Pro",
                "brandName": "华为"
            }
        }
        self.validate_request_data(data)
        return self._make_request('post', 'modify_the_sku_information', data, 'main', nocheck)

    @doc(a_transfer_items_special)
    @BaseApi.timing_decorator
    def transfer_items_special(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data(i=2)
        data = {
            "accessoryList": [
                {
                    "articlesNo": res[0]['articlesNo']
                }
            ],
            "deliveryType": 6,
            "userId": INFO['special_user_id'],
            "deliveryRemark": "备注"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'inventory_transfer', data, 'main', nocheck)

    @doc(a_handover_items_purchase_after_sales)
    @BaseApi.timing_decorator
    def handover_items_purchase_after_sales(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data(i=2)
        data = {
            "accessoryList": [
                {
                    "articlesNo": res[0]['articlesNo']
                }
            ],
            "deliveryType": 5,
            "userId": INFO['special_user_id'],
            "deliveryRemark": "备注"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'inventory_transfer', data, 'main', nocheck)

    @doc(a_handover_items_sell_personnel)
    @BaseApi.timing_decorator
    def handover_items_sell_personnel(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data(i=2)
        data = {
            "accessoryList": [
                {
                    "articlesNo": res[0]['articlesNo']
                }
            ],
            "deliveryType": 4,
            "userId": INFO['special_user_id'],
            "deliveryRemark": "备注"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'inventory_transfer', data, 'main', nocheck)

    @doc(a_handover_items_send_personnel)
    @BaseApi.timing_decorator
    def handover_items_send_personnel(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data(i=2)
        data = {
            "accessoryList": [
                {
                    "articlesNo": res[0]['articlesNo']
                }
            ],
            "deliveryType": 3,
            "userId": INFO['special_user_id'],
            "deliveryRemark": "备注"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'inventory_transfer', data, 'main', nocheck)

    @doc(a_handover_items_repair_personnel)
    @BaseApi.timing_decorator
    def handover_items_repair_personnel(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data(i=2)
        data = {
            "accessoryList": [
                {
                    "articlesNo": res[0]['articlesNo']
                }
            ],
            "deliveryType": 2,
            "userId": INFO['special_user_id'],
            "deliveryRemark": "备注"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'inventory_transfer', data, 'main', nocheck)

    @doc(a_handover_items_quality_personnel)
    @BaseApi.timing_decorator
    def handover_items_quality_personnel(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data(i=2)
        data = {
            "accessoryList": [
                {
                    "articlesNo": res[0]['articlesNo']
                }
            ],
            "deliveryType": 1,
            "userId": INFO['special_user_id'],
            "deliveryRemark": "备注"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'inventory_transfer', data, 'main', nocheck)

    @doc(a_list_edit_item_info)
    @BaseApi.timing_decorator
    def list_edit_item_info(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data(i=2)
        data = {
            "id": res[0]['id'],
            "articlesNo": res[0]['articlesNo'],
            "skuInfo": res[0]['skuInfo'],
            "accessoryType": 1,
            "channelType": 1,
            "baseAccessoryDTO": {
                "accessoryNo": "PJ0216",
                "accessoryName": "铁片",
                "brandId": 8,
                "modelId": 18111,
                "accessoryType": 1,
                "modelName": "Hi MatePad 11.5寸 2024款 柔光版",
                "brandName": "华为"
            }
        }
        self.validate_request_data(data)
        return self._make_request('post', 'modify_the_sku_information', data, 'main', nocheck)

    @doc(a_attachment_inventory_list_search_item)
    @BaseApi.timing_decorator
    def attachment_inventory_list_search_item(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data()
        obj = res[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesNo": obj
        }
        self.validate_request_data(data)
        return self._make_request('post', 'inventory_list', data, 'main', nocheck)

    @doc(a_attachment_inventory_list_search_suppliers)
    @BaseApi.timing_decorator
    def attachment_inventory_list_search_suppliers(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data()
        ParamCache.cache_object({"articlesNo": res[0]['articlesNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "supplierId": INFO['main_supplier_id']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'inventory_list', data, 'main', nocheck)

    @doc(a_attachment_inventory_list_search_affiliation)
    @BaseApi.timing_decorator
    def attachment_inventory_list_search_affiliation(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data()
        ParamCache.cache_object({"articlesNo": res[0]['articlesNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "userId": INFO['main_user_id']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'inventory_list', data, 'main', nocheck)

    @doc(a_attachment_inventory_list_search_order_no)
    @BaseApi.timing_decorator
    def attachment_inventory_list_search_order_no(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data()
        obj = res[0]['purchaseNo']
        ParamCache.cache_object({"purchaseNo": obj})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "purchaseNo": obj
        }
        self.validate_request_data(data)
        return self._make_request('post', 'inventory_list', data, 'main', nocheck)

    @doc(a_attachment_inventory_list_search_purchaser)
    @BaseApi.timing_decorator
    def attachment_inventory_list_search_purchaser(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data()
        ParamCache.cache_object({"purchaseNo": res[0]['purchaseNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "purchaseId": ['main_user_id']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'inventory_list', data, 'main', nocheck)

    @doc(a_attachment_inventory_list_search_time)
    @BaseApi.timing_decorator
    def attachment_inventory_list_search_time(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data()
        ParamCache.cache_object({"purchaseNo": res[0]['purchaseNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "purchaseEndTime": self.get_the_date(),
            "purchaseStartTime": self.get_the_date(days=1)
        }
        self.validate_request_data(data)
        return self._make_request('post', 'inventory_list', data, 'main', nocheck)

    @doc(a_attachment_inventory_list_search_class)
    @BaseApi.timing_decorator
    def attachment_inventory_list_search_class(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data()
        ParamCache.cache_object({"articlesNo": res[0]['articlesNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "accessoryType": 2,
        }
        self.validate_request_data(data)
        return self._make_request('post', 'inventory_list', data, 'main', nocheck)

    @doc(a_attachment_inventory_list_search_status)
    @BaseApi.timing_decorator
    def attachment_inventory_list_search_status(self, nocheck=False, status=None):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "inventoryStatus": status,
        }
        self.validate_request_data(data)
        return self._make_request('post', 'inventory_list', data, 'main', nocheck)

    @doc(a_attachment_inventory_list_search_category)
    @BaseApi.timing_decorator
    def attachment_inventory_list_search_category(self, nocheck=False, type_id=None):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesTypeId": type_id,
        }
        self.validate_request_data(data)
        return self._make_request('post', 'inventory_list', data, 'main', nocheck)

    @doc(a_attachment_inventory_list_search_color)
    @BaseApi.timing_decorator
    def attachment_inventory_list_search_color(self, nocheck=False, color=None):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "accessoryQuality": color,
        }
        self.validate_request_data(data)
        return self._make_request('post', 'inventory_list', data, 'main', nocheck)

    @doc(a_attachment_inventory_list_search_serial_number)
    @BaseApi.timing_decorator
    def attachment_inventory_list_search_serial_number(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data()
        obj = res[0]['accessoryNo']
        ParamCache.cache_object({"accessoryNo": obj})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "accessoryNo": obj,
        }
        self.validate_request_data(data)
        return self._make_request('post', 'inventory_list', data, 'main', nocheck)

    @doc(a_attachment_inventory_list_search_duration)
    @BaseApi.timing_decorator
    def attachment_inventory_list_search_duration(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data()
        ParamCache.cache_object({"articlesNo": res[0]['articlesNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "inventoryTime": 1,
        }
        self.validate_request_data(data)
        return self._make_request('post', 'inventory_list', data, 'main', nocheck)

    @doc(a_attachment_inventory_list_search_channel)
    @BaseApi.timing_decorator
    def attachment_inventory_list_search_channel(self, nocheck=False, channel=None):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "channelType": channel,
        }
        self.validate_request_data(data)
        return self._make_request('post', 'inventory_list', data, 'main', nocheck)

    @doc(a_attachment_inventory_list_search_brand_model)
    @BaseApi.timing_decorator
    def attachment_inventory_list_search_brand_model(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data()
        ParamCache.cache_object({"articlesNo": res[0]['articlesNo']})
        data = {
            "pageSize": 10,
            "pageNum": 1,
            "articlesTypeId": "1",
            "brandId": 8,
            "modelId": 18111
        }
        self.validate_request_data(data)
        return self._make_request('post', 'inventory_list', data, 'main', nocheck)

    @doc(a_attachment_inventory_list_search_warehouse)
    @BaseApi.timing_decorator
    def attachment_inventory_list_search_warehouse(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data()
        ParamCache.cache_object({"articlesNo": res[0]['articlesNo']})
        data = {
            "pageSize": 10,
            "pageNum": 1,
            "warehouseId": INFO['main_warehouse_id']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'inventory_list', data, 'main', nocheck)

    @doc(a_attachment_inventory_list_search_accessory_name)
    @BaseApi.timing_decorator
    def attachment_inventory_list_search_accessory_name(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data()
        obj = res[0]['accessoryName']
        ParamCache.cache_object({"articlesNo": obj})
        data = {
            "pageSize": 10,
            "pageNum": 1,
            "accessoryName": obj
        }
        self.validate_request_data(data)
        return self._make_request('post', 'inventory_list', data, 'main', nocheck)

    @doc(a_accessory_sales_express_delivery)
    @BaseApi.timing_decorator
    def accessory_sales_express_delivery(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data(i=2)
        data = {
            "status": "1",
            "accountNo": INFO['main_account_no'],
            "isEexpress": "1",
            "logisticsNoPrice": 10,
            "saleSupplierId": INFO['main_sale_supplier_id'],
            "supplierName": INFO['vice_sales_customer_name'],
            "walletAccountNo": INFO['main_wallet_account_no'],
            "payWay": 1,
            "pickUpType": 1,
            "remark": "备注",
            "logisticsCompanyType": 1,
            "userAddressId": INFO['main_user_address_id'],
            "saleOrderAccessoryList": [
                {
                    "accessoryNo": res[0]['articlesNo'],
                    "accessoryId": res[0]['id'],
                    "salePrice": "123",
                    "costPrice": res[0]['totalCost']
                }
            ],
            "deliveryNum": 1,
            "accountName": INFO['main_account_name']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'accessory_sales', data, 'main', nocheck)

    @doc(a_accessory_sales)
    @BaseApi.timing_decorator
    def accessory_sales(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data(i=2)
        data = {
            "status": "2",
            "accountNo": INFO['main_account_no'],
            "isEexpress": "0",
            "logisticsNo": self.jd,
            "logisticsNoPrice": "10",
            "saleSupplierId": INFO['main_sale_supplier_id'],
            "supplierName": INFO['vice_sales_customer_name'],
            "remark": "备注",
            "saleOrderAccessoryList": [
                {
                    "accessoryNo": res[0]['articlesNo'],
                    "accessoryId": res[0]['id'],
                    "salePrice": "70",
                    "costPrice": res[0]['totalCost']
                }
            ],
            "deliveryNum": 1,
            "accountName": INFO['main_account_name']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'accessory_sales', data, 'main', nocheck)


class AttachmentMaintenanceRequest(InitializeParams):
    """配件管理|配件维护"""

    @doc(a_added_a_button_category_external_category)
    @BaseApi.timing_decorator
    def added_a_button_category_external_category(self, nocheck=False):
        data = {
            "accessoryName": "配件名称" + self.imei,
            "accessoryType": "3",
            "status": 1
        }
        self.validate_request_data(data)
        return self._make_request('post', 'new_maintenance', data, 'idle', nocheck)

    @doc(a_added_a_button_category_matching)
    @BaseApi.timing_decorator
    def added_a_button_category_matching(self, nocheck=False):
        data = {
            "accessoryName": "配件名称" + self.imei,
            "accessoryType": "2",
            "status": 0
        }
        self.validate_request_data(data)
        return self._make_request('post', 'new_maintenance', data, 'idle', nocheck)

    @doc(a_modify_the_accessory_name)
    @BaseApi.timing_decorator
    def modify_the_accessory_name(self, nocheck=False):
        res = self.pc.attachment_maintenance_data()
        data = {
            "createBy": "杰克",
            "createTime": res[0]['createTime'],
            "pageSize": 10,
            "pageNum": 1,
            "orderByColumn": "create_time",
            "isAsc": "desc",
            "id": res[0]['id'],
            "accessoryNo": "PJ0352",
            "accessoryName": "名称I01779513423562",
            "accessoryType": "3",
            "price": 0,
            "status": 1,
            "tenantId": 573448,
            "isDelete": 0
        }
        self.validate_request_data(data)
        return self._make_request('put', 'modify_the_accessory_name', data, 'idle', nocheck)

    @doc(a_delete_the_accessory_name)
    @BaseApi.timing_decorator
    def delete_the_accessory_name(self, nocheck=False):
        res = self.pc.attachment_maintenance_data()
        data = {
            "id": res[0]['id']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'delete_the_accessory_name', data, 'idle', nocheck)

    @doc(a_attachment_maintenance_search_num)
    @BaseApi.timing_decorator
    def attachment_maintenance_search_num(self, nocheck=False):
        res = self.pc.attachment_maintenance_data()
        obj = res[0]['accessoryNo']
        ParamCache.cache_object({"accessoryNo": obj})
        data = {
            "accessoryNo": obj,
            "pageSize": 10,
            "pageNum": 1
        }
        self.validate_request_data(data)
        return self._make_request('post', 'maintenance_list', data, 'idle', nocheck)

    @doc(a_attachment_maintenance_search_name)
    @BaseApi.timing_decorator
    def attachment_maintenance_search_name(self, nocheck=False):
        res = self.pc.attachment_maintenance_data()
        obj = res[0]['accessoryName']
        ParamCache.cache_object({"accessoryName": obj})
        data = {
            "accessoryName": obj,
            "pageSize": 10,
            "pageNum": 1
        }
        self.validate_request_data(data)
        return self._make_request('post', 'maintenance_list', data, 'idle', nocheck)

    @doc(a_attachment_maintenance_search_status)
    @BaseApi.timing_decorator
    def attachment_maintenance_search_status(self, nocheck=False, status=None):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "status": status,
        }
        self.validate_request_data(data)
        return self._make_request('post', 'maintenance_list', data, 'main', nocheck)


class AttachmentOldWarehouseRequest(InitializeParams):
    """配件管理|入库管理|旧配件入库"""

    @doc(a_phone_old_attachment_warehouse)
    @BaseApi.timing_decorator
    def phone_old_attachment_warehouse(self, nocheck=False):
        data = {
            "warehouseId": INFO['main_in_warehouse_id'],
            "userId": INFO['special_user_id'],
            "storageTime": self.get_formatted_datetime(),
            "remark": "备注",
            "warehouseName": INFO['main_in_warehouse_name'],
            "accessoryDTOList": [
                {
                    "accessoryNum": "1",
                    "purchasePrice": "12",
                    "accessoryType": "2",
                    "articlesTypeId": "1",
                    "channelType": "1",
                    "baseAccessoryDTO": {
                        "accessoryName": "SIA8109",
                        "accessoryType": "3",
                        "brandId": 1,
                        "brandName": "苹果",
                        "modelId": 7692,
                        "modelName": "iPhone 5S",
                        "accessoryNo": "PJ0211"
                    }
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'old_create_purchase_order', data, 'main', nocheck)

    @doc(a_thousand_phone_old_attachment_warehouse)
    @BaseApi.timing_decorator
    def thousand_phone_old_attachment_warehouse(self, nocheck=False):
        data = {
            "warehouseId": INFO['main_in_warehouse_id'],
            "userId": INFO['special_user_id'],
            "storageTime": self.get_formatted_datetime(),
            "warehouseName": INFO['main_in_warehouse_name'],
            "accessoryDTOList": [
                {
                    "accessoryNum": "1000",
                    "purchasePrice": "345",
                    "accessoryType": "2",
                    "articlesTypeId": "1",
                    "channelType": "1",
                    "baseAccessoryDTO": {
                        "accessoryName": "铁片",
                        "accessoryType": "2",
                        "brandId": 1,
                        "brandName": "苹果",
                        "modelId": 7693,
                        "modelName": "iPhone 6",
                        "accessoryNo": "PJ0216"
                    }
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'old_create_purchase_order', data, 'main', nocheck)

    @doc(a_ipa_old_attachment_warehouse)
    @BaseApi.timing_decorator
    def ipa_old_attachment_warehouse(self, nocheck=False):
        data = {
            "warehouseId": INFO['main_in_warehouse_id'],
            "userId": INFO['special_user_id'],
            "storageTime": self.get_formatted_datetime(),
            "remark": "备注",
            "warehouseName": INFO['main_in_warehouse_name'],
            "accessoryDTOList": [
                {
                    "accessoryNum": "1",
                    "purchasePrice": "123",
                    "accessoryType": "2",
                    "articlesTypeId": "3",
                    "channelType": "1",
                    "baseAccessoryDTO": {
                        "accessoryName": "HI1102",
                        "accessoryType": "3",
                        "brandId": 802,
                        "brandName": "荣耀",
                        "modelId": 18031,
                        "modelName": "平板 10",
                        "accessoryNo": "PJ0171"
                    }
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'old_create_purchase_order', data, 'main', nocheck)

    @doc(a_notebook_old_attachment_warehouse)
    @BaseApi.timing_decorator
    def notebook_old_attachment_warehouse(self, nocheck=False):
        data = {
            "warehouseId": INFO['main_in_warehouse_id'],
            "userId": INFO['special_user_id'],
            "storageTime": self.get_formatted_datetime(),
            "remark": "备注",
            "warehouseName": INFO['main_in_warehouse_name'],
            "accessoryDTOList": [
                {
                    "accessoryNum": "1",
                    "purchasePrice": "12",
                    "accessoryType": "2",
                    "articlesTypeId": "4",
                    "channelType": "1",
                    "baseAccessoryDTO": {
                        "accessoryName": "HI1102",
                        "accessoryType": "3",
                        "brandId": 8,
                        "brandName": "华为",
                        "modelId": 15420,
                        "modelName": "MateBook X Pro 2018款",
                        "accessoryNo": "PJ0171"
                    }
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'old_create_purchase_order', data, 'main', nocheck)

    @doc(a_smartwatches_old_attachment_warehouse)
    @BaseApi.timing_decorator
    def smartwatches_old_attachment_warehouse(self, nocheck=False):
        data = {
            "warehouseId": INFO['main_in_warehouse_id'],
            "userId": INFO['special_user_id'],
            "storageTime": self.get_formatted_datetime(),
            "remark": "备注",
            "warehouseName": INFO['main_in_warehouse_name'],
            "accessoryDTOList": [
                {
                    "accessoryNum": "1",
                    "purchasePrice": "20",
                    "accessoryType": "2",
                    "articlesTypeId": "5",
                    "channelType": "1",
                    "baseAccessoryDTO": {
                        "accessoryName": "HI1102",
                        "accessoryType": "3",
                        "brandId": 802,
                        "brandName": "荣耀",
                        "modelId": 11923,
                        "modelName": "GS 3",
                        "accessoryNo": "PJ0171"
                    }
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'old_create_purchase_order', data, 'main', nocheck)

    @doc(a_attachment_old_warehouse_search_item)
    @BaseApi.timing_decorator
    def attachment_old_warehouse_search_item(self, nocheck=False):
        res = self.pc.attachment_old_warehouse_data(data='a')
        obj = res[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj})
        data = {
            "articlesNo": obj,
            "pageSize": 10,
            "pageNum": 1,
        }
        self.validate_request_data(data)
        return self._make_request('post', 'list_of_old_accessories', data, 'main', nocheck)

    @doc(a_attachment_old_warehouse_search_order)
    @BaseApi.timing_decorator
    def attachment_old_warehouse_search_order(self, nocheck=False):
        res = self.pc.attachment_old_warehouse_data()
        obj = res[0]['orderNo']
        ParamCache.cache_object({"orderNo": obj})
        data = {
            "orderNo": obj,
            "pageSize": 10,
            "pageNum": 1,
        }
        self.validate_request_data(data)
        return self._make_request('post', 'list_of_old_accessories', data, 'main', nocheck)

    @doc(a_attachment_old_warehouse_search_warehouse)
    @BaseApi.timing_decorator
    def attachment_old_warehouse_search_warehouse(self, nocheck=False):
        res = self.pc.attachment_old_warehouse_data()
        ParamCache.cache_object({"orderNo": res[0]['orderNo']})
        data = {
            "warehouseId": INFO['main_in_warehouse_id'],
            "pageSize": 10,
            "pageNum": 1,
        }
        self.validate_request_data(data)
        return self._make_request('post', 'list_of_old_accessories', data, 'main', nocheck)

    @doc(a_attachment_old_warehouse_search_user)
    @BaseApi.timing_decorator
    def attachment_old_warehouse_search_user(self, nocheck=False):
        res = self.pc.attachment_old_warehouse_data()
        ParamCache.cache_object({"orderNo": res[0]['orderNo']})
        data = {
            "userId": INFO['special_user_id'],
            "pageSize": 10,
            "pageNum": 1,
        }
        self.validate_request_data(data)
        return self._make_request('post', 'list_of_old_accessories', data, 'main', nocheck)

    @doc(a_attachment_old_warehouse_search_time)
    @BaseApi.timing_decorator
    def attachment_old_warehouse_search_time(self, nocheck=False):
        res = self.pc.attachment_old_warehouse_data()
        ParamCache.cache_object({"orderNo": res[0]['orderNo']})
        data = {
            "pageSize": 10,
            "pageNum": 1,
            "startTime": self.get_the_date(),
            "endTime": self.get_the_date(days=1),
        }
        self.validate_request_data(data)
        return self._make_request('post', 'list_of_old_accessories', data, 'main', nocheck)


class AttachmentPickListsRequest(InitializeParams):
    """配件管理|入库管理|分拣列表"""

    @doc(a_attachment_pick_lists_search_status)
    @BaseApi.timing_decorator
    def attachment_pick_lists_search_status(self, nocheck=False, status=None):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "sortationStatus": status,
        }
        self.validate_request_data(data)
        return self._make_request('post', 'sorting_list', data, 'main', nocheck)

    @doc(a_attachment_pick_lists_search_logistics)
    @BaseApi.timing_decorator
    def attachment_pick_lists_search_logistics(self, nocheck=False):
        res = self.pc.attachment_sorting_list_data()
        obj = res[0]['logisticsNo']
        ParamCache.cache_object({"logisticsNo": obj})
        data = {
            "pageSize": 10,
            "pageNum": 1,
            "logisticsNo": obj,
        }
        self.validate_request_data(data)
        return self._make_request('post', 'sorting_list', data, 'main', nocheck)

    @doc(a_attachment_pick_lists_search_item)
    @BaseApi.timing_decorator
    def attachment_pick_lists_search_item(self, nocheck=False):
        res = self.pc.attachment_new_arrival_data()
        obj = res[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj})
        data = {
            "pageSize": 10,
            "pageNum": 1,
            "articlesNo": obj,
        }
        self.validate_request_data(data)
        return self._make_request('post', 'sorting_list', data, 'main', nocheck)

    @doc(a_attachment_pick_lists_search_business)
    @BaseApi.timing_decorator
    def attachment_pick_lists_search_business(self, nocheck=False):
        res = self.pc.attachment_new_arrival_data()
        obj = res[0]['businessNo']
        ParamCache.cache_object({"businessNo": obj})
        data = {
            "pageSize": 10,
            "pageNum": 1,
            "businessNo": obj,
        }
        self.validate_request_data(data)
        return self._make_request('post', 'sorting_list', data, 'main', nocheck)

    @doc(a_attachment_pick_lists_search_time)
    @BaseApi.timing_decorator
    def attachment_pick_lists_search_time(self, nocheck=False):
        res = self.pc.attachment_sorting_list_data()
        obj = res[0]['logisticsNo']
        ParamCache.cache_object({"logisticsNo": obj})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "sortationStartTime": self.get_the_date(),
            "sortationEndTime": self.get_the_date(days=1),
        }
        self.validate_request_data(data)
        return self._make_request('post', 'sorting_list', data, 'main', nocheck)


class AttachmentPurchaseAddRequest(InitializeParams):
    """配件管理|配件采购|新增采购单"""

    @doc(a_added_purchase_order_unpaid_in_transit)
    @BaseApi.timing_decorator
    def added_purchase_order_unpaid_in_transit(self, nocheck=False):
        data = {
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "state": "3",
            "logisticsNo": self.jd,
            "payState": "2",
            "accountNo": INFO['main_account_no'],
            "purchaseSource": "2",
            "logisticsPrice": 20,
            "userId": INFO['main_user_id'],
            "purchaseTime": self.get_formatted_datetime(),
            "remark": "备注",
            "accessoryDTOList": [
                {
                    "purchasePrice": "10",
                    "accessoryNum": "1",
                    "baseAccessoryDTO": {
                        "accessoryName": "OXO",
                        "accessoryType": "2",
                        "purchasePrice": "10",
                        "accessoryNo": "PJ0215",
                        "brandId": 802,
                        "brandName": "荣耀",
                        "modelId": 11402,
                        "modelName": "MagicBook 14 Pro 2023款",
                        "colorId": "",
                        "colorName": "",
                        "fineness": "1",
                        "channelType": "1",
                        "articlesTypeName": "配件",
                        "articlesRemake": "",
                        "articlesTypeId": "4"
                    },
                    "warehouseId": "",
                    "articlesTypeId": "4",
                    "accessoryType": "1",
                    "channelType": "1"
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'create_purchase_order', data, 'main', nocheck)

    @doc(a_new_purchase_order_warehousing)
    @BaseApi.timing_decorator
    def new_purchase_order_warehousing(self, nocheck=False):
        data = {
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "state": "4",
            "logisticsNo": self.jd,
            "payState": "2",
            "accountNo": INFO['main_account_no'],
            "purchaseSource": "2",
            "logisticsPrice": 10,
            "userId": INFO['main_user_id'],
            "purchaseTime": self.get_formatted_datetime(),
            "warehouseId": INFO['main_warehouse_id'],
            "remark": "备注",
            "accessoryDTOList": [
                {
                    "purchasePrice": "10",
                    "accessoryNum": "1",
                    "baseAccessoryDTO": {
                        "accessoryName": "铁片",
                        "accessoryType": "2",
                        "purchasePrice": "111",
                        "accessoryNo": "PJ0216",
                        "brandId": 8,
                        "brandName": "华为",
                        "modelId": 18111,
                        "modelName": "Pocket 2 优享版",
                        "colorId": "",
                        "colorName": "",
                        "fineness": "1",
                        "channelType": "1",
                        "articlesTypeName": "配件",
                        "articlesRemake": "",
                        "articlesTypeId": "1"
                    },
                    "warehouseId": INFO['main_warehouse_id'],
                    "articlesTypeId": "1",
                    "accessoryType": "1",
                    "channelType": "1"
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'create_purchase_order', data, 'main', nocheck)

    @doc(a_attachment_new_purchase_order_payment)
    @BaseApi.timing_decorator
    def attachment_new_purchase_order_payment(self, nocheck=False):
        data = {
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "state": "4",
            "payState": "1",
            "accountNo": INFO['main_account_no'],
            "purchaseSource": "2",
            "userId": INFO['main_user_id'],
            "purchaseTime": self.get_formatted_datetime(),
            "warehouseId": INFO['main_warehouse_id'],
            "remark": "备注",
            "accessoryDTOList": [
                {
                    "purchasePrice": "12214",
                    "accessoryNum": "1",
                    "baseAccessoryDTO": {
                        "accessoryName": "漏液屏",
                        "accessoryType": "3",
                        "purchasePrice": "12214",
                        "accessoryNo": "PJ0143",
                        "brandId": 27,
                        "brandName": "OPPO",
                        "modelId": 13372,
                        "modelName": "Watch 4 Pro",
                        "colorId": "",
                        "colorName": "",
                        "fineness": "1",
                        "channelType": "1",
                        "articlesTypeName": "配件",
                        "articlesRemake": "",
                        "articlesTypeId": "5"
                    },
                    "warehouseId": INFO['main_warehouse_id'],
                    "articlesTypeId": "3",
                    "accessoryType": "1",
                    "channelType": "1"
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'create_purchase_order', data, 'main', nocheck)

    @doc(a_new_purchase_order_route)
    @BaseApi.timing_decorator
    def new_purchase_order_route(self, nocheck=False):
        data = {
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "state": "3",
            "logisticsNo": self.jd,
            "payState": "1",
            "accountNo": INFO['main_account_no'],
            "purchaseSource": "2",
            "logisticsPrice": "11",
            "userId": INFO['main_user_id'],
            "purchaseTime": self.get_formatted_datetime(),
            "remark": "备注",
            "accessoryDTOList": [
                {
                    "purchasePrice": 77,
                    "accessoryNum": "1",
                    "baseAccessoryDTO": {
                        "accessoryName": "HI1102",
                        "accessoryType": "3",
                        "purchasePrice": "10",
                        "accessoryNo": "PJ0171",
                        "brandId": 802,
                        "brandName": "荣耀",
                        "modelId": 18031,
                        "modelName": "平板 10",
                        "colorId": "",
                        "colorName": "",
                        "fineness": "2",
                        "channelType": "2",
                        "articlesTypeName": "配件",
                        "articlesRemake": "",
                        "articlesTypeId": "3"
                    },
                    "warehouseId": "",
                    "articlesTypeId": "3",
                    "accessoryType": "2",
                    "channelType": "2"
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'create_purchase_order', data, 'main', nocheck)

    @doc(a_generate_purchase_orders_in_bulk)
    @BaseApi.timing_decorator
    def generate_purchase_orders_in_bulk(self, nocheck=False):
        data = {
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "state": "4",
            "logisticsNo": self.jd,
            "payState": "2",
            "accountNo": INFO['main_account_no'],
            "purchaseSource": "2",
            "logisticsPrice": 20,
            "userId": INFO['main_user_id'],
            "purchaseTime": self.get_formatted_datetime(),
            "remark": "备注",
            "accessoryDTOList": [
                {
                    "purchasePrice": "10",
                    "accessoryNum": "1000",
                    "baseAccessoryDTO": {
                        "accessoryName": "摄像头1",
                        "accessoryType": "2",
                        "purchasePrice": "121",
                        "accessoryNo": "PJ0217",
                        "brandId": 1,
                        "brandName": "苹果",
                        "modelId": 7692,
                        "modelName": "iPhone 5S",
                        "colorId": "",
                        "colorName": "",
                        "fineness": "2",
                        "channelType": "1",
                        "articlesTypeName": "配件",
                        "articlesRemake": "",
                        "articlesTypeId": "1"
                    },
                    "warehouseId": INFO['main_warehouse_id'],
                    "articlesTypeId": "1",
                    "accessoryType": "2",
                    "channelType": "1"
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'create_purchase_order', data, 'main', nocheck)

    @doc(a_add_purchase_orders_in_bulk)
    @BaseApi.timing_decorator
    def add_purchase_orders_in_bulk(self, nocheck=False):
        data = {
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "state": "3",
            "logisticsNo": self.jd,
            "payState": "2",
            "accountNo": INFO['main_account_no'],
            "purchaseSource": "2",
            "logisticsPrice": "11",
            "userId": INFO['main_user_id'],
            "purchaseTime": self.get_formatted_datetime(),
            "remark": "备注",
            "accessoryDTOList": [
                {
                    "purchasePrice": "1",
                    "accessoryNum": "1",
                    "baseAccessoryDTO": {
                        "accessoryName": "摄像头",
                        "accessoryType": "2",
                        "purchasePrice": "1",
                        "accessoryNo": "PJ0217",
                        "brandId": 1,
                        "brandName": "苹果",
                        "modelId": 7692,
                        "modelName": "iPhone 5S",
                        "colorId": "",
                        "colorName": "",
                        "fineness": "1",
                        "channelType": "1",
                        "articlesTypeName": "配件",
                        "articlesRemake": "",
                        "articlesTypeId": "1"
                    },
                    "warehouseId": "",
                    "articlesTypeId": "1",
                    "accessoryType": "1",
                    "channelType": "1"
                },
                {
                    "purchasePrice": "22",
                    "accessoryNum": "1",
                    "baseAccessoryDTO": {
                        "accessoryName": "摄像头",
                        "accessoryType": "2",
                        "purchasePrice": "22",
                        "accessoryNo": "PJ0217",
                        "brandId": 8,
                        "brandName": "华为",
                        "modelId": 18111,
                        "modelName": "Pocket 2 优享版",
                        "colorId": "",
                        "colorName": "",
                        "fineness": "1",
                        "channelType": "1",
                        "articlesTypeName": "配件",
                        "articlesRemake": "",
                        "articlesTypeId": "1"
                    },
                    "warehouseId": "",
                    "articlesTypeId": "1",
                    "accessoryType": "1",
                    "channelType": "1"
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'create_purchase_order', data, 'main', nocheck)


class AttachmentPurchaseListRequest(InitializeParams):
    """配件管理|配件采购|采购列表"""

    @doc(a_refund_after_purchase_express)
    @BaseApi.timing_decorator
    def refund_after_purchase_express(self, nocheck=False):
        res = self.pc.attachment_purchase_list_data(data='a')
        data = {
            "saleState": "1",
            "payState": "2",
            "offExpressage": "1",
            "logisticsNoPrice": 10,
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "remark": "备注",
            "walletAccountNo": INFO['main_wallet_account_no'],
            "payWay": 1,
            "pickUpType": 1,
            "logisticsCompanyType": 1,
            "userAddressId": INFO['main_user_address_id'],
            "purchaseAccessoryDTOList": [
                {
                    "purchasePrice": res[0]['purchasePrice'],
                    "purchaseNo": res[0]['purchaseNo'],
                    "newPurchasePrice": res[0]['returnAblePrice'],
                    "articlesNo": res[0]['articlesNo'],
                    "salePrice": 0,
                    "id": res[0]['id']
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'procurement_after_sales', data, 'main', nocheck)

    @doc(a_refund_after_purchase)
    @BaseApi.timing_decorator
    def refund_after_purchase(self, nocheck=False):
        res = self.pc.attachment_purchase_list_data(data='a')
        data = {
            "saleState": "1",
            "payState": "2",
            "offExpressage": "0",
            "logisticsOrder": self.jd,
            "logisticsNoPrice": "11",
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "remark": "备注",
            "walletAccountNo": INFO['main_wallet_account_no'],
            "purchaseAccessoryDTOList": [
                {
                    "purchasePrice": res[0]['purchasePrice'],
                    "purchaseNo": res[0]['purchaseNo'],
                    "newPurchasePrice": res[0]['returnAblePrice'],
                    "articlesNo": res[0]['articlesNo'],
                    "salePrice": 0,
                    "id": res[0]['id']
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'procurement_after_sales', data, 'main', nocheck)

    @doc(a_purchase_sale_refund)
    @BaseApi.timing_decorator
    def purchase_sale_refund(self, nocheck=False):
        res = self.pc.attachment_purchase_list_data(data='a')
        data = {
            "saleState": "7",
            "payState": "2",
            "offExpressage": 0,
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "remark": "备注",
            "purchaseAccessoryDTOList": [
                {
                    "purchasePrice": res[0]['purchasePrice'],
                    "purchaseNo": res[0]['purchaseNo'],
                    "newPurchasePrice": 1,
                    "articlesNo": res[0]['articlesNo'],
                    "salePrice": 0,
                    "id": res[0]['id']
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'procurement_after_sales', data, 'main', nocheck)

    @doc(a_all_amount_refund_difference)
    @BaseApi.timing_decorator
    def all_amount_refund_difference(self, nocheck=False):
        res = self.pc.attachment_purchase_list_data(data='a')
        data = {
            "saleState": "7",
            "payState": "2",
            "offExpressage": 0,
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "remark": "备注",
            "purchaseAccessoryDTOList": [
                {
                    "purchasePrice": res[0]['purchasePrice'],
                    "purchaseNo": res[0]['purchaseNo'],
                    "newPurchasePrice": res[0]['returnAblePrice'],
                    "articlesNo": res[0]['articlesNo'],
                    "salePrice": 0,
                    "id": res[0]['id']
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'procurement_after_sales', data, 'main', nocheck)

    @doc(a_details_of_the_spare_parts_purchase_list)
    @BaseApi.timing_decorator
    def details_of_the_spare_parts_purchase_list(self, nocheck=False):
        res = self.pc.attachment_purchase_list_data()
        res_2 = self.pc.attachment_purchase_list_data(data='a')
        ParamCache.cache_object({"articlesNo": res_2[0]['articlesNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "purchaseNo": res[0]['orderNo']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'purchase_detail', data, 'main', nocheck)

    @doc(a_attachment_purchase_list_search_order)
    @BaseApi.timing_decorator
    def attachment_purchase_list_search_order(self, nocheck=False):
        res = self.pc.attachment_purchase_list_data()
        obj = res[0]['orderNo']
        ParamCache.cache_object({"orderNo": obj})
        data = {
            "articlesType": 2,
            "pageNum": 1,
            "pageSize": 10,
            "orderNo": obj
        }
        self.validate_request_data(data)
        return self._make_request('post', 'purchase_list', data, 'main', nocheck)

    @doc(a_attachment_purchase_list_search_suppliers)
    @BaseApi.timing_decorator
    def attachment_purchase_list_search_suppliers(self, nocheck=False):
        res = self.pc.attachment_purchase_list_data()
        ParamCache.cache_object({"orderNo": res[0]['orderNo']})
        data = {
            "articlesType": 2,
            "pageNum": 1,
            "pageSize": 10,
            "supplierId": INFO['main_supplier_id']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'purchase_list', data, 'main', nocheck)

    @doc(a_attachment_purchase_list_search_people)
    @BaseApi.timing_decorator
    def attachment_purchase_list_search_people(self, nocheck=False):
        res = self.pc.attachment_purchase_list_data()
        ParamCache.cache_object({"orderNo": res[0]['orderNo']})
        data = {
            "articlesType": 2,
            "pageNum": 1,
            "pageSize": 10,
            "userId": INFO['main_user_id']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'purchase_list', data, 'main', nocheck)

    @doc(a_attachment_purchase_list_search_time)
    @BaseApi.timing_decorator
    def attachment_purchase_list_search_time(self, nocheck=False):
        res = self.pc.attachment_purchase_list_data()
        ParamCache.cache_object({"orderNo": res[0]['orderNo']})
        data = {
            "articlesType": 2,
            "pageNum": 1,
            "pageSize": 10,
            "erpEndTime": self.get_the_date(days=1),
            "erpStartTime": self.get_the_date()
        }
        self.validate_request_data(data)
        return self._make_request('post', 'purchase_list', data, 'main', nocheck)

    @doc(a_attachment_purchase_list_search_status)
    @BaseApi.timing_decorator
    def attachment_purchase_list_search_status(self, nocheck=False, state=None):
        res = self.pc.attachment_purchase_list_data()
        ParamCache.cache_object({"orderNo": res[0]['orderNo']})
        data = {
            "articlesType": 2,
            "pageNum": 1,
            "pageSize": 10,
            "state": state
        }
        self.validate_request_data(data)
        return self._make_request('post', 'purchase_list', data, 'main', nocheck)

    @doc(a_attachment_purchase_list_search_payment)
    @BaseApi.timing_decorator
    def attachment_purchase_list_search_payment(self, nocheck=False, pay=None):
        res = self.pc.attachment_purchase_list_data()
        ParamCache.cache_object({"orderNo": res[0]['orderNo']})
        data = {
            "articlesType": 2,
            "pageNum": 1,
            "pageSize": 10,
            "payState": pay
        }
        self.validate_request_data(data)
        return self._make_request('post', 'purchase_list', data, 'main', nocheck)

    @doc(a_attachment_purchase_list_search_logistics)
    @BaseApi.timing_decorator
    def attachment_purchase_list_search_logistics(self, nocheck=False):
        res = self.pc.attachment_purchase_list_data()
        obj = res[0]['logisticsNo']
        ParamCache.cache_object({"logisticsNo": obj})
        data = {
            "articlesType": 2,
            "pageNum": 1,
            "pageSize": 10,
            "logisticsNo": obj
        }
        self.validate_request_data(data)
        return self._make_request('post', 'purchase_list', data, 'main', nocheck)


class AttachmentReceiveItemsRequest(InitializeParams):
    """库存管理|移交接收管理|接收物品"""

    @doc(a_item_inventory_accessory_item_receipt)
    @BaseApi.timing_decorator
    def item_inventory_accessory_item_receipt(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data(i=2)
        data = {
            "accessoryList": [
                {
                    "articlesNo": res[0]["articlesNo"]
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'accessory_receive_items', data, 'main', nocheck)

    @doc(a_handover_orders_received_in_batches)
    @BaseApi.timing_decorator
    def handover_orders_received_in_batches(self, nocheck=False):
        res = self.pc.attachment_receive_items_data()
        data = {
            "orderNoList": [
                res[0]['orderNo']
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'accessory_receive_items', data, 'main', nocheck)

    @doc(a_attachment_receive_item_search_item)
    @BaseApi.timing_decorator
    def attachment_receive_item_search_item(self, nocheck=False):
        res = self.pc.attachment_receive_items_data(data='a')
        obj = res[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesNo": obj,
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'items_to_be_received', data, 'main', nocheck)

    @doc(a_attachment_receive_item_search_category)
    @BaseApi.timing_decorator
    def attachment_receive_item_search_category(self, nocheck=False):
        res = self.pc.attachment_receive_items_data(data='a')
        ParamCache.cache_object({"articlesNo": res[0]['articlesNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesTypeId": "1",
            "brandId": 8,
            "modelId": 18111,
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'items_to_be_received', data, 'main', nocheck)

    @doc(a_attachment_receive_item_search_person)
    @BaseApi.timing_decorator
    def attachment_receive_item_search_person(self, nocheck=False):
        res = self.pc.attachment_receive_items_data(data='a')
        ParamCache.cache_object({"articlesNo": res[0]['articlesNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "distributorId": INFO['main_user_id'],
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'items_to_be_received', data, 'main', nocheck)

    @doc(a_attachment_receive_item_search_accept)
    @BaseApi.timing_decorator
    def attachment_receive_item_search_accept(self, nocheck=False):
        res = self.pc.attachment_receive_items_data(data='a')
        ParamCache.cache_object({"articlesNo": res[0]['articlesNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "userId": INFO['special_user_id'],
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'items_to_be_received', data, 'main', nocheck)

    @doc(a_attachment_receive_item_search_time)
    @BaseApi.timing_decorator
    def attachment_receive_item_search_time(self, nocheck=False):
        res = self.pc.attachment_receive_items_data(data='a')
        ParamCache.cache_object({"articlesNo": res[0]['articlesNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "erpStartTime": self.get_the_date(),
            "erpEndTime": self.get_the_date(days=1),
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'items_to_be_received', data, 'main', nocheck)

    @doc(a_attachment_receive_item_search_order)
    @BaseApi.timing_decorator
    def attachment_receive_item_search_order(self, nocheck=False):
        res = self.pc.attachment_receive_items_data(data='a')
        obj = res[0]['orderNo']
        ParamCache.cache_object({"orderNo": obj})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "orderNo": obj,
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'items_to_be_received', data, 'main', nocheck)

    @doc(a_attachment_receive_item_search_item_no)
    @BaseApi.timing_decorator
    def attachment_receive_item_search_item_no(self, nocheck=False):
        res = self.pc.attachment_receive_items_data(data='a')
        obj = res[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesNo": obj,
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'receive_items', data, 'main', nocheck)

    @doc(a_attachment_receive_item_search_order_no)
    @BaseApi.timing_decorator
    def attachment_receive_item_search_order_no(self, nocheck=False):
        res = self.pc.attachment_receive_items_data()
        obj = res[0]['orderNo']
        ParamCache.cache_object({"orderNo": obj})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "orderNo": obj,
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'receive_items', data, 'main', nocheck)

    @doc(a_attachment_receive_item_search_status)
    @BaseApi.timing_decorator
    def attachment_receive_item_search_status(self, nocheck=False, status=None):
        res = self.pc.attachment_receive_items_data()
        ParamCache.cache_object({"orderNo": res[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "status": status,
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'receive_items', data, 'main', nocheck)

    @doc(a_attachment_receive_item_search_transfer_person)
    @BaseApi.timing_decorator
    def attachment_receive_item_search_transfer_person(self, nocheck=False):
        res = self.pc.attachment_receive_items_data()
        ParamCache.cache_object({"orderNo": res[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesType": 2,
            "distributorId": INFO['main_user_id']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'receive_items', data, 'main', nocheck)

    @doc(a_attachment_receive_item_search_recipient)
    @BaseApi.timing_decorator
    def attachment_receive_item_search_recipient(self, nocheck=False):
        res = self.pc.attachment_receive_items_data()
        ParamCache.cache_object({"orderNo": res[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "userId": INFO['special_user_id'],
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'receive_items', data, 'main', nocheck)

    @doc(a_attachment_receive_item_search_transfer_time)
    @BaseApi.timing_decorator
    def attachment_receive_item_search_transfer_time(self, nocheck=False):
        res = self.pc.attachment_receive_items_data()
        ParamCache.cache_object({"orderNo": res[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "erpStartTime": self.get_the_date(),
            "erpEndTime": self.get_the_date(days=1),
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'receive_items', data, 'main', nocheck)


class AttachmentSalesListRequest(InitializeParams):
    """配件管理|配件销售|销售列表"""

    @doc(a_accessories_sales_express_received_payment)
    @BaseApi.timing_decorator
    def accessories_sales_express_received_payment(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data(i=2)
        data = {
            "status": "1",
            "accountNo": INFO['main_account_no'],
            "isEexpress": "0",
            "logisticsNo": self.jd,
            "logisticsNoPrice": "11",
            "saleSupplierId": INFO['main_sale_supplier_id'],
            "supplierName": INFO['vice_sales_customer_name'],
            "remark": "备注",
            "saleOrderAccessoryList": [
                {
                    "accessoryNo": res[0]['articlesNo'],
                    "accessoryId": res[0]['id'],
                    "salePrice": "70",
                    "costPrice": res[0]['totalCost']
                }
            ],
            "deliveryNum": 1,
            "accountName": INFO['main_account_name']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'accessory_sales', data, 'main', nocheck)

    @doc(a_accessory_sales_express_easy)
    @BaseApi.timing_decorator
    def accessory_sales_express_easy(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data(i=2)
        data = {
            "status": "2",
            "accountNo": INFO['main_account_no'],
            "isEexpress": "1",
            "logisticsNoPrice": 10,
            "saleSupplierId": INFO['main_sale_supplier_id'],
            "supplierName": INFO['vice_sales_customer_name'],
            "remark": "备注",
            "walletAccountNo": INFO['main_wallet_account_no'],
            "payWay": 1,
            "pickUpType": 1,
            "logisticsCompanyType": 1,
            "userAddressId": INFO['main_user_address_id'],
            "saleOrderAccessoryList": [
                {
                    "accessoryNo": res[0]['articlesNo'],
                    "accessoryId": res[0]['id'],
                    "salePrice": "70",
                    "costPrice": res[0]['totalCost']
                }
            ],
            "deliveryNum": 1,
            "accountName": INFO['main_account_name']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'accessory_sales', data, 'main', nocheck)

    @doc(a_accessory_sales_express_easy_maximum)
    @BaseApi.timing_decorator
    def accessory_sales_express_easy_maximum(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data(i=2)
        data = {
            "status": "2",
            "accountNo": INFO['main_account_no'],
            "isEexpress": "1",
            "logisticsNoPrice": 10,
            "saleSupplierId": INFO['main_sale_supplier_id'],
            "supplierName": INFO['vice_sales_customer_name'],
            "remark": "备注",
            "walletAccountNo": INFO['main_wallet_account_no'],
            "payWay": 1,
            "pickUpType": 1,
            "logisticsCompanyType": 1,
            "userAddressId": INFO['main_user_address_id'],
            "saleOrderAccessoryList": [
                {
                    "accessoryNo": res[0]['articlesNo'],
                    "accessoryId": res[0]['id'],
                    "salePrice": "99999",
                    "costPrice": res[0]['totalCost']
                }
            ],
            "deliveryNum": 1,
            "accountName": INFO['main_account_name']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'accessory_sales', data, 'main', nocheck)

    @doc(a_uncollected_partial_sales_amount)
    @BaseApi.timing_decorator
    def uncollected_partial_sales_amount(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data(i=2)
        data = {
            "status": "2",
            "accountNo": INFO['main_account_no'],
            "isEexpress": "0",
            "logisticsNo": self.jd,
            "logisticsNoPrice": "11",
            "saleSupplierId": INFO['main_sale_supplier_id'],
            "supplierName": INFO['vice_sales_customer_name'],
            "remark": "备注",
            "saleOrderAccessoryList": [
                {
                    "accessoryNo": res[0]['articlesNo'],
                    "accessoryId": res[0]['id'],
                    "salePrice": "644",
                    "costPrice": res[0]['totalCost']
                }
            ],
            "deliveryNum": 1,
            "accountName": INFO['main_account_name']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'accessory_sales', data, 'main', nocheck)

    @doc(a_sales_after_sale_refund_not_received)
    @BaseApi.timing_decorator
    def sales_after_sale_refund_not_received(self, nocheck=False):
        res = self.pc.attachment_sales_list_data(data='b')
        data = {
            "sellType": "1",
            "sellSupplierId": INFO['main_sale_supplier_id'],
            "status": 2,
            "receiveState": 1,
            "logisticsNo": self.jd,
            "logisticsNoPrice": "10",
            "remark": "备注",
            "isEexpress": "0",
            "afterSaleOrderAccessoryList": [
                {
                    "salePrice": res[0]['salePrice'],
                    "accessoryNo": res[0]['accessoryNo'],
                    "accessoryId": res[0]['id'],
                    "saleReturnPrice": res[0]['returnAblePrice'],
                    "saleOrderNo": res[0]['saleOrderNo']
                }
            ],
            "deliveryNum": 1,
            "supplierName": INFO['vice_sales_customer_name'],
        }
        self.validate_request_data(data)
        return self._make_request('post', 'after_sales_of_accessories', data, 'main', nocheck)

    @doc(a_sales_after_sale_refund_warehouse)
    @BaseApi.timing_decorator
    def sales_after_sale_refund_warehouse(self, nocheck=False):
        res = self.pc.attachment_sales_list_data(data='b')
        data = {
            "sellType": "1",
            "sellSupplierId": INFO['main_sale_supplier_id'],
            "status": 2,
            "receiveState": "2",
            "remark": "备注",
            "isEexpress": "0",
            "afterSaleOrderAccessoryList": [
                {
                    "salePrice": res[0]['salePrice'],
                    "accessoryNo": res[0]['accessoryNo'],
                    "accessoryId": res[0]['id'],
                    "saleReturnPrice": res[0]['returnAblePrice'],
                    "saleOrderNo": res[0]['saleOrderNo'],
                    "warehouseId": INFO['main_warehouse_id'],
                }
            ],
            "deliveryNum": 1,
            "supplierName": INFO['vice_sales_customer_name'],
        }
        self.validate_request_data(data)
        return self._make_request('post', 'after_sales_of_accessories', data, 'main', nocheck)

    @doc(a_sales_after_refund_the_price_difference)
    @BaseApi.timing_decorator
    def sales_after_refund_the_price_difference(self, nocheck=False):
        res = self.pc.attachment_sales_list_data()
        res_2 = self.pc.attachment_sales_list_data(data='a')
        res_3 = self.pc.attachment_sales_list_data(data='b')
        data = {
            "sellType": "2",
            "sellSupplierId": INFO['main_sale_supplier_id'],
            "status": 2,
            "remark": "备注",
            "isEexpress": "0",
            "afterSaleOrderAccessoryList": [
                {
                    "salePrice": res_2[0]['salePrice'],
                    "accessoryNo": res_2[0]['accessoryNo'],
                    "accessoryId": res[0]['id'],
                    "saleReturnPrice": res_3[0]['returnAblePrice'],
                    "saleOrderNo": res[0]['orderNo'],
                    "newSellPrice": "1"
                }
            ],
            "deliveryNum": 1,
            "supplierName": INFO['vice_sales_customer_name']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'after_sales_of_accessories', data, 'main', nocheck)

    @doc(a_the_full_amount_will_be_refunded_the_difference)
    @BaseApi.timing_decorator
    def the_full_amount_will_be_refunded_the_difference(self, nocheck=False):
        res = self.pc.attachment_sales_list_data()
        res_2 = self.pc.attachment_sales_list_data(data='a')
        res_3 = self.pc.attachment_sales_list_data(data='b')
        data = {
            "sellType": "2",
            "sellSupplierId": INFO['main_sale_supplier_id'],
            "status": 2,
            "remark": "备注",
            "isEexpress": "0",
            "afterSaleOrderAccessoryList": [
                {
                    "salePrice": res_2[0]['salePrice'],
                    "accessoryNo": res_2[0]['accessoryNo'],
                    "accessoryId": res[0]['id'],
                    "saleReturnPrice": res_3[0]['returnAblePrice'],
                    "saleOrderNo": res[0]['orderNo'],
                    "newSellPrice": res[0]['salePrice']
                }
            ],
            "deliveryNum": 1,
            "supplierName": INFO['vice_sales_customer_name']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'after_sales_of_accessories', data, 'main', nocheck)

    @doc(a_attachment_sales_list_search_order)
    @BaseApi.timing_decorator
    def attachment_sales_list_search_order(self, nocheck=False):
        res = self.pc.attachment_sales_list_data()
        obj = res[0]['orderNo']
        ParamCache.cache_object({"orderNo": obj})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "orderNo": obj,
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'sales_list', data, 'main', nocheck)

    @doc(a_attachment_sales_list_search_customer)
    @BaseApi.timing_decorator
    def attachment_sales_list_search_customer(self, nocheck=False):
        res = self.pc.attachment_sales_list_data()
        ParamCache.cache_object({"orderNo": res[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "saleSupplierId": INFO['main_sale_supplier_id'],
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'sales_list', data, 'main', nocheck)

    @doc(a_attachment_sales_list_search_status)
    @BaseApi.timing_decorator
    def attachment_sales_list_search_status(self, nocheck=False, status=None):
        res = self.pc.attachment_sales_list_data()
        ParamCache.cache_object({"orderNo": res[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesType": 2,
            "status": status
        }
        self.validate_request_data(data)
        return self._make_request('post', 'sales_list', data, 'main', nocheck)

    @doc(a_attachment_sales_list_search_logistics)
    @BaseApi.timing_decorator
    def attachment_sales_list_search_logistics(self, nocheck=False):
        res = self.pc.attachment_sales_list_data()
        obj = res[0]['logisticsNo']
        ParamCache.cache_object({"logisticsNo": obj})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "logisticsNo": obj,
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'sales_list', data, 'main', nocheck)


class AttachmentSortingListRequest(InitializeParams):
    """配件管理|入库管理|新到货入库"""

    @doc(a_search_for_tracking_number_inbound_and_handover)
    @BaseApi.timing_decorator
    def search_for_tracking_number_inbound_and_handover(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data(i=1)
        data = {
            "accessoryList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "warehouseId": INFO['main_warehouse_id']
                }
            ],
            "quickOperation": 1,
            "purchaseOrdersArticlesDTO": {
                "articlesNoList": [
                    res[0]['articlesNo']
                ],
                "createBy": INFO['special_account_name'],
                "type": "",
                "userId": INFO['special_user_id'],
                "remark": "备注"
            }
        }
        self.validate_request_data(data)
        return self._make_request('post', 'old_sign_into_the_library', data, 'main', nocheck)


class AttachmentStockTransferRequest(InitializeParams):
    """配件管理|配件库存|库存调拨"""

    @doc(a_select_add_item_transfer)
    @BaseApi.timing_decorator
    def new_allocation(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data(i=2)
        data = {
            "outWarehouseId": INFO['main_warehouse_id'],
            "inWarehouseId": INFO['main_item_in_warehouse_id'],
            "remark": "备注",
            "articlesType": "2",
            "articles": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": None
                }
            ],
            "expressInfo": {
                "walletAccountNo": INFO['main_wallet_account_no'],
                "isEexpress": 0,
                "estimateFreight": None,
                "expressNo": self.jd
            }
        }
        self.validate_request_data(data)
        return self._make_request('post', 'new_allocation', data, 'main', nocheck)

    @doc(a_express_is_easy_new_allocation)
    @BaseApi.timing_decorator
    def express_is_easy_new_allocation(self, nocheck=False):
        res = self.pc.attachment_inventory_list_data(i=2)
        data = {
            "outWarehouseId": INFO['main_warehouse_id'],
            "inWarehouseId": INFO['main_item_in_warehouse_id'],
            "remark": "备注",
            "articlesType": "2",
            "articles": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": None
                }
            ],
            "expressInfo": {
                "walletAccountNo": INFO['main_wallet_account_no'],
                "isEexpress": 1,
                "estimateFreight": 10,
                "expressCompanyId": "1",
                "expressCompanyName": "顺丰",
                "expectPostTimeStart": self.get_formatted_datetime(),
                "payWay": 1,
                "senderName": "admin",
                "senderPhone": INFO['receiving_phone'],
                "senderProvinceId": INFO['shipping_province_id'],
                "senderProvinceName": INFO['shipping_city_name'],
                "senderCityId": INFO['shipping_city_id'],
                "senderCityName": INFO['shipping_city_name'],
                "senderCountyId": INFO['shipping_county_id'],
                "senderCountyName": INFO['shipping_detailed_address'],
                "senderAddress": INFO['shipping_detailed_address'],
                "recipientName": INFO['shipping_address_creator'],
                "recipientPhone": INFO['receiving_phone'],
                "recipientProvinceId": INFO['province_id'],
                "recipientProvinceName": INFO['province_name'],
                "recipientCityId": INFO['city_id'],
                "recipientCityName": INFO['city_name'],
                "recipientCountyId": INFO['county_id'],
                "recipientCountyName": INFO['county_name'],
                "recipientAddress": INFO['detailed_address'],
            }
        }
        self.validate_request_data(data)
        return self._make_request('post', 'new_allocation', data, 'main', nocheck)

    @doc(a_receive)
    @BaseApi.timing_decorator
    def receive(self, nocheck=False):
        res = self.pc.attachment_warehouse_allocation_data()
        data = {
            "id": res[0]['id'],
            "quickOperation": 0
        }
        self.validate_request_data(data)
        return self._make_request('post', 'allocation_receive', data, 'main', nocheck)

    @doc(a_revoke)
    @BaseApi.timing_decorator
    def revoke(self, nocheck=False):
        res = self.pc.attachment_warehouse_allocation_data()
        res_2 = self.pc.attachment_warehouse_allocation_data(data='b')
        data = {
            "id": res[0]['id'],
            "articlesNoList": [
                res_2[0]['articlesNo']
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'allocation_revoke', data, 'main', nocheck)


if __name__ == '__main__':
    api = AttachmentGoodsReceivedRequest()
    result = api.goods_received()
    print(json.dumps(result, indent=4, ensure_ascii=False))
