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
            'excel': os.path.join(DATA_PATHS['excel'], 'sell_goods_listing_import.xlsx'),
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


class SellAfterSalesHandlingPages(CommonPages):
    """商品销售|销售售后管理|销售售后处理"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='sell_commodity_sales_menu', desc='商品销售')
         .step(key='sell_after_sales_manage_menu', desc='销售售后管理')
         .step(key='sell_after_sale_treatment_menu', desc='销售售后处理')
         .wait())
        return self

    @reset_after_execution
    @doc(s_sales_after_sales_returns)
    def sales_after_sales_returns(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=3, j=9)[0]['articleNo'])
        (self.step(key='item_ipt', desc='物品编号输入框')
         .custom(lambda: self.affix_carriage_return())
         .step(key='after_sale_treatment', desc='销售售后处理')
         .step(key='after_sale_type', desc='售后类型')
         .custom(lambda: self.down_arrow_return())
         .step(key='after_sales_have_been_received', desc='已收货')
         .step(key='circulation_warehouse', desc='流转仓库')
         .custom(lambda: self.down_arrow_return())
         .step(key='please_enter_remark', value=self.serial, action='input', desc='备注')
         .step(key='after_sales_return_confirmation', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(s_sell_returned_spare_parts_after_sale_journey)
    def sell_returned_spare_parts_after_sale_journey(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=3, j=9)[0]['articleNo'])
        (self.step(key='item_imei_input', desc='物品编号输入框')
         .custom(lambda: self.affix_carriage_return())
         .step(key='after_sale_treatment', desc='销售售后处理')
         .step(key='please_select_the_after_sales_type', desc='售后类型')
         .custom(lambda: self.down_arrow_return(2))
         .step(key='please_enter_the_new_sales_settlement_price', value='2873', action='input', desc='新销售结算价')
         .step(key='sort', desc='配件分类')
         .custom(lambda: self.up_arrow_return(2))
         .step(key='sort', desc='配件分类')
         .step(key='accessories_name', desc='配件名称')
         .custom(lambda: self.up_arrow_return())
         .step(key='brand', desc='品牌')
         .custom(lambda: self.up_arrow_return())
         .step(key='model', desc='型号')
         .custom(lambda: self.up_arrow_return())
         .step(key='accessories_channel', desc='配件渠道')
         .custom(lambda: self.up_arrow_return())
         .step(key='accessory_value', value='122', action='input', desc='配件价值')
         .step(key='tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='please_enter_remark', value=self.serial, action='input', desc='备注')
         .step(key='after_sales_processing_confirmation', desc='确定')
         .wait())
        return self


class SellGoodsListingPages(CommonPages):
    """商品销售|销售管理|销售上架"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='sell_commodity_sales_menu', desc='商品销售')
         .step(key='sell_manage_menu', desc='销售管理')
         .step(key='sell_listing_menu', desc='销售上架')
         .wait())
        return self

    @reset_after_execution
    @doc(s_sell_goods_listing)
    def sell_goods_listing(self):
        self.menu_manage()
        self.file.get_inventory_data('excel', 'articles_no', i=2, j=13)
        (self.step(key='custom_input', desc='销售客户')
         .custom(lambda: self.down_arrow_return())
         .step(key='add_goods_input', desc='物品输入框')
         .custom(lambda: self.affix())
         .step(key='sell_add_item_btn', desc='添加物品')
         .step(key='set_the_sale_price', value='263', action='input', desc='设置销售价')
         .step(key='articles_no_input', value=self.serial, action='input', desc='平台物品编号')
         .step(key='sales_listing_remarks', value=self.serial, action='input', desc='备注')
         .step(key='confirm_add_btn', desc='确认添加')
         .wait())
        return self


class SellGoodsReceivedPages(CommonPages):
    """商品销售|销售管理|待接收物品"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='sell_commodity_sales_menu', desc='商品销售')
         .step(key='sell_manage_menu', desc='销售管理')
         .step(key='sell_items_awaiting_receipt_menu', desc='待接收物品')
         .wait())
        return self

    @reset_after_execution
    @doc(s_goods_received)
    def goods_received(self):
        self.menu_manage()
        (self.step(key='select_all_dio', desc='全选')
         .step(key='sell_receive', desc='接收')
         .step(key='quality_items_receive_ok', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(s_scan_goods_received)
    def scan_goods_received(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=2)[0]['articlesNo'])
        (self.step(key='sales_scan_the_code_to_receive_accurately', desc='扫码精确接收')
         .custom(lambda: self.affix_carriage_return())
         .step(key='sell_scan_receive', desc='接收')
         .step(key='quality_items_receive_ok', desc='确定')
         .wait())
        return self


class SellMiddleItemListPages(CommonPages):
    """商品销售|销售管理|销售中物品列表"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='sell_commodity_sales_menu', desc='商品销售')
         .step(key='sell_manage_menu', desc='销售管理')
         .step(key='sell_middle_item_list_menu', desc='销售中物品列表')
         .wait())
        return self

    @reset_after_execution
    @doc(s_edit_sale_info_import)
    def edit_sale_info_import(self):
        self.menu_manage()
        self.file.get_inventory_data('excel', 'imei', i=2, j=13)
        (self.step(key='edit_info_btn', desc='修改销售信息')
         .step(key='import_btn', desc='导入添加')
         .step(key='import_the_template', desc='导入模版')
         .custom(lambda: self.up_arrow_return(2))
         .step(key='handover_import', value=self.file_paths['excel'], action='upload', desc='上传文件')
         .step(key='import_confirm', desc='确定')
         .step(key='new_platform_item_number', value=self.serial, action='input', desc='新平台物品编号')
         .scroll('edit_status_price', desc='新销售定价')
         .step(key='labor_costs', value=self.number, action='input', desc='新销售定价')
         .step(key='edit_status_confirm', desc='确认修改')
         .wait())
        return self

    @reset_after_execution
    @doc(s_edit_status_info_not_received)
    def edit_status_info_not_received(self):
        self.menu_manage()
        (self.step(key='edit_status_btn', desc='更新销售状态')
         .step(key='sell_unpaid', desc='未收款')
         .step(key='tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='express_amount', value=self.number, action='input', desc='物流费用')
         .step(key='edit_sale_status_confirm', desc='确认销售')
         .wait())
        return self

    @reset_after_execution
    @doc(s_on_and_off_shelves)
    def on_and_off_shelves(self):
        self.menu_manage()
        (self.step(key='take_it_down', desc='下架')
         .step(key='removed_items_added', desc='添加')
         .custom(lambda: self.wait_time())
         .step(key='confirm_the_shakedown', desc='确认下架')
         .wait())
        return self

    @reset_after_execution
    @doc(s_bulk_shakedown)
    def bulk_shakedown(self):
        self.menu_manage()
        (self.step(key='procurement_info', desc='销售中')
         .step(key='on_sale_single_selection', desc='单选')
         .step(key='bulk_shakedown', desc='批量下架')
         .step(key='removed_items_added', desc='添加')
         .step(key='confirm_the_shakedown', desc='确认下架')
         .wait())
        return self


class SellSaleItemPages(CommonPages):
    """商品销售|销售管理|待销售物品"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='sell_commodity_sales_menu', desc='商品销售')
         .step(key='sell_manage_menu', desc='销售管理')
         .step(key='sell_items_for_sale_menu', desc='待销售物品')
         .wait())
        return self

    @reset_after_execution
    @doc(s_sell_listing)
    def sell_listing(self):
        self.menu_manage()
        (self.step(key='to_be_sold_single', desc='单选')
         .step(key='more_handover_btn', desc='上架')
         .step(key='custom_input', desc='销售客户')
         .custom(lambda: self.up_arrow_return())
         .step(key='reject_the_note', value='299', action='input', desc='销售定价')
         .step(key='articles_no_input', value=self.serial, action='input', desc='平台物品编号')
         .step(key='remark_input', value=self.serial, action='input', desc='备注')
         .step(key='confirm_add_btn', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(s_sell_get_out)
    def sell_get_out(self):
        self.menu_manage()
        (self.step(key='to_be_sold_single', desc='单选')
         .step(key='out_storage', desc='出库')
         .step(key='sale_client', desc='销售客户')
         .custom(lambda: self.up_arrow_return())
         .step(key='tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='express_amount', value='12', action='input', desc='物流费用')
         .scroll('sell_sales_amount', desc='销售金额')
         .step(key='sell_sales_amount', value='263', action='input', desc='销售金额')
         .step(key='platform_number', value=self.serial, action='input', desc='平台物品编号')
         .step(key='sell_sales_order_number', value=self.serial, action='input', desc='平台销售订单号')
         .scroll('money_not_received', desc='未收款')
         .step(key='money_not_received', desc='未收款')
         .step(key='verify', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(s_sell_advance_sale)
    def sell_advance_sale(self):
        self.menu_manage()
        (self.step(key='to_be_sold_single', desc='单选')
         .step(key='out_storage', desc='出库')
         .step(key='distribution_warehouse', desc='铺货预售出库')
         .step(key='sale_client', desc='销售客户')
         .custom(lambda: self.up_arrow_return())
         .step(key='sale_predict', desc='预售')
         .step(key='tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='express_amount', value='21', action='input', desc='物流费用')
         .step(key='verify', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(s_sell_distribution)
    def sell_distribution(self):
        self.menu_manage()
        (self.step(key='to_be_sold_single', desc='单选')
         .step(key='out_storage', desc='出库')
         .step(key='distribution_warehouse', desc='铺货预售出库')
         .step(key='sale_client', desc='销售客户')
         .custom(lambda: self.up_arrow_return())
         .step(key='received_button', desc='铺货')
         .step(key='not_money_not_received', desc='未收款')
         .step(key='collection_account_2', desc='收款账户')
         .custom(lambda: self.up_arrow_return())
         .step(key='tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='express_amount', value='14', action='input', desc='物流费用')
         .scroll('remark_3', desc='备注')
         .step(key='sell_sales_amount_2', value='115', action='input', desc='销售金额')
         .step(key='remark_3', value=self.serial, action='input', desc='备注')
         .step(key='verify', desc='确认')
         .wait())
        return self


class SellSaleItemListPages(CommonPages):
    """商品销售|销售管理|已销售物品列表"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='sell_commodity_sales_menu', desc='商品销售')
         .step(key='sell_manage_menu', desc='销售管理')
         .step(key='sell_list_of_sold_items_menu', desc='已销售物品列表')
         .wait())
        return self

    @reset_after_execution
    @doc(s_sell_refund_difference)
    def sell_refund_difference(self):
        self.menu_manage()
        (self.step(key='sold_single_selection', desc='单选')
         .step(key='after_sales', desc='销售售后')
         .step(key='after_sale_treatment', desc='销售售后处理')
         .step(key='new_sales_price', value='1982', action='input', desc='新销售结算价')
         .step(key='please_enter_remark', value=self.serial, action='input', desc='备注')
         .step(key='verify_2', desc='确定')
         .wait())
        return self


    @reset_after_execution
    @doc(s_sell_return_goods_warehousing)
    def sell_return_goods_warehousing(self):
        self.menu_manage()
        (self.step(key='single_choice', desc='单选')
         .step(key='after_sales', desc='销售售后')
         .step(key='after_sale_treatment', desc='销售售后处理')
         .step(key='after_sale_type', desc='售后类型')
         .custom(lambda: self.down_arrow_return())
         .step(key='received_2', desc='已收货')
         .step(key='stash', desc='流转仓库')
         .custom(lambda: self.down_arrow_return())
         .step(key='please_enter_remark', value=self.serial, action='input', desc='备注')
         .step(key='verify_2', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(s_sell_return_only_parts_route)
    def sell_return_only_parts_route(self):
        self.menu_manage()
        (self.step(key='single_choice', desc='单选')
         .step(key='after_sales', desc='销售售后')
         .step(key='after_sale_treatment', desc='销售售后处理')
         .step(key='after_sale_type', desc='售后类型')
         .custom(lambda: self.down_arrow_return(2))
         .step(key='new_sales_price', value='100', action='input', desc='新销售结算价')
         .step(key='sort', desc='配件分类')
         .custom(lambda: self.up_arrow_return(2))
         .step(key='sort', desc='配件分类')
         .step(key='name', desc='配件名称')
         .custom(lambda: self.up_arrow_return())
         .step(key='brand', desc='品牌')
         .custom(lambda: self.up_arrow_return())
         .step(key='model_number', desc='型号')
         .custom(lambda: self.up_arrow_return())
         .step(key='channel', desc='配件渠道')
         .custom(lambda: self.up_arrow_return())
         .step(key='accessory_value', value='23', action='input', desc='配件价值')
         .step(key='tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='please_enter_remark', value=self.serial, action='input', desc='备注')
         .step(key='verify', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(s_sales_are_refunded_only)
    def sales_are_refunded_only(self):
        self.menu_manage()
        (self.step(key='single_choice', desc='单选')
         .step(key='after_sales', desc='销售售后')
         .step(key='after_sale_treatment', desc='销售售后处理')
         .step(key='after_sale_type', desc='售后类型')
         .custom(lambda: self.down_arrow_return(4))
         .step(key='please_enter_remark', value=self.serial, action='input', desc='备注')
         .step(key='verify_2', desc='确定')
         .wait())
        return self


class SellSalesListPages(CommonPages):
    """商品销售|销售售后管理|销售售后列表"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='sell_commodity_sales_menu', desc='商品销售')
         .step(key='sell_after_sales_manage_menu', desc='销售售后管理')
         .step(key='sell_after_sales_list_menu', desc='销售售后列表')
         .wait())
        return self

    @reset_after_execution
    @doc(s_sell_after_sale_attachment)
    def sell_after_sale_attachment(self):
        self.menu_manage()
        (self.step(key='update_the_aftermarket_selection', desc='单选')
         .step(key='generate_purchase_order', desc='更新售后状态')
         .step(key='select_the_warehouse_c', desc='流转仓库')
         .custom(lambda: self.up_arrow_return())
         .step(key='verify_stash', desc='确认入库')
         .wait())
        return self

    @reset_after_execution
    @doc(s_sell_after_sale_refund)
    def sell_after_sale_refund(self):
        self.menu_manage()
        (self.step(key='update_the_aftermarket_selection', desc='单选')
         .step(key='generate_purchase_order', desc='更新售后状态')
         .step(key='refund', desc='退货退款')
         .step(key='platform_penalty', value='23', action='input', desc='平台售后罚款')
         .step(key='remark_input', value=self.serial, action='input', desc='备注')
         .step(key='refund_verify', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(s_sell_after_sale_barter)
    def sell_after_sale_barter(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=2, j=15)[0]['imei'])
        (self.step(key='update_the_aftermarket_selection', desc='单选')
         .step(key='generate_purchase_order', desc='更新售后状态')
         .step(key='barter_btn', desc='换货')
         .step(key='refund_verify', desc='去出库')
         .step(key='tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='express_amount', value='23', action='input', desc='物流费用')
         .scroll('barter_item_input', desc='换货出库物品输入框')
         .step(key='barter_item_input', desc='换货出库物品输入框')
         .custom(lambda: self.affix())
         .step(key='barter_add', desc='添加')
         .scroll('barter_remark_2', desc='备注信息')
         .step(key='selling_price', value='10', action='input', desc='销售结算价')
         .step(key='platform_order_number_2', value=self.serial, action='input', desc='平台销售订单号')
         .step(key='barter_remark_2', value=self.serial, action='input', desc='备注信息')
         .step(key='verify_out', desc='确认出库')
         .wait())
        return self

    @reset_after_execution
    @doc(s_sell_after_sale_refusal_return)
    def sell_after_sale_refusal_return(self):
        self.menu_manage()
        (self.step(key='update_the_aftermarket_selection', desc='单选')
         .step(key='generate_purchase_order', desc='更新售后状态')
         .step(key='refusal_return', desc='拒退退回')
         .step(key='refund_verify', desc='去出库')
         .step(key='tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='express_amount', value='11', action='input', desc='物流费用')
         .step(key='verify_out', desc='确认出库')
         .wait())
        return self

    @reset_after_execution
    @doc(s_sell_after_sale_repair)
    def sell_after_sale_repair(self):
        self.menu_manage()
        (self.step(key='update_the_aftermarket_selection', desc='单选')
         .step(key='generate_purchase_order', desc='更新售后状态')
         .step(key='repair', desc='返修')
         .step(key='refund_verify', desc='去出库')
         .step(key='tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='express_amount', value='14', action='input', desc='物流费用')
         .step(key='verify_out', desc='确认出库')
         .wait())
        return self
