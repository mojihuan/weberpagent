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
            'new_purchase_order': os.path.join(DATA_PATHS['excel'], 'purchase_new_order_import.xlsx'),
            'logistics_delivery': os.path.join(DATA_PATHS['excel'], 'purchase_logistics_delivery_import.xlsx'),
            'purchase_new_order_zz': os.path.join(DATA_PATHS['excel'], 'purchase_new_order_zz_import.xlsx'),
            'img': os.path.join(DATA_PATHS['excel'], 'img.jpg')
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


class PurchaseAddPages(CommonPages):
    """商品采购|采购管理|新增采购单"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='purchase_commodity_procurement_menu', desc='商品采购')
         .step(key='purchase_manage_menu', desc='采购管理')
         .step(key='purchase_new_order_menu', desc='新增采购单')
         .wait())
        return self

    @reset_after_execution
    @doc(p_new_purchase_order_unpaid_journey)
    def new_purchase_order_unpaid_journey(self):
        self.menu_manage()
        (self.step(key='procurement_supplier', desc='采购供应商')
         .custom(lambda: self.down_arrow_return())
         .step(key='purchasing_staff', desc='采购人')
         .custom(lambda: self.down_arrow_return())
         .step(key='procurement_account', desc='采购账号')
         .custom(lambda: self.up_arrow_return())
         .step(key='please_select_the_status_of_your_package', desc='包裹状态')
         .custom(lambda: self.up_arrow_return(2))
         .step(key='express_delivery', value=self.sf, action='input', desc='物流单号')
         .step(key='express_amount', value='12', action='input', desc='物流费用')
         .step(key='remark', value=self.serial, action='input', desc='备注')
         .step(key='new_button', desc='新增')
         .step(key='ok_button', desc='确定')
         .step(key='auto_imei', desc='自动生成IMEI')
         .step(key='description', value=self.serial, action='input', desc='物品描述')
         .step(key='batch_amount', value='115', action='input', desc='金额')
         .step(key='please_enter_the_platform_item_number', value=self.serial, action='input', desc='平台物品编号')
         .step(key='serial_number', value=self.serial, action='input', desc='序列号')
         .step(key='order_number', value=self.serial, action='input', desc='平台订单号')
         .step(key='firm_commit', desc='确定')
         .step(key='payment_status_unpaid', desc='未付款')
         .step(key='generate_purchase_order', desc='确定生成采购单')
         .wait())
        return self

    @reset_after_execution
    @doc(p_create_batch_order)
    def create_batch_order(self):
        self.menu_manage()
        (self.step(key='procurement_supplier', desc='采购供应商')
         .custom(lambda: self.down_arrow_return())
         .step(key='purchasing_staff', desc='采购人')
         .custom(lambda: self.down_arrow_return())
         .step(key='procurement_account', desc='采购账号')
         .custom(lambda: self.up_arrow_return())
         .step(key='please_select_the_status_of_your_package', desc='包裹状态')
         .custom(lambda: self.up_arrow_return())
         .step(key='select_circulation_warehouse', desc='流转仓库')
         .custom(lambda: self.down_arrow_return())
         .step(key='express_delivery', value=self.sf, action='input', desc='物流单号')
         .step(key='express_amount', value=2, action='input', desc='物流费用')
         .step(key='remark', value='采购商品备注', action='input', desc='备注')
         .step(key='new_button', desc='新增')
         .step(key='ok_button', desc='确定')
         .step(key='batch_entry', desc='批量无串号录入')
         .step(key='enter_quantity', value='5', action='input', desc='数量')
         .step(key='batch_amount', value='5', action='input', desc='金额')
         .step(key='firm_commit', desc='确定')
         .scroll('payment_account', desc='付款账号')
         .step(key='payment_status_paid', desc='已付款')
         .step(key='send_payment_account', desc='付款账号')
         .custom(lambda: self.down_arrow_return())
         .step(key='payment_amount', value='10', action='input', desc='付款金额')
         .custom(lambda: self.carriage_return())
         .step(key='generate_purchase_order', desc='确定生成采购单')
         .step(key='stash_verify', desc='流转仓库确定')
         .wait())
        return self

    @reset_after_execution
    @doc(p_import_purchase_order)
    def import_purchase_order(self):
        self.menu_manage()
        (self.custom(lambda: self.update_and_modify_the_imei('new_purchase_order'))
         .step(key='purchase_to_lead_into', desc='导入')
         .step(key='import_model', desc='导入模板')
         .custom(lambda: self.wait_time())
         .custom(lambda: self.down_arrow_return(4))
         .step(key='handover_import', value=self.file_path('new_purchase_order'), action='upload', desc='上传文件')
         .step(key='to_lead_into_verify', desc='确定')
         .custom(lambda: self.wait_time())
         .step(key='again_confirm', desc='确定')
         .step(key='procurement_supplier', desc='采购供应商')
         .custom(lambda: self.down_arrow_return())
         .step(key='purchasing_staff', desc='采购人')
         .custom(lambda: self.down_arrow_return())
         .step(key='procurement_account', desc='采购账号')
         .custom(lambda: self.up_arrow_return())
         .step(key='please_select_the_status_of_your_package', desc='包裹状态')
         .custom(lambda: self.up_arrow_return())
         .step(key='select_circulation_warehouse', desc='流转仓库')
         .custom(lambda: self.down_arrow_return())
         .step(key='express_delivery', value=self.sf, action='input', desc='物流单号')
         .step(key='express_amount', value='2', action='input', desc='物流费用')
         .step(key='remark', value=self.serial, action='input', desc='备注')
         .step(key='payment_status_unpaid', desc='未付款')
         .step(key='generate_purchase_order', desc='确定生成采购单')
         .step(key='stash_verify', desc='流转仓库确定')
         .wait())
        return self

    @reset_after_execution
    @doc(p_transfer_import_create_a_purchase_order)
    def transfer_import_create_a_purchase_order(self):
        self.menu_manage()
        (self.custom(lambda: self.update_and_modify_the_imei('purchase_new_order_zz', column=10))
         .step(key='purchase_to_lead_into', desc='导入')
         .step(key='import_model', desc='导入模板')
         .custom(lambda: self.wait_time())
         .custom(lambda: self.down_arrow_return())
         .step(key='handover_import', value=self.file_path('purchase_new_order_zz'), action='upload', desc='上传文件')
         .step(key='to_lead_into_verify', desc='确定')
         .custom(lambda: self.wait_time())
         .step(key='again_confirm', desc='确定')
         .step(key='procurement_supplier', desc='采购供应商')
         .custom(lambda: self.down_arrow_return())
         .step(key='purchasing_staff', desc='采购人')
         .custom(lambda: self.down_arrow_return())
         .step(key='procurement_account', desc='采购账号')
         .custom(lambda: self.up_arrow_return())
         .step(key='please_select_the_status_of_your_package', desc='包裹状态')
         .custom(lambda: self.up_arrow_return())
         .step(key='select_circulation_warehouse', desc='流转仓库')
         .custom(lambda: self.down_arrow_return())
         .step(key='express_delivery', value=self.sf, action='input', desc='物流单号')
         .step(key='express_amount', value='2', action='input', desc='物流费用')
         .step(key='remark', value=self.serial, action='input', desc='备注')
         .step(key='payment_status_unpaid', desc='未付款')
         .step(key='generate_purchase_order', desc='确定生成采购单')
         .step(key='stash_verify', desc='流转仓库确定')
         .wait())
        return self

    @reset_after_execution
    @doc(p_import_and_adjust_price)
    def import_and_adjust_price(self):
        self.menu_manage()
        (self.custom(lambda: self.update_and_modify_the_imei('new_purchase_order'))
         .step(key='purchase_to_lead_into', desc='导入')
         .step(key='import_model', desc='导入模板')
         .custom(lambda: self.wait_time())
         .custom(lambda: self.down_arrow_return(4))
         .step(key='handover_import', value=self.file_path('new_purchase_order'), action='upload', desc='上传文件')
         .step(key='to_lead_into_verify', desc='确定')
         .custom(lambda: self.wait_time())
         .step(key='again_confirm', desc='确定')
         .step(key='batch_radio', desc='单选')
         .step(key='batch_adjust_price', desc='批量调价')
         .step(key='batch_purchase_amount', value='10', action='input', desc='批量采购金额')
         .step(key='adjust_price_verify', desc='确定')
         .step(key='procurement_supplier', desc='采购供应商')
         .custom(lambda: self.down_arrow_return())
         .step(key='procurement_account', desc='采购账号')
         .custom(lambda: self.up_arrow_return())
         .step(key='express_delivery', value=self.sf, action='input', desc='物流单号')
         .step(key='express_amount', value='11', action='input', desc='物流费用')
         .step(key='remark', value='采购商品备注', action='input', desc='备注')
         .step(key='payment_status_unpaid', desc='未付款')
         .step(key='generate_purchase_order', desc='确定生成采购单')
         .wait())
        return self

    @reset_after_execution
    @doc(p_create_and_transfer_order)
    def create_and_transfer_order(self):
        self.menu_manage()
        (self.step(key='procurement_supplier', desc='采购供应商')
         .custom(lambda: self.down_arrow_return())
         .step(key='procurement_account', desc='采购账号')
         .custom(lambda: self.down_arrow_return())
         .step(key='please_select_the_status_of_your_package', desc='包裹状态')
         .custom(lambda: self.up_arrow_return())
         .step(key='select_circulation_warehouse', desc='流转仓库')
         .custom(lambda: self.down_arrow_return())
         .step(key='express_delivery', value=self.sf, action='input', desc='物流单号')
         .step(key='express_amount', value=2, action='input', desc='物流费用')
         .step(key='remark', value=self.serial, action='input', desc='输入备注')
         .step(key='new_button', desc='新增')
         .step(key='ok_button', desc='确定')
         .step(key='auto_imei', desc='自动生成IMEI')
         .step(key='description', value=self.serial, action='input', desc='物品描述')
         .step(key='batch_amount', value='14', action='input', desc='金额')
         .step(key='please_enter_the_platform_item_number', value=self.serial, action='input', desc='平台物品编号')
         .step(key='serial_number', value=self.serial, action='input', desc='序列号')
         .step(key='order_number', value=self.serial, action='input', desc='平台订单号')
         .step(key='firm_commit', desc='确定')
         .scroll('payment_account', desc='付款账号')
         .step(key='payment_status_paid', desc='已付款')
         .step(key='send_payment_account', desc='付款账号')
         .custom(lambda: self.down_arrow_return())
         .step(key='payment_amount', value='1', action='input', desc='付款金额')
         .custom(lambda: self.carriage_return())
         .step(key='generate_purchase_order', desc='确定生成采购单')
         .step(key='quick_operation_btn', desc='快捷操作')
         .custom(lambda: self.down_arrow_return(2))
         .step(key='transfer', desc='移交')
         .step(key='hand_over_to_the_recipient', desc='接收人')
         .custom(lambda: self.down_arrow_return())
         .step(key='transfer_remarks_ipt', value='备注', action='input', desc='移交说明')
         .step(key='stash_verify', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(p_create_with_new_supplier)
    def create_with_new_supplier(self):
        self.menu_manage()
        (self.step(key='add_a_new_supplier', desc='点击+')
         .step(key='supplier_name', value='采购供应商' + self.serial, action='input', desc='输入供应商名称')
         .step(key='supplier_type', desc='供应商类型')
         .step(key='default_account', desc='财务账户')
         .custom(lambda: self.up_arrow_return())
         .step(key='default_payment_status', desc='付款状态')
         .step(key='contact_info', value=self.phone, action='input', desc='联系方式')
         .step(key='business_personnel', desc='业务人员')
         .custom(lambda: self.up_arrow_return())
         .step(key='select_province', desc='省')
         .custom(lambda: self.down_arrow_return())
         .step(key='select_city', desc='市')
         .custom(lambda: self.down_arrow_return())
         .step(key='area', desc='区')
         .custom(lambda: self.down_arrow_return())
         .step(key='detailed_address', value='广州市黄埔区生生广场' + self.number, action='input', desc='详细地址')
         .step(key='supplier_confirm', desc='确定')
         .step(key='procurement_supplier', desc='采购供应商')
         .custom(lambda: self.up_arrow_return())
         .step(key='procurement_account', desc='采购账号')
         .custom(lambda: self.down_arrow_return())
         .step(key='please_select_the_status_of_your_package', desc='包裹状态')
         .custom(lambda: self.up_arrow_return())
         .step(key='select_circulation_warehouse', desc='流转仓库')
         .custom(lambda: self.down_arrow_return())
         .step(key='express_delivery', value=self.sf, action='input', desc='物流单号')
         .step(key='express_amount', value=2, action='input', desc='物流费用')
         .step(key='remark', value='采购商品备注', action='input', desc='输入备注')
         .step(key='new_button', desc='新增')
         .step(key='ok_button', desc='确定')
         .step(key='auto_imei', desc='自动生成IMEI')
         .step(key='description', value='采购物品描述', action='input', desc='物品描述')
         .step(key='batch_amount', value='17', action='input', desc='金额')
         .step(key='please_enter_the_platform_item_number', value='采购平台物品编号', action='input', desc='平台物品编号')
         .step(key='serial_number', value=self.serial, action='input', desc='序列号')
         .step(key='order_number', value=self.serial, action='input', desc='平台订单号')
         .step(key='firm_commit', desc='确定')
         .scroll('payment_account')
         .step(key='payment_status_paid', desc='已付款')
         .step(key='send_payment_account', desc='付款账号')
         .custom(lambda: self.down_arrow_return())
         .step(key='payment_amount', value='5', action='input', desc='付款金额')
         .custom(lambda: self.carriage_return())
         .step(key='generate_purchase_order', desc='确定生成采购单')
         .step(key='stash_verify', desc='流转仓库确定')
         .wait())
        return self


class PurchaseAfterSaleListPages(CommonPages):
    """商品采购|采购售后管理|采购售后列表"""
    
    def menu_manage(self):
        """菜单"""
        (self.step(key='purchase_commodity_procurement_menu', desc='商品采购')
         .step(key='purchase_after_sale_manage_menu', desc='采购售后管理')
         .step(key='purchase_after_sale_list_menu', desc='采购售后列表')
         .wait())
        return self

    @reset_after_execution
    @doc(p_purchase_refund_single)
    def purchase_refund_single(self):
        self.menu_manage()
        (self.step(key='after_sale', desc='采购售后中')
         .step(key='update_status', desc='更新售后状态')
         .step(key='remark_input', value=self.serial, action='input', desc='备注')
         .step(key='hand_over_cancel', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(p_purchase_refuse_warehousing)
    def purchase_refuse_warehousing(self):
        self.menu_manage()
        (self.step(key='after_sale', desc='采购售后中')
         .step(key='update_status', desc='更新售后状态')
         .step(key='refusal_to_return', desc='拒退退回')
         .step(key='warehousing', desc='直接入库')
         .step(key='circulation_warehouse', desc='流转仓库')
         .custom(lambda: self.down_arrow_return())
         .step(key='remark_input', value=self.serial, action='input', desc='备注')
         .step(key='hand_over_cancel', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(p_purchase_barter_route)
    def purchase_barter_route(self):
        self.menu_manage()
        (self.step(key='after_sale', desc='采购售后中')
         .step(key='update_status', desc='更新售后状态')
         .step(key='alipay_payment', desc='换货')
         .step(key='please_enter_the_tracking_number', value=self.sf, action='input', desc='物流单号')
         .step(key='make_machine', desc='录入新机')
         .step(key='barter_new_imei', value=self.imei, action='input', desc='新物品IMEI')
         .step(key='barter_new_amount', value='34', action='input', desc='新物品金额')
         .step(key='barter_desc', value=self.number, action='input', desc='物品描述')
         .step(key='barter_remark_ipt', value=self.number, action='input', desc='备注')
         .step(key='barter_verify', desc='确认')
         .step(key='hand_over_cancel', desc='确认')
         .wait())
        return self


class PurchaseAwaitAfterSaleListPages(CommonPages):
    """商品采购|采购售后管理|待售后列表"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='purchase_commodity_procurement_menu', desc='商品采购')
         .step(key='purchase_after_sale_manage_menu', desc='采购售后管理')
         .step(key='purchase_post_sale_list_menu', desc='待售后列表')
         .wait())
        return self

    @reset_after_execution
    @doc(p_purchase_refund_difference_not_settled)
    def purchase_refund_difference_not_settled(self):
        self.menu_manage()
        (self.step(key='after_sale_operation', desc='售后操作')
         .step(key='reject_the_note', value=self.number, action='input', desc='新采购价')
         .step(key='after_sales_outbound_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(p_after_sales_delivery)
    def after_sales_delivery(self):
        self.menu_manage()
        (self.step(key='after_sale_operation', desc='售后操作')
         .step(key='after_sale_delivery', desc='售后出库')
         .step(key='tracking_number', value=self.sf, action='input', desc='物流单号')
         .step(key='express_charge', value='5', action='input', desc='物流费用')
         .step(key='after_sales_outbound_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(p_after_sales_outbound_return_refund_unsettled)
    def after_sales_outbound_return_refund_unsettled(self):
        self.menu_manage()
        (self.step(key='after_sale_operation', desc='售后操作')
         .step(key='after_sale_delivery', desc='售后出库')
         .step(key='tracking_number', value=self.sf, action='input', desc='物流单号')
         .step(key='express_charge', value='15', action='input', desc='物流费用')
         .step(key='returns_and_refunds', desc='退货退款')
         .step(key='after_sales_outbound_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(p_after_sales_outbound_refuse_to_return_warehousing)
    def after_sales_outbound_refuse_to_return_warehousing(self):
        self.menu_manage()
        (self.step(key='after_sale_operation', desc='售后操作')
         .step(key='after_sale_delivery', desc='售后出库')
         .step(key='tracking_number', value=self.sf, action='input', desc='物流单号')
         .step(key='express_charge', value='21', action='input', desc='物流费用')
         .step(key='price_adjustments', desc='拒退退回')
         .step(key='direct_warehousing', desc='直接入库')
         .step(key='circulation_warehouse', desc='流转仓库')
         .custom(lambda: self.down_arrow_return())
         .step(key='after_sales_outbound_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(p_after_sales_delivery_exchange_in_transit)
    def after_sales_delivery_exchange_in_transit(self):
        self.menu_manage()
        (self.step(key='after_sale_operation', desc='售后操作')
         .step(key='after_sale_delivery', desc='售后出库')
         .step(key='tracking_number', value=self.sf, action='input', desc='物流单号')
         .step(key='express_charge', value='24', action='input', desc='物流费用')
         .step(key='replacement', desc='换货')
         .step(key='tracking_number', value=self.sf, action='input', desc='物流单号')
         .step(key='enter_the_new_machine', desc='录入新机')
         .step(key='barter_new_imei', value=self.imei, action='input', desc='新物品imei')
         .step(key='barter_new_amount', value='23', action='input', desc='新物品采购金额')
         .step(key='enter_the_new_machine_to_confirm', desc='确定')
         .step(key='after_sales_outbound_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(p_cancel_purchase_after_sale)
    def cancel_purchase_after_sale(self):
        self.menu_manage()
        (self.step(key='cancel_after_sale', desc='取消售后')
         .step(key='cancel_after_sale_reason', value=self.serial, action='input', desc='售后原因')
         .step(key='confirm_cancel', desc='确认取消')
         .wait())
        return self


class PurchaseGoodsReceivedPages(CommonPages):
    """商品采购|采购售后管理|待接收物品"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='purchase_commodity_procurement_menu', desc='商品采购')
         .step(key='purchase_after_sale_manage_menu', desc='采购售后管理')
         .step(key='purchase_items_awaiting_receipt_menu', desc='待接收物品')
         .wait())
        return self

    @reset_after_execution
    @doc(p_goods_received)
    def goods_received(self):
        self.menu_manage()
        (self.step(key='select_all_dio', desc='全选')
         .step(key='more_handover_btn', desc='接收')
         .step(key='delete_address_ok', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(p_scan_goods_received)
    def scan_goods_received(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=2)[0]['articlesNo'])
        (self.step(key='scan_receive_btn', desc='扫码精确接收')
         .custom(self.affix_carriage_return)
         .step(key='scan_receive_btn', desc='接收')
         .step(key='delete_address_ok', desc='确定')
         .wait())
        return self


class PurchaseOrderListPages(CommonPages):
    """商品采购|采购管理|采购订单列表"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='purchase_commodity_procurement_menu', desc='商品采购')
         .step(key='purchase_manage_menu', desc='采购管理')
         .step(key='purchase_order_list_menu', desc='采购订单列表')
         .wait())
        return self

    @reset_after_execution
    @doc(p_new_purchase_order_refund)
    def new_purchase_order_refund(self):
        self.menu_manage()
        (self.step(key='purchase_order_number', desc='采购单号')
         .scroll('after_sale_treatment', desc='售后处理')
         .step(key='after_sale_treatment', desc='售后处理')
         .step(key='remark', value=self.serial, action='input', desc='备注')
         .step(key='verify', desc='确认售后')
         .wait())
        return self

    @reset_after_execution
    @doc(p_receive_goods)
    def receive_goods(self):
        self.menu_manage()
        (self.step(key='receive_goods', desc='收货')
         .custom(lambda: self.wait_time())
         .step(key='search', desc='搜索')
         .custom(lambda: self.tab_return(6))
         .step(key='be_put_in_storage', desc='签收入库')
         .step(key='stash', desc='流转仓库')
         .custom(lambda: self.down_arrow_return())
         .step(key='submit', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(p_logistics_delivery)
    def logistics_delivery(self):
        self.copy(self.pc.purchase_order_list_data(data='a')[0]['imei'])
        self.menu_manage()
        (self.step(key='logistics_delivery', desc='物流发货')
         .step(key='log_no_input_2', value=self.jd, action='input', desc='物流单号')
         .step(key='imei_input_2', desc='imei输入框')
         .custom(lambda: self.affix())
         .step(key='add', desc='添加')
         .step(key='verify_2', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(p_import_items_shipping)
    def import_items_shipping(self):
        self.menu_manage()
        (self.custom(lambda: self.file.get_inventory_data('logistics_delivery', 'imei', i=1, j=1))
         .step(key='logistics_delivery', desc='物流发货')
         .step(key='import_items', desc='导入物品')
         .step(key='handover_import', value=self.file_path('logistics_delivery'), action='upload', desc='上传文件')
         .step(key='determine', desc='确定')
         .step(key='log_no_input_2', value=self.jd, action='input', desc='物流单号')
         .step(key='verify_2', desc='确认')
         .wait())
        return self


class PurchaseSupplierManagePages(CommonPages):
    """商品采购|供应商管理"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='purchase_commodity_procurement_menu', desc='商品采购')
         .step(key='purchase_supplier_manage_menu', desc='供应商管理')
         .wait())
        return self

    @reset_after_execution
    @doc(p_new_supplier)
    def new_supplier(self):
        self.menu_manage()
        (self.step(key='add_a_new_supplier_btn', desc='新增')
         .step(key='please_enter_the_name_of_the_purchasing_supplier', value='供应商' + self.serial, action='input', desc='供应商名称')
         .step(key='select_supplier_type', desc='平台拍货')
         .step(key='default_account_dio', desc='默认账户')
         .custom(lambda: self.up_arrow_return())
         .step(key='default_payment_status_dio', desc='不选中')
         .step(key='contact_info_ipt', value=self.phone, action='input', desc='联系方式')
         .step(key='business_personnel_ipt', desc='业务人员')
         .custom(lambda: self.up_arrow_return())
         .step(key='please_select_your_province', desc='省')
         .custom(lambda: self.down_arrow_return())
         .step(key='please_select_the_city', desc='市')
         .custom(lambda: self.down_arrow_return())
         .step(key='please_select_the_zone', desc='区')
         .custom(lambda: self.down_arrow_return())
         .step(key='address', value='广州市黄埔区生生广场' + self.number, action='input', desc='详细地址')
         .step(key='refund_verify', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(p_edit_supplier)
    def edit_supplier(self):
        self.menu_manage()
        (self.step(key='edit_address_btn', desc='编辑')
         .step(key='contact_info', value=self.phone, action='input', desc='联系方式')
         .step(key='refund_verify', desc='确定')
         .wait())
        return self


class PurchaseWorkOrderPages(CommonPages):
    """商品采购|采购管理|采购工单"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='purchase_commodity_procurement_menu', desc='商品采购')
         .step(key='purchase_manage_menu', desc='采购管理')
         .step(key='purchase_work_order_menu', desc='采购工单')
         .wait())
        return self

    @reset_after_execution
    @doc(p_work_order_add)
    def work_order_add(self):
        self.menu_manage()
        (self.step(key='add_btn', desc='新增')
         .step(key='phone_add_icon', desc='+')
         .step(key='phone_confirm', desc='确定')
         .scroll('phone_item_confirm')
         .step(key='phone_item_confirm', desc='确定')
         .step(key='number', value=1, action='input', desc='计划数量')
         .step(key='please_select_a_supplier_w', desc='供应商')
         .custom(lambda: self.down_arrow_return())
         .step(key='add_work_order', desc='添加工序')
         .step(key='work_order_item', desc='工序选项')
         .step(key='work_order_confirm', desc='确定')
         .step(key='add_work_order_confirm', desc='确定')
         .wait())
        return self


class PurchaseUnsendListPages(CommonPages):
    """商品采购|采购管理|未发货订单列表"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='purchase_commodity_procurement_menu', desc='商品采购')
         .step(key='purchase_manage_menu', desc='采购管理')
         .step(key='purchase_the_list_of_unfulfilled_orders_menu', desc='未发货订单列表')
         .wait())
        return self

    @reset_after_execution
    @doc(p_order_export)
    def order_export(self):
        self.menu_manage()
        (self.step(key='surrender', desc='导出')
         .wait())
        return self
