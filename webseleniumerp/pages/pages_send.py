# coding: utf-8
import os
from config.settings import DATA_PATHS
from common.base_page import BasePage, ImportDataEdit, reset_after_execution
from common.import_desc import *


class CommonPages(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self._steps_queue = []
        self.file = ImportDataEdit(driver)
        self.file_paths = self.file.file_paths = {
            'excel': os.path.join(DATA_PATHS['excel'], 'send_repair_cost_import.xlsx'),
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


class SendBeenSentRepairPages(CommonPages):
    """送修管理|已送修物品"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='send_repair_manage_menu', desc='送修管理')
         .step(key='send_items_sent_for_repair_menu', desc='已送修物品')
         .wait())
        return self

    @reset_after_execution
    @doc(s_repair_completed_route)
    def repair_completed_route(self):
        self.menu_manage()
        (self.step(key='radio', desc='单选')
         .step(key='be_put_in_storage', desc='送修完成')
         .scroll('cost_sending_repairs', desc='送修工费')
         .step(key='cost_sending_repairs', value='5', action='input', desc='送修工费')
         .scroll(key='the_completion_of_the_repair_is_determined', desc='确定')
         .step(key='the_completion_of_the_repair_is_determined', desc='确定')
         .wait())
        return self


class SendRepairListPages(CommonPages):
    """送修管理-送修单列表"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='send_repair_manage_menu', desc='送修管理')
         .step(key='send_repair_single_list_menu', desc='送修单列表')
         .wait())
        return self

    @reset_after_execution
    @doc(s_repair_fee_settlement_paid)
    def repair_fee_settlement_paid(self):
        self.menu_manage()
        (self.step(key='labor_settlement', desc='送修工费结算')
         .step(key='send_payment_account', desc='付款账户')
         .custom(lambda: self.up_arrow_return())
         .step(key='send_settlement_verify', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(s_derived_data)
    def derived_data(self):
        self.menu_manage()
        (self.step(key='export', desc='导出')
         .wait())
        return self


class SendStayRepairPages(CommonPages):
    """送修管理-待送修物品"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='send_repair_manage_menu', desc='送修管理')
         .step(key='send_items_awaiting_receipt_menu', desc='待送修物品')
         .wait())
        return self

    @reset_after_execution
    @doc(s_send_out_for_repair)
    def send_out_for_repair(self):
        self.menu_manage()
        (self.step(key='stay_single_choice', desc='单选')
         .step(key='new_count', desc='送修出库')
         .step(key='supplier', desc='供应商')
         .custom(lambda: self.up_arrow_return())
         .step(key='material_flow', value=self.jd, action='input', desc='物流单号')
         .step(key='expense', value=self.number, action='input', desc='物流费用')
         .step(key='reason', value=self.serial, action='input', desc='送修原因')
         .step(key='confirmed_delivery', desc='确认出库')
         .wait())
        return self
