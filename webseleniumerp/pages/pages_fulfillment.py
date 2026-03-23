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
            'video': os.path.join(DATA_PATHS['excel'], 'video.mp4'),
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


class FulfillmentItemsToBeQuotedPages(CommonPages):
    """运营中心|待报价物品"""

    def menu_manage(self):
        """菜单"""
        (self.scroll('fulfillment_center_menu', desc='运营中心')
         .step(key='fulfillment_center_menu', desc='运营中心')
         .step(key='fulfillment_wait_for_quotation_goods_menu', desc='待报价物品')
         .wait())
        return self

    @doc(f_commodity_quotes)
    def commodity_quotes(self):
        """商品报价"""
        self.menu_manage()
        self.copy(self.pc.fulfillment_items_to_be_quoted_data()[0]['articlesNo'])
        (self.step(key='item_num', desc='物品编号')
         .custom(lambda: self.affix())
         .step(key='search', desc='搜索')
         .step(key='commodity_quotes', desc='商品报价')
         .step(key='please_enter_the_price', value=310, action='input', desc='输入价格')
         .step(key='determination', desc='确定')
         .wait())

    @reset_after_execution
    def requote(self):
        """重新报价"""
        self.menu_manage()
        self.copy(self.pc.fulfillment_items_to_be_quoted_data()[0]['articlesNo'])
        (self.step(key='item_num', desc='物品编号')
         .custom(lambda: self.affix())
         .step(key='search', desc='搜索')
         .step(key='again_price_btn', desc='重新报价')
         .step(key='please_enter_the_price', value=310, action='input', desc='输入价格')
         .step(key='determination', desc='确定')
         .wait())
        return self


class FulfillmentQualityManagePages(CommonPages):
    """运营中心|质检管理"""

    def menu_manage(self):
        """菜单"""
        (self.scroll('fulfillment_center_menu', desc='运营中心')
         .step(key='fulfillment_center_menu', desc='运营中心')
         .step(key='fulfillment_quality_manage_menu', desc='质检管理')
         .wait())
        return self

    @reset_after_execution
    @doc(f_receive_items_in_bulk)
    def receive_items_in_bulk(self):
        self.menu_manage()
        self.copy(self.pc.fulfillment_quality_manage_data()[0]['imei'])
        (self.step(key='imei_ipt', desc='imei输入框')
         .custom(lambda: self.affix())
         .step(key='search', desc='搜索')
         .custom(lambda: self.tab_return(5))
         .step(key='receive_in_batches', desc='批量接收')
         .step(key='confirm', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(f_direct_platform_review_receive_in_batches)
    def direct_platform_review_receive_in_batches(self):
        self.receive_items_in_bulk()

    @reset_after_execution
    @doc(f_quality_receive_items_in_bulk)
    def quality_receive_items_in_bulk(self):
        self.receive_items_in_bulk()

    @reset_after_execution
    @doc(f_direct_shot_physical_re_inspection_received)
    def direct_shot_physical_re_inspection_received(self):
        self.receive_items_in_bulk()

    @reset_after_execution
    @doc(f_submit_the_quality_inspection_results)
    def submit_the_quality_inspection_results(self):
        self.menu_manage()
        self.copy(self.pc.fulfillment_quality_manage_data(data='a')[0]['imei'])
        (self.step(key='items_in_quality_inspection', desc='质检中物品')
         .step(key='imei_ipt', desc='imei输入框')
         .custom(lambda: self.affix())
         .step(key='search', desc='搜索')
         .step(key='submit_the_quality_inspection_results', desc='提交质检结果')
         .custom(lambda: self.wait_time())
         .step(key='capacity', desc='rom容量')
         .custom(lambda: self.down_arrow_return(2))
         .scroll(key='submit_the_quality_inspection_confirm',desc='确定')
         .step(key='submit_the_quality_inspection_confirm', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_quality_submit_the_quality_inspection_results)
    def quality_submit_the_quality_inspection_results(self):
        self.submit_the_quality_inspection_results()

    @reset_after_execution
    @doc(f_direct_shot_of_the_real_thing_submit_quality)
    def direct_shot_of_the_real_thing_submit_quality(self):
        self.submit_the_quality_inspection_results()

    @reset_after_execution
    @doc(f_submit_the_quality_inspection_results_no)
    def submit_the_quality_inspection_results_no(self):
        self.submit_the_quality_inspection_results()

    @reset_after_execution
    @doc(f_direct_platform_review_submit_quality)
    def direct_platform_review_submit_quality(self):
        self.submit_the_quality_inspection_results()

    @reset_after_execution
    @doc(f_passed_the_re_inspection)
    def passed_the_re_inspection(self):
        self.menu_manage()
        self.copy(self.pc.fulfillment_quality_manage_data(data='c')[0]['imei'])
        (self.step(key='re_examine_the_application', desc='重验申请')
         .step(key='imei_ipt', desc='imei输入框')
         .custom(lambda: self.affix())
         .scroll(key='review', desc='审核')
         .step(key='review', desc='审核')
         .step(key='agree', desc='同意')
         .step(key='review_instructions', value='备注', action='input', desc='审核说明')
         .step(key='determination', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_rereview_rejected)
    def rereview_rejected(self):
        self.menu_manage()
        self.copy(self.pc.fulfillment_quality_manage_data(data='c')[0]['imei'])
        (self.step(key='re_examine_the_application', desc='重验申请')
         .step(key='imei_ipt', desc='imei输入框')
         .custom(lambda: self.affix())
         .step(key='search', desc='搜索')
         .scroll(key='review', desc='审核')
         .step(key='review', desc='审核')
         .step(key='rejected', desc='拒绝')
         .step(key='review_instructions', value='备注', action='input', desc='审核说明')
         .step(key='determination', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_modify_the_report)
    def modify_the_report(self):
        self.menu_manage()
        self.copy(self.pc.fulfillment_quality_manage_data(data='b')[0]['imei'])
        (self.step(key='inspected_items', desc='已质检物品')
         .step(key='imei_ipt', desc='imei输入框')
         .custom(lambda: self.affix())
         .step(key='search', desc='搜索')
         .step(key='modify_the_report', desc='修改报告')
         .custom(lambda: self.wait_time())
         .scroll(key='the_revision_report_is_determined',desc='确定')
         .step(key='the_revision_report_is_determined', desc='确定')
         .step(key='editorial_quality_inspection_determined', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_unverified_handover)
    def unverified_handover(self):
        self.menu_manage()
        self.copy(self.pc.fulfillment_quality_manage_data(data='a')[0]['imei'])
        (self.step(key='items_in_quality_inspection', desc='质检中物品')
         .step(key='imei_ipt', desc='imei输入框')
         .custom(lambda: self.affix())
         .step(key='search', desc='搜索')
         .custom(lambda: self.tab_return(5))
         .step(key='not_verified_handover', desc='未验移交')
         .step(key='select_the_recipient', desc='接收人')
         .custom(lambda: self.down_arrow_return())
         .step(key='determination', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_not_quality)
    def not_quality(self):
        self.menu_manage()
        (self.step(key='items_in_quality_inspection', desc='质检中物品')
         .scroll('no_quality_inspection_required')
         .step(key='no_quality_inspection_required', desc='无需质检')
         .step(key='unable_to_turn_on_item', desc='质检项1')
         .step(key='machine_failure_item', desc='质检项2')
         .step(key='determination', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_product_image_shooting_and_uploading)
    def product_image_shooting_and_uploading(self):
        self.menu_manage()
        (self.step(key='product_image_shooting', desc='商品图拍摄')
         .step(key='take_a_picture_of_the_product', desc='拍商品图')
         .step(key='upload_product_images', value=self.file_path('img'), action='upload', desc='拍商品图')
         .step(key='photo_confirmed', desc='确认')
         .wait())
        return self


class FulfillmentReturnsManage(CommonPages):
    """运营中心|退货管理"""

    def menu_manage(self):
        """菜单"""
        (self.scroll(key='fulfillment_center_menu', desc='运营中心')
         .step(key='fulfillment_center_menu', desc='运营中心')
         .step(key='fulfillment_returns_manage', desc='退货管理')
         .wait())
        return self

    @reset_after_execution
    @doc(f_return_to_the_warehouse)
    def return_to_the_warehouse(self):
        self.menu_manage()
        (self.step(key='pending_returns', desc='待退货')
         .step(key='item_details', desc='物品明细')
         .custom(lambda: self.wait_time())
         .custom(lambda: self.tab_return(3))
         .step(key='return_warehouse_one', desc='退货出库')
         .step(key='logistics_company', desc='请选择物流公司')
         .step(key='choose_sf', desc='选择顺丰速运')
         .step(key='material_flow', value=self.sf, action='input', desc='请输入物流单号')
         .step(key='confirm_button', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_return_to_the_warehouse)
    def return_to_the_warehouse_use_jd(self):
        self.menu_manage()
        (self.step(key='pending_returns', desc='待退货')
         .step(key='item_details', desc='物品明细')
         .custom(lambda: self.wait_time())
         .custom(lambda: self.tab_return(3))
         .step(key='return_warehouse_one', desc='退货出库')
         .step(key='logistics_company', desc='请选择物流公司')
         .step(key='choose_jd', desc='选择京东快运')
         .step(key='material_flow', value=self.jd, action='input', desc='请输入物流单号')
         .step(key='confirm_button', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_return_to_the_warehouse_export_information)
    def return_to_the_warehouse_export_information(self):
        self.menu_manage()
        (self.step(key='pending_returns', desc='待退货')
         .step(key='item_details', desc='物品明细')
         .custom(lambda: self.wait_time())
         .custom(lambda: self.tab_return(3))
         .custom(lambda: self.tab_return())
         .step(key='export_information', desc='导出信息')
         .wait())
        return self

    @reset_after_execution
    @doc(f_self_submitted_library)
    def self_submitted_library(self):
        self.copy(self.mg.auction_my_data(data='a')['pickupCode'])
        self.menu_manage()
        (self.step(key='waiting_for_pickup', desc='待取货')
         .step(key='item_details', desc='物品明细')
         .custom(lambda: self.wait_time())
         .custom(lambda: self.tab_return(4))
         .custom(lambda: self.wait_time())
         .step(key='self_pickup_returns_one', desc='自提出库')
         .step(key='input_self_number', desc='扫码或输入自提码')
         .custom(lambda: self.affix())
         .step(key='confirm_button_self', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_self_submitted_library_export_information)
    def self_submitted_library_export_information(self):
        self.menu_manage()
        (self.step(key='waiting_for_pickup', desc='待取货')
         .custom(lambda: self.wait_time())
         .step(key='export_information', desc='导出信息')
         .wait())
        return self

    @reset_after_execution
    @doc(f_the_return_has_been_removed_batch)
    def the_return_has_been_removed_batch(self):
        self.menu_manage()
        (self.step(key='the_return_has_been_removed', desc='退货已出库')
         .step(key='batch_details', desc='批次明细')
         .step(key='change_logistics_one', desc='更改物流')
         .step(key='logistics_company', desc='请选择物流公司')
         .step(key='choose_jd', desc='选择京东快运')
         .step(key='material_flow', value=self.jd, action='input', desc='请输入物流单号')
         .step(key='confirm_button_change', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_the_return_has_been_removed_items)
    def the_return_has_been_removed_items(self):
        self.menu_manage()
        (self.step(key='the_return_has_been_removed', desc='退货已出库')
         .step(key='item_details', desc='物品明细')
         .step(key='change_logistics_one', desc='更改物流')
         .step(key='logistics_company', desc='请选择物流公司')
         .step(key='choose_jd', desc='选择京东快运')
         .step(key='material_flow', value=self.jd, action='input', desc='请输入物流单号')
         .step(key='confirm_button_change', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_the_return_has_been_removed_batch_export)
    def the_return_has_been_removed_batch_export(self):
        self.menu_manage()
        (self.step(key='the_return_has_been_removed', desc='退货已出库')
         .step(key='batch_details', desc='批次明细')
         .custom(lambda: self.wait_time())
         .step(key='export_information', desc='导出信息')
         .wait())
        return self

    @reset_after_execution
    @doc(f_the_return_has_been_removed_items_export)
    def the_return_has_been_removed_items_export(self):
        self.menu_manage()
        (self.step(key='the_return_has_been_removed', desc='退货已出库')
         .step(key='item_details', desc='物品明细')
         .custom(lambda: self.wait_time())
         .step(key='export_information', desc='导出信息')
         .wait())
        return self

    @reset_after_execution
    @doc(f_cancelled_select_code)
    def cancelled_select_code(self):
        self.menu_manage()
        (self.step(key='the_return_has_been_removed', desc='退货已出库')
         .step(key='item_details', desc='物品明细')
         .custom(lambda: self.wait_time())
         .step(key='export_information', desc='导出信息')
         .wait())
        return self


class FulfillmentSignIntoTheLibraryPages(CommonPages):
    """运营中心|收货入库"""

    def menu_manage(self):
        """菜单"""
        (self.scroll(key='fulfillment_center_menu', desc='运营中心')
         .step(key='fulfillment_center_menu', desc='运营中心')
         .step(key='fulfillment_receive_goods_in_warehouse_menu', desc='收货入库')
         .wait())
        return self

    @reset_after_execution
    @doc(f_unpacking_and_receiving_goods_into_storage)
    def unpacking_and_receiving_goods_into_storage(self):
        self.copy(self.pc.fulfillment_order_manage_data(i=3)[0]['orderNo'])
        self.menu_manage()
        (self.step(key='ipt_order_number', desc='订单编号')
         .custom(lambda: self.affix())
         .step(key='add', desc='添加')
         .step(key='input_imei', value=self.imei, action='input', desc='输入imei')
         .step(key='record_unpacking_videos', desc='录制拆包视频')
         .step(key='upload_an_unpacking_video', value=self.file_path('video'), action='upload', desc='上传视频')
         .step(key='select_the_order_number', desc='选择订单编号')
         .custom(lambda: self.down_arrow_return())
         .step(key='unpacking_video_confirmation', desc='确定')
         .step(key='receive_goods_in_warehouse', desc='收货入库')
         .custom(lambda: self.wait_time())
         .step(key='receiver', desc='接收人')
         .custom(lambda: self.down_arrow_return())
         .step(key='confirm_button_received', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_quality_inspection_upload_videos_for_storage)
    def quality_inspection_upload_videos_for_storage(self):
        self.unpacking_and_receiving_goods_into_storage()

    @reset_after_execution
    @doc(f_goods_are_received_and_into_storage_no_imei)
    def goods_are_received_and_into_storage_no_imei(self):
        self.copy(self.pc.fulfillment_order_manage_data(i=3)[0]['orderNo'])
        self.menu_manage()
        (self.step(key='ipt_order_number', desc='订单编号')
         .custom(lambda: self.affix())
         .step(key='add', desc='添加')
         .step(key='record_unpacking_videos', desc='录制拆包视频')
         .step(key='upload_an_unpacking_video', value=self.file_path('video'), action='upload', desc='上传视频')
         .step(key='select_the_order_number', desc='选择订单编号')
         .custom(lambda: self.down_arrow_return())
         .step(key='unpacking_video_confirmation', desc='确定')
         .step(key='receive_goods_in_warehouse', desc='收货入库')
         .step(key='printed', desc='已打印')
         .custom(lambda: self.wait_time())
         .step(key='receiver', desc='请选择接收人')
         .step(key='choose_admin', desc='选择admin')
         .step(key='confirm_button_received', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_goods_are_received_and_into_storage_online_record)
    def goods_are_received_and_into_storage_online_record(self):
        self.copy(self.pc.fulfillment_order_manage_data(i=3)[0]['orderNo'])
        self.menu_manage()
        (self.step(key='ipt_order_number', desc='订单编号')
         .custom(lambda: self.affix())
         .step(key='add', desc='添加')
         .step(key='input_imei', value=self.imei, action='input', desc='输入imei')
         .step(key='record_unpacking_videos', desc='录制拆包视频')
         .step(key='online_record', desc='在线录制')
         .step(key='start_record', desc='开始录制')
         .custom(lambda: self.wait_time(3))
         .step(key='end_record', desc='结束录制')
         .step(key='confirm_button_tip', desc='确认')
         .custom(lambda: self.wait_time(2))
         .step(key='select_the_order_number', desc='选择订单编号')
         .custom(lambda: self.down_arrow_return())
         .step(key='unpacking_video_confirmation', desc='确定')
         .step(key='receive_goods_in_warehouse', desc='收货入库')
         .custom(lambda: self.wait_time())
         .step(key='receiver', desc='请选择接收人')
         .step(key='choose_admin', desc='选择admin')
         .step(key='confirm_button_received', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_received_goods_into_the_warehouse_express_no)
    def received_goods_into_the_warehouse_express_no(self):
        self.copy(self.pc.fulfillment_order_manage_data(i=3)[0]['expressNo'])
        self.menu_manage()
        (self.step(key='material_flow', desc='输入物流单号')
         .custom(lambda: self.affix())
         .step(key='add', desc='添加')
         .step(key='input_imei', value=self.imei, action='input', desc='输入imei')
         .step(key='record_unpacking_videos', desc='录制拆包视频')
         .step(key='upload_an_unpacking_video', value=self.file_path('video'), action='upload', desc='上传视频')
         .step(key='select_the_order_number', desc='选择订单编号')
         .custom(lambda: self.down_arrow_return())
         .step(key='unpacking_video_confirmation', desc='确定')
         .step(key='receive_goods_in_warehouse', desc='收货入库')
         .custom(lambda: self.wait_time())
         .step(key='receiver', desc='接收人')
         .custom(lambda :self.down_arrow_return())
         .step(key='confirm_button_received', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_received_goods_into_the_warehouse_modify_imei)
    def received_goods_into_the_warehouse_modify_imei(self):
        self.copy(self.pc.fulfillment_order_manage_data(i=3)[0]['orderNo'])
        self.menu_manage()
        (self.step(key='ipt_order_number', desc='订单编号')
         .custom(lambda: self.affix())
         .step(key='add', desc='添加')
         .custom(lambda: self.wait_time())
         .step(key='modify_number', desc='修改实收数量')
         .step(key='input_number', value="2", action='input', desc='输入实收数量')
         .step(key='add', desc='添加')
         .custom(lambda: self.wait_time())
         .custom(lambda: self.tab_return(3))
         .step(key='batch_modifications', desc='批量修改IMEI')
         .step(key='input_many_imei', value=f"{self.imei},{self.imei}", action='input', desc='输入多个imei')
         .step(key='confirm_button_edit_imei', desc='确定')
         .step(key='record_unpacking_videos', desc='录制拆包视频')
         .step(key='upload_an_unpacking_video', value=self.file_path('video'), action='upload', desc='上传视频')
         .step(key='select_the_order_number', desc='选择订单编号')
         .custom(lambda: self.down_arrow_return())
         .step(key='unpacking_video_confirmation', desc='确定')
         .step(key='receive_goods_in_warehouse', desc='收货入库')
         .custom(lambda: self.wait_time())
         .step(key='receiver', desc='接收人')
         .custom(lambda: self.down_arrow_return())
         .step(key='confirm_button_received', desc='确定')
         .wait())
        return self


class FulfillmentOrderManagePages(CommonPages):
    """运营中心|订单管理"""

    def menu_manage(self):
        """菜单"""
        (self.scroll(key='fulfillment_center_menu', desc='运营中心')
         .step(key='fulfillment_center_menu', desc='运营中心')
         .step(key='menu', desc='订单管理')
         .wait())
        return self


class FulfillmentItemsAreOutOfStoragePages(CommonPages):
    """运营中心|物品出库"""

    def menu_manage(self):
        """菜单"""
        (self.scroll('fulfillment_center_menu', desc='运营中心')
         .step(key='fulfillment_center_menu', desc='运营中心')
         .step(key='fulfillment_items_are_out_of_the_warehouse_menu', desc='物品出库')
         .wait())
        return self

    @reset_after_execution
    @doc(f_direct_shot_express_sales_out_of_the_warehouse)
    def direct_shot_express_sales_out_of_the_warehouse(self):
        self.copy(self.pc.fulfillment_sales_and_shipment_manage_data(data='a')[0]['articlesNo'])
        self.menu_manage()
        (self.step(key='receiving_merchants', desc='收货商户')
         .step(key='receiving_merchants', value=INFO['camera_username'], action='input', desc='收货商户')
         .custom(lambda: self.down_arrow_return())
         .step(key='item_number_ipt', desc='物品编号输入框')
         .custom(lambda: self.affix_carriage_return())
         .step(key='logistics_company', desc='物流公司')
         .custom(lambda: self.down_arrow_return())
         .step(key='logistics_tracking_number', value=self.sf, action='input', desc='物流单号')
         .step(key='item_outbound_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(f_direct_shot_jd_express_sales_out_of_the_warehouse)
    def direct_shot_jd_express_sales_out_of_the_warehouse(self):
        self.copy(self.pc.fulfillment_sales_and_shipment_manage_data(data='a')[0]['articlesNo'])
        self.menu_manage()
        (self.step(key='receiving_merchants', desc='收货商户')
         .step(key='receiving_merchants', value=INFO['camera_username'], action='input', desc='收货商户')
         .custom(lambda: self.down_arrow_return())
         .step(key='item_number_ipt', desc='物品编号输入框')
         .custom(lambda: self.affix_carriage_return())
         .step(key='logistics_company', desc='物流公司')
         .custom(lambda: self.down_arrow_return(2))
         .step(key='logistics_tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='item_outbound_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(f_direct_shooting_order_sales_out_of_the_warehouse)
    def direct_shooting_order_sales_out_of_the_warehouse(self):
        self.copy(self.pc.fulfillment_sales_and_shipment_manage_data(data='a')[0]['articlesNo'])
        self.menu_manage()
        (self.step(key='receiving_merchants', desc='收货商户')
         .step(key='receiving_merchants', value=INFO['camera_username'], action='input', desc='收货商户')
         .custom(lambda: self.down_arrow_return())
         .step(key='item_number_ipt', desc='物品编号输入框')
         .custom(lambda: self.affix_carriage_return())
         .step(key='express_is_easy', desc='系统叫件')
         .step(key='logistics_tracking_number', value=self.sf, action='input', desc='物流单号')
         .step(key='item_outbound_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(f_direct_shooting_order_sales_out_of_the_warehouse_jd)
    def direct_shooting_order_sales_out_of_the_warehouse_jd(self):
        self.copy(self.pc.fulfillment_sales_and_shipment_manage_data(data='a')[0]['articlesNo'])
        self.menu_manage()
        (self.step(key='receiving_merchants', desc='收货商户')
         .step(key='receiving_merchants', value=INFO['camera_username'], action='input', desc='收货商户')
         .custom(lambda: self.down_arrow_return())
         .step(key='item_number_ipt', desc='物品编号输入框')
         .custom(lambda: self.affix_carriage_return())
         .step(key='express_is_easy', desc='系统叫件')
         .step(key='jd_com', desc='京东')
         .step(key='logistics_tracking_number', value=self.jd, action='input', desc='物流单号')
         .step(key='item_outbound_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(f_direct_shooting_self_pick_up_and_sales)
    def direct_shooting_self_pick_up_and_sales(self):
        self.copy(self.mc.bidding_my_data(i=3)[0]['articlesNo'])
        self.menu_manage()
        (self.step(key='self_lifted', desc='自提')
         .step(key='self_pickup_code', action='input', desc='自提码')
         .custom(lambda: self.affix_carriage_return())
         .step(key='item_outbound_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(f_direct_sf_after_sales_delivery)
    def direct_sf_after_sales_delivery(self):
        self.copy(self.pc.fulfillment_after_sales_return_manage_data(i=1)[0]['articlesNo'])
        self.menu_manage()
        (self.step(key='item_number_ipt', desc='物品输入框')
         .custom(lambda: self.affix_carriage_return())
         .step(key='item_outbound_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(f_direct_jd_after_sales_delivery)
    def direct_jd_after_sales_delivery(self):
        self.copy(self.pc.fulfillment_after_sales_return_manage_data(i=1)[0]['articlesNo'])
        self.menu_manage()
        (self.step(key='item_number_ipt', desc='物品输入框')
         .custom(lambda: self.affix_carriage_return())
         .step(key='jd_com', desc='京东')
         .step(key='item_outbound_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(f_direct_zt_after_sales_delivery)
    def direct_zt_after_sales_delivery(self):
        self.copy(self.pc.fulfillment_after_sales_return_manage_data(i=1)[0]['articlesNo'])
        self.menu_manage()
        (self.step(key='self_lifted', desc='自提')
         .step(key='item_number_ipt', desc='物品输入框')
         .custom(lambda: self.affix_carriage_return())
         .step(key='item_outbound_confirmation', desc='确认')
         .wait())
        return self
