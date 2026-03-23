# coding: utf-8
import json
from common.base_api import BaseApi
from common.base_params import InitializeParams, is_performance_close
from common.file_cache_manager import ParamCache
from common.import_desc import *
from config.user_info import INFO


class SellAfterSalesHandlingRequest(InitializeParams):
    """商品销售|销售售后管理|销售售后处理"""

    @doc(s_sales_after_sales_returns)
    @BaseApi.timing_decorator
    def sales_after_sales_returns(self, nocheck=False):
        res = self.pc.inventory_list_data(i='3', j='9')
        data = {
            "saleType": "1",
            "remark": "备注",
            "status": 2,
            "payState": "2",
            "returnType": 1,
            "warehouseId": INFO['main_item_warehouse_id'],
            "sellSaleOrderArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "platformArticlesNo": res[0]['platformArticlesNo'],
                    "newSalePrice": 0,
                    "saleSettlePrice": res[0]['sumCost'],
                    "saleOrderNo": res[0]['salesOrder'],
                    "accountNo": None,
                    "accessoryNoList": []
                }
            ]
        }
        return self._make_request('post', 'sales_after_sales_list', data, 'main', nocheck)

    @doc(s_sell_returned_spare_parts_after_sale_journey_warehouse)
    @BaseApi.timing_decorator
    def sell_returned_spare_parts_after_sale_journey_warehouse(self, nocheck=False):
        res = self.pc.sell_sale_item_list_data()
        data = {
            "saleType": "2",
            "remark": "备注",
            "status": 2,
            "payState": "2",
            "warehouseId": INFO['main_item_warehouse_id'],
            "sellSaleOrderArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "platformArticlesNo": res[0]['platformArticlesNo'],
                    "newSalePrice": int(self.number),
                    "saleSettlePrice": res[0]['saleSettlePrice'],
                    "saleOrderNo": res[0]['salesOrder'],
                    "accountNo": None,
                    "accessoryNoList": [
                        {
                            "brandId": res[0]['brandId'],
                            "brandName": res[0]['brandName'],
                            "modelId": res[0]['modelId'],
                            "modelName": res[0]['modelName'],
                            "accessoryType": 2,
                            "accessoryNo": "PJ0216",
                            "accessoryQuality": 3,
                            "accessoryPrice": int(self.number),
                            "articlesTypeId": 1,
                            "articlesTypeName": res[0]['articlesTypeName'],
                            "channelType": 1,
                            "purchasePrice": int(self.number)
                        }
                    ]
                }
            ]
        }
        return self._make_request('post', 'sales_after_sales_list', data, 'main', nocheck)

    @doc(s_sell_returned_spare_parts_after_sale_journey)
    @BaseApi.timing_decorator
    def sell_returned_spare_parts_after_sale_journey(self, nocheck=False):
        res = self.pc.sell_sale_item_list_data()
        data = {
            "saleType": "2",
            "remark": "备注",
            "status": 1,
            "logisticsNo": str(self.jd),
            "payState": "2",
            "sellSaleOrderArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "platformArticlesNo": res[0]['platformArticlesNo'],
                    "newSalePrice": int(self.number),
                    "saleSettlePrice": res[0]['saleSettlePrice'],
                    "saleOrderNo": res[0]['salesOrder'],
                    "accountNo": None,
                    "accessoryNoList": [
                        {
                            "brandId": res[0]['brandId'],
                            "brandName": res[0]['brandName'],
                            "modelId": res[0]['modelId'],
                            "modelName": res[0]['modelName'],
                            "accessoryType": 2,
                            "accessoryNo": "PJ0215",
                            "accessoryQuality": 3,
                            "accessoryPrice": int(self.number),
                            "articlesTypeId": 1,
                            "articlesTypeName": res[0]['articlesTypeName'],
                            "channelType": 1,
                            "purchasePrice": int(self.number)
                        }
                    ]
                }
            ]
        }
        return self._make_request('post', 'sales_after_sales_list', data, 'main', nocheck)


class SellGoodsListingRequest(InitializeParams):
    """商品销售|销售管理|销售上架"""

    @doc(s_sell_goods_listing)
    @BaseApi.timing_decorator
    def sell_goods_listing(self, nocheck=False):
        time = self.get_current_timestamp_ms()
        res = self.pc.inventory_list_data(i='2', j='13')
        data = {
            "saleTime": self.get_formatted_datetime(),
            "saleType": 2,
            "clientId": INFO['main_sale_supplier_id'],
            "clientName": INFO['vice_sales_customer_name'],
            "accountNo": INFO['main_account_no'],
            "userId": INFO['main_user_id'],
            "offExpressage": "0",
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res[0]['id'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 13,
                    "salePrice": 100,
                    "platformArticlesNo": res[0]['platformArticlesNo'],
                    "platformOrderNo": None,
                    "remark": res[0]['remark'],
                    "finenessId": 1,
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1,
                        "id": time
                    }
                }
            ]
        }
        return self._make_request('post', 'sale_goods_listing', data, 'main', nocheck)


class SellMiddleItemListRequest(InitializeParams):
    """商品销售|销售管理|销售中物品列表"""

    @BaseApi.timing_decorator
    def item_number(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='15')
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'set_articles_no', data, 'main', nocheck)

    @doc(s_edit_status_info_pay)
    @BaseApi.timing_decorator
    def edit_status_info_pay(self, nocheck=False):
        self.item_number()
        res = self.pc.sell_list_of_items_for_sale_data()
        res_2 = self.pc.sell_list_of_items_for_sale_data(data='a')
        data = {
            "saleTime": self.get_formatted_datetime(),
            "saleType": "1",
            "clientId": res[0]['saleSupplierId'],
            "accountNo": INFO['main_account_no'],
            "accountName": INFO['main_account_name'],
            "userId": INFO['main_user_id'],
            "deliveryId": INFO['main_user_id'],
            "deliveryTime": self.get_formatted_datetime(),
            "status": 1,
            "logisticsOrder": self.jd,
            "logisticsNoPrice": 0,
            "offExpressage": "0",
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res_2[0]['id'],
                    "imei": res[0]['imei'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 13,
                    "salePrice": res[0]['salePrice'],
                    "platformArticlesNo": res[0]['platformArticlesNo'],
                    "platformOrderNo": None,
                    "remark": "备注",
                    "finenessId": 1,
                    "articlesInfoId": res_2[0]['articlesInfoId'],
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1,
                        "id": res_2[0]['articlesInfoId'],
                    },
                    "saleSettlePrice": res[0]['saleSettlePrice']
                }
            ]
        }
        return self._make_request('post', 'item_inventory_sell', data, 'main', nocheck)

    @doc(s_edit_status_info_not_received)
    @BaseApi.timing_decorator
    def edit_status_info_not_received(self, nocheck=False):
        self.item_number()
        res = self.pc.sell_list_of_items_for_sale_data()
        res_2 = self.pc.sell_list_of_items_for_sale_data(data='a')
        data = {
            "saleTime": self.get_formatted_datetime(),
            "saleType": "1",
            "clientId": res[0]['saleSupplierId'],
            "userId": INFO['main_user_id'],
            "deliveryId": INFO['main_user_id'],
            "status": 2,
            "logisticsOrder": 0,
            "logisticsNoPrice": 0,
            "offExpressage": "0",
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res_2[0]['id'],
                    "imei": res[0]['imei'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 13,
                    "salePrice": res[0]['salePrice'],
                    "platformArticlesNo": res[0]['platformArticlesNo'],
                    "platformOrderNo": None,
                    "remark": "备注",
                    "finenessId": 1,
                    "articlesInfoId": res_2[0]['articlesInfoId'],
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1,
                        "id": res_2[0]['articlesInfoId'],
                    },
                    "saleSettlePrice": res[0]['saleSettlePrice']
                }
            ]
        }
        return self._make_request('post', 'item_inventory_sell', data, 'main', nocheck)

    @doc(s_on_and_off_shelves)
    @BaseApi.timing_decorator
    def on_and_off_shelves(self, nocheck=False):
        res = self.pc.sell_list_of_items_for_sale_data(data='b')
        data = {
            "articlesList": [
                {
                    "id": res[0]['id'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 13,
                    "saleRecordId": res[0]['saleRecordId'],
                    "remark": ""
                }
            ]
        }
        return self._make_request('post', 'take_down', data, 'main', nocheck)

    @doc(s_presale_confirm_the_sale)
    @BaseApi.timing_decorator
    def presale_confirm_the_sale(self, nocheck=False):
        res = self.pc.sell_list_of_items_for_sale_data(i='1', j='5')
        res_2 = self.pc.inventory_list_data(i='3', j='19')
        data = [
            {
                "id": res[0]['id'],
                "articlesId": res_2[0]['id'],
                "supplierId": INFO['main_sale_supplier_id'],
                "accountNo": INFO['main_account_no'],
                "accountName": INFO['main_account_name'],
                "articlesNo": res[0]['articlesNo'],
                "status": "1",
                "articlesState": 19,
                "saleSettlePrice": 11,
                "salePrice": 100,
                "platformOrderNo": "",
                "saleType": 5
            }
        ]
        return self._make_request('put', 'confirm_the_sale', data, 'main', nocheck)

    @doc(s_sales_and_delivery_of_goods)
    @BaseApi.timing_decorator
    def sales_and_delivery_of_goods(self, nocheck=False):
        res = self.pc.sell_list_of_items_for_sale_data(i='1', j='5')
        res_2 = self.pc.inventory_list_data(i='3', j='19')
        data = {
            "articlesList": [
                {
                    "id": res[0]['id'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 14,
                    "saleRecordId": res_2[0]['id'],
                    "receiveStatus": 1,
                    "remark": "备注"
                }
            ],
            "logisticsPrice": 11,
            "logisticsNo": self.sf,
            "warehouseId": INFO['main_item_warehouse_id']
        }
        return self._make_request('put', 'return_of_the_goods', data, 'main', nocheck)

    @doc(s_sell_goods_out_of_the_warehouse)
    @BaseApi.timing_decorator
    def sell_goods_out_of_the_warehouse(self, nocheck=False):
        res = self.pc.sell_list_of_items_for_sale_data(i='1', j='5')
        res_2 = self.pc.inventory_list_data(i='3', j='19')
        data = [
            {
                "id": res[0]['id'],
                "articlesId": res_2[0]['id'],
                "supplierId": INFO['main_sale_supplier_id'],
                "accountNo": INFO['main_account_no'],
                "accountName": INFO['main_account_name'],
                "articlesNo": res[0]['articlesNo'],
                "status": "1",
                "articlesState": 14,
                "saleSettlePrice": 100,
                "salePrice": res[0]['salePrice'],
                "platformOrderNo": None,
                "saleType": 3
            }
        ]
        return self._make_request('put', 'confirm_the_sale', data, 'main', nocheck)

    @doc(s_sell_search_in_sale_type)
    @BaseApi.timing_decorator
    def sell_search_in_sale_type(self):
        saleType = 5
        ParamCache.cache_object({"saleType": saleType}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "saleType": saleType,
        }
        return self._make_request('post', 'goods_list_for_sale', data, 'main')

    @doc(s_sell_search_in_imei)
    @BaseApi.timing_decorator
    def sell_search_in_imei(self):
        res = self.pc.sell_list_of_items_for_sale_data()
        imei = res[0]['imei']
        ParamCache.cache_object({"imei": imei}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "queryNo": res[0]['imei']
        }
        return self._make_request('post', 'goods_list_for_sale', data, 'main')

    @doc(s_sell_search_in_supplier_id)
    @BaseApi.timing_decorator
    def sell_search_in_supplier_id(self):
        supplierId = INFO['main_sale_supplier_id']
        ParamCache.cache_object({"saleSupplierId": supplierId}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "supplierId": supplierId
        }
        return self._make_request('post', 'goods_list_for_sale', data, 'main')

    @doc(s_sell_search_in_belong_type)
    @BaseApi.timing_decorator
    def sell_search_in_belong_type(self):
        belongType = 1
        ParamCache.cache_object({"belongType": belongType}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "belongType": belongType
        }
        return self._make_request('post', 'goods_list_for_sale', data, 'main')

    @doc(s_sell_search_in_user_id)
    @BaseApi.timing_decorator
    def sell_search_in_user_id(self):
        user_id = INFO['main_user_id']
        ParamCache.cache_object({"userId": user_id}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "userId": user_id
        }
        return self._make_request('post', 'goods_list_for_sale', data, 'main')

    @doc(s_sell_search_in_date)
    @BaseApi.timing_decorator
    def sell_search_in_date(self):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "time": [
                self.get_the_date(-1),
                self.get_the_date()
            ],
            "startTime": self.get_the_date(-1),
            "endTime": self.get_the_date()
        }
        return self._make_request('post', 'goods_list_for_sale', data, 'main')


class SellSaleItemRequest(InitializeParams):
    """商品销售|销售管理|待销售物品"""

    @BaseApi.timing_decorator
    def item_number(self, nocheck=False):
        res = self.pc.sell_goods_received_data()
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'set_articles_no', data, 'main', nocheck)

    @doc(s_sell_listing)
    @BaseApi.timing_decorator
    def sell_listing(self, nocheck=False):
        res = self.pc.sell_items_for_sale_data()
        res_2 = self.pc.sell_items_for_sale_data(data='a')
        data = {
            "clientId": INFO['main_sale_supplier_id'],
            "clientName": INFO['vice_sales_customer_name'],
            "accountNo": INFO['main_account_no'],
            "saleTime": self.get_formatted_datetime(),
            "saleType": 2,
            "userId": INFO['main_user_id'],
            "offExpressage": "0",
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res_2[0]['id'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 13,
                    "salePrice": 100,
                    "platformArticlesNo": res[0]['platformArticlesNo'],
                    "platformOrderNo": None,
                    "remark": None,
                    "finenessId": 1,
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1,
                        "id": res_2[0]['articlesInfoId']
                    }
                }
            ]
        }
        return self._make_request('post', 'sale_goods_listing', data, 'main', nocheck)

    @doc(s_wait_sell_articles_search_by_imei)
    @BaseApi.timing_decorator
    def wait_sell_articles_search_by_imei(self):
        res = self.pc.sell_items_for_sale_data()
        imei = res[0]['imei']
        ParamCache.cache_object({"imei": imei}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesNoOrImei": imei
        }
        return self._make_request('post', 'items_for_sale', data, 'main')

    @doc(s_sell_get_out)
    @BaseApi.timing_decorator
    def sell_get_out(self, nocheck=False):
        res = self.pc.sell_items_for_sale_data()
        res_2 = self.pc.sell_items_for_sale_data(data='a')
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
            "logisticsNoPrice": 30,
            "isEexpress": "0",
            "offExpressage": "0",
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res_2[0]['id'],
                    "imei": res[0]['imei'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 13,
                    "salePrice": 30,
                    "platformArticlesNo": res[0]['platformArticlesNo'],
                    "platformOrderNo": self.serial,
                    "remark": None,
                    "finenessId": 1,
                    "articlesInfoId": res_2[0]['articlesInfoId'],
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1,
                        "id": res_2[0]['articlesInfoId']
                    },
                    "saleSettlePrice": 30
                }
            ]
        }
        return self._make_request('post', 'item_inventory_sell', data, 'main', nocheck)

    @doc(s_sell_advance_sale)
    @BaseApi.timing_decorator
    def sell_advance_sale(self, nocheck=False):
        self.item_number()
        res = self.pc.sell_items_for_sale_data()
        res_2 = self.pc.sell_items_for_sale_data(data='a')
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
            "logisticsNoPrice": 123,
            "isEexpress": "0",
            "offExpressage": "0",
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res_2[0]['id'],
                    "imei": res[0]['imei'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 13,
                    "salePrice": 0,
                    "platformArticlesNo": res[0]['platformArticlesNo'],
                    "platformOrderNo": None,
                    "remark": None,
                    "finenessId": 1,
                    "articlesInfoId": res_2[0]['articlesInfoId'],
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1,
                        "id": res_2[0]['articlesInfoId'],
                    },
                    "saleSettlePrice": ""
                }
            ]
        }
        return self._make_request('post', 'item_inventory_sell', data, 'main', nocheck)

    @doc(s_sell_distribution)
    @BaseApi.timing_decorator
    def sell_distribution(self, nocheck=False):
        self.item_number()
        res = self.pc.sell_items_for_sale_data()
        res_2 = self.pc.sell_items_for_sale_data(data='a')
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
            "status": 2,
            "logisticsOrder": self.jd,
            "logisticsNoPrice": 30,
            "isEexpress": "0",
            "offExpressage": "0",
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res_2[0]['id'],
                    "imei": res[0]['imei'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 13,
                    "salePrice": 30,
                    "platformArticlesNo": res[0]['platformArticlesNo'],
                    "platformOrderNo": self.serial,
                    "remark": None,
                    "finenessId": 1,
                    "articlesInfoId": res_2[0]['articlesInfoId'],
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1,
                        "id": res_2[0]['articlesInfoId'],
                    },
                    "saleSettlePrice": 30
                }
            ]
        }
        return self._make_request('post', 'item_inventory_sell', data, 'main', nocheck)


class SellSaleOrderListRequest(InitializeParams):
    """商品销售|销售管理|已销售订单列表"""

    @doc(s_search_by_order_no)
    @BaseApi.timing_decorator
    def search_by_order_no(self):
        res = self.pc.sell_sale_order_list_data()
        obj = res[0]['orderNo']
        ParamCache.cache_object({"orderNo": obj}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10
        }
        return self._make_request('post', 'list_of_sold_orders', data, 'main')

    @doc(s_search_by_state)
    @BaseApi.timing_decorator
    def search_by_state(self):
        status = 1
        ParamCache.cache_object({"status": status}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "status": status,
        }
        return self._make_request('post', 'list_of_sold_orders', data, 'main')

    @doc(s_search_by_sale_supplier_id)
    @BaseApi.timing_decorator
    def search_by_sale_supplier_id(self):
        sid = INFO['main_sale_supplier_id']
        ParamCache.cache_object({"saleSupplierId": sid}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "saleSupplierId": sid,
        }
        return self._make_request('post', 'list_of_sold_orders', data, 'main')

    @doc(s_search_by_sale_user_id)
    @BaseApi.timing_decorator
    def search_by_sale_user_id(self):
        sid = INFO['main_user_id']
        ParamCache.cache_object({"saleUserId": sid}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "saleUserId": sid,
        }
        return self._make_request('post', 'list_of_sold_orders', data, 'main')

    @doc(s_order_search_by_date)
    @BaseApi.timing_decorator
    def order_search_by_date(self):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "total": 0,
            "startSaleTime": self.get_the_date(-1),
            "endSaleTime": self.get_the_date()
        }
        return self._make_request('post', 'list_of_sold_orders', data, 'main')

    @doc(s_order_search_by_out_date)
    @BaseApi.timing_decorator
    def order_search_by_out_date(self):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "startSaleTime": self.get_the_date(-1),
            "endSaleTime": self.get_the_date()
        }
        return self._make_request('post', 'list_of_sold_orders', data, 'main')

    @doc(s_order_search_by_logistics_no)
    @BaseApi.timing_decorator
    def order_search_by_logistics_no(self):
        res = self.pc.sell_sale_order_list_data()
        ParamCache.cache_object({"logisticsNo": res[0]['logisticsNo']}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "logisticsNo": res[0]['logisticsNo'],
        }
        return self._make_request('post', 'list_of_sold_orders', data, 'main')


class SellSaleItemListRequest(InitializeParams):
    """商品销售|销售管理|已销售物品列表"""

    @doc(s_sell_refund_difference)
    @BaseApi.timing_decorator
    def sell_refund_difference(self, nocheck=False):
        res = self.pc.sell_sale_item_list_data()
        data = {
            "saleType": "5",
            "status": 1,
            "payState": "2",
            "sellSaleOrderArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "platformArticlesNo": res[0]['sellPlatformOrderNo'],
                    "newSalePrice": 60,
                    "saleSettlePrice": res[0]['saleSettlePrice'],
                    "saleOrderNo": res[0]['salesOrder'],
                    "accountNo": None,
                    "accessoryNoList": []
                }
            ]
        }
        return self._make_request('post', 'sales_after_sales_list', data, 'main', nocheck)

    @doc(s_sell_return_goods_route)
    @BaseApi.timing_decorator
    def sell_return_goods_route(self, nocheck=False):
        res = self.pc.sell_sale_item_list_data()
        data = {
            "saleType": "1",
            "remark": "test",
            "status": 2,
            "payState": "2",
            "returnType": 1,
            "warehouseId": INFO['main_item_in_warehouse_id'],
            "sellSaleOrderArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "platformArticlesNo": res[0]['sellPlatformOrderNo'],
                    "newSalePrice": 0,
                    "saleSettlePrice": res[0]['saleSettlePrice'],
                    "saleOrderNo": res[0]['salesOrder'],
                    "accountNo": None,
                    "accessoryNoList": []
                }
            ]
        }
        return self._make_request('post', 'sales_after_sales_list', data, 'main', nocheck)

    @doc(s_sell_return_only_parts_route)
    @BaseApi.timing_decorator
    def sell_return_only_parts_route(self, nocheck=False):
        res = self.pc.sell_sale_item_list_data()
        data = {
            "saleType": "2",
            "status": 1,
            "logisticsNo": self.jd,
            "payState": "2",
            "returnType": 1,
            "sellSaleOrderArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "platformArticlesNo": res[0]['sellPlatformOrderNo'],
                    "newSalePrice": 100,
                    "saleSettlePrice": res[0]['saleSettlePrice'],
                    "saleOrderNo": res[0]['salesOrder'],
                    "accountNo": None,
                    "accessoryNoList": [
                        {
                            "brandId": 905,
                            "brandName": "柔宇",
                            "modelId": 13578,
                            "modelName": "FlexPai",
                            "accessoryType": 2,
                            "accessoryNo": "PJ0001",
                            "accessoryQuality": 3,
                            "accessoryPrice": 40,
                            "articlesTypeId": 1,
                            "articlesTypeName": "手机",
                            "channelType": 2,
                            "purchasePrice": 40
                        }
                    ]
                }
            ]
        }
        return self._make_request('post', 'sales_after_sales_list', data, 'main', nocheck)

    @doc(s_sell_return_only_parts_warehousing)
    @BaseApi.timing_decorator
    def sell_return_only_parts_warehousing(self, nocheck=False):
        res = self.pc.sell_sale_item_list_data()
        data = {
            "saleType": "2",
            "remark": "123",
            "status": 2,
            "payState": "2",
            "returnType": 1,
            "warehouseId": INFO['main_in_warehouse_id'],
            "sellSaleOrderArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "platformArticlesNo": res[0]['sellPlatformOrderNo'],
                    "newSalePrice": 100,
                    "saleSettlePrice": res[0]['saleSettlePrice'],
                    "saleOrderNo": res[0]['salesOrder'],
                    "accountNo": None,
                    "accessoryNoList": [
                        {
                            "brandId": 905,
                            "brandName": "柔宇",
                            "modelId": 13578,
                            "modelName": "FlexPai",
                            "accessoryType": 2,
                            "accessoryNo": "PJ0001",
                            "accessoryQuality": 3,
                            "accessoryPrice": 40,
                            "articlesTypeId": 1,
                            "articlesTypeName": "手机",
                            "channelType": 2,
                            "purchasePrice": 40
                        }
                    ]
                }
            ]
        }
        return self._make_request('post', 'sales_after_sales_list', data, 'main', nocheck)

    @doc(s_sales_are_refunded_only)
    @BaseApi.timing_decorator
    def sales_are_refunded_only(self, nocheck=False):
        res = self.pc.sell_sale_item_list_data()
        data = {
            "saleType": "8",
            "remark": "test",
            "sellSaleOrderArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "platformArticlesNo": res[0]['sellPlatformOrderNo'],
                    "newSalePrice": 50,
                    "saleSettlePrice": res[0]['saleSettlePrice'],
                    "saleOrderNo": res[0]['salesOrder'],
                    "accountNo": None,
                    "accessoryNoList": []
                }
            ]
        }
        return self._make_request('post', 'sales_after_sales_list', data, 'main', nocheck)

    @doc(s_search_by_sale_no)
    @BaseApi.timing_decorator
    def search_by_sale_no(self):
        res = self.pc.sell_sale_item_list_data()
        obj = res[0]['salesOrder']
        ParamCache.cache_object({"salesOrder": obj}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10
        }
        return self._make_request('post', 'sell_sale_item_list', data, 'main')

    @doc(s_search_by_imei)
    @BaseApi.timing_decorator
    def search_by_imei(self):
        res = self.pc.sell_sale_item_list_data()
        obj = res[0]['imei']
        ParamCache.cache_object({"imei": obj}, 'practical.json')
        data = {
            "articlesNoOrImei": obj,
            "pageNum": 1,
            "pageSize": 10
        }
        return self._make_request('post', 'sell_sale_item_list', data, 'main')

    @doc(s_search_by_category_id)
    @BaseApi.timing_decorator
    def search_by_category_id(self):
        obj = 1
        ParamCache.cache_object({"categoryId": obj}, 'practical.json')
        data = {
            "categoryId": obj,
            "pageNum": 1,
            "pageSize": 10
        }
        return self._make_request('post', 'sell_sale_item_list', data, 'main')

    @doc(s_search_by_brand)
    @BaseApi.timing_decorator
    def search_by_brand(self):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "categoryId": 1,
            "brandId": 1
        }
        return self._make_request('post', 'sell_sale_item_list', data, 'main')

    @doc(s_search_by_model)
    @BaseApi.timing_decorator
    def search_by_model(self):
        model_id = 17569
        ParamCache.cache_object({"modelId": model_id}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "categoryId": "1",
            "brandId": 1,
            "modelId": model_id
        }
        return self._make_request('post', 'sell_sale_item_list', data, 'main')

    @doc(s_search_by_supplier_id)
    @BaseApi.timing_decorator
    def search_by_supplier_id(self):
        supplier_id = INFO['main_supplier_id']
        ParamCache.cache_object({"supplierId": supplier_id}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "supplierId": supplier_id
        }
        return self._make_request('post', 'sell_sale_item_list', data, 'main')

    @doc(s_search_by_sale_supplier_id)
    @BaseApi.timing_decorator
    def search_by_sale_supplier_id(self):
        client_id = INFO['main_sale_supplier_id']
        ParamCache.cache_object({"clientId": client_id}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "saleSupplierId": client_id
        }
        return self._make_request('post', 'sell_sale_item_list', data, 'main')

    @doc(s_search_by_status)
    @BaseApi.timing_decorator
    def search_by_status(self):
        status = 2
        ParamCache.cache_object({"status": status}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "status": status
        }
        return self._make_request('post', 'sell_sale_item_list', data, 'main')

    @doc(s_search_by_platform_no)
    @BaseApi.timing_decorator
    def search_by_platform_no(self):
        res = self.pc.sell_sale_item_list_data()
        obj = res[0]['platformNo']
        ParamCache.cache_object({"platformNo": obj}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "sellPlatformArticlesNo": obj
        }
        return self._make_request('post', 'sell_sale_item_list', data, 'main')

    @doc(s_search_by_sell_platform_no)
    @BaseApi.timing_decorator
    def search_by_sell_platform_no(self):
        res = self.pc.sell_sale_item_list_data()
        obj = res[0]['sellPlatformOrderNo']
        ParamCache.cache_object({"sellPlatformOrderNo": obj}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "sellPlatformOrderNo": obj
        }
        return self._make_request('post', 'sell_sale_item_list', data, 'main')

    @doc(s_search_by_sell_date)
    @BaseApi.timing_decorator
    def search_by_sell_date(self):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "time": [
                self.get_the_date(-1),
                self.get_the_date()
            ],
            "startSaleTime": self.get_the_date(-1),
            "endSaleTime": self.get_the_date()
        }
        return self._make_request('post', 'sell_sale_item_list', data, 'main')

    @doc(s_search_by_user_id)
    @BaseApi.timing_decorator
    def search_by_user_id(self):
        ParamCache.cache_object({"userId": INFO['main_user_id']}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "saleUserId": INFO['main_user_id']
        }
        return self._make_request('post', 'sell_sale_item_list', data, 'main')


class SellCustomManageRequest(InitializeParams):
    """商品销售|客户管理"""

    @doc(s_sell_after_sale_by_articles_no)
    @BaseApi.timing_decorator
    def sell_after_sale_by_articles_no(self):
        res = self.pc.sell_after_sales_list_data(data='a')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesNoOrImei": res[0]['articlesNo'],
            "saleStatus": "4"
        }
        return self._make_request('post', 'sales_aftermarket_list', data, 'main')


class SellStaticsRequest(InitializeParams):
    """商品销售|数据统计"""

    @doc(s_sell_statics_search_by_sale_custom)
    @BaseApi.timing_decorator
    def sell_statics_search_by_sale_custom(self):
        ParamCache.cache_object({"saleSupplierId": INFO['main_sale_supplier_id']}, 'practical.json')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "saleSupplierId": [INFO['main_sale_supplier_id']],
        }
        return self._make_request('post', 'sell_statics', data, 'main')


class SellSalesListRequest(InitializeParams):
    """商品销售|销售售后管理|销售售后列表"""

    @BaseApi.timing_decorator
    def item_number(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='15')
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'set_articles_no', data, 'main', nocheck)

    @doc(s_sell_after_sale_attachment)
    @BaseApi.timing_decorator
    def sell_after_sale_attachment(self, nocheck=False):
        res = self.pc.sell_after_sales_list_data(data='a')
        data = {
            "saleType": 2,
            "orderNo": res[0]['orderNo'],
            "saleUserId": INFO['main_sale_supplier_id'],
            "saleUserName": INFO['vice_sales_customer_name'],
            "sellSaleOrderArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo']
                }
            ],
            "ids": [
                res[0]['id']
            ],
            "articlesNoOrImei": res[0]['articlesNo'],
            "logisticsNo": res[0]['logisticsNo'],
            "warehouseId": INFO['main_in_warehouse_id']
        }
        return self._make_request('post', 'update_sale_status', data, 'main', nocheck)

    @doc(s_sell_after_sale_refund)
    @BaseApi.timing_decorator
    def sell_after_sale_refund(self, nocheck=False):
        res = self.pc.sell_after_sales_list_data(data='a')
        data = {
            "fineSalePrice": 100,
            "saleType": 4,
            "remark": "备注",
            "orderNo": res[0]['orderNo'],
            "saleUserId": INFO['main_sale_supplier_id'],
            "saleUserName": INFO['vice_sales_customer_name'],
            "sellSaleOrderArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo']
                }
            ],
            "ids": [
                res[0]['id']
            ],
            "articlesNoOrImei": res[0]['articlesNo']
        }
        return self._make_request('post', 'update_sale_status', data, 'main', nocheck)

    @doc(s_sell_after_sale_barter)
    @BaseApi.timing_decorator
    def sell_after_sale_barter(self, nocheck=False):
        res = self.pc.sell_after_sales_list_data(data='a')
        res_2 = self.pc.inventory_list_data(i='2', j='3')
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "saleUserId": INFO['main_sale_supplier_id'],
            "offExpressage": "0",
            "saleType": "7",
            "purchaseOrdersArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "remark": None,
                    "saleSettlePrice": 21
                }
            ],
            "newPurchaseOrdersArticlesDTO": {
                "articlesNo": res_2[0]['articlesNo'],
                "imei": res_2[0]['imei'],
                "newSalePrice": 60,
                "platformArticlesNo": self.serial,
                "platformOrderNo": self.serial,
                "remark": "",
                "costPrice": 130
            },
            "isSaleType": True
        }
        return self._make_request('post', 'sell_after_sale_out_stock', data, 'main', nocheck)

    @doc(s_sell_after_sale_refusal_return)
    @BaseApi.timing_decorator
    def sell_after_sale_refusal_return(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='15')
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "saleUserId": INFO['main_sale_supplier_id'],
            "offExpressage": "0",
            "logisticsNo": self.jd,
            "logisticsPrice": "11",
            "saleType": "6",
            "purchaseOrdersArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "remark": None,
                    "saleSettlePrice": 24
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

    @doc(s_sell_after_sale_by_articles_no)
    @BaseApi.timing_decorator
    def sell_after_sale_by_articles_no(self):
        res = self.pc.sell_after_sales_list_data(data='a')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesNoOrImei": res[0]['articlesNo'],
            "saleStatus": "4"
        }
        return self._make_request('post', 'sales_aftermarket_list', data, 'main')

    @doc(s_sell_after_sale_by_platform_articles_no)
    @BaseApi.timing_decorator
    def sell_after_sale_by_platform_articles_no(self):
        res = self.pc.sell_after_sales_list_data(data='a')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "platformArticlesNo": res[0]['purchasePlatformArticlesNo'],
            "saleStatus": "4"
        }
        return self._make_request('post', 'sales_aftermarket_list', data, 'main')

    @doc(s_sell_after_sale_by_sale_order_no)
    @BaseApi.timing_decorator
    def sell_after_sale_by_sale_order_no(self):
        res = self.pc.sell_after_sales_list_data(data='a')
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "orderNo": res[0]['orderNo'],
            "saleStatus": "4"
        }
        return self._make_request('post', 'sales_aftermarket_list', data, 'main')

    @doc(s_sell_after_sale_by_sale_user_id)
    @BaseApi.timing_decorator
    def sell_after_sale_by_sale_user_id(self):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "saleUserId": INFO['main_sale_supplier_id'],
            "saleStatus": "4"
        }
        return self._make_request('post', 'sales_aftermarket_list', data, 'main')

    @doc(s_sell_after_sale_by_sale_type)
    @BaseApi.timing_decorator
    def sell_after_sale_by_sale_type(self):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "saleTypes": [1],
            "saleStatus": "4"
        }
        return self._make_request('post', 'sales_aftermarket_list', data, 'main')

    @doc(s_sell_after_sale_by_create_time)
    @BaseApi.timing_decorator
    def sell_after_sale_by_create_time(self):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "saleStatus": "4",
            "time": [
                self.get_the_date(),
                self.get_the_date()
            ],
            "startSaleTime": self.get_the_date(),
            "endSaleTime": self.get_the_date()
        }
        return self._make_request('post', 'sales_aftermarket_list', data, 'main')

    @doc(s_sell_after_sale_by_return_type)
    @BaseApi.timing_decorator
    def sell_after_sale_by_return_type(self):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "saleStatus": "4",
            "returnType": 1,
        }
        return self._make_request('post', 'sales_aftermarket_list', data, 'main')

    @doc(s_sell_after_sale_by_is_sale_channel)
    @BaseApi.timing_decorator
    def sell_after_sale_by_is_sale_channel(self):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "saleStatus": "4",
            "isSaleChannel": 0,
        }
        return self._make_request('post', 'sales_aftermarket_list', data, 'main')

    @doc(s_sell_after_sale_repair)
    @BaseApi.timing_decorator
    def sell_after_sale_repair(self, nocheck=False):
        res = self.pc.sell_after_sales_list_data(data='a')
        data = {
            "articlesNoList": [
                res[0]['articlesNo'],
            ],
            "saleUserId": INFO['main_sale_supplier_id'],
            "offExpressage": "0",
            "logisticsNo": self.jd,
            "logisticsPrice": "321",
            "saleType": "3",
            "purchaseOrdersArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "remark": None,
                    "saleSettlePrice": 34
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


class SellWaitReceivedRequest(InitializeParams):
    """商品销售|销售管理|待接收物品"""

    @BaseApi.timing_decorator
    def wait_received_one_search_by_imei(self):
        res = self.pc.sell_goods_received_data()
        obj = res[0]['imei']
        ParamCache.cache_object({"imei": obj}, 'practical.json')
        data = {"pageNum": 1, "pageSize": 10, "articlesState": 13, "articlesType": "1", "articlesNo": obj}
        return self._make_request('post', 'inventory_receive_items', data, 'main')

    @BaseApi.timing_decorator
    def wait_received_one_search_by_date(self):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesState": 13,
            "articlesType": "1",
            "erpStartTime": self.get_the_date(-1),
            "erpEndTime": self.get_the_date()
        }
        return self._make_request('post', 'inventory_receive_items', data, 'main')


class SellingOrderListRequest(InitializeParams):
    """商品销售|销售管理|销售中订单列表"""

    @BaseApi.timing_decorator
    def selling_order_search_by_batch_no(self):
        res = self.pc.selling_order_list_data()
        obj = res[0]['batchNo']
        ParamCache.cache_object({"batchNo": obj}, 'practical.json')
        data = {
            "batchNo": obj,
            "pageNum": 1,
            "pageSize": 10
        }
        return self._make_request('post', 'order_list_for_sale', data, 'main')

    @BaseApi.timing_decorator
    def selling_order_search_by_type(self):
        type = 2
        ParamCache.cache_object({"type": type}, 'practical.json')
        data = {
            "type": type,
            "pageNum": 1,
            "pageSize": 10
        }
        return self._make_request('post', 'order_list_for_sale', data, 'main')

    @BaseApi.timing_decorator
    def selling_order_search_by_sale_supplier_id(self):
        sale_supplier_id = INFO['main_sale_supplier_id']
        ParamCache.cache_object({"saleSupplierId": sale_supplier_id}, 'practical.json')
        data = {
            "saleSupplierId": sale_supplier_id,
            "pageNum": 1,
            "pageSize": 10
        }
        return self._make_request('post', 'order_list_for_sale', data, 'main')

    @BaseApi.timing_decorator
    def selling_order_search_by_sale_user_id(self):
        sale_user_id = INFO['main_user_id']
        ParamCache.cache_object({"saleUserId": sale_user_id}, 'practical.json')
        data = {
            "saleUserId": sale_user_id,
            "pageNum": 1,
            "pageSize": 10
        }
        return self._make_request('post', 'order_list_for_sale', data, 'main')

    @BaseApi.timing_decorator
    def selling_order_search_by_logistics_no(self):
        res = self.pc.selling_order_list_data()
        obj = res[0]['logisticsNo']
        ParamCache.cache_object({"logisticsNo": obj}, 'practical.json')
        data = {
            "logisticsNo": obj,
            "pageNum": 1,
            "pageSize": 10
        }
        return self._make_request('post', 'order_list_for_sale', data, 'main')

    @BaseApi.timing_decorator
    def selling_order_search_by_sale_date(self):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "startTime": self.get_the_date(-1),
            "endTime": self.get_the_date()
        }
        return self._make_request('post', 'order_list_for_sale', data, 'main')

    @BaseApi.timing_decorator
    def wait_received_one_search_by_date(self):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesState": 13,
            "articlesType": "1",
            "erpStartTime": self.get_the_date(-1),
            "erpEndTime": self.get_the_date()
        }
        return self._make_request('post', 'inventory_receive_items', data, 'main')


if __name__ == '__main__':
    api = None
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
