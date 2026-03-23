# coding: utf-8
import os
from common.base_page import BasePage, ImportDataEdit, reset_after_execution
from common.base_params import InitializeParams
from config.settings import DATA_PATHS
from common.import_desc import *


class CommonPages(BasePage, InitializeParams):

    def __init__(self, driver):
        super().__init__(driver)
        self._steps_queue = []
        self.file = ImportDataEdit(driver)
        self.file_paths = self.file.file_paths = {
            'img': os.path.join(DATA_PATHS['excel'], 'img.jpg'),
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


class QualityCentreItemPages(CommonPages):
    """质检管理|质检中物品"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='quality_inspection_manage_menu', desc='质检管理')
         .step(key='quality_items_in_quality_inspection_menu', desc='质检中物品')
         .wait())
        return self

    @reset_after_execution
    @doc(q_submit_quality_results)
    def submit_quality_results(self):
        self.menu_manage()
        (self.step(key='submit_inspection_results', desc='提交质检结果')
         .scroll('remark', desc='质检备注')
         .step(key='remark', value=self.serial, action='input', desc='质检备注')
         .step(key='inspection_img', value=self.file_path('img'), action='upload', desc='上传质检图片')
         .step(key='please_enter_the_pre_sale', value='23', action='input', desc='预售保卖价')
         .scroll(key='hand_over_inventory_dio', desc='移交库存')
         .step(key='hand_over_inventory_dio', desc='移交库存')
         .step(key='select_recipient', desc='接收人')
         .custom(lambda: self.down_arrow_return())
         .step(key='repair_instructions', value=self.serial, action='input', desc='移交说明')
         .step(key='submit_quality_verify', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(q_fast_submit_inspection_results)
    def fast_submit_inspection_results(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=2, j=5)[0]['imei'])
        (self.step(key='rapid_quality_inspection', desc='快速质检输入框')
         .custom(lambda: self.affix())
         .step(key='fast_inspection_btn', desc='快速质检')
         .step(key='fineness_color', desc='成色')
         .scroll('remark', desc='质检备注')
         .step(key='remark', value='质检备注', action='input', desc='质检备注')
         .step(key='inspection_img', value=self.file_path('img'), action='upload', desc='上传质检图片')
         .scroll(key='please_enter_the_pre_sale', desc='预售保卖价')
         .step(key='please_enter_the_pre_sale', value='82', action='input', desc='预售保卖价')
         .step(key='hand_over_inventory', desc='移交库存')
         .step(key='select_recipient', desc='接收人')
         .custom(lambda: self.down_arrow_return())
         .step(key='repair_instructions', value=self.serial, action='input', desc='移交说明')
         .step(key='submit_quality_verify', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(q_unverified_handover)
    def unverified_handover(self):
        self.menu_manage()
        (self.step(key='single_choice_dio', desc='单选')
         .step(key='unrepaired', desc='未验移交')
         .step(key='hand_over_inventory_s', desc='移交库存')
         .step(key='select_recipient_o', desc='接收人')
         .custom(lambda: self.up_arrow_return())
         .step(key='handover_instructions_ipt', value=self.serial, action='input', desc='移交说明')
         .step(key='the_maintenance_handover_is_determined', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(q_more_unverified_handover_purchase)
    def more_unverified_handover_purchase(self):
        self.menu_manage()
        (self.step(key='single_choice_dio', desc='单选')
         .step(key='unrepaired', desc='未验移交')
         .step(key='hand_over_purchase', desc='移交采购售后')
         .step(key='select_recipient_o', desc='接收人')
         .custom(lambda: self.up_arrow_return())
         .step(key='handover_instructions_ipt', value=self.serial, action='input', desc='移交说明')
         .step(key='hand_over_cancel', desc='取消')
         .wait())
        return self


class QualityContentTemplatePages(CommonPages):
    """质检管理|质检内容模版"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='quality_inspection_manage_menu', desc='质检管理')
         .step(key='menu', desc='质检内容模版')
         .wait())
        return self

    @reset_after_execution
    @doc(q_new_template_added)
    def new_template_added(self):
        self.menu_manage()
        (self.step(key='new_quality_template', desc='新增')
         .step(key='content_name', value='质检内容名称' + self.serial, action='input', desc='质检内容名称')
         .step(key='sort_name', value='分类名称' + self.serial, action='input', desc='分类名称')
         .step(key='options_type', desc='选项类型')
         .step(key='quality_template_verify', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(q_editor_template)
    def editor_template(self):
        self.menu_manage()
        (self.step(key='editor', desc='编辑')
         .step(key='content_name', value='质检内容名称' + self.serial, action='input', desc='质检内容名称')
         .step(key='sort_name', value='分类名称' + self.serial, action='input', desc='分类名称')
         .step(key='options_type_dio', desc='选项类型')
         .step(key='quality_template_verify', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(q_delete_template)
    def delete_template(self):
        self.menu_manage()
        (self.step(key='delete_template', desc='删除')
         .step(key='delete_verify_btn', desc='确认删除')
         .wait())
        return self


class QualityGoodsReceivedPages(CommonPages):
    """质检管理|待接收物品"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='quality_inspection_manage_menu', desc='质检管理')
         .step(key='menu', desc='待接收物品')
         .wait())
        return self

    @reset_after_execution
    @doc(q_goods_received)
    def goods_received(self):
        self.menu_manage()
        (self.step(key='select_all_dio', desc='全选')
         .step(key='more_handover_btn', desc='接收')
         .step(key='quality_items_receive_ok', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(q_scan_goods_received)
    def scan_goods_received(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=2)[0]['articlesNo'])
        (self.step(key='scan_receive_btn', desc='扫码精确接收')
         .custom(self.affix_carriage_return)
         .step(key='scan_receive_btn', desc='接收')
         .step(key='scan_receive_btn_ok', desc='确定')
         .wait())
        return self


class QualityStorePages(CommonPages):
    """质检管理|先质检后入库"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='quality_inspection_manage_menu', desc='质检管理')
         .step(key='menu', desc='先质检后入库')
         .wait())
        return self

    @reset_after_execution
    @doc(q_quality_artificial_add)
    def quality_artificial_add(self):
        self.menu_manage()
        (self.step(key='manual_quality_inspection', desc='人工快速质检')
         .step(key='select_the_model', desc='选择型号')
         .step(key='select_the_model_ok', desc='确定')
         .step(key='automatically_generate_imei', desc='自动生成imei')
         .step(key='fineness_color', desc='成色')
         .custom(lambda: self.up_arrow_return())
         .step(key='select_the_color', desc='颜色')
         .custom(lambda: self.up_arrow_return())
         .step(key='rom_capacity', desc='rom')
         .custom(lambda: self.up_arrow_return())
         .step(key='select_the_purchase_channel', desc='购买渠道')
         .custom(lambda: self.up_arrow_return())
         .step(key='choose_the_apple_small_model', desc='苹果小型号')
         .custom(lambda: self.up_arrow_return())
         .step(key='select_the_source_of_the_product', desc='商品来源')
         .custom(lambda: self.up_arrow_return())
         .scroll('price', desc='预售保卖价')
         .step(key='price', value='52', action='input', desc='预售保卖价')
         .custom(lambda: self.wait_time())
         .step(key='complete_inventory', desc='提交质检报告')
         .wait())
        return self

    @reset_after_execution
    @doc(q_purchase_warehousing_handover_batch)
    def purchase_warehousing_handover_batch(self):
        self.menu_manage()
        (self.step(key='quality_radio', desc='单选')
         .step(key='bulk_purchase_warehousing', desc='批量采购入库')
         .step(key='go_to', desc='提交采购入库')
         .step(key='procurement_supplier', desc='采购供应商')
         .custom(lambda: self.down_arrow_return())
         .step(key='procurement_account', desc='采购账号')
         .custom(lambda: self.down_arrow_return())
         .step(key='select_circulation_warehouse', desc='流转仓库')
         .custom(lambda: self.down_arrow_return())
         .scroll(key='send_payment_account', desc='付款账户')
         .step(key='payment_amount', value='6.12', action='input', desc='付款金额')
         .custom(lambda: self.carriage_return())
         .step(key='generate_purchase_order', desc='确定生成采购单')
         .step(key='stash_verify', desc='流转仓库确定')
         .wait())
        return self

    @reset_after_execution
    @doc(q_purchase_warehousing_handover)
    def purchase_warehousing_handover(self):
        self.menu_manage()
        (self.step(key='purchase_warehousing', desc='采购入库')
         .step(key='go_to', desc='前往采购入库')
         .custom(lambda: self.wait_time())
         .step(key='procurement_supplier', desc='采购供应商')
         .custom(lambda: self.down_arrow_return())
         .step(key='procurement_account', desc='采购账号')
         .custom(lambda: self.down_arrow_return())
         .step(key='select_circulation_warehouse', desc='流转仓库')
         .custom(lambda: self.down_arrow_return())
         .scroll('payment_account', desc='付款账户')
         .step(key='payment_amount', value='5.12', action='input', desc='付款金额')
         .custom(lambda: self.carriage_return())
         .step(key='generate_purchase_order', desc='确定生成采购单')
         .step(key='stash_verify', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(q_purchase_warehousing_put_on_the_mall)
    def purchase_warehousing_put_on_the_mall(self):
        self.menu_manage()
        (self.step(key='purchase_warehousing', desc='采购入库')
         .step(key='go_to', desc='提交采购入库')
         .step(key='procurement_supplier', desc='采购供应商')
         .custom(lambda: self.down_arrow_return())
         .step(key='procurement_account', desc='采购账号')
         .custom(lambda: self.down_arrow_return())
         .step(key='select_circulation_warehouse', desc='流转仓库')
         .custom(lambda: self.down_arrow_return())
         .scroll('payment_account', desc='付款账号')
         .step(key='payment_amount', value='5', action='input', desc='付款金额')
         .custom(lambda: self.carriage_return())
         .step(key='generate_purchase_order', desc='确定生成采购单')
         .step(key='quick_operation', desc='快捷操作')
         .custom(lambda: self.up_arrow_return())
         .step(key='stash_verify', desc='确定')
         .scroll('product_picture', desc='商品图片')
         .step(key='color_grade', desc='成色等级')
         .custom(lambda: self.up_arrow_return())
         .step(key='selling_price', value=self.number, action='input', desc='销售价')
         .step(key='commission_ratio', value=self.number, action='input', desc='分佣比例')
         .step(key='product_picture', desc='商品图片')
         .step(key='handover_import', value=self.file_path('img'), action='upload', desc='上传文件')
         .step(key='confirm', desc='确认')
         .step(key='confirm_listing', desc='确认上架')
         .wait())
        return self

    @reset_after_execution
    @doc(q_item_report_create_again)
    def item_report_create_again(self):
        self.menu_manage()
        (self.step(key='edit_report', desc='编辑报告')
         .scroll('edit_btn', desc='修改')
         .custom(lambda: self.wait_time())
         .step(key='again_report', desc='重新生成质检报告')
         .step(key='again_confirm', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(q_item_report_edit)
    def item_report_edit(self):
        self.menu_manage()
        (self.step(key='edit_report', desc='编辑报告')
         .scroll('edit_btn', desc='修改')
         .custom(lambda: self.wait_time())
         .step(key='edit_btn', desc='修改当前报告')
         .wait())
        return self


class QualityWaitTurnOverPages(CommonPages):
    """质检管理|待移交物品"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='quality_inspection_manage_menu', desc='质检管理')
         .step(key='menu', desc='待移交物品')
         .wait())
        return self

    @reset_after_execution
    @doc(q_quality_inspection)
    def quality_inspection(self):
        self.menu_manage()
        (self.step(key='check_again', desc='复检')
         .step(key='quality', desc='成色')
         .custom(lambda: self.up_arrow_return())
         .step(key='color', desc='颜色')
         .custom(lambda: self.up_arrow_return())
         .step(key='source', desc='商品来源')
         .custom(lambda: self.up_arrow_return())
         .scroll('guaranteed_price', desc='预售保卖价')
         .step(key='labor_costs', value='23', action='input', desc='预售保卖价')
         .step(key='hand_over_quality', desc='移交质检')
         .step(key='receiver', desc='选择接收人')
         .step(key='complete_inventory', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(q_handover_inventory)
    def handover_inventory(self):
        self.menu_manage()
        (self.step(key='work_order_item', desc='单选')
         .step(key='more_handover_btn', desc='移交')
         .step(key='handover_inventory', desc='移交库存')
         .step(key='receiver', desc='选择接收人')
         .custom(lambda: self.up_arrow_return())
         .step(key='transfer_remarks', value=self.serial, action='input', desc='移交说明')
         .step(key='verify_2', desc='确定')
         .wait())
        return self
