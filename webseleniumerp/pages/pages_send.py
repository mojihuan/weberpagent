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


class HxV90Wh2Jkw(CommonPages):
    """送修管理|已送修物品"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='vogKAtlrXKX6r', desc='送修管理')
         .step(key='AuCUIakXn5303', desc='已送修物品')
         .wait())
        return self

    @reset_after_execution
    @doc(oaxztsMnbnAXzAxWj6JK)
    def oaxztsMnbnAXzAxWj6JK(self):
        self.menu_manage()
        (self.step(key='qe7q3WxKE6VaF', desc='单选')
         .step(key='U7ILHvMqELbqp', desc='送修完成')
         .scroll('cost_sending_repairs', desc='送修工费')
         .step(key='XGntkmAHGrX83', value='5', action='input', desc='送修工费')
         .scroll(key='cSgfbfNFlHMFK', desc='确定')
         .step(key='VWKlR9zlSFo24', desc='确定')
         .wait())
        return self


class B0rX5iYQN6L(CommonPages):
    """送修管理|送修单列表"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='AO5rox3MPyLv6', desc='送修管理')
         .step(key='eM6avohsgBGZZ', desc='送修单列表')
         .wait())
        return self

    @reset_after_execution
    @doc(woND08hYZ9lwms8Lse0i)
    def woND08hYZ9lwms8Lse0i(self):
        self.menu_manage()
        (self.step(key='zO97VnHOtYAWU', desc='送修工费结算')
         .step(key='hCrDd2Foa8qQ7', desc='付款账户')
         .custom(lambda: self.up_enter())
         .step(key='Nvxgmy8n9trFv', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(MKKvPqQBfeXIBJT3V5Jl)
    def MKKvPqQBfeXIBJT3V5Jl(self):
        self.menu_manage()
        (self.step(key='q2nspwTcyvcjC', desc='导出')
         .wait())
        return self


class Xt1lLWcjOv9(CommonPages):
    """送修管理|待送修物品"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='cwv4Y3VXZgHco', desc='送修管理')
         .step(key='TqRXNVau1w1vc', desc='待送修物品')
         .wait())
        return self

    @reset_after_execution
    @doc(FDe96kyUKHRoCJ6I7nfE)
    def FDe96kyUKHRoCJ6I7nfE(self):
        self.menu_manage()
        (self.step(key='MdScOGIYohsv2', desc='单选')
         .step(key='uFtJDEmJdJZqI', desc='送修出库')
         .step(key='D4fNykm9Nk1Un', desc='供应商')
         .custom(lambda: self.up_enter())
         .step(key='UL1tKhVjINL2G', value=self.jd, action='input', desc='物流单号')
         .step(key='nHSndjA3CsHo2', value=self.number, action='input', desc='物流费用')
         .step(key='TQJjOZhGEaZvs', value=self.serial, action='input', desc='送修原因')
         .step(key='UXKhi9DgIDUKH', desc='确认出库')
         .wait())
        return self
