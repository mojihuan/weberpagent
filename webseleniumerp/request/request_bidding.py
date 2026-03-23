# coding: utf-8
from common.base_api import BaseApi
from common.base_params import InitializeParams
from common.file_cache_manager import ParamCache
from common.import_desc import *
from config.user_info import INFO


class BiddingCameraRequest(InitializeParams):
    """竞拍"""

    @doc(b_bidding_offer)
    @BaseApi.timing_decorator
    def bidding_offer(self, nocheck=False):
        self.wait_default()
        res = self.pc.platform_auction_product_manage_data(i=2)
        res_2 = self.pc.platform_list_of_dark_auction_houses_data(i=1)
        res_3 = self.pc.platform_list_of_dark_auction_houses_data(data='b')
        obj = res[0]['articlesNo']
        obj_2 = '8888'
        ParamCache.cache_object({"articlesNo": obj}, {"bidPrice": obj_2}, 'practical.json')
        data = {
            "sessionId": res_3[0]['id'],
            "marketId": res_2[0]['id'],
            "articlesNo": obj,
            "bidPrice": obj_2,
            "marketCategory": "1"
        }
        return self._make_request('post', 'bidding_manual_bidding', data, 'camera', nocheck)

    @doc(b_direct_auction_bidding)
    @BaseApi.timing_decorator
    def direct_auction_bidding(self, nocheck=False):
        self.wait_default()
        res = self.pc.platform_auction_product_manage_data(i=2)
        res_2 = self.pc.platform_list_of_direct_auction_houses_data()
        res_3 = self.pc.platform_list_of_direct_auction_houses_data(data='b')
        obj = res[0]['articlesNo']
        obj_2 = '9999'
        ParamCache.cache_object({"articlesNo": obj}, {"bidPrice": obj_2}, 'practical.json')
        data = {
            "sessionId": res_3[0]['id'],
            "marketId": res_2[0]['id'],
            "articlesNo": obj,
            "bidPrice": obj_2,
            "marketCategory": "2"
        }
        return self._make_request('post', 'bidding_manual_bidding', data, 'camera', nocheck)

    @doc(b_modify_the_price)
    @BaseApi.timing_decorator
    def modify_the_price(self, nocheck=False):
        res = self.pc.platform_auction_product_manage_data(i=2)
        res_2 = self.pc.platform_list_of_dark_auction_houses_data()
        res_3 = self.pc.platform_list_of_dark_auction_houses_data(data='b')
        res_4 = self.pc.bidding_camera_data(data='a')
        obj = res[0]['articlesNo']
        obj_2 = '5555'
        ParamCache.cache_object({"articlesNo": obj}, {"bidPrice": obj_2}, 'practical.json')
        data = {
            "sessionId": res_3[0]['id'],
            "marketId": res_2[0]['id'],
            "articlesNo": obj,
            "bidPrice": obj_2,
            "id": res_4[0]['bidPriceId']
        }
        return self._make_request('post', 'modify_the_price', data, 'camera', nocheck)

    @doc(b_direct_auction_price_change)
    @BaseApi.timing_decorator
    def direct_auction_price_change(self, nocheck=False):
        res = self.pc.platform_auction_product_manage_data(i=2)
        res_2 = self.pc.platform_list_of_dark_auction_houses_data()
        res_3 = self.pc.platform_list_of_dark_auction_houses_data(data='b')
        res_4 = self.pc.bidding_camera_data()
        obj = res[0]['articlesNo']
        obj_2 = '5555'
        ParamCache.cache_object({"articlesNo": obj}, {"bidPrice": obj_2}, 'practical.json')
        data = {
            "sessionId": res_3[0]['id'],
            "marketId": res_2[0]['id'],
            "articlesNo": obj,
            "bidPrice": obj_2,
            "id": res_4[0]['bidPriceId']
        }
        return self._make_request('post', 'modify_the_price', data, 'camera', nocheck)


class BiddingMyRequest(InitializeParams):

    @doc(b_straight_shot_change_to_self_pickup)
    @BaseApi.timing_decorator
    def straight_shot_change_to_self_pickup(self, nocheck=False):
        res = self.pc.bidding_my_data(i=2)
        obj = res[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj}, 'practical.json')
        data = {
            "orderNo": res[0]['saleOrderNo'],
            "articlesNo": obj
        }
        return self._make_request('post', 'pending_shipment_to_pick_up', data, 'camera', nocheck)

    @doc(b_direct_shot_change_to_mailing)
    @BaseApi.timing_decorator
    def direct_shot_change_to_mailing(self, nocheck=False):
        res = self.pc.fulfillment_sales_and_shipment_manage_data(data='b')
        obj = res[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj}, 'practical.json')
        data = {
            "orderNo": res[0]['saleOrderNo'],
            "articlesNo": obj
        }
        return self._make_request('post', 'pending_shipment_to_pick_up', data, 'camera', nocheck)

    @doc(b_direct_shot_confirm_receipt)
    @BaseApi.timing_decorator
    def direct_shot_confirm_receipt(self, nocheck=False):
        res = self.pc.bidding_my_data(i=3)
        obj = res[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj}, 'practical.json')
        data = {
            "orderNo": res[0]['saleOrderNo'],
            "articlesNo": obj
        }
        return self._make_request('post', 'bidding_confirm_receipt', data, 'camera', nocheck)

    @doc(b_direct_shooting_apply_for_after_sales)
    @BaseApi.timing_decorator
    def direct_shooting_apply_for_after_sales(self, nocheck=False):
        res = self.pc.bidding_my_data(i=4)
        data = {
            "articlesNo": res[0]['articlesNo'],
            "auctionAfterSalesOrderReason": {
                "afterReason": "4",
                "afterDesc": "售后",
                "imageUrl": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com//erp-imgfiles/%2Fepbox-erp/20260203/Cky5EnqksaGALjZuTUQMkA%3D%3D.png",
                "videoUrl": "",
                "qualityInspectionReportList": [

                ]
            }
        }
        return self._make_request('post', 'apply_for_after_sales', data, 'camera', nocheck)

    @doc(b_direct_auction_receives_the_difference)
    @BaseApi.timing_decorator
    def direct_auction_receives_the_difference(self, nocheck=False):
        res = self.pc.bidding_my_data(data='a', i=[6])
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'receive_the_difference', data, 'camera', nocheck)

    @doc(b_direct_shot_re_inspection_receive_the_spread)
    @BaseApi.timing_decorator
    def direct_shot_re_inspection_receive_the_spread(self, nocheck=False):
        res = self.pc.bidding_my_data(data='a', i=[6])
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'receive_the_difference', data, 'camera', nocheck)

    @doc(b_direct_shot_re_inspection_rejection_price)
    @BaseApi.timing_decorator
    def direct_shot_re_inspection_rejection_price(self, nocheck=False):
        res = self.pc.bidding_my_data(data='a', i=[6])
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'refuse_to_pay_the_price_difference', data, 'camera', nocheck)

    @doc(b_direct_platform_review_no_rejection_price)
    @BaseApi.timing_decorator
    def direct_platform_review_no_rejection_price(self, nocheck=False):
        res = self.pc.bidding_my_data(data='a', i=[6])
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'refuse_to_pay_the_price_difference', data, 'camera', nocheck)

    @doc(b_direct_shot_refuses_to_make_up_for_the_difference)
    @BaseApi.timing_decorator
    def direct_shot_refuses_to_make_up_for_the_difference(self, nocheck=False):
        res = self.pc.bidding_my_data(data='a', i=[6])
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'refuse_to_pay_the_price_difference', data, 'camera', nocheck)

    @doc(b_direct_shooting_ends_after_sales)
    @BaseApi.timing_decorator
    def direct_shooting_ends_after_sales(self, nocheck=False):
        res = self.pc.bidding_my_data(data='a', i=[6])
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'end_after_sales', data, 'camera', nocheck)

    @doc(b_direct_shooting_re_inspection_ends_after_sales)
    @BaseApi.timing_decorator
    def direct_shooting_re_inspection_ends_after_sales(self, nocheck=False):
        res = self.pc.bidding_my_data(data='a', i=[2])
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'end_after_sales', data, 'camera', nocheck)

    @doc(b_direct_platform_review_ends_after_sales)
    @BaseApi.timing_decorator
    def direct_platform_review_ends_after_sales(self, nocheck=False):
        res = self.pc.bidding_my_data(data='a', i=[6])
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'end_after_sales', data, 'camera', nocheck)

    @doc(b_direct_shot_go_shipping)
    @BaseApi.timing_decorator
    def direct_shot_go_shipping(self, nocheck=False):
        res = self.pc.bidding_my_data(data='a', i=[7])
        res_2 = self.pc.platform_inspection_center_manage_data()
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "sendType": 1,
            "expressCompanyId": "1",
            "expressCompanyName": "顺丰物流",
            "expectPostTimeStart": self.get_formatted_datetime(),
            "expressType": 1,
            "express": {
                "senderName": INFO['camera_name'],
                "senderPhone": INFO['camera_phone'],
                "senderProvinceId": INFO['province_id'],
                "senderProvinceName": INFO['province_name'],
                "senderCityId": INFO['city_id'],
                "senderCityName": INFO['city_name'],
                "senderCountyId": INFO['county_id'],
                "senderCountyName": INFO['county_name'],
                "senderAddress": INFO['detailed_address']
            },
            "id": obj,
            "centerId": res_2[0]['id']
        }
        return self._make_request('post', 'to_be_sent_back_for_shipment', data, 'camera', nocheck)

    @doc(b_direct_shooting_to_ship_logistics)
    @BaseApi.timing_decorator
    def direct_shooting_to_ship_logistics(self, nocheck=False):
        res = self.pc.bidding_my_data(data='a', i=[7])
        res_2 = self.pc.platform_inspection_center_manage_data()
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "expressNo": self.sf,
            "expressCompanyId": INFO['sf_express_logo'],
            "expressCompanyName": "顺丰快运",
            "id": obj,
            "centerId": res_2[0]['id'],
            "sendType": 2
        }
        return self._make_request('post', 'to_be_sent_back_for_shipment', data, 'camera', nocheck)

    @doc(b_direct_platform_review_self_proclaimed_logistics)
    @BaseApi.timing_decorator
    def direct_platform_review_self_proclaimed_logistics(self, nocheck=False):
        res = self.pc.bidding_my_data(data='a', i=[7])
        res_2 = self.pc.platform_inspection_center_manage_data()
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "expressNo": self.sf,
            "expressCompanyId": INFO['sf_express_logo'],
            "expressCompanyName": "顺丰快运",
            "id": obj,
            "centerId": res_2[0]['id'],
            "sendType": 2
        }
        return self._make_request('post', 'to_be_sent_back_for_shipment', data, 'camera', nocheck)

    @doc(b_direct_shot_to_ship_by_yourself)
    @BaseApi.timing_decorator
    def direct_shot_to_ship_by_yourself(self, nocheck=False):
        res = self.pc.bidding_my_data(data='a', i=[7])
        res_2 = self.pc.platform_inspection_center_manage_data()
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj,
            "centerId": res_2[0]['id'],
            "sendType": 3
        }
        return self._make_request('post', 'to_be_sent_back_for_shipment', data, 'camera', nocheck)

    @doc(b_direct_platform_review_mail_it_yourself)
    @BaseApi.timing_decorator
    def direct_platform_review_mail_it_yourself(self, nocheck=False):
        res = self.pc.bidding_my_data(data='a', i=[7])
        res_2 = self.pc.platform_inspection_center_manage_data()
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj,
            "centerId": res_2[0]['id'],
            "sendType": 3
        }
        return self._make_request('post', 'to_be_sent_back_for_shipment', data, 'camera', nocheck)

    @doc(b_straight_shot_i_want_to_appeal)
    @BaseApi.timing_decorator
    def straight_shot_i_want_to_appeal(self, nocheck=False):
        res = self.pc.bidding_my_data(data='a', i=[2])
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj,
            "auctionAfterSalesOrderAppeal": {
                "afterDesc": "申诉",
                "imageUrl": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com//erp-imgfiles/%2Fepbox-erp/20260206/Cky5EnqksaGALjZuTUQMkA%3D%3D.png",
                "videoUrl": "",
                "appealType": "0"
            }
        }
        return self._make_request('post', 'pending_appeal_i_want_to_appeal', data, 'camera', nocheck)

    @doc(b_pending_appeal_and_end_after_sales)
    @BaseApi.timing_decorator
    def pending_appeal_and_end_after_sales(self, nocheck=False):
        res = self.pc.bidding_my_data(data='a', i=[2])
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj,
            "auctionAfterSalesOrderAppeal": {
                "afterDesc": "申诉",
                "imageUrl": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com//erp-imgfiles/%2Fepbox-erp/20260206/Cky5EnqksaGALjZuTUQMkA%3D%3D.png",
                "videoUrl": "",
                "appealType": "0"
            }
        }
        return self._make_request('post', 'pending_appeal_i_want_to_appeal', data, 'camera', nocheck)

    @doc(b_direct_platform_review_receive_the_spread)
    @BaseApi.timing_decorator
    def direct_platform_review_receive_the_spread(self, nocheck=False):
        res = self.pc.bidding_my_data(data='a', i=[6])
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'receive_the_difference', data, 'camera', nocheck)

    @doc(b_direct_platform_review_go_shipping)
    @BaseApi.timing_decorator
    def direct_platform_review_go_shipping(self, nocheck=False):
        res = self.pc.bidding_my_data(data='a', i=[7])
        res_2 = self.pc.platform_inspection_center_manage_data()
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "sendType": 1,
            "expressCompanyId": "1",
            "expressCompanyName": "顺丰物流",
            "expectPostTimeStart": self.get_formatted_datetime(),
            "expressType": 1,
            "express": {
                "senderName": INFO['camera_name'],
                "senderPhone": INFO['camera_phone'],
                "senderProvinceId": INFO['province_id'],
                "senderProvinceName": INFO['province_name'],
                "senderCityId": INFO['city_id'],
                "senderCityName": INFO['city_name'],
                "senderCountyId": INFO['county_id'],
                "senderCountyName": INFO['county_name'],
                "senderAddress": INFO['detailed_address']
            },
            "id": obj,
            "centerId": res_2[0]['id']
        }
        return self._make_request('post', 'to_be_sent_back_for_shipment', data, 'camera', nocheck)


if __name__ == '__main__':
    api = BiddingMyRequest()
    result = api.direct_shot_to_ship_by_yourself()
    print(result)
