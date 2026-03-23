# coding: utf-8
import os

from common.base_params import InitializeParams
from config.settings import DATA_PATHS
from common.base_page import BasePage, ImportDataEdit, reset_after_execution
from common.import_desc import *


class CommonPages(BasePage, InitializeParams):

    def __init__(self, driver):
        super().__init__(driver)
        self._steps_queue = []
        self.file = ImportDataEdit(driver)
        self.file_paths = self.file.file_paths = {
            'excel': os.path.join(DATA_PATHS['excel'], 'help_sell_orders_import.xlsx')
        }

    def menu(self, menu_type, key):
        """获取元素"""
        menu_mapping = {
            'main': self.elem_positioning['positioning'],
        }
        if menu_type in menu_mapping:
            return self.exc(lambda: menu_mapping[menu_type][key])
        else:
            raise ValueError(f"menu not found: {menu_type}")


class HelpGenerateOrderPages(CommonPages):
    """帮卖管理|帮卖上架列表"""

    def menu_manage(self):
        """菜单"""
        (self.scroll(key='help_sell_manage_menu', desc='帮卖管理')
         .step(key='help_sell_manage_menu', desc='帮卖管理')
         .step(key='help_sell_the_listing_list_menu', desc='帮卖上架列表')
         .wait())
        return self

    @reset_after_execution
    @doc(h_add_item)
    def add_item(self):
        self.menu_manage()
        (self.step(key='bulk_shakedown', desc='发起帮卖')
         .step(key='inventory_add', desc='从库存列表添加')
         .step(key='search', desc='搜索')
         .custom(lambda: self.tab_return(3))
         .scroll('confirm_select', desc='确认选择')
         .step(key='confirm_select', desc='确认选择')
         .custom(lambda: self.wait_time(2))
         .wait())
        return self

    @reset_after_execution
    def place_a_help_order(self):
        self.menu_manage()
        (self.step(key='bulk_shakedown', desc='发起帮卖')
         .step(key='inventory_add', desc='从库存列表添加')
         .step(key='search', desc='搜索')
         .custom(lambda: self.tab_return(3))
         .scroll('confirm_select', desc='确认选择')
         .step(key='confirm_select', desc='确认选择')
         .step(key='expected_price', value=self.number, action='input', desc='期望价格')
         .step(key='add_item_btn', desc='添加')
         .custom(lambda: self.tab_return(3))
         .step(key='batch_note', value=self.serial, action='input', desc='批次备注')
         .step(key='generate_help_orders', desc='生成帮卖订单')
         .step(key='delete_address_ok', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(h_new_help_order)
    def new_help_order(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=2)[0]['imei'])
        (self.step(key='bulk_shakedown', desc='发起帮卖')
         .step(key='item_imei_input', desc='物品编号')
         .custom(lambda: self.affix())
         .step(key='add_item_btn', desc='添加')
         .step(key='expected_price', value=self.number, action='input', desc='期望价格')
         .step(key='add_item_btn', desc='添加')
         .custom(lambda: self.tab_return(3))
         .step(key='batch_note', value=self.serial, action='input', desc='批次备注')
         .step(key='generate_help_orders', desc='生成帮卖订单')
         .step(key='delete_address_ok', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(h_sf_express_delivery_is_easy)
    def sf_express_delivery_is_easy(self):
        self.menu_manage()
        (self.step(key='to_deliver_goods', desc='去发货')
         .step(key='help_calculate_freight', desc='计算运费')
         .step(key='shipment_confirmed', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(h_self_dispatch)
    def self_dispatch(self):
        self.menu_manage()
        (self.step(key='to_deliver_goods', desc='去发货')
         .step(key='self_post', desc='自行邮寄')
         .step(key='tracking_number', value=self.jd, action='input', desc='快递单号')
         .step(key='express_company_ipt', value='京东快递', action='input', desc='快递公司')
         .step(key='phone_number', value=self.phone, action='input', desc='手机号码')
         .step(key='shipment_confirmed', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(h_send_it_yourself)
    def send_it_yourself(self):
        self.menu_manage()
        (self.step(key='to_deliver_goods', desc='去发货')
         .step(key='self_delivery', desc='自己送')
         .step(key='shipment_confirmed', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(h_cancel_order)
    def cancel_order(self):
        self.menu_manage()
        (self.step(key='delivery_receipt', desc='订单列表')
         .step(key='cancel_order', desc='取消订单')
         .step(key='quality_items_receive_ok', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(h_apply_for_cancellation)
    def apply_for_cancellation(self):
        self.menu_manage()
        (self.step(key='delivery_receipt', desc='订单列表')
         .step(key='manual_signature', desc='申请退机')
         .step(key='quality_items_receive_ok', desc='确认申请退机')
         .wait())
        return self

    @reset_after_execution
    @doc(h_manual_signature)
    def manual_signature(self):
        self.menu_manage()
        (self.step(key='delivery_receipt', desc='订单列表')
         .step(key='manual_signature', desc='手动签收')
         .step(key='delete_address_ok', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(h_logistics_signature)
    def logistics_signature(self):
        self.menu_manage()
        (self.step(key='delivery_receipt', desc='订单列表')
         .step(key='logistics_signature', desc='物流签收')
         .step(key='inbound_search', desc='搜索')
         .custom(lambda: self.tab_return(6))
         .step(key='be_put_in_storage', desc='签收入库')
         .step(key='circulation_warehouse', desc='流转仓库')
         .custom(lambda: self.up_arrow_return())
         .step(key='submit_into_the_warehouse', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(h_confirmation_bond)
    def confirmation_bond(self):
        self.menu_manage()
        (self.step(key='delivery_receipt', desc='订单列表')
         .step(key='confirmation_bond', desc='确认保卖')
         .step(key='platform_review_ok', desc='确定')
         .custom(lambda: self.wait_time(5))
         .custom(lambda: self.refresh_page())
         .wait())
        return self

    @reset_after_execution
    @doc(h_apply_for_bargaining)
    def apply_for_bargaining(self):
        self.menu_manage()
        (self.step(key='delivery_receipt', desc='订单列表')
         .step(key='apply_for_bargaining', desc='申请议价')
         .step(key='application_instructions', value=self.serial, action='input', desc='申请说明')
         .step(key='platform_review_ok', desc='确定')
         .wait())
        return self


class HelpSellTheListOfGoodsPages(CommonPages):
    """帮卖管理|帮卖来货列表"""

    def menu_manage(self):
        """菜单"""
        (self.scroll(key='help_sell_manage_menu', desc='帮卖管理')
         .step(key='help_sell_manage_menu', desc='帮卖管理')
         .step(key='help_sell_the_list_of_goods_menu', desc='帮卖来货列表')
         .wait())
        return self

    @reset_after_execution
    @doc(h_the_flow_of_goods_is_signed)
    def the_flow_of_goods_is_signed(self):
        self.menu_manage()
        (self.step(key='logistics_sign_off', desc='物流签收')
         .custom(lambda: self.wait_time())
         .step(key='inbound_search', desc='搜索')
         .custom(lambda: self.tab_return(6))
         .step(key='be_put_in_storage', desc='签收入库')
         .step(key='circulation_warehouse', desc='流转仓库')
         .custom(lambda: self.up_arrow_return())
         .step(key='submit_into_the_warehouse', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(h_manual_signature)
    def manual_signature(self):
        self.menu_manage()
        (self.step(key='manual_signature', desc='手动签收')
         .step(key='manual_sign_off_is_confirmed', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(h_go_to_quality)
    def go_to_quality(self):
        self.menu_manage()
        (self.step(key='delivery_receipt', desc='订单列表')
         .step(key='return_machine', desc='去质检')
         .step(key='fineness_color', desc='成色')
         .custom(lambda: self.up_arrow_return())
         .step(key='remarks', value='质检备注', action='input', desc='备注')
         .step(key='labor_costs', value=self.number, action='input', desc='预售保卖价')
         .step(key='go_to_quality_inspection_to_determine', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(h_de_check)
    def de_check(self):
        self.menu_manage()
        (self.step(key='delivery_receipt', desc='订单列表')
         .step(key='return_machine', desc='去复检')
         .scroll('guaranteed_price', desc='预售保卖价')
         .step(key='labor_costs', value=self.number, action='input', desc='预售保卖价')
         .step(key='go_to_the_re_inspection_to_confirm', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(h_audit_rejection)
    def audit_rejection(self):
        self.menu_manage()
        (self.step(key='delivery_receipt', desc='订单列表')
         .step(key='audit_rejection', desc='审核拒绝')
         .step(key='reason_for_refusal', value=self.serial, action='input', desc='拒绝原因')
         .step(key='help_review_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(h_go_to_sale)
    def go_to_sale(self):
        self.menu_manage()
        (self.step(key='delivery_receipt', desc='订单列表')
         .step(key='go_to_sell', desc='去销售')
         .step(key='definite_jump', desc='确认跳转')
         .custom(lambda: self.wait_time())
         .step(key='single_choice', desc='单选')
         .step(key='out_storage', desc='出库')
         .step(key='sale_client', desc='销售客户')
         .custom(lambda: self.up_arrow_return())
         .step(key='tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='express_amount', value=self.number, action='input', desc='物流费用')
         .scroll('sell_sales_order_number', desc='销售金额')
         .step(key='sell_sales_amount', value='5', action='input', desc='销售金额')
         .step(key='platform_number', value=self.serial, action='input', desc='平台物品编号')
         .step(key='sell_sales_order_number', value=self.serial, action='input', desc='平台销售订单号')
         .scroll('the_amount_of_the_payout', desc='收款金额')
         .step(key='money_received', desc='已收款')
         .step(key='collection_account', desc='收款账户')
         .custom(lambda: self.up_arrow_return())
         .step(key='the_amount_of_the_payout', value='5', action='input', desc='收款金额')
         .step(key='verify', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(h_manual_settlement)
    def manual_settlement(self):
        self.menu_manage()
        (self.step(key='delivery_receipt', desc='订单列表')
         .step(key='return_machine', desc='手动结算')
         .step(key='inventory_count_determined', desc='确定')
         .step(key='return_machine', desc='手动结算')
         .step(key='inventory_count_determined', desc='确定')
         .custom(lambda: self.wait_time())
         .wait())
        return self

    @reset_after_execution
    @doc(h_express_delivery_unit_set_return_machine)
    def express_delivery_unit_set_return_machine(self):
        self.menu_manage()
        (self.step(key='delivery_receipt', desc='订单列表')
         .step(key='return_machine', desc='去退机')
         .scroll('go_to_the_retirement_machine_ok', desc='确定')
         .step(key='calculate_freight', desc='计算运费')
         .custom(lambda: self.wait_time())
         .step(key='go_to_the_retirement_machine_ok', desc='确定')
         .wait())
        return self


class HelpServiceConfigurationPages(CommonPages):
    """帮卖管理|帮卖业务配置"""

    def menu_manage(self):
        """菜单"""
        (self.scroll(key='help_sell_manage_menu', desc='帮卖管理')
         .step(key='help_sell_manage_menu', desc='帮卖管理')
         .step(key='help_sell_business_config_menu', desc='帮卖业务配置')
         .wait())
        return self

    @reset_after_execution
    @doc(h_edit_configuration_information)
    def edit_configuration_information(self):
        self.menu_manage()
        (self.step(key='modify_the_business_configuration', desc='编辑')
         .scroll('selling_days', desc='销售天数')
         .step(key='selling_days', value='30', action='input', desc='销售天数')
         .step(key='return_flight', value='10', action='input', desc='退机回寄天数')
         .step(key='auto_settlement', value='10', action='input', desc='自动结算天数')
         .step(key='service_configuration_confirmation', desc='确认')
         .wait())
        return self
