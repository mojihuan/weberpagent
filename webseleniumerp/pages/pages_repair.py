# coding: utf-8
from common.base_page import BasePage, reset_after_execution
from common.base_params import InitializeParams
from common.import_desc import *


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


class RepairAuditListPages(CommonPages):
    """维修管理|维修审核列表"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='repair_manage_menu', desc='维修管理')
         .step(key='repair_audit_list_menu', desc='维修审核列表')
         .wait())
        return self

    @reset_after_execution
    @doc(r_the_maintenance_audit_passed)
    def the_maintenance_audit_passed(self):
        self.menu_manage()
        (self.step(key='repair_examine', desc='审核')
         .step(key='repair_audit_instructions', value=self.serial, action='input', desc='审核说明')
         .step(key='repair_audit_verify', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(r_audit_rejection)
    def audit_rejection(self):
        self.menu_manage()
        (self.step(key='repair_examine', desc='审核')
         .step(key='repair_audit_turn_down', desc='未通过')
         .step(key='repair_audit_instructions', value=self.serial, action='input', desc='审核说明')
         .step(key='repair_audit_verify', desc='确认')
         .wait())
        return self


class RepairCentreItemPages(CommonPages):
    """维修管理|维修中物品"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='repair_manage_menu', desc='维修管理')
         .step(key='repair_centre_item_menu', desc='维修中物品')
         .wait())
        return self

    @reset_after_execution
    @doc(r_submit_the_maintenance_results)
    def submit_the_maintenance_results(self):
        self.menu_manage()
        (self.step(key='submit_repair_results', desc='提交维修结果')
         .step(key='repair_item_one', desc='维修项目-1')
         .step(key='repair_item_two', desc='维修项目-2')
         .scroll('repair_details', desc='维修详情')
         .step(key='purpose_of_transfer', desc='移交库存')
         .step(key='select_recipient', desc='接收人')
         .custom(lambda: self.up_arrow_return())
         .step(key='repair_details', value=self.serial, action='input', desc='维修详情')
         .step(key='submit_a_repair_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(r_add_accessories_submit_repair_results)
    def add_accessories_submit_repair_results(self):
        self.menu_manage()
        (self.step(key='submit_repair_results', desc='提交维修结果')
         .step(key='add_accessories', desc='添加配件')
         .step(key='accessories_radio', desc='单选')
         .scroll('add_accessories_verify', desc='确定')
         .step(key='add_accessories_verify', desc='确定')
         .step(key='repair_item_one', desc='维修项目-1')
         .step(key='repair_item_two', desc='维修项目-2')
         .scroll(key='submit_a_repair_confirmation', desc='确认')
         .step(key='purpose_of_transfer', desc='移交库存')
         .step(key='select_recipient', desc='接收人')
         .custom(lambda: self.up_arrow_return())
         .step(key='repair_details', value=self.serial, action='input', desc='维修详情')
         .step(key='submit_a_repair_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(r_scan_the_code_to_add_accessories)
    def scan_the_code_to_add_accessories(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=2)[0]['articlesNo'])
        (self.step(key='submit_repair_results', desc='提交维修结果')
         .step(key='scan_add_accessories', desc='扫码添加配件')
         .custom(self.affix_carriage_return)
         .step(key='verify_add', desc='确认添加')
         .step(key='repair_item_one', desc='维修项目-1')
         .step(key='repair_item_two', desc='维修项目-2')
         .scroll(key='submit_a_repair_confirmation', desc='确认')
         .step(key='purpose_of_transfer', desc='移交库存')
         .step(key='select_recipient', desc='接收人')
         .custom(lambda: self.up_arrow_return())
         .step(key='repair_details', value=self.serial, action='input', desc='维修详情')
         .step(key='submit_a_repair_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(r_fast_submit_repair_results)
    def fast_submit_repair_results(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=2)[0]['articlesNo'])
        (self.step(key='enter_the_imei_number', desc='点击IMEI输入框')
         .custom(lambda: self.affix())
         .step(key='quick_repair', desc='快速维修')
         .step(key='repair_item_one', desc='维修项目-1')
         .step(key='repair_item_two', desc='维修项目-2')
         .scroll(key='submit_a_repair_confirmation', desc='确认')
         .step(key='purpose_of_transfer', desc='移交库存')
         .step(key='select_recipient', desc='接收人')
         .custom(lambda: self.up_arrow_return())
         .step(key='repair_details', value=self.serial, action='input', desc='维修详情')
         .step(key='submit_a_repair_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(r_fast_submit_repair_bulk_submission)
    def fast_submit_repair_bulk_submission(self):
        self.menu_manage()
        (self.step(key='multiple_choice', desc='全选')
         .step(key='bulk_submission', desc='批量提交维修结果')
         .step(key='repair_item_one', desc='维修项目-1')
         .step(key='repair_item_two', desc='维修项目-2')
         .scroll(key='submit_a_repair_confirmation', desc='确认')
         .step(key='purpose_of_transfer', desc='移交库存')
         .step(key='select_recipient', desc='接收人')
         .custom(lambda: self.up_arrow_return())
         .step(key='repair_details', value=self.serial, action='input', desc='维修详情')
         .step(key='submit_a_repair_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(r_unrepaired_handover)
    def unrepaired_handover(self):
        self.menu_manage()
        (self.step(key='item_radio', desc='单选')
         .step(key='unrepaired', desc='未修移交')
         .step(key='hand_over_stock', desc='移交库存')
         .step(key='select_recipient', desc='接收人')
         .custom(lambda: self.up_arrow_return())
         .step(key='repair_instructions', value=self.serial, action='input', desc='移交说明')
         .step(key='the_maintenance_handover_is_determined', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(r_scan_unverified_handover)
    def scan_unverified_handover(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=2, j=7)[0]['articlesNo'])
        (self.step(key='scan_batch_open_handoffs', desc='扫描批量未修移交')
         .step(key='repair_item_imei_input', desc='物品IMEI框')
         .custom(self.affix_carriage_return)
         .step(key='unverified_handover_dio', desc='未修移交')
         .step(key='hand_over_stock', desc='移交库存')
         .step(key='select_recipient', desc='接收人')
         .custom(lambda: self.up_arrow_return())
         .step(key='repair_instructions', value=self.serial, action='input', desc='移交说明')
         .step(key='the_maintenance_handover_is_determined', desc='确定')
         .step(key='handover_prompt_is_confirm', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(r_purpose_of_transfer_repair)
    def purpose_of_transfer_repair(self):
        self.menu_manage()
        (self.step(key='submit_repair_results', desc='提交维修结果')
         .scroll(key='submit_a_repair_confirmation', desc='确认')
         .step(key='labor_costs', value="200", action='input', desc='输入工费200')
         .step(key='purpose_of_transfer_repair', desc='移交维修')
         .step(key='select_recipient', desc='接收人')
         .custom(lambda: self.up_arrow_return())
         .step(key='repair_details', value=self.serial, action='input', desc='维修详情')
         .step(key='submit_a_repair_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(r_purpose_of_transfer_sales)
    def purpose_of_transfer_sales(self):
        self.menu_manage()
        (self.step(key='submit_repair_results', desc='提交维修结果')
         .scroll(key='submit_a_repair_confirmation', desc='确认')
         .step(key='labor_costs', value="200", action='input', desc='工费')
         .step(key='purpose_of_transfer_sales', desc='移交销售')
         .step(key='select_recipient', desc='接收人')
         .custom(lambda: self.up_arrow_return())
         .step(key='repair_details', value=self.serial, action='input', desc='维修详情')
         .step(key='submit_a_repair_confirmation', desc='确认')
         .wait())
        return self


class RepairDataStatisticsPages(CommonPages):
    """维修管理|维修数据统计"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='repair_manage_menu', desc='维修管理')
         .step(key='repair_data_statistics_menu', desc='维修数据统计')
         .wait())
        return self

    @doc(r_derived_data)
    def derived_data(self):
        """导出按钮"""
        self.menu_manage()
        (self.step(key='sales_after_sales_btn', desc='导出')
         .wait())
        return self


class RepairGoodsReceivedPages(CommonPages):
    """维修管理|待接收物品"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='repair_manage_menu', desc='维修管理')
         .step(key='repair_items_awaiting_receipt_menu', desc='待接收物品')
         .wait())
        return self

    @reset_after_execution
    @doc(r_goods_received)
    def goods_received(self):
        self.menu_manage()
        (self.step(key='multiple_choice', desc='全选')
         .step(key='more_handover_btn', desc='接收')
         .step(key='quality_items_receive_ok', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(r_scan_goods_received)
    def scan_goods_received(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=2)[0]['articlesNo'])
        (self.step(key='scan_receive_btn', desc='扫码精确接收')
         .custom(self.affix_carriage_return)
         .step(key='scan_receive_btn', desc='接收')
         .step(key='delete_address_ok', desc='确定')
         .wait())
        return self


class RepairProjectListPages(CommonPages):
    """维修管理|维修项目列表"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='repair_manage_menu', desc='维修管理')
         .step(key='repair_audit_list_menu', desc='维修项目列表')
         .wait())
        return self

    @reset_after_execution
    @doc(r_new_maintenance_items_iphone)
    def new_maintenance_items_iphone(self):
        self.menu_manage()
        (self.step(key='sales_after_sales_btn', desc='新增维修项目')
         .step(key='maintenance_category', desc='维修类目')
         .custom(lambda: self.up_arrow_return())
         .step(key='maintenance_item', value=self.serial, action='input', desc='维修项目')
         .step(key='maintenance_cost', value='21', action='input', desc='维修工费')
         .step(key='applicable_category', desc='适用品类')
         .custom(lambda: self.down_arrow_return())
         .step(key='tip_txt', desc='弹窗标题')
         .step(key='maintenance_item_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(r_new_maintenance_items_ipa)
    def new_maintenance_items_ipa(self):
        self.menu_manage()
        (self.step(key='sales_after_sales_btn', desc='新增维修项目')
         .step(key='maintenance_category', desc='维修类目')
         .custom(lambda: self.up_arrow_return())
         .step(key='maintenance_item', value=self.serial, action='input', desc='维修项目名称')
         .step(key='maintenance_cost', value='34', action='input', desc='维修工费')
         .step(key='applicable_category', desc='适用品类')
         .custom(lambda: self.down_arrow_return())
         .custom(lambda: self.down_arrow_return())
         .step(key='tip_txt', desc='弹窗标题')
         .step(key='maintenance_item_confirmation', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(r_editor_maintenance_items)
    def editor_maintenance_items(self):
        self.menu_manage()
        (self.step(key='maintenance_item_editor', desc='编辑')
         .step(key='maintenance_category', desc='点击维修类目')
         .custom(lambda: self.up_arrow_return(2))
         .step(key='maintenance_item', value=self.serial, action='input', desc='维修项目名称')
         .step(key='maintenance_cost', value='22', action='input', desc='维修工费')
         .step(key='edit_confirm', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(r_delete_maintenance_items)
    def delete_maintenance_items(self):
        self.menu_manage()
        (self.step(key='maintenance_item_delete', desc='删除')
         .step(key='maintenance_item_delete_verify', desc='确认删除')
         .wait())
        return self

    @reset_after_execution
    @doc(r_new_model_configuration)
    def new_model_configuration(self):
        self.menu_manage()
        (self.step(key='model_configuration', desc='机型配置')
         .step(key='new_model_configuration', desc='新增')
         .step(key='brand', desc='品牌')
         .custom(lambda: self.down_arrow_return(2))
         .step(key='model', desc='型号')
         .custom(lambda: self.down_arrow_return(3))
         .step(key='new_verify', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(r_delete_model_configuration)
    def delete_model_configuration(self):
        self.menu_manage()
        (self.step(key='model_configuration', desc='机型配置')
         .step(key='the_model_configuration_is_deleted', desc='删除')
         .step(key='delete_address_ok', desc='确认删除')
         .wait())
        return self
