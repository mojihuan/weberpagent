# coding: utf-8
import os
from common.base_page import BasePage, ImportDataEdit, reset_after_execution
from common.base_params import InitializeParams
from common.file_cache_manager import ParamCache
from common.import_desc import *
from config.settings import DATA_PATHS


class CommonPages(BasePage, InitializeParams):
    def __init__(self, driver):
        super().__init__(driver)
        self._steps_queue = []
        self.file = ImportDataEdit(driver)
        self.file_paths = self.file.file_paths = {
            'attachment_allocation': os.path.join(DATA_PATHS['excel'], 'attachment_allocation_import.xlsx')
        }


class AttachmentGoodsReceivedPages(CommonPages):
    """配件管理|入库管理|待接收物品"""

    def menu_manage(self):
        """菜单"""
        self.click(key='attachment_menu_1', desc='配件管理', tag='span', auto=False)
        self.click(key='attachment_menu_2', desc='入库管理', index=2, tag='span', auto=False)
        self.click(key='attachment_menu_3', desc='待接收物品', index=6, tag='span', auto=False)
        self.refresh_html_source()
        return self

    @reset_after_execution
    @doc(a_goods_received)
    def goods_received(self):
        self.menu_manage()
        self.click(key='goods_received_1', desc='搜索', tag='span')
        self.tab_return(5)
        self.click(key='goods_received_2', desc='接收', tag='span')
        self.refresh_html_source()
        self.click(key='goods_received_3', desc='确定', index=2, tag='span')
        self.capture_api_request(url_keyword=self.URL['accessory_receive_items'])
        return self

    @reset_after_execution
    @doc(a_scan_goods_received)
    def scan_goods_received(self):
        self.menu_manage()
        self.copy(self.pc.attachment_inventory_list_data(i=2)[0]['articlesNo'])
        self.click(key='scan_goods_received_1', desc='扫码精准接收', tag='span')
        self.affix_carriage_return()
        self.tab_return(2)
        self.refresh_html_source()
        self.click(key='scan_goods_received_2', desc='接收', index=2, tag='span')
        return self

    @reset_after_execution
    @doc(a_goods_received_search_item)
    def goods_received_search_item(self):
        self.menu_manage()
        obj = self.pc.attachment_inventory_list_data(i=2)[0]['articlesNo']
        self.copy(obj)
        ParamCache.cache_object({"articlesNo": obj})
        self.click(key='goods_received_search_item_1', desc='请输入物品编号', tag='input')
        self.affix()
        self.click(key='goods_received_search_item_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['items_to_be_received'])
        return self

    @reset_after_execution
    @doc(a_goods_received_search_time)
    def goods_received_search_time(self):
        self.menu_manage()
        obj = self.pc.attachment_inventory_list_data(i=2)[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj})
        self.input(key='goods_received_search_time_1', text=self.get_the_date(), desc='开始日期', tag='input')
        self.input(key='goods_received_search_time_2', text=self.get_the_date(days=1), desc='结束日期', tag='input')
        self.click(key='goods_received_search_time_3', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['items_to_be_received'])
        return self


class AttachmentHandOverItemsPages(CommonPages):
    """配件管理|移交接收管理|移交物品"""

    def menu_manage(self):
        """菜单"""
        self.click(key='attachment_menu_1', desc='配件管理', tag='span', auto=False)
        self.click(key='attachment_menu_4', desc='移交接收管理', tag='span', index=2, auto=False)
        self.click(key='attachment_menu_5', desc='移交物品', tag='span', index=2, auto=False)
        self.refresh_html_source()
        return self

    @reset_after_execution
    @doc(a_hand_over_items_to_inventory)
    def hand_over_items_to_inventory(self):
        self.menu_manage()
        self.copy(self.pc.attachment_inventory_list_data(i=2)[0]['articlesNo'])
        self.click(key='hand_over_items_to_inventory_1', desc='请输入物品编号或者IMEI', tag='input')
        self.affix()
        self.click(key='hand_over_items_to_inventory_2', desc='搜索', tag='span')
        self.click(key='hand_over_items_to_inventory_3', desc='移交', tag='span')
        self.refresh_html_source()
        self.click(key='hand_over_items_to_inventory_4', desc='请选择接收人', tag='input')
        self.down_arrow_return()
        self.input(key='hand_over_items_to_inventory_5', text='备注', desc='请填写移交说明', tag='textarea')
        self.click(key='hand_over_items_to_inventory_6', desc='确定', index=4, tag='span')
        self.capture_api_request(url_keyword=self.URL['inventory_transfer'])
        return self

    @reset_after_execution
    @doc(a_hand_over_items_to_purchase)
    def hand_over_items_to_purchase(self):
        self.menu_manage()
        self.copy(self.pc.attachment_inventory_list_data(i=2)[0]['articlesNo'])
        self.click(key='hand_over_items_to_purchase_1', desc='请输入物品编号或者IMEI', tag='input')
        self.affix()
        self.click(key='hand_over_items_to_purchase_2', desc='搜索', tag='span')
        self.click(key='hand_over_items_to_purchase_3', desc='移交', tag='span')
        self.refresh_html_source()
        self.click(key='hand_over_items_to_purchase_4', desc='采购售后', tag='span')
        self.click(key='hand_over_items_to_purchase_5', desc='请选择接收人', tag='input')
        self.down_arrow_return()
        self.input(key='hand_over_items_to_purchase_6', text='备注', desc='请填写移交说明', tag='textarea')
        self.click(key='hand_over_items_to_purchase_7', desc='确定', index=4, tag='span')
        self.capture_api_request(url_keyword=self.URL['inventory_transfer'])
        return self

    @reset_after_execution
    @doc(a_hand_over_items_to_sell)
    def hand_over_items_to_sell(self):
        self.menu_manage()
        self.copy(self.pc.attachment_inventory_list_data(i=2)[0]['articlesNo'])
        self.click(key='hand_over_items_to_sell_1', desc='请输入物品编号或者IMEI', tag='input')
        self.affix()
        self.click(key='hand_over_items_to_sell_2', desc='搜索', tag='span')
        self.click(key='hand_over_items_to_sell_3', desc='移交', tag='span')
        self.refresh_html_source()
        self.click(key='hand_over_items_to_sell_4', desc='销售', tag='span')
        self.click(key='hand_over_items_to_sell_5', desc='请选择接收人', tag='input')
        self.down_arrow_return()
        self.input(key='hand_over_items_to_sell_6', text='备注', desc='请填写移交说明', tag='textarea')
        self.click(key='hand_over_items_to_sell_7', desc='确定', index=4, tag='span')
        self.capture_api_request(url_keyword=self.URL['inventory_transfer'])
        return self

    @reset_after_execution
    @doc(a_hand_over_items_to_send)
    def hand_over_items_to_send(self):
        self.menu_manage()
        self.copy(self.pc.attachment_inventory_list_data(i=2)[0]['articlesNo'])
        self.click(key='hand_over_items_to_send_1', desc='请输入物品编号或者IMEI', tag='input')
        self.affix()
        self.click(key='hand_over_items_to_send_2', desc='搜索', tag='span')
        self.click(key='hand_over_items_to_send_3', desc='移交', tag='span')
        self.refresh_html_source()
        self.click(key='hand_over_items_to_send_4', desc='送修', tag='span')
        self.click(key='hand_over_items_to_send_5', desc='请选择接收人', tag='input')
        self.down_arrow_return()
        self.input(key='hand_over_items_to_send_6', text='备注', desc='请填写移交说明', tag='textarea')
        self.click(key='hand_over_items_to_send_7', desc='确定', index=4, tag='span')
        self.capture_api_request(url_keyword=self.URL['inventory_transfer'])
        return self

    @reset_after_execution
    @doc(a_hand_over_items_to_repair)
    def hand_over_items_to_repair(self):
        self.menu_manage()
        self.copy(self.pc.attachment_inventory_list_data(i=2)[0]['articlesNo'])
        self.click(key='hand_over_items_to_repair_1', desc='请输入物品编号或者IMEI', tag='input')
        self.affix()
        self.click(key='hand_over_items_to_repair_2', desc='搜索', tag='span')
        self.click(key='hand_over_items_to_repair_3', desc='移交', tag='span')
        self.refresh_html_source()
        self.click(key='hand_over_items_to_repair_4', desc='维修', tag='span')
        self.click(key='hand_over_items_to_repair_5', desc='请选择接收人', tag='input')
        self.down_arrow_return()
        self.input(key='hand_over_items_to_repair_6', text='备注', desc='请填写移交说明', tag='textarea')
        self.click(key='hand_over_items_to_repair_7', desc='确定', index=4, tag='span')
        self.capture_api_request(url_keyword=self.URL['inventory_transfer'])
        return self

    @reset_after_execution
    @doc(a_hand_over_items_to_quality)
    def hand_over_items_to_quality(self):
        self.menu_manage()
        self.copy(self.pc.attachment_inventory_list_data(i=2)[0]['articlesNo'])
        self.click(key='hand_over_items_to_quality_1', desc='请输入物品编号或者IMEI', tag='input')
        self.affix()
        self.click(key='hand_over_items_to_quality_2', desc='搜索', tag='span')
        self.click(key='hand_over_items_to_quality_3', desc='移交', tag='span')
        self.refresh_html_source()
        self.click(key='hand_over_items_to_quality_4', desc='质检', tag='span')
        self.click(key='hand_over_items_to_quality_5', desc='请选择接收人', tag='input')
        self.down_arrow_return()
        self.input(key='hand_over_items_to_quality_6', text='备注', desc='请填写移交说明', tag='textarea')
        self.click(key='hand_over_items_to_quality_7', desc='确定', index=4, tag='span')
        self.capture_api_request(url_keyword=self.URL['inventory_transfer'])
        return self

    @reset_after_execution
    @doc(a_hand_over_different_recipients)
    def hand_over_different_recipients(self):
        self.menu_manage()
        self.copy(self.pc.attachment_inventory_list_data(i=2)[0]['articlesNo'])
        self.click(key='hand_over_different_recipients_1', desc='请输入物品编号或者IMEI', tag='input')
        self.affix()
        self.click(key='hand_over_different_recipients_2', desc='搜索', tag='span')
        self.click(key='hand_over_different_recipients_3', desc='移交', tag='span')
        self.refresh_html_source()
        self.click(key='hand_over_different_recipients_4', desc='质检', tag='span')
        self.click(key='hand_over_different_recipients_5', desc='请选择接收人', tag='input')
        self.down_arrow_return(2)
        self.input(key='hand_over_different_recipients_6', text='备注', desc='请填写移交说明', tag='textarea')
        self.click(key='hand_over_different_recipients_7', desc='确定', index=4, tag='span')
        self.capture_api_request(url_keyword=self.URL['inventory_transfer'])
        return self

    @reset_after_execution
    @doc(a_hand_over_items_search_item)
    def hand_over_items_search_item(self):
        self.menu_manage()
        obj = self.pc.attachment_inventory_list_data(i=2)[0]['articlesNo']
        self.copy(obj)
        ParamCache.cache_object({"articlesNo": obj})
        self.click(key='hand_over_items_search_item_1', desc='请输入物品编号或者IMEI', tag='input')
        self.affix()
        self.click(key='hand_over_items_search_item_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['accessories_search_items'])
        return self


class AttachmentHandOverRecordsPages(CommonPages):
    """配件管理|移交接收管理|移交记录"""

    def menu_manage(self):
        """菜单"""
        self.click(key='attachment_menu_1', desc='配件管理', tag='span', auto=False)
        self.click(key='attachment_menu_4', desc='移交接收管理', tag='span', index=2, auto=False)
        self.click(key='attachment_menu_6', desc='移交记录', tag='span', index=2, auto=False)
        self.refresh_html_source()
        return self

    @reset_after_execution
    @doc(a_transfer_records_export)
    def transfer_records_export(self):
        self.menu_manage()
        self.click(key='transfer_records_export_1', desc='导出', index=3, tag='span')
        return self

    @reset_after_execution
    @doc(a_bulk_cancel_handovers)
    def bulk_cancel_handovers(self):
        self.menu_manage()
        self.click(key='bulk_cancel_handovers_1', desc='移交物品数量链接', tag='button', auto=False)
        self.refresh_html_source()
        self.click(key='bulk_cancel_handovers_2', desc='搜索', index=2, tag='span')
        self.tab_return(4)
        self.click(key='bulk_cancel_handovers_3', desc='批量取消移交', tag='span')
        self.refresh_html_source()
        self.click(key='bulk_cancel_handovers_4', desc='确定', index=2, tag='span')
        self.capture_api_request(url_keyword=self.URL['bulk_cancel_handovers'])
        return self

    @reset_after_execution
    @doc(a_cancel_handovers)
    def cancel_handovers(self):
        self.menu_manage()
        self.click(key='cancel_handovers_1', desc='移交物品数量链接', tag='button', auto=False)
        self.refresh_html_source()
        self.click(key='cancel_handovers_2', desc='搜索', index=2, tag='span')
        self.tab_return(4)
        self.click(key='cancel_handovers_3', desc='取消移交', tag='span', auto=False)
        self.refresh_html_source()
        self.click(key='cancel_handovers_4', desc='确定', index=2, tag='span')
        return self

    @reset_after_execution
    @doc(a_hand_over_items_search_item_no)
    def hand_over_items_search_item_no(self):
        self.menu_manage()
        obj = self.pc.attachment_handover_records_data(data='a')[0]['articlesNo']
        self.copy(obj)
        ParamCache.cache_object({"articlesNo": obj})
        self.click(key='hand_over_items_search_item_no_1', desc='请输入编号/IMEI', tag='input')
        self.affix()
        self.click(key='hand_over_items_search_item_no_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['handover_records'])
        return self

    @reset_after_execution
    @doc(a_hand_over_items_search_order)
    def hand_over_items_search_order(self):
        self.menu_manage()
        obj = self.pc.attachment_handover_records_data()[0]['orderNo']
        self.copy(obj)
        ParamCache.cache_object({"orderNo": obj})
        self.click(key='hand_over_items_search_order_1', desc='请输入移交单号', tag='input')
        self.affix()
        self.click(key='hand_over_items_search_order_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['handover_records'])
        return self

    @reset_after_execution
    @doc(a_hand_over_items_search_status)
    def hand_over_items_search_status(self):
        self.menu_manage()
        obj = self.pc.attachment_handover_records_data()[0]['orderNo']
        ParamCache.cache_object({"orderNo": obj})
        self.click(key='hand_over_items_search_status_1', desc='请选择移交单状态', tag='input')
        self.down_arrow_return()
        self.click(key='hand_over_items_search_status_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['handover_records'])
        return self

    @reset_after_execution
    @doc(a_hand_over_items_search_name)
    def hand_over_items_search_name(self):
        self.menu_manage()
        obj = self.pc.attachment_handover_records_data()[0]['orderNo']
        ParamCache.cache_object({"orderNo": obj})
        self.click(key='hand_over_items_search_name_1', desc='请选择移交人', tag='input')
        self.down_arrow_return()
        self.click(key='hand_over_items_search_name_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['handover_records'])
        return self

    @reset_after_execution
    @doc(a_hand_over_items_search_receive)
    def hand_over_items_search_receive(self):
        self.menu_manage()
        obj = self.pc.attachment_handover_records_data()[0]['orderNo']
        ParamCache.cache_object({"orderNo": obj})
        self.click(key='hand_over_items_search_receive_1', desc='请选择接收人', tag='input')
        self.down_arrow_return(2)
        self.click(key='hand_over_items_search_receive_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['handover_records'])
        return self

    @reset_after_execution
    @doc(a_hand_over_items_search_time)
    def hand_over_items_search_time(self):
        self.menu_manage()
        obj = self.pc.attachment_handover_records_data()[0]['orderNo']
        ParamCache.cache_object({"orderNo": obj})
        self.input(key='hand_over_items_search_time_1', desc='开始日期', text=self.get_the_date(), tag='input')
        self.input(key='hand_over_items_search_time_2', desc='结束日期', text=self.get_the_date(days=1), tag='input')
        self.click(key='hand_over_items_search_time_3', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['handover_records'])
        return self


class AttachmentInventoryListPages(CommonPages):
    """配件管理|配件库存|库存列表"""

    def menu_manage(self):
        """菜单"""
        self.click(key='attachment_menu_1', desc='配件管理', tag='span', auto=False)
        self.scroll_custom(element='attachment_menu_7')
        self.click(key='attachment_menu_7', desc='配件库存', tag='span', auto=False)
        self.click(key='attachment_menu_8', desc='库存列表', tag='span', index=2, auto=False)
        return self

    @reset_after_execution
    @doc(a_transfer_items_special)
    def transfer_items_special(self):
        self.menu_manage()
        self.click(key='transfer_items_special_1', desc='请选择库存状态', tag='input')
        self.down_arrow_return(2)
        self.click(key='transfer_items_special_2', desc='搜索', tag='span')
        self.tab_return(6)
        self.click(key='transfer_items_special_3', desc='批量移交', tag='span')
        self.refresh_html_source()
        self.click(key='transfer_items_special_4', desc='请选择接收人', tag='input')
        self.down_arrow_return(2)
        self.input(key='transfer_items_special_5', text='备注', desc='请填写移交说明', tag='textarea')
        self.click(key='transfer_items_special_6', desc='确定', index=5, tag='span')
        self.capture_api_request(url_keyword=self.URL['inventory_transfer'])
        return self

    @reset_after_execution
    @doc(a_handover_items_purchase_after_sales)
    def handover_items_purchase_after_sales(self):
        self.menu_manage()
        self.click(key='handover_items_purchase_after_sales_1', desc='请选择库存状态', tag='input')
        self.down_arrow_return(2)
        self.click(key='handover_items_purchase_after_sales_2', desc='搜索', tag='span')
        self.tab_return(6)
        self.click(key='handover_items_purchase_after_sales_3', desc='批量移交', tag='span')
        self.refresh_html_source()
        self.click(key='handover_items_purchase_after_sales_4', desc='请选择接收人', tag='input')
        self.down_arrow_return(2)
        self.click(key='handover_items_purchase_after_sales_5', desc='采购售后', tag='span', index=2)
        self.input(key='handover_items_purchase_after_sales_6', text='备注', desc='请填写移交说明', tag='textarea')
        self.click(key='handover_items_purchase_after_sales_7', desc='确定', index=5, tag='span')
        self.capture_api_request(url_keyword=self.URL['inventory_transfer'])
        return self

    @reset_after_execution
    @doc(a_handover_items_sell_personnel)
    def handover_items_sell_personnel(self):
        self.menu_manage()
        self.click(key='handover_items_sell_personnel_1', desc='请选择库存状态', tag='input')
        self.down_arrow_return(2)
        self.click(key='handover_items_sell_personnel_2', desc='搜索', tag='span')
        self.tab_return(6)
        self.click(key='handover_items_sell_personnel_3', desc='批量移交', tag='span')
        self.refresh_html_source()
        self.click(key='handover_items_sell_personnel_4', desc='请选择接收人', tag='input')
        self.down_arrow_return(2)
        self.click(key='handover_items_sell_personnel_5', desc='销售', tag='span')
        self.input(key='handover_items_sell_personnel_6', text='备注', desc='请填写移交说明', tag='textarea')
        self.click(key='handover_items_sell_personnel_7', desc='确定', index=5, tag='span')
        self.capture_api_request(url_keyword=self.URL['inventory_transfer'])
        return self

    @reset_after_execution
    @doc(a_handover_items_send_personnel)
    def handover_items_send_personnel(self):
        self.menu_manage()
        self.click(key='handover_items_send_personnel_1', desc='请选择库存状态', tag='input')
        self.down_arrow_return(2)
        self.click(key='handover_items_send_personnel_2', desc='搜索', tag='span')
        self.tab_return(6)
        self.click(key='handover_items_send_personnel_3', desc='批量移交', tag='span')
        self.refresh_html_source()
        self.click(key='handover_items_send_personnel_4', desc='请选择接收人', tag='input')
        self.down_arrow_return(2)
        self.click(key='handover_items_send_personnel_5', desc='送修', tag='span')
        self.input(key='handover_items_send_personnel_6', text='备注', desc='请填写移交说明', tag='textarea')
        self.click(key='handover_items_send_personnel_7', desc='确定', index=5, tag='span')
        self.capture_api_request(url_keyword=self.URL['inventory_transfer'])
        return self

    @reset_after_execution
    @doc(a_handover_items_repair_personnel)
    def handover_items_repair_personnel(self):
        self.menu_manage()
        self.click(key='handover_items_repair_personnel_1', desc='请选择库存状态', tag='input')
        self.down_arrow_return(2)
        self.click(key='handover_items_repair_personnel_2', desc='搜索', tag='span')
        self.tab_return(6)
        self.click(key='handover_items_repair_personnel_3', desc='批量移交', tag='span')
        self.refresh_html_source()
        self.click(key='handover_items_repair_personnel_4', desc='请选择接收人', tag='input')
        self.down_arrow_return(2)
        self.click(key='handover_items_repair_personnel_5', desc='维修', tag='span')
        self.input(key='handover_items_repair_personnel_6', text='备注', desc='请填写移交说明', tag='textarea')
        self.click(key='handover_items_repair_personnel_7', desc='确定', index=5, tag='span')
        self.capture_api_request(url_keyword=self.URL['inventory_transfer'])
        return self

    @reset_after_execution
    @doc(a_handover_items_quality_personnel)
    def handover_items_quality_personnel(self):
        self.menu_manage()
        self.click(key='handover_items_quality_personnel_1', desc='请选择库存状态', tag='input')
        self.down_arrow_return(2)
        self.click(key='handover_items_quality_personnel_2', desc='搜索', tag='span')
        self.tab_return(6)
        self.click(key='handover_items_quality_personnel_3', desc='批量移交', tag='span')
        self.refresh_html_source()
        self.click(key='handover_items_quality_personnel_4', desc='请选择接收人', tag='input')
        self.down_arrow_return(2)
        self.click(key='handover_items_quality_personnel_5', desc='维修', tag='span')
        self.input(key='handover_items_quality_personnel_6', text='备注', desc='请填写移交说明', tag='textarea')
        self.click(key='handover_items_quality_personnel_7', desc='确定', index=5, tag='span')
        self.capture_api_request(url_keyword=self.URL['inventory_transfer'])
        return self

    @reset_after_execution
    @doc(a_accessory_sales_express_delivery)
    def accessory_sales_express_delivery(self):
        self.menu_manage()
        self.click(key='accessory_sales_express_delivery_1', desc='请选择库存状态', tag='input')
        self.down_arrow_return(2)
        self.click(key='accessory_sales_express_delivery_2', desc='搜索', tag='span')
        self.tab_return(6)
        self.click(key='accessory_sales_express_delivery_3', desc='配件销售', index=2, tag='span')
        self.refresh_html_source()
        self.click(key='accessory_sales_express_delivery_4', desc='请选择客户', tag='input')
        self.down_arrow_return(2)
        self.click(key='accessory_sales_express_delivery_5', desc='已收款', tag='span')
        self.click(key='accessory_sales_express_delivery_6', desc='请选择收款账户', tag='input')
        self.down_arrow_return()
        self.click(key='accessory_sales_express_delivery_7', desc='快递易图标开关', auto=False)
        self.refresh_html_source()
        self.click(key='accessory_sales_express_delivery_8', desc='计算运费', tag='span')
        self.input(key='accessory_sales_express_delivery_9', text='备注', desc='请填写备注', tag='input')
        self.input(key='accessory_sales_express_delivery_10', text='120', desc='请输入销售金额', tag='input')
        self.scroll_custom(element='accessory_sales_express_delivery_11')
        self.click(key='accessory_sales_express_delivery_11', desc='确定', index=5, tag='span')
        self.capture_api_request(url_keyword=self.URL['accessory_sales'])
        return self

    @reset_after_execution
    @doc(a_accessory_sales)
    def accessory_sales(self):
        self.menu_manage()
        self.click(key='accessory_sales_1', desc='请选择库存状态', tag='input')
        self.down_arrow_return(2)
        self.click(key='accessory_sales_2', desc='搜索', tag='span')
        self.tab_return(6)
        self.click(key='accessory_sales_3', desc='配件销售', index=2, tag='span')
        self.refresh_html_source()
        self.click(key='accessory_sales_4', desc='请选择客户', tag='input')
        self.down_arrow_return(2)
        self.click(key='accessory_sales_5', desc='未收款', tag='span')
        self.click(key='accessory_sales_6', desc='请选择收款账户', tag='input')
        self.down_arrow_return()
        self.input(key='accessory_sales_7', text=self.sf, desc='请填写物流单号', tag='input')
        self.input(key='accessory_sales_8', text='12', desc='请填写物流费用', tag='input')
        self.input(key='accessory_sales_9', text='备注', desc='请填写备注', tag='input')
        self.input(key='accessory_sales_10', text='120', desc='请输入销售金额', tag='input')
        self.scroll_custom(element='accessory_sales_11')
        self.click(key='accessory_sales_11', desc='确定', index=4, tag='span')
        self.capture_api_request(url_keyword=self.URL['accessory_sales'])
        return self

    @reset_after_execution
    @doc(a_item_details_modify_item_information)
    def item_details_modify_item_information(self):
        self.menu_manage()
        self.click(key='item_details_modify_item_information_1', desc='物品编号链接', auto=False)
        self.click(key='item_details_modify_item_information_2', desc='修改图标', auto=False)
        self.refresh_html_source()
        self.click(key='item_details_modify_item_information_3', desc='请选择品牌', tag='input', auto=False)
        self.down_arrow_return(2)
        self.click(key='item_details_modify_item_information_4', desc='请选择型号', tag='input', auto=False)
        self.down_arrow_return(2)
        self.wait_time(2)
        self.click(key='item_details_modify_item_information_5', desc='请选择配件名称', auto=False, tag='input')
        self.down_arrow_return(2)
        self.click(key='item_details_modify_item_information_6', desc='确 定', tag='span')
        self.capture_api_request(url_keyword=self.URL['modify_the_sku_information'])
        return self

    @reset_after_execution
    @doc(a_list_edit_item_info)
    def list_edit_item_info(self):
        self.menu_manage()
        self.click(key='list_edit_item_info_1', desc='修改图标', auto=False)
        self.refresh_html_source()
        self.click(key='list_edit_item_info_2', desc='请选择品牌', index=2, tag='input')
        self.down_arrow_return(2)
        self.click(key='list_edit_item_info_3', desc='请选择型号', index=2, tag='input')
        self.down_arrow_return(2)
        self.click(key='list_edit_item_info_4', desc='请选择配件名称', tag='input')
        self.down_arrow_return(2)
        self.click(key='list_edit_item_info_5', desc='确 定', tag='span')
        self.capture_api_request(url_keyword=self.URL['modify_the_sku_information'])
        return self

    @reset_after_execution
    @doc(a_attachment_inventory_list_search_item)
    def attachment_inventory_list_search_item(self):
        self.menu_manage()
        obj = self.pc.attachment_inventory_list_data()[0]['articlesNo']
        self.copy(obj)
        ParamCache.cache_object({"articlesNo": obj})
        self.click(key='attachment_inventory_list_search_item_1', desc='请输入物品编号', tag='input')
        self.affix()
        self.click(key='attachment_inventory_list_search_item_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['inventory_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_inventory_list_search_suppliers)
    def attachment_inventory_list_search_suppliers(self):
        self.menu_manage()
        obj = self.pc.attachment_inventory_list_data()[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj})
        self.click(key='attachment_inventory_list_search_suppliers_1', desc='请选择供应商名称', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_inventory_list_search_suppliers_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['inventory_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_inventory_list_search_affiliation)
    def attachment_inventory_list_search_affiliation(self):
        self.menu_manage()
        obj = self.pc.attachment_inventory_list_data()[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj})
        self.click(key='attachment_inventory_list_search_affiliation_1', desc='请选择所属人', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_inventory_list_search_affiliation_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['inventory_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_inventory_list_search_order_no)
    def attachment_inventory_list_search_order_no(self):
        self.menu_manage()
        obj = self.pc.attachment_inventory_list_data()[0]['purchaseNo']
        ParamCache.cache_object({"purchaseNo": obj})
        self.click(key='attachment_inventory_list_search_order_no_1', desc='请输入采购单号', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_inventory_list_search_order_no_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['inventory_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_inventory_list_search_purchaser)
    def attachment_inventory_list_search_purchaser(self):
        self.menu_manage()
        obj = self.pc.attachment_inventory_list_data()[0]['purchaseNo']
        ParamCache.cache_object({"purchaseNo": obj})
        self.click(key='attachment_inventory_list_search_purchaser_1', desc='请选择采购人员', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_inventory_list_search_purchaser_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['inventory_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_inventory_list_search_time)
    def attachment_inventory_list_search_time(self):
        self.menu_manage()
        obj = self.pc.attachment_inventory_list_data()[0]['purchaseNo']
        ParamCache.cache_object({"purchaseNo": obj})
        self.input(key='attachment_inventory_list_search_time_1', text=self.get_the_date(), desc='开始日期', tag='input')
        self.input(key='attachment_inventory_list_search_time_2', text=self.get_the_date(days=1), desc='结束日期', tag='input')
        self.click(key='attachment_inventory_list_search_time_3', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['inventory_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_inventory_list_search_class)
    def attachment_inventory_list_search_class(self):
        self.menu_manage()
        obj = self.pc.attachment_inventory_list_data()[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj})
        self.click(key='attachment_inventory_list_search_class_1', desc='请选择配件分类', tag='input')
        self.down_arrow_return(2)
        self.click(key='attachment_inventory_list_search_class_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['inventory_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_inventory_list_search_status)
    def attachment_inventory_list_search_status(self):
        self.menu_manage()
        obj = self.pc.attachment_inventory_list_data()[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj})
        self.click(key='attachment_inventory_list_search_status_1', desc='请选择库存状态', tag='input')
        self.down_arrow_return(2)
        self.click(key='attachment_inventory_list_search_status_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['inventory_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_inventory_list_search_category)
    def attachment_inventory_list_search_category(self):
        self.menu_manage()
        obj = self.pc.attachment_inventory_list_data()[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj})
        self.click(key='attachment_inventory_list_search_category_1', desc='请选择品类', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_inventory_list_search_category_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['inventory_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_inventory_list_search_brand_model)
    def attachment_inventory_list_search_brand_model(self):
        self.menu_manage()
        obj = self.pc.attachment_inventory_list_data()[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj})
        self.click(key='attachment_inventory_list_search_brand_model_1', desc='请选择品类', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_inventory_list_search_brand_model_2', desc='请选择品牌', tag='input')
        self.down_arrow_return(2)
        self.click(key='attachment_inventory_list_search_brand_model_3', desc='请选择型号', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_inventory_list_search_brand_model_4', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['inventory_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_inventory_list_search_warehouse)
    def attachment_inventory_list_search_warehouse(self):
        self.menu_manage()
        obj = self.pc.attachment_inventory_list_data()[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj})
        self.click(key='attachment_inventory_list_search_warehouse_1', desc='请选择仓库', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_inventory_list_search_warehouse_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['inventory_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_inventory_list_search_accessory_name)
    def attachment_inventory_list_search_accessory_name(self):
        self.menu_manage()
        obj = self.pc.attachment_inventory_list_data()[0]['articlesNo']
        obj_2 = self.pc.attachment_inventory_list_data()[0]['accessoryName']
        self.copy(obj_2)
        ParamCache.cache_object({"articlesNo": obj})
        self.click(key='attachment_inventory_list_search_accessory_name_1', desc='展开筛选链接', tag='span', auto=False)
        self.click(key='attachment_inventory_list_search_accessory_name_2', desc='请输入配件名称', tag='input')
        self.affix()
        self.click(key='attachment_inventory_list_search_accessory_name_3', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['inventory_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_inventory_list_search_color)
    def attachment_inventory_list_search_color(self):
        self.menu_manage()
        obj = self.pc.attachment_inventory_list_data()[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj})
        self.click(key='attachment_inventory_list_search_color_1', desc='展开筛选链接', tag='span', auto=False)
        self.click(key='attachment_inventory_list_search_color_2', desc='请选择配件成色', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_inventory_list_search_color_3', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['inventory_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_inventory_list_search_serial_number)
    def attachment_inventory_list_search_serial_number(self):
        self.menu_manage()
        obj = self.pc.attachment_inventory_list_data()[0]['accessoryNo']
        ParamCache.cache_object({"accessoryNo": obj})
        self.click(key='attachment_inventory_list_search_serial_number_1', desc='展开筛选链接', tag='span', auto=False)
        self.click(key='attachment_inventory_list_search_serial_number_2', desc='请输入配件编号', tag='input')
        self.affix()
        self.click(key='attachment_inventory_list_search_serial_number_3', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['inventory_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_inventory_list_search_duration)
    def attachment_inventory_list_search_duration(self):
        self.menu_manage()
        obj = self.pc.attachment_inventory_list_data()[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj})
        self.click(key='attachment_inventory_list_search_duration_1', desc='展开筛选链接', tag='span', auto=False)
        self.click(key='attachment_inventory_list_search_duration_2', desc='请选择天数', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_inventory_list_search_duration_3', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['inventory_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_inventory_list_search_channel)
    def attachment_inventory_list_search_channel(self):
        self.menu_manage()
        obj = self.pc.attachment_inventory_list_data()[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj})
        self.click(key='attachment_inventory_list_search_channel_1', desc='展开筛选链接', tag='span', auto=False)
        self.click(key='attachment_inventory_list_search_channel_2', desc='请选择配件渠道', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_inventory_list_search_channel_3', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['inventory_list'])
        return self


class AttachmentMaintenancePages(CommonPages):
    """配件管理|配件维护"""

    def menu_manage(self):
        """菜单"""
        self.click(key='attachment_menu_1', desc='配件管理', tag='span', auto=False)
        self.scroll_custom(element='attachment_menu_9')
        self.click(key='attachment_menu_9', desc='配件维护', tag='span', auto=False)
        self.refresh_html_source()
        return self

    @reset_after_execution
    @doc(a_added_a_button_category_external_category)
    def added_a_button_category_external_category(self):
        self.menu_manage()
        self.click(key='added_a_button_category_external_category_1', desc='新增', tag='span')
        self.refresh_html_source()
        self.click(key='added_a_button_category_external_category_2', desc='请选择配件品类', tag='input')
        self.up_arrow_return()
        self.input(key='added_a_button_category_external_category_3', text='名称' + self.imei, desc='请输入配件名称', index=2, tag='input')
        self.click(key='added_a_button_category_external_category_4', desc='状态开关', auto=False)
        self.click(key='added_a_button_category_external_category_5', desc='确 定', tag='span')
        self.capture_api_request(url_keyword=self.URL['new_maintenance'])
        return self

    @reset_after_execution
    @doc(a_added_a_button_category_matching)
    def added_a_button_category_matching(self):
        self.menu_manage()
        self.click(key='added_a_button_category_matching_1', desc='新增', tag='span')
        self.refresh_html_source()
        self.click(key='added_a_button_category_matching_2', desc='请选择配件品类', tag='input')
        self.down_arrow_return(2)
        self.input(key='added_a_button_category_matching_3', text='名称' + self.imei, desc='请输入配件名称', index=2, tag='input')
        self.click(key='added_a_button_category_matching_4', desc='状态开关', auto=False)
        self.click(key='added_a_button_category_matching_5', desc='确 定', tag='span')
        self.capture_api_request(url_keyword=self.URL['new_maintenance'])
        return self

    @reset_after_execution
    @doc(a_modify_the_accessory_name)
    def modify_the_accessory_name(self):
        self.menu_manage()
        self.click(key='modify_the_accessory_name_1', desc='编辑', tag='span', auto=False)
        self.refresh_html_source()
        self.input(key='modify_the_accessory_name_2', text='摄像头', desc='请输入配件名称', tag='input', index=2)
        self.click(key='modify_the_accessory_name_3', desc='确 定', tag='span')
        self.capture_api_request(url_keyword=self.URL['modify_the_accessory_name'])
        return self

    @reset_after_execution
    @doc(a_delete_the_accessory_name)
    def delete_the_accessory_name(self):
        self.menu_manage()
        self.click(key='delete_the_accessory_name_1', desc='删除', tag='span', auto=False)
        self.refresh_html_source()
        self.click(key='delete_the_accessory_name_2', desc='确定', tag='span', index=2)
        self.capture_api_request(url_keyword=self.URL['delete_the_accessory_name'])
        return self

    @reset_after_execution
    @doc(a_attachment_maintenance_search_num)
    def attachment_maintenance_search_num(self):
        self.menu_manage()
        obj = self.pc.attachment_maintenance_data()[0]['accessoryNo']
        self.copy(obj)
        ParamCache.cache_object({"accessoryNo": obj})
        self.click(key='attachment_maintenance_search_num_1', desc='请输入配件编号', tag='input')
        self.affix()
        self.click(key='attachment_maintenance_search_num_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['maintenance_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_maintenance_search_name)
    def attachment_maintenance_search_name(self):
        self.menu_manage()
        obj = self.pc.attachment_maintenance_data()[0]['accessoryName']
        self.copy(obj)
        ParamCache.cache_object({"accessoryName": obj})
        self.click(key='attachment_maintenance_search_name_1', desc='请输入配件名称', tag='input')
        self.affix()
        self.click(key='attachment_maintenance_search_name_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['maintenance_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_maintenance_search_status)
    def attachment_maintenance_search_status(self):
        self.menu_manage()
        obj = self.pc.attachment_maintenance_data()[0]['accessoryName']
        self.copy(obj)
        ParamCache.cache_object({"accessoryName": obj})
        self.click(key='attachment_maintenance_search_status_1', desc='请选择配件状态', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_maintenance_search_status_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['maintenance_list'])
        return self


class AttachmentOldWarehousePages(CommonPages):
    """配件管理|入库管理|旧配件入库"""

    def menu_manage(self):
        """菜单"""
        self.click(key='attachment_menu_1', desc='配件管理', tag='span', auto=False)
        self.click(key='attachment_menu_2', desc='入库管理', tag='span', index=2, auto=False)
        self.click(key='attachment_menu_10', desc='旧配件入库', tag='span', auto=False)
        self.refresh_html_source()
        return self

    @reset_after_execution
    @doc(a_phone_old_attachment_warehouse)
    def phone_old_attachment_warehouse(self):
        self.menu_manage()
        self.click(key='phone_old_attachment_warehouse_1', desc='新建入库', tag='span')
        self.refresh_html_source()
        self.click(key='phone_old_attachment_warehouse_2', desc='请选择仓库', index=2, tag='input')
        self.down_arrow_return(2)
        self.click(key='phone_old_attachment_warehouse_3', desc='请选择入库人', index=2, tag='input')
        self.down_arrow_return(2)
        self.input(key='phone_old_attachment_warehouse_4', text='备注', desc='请输入备注', tag='input')
        self.click(key='phone_old_attachment_warehouse_5', desc='添加物品', tag='span')
        self.refresh_html_source()
        self.click(key='phone_old_attachment_warehouse_6', desc='请选择品类', tag='input')
        self.down_arrow_return()
        self.click(key='phone_old_attachment_warehouse_7', desc='请选择适用品牌', tag='input')
        self.down_arrow_return()
        self.click(key='phone_old_attachment_warehouse_8', desc='请选择适用型号', tag='input')
        self.down_arrow_return()
        self.click(key='phone_old_attachment_warehouse_9', desc='请选择配件品类', tag='input')
        self.up_arrow_return()
        self.click(key='phone_old_attachment_warehouse_10', desc='请选择配件名称', tag='input')
        self.down_arrow_return()
        self.click(key='phone_old_attachment_warehouse_11', desc='请选择渠道', tag='input')
        self.down_arrow_return()
        self.input(key='phone_old_attachment_warehouse_12', text='1', desc='请输入具体数量', tag='input')
        self.input(key='phone_old_attachment_warehouse_13', text='15', desc='请输入采购价格', tag='input')
        self.click(key='phone_old_attachment_warehouse_14', desc='添加并关闭', tag='span')
        self.refresh_html_source()
        self.click(key='phone_old_attachment_warehouse_15', desc='确认入库', tag='span')
        self.capture_api_request(url_keyword=self.URL['old_create_purchase_order'])
        return self

    @reset_after_execution
    @doc(a_thousand_phone_old_attachment_warehouse)
    def thousand_phone_old_attachment_warehouse(self):
        self.menu_manage()
        self.click(key='thousand_phone_old_attachment_warehouse_1', desc='新建入库', tag='span')
        self.refresh_html_source()
        self.click(key='thousand_phone_old_attachment_warehouse_2', desc='请选择仓库', index=2, tag='input')
        self.down_arrow_return(2)
        self.click(key='thousand_phone_old_attachment_warehouse_3', desc='请选择入库人', index=2, tag='input')
        self.down_arrow_return(2)
        self.input(key='thousand_phone_old_attachment_warehouse_4', text='备注', desc='请输入备注', tag='input')
        self.click(key='thousand_phone_old_attachment_warehouse_5', desc='添加物品', tag='span')
        self.refresh_html_source()
        self.click(key='thousand_phone_old_attachment_warehouse_6', desc='请选择品类', tag='input')
        self.down_arrow_return()
        self.click(key='thousand_phone_old_attachment_warehouse_7', desc='请选择适用品牌', tag='input')
        self.down_arrow_return()
        self.click(key='thousand_phone_old_attachment_warehouse_8', desc='请选择适用型号', tag='input')
        self.down_arrow_return()
        self.click(key='thousand_phone_old_attachment_warehouse_9', desc='请选择配件品类', tag='input')
        self.up_arrow_return()
        self.click(key='thousand_phone_old_attachment_warehouse_10', desc='请选择配件名称', tag='input')
        self.down_arrow_return()
        self.click(key='thousand_phone_old_attachment_warehouse_11', desc='请选择渠道', tag='input')
        self.down_arrow_return()
        self.input(key='thousand_phone_old_attachment_warehouse_12', text='1000', desc='请输入具体数量', tag='input')
        self.input(key='thousand_phone_old_attachment_warehouse_13', text='15', desc='请输入采购价格', tag='input')
        self.click(key='thousand_phone_old_attachment_warehouse_14', desc='添加并关闭', tag='span')
        self.refresh_html_source()
        self.click(key='thousand_phone_old_attachment_warehouse_15', desc='确认入库', tag='span')
        self.capture_api_request(url_keyword=self.URL['old_create_purchase_order'])
        return self

    @reset_after_execution
    @doc(a_ipa_old_attachment_warehouse)
    def ipa_old_attachment_warehouse(self):
        self.menu_manage()
        self.click(key='ipa_old_attachment_warehouse_1', desc='新建入库', tag='span')
        self.refresh_html_source()
        self.click(key='ipa_old_attachment_warehouse_2', desc='请选择仓库', index=2, tag='input')
        self.down_arrow_return(2)
        self.click(key='ipa_old_attachment_warehouse_3', desc='请选择入库人', index=2, tag='input')
        self.down_arrow_return(2)
        self.input(key='ipa_old_attachment_warehouse_4', text='备注', desc='请输入备注', tag='input')
        self.click(key='ipa_old_attachment_warehouse_5', desc='添加物品', tag='span')
        self.refresh_html_source()
        self.click(key='ipa_old_attachment_warehouse_6', desc='请选择品类', tag='input')
        self.down_arrow_return(2)
        self.click(key='ipa_old_attachment_warehouse_7', desc='请选择适用品牌', tag='input')
        self.down_arrow_return(2)
        self.click(key='ipa_old_attachment_warehouse_8', desc='请选择适用型号', tag='input')
        self.down_arrow_return(2)
        self.click(key='ipa_old_attachment_warehouse_9', desc='请选择配件品类', tag='input')
        self.up_arrow_return()
        self.click(key='ipa_old_attachment_warehouse_10', desc='请选择配件名称', tag='input')
        self.down_arrow_return()
        self.click(key='ipa_old_attachment_warehouse_11', desc='请选择渠道', tag='input')
        self.down_arrow_return()
        self.input(key='ipa_old_attachment_warehouse_12', text='1000', desc='请输入具体数量', tag='input')
        self.input(key='ipa_old_attachment_warehouse_13', text='15', desc='请输入采购价格', tag='input')
        self.click(key='ipa_old_attachment_warehouse_14', desc='添加并关闭', tag='span')
        self.refresh_html_source()
        self.click(key='ipa_old_attachment_warehouse_15', desc='确认入库', tag='span')
        self.capture_api_request(url_keyword=self.URL['old_create_purchase_order'])
        return self

    @reset_after_execution
    @doc(a_notebook_old_attachment_warehouse)
    def notebook_old_attachment_warehouse(self):
        self.menu_manage()
        self.click(key='notebook_old_attachment_warehouse_1', desc='新建入库', tag='span')
        self.refresh_html_source()
        self.click(key='notebook_old_attachment_warehouse_2', desc='请选择仓库', index=2, tag='input')
        self.down_arrow_return(2)
        self.click(key='notebook_old_attachment_warehouse_3', desc='请选择入库人', index=2, tag='input')
        self.down_arrow_return(2)
        self.input(key='notebook_old_attachment_warehouse_4', text='备注', desc='请输入备注', tag='input')
        self.click(key='notebook_old_attachment_warehouse_5', desc='添加物品', tag='span')
        self.refresh_html_source()
        self.click(key='notebook_old_attachment_warehouse_6', desc='请选择品类', tag='input')
        self.down_arrow_return(3)
        self.click(key='notebook_old_attachment_warehouse_7', desc='请选择适用品牌', tag='input')
        self.down_arrow_return(3)
        self.click(key='notebook_old_attachment_warehouse_8', desc='请选择适用型号', tag='input')
        self.down_arrow_return(3)
        self.click(key='notebook_old_attachment_warehouse_9', desc='请选择配件品类', tag='input')
        self.up_arrow_return()
        self.click(key='notebook_old_attachment_warehouse_10', desc='请选择配件名称', tag='input')
        self.down_arrow_return()
        self.click(key='notebook_old_attachment_warehouse_11', desc='请选择渠道', tag='input')
        self.down_arrow_return()
        self.input(key='notebook_old_attachment_warehouse_12', text='1000', desc='请输入具体数量', tag='input')
        self.input(key='notebook_old_attachment_warehouse_13', text='15', desc='请输入采购价格', tag='input')
        self.click(key='notebook_old_attachment_warehouse_14', desc='添加并关闭', tag='span')
        self.refresh_html_source()
        self.click(key='notebook_old_attachment_warehouse_15', desc='确认入库', tag='span')
        self.capture_api_request(url_keyword=self.URL['old_create_purchase_order'])
        return self

    @reset_after_execution
    @doc(a_smartwatches_old_attachment_warehouse)
    def smartwatches_old_attachment_warehouse(self):
        self.menu_manage()
        self.click(key='smartwatches_old_attachment_warehouse_1', desc='新建入库', tag='span')
        self.refresh_html_source()
        self.click(key='smartwatches_old_attachment_warehouse_2', desc='请选择仓库', index=2, tag='input')
        self.down_arrow_return(2)
        self.click(key='smartwatches_old_attachment_warehouse_3', desc='请选择入库人', index=2, tag='input')
        self.down_arrow_return(2)
        self.input(key='smartwatches_old_attachment_warehouse_4', text='备注', desc='请输入备注', tag='input')
        self.click(key='smartwatches_old_attachment_warehouse_5', desc='添加物品', tag='span')
        self.refresh_html_source()
        self.click(key='smartwatches_old_attachment_warehouse_6', desc='请选择品类', tag='input')
        self.down_arrow_return(4)
        self.click(key='smartwatches_old_attachment_warehouse_7', desc='请选择适用品牌', tag='input')
        self.down_arrow_return(4)
        self.click(key='smartwatches_old_attachment_warehouse_8', desc='请选择适用型号', tag='input')
        self.down_arrow_return(4)
        self.click(key='smartwatches_old_attachment_warehouse_9', desc='请选择配件品类', tag='input')
        self.up_arrow_return()
        self.click(key='smartwatches_old_attachment_warehouse_10', desc='请选择配件名称', tag='input')
        self.down_arrow_return()
        self.click(key='smartwatches_old_attachment_warehouse_11', desc='请选择渠道', tag='input')
        self.down_arrow_return()
        self.input(key='smartwatches_old_attachment_warehouse_12', text='1000', desc='请输入具体数量', tag='input')
        self.input(key='smartwatches_old_attachment_warehouse_13', text='15', desc='请输入采购价格', tag='input')
        self.click(key='smartwatches_old_attachment_warehouse_14', desc='添加并关闭', tag='span')
        self.refresh_html_source()
        self.click(key='smartwatches_old_attachment_warehouse_15', desc='确认入库', tag='span')
        self.capture_api_request(url_keyword=self.URL['old_create_purchase_order'])
        return self

    @reset_after_execution
    @doc(a_attachment_old_warehouse_search_item)
    def attachment_old_warehouse_search_item(self):
        self.menu_manage()
        obj = self.pc.attachment_old_warehouse_data(data='a')[0]['articlesNo']
        self.copy(obj)
        ParamCache.cache_object({"articlesNo": obj})
        self.click(key='attachment_old_warehouse_search_item_1', desc='请输入物品编号', tag='input')
        self.affix()
        self.click(key='attachment_old_warehouse_search_item_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['list_of_old_accessories'])
        return self

    @reset_after_execution
    @doc(a_attachment_old_warehouse_search_order)
    def attachment_old_warehouse_search_order(self):
        self.menu_manage()
        obj = self.pc.attachment_old_warehouse_data()[0]['orderNo']
        self.copy(obj)
        ParamCache.cache_object({"orderNo": obj})
        self.click(key='attachment_old_warehouse_search_order_1', desc='请输入入库单号', tag='input')
        self.affix()
        self.click(key='attachment_old_warehouse_search_order_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['list_of_old_accessories'])
        return self

    @reset_after_execution
    @doc(a_attachment_old_warehouse_search_warehouse)
    def attachment_old_warehouse_search_warehouse(self):
        self.menu_manage()
        obj = self.pc.attachment_old_warehouse_data()[0]['orderNo']
        ParamCache.cache_object({"orderNo": obj})
        self.click(key='attachment_old_warehouse_search_warehouse_1', desc='请选择仓库', tag='input')
        self.down_arrow_return(2)
        self.click(key='attachment_old_warehouse_search_warehouse_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['list_of_old_accessories'])
        return self

    @reset_after_execution
    @doc(a_attachment_old_warehouse_search_user)
    def attachment_old_warehouse_search_user(self):
        self.menu_manage()
        obj = self.pc.attachment_old_warehouse_data()[0]['orderNo']
        ParamCache.cache_object({"orderNo": obj})
        self.click(key='attachment_old_warehouse_search_user_1', desc='请选择入库人', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_old_warehouse_search_user_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['list_of_old_accessories'])
        return self

    @reset_after_execution
    @doc(a_attachment_old_warehouse_search_time)
    def attachment_old_warehouse_search_time(self):
        self.menu_manage()
        obj = self.pc.attachment_old_warehouse_data()[0]['orderNo']
        ParamCache.cache_object({"orderNo": obj})
        self.input(key='attachment_old_warehouse_search_time_1', text=self.get_the_date(), desc='开始日期', tag='input')
        self.input(key='attachment_old_warehouse_search_time_2', text=self.get_the_date(days=1), desc='结束日期', tag='input')
        self.click(key='attachment_old_warehouse_search_time_3', desc='请输入物品编号', tag='input')
        self.click(key='attachment_old_warehouse_search_time_4', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['list_of_old_accessories'])
        return self


class AttachmentPickListsPages(CommonPages):
    """配件管理|入库管理|分拣列表"""

    def menu_manage(self):
        """菜单"""
        self.click(key='attachment_menu_1', desc='配件管理', auto=False)
        self.click(key='attachment_menu_2', desc='入库管理', index=2, tag='span', auto=False)
        self.click(key='attachment_menu_11', desc='分拣列表', tag='span', auto=False)
        self.refresh_html_source()
        return self

    @doc(a_attachment_pick_lists_export_all)
    def attachment_pick_lists_export_all(self):
        self.menu_manage()
        self.click(key='attachment_pick_lists_export_all_1', desc='导出全部', tag='span')
        return self

    @reset_after_execution
    @doc(a_attachment_pick_lists_search_logistics)
    def attachment_pick_lists_search_logistics(self):
        self.menu_manage()
        obj = self.pc.attachment_sorting_list_data()[0]['logisticsNo']
        ParamCache.cache_object({"logisticsNo": obj})
        self.click(key='attachment_pick_lists_search_logistics_1', desc='请输入快递单号', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_pick_lists_search_logistics_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['sorting_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_pick_lists_search_item)
    def attachment_pick_lists_search_item(self):
        self.menu_manage()
        obj = self.pc.attachment_new_arrival_data()[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj})
        self.click(key='attachment_pick_lists_search_item_1', desc='请输入物品编号', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_pick_lists_search_item_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['sorting_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_pick_lists_search_business)
    def attachment_pick_lists_search_business(self):
        self.menu_manage()
        obj = self.pc.attachment_new_arrival_data()[0]['businessNo']
        ParamCache.cache_object({"businessNo": obj})
        self.click(key='attachment_pick_lists_search_business_1', desc='请输入业务单号', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_pick_lists_search_business_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['sorting_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_pick_lists_search_status)
    def attachment_pick_lists_search_status(self):
        self.menu_manage()
        obj = self.pc.attachment_sorting_list_data()[0]['logisticsNo']
        ParamCache.cache_object({"logisticsNo": obj})
        self.click(key='attachment_pick_lists_search_status_1', desc='请选择分拣状态', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_pick_lists_search_status_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['sorting_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_pick_lists_search_time)
    def attachment_pick_lists_search_time(self):
        self.menu_manage()
        obj = self.pc.attachment_sorting_list_data()[0]['logisticsNo']
        ParamCache.cache_object({"logisticsNo": obj})
        self.input(key='attachment_pick_lists_search_time_1', text=self.get_the_date(), desc='开始日期', tag='input')
        self.input(key='attachment_pick_lists_search_time_1', text=self.get_the_date(days=1), desc='结束日期', tag='input')
        self.click(key='attachment_pick_lists_search_time_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['sorting_list'])
        return self


class AttachmentPurchaseAddPages(CommonPages):
    """配件管理|配件采购|新增采购单"""

    def menu_manage(self):
        """菜单"""
        self.click(key='attachment_menu_1', desc='配件管理', tag='span', auto=False)
        self.scroll_custom(element='attachment_menu_12')
        self.click(key='attachment_menu_12', desc='配件采购', tag='span', auto=False)
        self.click(key='attachment_menu_13', desc='新增采购单', tag='span', index=2, auto=False)
        self.refresh_html_source()
        return self

    @reset_after_execution
    @doc(a_new_purchase_order_route)
    def new_purchase_order_route(self):
        self.menu_manage()
        self.click(key='new_purchase_order_route_1', desc='请选择供应商名称', tag='input')
        self.down_arrow_return()
        self.click(key='new_purchase_order_route_2', desc='请选择采购人', tag='input')
        self.down_arrow_return()
        self.click(key='new_purchase_order_route_3', desc='请选择付款状态', tag='input')
        self.down_arrow_return()
        self.input(key='new_purchase_order_route_4', text=self.sf, desc='请输入物流单号', tag='input')
        self.input(key='new_purchase_order_route_5', text='12', desc='请输入物流费用', tag='input')
        self.input(key='new_purchase_order_route_6', text='备注', desc='请输入备注', tag='input')
        self.click(key='new_purchase_order_route_7', desc='新增', tag='span')
        self.refresh_html_source()
        self.click(key='new_purchase_order_route_8', desc='请选择品类', tag='input')
        self.down_arrow_return(2)
        self.click(key='new_purchase_order_route_9', desc='请选择品牌', tag='input')
        self.down_arrow_return(2)
        self.click(key='new_purchase_order_route_10', desc='请选择', auto=False)
        self.down_arrow_return(2)
        self.click(key='new_purchase_order_route_11', desc='请选择配件品类', tag='input')
        self.up_arrow_return()
        self.click(key='new_purchase_order_route_12', desc='请选择配件名称', tag='input')
        self.down_arrow_return(2)
        self.click(key='new_purchase_order_route_13', desc='请选择成色', tag='input')
        self.down_arrow_return(2)
        self.click(key='new_purchase_order_route_14', desc='请选择渠道', tag='input')
        self.down_arrow_return(2)
        self.input(key='new_purchase_order_route_15', text='1', desc='请输入具体数量', tag='input')
        self.input(key='new_purchase_order_route_16', text='123', desc='请输入采购价格', tag='input')
        self.click(key='new_purchase_order_route_17', desc='添加并关闭', tag='span')
        self.refresh_html_source()
        self.click(key='new_purchase_order_route_18', desc='确定生成采购单', tag='span')
        self.capture_api_request(url_keyword=self.URL['create_purchase_order'])
        return self

    @reset_after_execution
    @doc(a_new_purchase_order_warehousing)
    def new_purchase_order_warehousing(self):
        self.menu_manage()
        self.click(key='new_purchase_order_warehousing_1', desc='请选择供应商名称', tag='input')
        self.down_arrow_return()
        self.click(key='new_purchase_order_warehousing_2', desc='请选择采购人', tag='input')
        self.down_arrow_return()
        self.click(key='new_purchase_order_warehousing_3', desc='请选择付款状态', tag='input')
        self.down_arrow_return(2)
        self.click(key='new_purchase_order_warehousing_4', desc='请选择付款账户', tag='input')
        self.down_arrow_return()
        self.click(key='new_purchase_order_warehousing_5', desc='请选择包裹状态', tag='input')
        self.down_arrow_return(2)
        self.click(key='new_purchase_order_warehousing_6', desc='请选择仓库', tag='input')
        self.down_arrow_return()
        self.input(key='new_purchase_order_warehousing_7', text=self.sf, desc='请输入物流单号', tag='input')
        self.input(key='new_purchase_order_warehousing_8', text='12', desc='请输入物流费用', tag='input')
        self.input(key='new_purchase_order_warehousing_9', text='备注', desc='请输入备注', tag='input')
        self.click(key='new_purchase_order_warehousing_10', desc='新增', tag='span')
        self.refresh_html_source()
        self.click(key='new_purchase_order_warehousing_11', desc='请选择品类', tag='input')
        self.down_arrow_return()
        self.click(key='new_purchase_order_warehousing_12', desc='请选择品牌', tag='input')
        self.down_arrow_return()
        self.click(key='new_purchase_order_warehousing_13', desc='请选择', auto=False)
        self.down_arrow_return()
        self.click(key='new_purchase_order_warehousing_14', desc='请选择配件品类', tag='input')
        self.up_arrow_return()
        self.click(key='new_purchase_order_warehousing_15', desc='请选择配件名称', tag='input')
        self.down_arrow_return(2)
        self.click(key='new_purchase_order_warehousing_16', desc='请选择成色', tag='input')
        self.down_arrow_return(2)
        self.click(key='new_purchase_order_warehousing_17', desc='请选择渠道', tag='input')
        self.down_arrow_return(2)
        self.input(key='new_purchase_order_warehousing_18', text='1', desc='请输入具体数量', tag='input')
        self.input(key='new_purchase_order_warehousing_19', text='123', desc='请输入采购价格', tag='input')
        self.click(key='new_purchase_order_warehousing_20', desc='添加并关闭', tag='span')
        self.refresh_html_source()
        self.click(key='new_purchase_order_warehousing_21', desc='确定生成采购单', tag='span')
        self.capture_api_request(url_keyword=self.URL['create_purchase_order'])
        return self

    @reset_after_execution
    @doc(a_added_purchase_order_unpaid_in_transit)
    def added_purchase_order_unpaid_in_transit(self):
        self.menu_manage()
        self.click(key='added_purchase_order_unpaid_in_transit_1', desc='请选择供应商名称', tag='input')
        self.down_arrow_return()
        self.click(key='added_purchase_order_unpaid_in_transit_2', desc='请选择采购人', tag='input')
        self.down_arrow_return()
        self.click(key='added_purchase_order_unpaid_in_transit_3', desc='请选择付款状态', tag='input')
        self.down_arrow_return()
        self.input(key='added_purchase_order_unpaid_in_transit_4', text=self.sf, desc='请输入物流单号', tag='input')
        self.input(key='added_purchase_order_unpaid_in_transit_5', text='12', desc='请输入物流费用', tag='input')
        self.input(key='added_purchase_order_unpaid_in_transit_6', text='备注', desc='请输入备注', tag='input')
        self.click(key='added_purchase_order_unpaid_in_transit_7', desc='新增', tag='span')
        self.refresh_html_source()
        self.click(key='added_purchase_order_unpaid_in_transit_8', desc='请选择品类', tag='input')
        self.down_arrow_return(3)
        self.click(key='added_purchase_order_unpaid_in_transit_9', desc='请选择品牌', tag='input')
        self.down_arrow_return(3)
        self.click(key='added_purchase_order_unpaid_in_transit_10', desc='请选择', auto=False)
        self.down_arrow_return(3)
        self.click(key='added_purchase_order_unpaid_in_transit_11', desc='请选择配件品类', tag='input')
        self.up_arrow_return()
        self.click(key='added_purchase_order_unpaid_in_transit_12', desc='请选择配件名称', tag='input')
        self.down_arrow_return(2)
        self.click(key='added_purchase_order_unpaid_in_transit_13', desc='请选择成色', tag='input')
        self.down_arrow_return(2)
        self.click(key='added_purchase_order_unpaid_in_transit_14', desc='请选择渠道', tag='input')
        self.down_arrow_return(2)
        self.input(key='added_purchase_order_unpaid_in_transit_15', text='1', desc='请输入具体数量', tag='input')
        self.input(key='added_purchase_order_unpaid_in_transit_16', text='123', desc='请输入采购价格', tag='input')
        self.click(key='added_purchase_order_unpaid_in_transit_17', desc='添加并关闭', tag='span')
        self.refresh_html_source()
        self.click(key='added_purchase_order_unpaid_in_transit_18', desc='确定生成采购单', tag='span')
        self.capture_api_request(url_keyword=self.URL['create_purchase_order'])
        return self

    @reset_after_execution
    @doc(a_attachment_new_purchase_order_payment)
    def attachment_new_purchase_order_payment(self):
        self.menu_manage()
        self.click(key='attachment_new_purchase_order_payment_1', desc='请选择供应商名称', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_new_purchase_order_payment_2', desc='请选择采购人', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_new_purchase_order_payment_3', desc='请选择付款状态', tag='input')
        self.down_arrow_return(2)
        self.click(key='attachment_new_purchase_order_payment_4', desc='请选择付款账户', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_new_purchase_order_payment_5', desc='请选择包裹状态', tag='input')
        self.down_arrow_return(2)
        self.click(key='attachment_new_purchase_order_payment_6', desc='请选择仓库', tag='input')
        self.down_arrow_return()
        self.input(key='attachment_new_purchase_order_payment_7', text=self.sf, desc='请输入物流单号', tag='input')
        self.input(key='attachment_new_purchase_order_payment_8', text='12', desc='请输入物流费用', tag='input')
        self.input(key='attachment_new_purchase_order_payment_9', text='备注', desc='请输入备注', tag='input')
        self.click(key='attachment_new_purchase_order_payment_10', desc='新增', tag='span')
        self.refresh_html_source()
        self.click(key='attachment_new_purchase_order_payment_11', desc='请选择品类', tag='input')
        self.down_arrow_return(4)
        self.click(key='attachment_new_purchase_order_payment_12', desc='请选择品牌', tag='input')
        self.down_arrow_return(4)
        self.click(key='attachment_new_purchase_order_payment_13', desc='请选择', auto=False)
        self.down_arrow_return(4)
        self.click(key='attachment_new_purchase_order_payment_14', desc='请选择配件品类', tag='input')
        self.up_arrow_return()
        self.click(key='attachment_new_purchase_order_payment_15', desc='请选择配件名称', tag='input')
        self.down_arrow_return(2)
        self.click(key='attachment_new_purchase_order_payment_16', desc='请选择成色', tag='input')
        self.down_arrow_return(2)
        self.click(key='attachment_new_purchase_order_payment_17', desc='请选择渠道', tag='input')
        self.down_arrow_return(2)
        self.input(key='attachment_new_purchase_order_payment_18', text='1', desc='请输入具体数量', tag='input')
        self.input(key='attachment_new_purchase_order_payment_19', text='123', desc='请输入采购价格', tag='input')
        self.click(key='attachment_new_purchase_order_payment_20', desc='添加并关闭', tag='span')
        self.refresh_html_source()
        self.click(key='attachment_new_purchase_order_payment_21', desc='确定生成采购单', tag='span')
        self.capture_api_request(url_keyword=self.URL['create_purchase_order'])
        return self

    @reset_after_execution
    @doc(a_generate_purchase_orders_in_bulk)
    def generate_purchase_orders_in_bulk(self):
        self.menu_manage()
        self.click(key='generate_purchase_orders_in_bulk_1', desc='请选择供应商名称', tag='input')
        self.down_arrow_return()
        self.click(key='generate_purchase_orders_in_bulk_2', desc='请选择采购人', tag='input')
        self.down_arrow_return()
        self.click(key='generate_purchase_orders_in_bulk_3', desc='请选择付款状态', tag='input')
        self.down_arrow_return()
        self.input(key='generate_purchase_orders_in_bulk_4', text=self.sf, desc='请输入物流单号', tag='input')
        self.input(key='generate_purchase_orders_in_bulk_5', text='12', desc='请输入物流费用', tag='input')
        self.input(key='generate_purchase_orders_in_bulk_6', text='备注', desc='请输入备注', tag='input')
        self.click(key='generate_purchase_orders_in_bulk_7', desc='新增', tag='span')
        self.refresh_html_source()
        self.click(key='generate_purchase_orders_in_bulk_8', desc='请选择品类', tag='input')
        self.down_arrow_return(2)
        self.click(key='generate_purchase_orders_in_bulk_9', desc='请选择品牌', tag='input')
        self.down_arrow_return(2)
        self.click(key='generate_purchase_orders_in_bulk_10', desc='请选择', auto=False)
        self.down_arrow_return(2)
        self.click(key='generate_purchase_orders_in_bulk_11', desc='请选择配件品类', tag='input')
        self.up_arrow_return()
        self.click(key='generate_purchase_orders_in_bulk_12', desc='请选择配件名称', tag='input')
        self.down_arrow_return(2)
        self.click(key='generate_purchase_orders_in_bulk_13', desc='请选择成色', tag='input')
        self.down_arrow_return(2)
        self.click(key='generate_purchase_orders_in_bulk_14', desc='请选择渠道', tag='input')
        self.down_arrow_return(2)
        self.input(key='generate_purchase_orders_in_bulk_15', text='1000', desc='请输入具体数量', tag='input')
        self.input(key='generate_purchase_orders_in_bulk_16', text='12', desc='请输入采购价格', tag='input')
        self.click(key='generate_purchase_orders_in_bulk_17', desc='添加并关闭', tag='span')
        self.refresh_html_source()
        self.click(key='generate_purchase_orders_in_bulk_18', desc='确定生成采购单', tag='span')
        self.capture_api_request(url_keyword=self.URL['create_purchase_order'])
        return self

    @reset_after_execution
    @doc(a_add_purchase_orders_in_bulk)
    def add_purchase_orders_in_bulk(self):
        self.menu_manage()
        self.click(key='add_purchase_orders_in_bulk_1', desc='请选择供应商名称', tag='input')
        self.down_arrow_return()
        self.click(key='add_purchase_orders_in_bulk_2', desc='请选择采购人', tag='input')
        self.down_arrow_return()
        self.click(key='add_purchase_orders_in_bulk_3', desc='请选择付款状态', tag='input')
        self.down_arrow_return()
        self.input(key='add_purchase_orders_in_bulk_4', text=self.sf, desc='请输入物流单号', tag='input')
        self.input(key='add_purchase_orders_in_bulk_5', text='12', desc='请输入物流费用', tag='input')
        self.input(key='add_purchase_orders_in_bulk_6', text='备注', desc='请输入备注', tag='input')
        self.click(key='add_purchase_orders_in_bulk_7', desc='新增', tag='span')
        self.refresh_html_source()
        self.click(key='add_purchase_orders_in_bulk_8', desc='请选择品类', tag='input')
        self.down_arrow_return(2)
        self.click(key='add_purchase_orders_in_bulk_9', desc='请选择品牌', tag='input')
        self.down_arrow_return(2)
        self.click(key='add_purchase_orders_in_bulk_10', desc='请选择', auto=False)
        self.down_arrow_return(2)
        self.click(key='add_purchase_orders_in_bulk_11', desc='请选择配件品类', tag='input')
        self.up_arrow_return()
        self.click(key='add_purchase_orders_in_bulk_12', desc='请选择配件名称', tag='input')
        self.down_arrow_return(2)
        self.click(key='add_purchase_orders_in_bulk_13', desc='请选择成色', tag='input')
        self.down_arrow_return(2)
        self.click(key='add_purchase_orders_in_bulk_14', desc='请选择渠道', tag='input')
        self.down_arrow_return(2)
        self.input(key='add_purchase_orders_in_bulk_15', text='1000', desc='请输入具体数量', tag='input')
        self.input(key='add_purchase_orders_in_bulk_16', text='12', desc='请输入采购价格', tag='input')
        self.click(key='add_purchase_orders_in_bulk_17', desc='＋图标', tag='i', auto=False)
        self.refresh_html_source()
        self.click(key='add_purchase_orders_in_bulk_18', desc='请选择配件品类', tag='input', index=2)
        self.up_arrow_return()
        self.click(key='add_purchase_orders_in_bulk_19', desc='请选择配件名称', tag='input', index=2)
        self.down_arrow_return(2)
        self.click(key='add_purchase_orders_in_bulk_20', desc='请选择成色', tag='input', index=2)
        self.down_arrow_return(2)
        self.click(key='add_purchase_orders_in_bulk_21', desc='请选择渠道', tag='input', index=2)
        self.down_arrow_return(2)
        self.click(key='add_purchase_orders_in_bulk_22', desc='添加并关闭', tag='span')
        self.refresh_html_source()
        self.click(key='add_purchase_orders_in_bulk_23', desc='确定生成采购单', tag='span')
        self.capture_api_request(url_keyword=self.URL['create_purchase_order'])
        return self


class AttachmentPurchaseListPages(CommonPages):
    """配件管理|配件采购|采购列表"""

    def menu_manage(self):
        """菜单"""
        self.click(key='attachment_menu_1', desc='配件管理', tag='span', auto=False)
        self.scroll_custom(element='attachment_menu_12')
        self.click(key='attachment_menu_12', desc='配件采购', tag='span', auto=False)
        self.click(key='attachment_menu_14', desc='采购列表', tag='span', auto=False)
        self.refresh_html_source()
        return self

    @reset_after_execution
    @doc(a_refund_after_purchase_express)
    def refund_after_purchase_express(self):
        self.menu_manage()
        self.click(key='refund_after_purchase_express_1', desc='搜索', tag='span')
        self.tab_return(5)
        self.click(key='refund_after_purchase_express_2', desc='采购售后', tag='span')
        self.refresh_html_source()
        self.click(key='refund_after_purchase_express_3', desc='请选择售后类型', tag='input')
        self.down_arrow_return()
        self.refresh_html_source()
        self.click(key='refund_after_purchase_express_4', desc='快递易图标开关', auto=False)
        self.refresh_html_source()
        self.click(key='refund_after_purchase_express_5', desc='计算运费', tag='span')
        self.click(key='refund_after_purchase_express_6', desc='确定', index=3, tag='span')
        self.capture_api_request(url_keyword=self.URL['procurement_after_sales'])
        return self

    @reset_after_execution
    @doc(a_refund_after_purchase)
    def refund_after_purchase(self):
        self.menu_manage()
        self.click(key='refund_after_purchase_1', desc='搜索', tag='span')
        self.tab_return(5)
        self.click(key='refund_after_purchase_2', desc='采购售后', tag='span')
        self.refresh_html_source()
        self.click(key='refund_after_purchase_3', desc='请选择售后类型', tag='input')
        self.down_arrow_return()
        self.input(key='refund_after_purchase_4', text=self.sf, desc='请填写物流单号', tag='input')
        self.input(key='refund_after_purchase_5', text='12', desc='请填写物流费用', tag='input')
        self.input(key='refund_after_purchase_6', text='备注', desc='请填写备注', tag='input')
        self.click(key='refund_after_purchase_7', desc='确定', index=2, tag='span')
        self.capture_api_request(url_keyword=self.URL['procurement_after_sales'])
        return self

    @reset_after_execution
    @doc(a_purchase_sale_refund)
    def purchase_sale_refund(self):
        self.menu_manage()
        self.click(key='purchase_sale_refund_1', desc='搜索', tag='span')
        self.tab_return(5)
        self.click(key='purchase_sale_refund_2', desc='采购售后', tag='span')
        self.refresh_html_source()
        self.click(key='purchase_sale_refund_3', desc='请选择售后类型', tag='input')
        self.down_arrow_return(2)
        self.refresh_html_source()
        self.input(key='purchase_sale_refund_4', text='3', desc='请输入退款金额', tag='input')
        self.click(key='purchase_sale_refund_5', desc='确定', index=2, tag='span')
        self.capture_api_request(url_keyword=self.URL['procurement_after_sales'])
        return self

    @reset_after_execution
    @doc(a_refund_after_purchase_add_item)
    def refund_after_purchase_add_item(self):
        self.menu_manage()
        self.copy(self.pc.attachment_inventory_list_data(i=2)[0]['articlesNo'])
        self.click(key='refund_after_purchase_add_item_1', desc='采购售后', tag='span')
        self.refresh_html_source()
        self.click(key='refund_after_purchase_add_item_2', desc='请选择售后类型', tag='input')
        self.down_arrow_return()
        self.refresh_html_source()
        self.click(key='refund_after_purchase_add_item_3', desc='请选择供应商', tag='input')
        self.down_arrow_return()
        self.input(key='refund_after_purchase_add_item_4', text=self.sf, desc='请填写物流单号', tag='input')
        self.input(key='refund_after_purchase_add_item_5', text='10', desc='请填写物流费用', tag='input')
        self.click(key='refund_after_purchase_add_item_6', desc='请输入物品编号', tag='input')
        self.affix()
        self.click(key='refund_after_purchase_add_item_7', desc='添加', tag='span')
        self.click(key='refund_after_purchase_add_item_8', desc='确定', index=2, tag='span')
        return self

    @reset_after_execution
    @doc(a_all_amount_refund_difference)
    def all_amount_refund_difference(self):
        self.menu_manage()
        self.click(key='all_amount_refund_difference_1', desc='搜索', tag='span')
        self.tab_return(5)
        self.click(key='all_amount_refund_difference_2', desc='采购售后', tag='span')
        self.refresh_html_source()
        self.click(key='all_amount_refund_difference_3', desc='请选择售后类型', tag='input')
        self.down_arrow_return(2)
        self.refresh_html_source()
        self.input(key='all_amount_refund_difference_4', text='9999999', desc='请输入退款金额', tag='input')
        self.click(key='all_amount_refund_difference_5', desc='确定', index=2, tag='span')
        self.capture_api_request(url_keyword=self.URL['procurement_after_sales'])
        return self

    @reset_after_execution
    @doc(a_details_of_the_spare_parts_purchase_list)
    def details_of_the_spare_parts_purchase_list(self):
        obj = self.pc.attachment_purchase_list_data(data='a')[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj})
        self.menu_manage()
        self.click(key='details_of_the_spare_parts_purchase_list_1', desc='采购单号超链接', tag='span', auto=False)
        self.capture_api_request(url_keyword=self.URL['purchase_detail'])
        return self

    @reset_after_execution
    @doc(a_attachment_purchase_list_search_order)
    def attachment_purchase_list_search_order(self):
        obj = self.pc.attachment_purchase_list_data()[0]['orderNo']
        self.copy(obj)
        ParamCache.cache_object({"orderNo": obj})
        self.menu_manage()
        self.click(key='attachment_purchase_list_search_order_1', desc='请输入采购单号', tag='input')
        self.affix()
        self.click(key='attachment_purchase_list_search_order_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['purchase_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_purchase_list_search_suppliers)
    def attachment_purchase_list_search_suppliers(self):
        obj = self.pc.attachment_purchase_list_data()[0]['orderNo']
        ParamCache.cache_object({"orderNo": obj})
        self.menu_manage()
        self.click(key='attachment_purchase_list_search_suppliers_1', desc='请选择采购供应商', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_purchase_list_search_suppliers_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['purchase_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_purchase_list_search_people)
    def attachment_purchase_list_search_people(self):
        obj = self.pc.attachment_purchase_list_data()[0]['orderNo']
        ParamCache.cache_object({"orderNo": obj})
        self.menu_manage()
        self.click(key='attachment_purchase_list_search_people_1', desc='请选择采购人', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_purchase_list_search_people_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['purchase_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_purchase_list_search_time)
    def attachment_purchase_list_search_time(self):
        obj = self.pc.attachment_purchase_list_data()[0]['orderNo']
        ParamCache.cache_object({"orderNo": obj})
        self.menu_manage()
        self.input(key='attachment_purchase_list_search_time_1', text=self.get_the_date(), desc='开始时间', tag='input')
        self.input(key='attachment_purchase_list_search_time_2', text=self.get_the_date(days=1), desc='结束时间', tag='input')
        self.click(key='attachment_purchase_list_search_time_3', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['purchase_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_purchase_list_search_status)
    def attachment_purchase_list_search_status(self):
        obj = self.pc.attachment_purchase_list_data()[0]['orderNo']
        ParamCache.cache_object({"orderNo": obj})
        self.menu_manage()
        self.click(key='attachment_purchase_list_search_status_1', desc='请选择采购单状态', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_purchase_list_search_status_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['purchase_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_purchase_list_search_payment)
    def attachment_purchase_list_search_payment(self):
        obj = self.pc.attachment_purchase_list_data()[0]['orderNo']
        ParamCache.cache_object({"orderNo": obj})
        self.menu_manage()
        self.click(key='attachment_purchase_list_search_payment_1', desc='请选择付款状态', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_purchase_list_search_payment_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['purchase_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_purchase_list_search_logistics)
    def attachment_purchase_list_search_logistics(self):
        obj = self.pc.attachment_purchase_list_data()[0]['logisticsNo']
        self.copy(obj)
        ParamCache.cache_object({"logisticsNo": obj})
        self.menu_manage()
        self.click(key='attachment_purchase_list_search_status_1', desc='请输入物流单号', tag='input')
        self.affix()
        self.click(key='attachment_purchase_list_search_status_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['purchase_list'])
        return self


class AttachmentReceiveItemsPages(CommonPages):
    """配件管理|移交接收管理|接收物品"""

    def menu_manage(self):
        """菜单"""
        self.click(key='attachment_menu_1', desc='配件管理', tag='span', auto=False)
        self.click(key='attachment_menu_4', desc='移交接收管理', tag='span', index=2, auto=False)
        self.click(key='attachment_menu_15', desc='接收物品', tag='span', index=2, auto=False)
        self.refresh_html_source()
        return self

    @reset_after_execution
    @doc(a_item_inventory_accessory_item_receipt)
    def item_inventory_accessory_item_receipt(self):
        self.menu_manage()
        self.click(key='item_inventory_accessory_item_receipt_1', desc='搜索', tag='span')
        self.tab_return(5)
        self.click(key='item_inventory_accessory_item_receipt_2', desc='接收', tag='span')
        self.refresh_html_source()
        self.click(key='item_inventory_accessory_item_receipt_3', desc='确定', index=2, tag='span')
        self.capture_api_request(url_keyword=self.URL['accessory_receive_items'])
        return self

    @reset_after_execution
    @doc(a_handover_orders_received_in_batches)
    def handover_orders_received_in_batches(self):
        self.menu_manage()
        self.click(key='handover_orders_received_in_batches_1', desc='搜索', tag='span')
        self.tab_return(5)
        self.click(key='handover_orders_received_in_batches_2', desc='接收', tag='span')
        self.refresh_html_source()
        self.click(key='handover_orders_received_in_batches_3', desc='确定', index=2, tag='span')
        self.capture_api_request(url_keyword=self.URL['accessory_receive_items'])
        return self

    @reset_after_execution
    @doc(a_scan_the_code_to_receive_accurately)
    def scan_the_code_to_receive_accurately(self):
        self.menu_manage()
        self.copy(self.pc.attachment_inventory_list_data(i=2)[0]['articlesNo'])
        self.click(key='scan_the_code_to_receive_accurately_1', desc='扫码精确接收', tag='span')
        self.refresh_html_source()
        self.click(key='scan_the_code_to_receive_accurately_2', desc='请输入物品编号', tag='input')
        self.affix_carriage_return()
        self.tab_return(2)
        self.click(key='scan_the_code_to_receive_accurately_3', desc='接收', index=2, tag='span')
        return self

    @reset_after_execution
    @doc(a_handover_export)
    def handover_export(self):
        self.menu_manage()
        self.click(key='handover_export_1', desc='移交单接收', tag='div')
        self.click(key='handover_export_2', desc='导出', tag='span')
        return self

    @reset_after_execution
    @doc(a_attachment_receive_item_search_item)
    def attachment_receive_item_search_item(self):
        self.menu_manage()
        obj = self.pc.attachment_receive_items_data(data='a')[0]['articlesNo']
        self.copy(obj)
        ParamCache.cache_object({"articlesNo": obj})
        self.click(key='attachment_receive_item_search_item_1', desc='请输入编号/IMEI', tag='input')
        self.affix()
        self.click(key='attachment_receive_item_search_item_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['items_to_be_received'])
        return self

    @reset_after_execution
    @doc(a_attachment_receive_item_search_category)
    def attachment_receive_item_search_category(self):
        self.menu_manage()
        obj = self.pc.attachment_receive_items_data(data='a')[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj})
        self.click(key='attachment_receive_item_search_category_1', desc='请选择品类', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_receive_item_search_category_2', desc='请选择品牌', tag='input')
        self.down_arrow_return(2)
        self.click(key='attachment_receive_item_search_category_3', desc='请选择型号', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_receive_item_search_category_4', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['items_to_be_received'])
        return self

    @reset_after_execution
    @doc(a_attachment_receive_item_search_person)
    def attachment_receive_item_search_person(self):
        self.menu_manage()
        obj = self.pc.attachment_receive_items_data(data='a')[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj})
        self.click(key='attachment_receive_item_search_person_1', desc='请选择移交人', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_receive_item_search_person_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['items_to_be_received'])
        return self

    @reset_after_execution
    @doc(a_attachment_receive_item_search_accept)
    def attachment_receive_item_search_accept(self):
        self.menu_manage()
        obj = self.pc.attachment_receive_items_data(data='a')[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj})
        self.click(key='attachment_receive_item_search_accept_1', desc='请选择接收人', tag='input')
        self.down_arrow_return(2)
        self.click(key='attachment_receive_item_search_accept_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['items_to_be_received'])
        return self

    @reset_after_execution
    @doc(a_attachment_receive_item_search_time)
    def attachment_receive_item_search_time(self):
        self.menu_manage()
        obj = self.pc.attachment_receive_items_data(data='a')[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj})
        self.input(key='attachment_receive_item_search_time_1', text=self.get_the_date(), desc='开始日期', tag='input')
        self.input(key='attachment_receive_item_search_time_2', text=self.get_the_date(days=1), desc='结束日期', tag='input')
        self.click(key='attachment_receive_item_search_time_3', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['items_to_be_received'])
        return self

    @reset_after_execution
    @doc(a_attachment_receive_item_search_order)
    def attachment_receive_item_search_order(self):
        self.menu_manage()
        obj = self.pc.attachment_receive_items_data(data='a')[0]['orderNo']
        self.copy(obj)
        ParamCache.cache_object({"orderNo": obj})
        self.click(key='attachment_receive_item_search_order_1', desc='请输入移交单号', tag='input')
        self.affix()
        self.click(key='attachment_receive_item_search_order_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['items_to_be_received'])
        return self

    @reset_after_execution
    @doc(a_attachment_receive_item_search_item_no)
    def attachment_receive_item_search_item_no(self):
        self.menu_manage()
        obj = self.pc.attachment_receive_items_data(data='a')[0]['articlesNo']
        self.copy(obj)
        ParamCache.cache_object({"articlesNo": obj})
        self.click(key='attachment_receive_item_search_item_no_1', desc='请输入编号/IMEI', tag='input')
        self.affix()
        self.click(key='attachment_receive_item_search_item_no_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['receive_items'])
        return self

    @reset_after_execution
    @doc(a_attachment_receive_item_search_order_no)
    def attachment_receive_item_search_order_no(self):
        self.menu_manage()
        obj = self.pc.attachment_receive_items_data()[0]['orderNo']
        self.copy(obj)
        ParamCache.cache_object({"orderNo": obj})
        self.click(key='attachment_receive_item_search_order_no_1', desc='请输入移交单号', tag='input')
        self.affix()
        self.click(key='attachment_receive_item_search_order_no_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['receive_items'])
        return self

    @reset_after_execution
    @doc(a_attachment_receive_item_search_status)
    def attachment_receive_item_search_status(self):
        self.menu_manage()
        obj = self.pc.attachment_receive_items_data()[0]['orderNo']
        ParamCache.cache_object({"orderNo": obj})
        self.click(key='attachment_receive_item_search_status_1', desc='请选择移交单状态', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_receive_item_search_status_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['receive_items'])
        return self

    @reset_after_execution
    @doc(a_attachment_receive_item_search_transfer_person)
    def attachment_receive_item_search_transfer_person(self):
        self.menu_manage()
        obj = self.pc.attachment_receive_items_data()[0]['orderNo']
        ParamCache.cache_object({"orderNo": obj})
        self.click(key='attachment_receive_item_search_transfer_person_1', desc='请选择移交人', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_receive_item_search_transfer_person_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['receive_items'])
        return self

    @reset_after_execution
    @doc(a_attachment_receive_item_search_recipient)
    def attachment_receive_item_search_recipient(self):
        self.menu_manage()
        obj = self.pc.attachment_receive_items_data()[0]['orderNo']
        ParamCache.cache_object({"orderNo": obj})
        self.click(key='attachment_receive_item_search_recipient_1', desc='请选择接收人', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_receive_item_search_recipient_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['receive_items'])
        return self

    @reset_after_execution
    @doc(a_attachment_receive_item_search_transfer_time)
    def attachment_receive_item_search_transfer_time(self):
        self.menu_manage()
        obj = self.pc.attachment_receive_items_data()[0]['orderNo']
        ParamCache.cache_object({"orderNo": obj})
        self.input(key='attachment_receive_item_search_transfer_time_1', text=self.get_the_date(), desc='开始日期', tag='input')
        self.input(key='attachment_receive_item_search_transfer_time_2', text=self.get_the_date(days=1), desc='结束日期', tag='input')
        self.click(key='attachment_receive_item_search_transfer_time_3', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['receive_items'])
        return self


class AttachmentSalesListPages(CommonPages):
    """配件管理|配件销售|销售列表"""

    def menu_manage(self):
        """菜单"""
        self.click(key='attachment_menu_1', desc='配件管理', auto=False, tag='span')
        self.click(key='attachment_menu_16', desc='配件销售', tag='span', auto=False)
        self.click(key='attachment_menu_17', desc='销售列表', tag='span', auto=False)
        self.refresh_html_source()
        return self

    @reset_after_execution
    @doc(a_accessory_sales_express_easy)
    def accessory_sales_express_easy(self):
        self.menu_manage()
        self.copy(self.pc.attachment_inventory_list_data(i=2)[0]['articlesNo'])
        self.click(key='accessory_sales_express_easy_1', desc='配件销售', index=2, tag='span')
        self.refresh_html_source()
        self.click(key='accessory_sales_express_easy_2', desc='请输入物品编号', tag='input')
        self.affix()
        self.click(key='accessory_sales_express_easy_3', desc='添加', tag='span')
        self.refresh_html_source()
        self.click(key='accessory_sales_express_easy_4', desc='请选择客户', index=2, tag='input')
        self.down_arrow_return(2)
        self.click(key='accessory_sales_express_easy_5', desc='未收款', index=2, tag='span')
        self.click(key='accessory_sales_express_easy_6', desc='请选择收款账户', tag='input')
        self.down_arrow_return(2)
        self.click(key='accessory_sales_express_easy_7', desc='快递易图标开关', auto=False)
        self.refresh_html_source()
        self.click(key='accessory_sales_express_easy_8', desc='计算运费', tag='span')
        self.input(key='accessory_sales_express_easy_9', text='12', desc='请输入销售金额', tag='input')
        self.scroll_custom(element='accessory_sales_express_easy_10')
        self.click(key='accessory_sales_express_easy_10', desc='确定', index=3, tag='span')
        self.capture_api_request(url_keyword=self.URL['accessory_sales'])
        return self

    @reset_after_execution
    @doc(a_accessory_sales_express_easy_maximum)
    def accessory_sales_express_easy_maximum(self):
        self.menu_manage()
        self.copy(self.pc.attachment_inventory_list_data(i=2)[0]['articlesNo'])
        self.click(key='accessory_sales_express_easy_maximum_1', desc='配件销售', index=2, tag='span')
        self.refresh_html_source()
        self.click(key='accessory_sales_express_easy_maximum_2', desc='请输入物品编号', tag='input')
        self.affix()
        self.click(key='accessory_sales_express_easy_maximum_3', desc='添加', tag='span')
        self.refresh_html_source()
        self.click(key='accessory_sales_express_easy_maximum_4', desc='请选择客户', index=2, tag='input')
        self.down_arrow_return(2)
        self.click(key='accessory_sales_express_easy_maximum_5', desc='未收款', index=2, tag='span')
        self.click(key='accessory_sales_express_easy_maximum_6', desc='请选择收款账户', tag='input')
        self.down_arrow_return()
        self.click(key='accessory_sales_express_easy_maximum_7', desc='快递易图标开关', auto=False)
        self.refresh_html_source()
        self.click(key='accessory_sales_express_easy_maximum_8', desc='计算运费', tag='span')
        self.input(key='accessory_sales_express_easy_maximum_9', text='999999', desc='请输入销售金额', tag='input')
        self.scroll_custom(element='accessory_sales_express_easy_maximum_10')
        self.click(key='accessory_sales_express_easy_maximum_10', desc='确定', index=3, tag='span')
        self.capture_api_request(url_keyword=self.URL['accessory_sales'])
        return self

    @reset_after_execution
    @doc(a_uncollected_partial_sales_amount)
    def uncollected_partial_sales_amount(self):
        self.menu_manage()
        self.copy(self.pc.attachment_inventory_list_data(i=2)[0]['articlesNo'])
        self.click(key='uncollected_partial_sales_amount_1', desc='配件销售', index=2, tag='span')
        self.refresh_html_source()
        self.click(key='uncollected_partial_sales_amount_2', desc='请输入物品编号', tag='input')
        self.affix()
        self.click(key='uncollected_partial_sales_amount_3', desc='添加', tag='span')
        self.refresh_html_source()
        self.click(key='uncollected_partial_sales_amount_4', desc='请选择客户', index=2, tag='input')
        self.down_arrow_return(2)
        self.click(key='uncollected_partial_sales_amount_5', desc='未收款', index=2, tag='span')
        self.click(key='uncollected_partial_sales_amount_6', desc='请选择收款账户', tag='input')
        self.down_arrow_return()
        self.input(key='uncollected_partial_sales_amount_7', text=self.sf, desc='请填写物流单号', tag='input')
        self.input(key='uncollected_partial_sales_amount_8', text='12', desc='请填写物流费用', tag='input')
        self.input(key='uncollected_partial_sales_amount_9', text='备注', desc='请填写备注', tag='input')
        self.input(key='uncollected_partial_sales_amount_10', text='124', desc='请输入销售金额', tag='input')
        self.click(key='uncollected_partial_sales_amount_11', desc='确定', index=3, tag='span')
        self.capture_api_request(url_keyword=self.URL['accessory_sales'])
        return self

    @reset_after_execution
    @doc(a_accessories_sales_express_received_payment)
    def accessories_sales_express_received_payment(self):
        self.menu_manage()
        self.copy(self.pc.attachment_inventory_list_data(i=2)[0]['articlesNo'])
        self.click(key='accessories_sales_express_received_payment_1', desc='配件销售', index=2, tag='span')
        self.refresh_html_source()
        self.click(key='accessories_sales_express_received_payment_2', desc='请输入物品编号', tag='input')
        self.affix()
        self.click(key='accessories_sales_express_received_payment_3', desc='添加', tag='span')
        self.refresh_html_source()
        self.click(key='accessories_sales_express_received_payment_4', desc='请选择客户', index=2, tag='input')
        self.down_arrow_return(2)
        self.click(key='accessories_sales_express_received_payment_5', desc='已收款', index=2, tag='span')
        self.click(key='accessories_sales_express_received_payment_6', desc='请选择收款账户', tag='input')
        self.down_arrow_return()
        self.input(key='accessories_sales_express_received_payment_7', text=self.sf, desc='请填写物流单号', tag='input')
        self.input(key='accessories_sales_express_received_payment_8', text='12', desc='请填写物流费用', tag='input')
        self.input(key='accessories_sales_express_received_payment_9', text='备注', desc='请填写备注', tag='input')
        self.input(key='accessories_sales_express_received_payment_10', text='124', desc='请输入销售金额', tag='input')
        self.click(key='accessories_sales_express_received_payment_11', desc='确定', index=3, tag='span')
        self.capture_api_request(url_keyword=self.URL['accessory_sales'])
        return self

    @reset_after_execution
    @doc(a_sales_after_sale_refund_not_received)
    def sales_after_sale_refund_not_received(self):
        self.menu_manage()
        self.click(key='sales_after_sale_refund_not_received_1', desc='搜索', tag='span')
        self.tab_return(6)
        self.click(key='sales_after_sale_refund_not_received_2', desc='销售售后', tag='span')
        self.refresh_html_source()
        self.click(key='sales_after_sale_refund_not_received_3', desc='请选择售后类型', tag='input')
        self.down_arrow_return()
        self.refresh_html_source()
        self.input(key='sales_after_sale_refund_not_received_4', text=self.sf, desc='请填写物流单号', tag='input')
        self.input(key='sales_after_sale_refund_not_received_5', text='12', desc='请填写物流费用', tag='input')
        self.click(key='sales_after_sale_refund_not_received_6', desc='确定', index=4, tag='span')
        self.capture_api_request(url_keyword=self.URL['after_sales_of_accessories'])
        return self

    @reset_after_execution
    @doc(a_sales_after_sale_refund_warehouse)
    def sales_after_sale_refund_warehouse(self):
        self.menu_manage()
        self.click(key='sales_after_sale_refund_warehouse_1', desc='搜索', tag='span')
        self.tab_return(6)
        self.click(key='sales_after_sale_refund_warehouse_2', desc='销售售后', tag='span')
        self.refresh_html_source()
        self.click(key='sales_after_sale_refund_warehouse_3', desc='请选择售后类型', tag='input')
        self.down_arrow_return()
        self.refresh_html_source()
        self.click(key='sales_after_sale_refund_warehouse_4', desc='已收货', tag='span')
        self.click(key='sales_after_sale_refund_warehouse_5', desc='请选择仓库', tag='input')
        self.down_arrow_return()
        self.input(key='sales_after_sale_refund_warehouse_6', text='备注', desc='请填写备注', index=2, tag='input')
        self.click(key='sales_after_sale_refund_warehouse_7', desc='确定', index=4, tag='span')
        self.capture_api_request(url_keyword=self.URL['after_sales_of_accessories'])
        return self

    @reset_after_execution
    @doc(a_sales_after_refund_the_price_difference)
    def sales_after_refund_the_price_difference(self):
        self.menu_manage()
        self.click(key='sales_after_refund_the_price_difference_1', desc='搜索', tag='span')
        self.tab_return(6)
        self.click(key='sales_after_refund_the_price_difference_2', desc='销售售后', tag='span')
        self.refresh_html_source()
        self.click(key='sales_after_refund_the_price_difference_3', desc='请选择售后类型', tag='input')
        self.up_arrow_return()
        self.refresh_html_source()
        self.input(key='sales_after_refund_the_price_difference_4', text='5', desc='请输入退款金额', tag='input')
        self.click(key='sales_after_refund_the_price_difference_5', desc='确定', index=4, tag='span')
        self.capture_api_request(url_keyword=self.URL['after_sales_of_accessories'])
        return self

    @reset_after_execution
    @doc(a_the_full_amount_will_be_refunded_the_difference)
    def the_full_amount_will_be_refunded_the_difference(self):
        self.menu_manage()
        self.click(key='the_full_amount_will_be_refunded_the_difference_1', desc='搜索', tag='span')
        self.tab_return(6)
        self.click(key='the_full_amount_will_be_refunded_the_difference_2', desc='销售售后', tag='span')
        self.refresh_html_source()
        self.click(key='the_full_amount_will_be_refunded_the_difference_3', desc='请选择售后类型', tag='input')
        self.up_arrow_return()
        self.refresh_html_source()
        self.input(key='the_full_amount_will_be_refunded_the_difference_4', text='999999', desc='请输入退款金额', tag='input')
        self.click(key='the_full_amount_will_be_refunded_the_difference_5', desc='确定', index=4, tag='span')
        self.capture_api_request(url_keyword=self.URL['after_sales_of_accessories'])
        return self

    @reset_after_execution
    @doc(a_attachment_sales_list_search_order)
    def attachment_sales_list_search_order(self):
        self.menu_manage()
        obj = self.pc.attachment_sales_list_data()[0]['orderNo']
        self.copy(obj)
        ParamCache.cache_object({"orderNo": obj})
        self.click(key='attachment_sales_list_search_order_1', desc='请输入销售单号', tag='input')
        self.affix()
        self.click(key='attachment_sales_list_search_order_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['sales_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_sales_list_search_customer)
    def attachment_sales_list_search_customer(self):
        self.menu_manage()
        obj = self.pc.attachment_sales_list_data()[0]['orderNo']
        ParamCache.cache_object({"orderNo": obj})
        self.click(key='attachment_sales_list_search_customer_1', desc='请选择客户', tag='input')
        self.down_arrow_return(2)
        self.click(key='attachment_sales_list_search_customer_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['sales_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_sales_list_search_status)
    def attachment_sales_list_search_status(self):
        self.menu_manage()
        obj = self.pc.attachment_sales_list_data()[0]['orderNo']
        ParamCache.cache_object({"orderNo": obj})
        self.click(key='attachment_sales_list_search_status_1', desc='请选择收款状态', tag='input')
        self.down_arrow_return()
        self.click(key='attachment_sales_list_search_status_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['sales_list'])
        return self

    @reset_after_execution
    @doc(a_attachment_sales_list_search_logistics)
    def attachment_sales_list_search_logistics(self):
        self.menu_manage()
        obj = self.pc.attachment_sales_list_data()[0]['logisticsNo']
        self.copy(obj)
        ParamCache.cache_object({"logisticsNo": obj})
        self.click(key='attachment_sales_list_search_logistics_1', desc='请输入物流单号', tag='input')
        self.affix()
        self.click(key='attachment_sales_list_search_logistics_2', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['sales_list'])
        return self


class AttachmentSortingListPages(CommonPages):
    """配件管理|入库管理|新到货入库"""

    def menu_manage(self):
        """菜单"""
        self.click(key='attachment_menu_1', desc='配件管理', tag='span', auto=False)
        self.click(key='attachment_menu_2', desc='入库管理', tag='span', index=2, auto=False)
        self.click(key='attachment_menu_18', desc='新到货入库', tag='span', auto=False)
        self.refresh_html_source()
        return self

    @reset_after_execution
    @doc(a_search_for_express_sign_in_warehouse)
    def search_for_express_sign_in_warehouse(self):
        self.menu_manage()
        self.copy(self.pc.attachment_sorting_list_data()[0]['logisticsNo'])
        self.click(key='search_for_express_sign_in_warehouse_1', desc='请输入物流单号', tag='input')
        self.affix()
        self.click(key='search_for_express_sign_in_warehouse_2', desc='搜索', tag='span')
        self.tab_return(5)
        self.click(key='search_for_express_sign_in_warehouse_3', desc='签收/入库', tag='span')
        self.refresh_html_source()
        self.click(key='search_for_express_sign_in_warehouse_4', desc='请选择入库流转仓', tag='input')
        self.up_arrow_return()
        self.click(key='search_for_express_sign_in_warehouse_5', desc='请选择快捷操作', tag='input')
        self.down_arrow_return()
        self.click(key='search_for_express_sign_in_warehouse_6', desc='确定', tag='span')
        return self


class AttachmentStockTransferPages(CommonPages):
    """配件管理|配件库存|库存调拨"""

    def menu_manage(self):
        """菜单"""
        self.click(key='attachment_menu_1', desc='配件管理', tag='span', auto=False)
        self.scroll_custom(element='attachment_menu_7')
        self.click(key='attachment_menu_7', desc='配件库存', tag='span', auto=False)
        self.click(key='attachment_menu_19', desc='库存调拨', index=2, tag='span', auto=False)
        self.refresh_html_source()
        return self

    @reset_after_execution
    @doc(a_express_is_easy_new_allocation)
    def express_is_easy_new_allocation(self):
        self.menu_manage()
        self.copy(self.pc.attachment_inventory_list_data(i=2)[0]['articlesNo'])
        self.click(key='express_is_easy_new_allocation_1', desc='新增调拨', tag='span')
        self.refresh_html_source()
        self.click(key='express_is_easy_new_allocation_2', desc='请选择调出仓库', index=2, tag='input')
        self.down_arrow_return()
        self.click(key='express_is_easy_new_allocation_3', desc='请选择调入仓库', index=2, tag='input')
        self.down_arrow_return(2)
        self.input(key='express_is_easy_new_allocation_4', text='备注', desc='请输入备注', tag='input')
        self.click(key='express_is_easy_new_allocation_5', desc='请输入物品编号/IMEI', tag='input')
        self.affix()
        self.click(key='express_is_easy_new_allocation_6', desc='搜索添加', tag='span')
        self.click(key='express_is_easy_new_allocation_7', desc='快递易开关图标', auto=False)
        self.refresh_html_source()
        self.click(key='express_is_easy_new_allocation_8', desc='请选择快递公司', tag='input')
        self.down_arrow_return()
        self.click(key='express_is_easy_new_allocation_9', desc='计算运费', tag='span')
        self.click(key='express_is_easy_new_allocation_10', desc='确定', tag='span')
        return self

    @reset_after_execution
    @doc(a_import_new_allocation)
    def import_new_allocation(self):
        self.menu_manage()
        self.file.get_attachment_data('attachment_allocation')
        self.copy(self.pc.attachment_inventory_list_data(i=2)[0]['articlesNo'])
        self.click(key='import_new_allocation_1', desc='新增调拨', tag='span')
        self.refresh_html_source()
        self.click(key='import_new_allocation_2', desc='请选择调出仓库', index=2, tag='input')
        self.down_arrow_return()
        self.click(key='import_new_allocation_3', desc='请选择调入仓库', index=2, tag='input')
        self.down_arrow_return(2)
        self.input(key='import_new_allocation_4', text='备注', desc='请输入备注', tag='input')
        self.click(key='import_new_allocation_5', desc='导入', tag='span')
        self.upload_file(key='import_new_allocation_6', file_path=self.file_path('attachment_allocation'))
        self.click(key='import_new_allocation_7', desc='确定', index=4, tag='span')
        self.click(key='import_new_allocation_8', desc='确定', tag='span')
        return self

    @reset_after_execution
    @doc(a_select_add_item_transfer)
    def select_add_item_transfer(self):
        self.menu_manage()
        self.copy(self.pc.attachment_inventory_list_data(i=2)[0]['articlesNo'])
        self.click(key='select_add_item_transfer_1', desc='新增调拨', tag='span')
        self.refresh_html_source()
        self.click(key='select_add_item_transfer_2', desc='请选择调出仓库', index=2, tag='input')
        self.down_arrow_return()
        self.click(key='select_add_item_transfer_3', desc='请选择调入仓库', index=2, tag='input')
        self.down_arrow_return(2)
        self.input(key='select_add_item_transfer_4', text='备注', desc='请输入备注', tag='input')
        self.click(key='select_add_item_transfer_5', desc='选择添加', tag='span')
        self.refresh_html_source()
        self.click(key='select_add_item_transfer_6', desc='搜索', index=2, tag='span')
        self.tab_return(3)
        self.scroll_custom(element='select_add_item_transfer_7')
        self.click(key='select_add_item_transfer_7', desc='确定', index=5, tag='span')
        self.refresh_html_source()
        self.click(key='select_add_item_transfer_8', desc='确定', index=2, tag='span')
        return self

    @reset_after_execution
    @doc(a_receive)
    def receive(self):
        self.menu_manage()
        self.click(key='receive_1', desc='接收', tag='span', auto=False)
        self.refresh_html_source()
        self.click(key='receive_2', desc='确定', index=2, tag='span', auto=False)
        return self

    @reset_after_execution
    @doc(a_add_item_receive_inbound)
    def add_item_receive_inbound(self):
        self.menu_manage()
        self.copy(self.pc.attachment_warehouse_allocation_data(data='a')['itemList'][0]['articlesNo'])
        self.click(key='add_item_receive_inbound_1', desc='扫码接收', tag='span')
        self.refresh_html_source()
        self.click(key='add_item_receive_inbound_2', desc='请输入物品编号/IMEI', tag='input')
        self.affix()
        self.click(key='add_item_receive_inbound_3', desc='添加', tag='span')
        self.click(key='add_item_receive_inbound_4', desc='接收入库', tag='span')
        return self

    @reset_after_execution
    @doc(a_revoke)
    def revoke(self):
        self.menu_manage()
        self.click(key='revoke_1', desc='撤销', tag='span', auto=False)
        self.refresh_html_source()
        self.click(key='revoke_2', desc='确定', index=3, tag='span', auto=False)
        return self

    @reset_after_execution
    @doc(a_export_data)
    def export_data(self):
        self.menu_manage()
        self.click(key='export_data_1', desc='导出', tag='span')
        return self
