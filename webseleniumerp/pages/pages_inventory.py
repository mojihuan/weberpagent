# coding: utf-8
import os
from common.base_page import BasePage, ImportDataEdit, reset_after_execution
from common.base_params import InitializeParams
from common.import_desc import *
from config.settings import DATA_PATHS
from config.user_info import INFO


class CommonPages(BasePage, InitializeParams):

    def __init__(self, driver):
        super().__init__(driver)
        self._steps_queue = []
        self.file = ImportDataEdit(driver)
        self.file_paths = self.file.file_paths = {
            'inventory_scan_code_transfer': os.path.join(DATA_PATHS['excel'], 'inventory_scan_code_transfer_import.xlsx'),
            'inventory_item_sign_in_enter_warehouse': os.path.join(DATA_PATHS['excel'], 'inventory_item_sign_in_enter_warehouse_import.xlsx'),
            'purchase_post_sale_out_warehouse': os.path.join(DATA_PATHS['excel'], 'purchase_post_sale_out_warehouse_import.xlsx'),
            'sell_sales_outbound': os.path.join(DATA_PATHS['excel'], 'sell_sales_outbound_import.xlsx'),
            'sell_pre_sale_only_outbound': os.path.join(DATA_PATHS['excel'], 'sell_pre_sale_only_outbound_import.xlsx'),
            'send_repair_out_warehouse': os.path.join(DATA_PATHS['excel'], 'send_repair_out_warehouse_import.xlsx'),
            'inventory_warehouse_allocation_menu': os.path.join(DATA_PATHS['excel'], 'inventory_warehouse_allocation_menu_import.xlsx'),
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


class InventoryAddressManagePages(CommonPages):
    """库存管理|出库管理|地址管理"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='inventory_manage_menu', desc='库存管理')
         .step(key='inventory_outbound_manage_menu', desc='出库管理')
         .step(key='inventory_address_manage_menu', desc='地址管理')
         .wait())
        return self

    @reset_after_execution
    @doc(i_add_address)
    def add_address(self):
        self.menu_manage()
        (self.step(key='new_address', desc='新增')
         .step(key='business_type', desc='业务类型')
         .custom(lambda: self.down_arrow_return())
         .step(key='name', value='杰克' + self.serial, action='input', desc='姓名')
         .step(key='phone', value=self.phone, action='input', desc='手机号')
         .step(key='district', desc='所在地区')
         .step(key='province', desc='省')
         .step(key='city', desc='市')
         .step(key='area', desc='区')
         .step(key='address', value='和平路' + self.number + '号', action='input', desc='详细地址')
         .step(key='coordinate', value=INFO['coordinate'], action='input', desc='坐标')
         .step(key='new_address_ok', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(i_edit_address)
    def edit_address(self):
        self.menu_manage()
        (self.step(key='edit_address', desc='编辑')
         .step(key='name', value='杰克' + self.number, action='input', desc='姓名')
         .step(key='phone', value='13627638472', action='input', desc='手机号')
         .step(key='address', value='和平路' + self.serial + '号', action='input', desc='详细地址')
         .step(key='new_address_ok', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(i_delete_address)
    def delete_address(self):
        self.menu_manage()
        (self.scroll('delete_address', desc='删除')
         .step(key='delete_address', desc='删除')
         .step(key='delete_address_ok', desc='确定')
         .wait())
        return self


class InventoryHandOverGoodsPages(CommonPages):
    """库存管理|移交接收管理|移交物品"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='inventory_manage_menu', desc='库存管理')
         .step(key='inventory_handover_reception_manage_menu', desc='移交接收管理')
         .step(key='inventory_transfer_items_menu', desc='移交物品')
         .wait())
        return self

    @reset_after_execution
    @doc(i_hand_over_goods)
    def hand_over_goods(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=2)[0]['imei'])
        (self.step(key='number_imei', desc='物品输入框')
         .custom(self.affix_carriage_return)
         .step(key='be_put_in_storage', desc='移交按钮')
         .step(key='inventory', desc='移交库存')
         .step(key='receiver', desc='接收人')
         .custom(lambda: self.down_arrow_return(3))
         .step(key='repair_instructions', value=self.serial, action='input', desc='移交说明')
         .step(key='handover_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(i_import_hand_over_goods)
    def import_hand_over_goods(self):
        self.menu_manage()
        self.file.get_inventory_data('inventory_scan_code_transfer', 'imei', i=2, j=3)
        (self.step(key='import_items', desc='导入物品')
         .step(key='handover_import', value=self.file_path('inventory_scan_code_transfer'), action='upload', desc='导入文件')
         .step(key='handover_import_ok', desc='确定')
         .custom(lambda: self.wait_time())
         .step(key='search', desc='搜索')
         .custom(lambda: self.tab_return(5))
         .step(key='be_put_in_storage', desc='移交按钮')
         .step(key='inventory', desc='移交库存')
         .step(key='receiver', desc='接收人')
         .custom(lambda: self.down_arrow_return(3))
         .step(key='repair_instructions', value=self.serial, action='input', desc='移交说明')
         .step(key='handover_confirmation', desc='确认')
         .wait())
        return self


class InventoryItemSignWarehousingPages(CommonPages):
    """库存管理|入库管理|物品签收入库"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='inventory_manage_menu', desc='库存管理')
         .step(key='inventory_inbound_manage_menu', desc='入库管理')
         .step(key='inventory_item_sign_in_enter_warehouse_menu', desc='物品签收入库')
         .wait())
        return self

    @reset_after_execution
    @doc(i_sign_for_receipt)
    def sign_for_receipt(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=1)[0]['imei'])
        (self.step(key='please_enter_the_item_number_ipt', desc='物品输入框')
         .custom(lambda: self.affix())
         .step(key='check_in_library_search', desc='搜索')
         .custom(lambda: self.wait_time())
         .step(key='sign_for_receipt', desc='签收入库')
         .step(key='circulation_warehouse', desc='流转仓库')
         .custom(lambda: self.up_arrow_return())
         .step(key='the_signature_is_confirmed_in_the_database', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(i_import_sign_for_receipt)
    def import_sign_for_receipt(self):
        self.menu_manage()
        self.file.get_inventory_data('inventory_item_sign_in_enter_warehouse', 'imei', i=1)
        (self.step(key='import_items_into_storage', desc='导入入库物品')
         .step(key='handover_import', value=self.file_path('inventory_item_sign_in_enter_warehouse'), action='upload', desc='上传文件')
         .step(key='import_confirmation', desc='确定')
         .step(key='check_in_library_search', desc='搜索')
         .custom(lambda: self.tab_return(6))
         .step(key='sign_for_receipt', desc='签收入库')
         .step(key='circulation_warehouse', desc='流转仓库')
         .custom(lambda: self.up_arrow_return())
         .step(key='the_signature_is_confirmed_in_the_database', desc='确定')
         .wait())
        return self


class InventoryListPages(CommonPages):
    """库存管理|库存列表"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='inventory_manage_menu', desc='库存管理')
         .step(key='inventory_list_menu', desc='库存列表')
         .wait())
        return self

    @reset_after_execution
    @doc(i_sale_out_of_warehouse_has)
    def sale_out_of_warehouse_has(self):
        self.menu_manage()
        (self.step(key='item_number_btn', desc='物品编号')
         .step(key='sales_information', desc='销售信息')
         .step(key='sales_out_of_the_warehouse', desc='销售出库')
         .step(key='please_select_sales_customer', desc='销售客户')
         .custom(lambda: self.down_arrow_return())
         .step(key='money_not_received', desc='已收款')
         .step(key='please_select_the_receiving_account', desc='收款账户')
         .custom(lambda: self.down_arrow_return())
         .step(key='tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='express_amount', value='11', action='input', desc='物流费用')
         .step(key='selling_price_ipt', value='23', action='input', desc='销售价')
         .step(key='platform_item_number_btn_sales', value=self.serial, action='input', desc='平台物品编号销售')
         .step(key='platform_sales_order_number', value=self.serial, action='input', desc='平台销售单号')
         .step(key='sales_outbound_is_confirmed', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(i_return_after_sale_has)
    def return_after_sale_has(self):
        self.menu_manage()
        (self.step(key='select_the_item_status', desc='物品状态')
         .custom(lambda: self.down_arrow_return(9))
         .step(key='inventory_status', desc='库存状态')
         .custom(lambda: self.up_arrow_return())
         .step(key='inventory_search', desc='搜索')
         .step(key='item_number_btn', desc='物品编号')
         .step(key='sales_information', desc='销售信息')
         .step(key='sales_after_sales_btn', desc='销售售后')
         .step(key='sell_return', desc='退货')
         .step(key='mail', desc='邮寄')
         .step(key='received_btn', desc='已收货')
         .step(key='circulation_warehouse', desc='流转仓库')
         .custom(lambda: self.down_arrow_return())
         .step(key='please_enter_remark', value=self.serial, action='input', desc='备注')
         .step(key='sales_after_sales_confirmed', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(i_return_only_parts_has)
    def return_only_parts_has(self):
        self.menu_manage()
        (self.step(key='select_the_item_status', desc='物品状态')
         .custom(lambda: self.down_arrow_return(9))
         .step(key='inventory_status', desc='库存状态')
         .custom(lambda: self.up_arrow_return())
         .step(key='inventory_search', desc='搜索')
         .step(key='item_number_btn', desc='物品编号')
         .step(key='sales_information', desc='销售信息')
         .step(key='sales_after_sales_btn', desc='销售售后')
         .step(key='returns_only', desc='仅退配件')
         .step(key='new_sales_price', value='10', action='input', desc='新销售结算价')
         .step(key='sort', desc='配件分类')
         .custom(lambda: self.up_arrow_return())
         .step(key='accessories_name', desc='配件名称')
         .custom(lambda: self.down_arrow_return(3))
         .step(key='please_select_the_brand', desc='品牌')
         .custom(lambda: self.down_arrow_return(3))
         .step(key='model', desc='型号')
         .custom(lambda: self.down_arrow_return(3))
         .step(key='accessories_channel', desc='配件渠道')
         .custom(lambda: self.down_arrow_return())
         .step(key='accessory_value', value='10', action='input', desc='配件价值')
         .step(key='received_button', desc='已收货')
         .step(key='circulation_warehouse', desc='流转仓库')
         .custom(lambda: self.down_arrow_return())
         .step(key='please_enter_remark', value=self.serial, action='input', desc='备注')
         .scroll('sales_after_sales_confirmed', desc='确定')
         .step(key='sales_after_sales_confirmed', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(i_price_adjustment_after_sales)
    def price_adjustment_after_sales(self):
        self.menu_manage()
        (self.step(key='select_the_item_status', desc='物品状态')
         .custom(lambda: self.down_arrow_return(9))
         .step(key='inventory_status', desc='库存状态')
         .custom(lambda: self.up_arrow_return())
         .step(key='inventory_search', desc='搜索')
         .step(key='item_number_btn', desc='物品编号')
         .step(key='sales_information', desc='销售信息')
         .step(key='sales_after_sales_btn', desc='销售售后')
         .step(key='price_adjustments', desc='调价')
         .step(key='new_sales_price', value='5', action='input', desc='新销售结算价')
         .step(key='please_enter_remark', value=self.serial, action='input', desc='备注')
         .step(key='sales_after_sales_confirmed', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(i_refund_only_after_purchase)
    def refund_only_after_purchase(self):
        self.menu_manage()
        (self.step(key='inventory_status', desc='库存状态')
         .custom(lambda: self.down_arrow_return())
         .step(key='inventory_search', desc='搜索')
         .step(key='item_number_btn', desc='物品编号')
         .step(key='procurement_info', desc='采购信息')
         .step(key='procurement_after_sales_2', desc='采购售后')
         .step(key='remark_input', value=self.serial, action='input', desc='备注')
         .step(key='only_refunds_are_confirmed', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(i_item_info_edit)
    def item_info_edit(self):
        self.menu_manage()
        (self.step(key='item_number_btn', desc='物品编号')
         .custom(lambda: self.wait_time(3))
         .step(key='modify_inventory_information', desc='编辑')
         .step(key='please_select_the_brand', desc='品牌')
         .custom(lambda: self.down_arrow_return())
         .step(key='model', desc='型号')
         .custom(lambda: self.down_arrow_return())
         .step(key='quality', desc='成色')
         .custom(lambda: self.down_arrow_return())
         .step(key='item_info_edit_ok', desc='确定')
         .wait())
        return self


class InventoryNewItemPages(CommonPages):
    """库存管理|入库管理|物流签收入库"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='inventory_manage_menu', desc='库存管理')
         .step(key='inventory_inbound_manage_menu', desc='入库管理')
         .step(key='inventory_logistics_list_menu', desc='物流列表')
         .wait())
        return self

    @reset_after_execution
    @doc(i_logistics_signature_for_receipt)
    def logistics_signature_for_receipt(self):
        self.menu_manage()
        (self.scroll('package_details', desc='包裹详情')
         .step(key='package_details', desc='包裹详情')
         .custom(lambda: self.wait_time())
         .step(key='inbound_search', desc='搜索')
         .custom(lambda: self.tab_return(6))
         .step(key='be_put_in_storage', desc='签收入库')
         .step(key='circulation_warehouse', desc='流转仓库')
         .custom(lambda: self.down_arrow_return())
         .step(key='submit_into_the_warehouse', desc='确定')
         .wait())
        return self


class InventoryOutboundOrdersListPages(CommonPages):
    """库存管理|出库管理|仅出库订单列表"""

    def menu_manage(self):
        """菜单"""
        (self.scroll(key='inventory_manage_menu', desc='库存管理')
         .step(key='inventory_manage_menu', desc='库存管理')
         .step(key='inventory_outbound_manage_menu', desc='出库管理')
         .step(key='inventory_only_list_of_outbound_orders_menu', desc='仅出库订单列表')
         .wait())
        return self

    @reset_after_execution
    @doc(i_return_outgoing_items_warehousing)
    def return_outgoing_items_warehousing(self):
        self.menu_manage()
        (self.step(key='search', desc='搜索')
         .custom(lambda: self.tab_return(8))
         .step(key='return_outgoing_items', desc='出库物品退回')
         .step(key='tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='select_the_warehouse_c', desc='流转仓库')
         .custom(lambda: self.up_arrow_return())
         .step(key='remark', value=self.serial, action='input', desc='备注')
         .step(key='outbound_return_confirmation', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(i_outbound_sales_only_received)
    def outbound_sales_only_received(self):
        self.menu_manage()
        (self.step(key='search', desc='搜索')
         .custom(lambda: self.tab_return(8))
         .step(key='outbound_sales_only', desc='仅出库销售')
         .step(key='money_not_received_btn', desc='已收款')
         .step(key='collection_account_btn', desc='收款账户')
         .custom(lambda: self.up_arrow_return())
         .step(key='selling_price_ipt', value='34', action='input', desc='销售价')
         .step(key='sales_order_number', value=self.serial, action='input', desc='平台销售订单号')
         .step(key='only_outbound_sales_are_determined', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(i_create_an_outbound_only_order)
    def create_an_outbound_only_order(self):
        self.copy(self.pc.inventory_list_data(i=2)[0]['imei'])
        self.menu_manage()
        (self.step(key='create_a_new_order', desc='新建订单')
         .step(key='customer_btn', desc='销售客户')
         .custom(lambda: self.down_arrow_return(2))
         .step(key='remarks', value='出库备注', action='input', desc='备注')
         .step(key='tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='express_amount', value='13', action='input', desc='物流费用')
         .step(key='item_ipt', desc='物品编号输入框')
         .custom(lambda: self.affix())
         .step(key='sell_item_add', desc='添加')
         .scroll(key='only_outbound_notes', desc='备注')
         .step(key='only_outbound_notes', value='物品备注', action='input', desc='备注')
         .step(key='only_outbound_new_orders_are_confirmed', desc='确定')
         .wait())
        return self


class InventoryPurchaseAndSellOutPages(CommonPages):
    """库存管理|出库管理|采购售后出库"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='inventory_manage_menu', desc='库存管理')
         .step(key='inventory_outbound_manage_menu', desc='出库管理')
         .step(key='inventory_purchase_post_sale_out_warehouse_menu', desc='采购售后出库')
         .wait())
        return self

    @reset_after_execution
    @doc(i_purchase_after_sales_warehouse)
    def purchase_after_sales_warehouse(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=2)[0]['imei'])
        (self.step(key='tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='express_charge', value='15', action='input', desc='物流费用')
         .step(key='number_imei', desc='物品框输入框')
         .custom(lambda: self.affix())
         .step(key='add_items_after_the_sale', desc='添加')
         .step(key='after_sales_reason', value=self.serial, action='input', desc='售后原因')
         .step(key='confirmed_delivery', desc='确认出库')
         .wait())
        return self

    @reset_after_execution
    @doc(i_import_purchase_and_sell_out)
    def import_purchase_and_sell_out(self):
        self.menu_manage()
        self.file.get_inventory_data('purchase_post_sale_out_warehouse', 'imei', i=2, j=10)
        (self.step(key='tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='express_charge', value='15', action='input', desc='物流费用')
         .step(key='imei_import', desc='IMEI导入')
         .step(key='handover_import', value=self.file_path('purchase_post_sale_out_warehouse'), action='upload', desc='上传文件')
         .step(key='purchasing_after_sales_ok', desc='确定')
         .step(key='after_sales_reason', value=self.serial, action='input', desc='售后原因')
         .step(key='confirmed_delivery', desc='确认出库')
         .wait())
        return self


class InventoryReceiveItemPages(CommonPages):
    """库存管理|移交接收管理|接收物品"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='inventory_manage_menu', desc='库存管理')
         .step(key='inventory_handover_reception_manage_menu', desc='移交接收管理')
         .step(key='inventory_receive_items_menu', desc='接收物品')
         .wait())
        return self

    @reset_after_execution
    @doc(i_item_acceptance_repair_status)
    def item_acceptance_repair_status(self):
        self.menu_manage()
        (self.step(key='select_the_item_status', desc='请选择物品状态')
         .step(key='select_the_item_status', value='待维修', action='input', desc='物品状态')
         .custom(lambda: self.down_arrow_return())
         .step(key='search', desc='搜索')
         .custom(lambda: self.tab_return(5))
         .step(key='receive_button', desc='接收')
         .step(key='cancel_the_sale_confirmation', desc='确定')
         .wait())
        return self


class InventorySaleOutWarehousePages(CommonPages):
    """库存管理|出库管理|销售出库"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='inventory_manage_menu', desc='库存管理')
         .step(key='inventory_outbound_manage_menu', desc='出库管理')
         .step(key='inventory_sales_outbound_menu', desc='销售出库')
         .wait())
        return self

    @reset_after_execution
    @doc(i_sales_out_warehouse_received)
    def sales_out_warehouse_received(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=2, j=13)[0]['imei'])

        res = self.pc.inventory_list_data(i=2, j=13)
        imei = self.copy(res[0]['imei'])
        (self.step(key='sale_client', desc='销售客户')
         .custom(lambda: self.up_arrow_return())
         .step(key='tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='express_amount', value='21', action='input', desc='物流费用')
         .step(key='sell_outbound_items', desc='物品输入框')
         .custom(lambda: self.affix())
         .step(key='sell_outbound_items_add', desc='添加')
         .scroll('platform_number', desc='平台物品编号')
         .step(key='sell_sales_amount_ipt', value='15', action='input', desc='销售金额')
         .step(key='platform_number', value=self.serial, action='input', desc='平台物品编号')
         .step(key='sell_sales_order_number', value=self.serial, action='input', desc='平台销售订单号')
         .scroll('the_amount_of_the_payout', desc='收款金额')
         .step(key='money_received', desc='已收款')
         .step(key='send_payment_account', desc='收款账户')
         .custom(lambda: self.up_arrow_return())
         .step(key='the_amount_of_the_payout', value='5', action='input', desc='收款金额')
         .step(key='sales_outbound_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(i_sell_outbound_accessories)
    def sell_outbound_accessories(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=2, j=13)[0]['imei'])
        (self.step(key='sale_client', desc='销售客户')
         .custom(lambda: self.up_arrow_return())
         .step(key='tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='express_amount', value='27', action='input', desc='物流费用')
         .step(key='sell_outbound_items', desc='物品输入框')
         .custom(lambda: self.affix())
         .step(key='sell_outbound_items_add', desc='添加')
         .scroll('platform_number', desc='平台物品编号')
         .step(key='sell_sales_amount_ipt', value='25', action='input', desc='销售金额')
         .step(key='platform_number', value=self.serial, action='input', desc='平台物品编号')
         .step(key='sell_sales_order_number', value=self.serial, action='input', desc='平台销售订单号')
         .scroll('money_not_received', desc='未收款')
         .step(key='money_not_received', desc='未收款')
         .step(key='add_manually', desc='手动添加')
         .step(key='reset_data', desc='重置')
         .custom(lambda: self.tab_return(2))
         .scroll(key='add_ok_manually', desc='确定')
         .step(key='add_ok_manually', desc='确定')
         .step(key='sales_outbound_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(i_import_sell_get_out)
    def import_sell_get_out(self):
        self.menu_manage()
        self.file.get_inventory_data('sell_sales_outbound', 'imei', i=2)
        (self.step(key='sale_client', desc='销售客户')
         .custom(lambda: self.up_arrow_return())
         .step(key='tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='express_amount', value='42', action='input', desc='物流费用')
         .step(key='import_add', desc='导入添加')
         .step(key='import_the_template', desc='导入模版')
         .custom(lambda: self.up_arrow_return())
         .step(key='handover_import', value=self.file_path('sell_sales_outbound'), action='upload', desc='上传文件')
         .step(key='import_ok', desc='确定')
         .scroll('platform_number')
         .step(key='sell_sales_amount_ipt', value='25.6', action='input', desc='销售金额')
         .step(key='platform_number', value=self.serial, action='input', desc='平台物品编号')
         .step(key='sell_sales_order_number', value=self.serial, action='input', desc='平台销售订单号')
         .scroll('the_amount_of_the_payout')
         .step(key='money_not_received', desc='未收款')
         .step(key='sales_outbound_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(i_sell_distribution)
    def sell_distribution(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=2, j=13)[0]['imei'])
        (self.step(key='distribution_warehouse', desc='铺货预售出库')
         .step(key='sale_client', desc='销售客户')
         .custom(lambda: self.up_arrow_return())
         .step(key='received_button', desc='铺货')
         .step(key='received_the_payment', desc='已收款')
         .step(key='collection_account_btn', desc='收款账户')
         .custom(lambda: self.up_arrow_return())
         .step(key='tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='express_amount', value='3', action='input', desc='物流费用')
         .step(key='sell_outbound_items', desc='物品输入框')
         .custom(lambda: self.affix())
         .step(key='sell_outbound_items_add', desc='添加')
         .scroll(key='sell_sales_amount_input',desc='销售金额')
         .step(key='sell_sales_amount_input', value='235', action='input', desc='销售金额')
         .step(key='sales_outbound_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(i_import_sell_distribution)
    def import_sell_distribution(self):
        self.menu_manage()
        self.file.get_inventory_data('sell_pre_sale_only_outbound', 'imei', i=2)
        (self.step(key='distribution_warehouse', desc='铺货预售出库')
         .step(key='sale_client', desc='销售客户')
         .custom(lambda: self.up_arrow_return())
         .step(key='received_button', desc='铺货')
         .step(key='received_the_payment', desc='已收款')
         .step(key='collection_account_btn', desc='收款账户')
         .custom(lambda: self.up_arrow_return())
         .step(key='tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='import_add', desc='导入添加')
         .step(key='handover_import', value=self.file_path('sell_pre_sale_only_outbound'), action='upload', desc='上传文件')
         .step(key='import_ok', desc='确定')
         .scroll(key='sell_sales_amount_input',desc='销售金额')
         .step(key='sell_sales_amount_input', value='115', action='input', desc='销售金额')
         .step(key='sales_outbound_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(i_sell_advance_sale)
    def sell_advance_sale(self):
        self.menu_manage()
        self.file.get_inventory_data('excel', 'imei', i=2, j=13)
        (self.step(key='distribution_warehouse', desc='铺货预售出库')
         .step(key='sale_client', desc='销售客户')
         .custom(lambda: self.up_arrow_return())
         .step(key='sale_predict', desc='预售')
         .step(key='tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='express_amount', value='32', action='input', desc='物流费用')
         .step(key='sell_outbound_items', desc='物品输入框')
         .custom(lambda: self.affix())
         .step(key='sell_outbound_items_add', desc='添加')
         .step(key='sales_outbound_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(i_import_sell_advance_sale)
    def import_sell_advance_sale(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=2, j=13)[0]['imei'])
        (self.step(key='distribution_warehouse', desc='铺货预售出库')
         .step(key='sale_client', desc='销售客户')
         .custom(lambda: self.up_arrow_return())
         .step(key='sale_predict', desc='预售')
         .step(key='tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='express_amount', value='53', action='input', desc='物流费用')
         .step(key='import_add', desc='导入')
         .step(key='handover_import', value=self.file_path('inventory_item_sign_in_enter_warehouse'), action='upload', desc='上传文件')
         .step(key='import_ok', desc='确定')
         .step(key='sales_outbound_confirmation', desc='确认')
         .wait())
        return self


class InventorySellAfterSaleDeliveryPages(CommonPages):
    """库存管理|出库管理|销售售后出库"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='inventory_manage_menu', desc='库存管理')
         .step(key='inventory_outbound_manage_menu', desc='出库管理')
         .step(key='inventory_sales_after_sales_delivery_menu', desc='销售售后出库')
         .wait())
        return self

    @reset_after_execution
    @doc(i_sell_get_out)
    def sell_get_out(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=2, j=15)[0]['articlesNo'])
        (self.step(key='tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='express_amount', value='24', action='input', desc='物流费用')
         .step(key='after_sale_item_input', desc='售后退回物品输入框')
         .custom(lambda: self.affix())
         .step(key='after_sale_add', desc='添加')
         .scroll('barter_remark', desc='平台销售订单号')
         .step(key='platform_order_number', value=self.serial, action='input', desc='平台销售订单号')
         .step(key='barter_remark', value=self.serial, action='input', desc='备注')
         .wait())
        self.copy(self.pc.inventory_list_data(i=2, j=3)[0]['articlesNo'])
        (self.step(key='barter_item_input', desc='换货出库物品输入框')
         .custom(lambda: self.affix())
         .step(key='barter_add', desc='添加')
         .scroll(key='barter_remark_info', desc='备注信息')
         .step(key='selling_price', value='121', action='input', desc='销售结算价')
         .step(key='platform_order_number_ipt', value=self.serial, action='input', desc='平台销售订单号')
         .step(key='barter_remark_info', value=self.serial, action='input', desc='备注信息')
         .step(key='verify_out', desc='确认出库')
         .wait())
        return self

    @reset_after_execution
    @doc(i_sell_after_sale_refusal_return)
    def sell_after_sale_refusal_return(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(j=15)[0]['articlesNo'])
        (self.step(key='please_select_the_after_sales_type', desc='售后类型')
         .custom(lambda: self.up_arrow_return(2))
         .step(key='tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='express_amount', value='72', action='input', desc='物流费用')
         .step(key='number_imei', desc='物品输入框')
         .custom(lambda: self.affix())
         .step(key='start_counting', desc='添加')
         .scroll('reject_the_note')
         .step(key='reject_the_note', value=self.serial, action='input', desc='备注信息')
         .step(key='verify_out', desc='确认出库')
         .wait())
        return self

    @reset_after_execution
    @doc(i_sell_after_sale_repair)
    def sell_after_sale_repair(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(j=15)[0]['articlesNo'])
        (self.step(key='please_select_the_after_sales_type', desc='售后类型')
         .custom(lambda: self.up_arrow_return())
         .step(key='tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='express_amount', value='25', action='input', desc='物流费用')
         .step(key='number_imei', desc='物品输入框')
         .custom(lambda: self.affix())
         .step(key='start_counting', desc='添加')
         .scroll('reject_the_note')
         .step(key='reject_the_note', value=self.serial, action='input', desc='备注信息')
         .step(key='verify_out', desc='确认出库')
         .wait())
        return self


class InventorySendOutRepairPages(CommonPages):
    """库存管理|出库管理|送修出库"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='inventory_manage_menu', desc='库存管理')
         .step(key='inventory_outbound_manage_menu', desc='出库管理')
         .step(key='inventory_send_repair_outbound_menu', desc='送修出库')
         .wait())
        return self

    @reset_after_execution
    @doc(i_send_out_the_warehouse)
    def send_out_the_warehouse(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=2)[0]['articlesNo'])
        (self.step(key='supplier', desc='供应商')
         .custom(lambda: self.up_arrow_return())
         .step(key='material_flow', value=self.jd, action='input', desc='物流单号')
         .step(key='expense', value='12', action='input', desc='物流费用')
         .step(key='number_imei', desc='点击物品输入框')
         .custom(lambda: self.affix())
         .step(key='send_add_item', desc='点击添加')
         .step(key='reason', value=self.serial, action='input', desc='送修原因')
         .step(key='confirmed_delivery', desc='点击确认出库')
         .wait())
        return self

    @reset_after_execution
    @doc(i_import_send_out_for_repair)
    def import_send_out_for_repair(self):
        self.menu_manage()
        self.file.get_inventory_data('send_repair_out_warehouse', 'imei', i=2)
        (self.step(key='please_select_a_supplier_s', desc='供应商')
         .custom(lambda: self.up_arrow_return())
         .step(key='material_flow', value=self.jd, action='input', desc='物流单号')
         .step(key='expense', value='40', action='input', desc='物流费用')
         .step(key='imei_import', desc='IMEI导入')
         .step(key='handover_import', value=self.file_path('excel'), action='upload', desc='上传文件')
         .step(key='the_introduction_of_repair_is_determined', desc='确定')
         .step(key='reason', value=self.serial, action='input', desc='送修原因')
         .step(key='generate_help_orders', desc='确认出库')
         .wait())
        return self


class InventoryStockCountPages(CommonPages):
    """库存管理|库存盘点"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='inventory_manage_menu', desc='库存管理')
         .step(key='inventory_inventory_count_menu', desc='库存盘点')
         .wait())
        return self

    @reset_after_execution
    @doc(i_completed_inventory_count)
    def completed_inventory_count(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=2)[0]['articlesNo'])
        (self.step(key='new_count', desc='新建盘点')
         .step(key='ownership', desc='盘点物品所属人')
         .custom(lambda: self.up_arrow_return())
         .step(key='review_confirmation', desc='确认')
         .step(key='remark', value=self.serial, action='input', desc='备注')
         .step(key='start_counting', desc='开始盘点')
         .step(key='add_goods_input', desc='物品输入框')
         .custom(lambda: self.affix_carriage_return())
         .step(key='submit_inventory', desc='提交盘点')
         .step(key='complete_inventory', desc='完成盘点')
         .step(key='inventory_count_determined', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(i_delete_count)
    def delete_count(self):
        self.menu_manage()
        (self.step(key='delete_count', desc='删除')
         .step(key='inventory_count_determined', desc='确定')
         .wait())
        return self


class InventoryStoreTransferPages(CommonPages):
    """库存管理-库存调拨"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='inventory_manage_menu', desc='库存管理')
         .step(key='inventory_warehouse_allocation_menu', desc='库存调拨')
         .wait())
        return self

    @reset_after_execution
    @doc(i_new_allocation)
    def new_allocation(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=2)[0]['articlesNo'])
        (self.step(key='new_allocation', desc='新增调拨')
         .step(key='select_call_out_of_the_repository', desc='调出仓库')
         .custom(lambda: self.down_arrow_return())
         .step(key='select_transfer_to_repository', desc='调入仓库')
         .custom(lambda: self.down_arrow_return(2))
         .step(key='remarks', value=self.serial, action='input', desc='备注')
         .step(key='tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='item_imei_input', desc='物品输入框')
         .custom(lambda: self.affix())
         .step(key='add_allocation_item', desc='添加')
         .step(key='warehouse_allocation_ok', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(i_import_new_allot)
    def import_new_allot(self):
        self.menu_manage()
        self.file.get_inventory_data('inventory_warehouse_allocation_menu', 'articles_no', i=2)
        (self.step(key='new_allocation', desc='新增调拨')
         .step(key='select_call_out_of_the_repository', desc='调出仓库')
         .custom(lambda: self.down_arrow_return())
         .step(key='select_transfer_to_repository', desc='调入仓库')
         .custom(lambda: self.down_arrow_return(2))
         .step(key='remarks', value=self.serial, action='input', desc='备注')
         .step(key='tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='import', desc='导入')
         .step(key='handover_import', value=self.file_path('excel'), action='upload', desc='上传文件')
         .step(key='transfer_upload_ok', desc='确定')
         .step(key='warehouse_allocation_ok', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(i_select_add_item_transfer)
    def select_add_item_transfer(self):
        self.menu_manage()
        (self.step(key='new_allocation', desc='新增调拨')
         .step(key='select_call_out_of_the_repository', desc='调出仓库')
         .custom(lambda: self.down_arrow_return())
         .step(key='select_transfer_to_repository', desc='调入仓库')
         .custom(lambda: self.down_arrow_return(2))
         .step(key='remarks', value=self.serial, action='input', desc='备注')
         .step(key='tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='select_add_btn', desc='选择添加')
         .step(key='reset_item_data', desc='重置')
         .custom(lambda: self.tab_return(2))
         .scroll(key='item_ok', desc='确定')
         .step(key='item_ok', desc='确定')
         .step(key='warehouse_allocation_ok', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(i_receive)
    def receive(self):
        self.menu_manage()
        (self.step(key='allocation_receive', desc='接收')
         .custom(lambda: self.wait_time())
         .step(key='quick_actions', desc='快捷操作')
         .custom(lambda: self.down_arrow_return())
         .step(key='allocation_receive_ok', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(i_cancel)
    def cancel(self):
        self.menu_manage()
        (self.step(key='cancel', desc='撤销')
         .custom(lambda: self.wait_time())
         .step(key='revoke_the_determination', desc='确定')
         .wait())
        return self
