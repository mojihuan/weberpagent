# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.decorators import cached
from common.import_case import *


class TestPlatformAuctionProductManage(BaseCase, unittest.TestCase):
    """平台管理|虚拟库存|上拍商品管理"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return platform_r.PlatformAuctionProductManageRequest()
        else:
            return None

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0select_the_session_to_add_product_confirm(self):
        """[可上拍物品tab]选择场次-暗拍卖场-添加商品上架"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DD2'])
        case = self.common_operations(login='super')
        case.select_the_session_to_add_product_confirm()
        res = [lambda: self.pc.platform_auction_product_manage_assert(headers='super', i=2, updateTime='now', statusStr='销售中', auctionMarketSession='暗拍')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_direct_auction_add_items_to_the_shelves(self):
        """[可上拍物品tab]-选择场次-直拍卖场-添加商品上架"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1'])
        case = self.common_operations()
        case.direct_auction_add_items_to_the_shelves()
        res = [lambda: self.pc.platform_auction_product_manage_assert(headers='super', i=2, updateTime='now', statusStr='销售中', auctionMarketSession='直拍')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_guaranteed_sale_cancellation_of_sale(self):
        """[可上拍物品tab]-取消销售"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4'])
        case = self.common_operations()
        case.guaranteed_sale_cancellation_of_sale()
        obj = cached('id')
        res = [lambda: self.pc.auction_my_assert(j=1, i=2, id=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_secret_shooting_modification_sessions(self):
        """[可上拍物品tab]-修改场次-暗拍修改场次"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DD2', 'DF1'])
        case = self.common_operations()
        case.secret_shooting_modification_sessions()
        res = [lambda: self.pc.platform_auction_product_manage_assert(headers='super', i=2, updateTime='now', statusStr='销售中', auctionMarketSession='暗拍')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_cancel_the_auction(self):
        """[可上拍物品tab]-取消上拍"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DD2', 'DF1'])
        case = self.common_operations()
        case.cancel_the_auction()
        res = [lambda: self.pc.platform_auction_product_manage_assert(headers='super', i=1, updateTime='now')]
        self.assert_all(*res)


class TestPlatformItemsToBeSpecified(BaseCase, unittest.TestCase):
    """平台管理|运营中心|待指定物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return platform_r.PlatformItemsToBeSpecifiedRequest()
        else:
            return platform_p.PlatformItemsToBeSpecifiedPages(self.driver)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0designated_recyclers(self):
        """[指定回收商]"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB4'])
        case = self.common_operations(login='platform')
        case.designated_recyclers()
        res = [lambda: self.pc.platform_items_to_be_specified_assert(headers='platform', assignTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_modify_the_recycler(self):
        """[修改回收商]"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB4'])
        case = self.common_operations()
        case.modify_the_recycler()
        res = [lambda: self.pc.platform_items_to_be_specified_assert(headers='platform', assignTime='now')]
        self.assert_all(*res)


class TestPlatformListOfDarkAuctionHouses(BaseCase, unittest.TestCase):
    """平台管理|卖场管理|暗拍卖场列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return platform_r.PlatformListOfDarkAuctionHousesRequest()
        else:
            return platform_p.PlatformListOfDarkAuctionHousesPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0every_day_on_a_expired_phone(self):
        """[创建卖场]指定日期-场次频率每天-无保证金-手机-保存并上架"""
        case = self.common_operations(login='super')
        case.every_day_on_a_expired_phone()
        res = [lambda: self.pc.platform_list_of_dark_auction_houses_assert(headers='super', createTime='now', statusStr='已上架')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_price_priority_for_close_proximity(self):
        """[创建卖场]暗拍-仅保存"""
        case = self.common_operations()
        case.price_priority_for_close_proximity()
        res = [lambda: self.pc.platform_list_of_dark_auction_houses_assert(i=2, headers='super', createTime='now', statusStr='待上架')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_create_five_minute_auction_session(self):
        """[创建卖场]指定5分钟一场-保存并上架"""
        case = self.common_operations()
        case.create_five_minute_auction_session()
        res = [lambda: self.pc.platform_list_of_dark_auction_houses_assert(headers='super', createTime='now', statusStr='已上架')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_modify_the_store_event_time(self):
        """[已下架tab]暗拍卖场-编辑-保存并上架"""
        self.pre.operations(data=['DD2', 'DD3'])
        case = self.common_operations()
        case.modify_the_store_event_time()
        res = [lambda: self.pc.platform_list_of_dark_auction_houses_assert(headers='super', updateTime='now', statusStr='已上架')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_save_and_list_is_modified_to_save_only(self):
        """[已下架tab]暗拍卖场-重新上架"""
        self.pre.operations(data=['DD2', 'DD3'])
        case = self.common_operations()
        case.save_and_list_is_modified_to_save_only()
        res = [lambda: self.pc.platform_list_of_dark_auction_houses_assert(headers='super', updateTime='now', statusStr='已上架')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_listed_status_removed_from_the_store(self):
        """[下架]已上架状态-下架卖场"""
        self.pre.operations(data=['DD1'])
        case = self.common_operations()
        case.listed_status_removed_from_the_store()
        res = [lambda: self.pc.platform_list_of_dark_auction_houses_assert(headers='super', createTime='now', statusStr='已下架')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_add_goods_mobile_phones(self):
        """[查看场次详情]-已上架状态-添加商品-手机"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DD2'])
        case = self.common_operations()
        case.add_goods_mobile_phones()
        res = [lambda: self.pc.platform_list_of_dark_auction_houses_assert(headers='super', data='a', totalMum=1)]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_turn_off_the_open_view_of_the_product(self):
        """[查看场次详情]关闭开放查看商品"""
        self.pre_platform.every_day_on_a_specified_date_phone()
        case = self.common_operations()
        case.turn_off_the_open_view_of_the_product()

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_pending_status_listed(self):
        """[待上架tab]-上架"""
        self.pre.operations(data=['DD5'])
        case = self.common_operations()
        case.pending_status_listed()
        res = [lambda: self.pc.platform_list_of_dark_auction_houses_assert(headers='super', statusStr='已上架', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_pending_status_edit_save_and_list(self):
        """[待上架tab]-编辑-保存并上架"""
        self.pre.operations(data=['DD5'])
        case = self.common_operations()
        case.pending_status_edit_save_and_list()
        res = [lambda: self.pc.platform_list_of_dark_auction_houses_assert(headers='super', statusStr='已上架', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_pending_status_deleted(self):
        """[待上架tab]-删除"""
        self.pre.operations(data=['DD5'])
        case = self.common_operations()
        case.pending_status_deleted()

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_delisted_edit_save_and_list(self):
        """[已下架tab]-编辑-保存并上架"""
        self.pre.operations(data=['DD2', 'DD3'])
        case = self.common_operations()
        case.delisted_edit_save_and_list()
        res = [lambda: self.pc.platform_list_of_dark_auction_houses_assert(headers='super', statusStr='已上架', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_multi_select_show_listed_to_be_listed(self):
        """[调整广告位]多选-显示已上架和待上架-保存并更新"""
        case = self.common_operations()
        case.multi_select_show_listed_to_be_listed()

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_multi_select_show_listed_pending_removed(self):
        """[调整广告位]多选-显示已上架和待上架和已下架-保存并更新"""
        case = self.common_operations()
        case.multi_select_show_listed_pending_removed()

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_view_logs(self):
        """[查看日志]"""
        case = self.common_operations()
        case.view_logs()

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_derived(self):
        """[导出]"""
        case = self.common_operations()
        case.derived()


class TestPlatformListOfDirectAuctionHouses(BaseCase, unittest.TestCase):
    """平台管理|卖场管理|直拍卖场列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return platform_r.PlatformListOfDirectAuctionHousesRequest()
        else:
            return platform_p.PlatformListOfDirectAuctionHousePages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0zhi_every_day_on_a_specified_date_phone(self):
        """[创建卖场]指定日期-场次频率每天-手机-保存并上架"""
        case = self.common_operations(login='super')
        case.zhi_every_day_on_a_specified_date_phone()
        res = [lambda: self.pc.platform_list_of_direct_auction_houses_assert(headers='super', createTime='now', statusStr='已上架')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_zhi_price_priority_for_close_proximity(self):
        """[创建卖场]仅保存"""
        case = self.common_operations()
        case.zhi_price_priority_for_close_proximity()
        res = [lambda: self.pc.platform_list_of_direct_auction_houses_assert(headers='super', createTime='now', statusStr='待上架')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_zhi_modify_the_store_event_time(self):
        """[已下架tab]-编辑-保存并上架"""
        self.pre.operations(data=['DB1', 'DB4'])
        case = self.common_operations()
        case.zhi_modify_the_store_event_time()
        res = [lambda: self.pc.platform_list_of_direct_auction_houses_assert(headers='super', updateTime='now', statusStr='已上架')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_zhi_listed_status_removed_from_the_store(self):
        """[已上架tab]-下架"""
        self.pre.operations(data=['DB1'])
        case = self.common_operations()
        case.zhi_listed_status_removed_from_the_store()
        res = [lambda: self.pc.platform_list_of_direct_auction_houses_assert(headers='super', updateTime='now', statusStr='已下架')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_zhi_add_goods_mobile_phones(self):
        """[查看场次详情]已上架状态-添加商品-手机"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1'])
        case = self.common_operations()
        case.zhi_add_goods_mobile_phones()
        res = [lambda: self.pc.platform_list_of_direct_auction_houses_assert(headers='super', data='a', totalMum=1),
               lambda: self.pc.platform_list_of_direct_auction_houses_assert(headers='super', data='b', updateTime='now', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_zhi_turn_off_the_open_view_of_the_product(self):
        """[查看场次详情]关闭开放查看商品"""
        self.pre.operations(data=['DB1'])
        case = self.common_operations()
        case.zhi_turn_off_the_open_view_of_the_product()

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_zhi_multi_select_show_listed_to_be_listed(self):
        """[调整广告位]多选-显示已上架和待上架-保存并更新"""
        case = self.common_operations()
        case.zhi_multi_select_show_listed_to_be_listed()

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_zhi_multi_select_show_listed_pending_removed(self):
        """[调整广告位]多选-显示已上架和待上架和已下架-保存并更新"""
        case = self.common_operations()
        case.zhi_multi_select_show_listed_pending_removed()

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_zhi_view_logs(self):
        """[查看日志]"""
        case = self.common_operations()
        case.zhi_view_logs()

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_zhi_derived(self):
        """[导出]"""
        case = self.common_operations()
        case.zhi_derived()


class TestPlatformMessageReleaseList(BaseCase, unittest.TestCase):
    """平台管理|消息管理|消息发布列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return platform_r.PlatformMessageReleaseListRequest()
        else:
            return platform_p.PlatformMessageReleaseListPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0platform_refuse(self):
        """[审核]-平台审核拒绝"""
        self.pre.operations(data=['JA2'])
        case = self.common_operations(login='platform')
        case.platform_refuse()
        res = [lambda: self.pc.message_release_list_assert(publishStateDesc='待发布', internalAuditStateDesc='审核通过', platformAuditStateDesc='审核不通过', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_platform_approved(self):
        """[审核]-平台审核通过"""
        self.pre.operations(data=['JA2'])
        case = self.common_operations()
        case.platform_approved()
        res = [lambda: self.pc.message_release_list_assert(publishStateDesc='已发布', internalAuditStateDesc='审核通过', platformAuditStateDesc='审核通过', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_platform_back(self):
        """[审核]-平台撤回"""
        self.pre.operations(data=['JA2', 'DE1'])
        case = self.common_operations()
        case.platform_back()
        res = [lambda: self.pc.message_release_list_assert(publishStateDesc='已撤回', internalAuditStateDesc='审核通过', platformAuditStateDesc='审核通过', createTime='now')]
        self.assert_all(*res)


class TestPlatformProductReview(BaseCase, unittest.TestCase):
    """平台管理|同售管理|商品审核"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return platform_r.PlatformProductReviewRequest()
        else:
            return platform_p.PlatformProductReviewPages(self.driver)


class TestPlatformPurseCenter(BaseCase, unittest.TestCase):
    """平台管理|订单管理|订单审核"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return platform_r.PlatformPurseCenterRequest()
        else:
            return platform_p.PlatformPurseCenterPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0platform_approval(self):
        """[审核]-快递易-对公充值-平台审核通过"""
        self.pre.operations(data=['KA1'])
        case = self.common_operations(login='platform')
        case.platform_approval()
        res = [lambda: self.pc.platform_order_review_assert(headers='platform', orderBusinessTypeStr='钱包充值', auditStatusStr='已通过', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_platform_audit_rejection(self):
        """[审核]-快递易-对公充值-平台审核拒绝"""
        self.pre.operations(data=['KA1'])
        case = self.common_operations()
        case.platform_audit_rejection()
        res = [lambda: self.pc.platform_order_review_assert(headers='platform', orderBusinessTypeStr='钱包充值', auditStatusStr='未通过', createTime='now')]
        self.assert_all(*res)


class TestGrievanceManage(BaseCase, unittest.TestCase):
    """平台管理|壹准拍机|售后管理|申诉管理"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return platform_r.PlatformGrievanceManageRequest()
        else:
            return None

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_straight_shot_through_make_up_the_difference(self):
        """[待处理]-直拍-审核通过-仅补差"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF5', '@BB5'])
        case = self.common_operations()
        case.straight_shot_through_make_up_the_difference()
        res = [lambda: self.pc.platform_grievance_manage_assert(i=1, headers='platform', statusStr='申诉成功', auditTime='now'),
               lambda: self.pc.platform_yz_auction_assert(i=[5], headers='platform', afterStatusStr='补差成功', firstAppealAuditTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_direct_shooting_through_priority_supplementation(self):
        """[待处理]-直拍-审核通过-优先补差"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF5', '@BB5'])
        case = self.common_operations()
        case.direct_shooting_through_priority_supplementation()
        obj = cached('afterOrderNo')
        res = [lambda: self.pc.platform_grievance_manage_assert(i=1, headers='platform', statusStr='申诉成功', auditTime='now'),
               lambda: self.pc.bidding_my_assert(data='c', i=[6], headers='camera', orderNo=obj, afterStatus=6)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_direct_approved_refund(self):
        """[待处理]-直拍-审核通过-退货退款"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF5', '@BB5'])
        case = self.common_operations()
        case.direct_approved_refund()
        obj = cached('afterOrderNo')
        res = [lambda: self.pc.platform_grievance_manage_assert(i=1, headers='platform', statusStr='申诉成功', auditTime='now'),
               lambda: self.pc.bidding_my_assert(data='c', i=[7], headers='camera', orderNo=obj, afterStatus=7)]
        self.assert_all(*res)


if __name__ == '__main__':
    unittest.main()
