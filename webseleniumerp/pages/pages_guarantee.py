# coding: utf-8
import os
from common.base_page import BasePage, ImportDataEdit, reset_after_execution
from common.base_params import InitializeParams
from common.import_desc import *
from config.settings import DATA_PATHS


class CommonPages(BasePage, InitializeParams):

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


class GuaranteeOrderManagePages(CommonPages):
    """保卖管理|订单列表"""

    def menu_manage(self):
        """菜单"""
        (self.scroll('guarantee_menu', desc='保卖管理')
         .step(key='guarantee_menu', desc='保卖管理')
         .step(key='guarantee_order_manage_menu', desc='订单列表')
         .wait())
        return self

    @reset_after_execution
    @doc(g_quick_guarantee_item_submission)
    def quick_guarantee_item_submission(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=2, j=3)[0]['articlesNo'])
        (self.step(key='quick_guarantee', desc='快速保卖')
         .step(key='item_number_ipt', desc='物品编号输入框')
         .step(key='input_articlesNo_box', desc='物品编号输入框')
         .custom(lambda: self.affix())
         .step(key='input_confirm', desc='确认输入')
         .step(key='ask_price_first', value=998, action='input', desc='期望卖出价')
         .step(key='submit', desc='提交')
         .wait())
        return self

    @reset_after_execution
    @doc(g_quick_guarantee_item_submission_delivery)
    def quick_guarantee_item_submission_delivery(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=2, j=3)[0]['articlesNo'])
        (self.step(key='quick_guarantee', desc='快速保卖')
         .step(key='item_number_ipt', desc='物品编号输入框')
         .step(key='input_articlesNo_box', desc='物品编号输入框')
         .custom(lambda: self.affix())
         .step(key='input_confirm', desc='确认输入')
         .step(key='ask_price_first', value=998, action='input', desc='期望卖出价')
         .step(key='submit_and_delivery', desc='提交并发货')
         .step(key='sf_express', desc='选择顺丰')
         .step(key='delivery_confirm', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(g_quick_guarantee_item_submission_delivery_jd)
    def quick_guarantee_item_submission_delivery_jd(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=2, j=3)[0]['articlesNo'])
        (self.step(key='quick_guarantee', desc='快速保卖')
         .step(key='item_number_ipt', desc='物品编号输入框')
         .step(key='input_articlesNo_box', desc='物品编号输入框')
         .custom(lambda: self.affix())
         .step(key='input_confirm', desc='确认输入')
         .step(key='ask_price_first', value=998, action='input', desc='期望卖出价')
         .step(key='submit_and_delivery', desc='提交并发货')
         .step(key='jd_express', desc='选择京东')
         .step(key='delivery_confirm', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(g_quick_guarantee_item_submission_delivery_self_mail)
    def quick_guarantee_item_submission_delivery_self_mail(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=2, j=3)[0]['articlesNo'])
        (self.step(key='quick_guarantee', desc='快速保卖')
         .step(key='item_number_ipt', desc='物品编号输入框')
         .step(key='input_articlesNo_box', desc='物品编号输入框')
         .custom(lambda: self.affix())
         .step(key='input_confirm', desc='确认输入')
         .step(key='ask_price_first', value=998, action='input', desc='期望卖出价')
         .step(key='submit_and_delivery', desc='提交并发货')
         .step(key='self_mail', desc='选择自行邮寄')
         .step(key='input_logistics', value=self.jd, action='input', desc='物流单号')
         .step(key='choice_company', desc='选择物流公司')
         .custom(lambda: self.down_arrow_return(6))
         .step(key='delivery_confirm', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(g_fast_item_shipping_by_yourself)
    def fast_item_shipping_by_yourself(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=2, j=3)[0]['articlesNo'])
        (self.step(key='quick_guarantee', desc='快速保卖')
         .step(key='item_number_ipt', desc='物品编号输入框')
         .step(key='input_articlesNo_box', desc='物品编号输入框')
         .custom(lambda: self.affix())
         .step(key='input_confirm', desc='确认输入')
         .step(key='ask_price_first', value=998, action='input', desc='期望卖出价')
         .step(key='submit_and_delivery', desc='提交并发货')
         .step(key='deliver_it_yourself', desc='选择自己送货')
         .step(key='delivery_confirm', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(g_ship_now_by_express_sf)
    def ship_now_by_express_sf(self):
        self.menu_manage()
        (self.step(key='shipped_immediately_first', desc='立即发货')
         .step(key='sf_express', desc='选择顺丰')
         .step(key='delivery_confirm', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(g_ship_now_by_express_jd)
    def ship_now_by_express_jd(self):
        self.menu_manage()
        (self.step(key='shipped_immediately_first', desc='立即发货')
         .step(key='submit_and_delivery', desc='提交并发货')
         .step(key='jd_express', desc='选择京东')
         .step(key='delivery_confirm', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(g_ship_now_by_express_self_mail)
    def ship_now_by_express_self_mail(self):
        self.menu_manage()
        (self.step(key='shipped_immediately_first', desc='立即发货')
         .step(key='self_mail', desc='选择自行邮寄')
         .step(key='input_logistics', value=self.jd, action='input', desc='输入物流单号')
         .step(key='choice_company', desc='选择物流公司')
         .custom(lambda: self.down_arrow_return(6))
         .step(key='delivery_confirm', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(g_quick_guarantee_cancel_the_order)
    def quick_guarantee_cancel_the_order(self):
        self.menu_manage()
        (self.step(key='cancel_order_first', desc='取消订单')
         .step(key='confirm_button_tip', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(g_fast_guarantee_reshipment)
    def fast_guarantee_reshipment(self):
        self.menu_manage()
        (self.step(key='reship_first', desc='重新发货')
         .step(key='sf_express', desc='选择顺丰')
         .step(key='delivery_confirm', desc='确定')
         .wait())
        return self


class GuaranteeReturnsManagePages(CommonPages):
    """保卖管理|退货管理"""

    def menu_manage(self):
        """菜单"""
        (self.scroll('guarantee_menu', desc='保卖管理')
         .step(key='guarantee_menu', desc='保卖管理')
         .step(key='guarantee_returns_manage_menu', desc='退货管理')
         .wait())
        return self

    @reset_after_execution
    @doc(g_cancel_returns_by_mail)
    def cancel_returns_by_mail(self):
        self.menu_manage()
        (self.step(key='pending_returns_btn', desc='待退货')
         .step(key='cancel_return', desc='取消退货')
         .step(key='cancel_the_sale_confirmation', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(g_change_the_return_method_by_mail)
    def change_the_return_method_by_mail(self):
        self.menu_manage()
        (self.step(key='pending_returns_btn', desc='待退货')
         .step(key='change_return_method', desc='更改退货方式')
         .step(key='change_confirm', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(g_self_lifted_cancel_a_return)
    def self_lifted_cancel_a_return(self):
        self.menu_manage()
        (self.step(key='waiting_for_pickup_btn', desc='待取货')
         .step(key='cancel_return', desc='取消退货')
         .step(key='cancel_the_sale_confirmation', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(g_change_the_return_method)
    def change_the_return_method(self):
        self.menu_manage()
        (self.step(key='waiting_for_pickup_btn', desc='待取货')
         .step(key='change_return_method', desc='更改退货方式')
         .step(key='change_confirm', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(g_confirm_receipt)
    def confirm_receipt(self):
        self.menu_manage()
        (self.step(key='return_has_been_removed', desc='退货已出库')
         .step(key='confirm_receipt', desc='确认收货')
         .wait())
        return self


class GuaranteeGoodsManagePages(CommonPages):
    """保卖管理|商品管理"""

    def menu_manage(self):
        """菜单"""
        (self.scroll('guarantee_menu', desc='保卖管理')
         .step(key='guarantee_menu', desc='保卖管理')
         .step(key='guarantee_goods_manage_menu', desc='商品管理')
         .wait())
        return self

    @reset_after_execution
    @doc(g_return_method_express)
    def return_method_express(self):
        self.menu_manage()
        (self.step(key='return', desc='退货')
         .step(key='next_step', desc='下一步')
         .step(key='return_confirm', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(g_return_method_self_lifted)
    def return_method_self_lifted(self):
        self.menu_manage()
        (self.step(key='return', desc='退货')
         .step(key='next_step', desc='下一步')
         .step(key='returns_and_self_pickup', desc='自提')
         .step(key='return_confirm', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(g_sell_bid_reference_price)
    def sell_bid_reference_price(self):
        self.menu_manage()
        (self.step(key='sales_first', desc='销售')
         .step(key='today_price', desc='今日参考价')
         .step(key='sales_confirm', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(g_cancel_the_sale)
    def cancel_the_sale(self):
        self.menu_manage()
        (self.step(key='cancel_sales', desc='取消销售')
         .step(key='cancel_the_sale_confirmation', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(g_update_price)
    def update_price(self):
        self.menu_manage()
        (self.step(key='update_sales', desc='改价')
         .step(key='input_update_sales', value="50", action='input', desc='输入价格')
         .step(key='update_sales_button', desc='确认改价')
         .wait())
        return self
