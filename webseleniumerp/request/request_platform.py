# coding: utf-8
import json
from common.base_api import BaseApi
from common.base_params import InitializeParams, is_performance_close
from common.file_cache_manager import ParamCache
from common.import_desc import *
from config.user_info import INFO


class PlatformAuctionProductManageRequest(InitializeParams):
    """平台管理|虚拟库存|上拍商品管理"""

    @doc(p_select_the_session_to_add_product_confirm)
    @BaseApi.timing_decorator
    def select_the_session_to_add_product_confirm(self, nocheck=False):
        res = self.pc.platform_auction_product_manage_data(i=1)
        res_2 = self.pc.platform_auction_product_manage_data(data='a', i=1)
        data = {
            "sessionId": res_2[0]['id'],
            "marketId": res_2[0]['marketId'],
            "articlesNoList": [
                res[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'auction_session_details_add_products', data, 'super', nocheck)

    @doc(p_direct_auction_add_items_to_the_shelves)
    @BaseApi.timing_decorator
    def direct_auction_add_items_to_the_shelves(self, nocheck=False):
        res = self.pc.platform_auction_product_manage_data(i=1)
        res_2 = self.pc.platform_auction_product_manage_data(data='a', i=2)
        data = {
            "sessionId": res_2[0]['id'],
            "marketId": res_2[0]['marketId'],
            "articlesNoList": [
                res[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'auction_session_details_add_products', data, 'super', nocheck)

    @doc(p_guaranteed_sale_cancellation_of_sale)
    @BaseApi.timing_decorator
    def guaranteed_sale_cancellation_of_sale(self, nocheck=False):
        res = self.pc.platform_auction_product_manage_data(i=1)
        obj = res[0]['articlesId']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": res[0]['id']
        }
        return self._make_request('post', 'cancel_the_sale', data, 'super', nocheck)

    @doc(p_secret_shooting_modification_sessions)
    @BaseApi.timing_decorator
    def secret_shooting_modification_sessions(self, nocheck=False):
        res = self.pc.platform_auction_product_manage_data(i=1)
        res_2 = self.pc.platform_auction_product_manage_data(data='a', i=2)
        data = {
            "sessionId": res_2[0]['id'],
            "marketId": res_2[0]['marketId'],
            "articlesNo": res[0]['articlesNo'],
            "oldSessionId": res_2[1]['id'],
        }
        return self._make_request('post', 'modify_the_session', data, 'super', nocheck)

    @doc(p_cancel_the_auction)
    @BaseApi.timing_decorator
    def cancel_the_auction(self, nocheck=False):
        res = self.pc.platform_auction_product_manage_data(i=2)
        data = {
            "id": res[0]['id']
        }
        return self._make_request('post', 'cancel_the_auction', data, 'super', nocheck)


class PlatformItemsToBeSpecifiedRequest(InitializeParams):
    """平台管理|运营中心|待指定物品"""

    @doc(p_designated_recyclers)
    @BaseApi.timing_decorator
    def designated_recyclers(self, nocheck=False):
        res = self.pc.platform_items_to_be_specified_data()
        data = {
            "assignTenantId": INFO['merchant_id'],
            "id": res[-1]['id']
        }
        return self._make_request('post', 'wait_for_specification', data, 'super', nocheck)

    @doc(p_modify_the_recycler)
    @BaseApi.timing_decorator
    def modify_the_recycler(self, nocheck=False):
        res = self.pc.platform_items_to_be_specified_data()
        data = {
            "assignTenantId": INFO['merchant_id'],
            "id": res[-1]['id']
        }
        return self._make_request('post', 'wait_for_specification', data, 'super', nocheck)


class PlatformListOfDarkAuctionHousesRequest(InitializeParams):
    """"平台管理|卖场管理|暗拍卖场列表"""

    @doc(p_price_priority_for_close_proximity)
    def price_priority_for_close_proximity(self, nocheck=False):
        data = {
            "name": self.mixed_random,
            "desc": '卖场描述' + self.mixed_random,
            "sort": 11,
            "marketCategory": 1,
            "marketType": 1,
            "sessionFrequency": 0,
            "sessionNum": 1,
            "marketActivityList": self.generate_five_minute_sessions(),
            "auctionMarketRuleConfig": {
                "countdownType": 1,
                "merchantLimitList": [
                    3,
                    4
                ],
                "conditionType": 1,
                "lockType": 1,
                "winRuleType": 2,
                "depositType": 1,
                "rangeLimit": 44,
                "failedSessionRule": 2,
                "failedNum": 3,
                "depositPrice": 999,
                "timer": ""
            },
            "auctionMarketArticlesRuleConfig": {
                "minMum": 1,
                "maxMum": 11111,
                "autoAssignType": 1,
                "countdownType": 1,
                "auctionAutoAssignTypeList": [
                    {
                        "categoryId": "",
                        "brandId": "",
                        "modelIdList": [],
                        "finenessIdList": []
                    }
                ]
            },
            "marketTimeType": 2,
            "isEnable": False,
            "activityStartTime": f"{self.get_the_date()} 00:00:00",
            "activityEndTime": f"{self.get_the_date(days=+20)} 00:00:00"
        }
        return self._make_request('post', 'auction_add_stores', data, 'super', nocheck)

    @doc(p_every_day_on_a_expired_phone)
    def every_day_on_a_expired_phone(self, nocheck=False):
        data = {
            "name": self.mixed_random,
            "desc": "卖场描述" + self.mixed_random,
            "sort": 11,
            "marketCategory": 1,
            "marketType": 1,
            "sessionFrequency": 0,
            "sessionNum": 1,
            "marketActivityList": self.generate_hourly_sessions(),
            "auctionMarketRuleConfig": {
                "countdownType": 1,
                "merchantLimitList": [
                    3,
                    4
                ],
                "conditionType": 1,
                "lockType": 1,
                "winRuleType": 2,
                "depositType": 1,
                "rangeLimit": 44,
                "failedSessionRule": 2,
                "failedNum": 3,
                "depositPrice": 999,
                "timer": ""
            },
            "auctionMarketArticlesRuleConfig": {
                "minMum": 1,
                "maxMum": 10000,
                "autoAssignType": 1,
                "countdownType": 1,
                "auctionAutoAssignTypeList": [
                    {
                        "categoryId": 1,
                        "brandId": 1,
                        "modelIdList": [
                            9232
                        ],
                        "finenessIdList": [
                            130
                        ],
                        "minValue": 1,
                        "maxValue": 10000
                    }
                ]
            },
            "marketTimeType": 2,
            "isEnable": True,
            "activityStartTime": f"{self.get_the_date()} 00:00:00",
            "activityEndTime": f"{self.get_the_date(days=+20)} 00:00:00"
        }
        return self._make_request('post', 'auction_add_stores', data, 'super', nocheck)

    @doc(p_create_five_minute_auction_session)
    def create_five_minute_auction_session(self, nocheck=False):
        sessions = self.generate_five_minute_sessions()
        data = {
            "name": self.mixed_random,
            "desc": "卖场描述" + self.mixed_random,
            "marketCategory": 1,
            "marketType": 1,
            "sessionFrequency": 0,
            "sessionNum": len(sessions),
            "marketActivityList": sessions,
            "auctionMarketRuleConfig": {
                "countdownType": 1,
                "merchantLimitList": [
                    3,
                    4
                ],
                "conditionType": 1,
                "lockType": 1,
                "winRuleType": 2,
                "depositType": 1,
                "rangeLimit": 44,
                "failedSessionRule": 2,
                "failedNum": 3,
                "depositPrice": 999,
                "timer": ""
            },
            "auctionMarketArticlesRuleConfig": {
                "autoAssignType": 1,
                "minMum": 1,
                "maxMum": 10000,
                "countdownType": 1,
                "auctionAutoAssignTypeList": [
                    {
                        "categoryId": "",
                        "brandId": "",
                        "modelIdList": [],
                        "finenessIdList": []
                    }
                ]
            },
            "sort": 1,
            "marketTimeType": 1,
            "isEnable": True
        }
        return self._make_request('post', 'auction_add_stores', data, 'super', nocheck)

    @doc(p_modify_the_store_event_time)
    def modify_the_store_event_time(self, nocheck=False):
        res = self.pc.platform_list_of_dark_auction_houses_data(i=3)
        data = {
            "name": self.mixed_random,
            "desc": "卖场描述" + self.mixed_random,
            "sort": 11,
            "marketCategory": 1,
            "marketType": 1,
            "sessionFrequency": 0,
            "sessionNum": 15,
            "marketActivityList": self.generate_five_minute_sessions(),
            "auctionMarketRuleConfig": {
                "countdownType": 1,
                "merchantLimitList": [
                    3,
                    4
                ],
                "conditionType": 1,
                "lockType": 1,
                "winRuleType": 2,
                "depositType": 1,
                "rangeLimit": 44,
                "failedSessionRule": 2,
                "failedNum": 3,
                "depositPrice": 999,
                "timer": ""
            },
            "auctionMarketArticlesRuleConfig": {
                "minMum": 1,
                "maxMum": 10000,
                "autoAssignType": 1,
                "countdownType": 1,
                "auctionAutoAssignTypeList": [
                    {
                        "categoryId": 1,
                        "brandId": 1,
                        "modelIdList": [
                            9232
                        ],
                        "finenessIdList": [
                            130
                        ],
                        "minValue": 1,
                        "maxValue": 10000
                    }
                ]
            },
            "id": res[0]['id'],
            "marketTimeType": 2,
            "isEnable": True,
            "activityStartTime": f"{self.get_the_date()} 00:00:00",
            "activityEndTime": f"{self.get_the_date(days=+20)} 00:00:00"
        }
        return self._make_request('post', 'auction_edit_stores', data, 'super', nocheck)

    @doc(p_save_and_list_is_modified_to_save_only)
    def save_and_list_is_modified_to_save_only(self, nocheck=False):
        res = self.pc.platform_list_of_dark_auction_houses_data(i=3)
        data = {
            "id": res[0]['id']
        }
        return self._make_request('post', 'auction_re_listing', data, 'super', nocheck)

    @doc(p_listed_status_removed_from_the_store)
    def listed_status_removed_from_the_store(self, nocheck=False):
        res = self.pc.platform_list_of_dark_auction_houses_data(i=1)
        data = {
            "id": res[0]["id"]
        }
        return self._make_request('post', 'auction_down_stores', data, 'super', nocheck)

    @doc(p_add_goods_mobile_phones)
    def add_goods_mobile_phones(self, nocheck=False):
        res = self.pc.platform_list_of_dark_auction_houses_data(i=1)
        res_2 = self.pc.platform_list_of_dark_auction_houses_data(data='b')
        res_3 = self.pc.platform_list_of_dark_auction_houses_data(data='c')
        data = {
            "sessionId": res_2[0]['id'],
            "marketId": res[0]['id'],
            "articlesNoList": [
                res_3[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'auction_session_details_add_products', data, 'super', nocheck)

    @doc(p_pending_status_listed)
    def pending_status_listed(self, nocheck=False):
        res = self.pc.platform_list_of_dark_auction_houses_data(i=2)
        data = {
            'id': res[0]['id']
        }
        return self._make_request('post', 'auction_shelves', data, 'super', nocheck)

    @doc(p_pending_status_edit_save_and_list)
    def pending_status_edit_save_and_list(self, nocheck=False):
        res = self.pc.platform_list_of_dark_auction_houses_data(i=2)
        data = {
            "name": self.mixed_random,
            "desc": '卖场描述' + self.mixed_random,
            "sort": 1,
            "marketCategory": 1,
            "marketTimeType": 2,
            "marketType": 1,
            "sessionFrequency": 0,
            "sessionNum": 15,
            "marketActivityList": self.generate_five_minute_sessions(),
            "auctionMarketRuleConfig": {
                "countdownType": 1,
                "merchantLimitList": [
                    3,
                    4
                ],
                "conditionType": 1,
                "lockType": 1,
                "winRuleType": 2,
                "depositType": 1,
                "rangeLimit": 44,
                "failedSessionRule": 2,
                "failedNum": 3,
                "depositPrice": 999,
                "timer": ""
            },
            "auctionMarketArticlesRuleConfig": {
                "minMum": 3,
                "maxMum": 100,
                "autoAssignType": 1,
                "countdownType": 1,
                "auctionAutoAssignTypeList": [
                    {
                        "categoryId": 3,
                        "brandId": 802,
                        "modelIdList": [
                            18031
                        ],
                        "finenessIdList": [
                            108,
                            109
                        ],
                        "minValue": 199
                    }
                ]
            },
            "id": res[0]['id'],
            "isEnable": True,
            "activityStartTime": f"{self.get_the_date()} 00:00:00",
            "activityEndTime": f"{self.get_the_date(days=7)} 00:00:00",
        }
        return self._make_request('post', 'auction_edit_stores', data, 'super', nocheck)

    @doc(p_pending_status_deleted)
    def pending_status_deleted(self, nocheck=False):
        res = self.pc.platform_list_of_dark_auction_houses_data(i=2)
        data = {
            "id": res[0]["id"]
        }
        return self._make_request('post', 'auction_deletion', data, 'super', nocheck)

    @doc(p_delisted_edit_save_and_list)
    def delisted_edit_save_and_list(self, nocheck=False):
        res = self.pc.platform_list_of_dark_auction_houses_data(i=3)
        data = {
            "name": self.mixed_random,
            "desc": '卖场描述' + self.mixed_random,
            "sort": 1,
            "marketCategory": 1,
            "marketTimeType": 2,
            "marketType": 1,
            "sessionFrequency": 0,
            "sessionNum": 15,
            "marketActivityList": self.generate_five_minute_sessions(),
            "auctionMarketRuleConfig": {
                "countdownType": 1,
                "merchantLimitList": [
                    3,
                    4
                ],
                "conditionType": 1,
                "lockType": 1,
                "winRuleType": 2,
                "depositType": 1,
                "rangeLimit": 44,
                "failedSessionRule": 2,
                "failedNum": 3,
                "depositPrice": 999,
                "timer": ""
            },
            "auctionMarketArticlesRuleConfig": {
                "minMum": 3,
                "maxMum": 100,
                "autoAssignType": 1,
                "countdownType": 1,
                "auctionAutoAssignTypeList": [
                    {
                        "categoryId": 3,
                        "brandId": 802,
                        "modelIdList": [
                            18031
                        ],
                        "finenessIdList": [
                            108,
                            109
                        ],
                        "minValue": 199
                    }
                ]
            },
            "id": res[0]['id'],
            "isEnable": True,
            "activityStartTime": f"{self.get_the_date()} 00:00:00",
            "activityEndTime": f"{self.get_the_date(days=7)} 00:00:00"
        }

        return self._make_request('post', 'auction_edit_stores', data, 'super', nocheck)


class PlatformListOfDirectAuctionHousesRequest(InitializeParams):
    """平台管理|卖场管理|直拍卖场列表"""

    @doc(p_zhi_every_day_on_a_specified_date_phone)
    @BaseApi.timing_decorator
    def zhi_every_day_on_a_specified_date_phone(self, nocheck=False):
        sessions = self.generate_five_minute_sessions()
        data = {
            "name": self.mixed_random,
            "desc": '卖场描述' + self.mixed_random,
            "marketCategory": 2,
            "marketType": 1,
            "sessionFrequency": 0,
            "sessionNum": len(sessions),
            "marketActivityList": sessions,
            "auctionMarketRuleConfig": {
                "countdownType": 2,
                "merchantLimitList": [
                    3
                ],
                "conditionType": 1,
                "lockType": 1,
                "winRuleType": 2,
                "depositType": 1,
                "rangeLimit": 14,
                "failedSessionRule": 1,
                "failedNum": 15,
                "depositPrice": 0,
                "failedArticlesRule": 1,
                "timer": 4
            },
            "auctionMarketArticlesRuleConfig": {
                "autoAssignType": 1,
                "minMum": 1,
                "maxMum": 100000,
                "countdownType": 2,
                "auctionAutoAssignTypeList": [
                    {
                        "categoryId": 1,
                        "brandId": 1,
                        "modelIdList": [
                            9232
                        ],
                        "finenessIdList": [
                            129
                        ],
                        "minValue": 1,
                        "maxValue": 100000
                    }
                ]
            },
            "sort": 1,
            "marketTimeType": 2,
            "isEnable": True,
            "activityStartTime": self.get_formatted_datetime(),
            "activityEndTime": self.get_formatted_datetime(days=+20),
        }
        return self._make_request('post', 'auction_add_stores', data, 'super', nocheck)

    @doc(p_zhi_price_priority_for_close_proximity)
    def zhi_price_priority_for_close_proximity(self, nocheck=False):
        sessions = self.generate_five_minute_sessions()
        data = {
            "name": self.mixed_random,
            "desc": '卖场描述' + self.mixed_random,
            "sort": 1,
            "marketCategory": 2,
            "marketType": 1,
            "sessionFrequency": 0,
            "sessionNum": len(sessions),
            "marketActivityList": sessions,
            "auctionMarketRuleConfig": {
                "countdownType": 2,
                "merchantLimitList": [
                    4
                ],
                "conditionType": 1,
                "lockType": 1,
                "winRuleType": 2,
                "depositType": 1,
                "rangeLimit": 14,
                "failedSessionRule": 1,
                "failedNum": 15,
                "depositPrice": 0,
                "failedArticlesRule": 1,
                "timer": 3
            },
            "auctionMarketArticlesRuleConfig": {
                "minMum": 1,
                "maxMum": 1000,
                "autoAssignType": 1,
                "countdownType": 2,
                "auctionAutoAssignTypeList": [
                    {
                        "categoryId": "",
                        "brandId": "",
                        "modelIdList": [],
                        "finenessIdList": []
                    }
                ]
            },
            "marketTimeType": 2,
            "isEnable": False,
            "activityStartTime": self.get_formatted_datetime(),
            "activityEndTime": self.get_formatted_datetime(days=+20),
        }
        return self._make_request('post', 'auction_add_stores', data, 'super', nocheck)

    @doc(p_zhi_listed_status_removed_from_the_store)
    @BaseApi.timing_decorator
    def zhi_listed_status_removed_from_the_store(self, nocheck=False):
        res = self.pc.platform_list_of_direct_auction_houses_data(i=1)
        data = {
            "id": res[0]['id']
        }
        return self._make_request('post', 'auction_down_stores', data, 'super', nocheck)

    @doc(p_zhi_modify_the_store_event_time)
    @BaseApi.timing_decorator
    def zhi_modify_the_store_event_time(self, nocheck=False):
        res = self.pc.platform_list_of_direct_auction_houses_data(i=3)
        data = {
            "name": self.mixed_random,
            "desc": '卖场描述' + self.mixed_random,
            "sort": 1,
            "marketCategory": 2,
            "marketType": 1,
            "sessionFrequency": 0,
            "sessionNum": 1,
            "marketActivityList": self.generate_five_minute_sessions(),
            "auctionMarketRuleConfig": {
                "countdownType": 2,
                "merchantLimitList": [
                    3
                ],
                "conditionType": 1,
                "lockType": 1,
                "winRuleType": 2,
                "failedArticlesRule": 1,
                "depositType": 1,
                "rangeLimit": 14,
                "failedSessionRule": 1,
                "failedNum": 15,
                "depositPrice": 0,
                "timer": 4
            },
            "auctionMarketArticlesRuleConfig": {
                "minMum": 1,
                "maxMum": 1000,
                "autoAssignType": 1,
                "countdownType": 2,
                "auctionAutoAssignTypeList": [
                    {
                        "categoryId": 1,
                        "brandId": 1,
                        "modelIdList": [
                            7692
                        ],
                        "finenessIdList": [
                            129
                        ],
                        "minValue": 1,
                        "maxValue": 100000
                    }
                ]
            },
            "id": res[0]['id'],
            "marketTimeType": 2,
            "isEnable": True,
            "activityStartTime": self.get_formatted_datetime(),
            "activityEndTime": self.get_formatted_datetime(days=+20),
        }
        return self._make_request('post', 'auction_edit_stores', data, 'super', nocheck)

    @doc(p_zhi_add_goods_mobile_phones)
    @BaseApi.timing_decorator
    def zhi_add_goods_mobile_phones(self, nocheck=False):
        res = self.pc.platform_list_of_direct_auction_houses_data(i=1)
        res_2 = self.pc.platform_list_of_direct_auction_houses_data(data='b')
        res_3 = self.pc.platform_list_of_direct_auction_houses_data(data='c')
        data = {
            "sessionId": res_2[0]['id'],
            "marketId": res[0]['id'],
            "articlesNoList": [
                res_3[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'auction_session_details_add_products', data, 'super', nocheck)


class PlatformMerchantManageRequest(InitializeParams):
    """平台管理|商户管理"""


class PlatformProductReviewRequest(InitializeParams):
    """平台管理|同售管理|商品审核"""


class PlatformPurseCenterRequest(InitializeParams):
    """平台管理|订单管理|订单审核"""

    @doc(p_platform_approval)
    @BaseApi.timing_decorator
    def platform_approval(self, nocheck=False):
        res = self.pc.platform_order_review_data()
        data = {
            "auditStatus": 2,
            "auditRemark": "通过",
            "receipt": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com//erp-imgfiles/%2Fepbox-erp/20250820/WIehcT%2B7sg/I4FjLToJM%2Bw%3D%3D.jpg",
            "businessNo": res[0]['orderNo'],
            "id": res[0]['id']
        }
        return self._make_request('put', 'recharge_audit', data, 'platform', nocheck)

    @doc(p_platform_audit_rejection)
    @BaseApi.timing_decorator
    def platform_audit_rejection(self, nocheck=False):
        res = self.pc.platform_order_review_data()
        data = {
            "auditStatus": 3,
            "auditRemark": "拒绝",
            "receipt": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com//erp-imgfiles/%2Fepbox-erp/20250820/WIehcT%2B7sg/I4FjLToJM%2Bw%3D%3D.jpg",
            "businessNo": res[0]['orderNo'],
            "id": res[0]['id']
        }
        return self._make_request('put', 'recharge_audit', data, 'platform', nocheck)


class PlatformMessageReleaseListRequest(InitializeParams):
    """平台管理|消息管理|消息发布列表"""

    @doc(p_platform_approved)
    @BaseApi.timing_decorator
    def platform_approved(self, nocheck=False):
        res = self.pc.platform_message_release_list_data()
        data = {
            "auditResult": "1",
            "ids": [
                res[0]['id']
            ],
            "selectType": "1",
            "operationType": 8
        }
        return self._make_request('post', 'platform_audit', data, 'platform', nocheck)

    @doc(p_platform_refuse)
    @BaseApi.timing_decorator
    def platform_refuse(self, nocheck=False):
        res = self.pc.platform_message_release_list_data()
        data = {
            "auditResult": "2",
            "reason": "test1",
            "platformReason": "test1",
            "ids": [
                res[0]['id']
            ],
            "selectType": "1",
            "operationType": 8
        }
        return self._make_request('post', 'platform_audit', data, 'platform', nocheck)

    @doc(p_platform_back)
    @BaseApi.timing_decorator
    def platform_back(self, nocheck=False):
        res = self.pc.platform_message_release_list_data()
        data = {
            "id": res[0]['id'],
            "selectType": "1",
            "operationType": 6
        }
        return self._make_request('post', 'platform_back', data, 'platform', nocheck)


class PlatformGrievanceManageRequest(InitializeParams):
    """平台管理|壹准拍机|售后管理|申诉管理"""

    @doc(p_straight_shot_through_make_up_the_difference)
    @BaseApi.timing_decorator
    def straight_shot_through_make_up_the_difference(self, nocheck=False):
        res = self.pc.platform_grievance_manage_data(i=0)
        data = {
            "id": res[0]['id'],
            "auctionAfterSalesOrderAuditResult": {
                "auditResult": 1,
                "handleMode": 1
            },
            "amount": 1
        }
        return self._make_request('post', 'appeal_review', data, 'platform', nocheck)

    @doc(p_direct_shooting_through_priority_supplementation)
    @BaseApi.timing_decorator
    def direct_shooting_through_priority_supplementation(self, nocheck=False):
        res = self.pc.platform_grievance_manage_data(i=0)
        obj = res[0]['afterOrderNo']
        ParamCache.cache_object({"afterOrderNo": obj}, 'practical.json')
        data = {
            "id": res[0]['id'],
            "auctionAfterSalesOrderAuditResult": {
                "auditResult": 1,
                "handleMode": 2
            },
            "amount": 2
        }
        return self._make_request('post', 'appeal_review', data, 'platform', nocheck)

    @doc(p_direct_approved_refund)
    @BaseApi.timing_decorator
    def direct_approved_refund(self, nocheck=False):
        res = self.pc.platform_grievance_manage_data(i=0)
        obj = res[0]['afterOrderNo']
        ParamCache.cache_object({"afterOrderNo": obj}, 'practical.json')
        data = {
            "id": res[0]['id'],
            "auctionAfterSalesOrderAuditResult": {
                "auditResult": 1,
                "handleMode": 3
            }
        }
        return self._make_request('post', 'appeal_review', data, 'super', nocheck)


if __name__ == '__main__':
    api = PlatformGrievanceManageRequest()
    result = api.direct_approved_refund()
    print(json.dumps(result, indent=4, ensure_ascii=False))
