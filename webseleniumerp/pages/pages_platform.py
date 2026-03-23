# coding: utf-8
from common.base_page import BasePage, reset_after_execution
from common.import_desc import *


class CommonPages(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self._steps_queue = []

    def menu(self, menu_type, key):
        """获取元素"""
        menu_mapping = {
            'main': self.elem_positioning['positioning'],
        }
        if menu_type in menu_mapping:
            return self.exc(lambda: menu_mapping[menu_type][key])
        else:
            raise ValueError(f"menu not found: {menu_type}")


class PlatformItemsToBeSpecifiedPages(CommonPages):
    """平台管理|运营中心|待指定物品"""


class PlatformListOfDarkAuctionHousesPages(CommonPages):
    """平台管理|卖场管理|暗拍卖场列表"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='platform_manage_menu', desc='平台管理')
         .scroll(key='platform_store_manage_menu', desc='卖场管理')
         .step(key='platform_store_manage_menu', desc='卖场管理')
         .step(key='platform_dark_auction_house_listings_menu', desc='暗拍卖场列表')
         .wait())
        return self

    @reset_after_execution
    @doc(p_every_day_on_a_expired_phone)
    def every_day_on_a_expired_phone(self, ):
        self.menu_manage()
        (self.step(key='create_a_store', desc='创建卖场')
         .step(key='store_name', value='直拍卖场' + self.serial, action='input', desc='卖场名称')
         .step(key='store_description', value='卖场描述' + self.serial, action='input', desc='卖场描述')
         .step(key='ad_space_priority', value='1', action='input', desc='广告位优先级')
         .step(key='add_event_start_time', value=self.get_the_date(days=-2), action='input', desc='活动开始时间')
         .step(key='add_event_end_time', value=self.get_the_date(days=-1), action='input', desc='活动结束时间')
         .custom(lambda: self.wait_time())
         .step(key='input_imei', value='场次标题' + self.serial, action='input', desc='场次1标题')
         .step(key='start_time', value=f"00:10:00", action='input', desc='场次开始时间')
         .step(key='add_end_time', value=f"22:00:00", action='input', desc='场次结束时间')
         .step(key='determine_the_time', desc='确定时间')
         .step(key='show_time', value=f"20:00", action='input', desc='展示排名时间')
         .step(key='choice_of_goods_winning_rules', desc='商品中标规则')
         .custom(lambda: self.down_arrow_return(2))
         .step(key='choice_session_rules', desc='请选择场次流拍规则')
         .custom(lambda: self.down_arrow_return(2))
         .step(key='the_number_of_guaranteed_sessions', value='1', action='input', desc='场次保底数量')
         .step(key='the_number_of_sessions_capped', value='1000', action='input', desc='场次封顶数量')
         .step(key='cond', desc='所有条件(and)')
         .step(key='category', desc='品类')
         .custom(lambda: self.down_arrow_return())
         .step(key='brand', desc='品牌')
         .custom(lambda: self.down_arrow_return())
         .step(key='model', desc='型号')
         .custom(lambda: self.down_arrow_return())
         .step(key='fine_quality_requirements', desc='成色要求')
         .step(key='beautiful_machine', desc='选择靓机')
         .step(key='fine_quality', desc='关闭选项')
         .step(key='minimum_bidding_price', value='100', action='input', desc='最小起拍价')
         .step(key='fine_quality', desc='点击一下其他位置【成色要求】')
         .step(key='maximum_starting_price', value='100000', action='input', desc='最大起拍价')
         .step(key='save_and_put_it_on_the_shelf', desc='保存并上架')
         .step(key='the_secret_auction_is_confirmed', desc='确定')
         .step(key='i_know', desc='我知道了')
         .wait())

    @reset_after_execution
    @doc(p_modify_the_store_event_time)
    def modify_the_store_event_time(self):
        self.menu_manage()
        (self.step(key='down_shelves', desc='已下架')
         .custom(lambda: self.wait_time())
         .step(key='edit_one', desc='编辑')
         .step(key='clear_date', desc='清空原来的日期')
         .step(key='event_start_time_edit', value=self.get_the_date(), action='input', desc='活动开始时间')
         .step(key='event_end_time_edit', value=self.get_the_date(days=7), action='input', desc='活动结束时间')
         .custom(lambda: self.wait_time())
         .scroll('save_only', desc='仅保存')
         .step(key='save_and_put_it_on_the_shelf', desc='保存并上架')
         .step(key='the_secret_auction_is_confirmed', desc='确定')
         .step(key='i_know', desc='我知道了')
         .wait())
        return

    @reset_after_execution
    @doc(p_listed_status_removed_from_the_store)
    def listed_status_removed_from_the_store(self):
        self.menu_manage()
        (self.step(key='already_shelves', desc='已上架')
         .step(key='down_one', desc='下架')
         .step(key='down_determine', desc='确定')
         .wait())
        return

    @reset_after_execution
    @doc(p_add_goods_mobile_phones)
    def add_goods_mobile_phones(self):
        self.menu_manage()
        (self.step(key='already_shelves', desc='已上架')
         .step(key='view_sessions', desc='查看场次')
         .step(key='add_products', desc='添加商品')
         .step(key='select_a_category', desc='选择品类-手机')
         .custom(lambda: self.down_arrow_return())
         .step(key='search_button', desc='搜索')
         .custom(lambda: self.down_arrow_return(3))
         .step(key='add_product_ok', desc='确定')
         .wait())
        return

    @reset_after_execution
    @doc(p_turn_off_the_open_view_of_the_product)
    def turn_off_the_open_view_of_the_product(self):
        self.menu_manage()
        (self.step(key='already_shelves', desc='已上架')
         .step(key='view_sessions', desc='查看场次')
         .step(key='open_to_view_products', desc='关闭查看商品')
         .wait())
        return

    @reset_after_execution
    @doc(p_pending_status_listed)
    def pending_status_listed(self):
        self.menu_manage()
        (self.step(key='wait_shelves', desc='待上架')
         .step(key='up_one', desc='上架')
         .step(key='the_secret_auction_is_confirmed', desc='确定')
         .step(key='wait_shelves_i_know', desc='我知道了')
         .wait())
        return

    @reset_after_execution
    @doc(p_pending_status_deleted)
    def pending_status_deleted(self):
        self.menu_manage()
        (self.step(key='wait_shelves', desc='待上架')
         .step(key='delete_one', desc='删除')
         .scroll('tip_determine', desc='确定')
         .wait())
        return

    @reset_after_execution
    @doc(p_multi_select_show_listed_to_be_listed)
    def multi_select_show_listed_to_be_listed(self):
        self.menu_manage()
        (self.step(key='adjust_ad_placements', desc='调整广告位')
         .step(key='show_wait_shelves', desc='显示待上架')
         .step(key='save_and_update', desc='保存并更新')
         .wait())
        return

    @reset_after_execution
    @doc(p_multi_select_show_listed_pending_removed)
    def multi_select_show_listed_pending_removed(self):
        self.menu_manage()
        (self.step(key='adjust_ad_placements', desc='调整广告位')
         .step(key='show_wait_shelves', desc='显示待上架')
         .step(key='show_removed', desc='显示已下架')
         .step(key='save_and_update', desc='保存并更新')
         .wait())
        return

    @reset_after_execution
    @doc(p_view_logs)
    def view_logs(self):
        self.menu_manage()
        (self.step(key='view_logs', desc='查看日志')
         .wait())
        return

    @reset_after_execution
    @doc(p_derived)
    def derived(self):
        self.menu_manage()
        (self.step(key='export', desc='导出')
         .wait())


class PlatformListOfDirectAuctionHousePages(CommonPages):
    """平台管理|卖场管理|直拍卖场列表"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='platform_manage_menu', desc='平台管理')
         .scroll(key='platform_store_manage_menu', desc='卖场管理')
         .step(key='platform_store_manage_menu', desc='卖场管理')
         .step(key='platform_direct_auction_house_listings_menu', desc='直拍卖场列表')
         .wait())
        return self

    @reset_after_execution
    @doc(p_zhi_every_day_on_a_specified_date_phone)
    def zhi_every_day_on_a_specified_date_phone(self):
        """创建直拍卖场"""
        self.menu_manage()
        (self.step(key='create_a_store', desc='创建卖场')
         .step(key='store_name', value='直拍卖场' + self.serial, action='input', desc='卖场名称')
         .step(key='store_description', value='卖场描述' + self.serial, action='input', desc='卖场描述')
         .step(key='ad_space_priority', value='1', action='input', desc='广告位优先级')
         .step(key='event_start_time', value=self.get_formatted_datetime(), action='input', desc='活动开始时间')
         .step(key='event_end_time', value=self.get_formatted_datetime(days=1), action='input', desc='活动开结束时间')
         .step(key='input_imei', value='场次标题' + self.serial, action='input', desc='场次1标题')
         .step(key='input_imei', desc='场次1标题')
         .step(key='start_time_of_the_session', value="09:00", action='input', desc='场次开始时间')
         .step(key='end_time', value="09:55", action='input', desc='场次结束时间')
         .step(key='countdown_to_the_commodity', value='1', action='input', desc='商品倒计时分钟')
         .step(key='the_number_of_guaranteed_sessions', value='1', action='input', desc='场次保底数量')
         .step(key='the_number_of_sessions_capped', value='10000', action='input', desc='场次封顶数量')
         .step(key='category', desc='品类')
         .custom(lambda: self.down_arrow_return())
         .step(key='brand', desc='品牌')
         .custom(lambda: self.down_arrow_return())
         .step(key='model', desc='型号')
         .custom(lambda: self.down_arrow_return())
         .step(key='fine_quality_requirements', desc='成色要求')
         .custom(lambda: self.down_arrow_return())
         .step(key='minimum_bidding_price', value='1', action='input', desc='最小起拍价')
         .step(key='conditional_group_configuration', desc='条件组配置')
         .step(key='maximum_starting_price', value='100000', action='input', desc='最大起拍价')
         .step(key='save_and_put_it_on_the_shelf', desc='保存并上架')
         .step(key='ok', desc='确定')
         .step(key='i_know', desc='我知道了')
         .wait())
        return

    @reset_after_execution
    @doc(p_zhi_listed_status_removed_from_the_store)
    def zhi_listed_status_removed_from_the_store(self):
        self.menu_manage()
        (self.step(key='removed_from_the_shelves', desc='下架')
         .step(key='ok', desc='确定')
         .wait())
        return

    @reset_after_execution
    @doc(p_zhi_add_goods_mobile_phones)
    def zhi_add_goods_mobile_phones(self):
        self.menu_manage()
        (self.step(key='already_shelves', desc='已上架')
         .step(key='view_sessions', desc='查看场次')
         .step(key='add_products', desc='添加商品')
         .step(key='select_a_category', desc='选择品类')
         .custom(lambda: self.down_arrow_return())
         .step(key='search_button', desc='搜索')
         .custom(lambda: self.down_arrow_return(3))
         .step(key='add_product_ok', desc='确定')
         .wait())
        return

    @reset_after_execution
    @doc(p_zhi_turn_off_the_open_view_of_the_product)
    def zhi_turn_off_the_open_view_of_the_product(self):
        self.menu_manage()
        (self.step(key='already_shelves', desc='已上架')
         .step(key='view_sessions', desc='查看场次')
         .step(key='express_is_easy', desc='关闭开发查看商品')
         .wait())
        return

    @reset_after_execution
    @doc(p_zhi_multi_select_show_listed_to_be_listed)
    def zhi_multi_select_show_listed_to_be_listed(self):
        self.menu_manage()
        (self.step(key='adjust_ad_placements', desc='调整广告位')
         .step(key='show_wait_shelves', desc='显示待上架')
         .scroll('save_and_update', desc='保存并更新')
         .step(key='save_and_update', desc='保存并更新')
         .wait())
        return

    @reset_after_execution
    @doc(p_zhi_multi_select_show_listed_pending_removed)
    def zhi_multi_select_show_listed_pending_removed(self):
        self.menu_manage()
        (self.step(key='adjust_ad_placements', desc='调整广告位')
         .step(key='show_wait_shelves', desc='显示待上架')
         .step(key='show_removed', desc='显示已下架')
         .scroll('save_and_update', desc='保存并更新')
         .step(key='save_and_update', desc='保存并更新')
         .wait())
        return

    @reset_after_execution
    @doc(p_zhi_view_logs)
    def zhi_view_logs(self):
        self.menu_manage()
        (self.step(key='view_logs', desc='查看日志')
         .wait())
        return

    @reset_after_execution
    @doc(p_zhi_derived)
    def zhi_derived(self):
        self.menu_manage()
        (self.step(key='direct_deduced', desc='导出')
         .wait())
        return


class PlatformMerchantManagePages(CommonPages):
    """平台管理|商户管理"""


class PlatformMessageReleaseListPages(CommonPages):
    """平台管理|消息管理|消息发布列表"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='platform_manage_menu', desc='平台管理')
         .scroll(key='platform_message_manage_menu', desc='消息管理')
         .step(key='platform_message_manage_menu', desc='消息管理')
         .step(key='platform_message_release_list_menu', desc='消息发布列表')
         .wait())
        return self

    @reset_after_execution
    @doc(p_platform_approved)
    def platform_approved(self):
        self.menu_manage()
        (self.step(key='delivery_receipt', desc='回收商发布')
         .step(key='order_review_search', desc='搜索')
         .step(key='platform_review', desc='平台审核')
         .step(key='platform_review_through', desc='通过')
         .step(key='platform_review_ok', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(p_platform_refuse)
    def platform_refuse(self):
        self.menu_manage()
        (self.step(key='delivery_receipt', desc='回收商发布')
         .step(key='order_review_search', desc='搜索')
         .step(key='platform_review', desc='平台审核')
         .step(key='platform_review_refuse', desc='拒绝')
         .step(key='platform_reason_refusal', value=self.serial, action='input', desc='拒绝原因')
         .step(key='platform_review_ok', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(p_platform_back)
    def platform_back(self):
        self.menu_manage()
        (self.step(key='delivery_receipt', desc='回收商发布')
         .step(key='search', desc='搜索')
         .step(key='platform_back', desc='平台撤回')
         .custom(self.wait_time)
         .step(key='ok', desc='确定')
         .wait())
        return self


class PlatformProductReviewPages(CommonPages):
    """平台管理|同售管理|商品审核"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='platform_manage_menu', desc='平台管理')
         .scroll(key='platform_sold_manage_menu', desc='同售管理')
         .step(key='platform_sold_manage_menu', desc='同售管理')
         .step(key='platform_goods_review_menu', desc='商品审核')
         .wait())
        return self


class PlatformPurseCenterPages(CommonPages):
    """平台管理|订单管理|订单审核"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='platform_manage_menu', desc='平台管理')
         .scroll(key='platform_order_manage_menu', desc='订单管理')
         .step(key='platform_order_manage_menu', desc='订单管理')
         .step(key='platform_order_review_menu', desc='订单审核')
         .wait())
        return self

    @reset_after_execution
    @doc(p_platform_approval)
    def platform_approval(self):
        self.menu_manage()
        (self.step(key='order_examine', desc='审核')
         .step(key='audit_opinion', value=self.serial, action='input', desc='审核说明')
         .step(key='review_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(p_platform_audit_rejection)
    def platform_audit_rejection(self):
        self.menu_manage()
        (self.step(key='order_examine', desc='审核')
         .step(key='turn_down', desc='未通过')
         .step(key='audit_opinion', value=self.serial, action='input', desc='审核说明')
         .step(key='review_confirmation', desc='确认')
         .wait())
        return self
