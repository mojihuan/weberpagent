# coding: utf-8
from common.base_api import BaseApi
from common.base_params import InitializeParams
from config.user_info import INFO
from common.import_desc import *

qualityCategoryList = BaseApi.load_json_file('request_quality.json')['qualityCategoryList']
optionIdList = BaseApi.load_json_file('request_quality.json')['optionIdList']
backfillList = BaseApi.load_json_file('request_quality.json')['backfillList']


class TraffickerHelpRequest(InitializeParams):
    """首页|帮卖"""

    @doc(t_execute_one_click_help)
    def execute_one_click_help(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='3')
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "helpSellTenantId": INFO['main_help_sell_tenant_id'],
            "batchRemark": "备注",
            "settlementType": 1
        }
        return self._make_request('post', 'one_click_submit', data, 'main', nocheck)

    @doc(t_guaranteed_sale_buyout)
    def guaranteed_sale_buyout(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='3')
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "batchRemark": "",
            "helpSellTenantId": INFO['main_help_sell_tenant_id'],
            "settlementType": 2
        }

        return self._make_request('post', 'one_click_submit', data, 'main', nocheck)

    @doc(t_guaranteed_sales_and_profit_sharing)
    def guaranteed_sales_and_profit_sharing(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='3')
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "batchRemark": "",
            "helpSellTenantId": INFO['main_help_sell_tenant_id'],
            "settlementType": 3
        }
        return self._make_request('post', 'one_click_submit', data, 'main', nocheck)

    @doc(t_express_delivery_is_easy_to_ship)
    def express_delivery_is_easy_to_ship(self, nocheck=False):
        res = self.pc.help_generate_order_data(i='wsg')
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

        return self._make_request('post', 'help_sell_add', data, 'main', nocheck)

    @doc(t_self_mailing)
    def self_mailing(self, nocheck=False):
        res = self.pc.help_generate_order_data(i='wsg')
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
        return self._make_request('post', 'help_sell_add', data, 'main', nocheck)

    @doc(t_deliver_it_yourself)
    def deliver_it_yourself(self, nocheck=False):
        res = self.pc.help_generate_order_data(i='wsg')
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
        return self._make_request('post', 'help_sell_add', data, 'main', nocheck)

    @doc(t_quality_inspection_retirement)
    def quality_inspection_retirement(self, nocheck=False):
        res = self.pc.help_generate_order_data(i='wr')
        data = {
            "orderNoList": [
                res[0]['orderNo']
            ]
        }
        return self._make_request('post', 'apply_for_cancellation', data, 'main', nocheck)

    @doc(t_pending_confirmation_request_to_withdraw)
    def pending_confirmation_request_to_withdraw(self, nocheck=False):
        res = self.pc.help_generate_order_data(i='wb')
        data = {
            "orderNoList": [
                res[0]['orderNo']
            ]
        }
        return self._make_request('post', 'apply_for_cancellation', data, 'main', nocheck)

    @doc(t_negotiate_a_refund_request)
    def negotiate_a_refund_request(self, nocheck=False):
        res = self.pc.help_generate_order_data(i='wbi')
        data = {
            "orderNoList": [
                res[0]['orderNo']
            ]
        }
        return self._make_request('post', 'apply_for_cancellation', data, 'main', nocheck)

    @doc(t_for_sale_request_to_withdraw)
    def for_sale_request_to_withdraw(self, nocheck=False):
        res = self.pc.help_generate_order_data(i='wsr')
        data = {
            "orderNoList": [
                res[0]['orderNo']
            ]
        }
        return self._make_request('post', 'apply_for_cancellation', data, 'main', nocheck)

    @doc(t_negotiation_confirm_the_guarantee_of_sale)
    def negotiation_confirm_the_guarantee_of_sale(self, nocheck=False):
        res = self.pc.help_generate_order_data(i='wb')
        data = {
            "orderNo": res[0]['orderNo'],
            "description": "备注"
        }
        return self._make_request('post', 'apply_for_bargaining', data, 'main', nocheck)

    @doc(t_pending_departure_cancel_the_departure)
    def pending_departure_cancel_the_departure(self, nocheck=False):
        res = self.pc.help_generate_order_data(i='wrg')
        data = {
            "orderNoList": [
                res[0]['orderNo']
            ]
        }
        return self._make_request('post', 'help_sell_cancel_back', data, 'main', nocheck)

    @doc(t_manual_sign_in_during_exit)
    def manual_sign_in_during_exit(self, nocheck=False):
        res = self.pc.help_generate_order_data(i='rig')
        data = {
            "orderIdList": [
                res[0]['orderNo']
            ]
        }
        return self._make_request('post', 'help_sell_sign_in', data, 'main', nocheck)

    @doc(t_logistics_signing_during_retirement)
    def logistics_signing_during_retirement(self, nocheck=False):
        res = self.pc.help_generate_order_data(i='rig')
        res_2 = self.pc.inventory_logistics_list_data()
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
        return self._make_request('post', 'sign_in_warehouse', data, 'main', nocheck)


class TraffickerInventoryRequest(InitializeParams):
    """首页|库存"""

    @doc(t_individual_item_counting)
    def create_a_new_inventory_count(self, nocheck=False):
        data = {
            'stockUserId': -1
        }
        return self._make_request('post', 'inventory_count_add', data, 'main', nocheck)

    @doc(t_individual_item_counting)
    def submit_an_inventory_count(self, nocheck=False):
        res = self.pc.inventory_list_data()
        res_2 = self.pc.inventory_count_data()
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "stockNo": res_2[0]['stockNo']
        }
        return self._make_request('post', 'inventory_count_submit', data, 'main', nocheck)

    @doc(t_individual_item_counting)
    def individual_item_counting(self, nocheck=False):
        self.create_a_new_inventory_count()
        self.submit_an_inventory_count()
        res = self.pc.inventory_count_data()
        data = {
            "stockNo": res[0]['stockNo']
        }
        return self._make_request('post', 'inventory_count_complete', data, 'main', nocheck)

    @doc(t_handover_for_quality_inspection)
    def handover_for_quality_inspection(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='3')
        data = {
            "type": "1",
            "userId": INFO['main_user_id'],
            "remark": "",
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "createBy": INFO['super_admin_account']
        }
        return self._make_request('post', 'hand_over_operate', data, 'main', nocheck)

    @doc(t_handover_for_maintenance)
    def handover_for_maintenance(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='3')
        data = {
            "type": "2",
            "userId": INFO['main_user_id'],
            "remark": "",
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "createBy": INFO['super_admin_account']
        }
        return self._make_request('post', 'hand_over_operate', data, 'main', nocheck)

    @doc(t_transfer_for_repair)
    def transfer_for_repair(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='3')
        data = {
            "type": "3",
            "userId": INFO['main_user_id'],
            "remark": "",
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "createBy": INFO['super_admin_account']
        }
        return self._make_request('post', 'hand_over_operate', data, 'main', nocheck)

    @doc(t_transfer_for_sales)
    def transfer_for_sales(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='3')
        data = {
            "type": "4",
            "userId": INFO['main_user_id'],
            "remark": "",
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "createBy": INFO['super_admin_account']
        }
        return self._make_request('post', 'hand_over_operate', data, 'main', nocheck)

    @doc(t_transfer_for_purchasing_after_sales)
    def transfer_for_purchasing_after_sales(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='3')
        data = {
            "type": "5",
            "userId": INFO['main_user_id'],
            "remark": "",
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "createBy": INFO['super_admin_account']
        }
        return self._make_request('post', 'hand_over_operate', data, 'main', nocheck)

    @doc(t_transfer_for_stock)
    def transfer_for_stock(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='3')
        data = {
            "type": "6",
            "userId": INFO['main_user_id'],
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "createBy": INFO['super_admin_account']
        }
        return self._make_request('post', 'hand_over_operate', data, 'main', nocheck)

    @doc(t_sign_in_warehouse)
    def sign_in_warehouse(self, nocheck=False):
        res = self.pc.inventory_logistics_list_data()
        res_2 = self.pc.inventory_logistics_into_warehouse_data()
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
        return self._make_request('post', 'sign_in_warehouse', data, 'main', nocheck)

    @doc(t_sign_in_warehouse_in_quality)
    def sign_in_warehouse_in_quality(self, nocheck=False):
        res = self.pc.inventory_logistics_list_data()
        res_2 = self.pc.inventory_logistics_into_warehouse_data()
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
        return self._make_request('post', 'sign_in_warehouse', data, 'main', nocheck)

    @doc(t_sign_in_warehouse_in_repair)
    def sign_in_warehouse_in_repair(self, nocheck=False):
        res = self.pc.inventory_logistics_list_data()
        res_2 = self.pc.inventory_logistics_into_warehouse_data()
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
        return self._make_request('post', 'sign_in_warehouse', data, 'main', nocheck)

    @doc(t_sign_in_warehouse_in_send)
    def sign_in_warehouse_in_send(self, nocheck=False):
        res = self.pc.inventory_logistics_list_data()
        res_2 = self.pc.inventory_logistics_into_warehouse_data()
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
        return self._make_request('post', 'sign_in_warehouse', data, 'main', nocheck)

    @doc(t_sign_in_warehouse_in_sell)
    def sign_in_warehouse_in_sell(self, nocheck=False):
        res = self.pc.inventory_logistics_list_data()
        res_2 = self.pc.inventory_logistics_into_warehouse_data()
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
        return self._make_request('post', 'sign_in_warehouse', data, 'main', nocheck)

    @doc(t_sign_in_warehouse_in_purchase)
    def sign_in_warehouse_in_purchase(self, nocheck=False):
        res = self.pc.inventory_logistics_list_data()
        res_2 = self.pc.inventory_logistics_into_warehouse_data()
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
        return self._make_request('post', 'sign_in_warehouse', data, 'main', nocheck)

    @doc(t_sign_in_warehouse_in_inventory)
    def sign_in_warehouse_in_inventory(self, nocheck=False):
        res = self.pc.inventory_logistics_list_data()
        res_2 = self.pc.inventory_logistics_into_warehouse_data()
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
        return self._make_request('post', 'sign_in_warehouse', data, 'main', nocheck)

    @doc(t_receive_items_in_sell)
    def receive_items_in_sell(self, nocheck=False):
        res = self.pc.sell_goods_received_data()
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'mg_receive_items', data, 'main', nocheck)

    @doc(t_sign_into_the_library)
    def sign_into_the_library(self, nocheck=False):
        res = self.pc.inventory_logistics_list_data()
        res_2 = self.pc.inventory_logistics_into_warehouse_data()
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
        return self._make_request('post', 'sign_in_warehouse', data, 'main', nocheck)


class TraffickerPurchaseRequest(InitializeParams):
    """首页|采购"""

    @doc(t_purchase_orders)
    def purchase_orders(self, nocheck=False):
        res = self.pc.inventory_list_data(i=1)
        res_2 = self.pc.inventory_logistics_list_data()
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
        return self._make_request('post', 'sign_in_warehouse', data, 'main', nocheck)

    @doc(t_purchase_orders_in_quality)
    def purchase_orders_in_quality(self, nocheck=False):
        res = self.pc.inventory_list_data(i=1)
        res_2 = self.pc.inventory_logistics_list_data()
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
        return self._make_request('post', 'sign_in_warehouse', data, 'main', nocheck)

    @doc(t_add_smartwatch_arrived_unpaid)
    def add_smartwatch_arrived_unpaid(self, nocheck=False):
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
        return self._make_request('post', 'add_purchase_order', data, 'main', nocheck)

    @doc(t_add_mobile_handover_repair)
    def add_mobile_handover_repair(self, nocheck=False):
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

        return self._make_request('post', 'add_purchase_order', data, 'main', nocheck)


class TraffickerQualityRequest(InitializeParams):
    """首页|质检"""

    @doc(t_submit_the_quality_inspection_results)
    def submit_the_quality_inspection_results(self, nocheck=False):
        res = self.pc.quality_centre_item_data()
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
        return self._make_request('post', 'submit_quality_results', data, 'main', nocheck)

    @doc(t_fast_quality_inspection)
    def fast_quality_inspection(self, nocheck=False):
        res = self.pc.quality_centre_item_data()
        res_2 = self.pc.inventory_list_data(i=2, j=5)
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
        return self._make_request('post', 'submit_quality_results', data, 'main', nocheck)

    @doc(t_new_quality_inspection_form)
    def new_quality_inspection_form(self, nocheck=False):
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
        return self._make_request('post', 'quality_add', data, 'main', nocheck)

    @doc(t_quality_complete_purchase_warehousing)
    def quality_complete_purchase_warehousing(self, nocheck=False):
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
        return self._make_request('post', 'submit_quality_results', data, 'main', nocheck)


class TraffickerRepairRequest(InitializeParams):
    """首页|维修"""

    @doc(t_repair_items_in_repair)
    def repair_items_in_repair(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='7')
        res_2 = self.pc.attachment_inventory_list_data(i='2', j='1', k=1, l='17569')
        res_3 = self.pc.repair_project_list_data(i=1, data='a')
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
        return self._make_request('post', 'handover_repair', data, 'main', nocheck)


class TraffickerSellRequest(InitializeParams):
    """首页|销售"""

    @doc(t_partial_receipt_of_sales_outbound)
    def partial_receipt_of_sales_outbound(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='13')
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
        return self._make_request('post', 'sale_out', data, 'main', nocheck)

    @doc(t_sales_out_of_the_warehouse_in_full)
    def sales_out_of_the_warehouse_in_full(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='13')
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
        return self._make_request('post', 'sale_out', data, 'main', nocheck)

    @doc(t_sales_outbound_add_accessories)
    def sales_outbound_add_accessories(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='13')
        res_2 = self.pc.attachment_inventory_list_data(i='2')
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
        return self._make_request('post', 'sale_out', data, 'main', nocheck)

    @doc(t_sales_outbound_new_customer)
    def sales_outbound_new_customer(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='13')
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
        return self._make_request('post', 'sale_out', data, 'main', nocheck)

    @doc(t_sales_outbound_express_easy)
    def sales_outbound_express_easy(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='13')
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
        return self._make_request('post', 'sale_out', data, 'main', nocheck)


if __name__ == '__main__':
    api = TraffickerHelpRequest()
    result = api.execute_one_click_help()
    print(result)
