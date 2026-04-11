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
            'inventory_out_of_the_warehouse': os.path.join(DATA_PATHS['excel'], 'inventory_out_of_the_warehouse.xlsx'),
        }


class P5fs2CfGvgd(CommonPages):
    """库存管理|出库管理|地址管理"""

    def menu_manage(self):
        """菜单"""
        self.click(key='TivZw6ZuFnMui', desc='库存管理', tag='span')
        self.click(key='vhjxnngFi0VdD', desc='出库管理', tag='span')
        self.click(key='iBKH5ZNQv6P7M', desc='地址管理', tag='span')
        return self

    @reset_after_execution
    @doc(SJlFNv1wjIprgodoi79t)
    def SJlFNv1wjIprgodoi79t(self):
        self.menu_manage()
        self.click(key='nkzQD7a0A4oOB', desc='新增', tag='span')
        self.click(key='ca4Rv3sWxCLTI', desc='请选择业务类型', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新增')
        self.down_enter()
        self.input(key='FYImMUD4dVvzp', desc='长度不超过25个字符', text='姓名' + self.number, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新增')
        self.input(key='olxYcl4dzLUH4', desc='请输入手机号码', text=self.phone, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新增')
        self.click(key='fKupEkKbxSood', desc='请选择省/市/区/', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新增')
        self.down_right_right_enter()
        self.input(key='yBvdnvcrofPnz', desc='请输入详细地址', text='幸福路10号', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新增')
        self.input(key='VaWYpFsoVOmH2', desc='请输入坐标', text=INFO['coordinate'], tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新增')
        self.click(key='b4HYSLx4X5CqR', desc='确定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='新增')
        self.capture_api_request(url_keyword=self.URL['uyaeF0TZA'])
        return self

    @reset_after_execution
    @doc(CLneoMv0agHMlOvAteqD)
    def CLneoMv0agHMlOvAteqD(self):
        self.menu_manage()
        self.click(key='R4GjazlTYsJZu', desc='编辑', tag='span', p_tag='td', p_name='el-table_1_column_12   el-table__cell')
        self.input(key='MTYLo6IWhvARE', desc='请输入手机号码', text=self.phone, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='编辑')
        self.click(key='gKDE0epYLjJcw', desc='确定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='编辑')
        self.capture_api_request(url_keyword=self.URL['uyaeF0TZA'])
        return self

    @reset_after_execution
    @doc(VqptzJXhFGbWdaK6jWAT)
    def VqptzJXhFGbWdaK6jWAT(self):
        self.menu_manage()
        self.click(key='Erxd3Pt3N8YtQ', desc='删除', tag='span', p_tag='td', p_name='el-table_1_column_12   el-table__cell')
        self.click(key='ozyhrA6R1WVbE', desc='确定', tag='span', p_tag='div', p_name='el-message-box')
        self.capture_api_request(url_keyword=self.URL['IrUQf3u3u'])
        return self


class TkKTB87MJyz(CommonPages):
    """库存管理|移交接收管理|移交物品"""

    def menu_manage(self):
        """菜单"""
        self.click(key='EgrwllhVtC2Y6', desc='库存管理', tag='span')
        self.click(key='GlmqrWSCB26t8', desc='移交接收管理', tag='span')
        self.click(key='P5i8UmOczvR6f', desc='移交物品', tag='span')
        return self

    @reset_after_execution
    @doc(fcMGsTQ8oTnZfsCSP4CV)
    def fcMGsTQ8oTnZfsCSP4CV(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2)[0]['imei'])
        self.click(key='RVSoBvSWUGgUE', desc='请输入物品编号或者IMEI', tag='input')
        self.ctrl_v_enter()
        self.click(key='eWKJkxkjLdaTg', desc='移交', tag='span')
        self.click(key='VAPWmbgPFVN7h', desc='请选择接收人', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.down_enter()
        self.input(key='J4rM9WyA3CF7p', desc='请填写移交说明', text='备注', tag='textarea', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.click(key='A6qHoTgmCO2hf', desc='确定', tag='span', index=2, p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='移交')
        self.capture_api_request(url_keyword=self.URL['ShqXAnyJL'])
        return self

    @reset_after_execution
    @doc(RHctu5vyliQtE3nHTEWH)
    def RHctu5vyliQtE3nHTEWH(self):
        self.menu_manage()
        self.file.get_inventory_data('inventory_scan_code_transfer', 'imei', i=2, j=3)
        self.click(key='GOOYcxkO6Kr6Y', desc='导入物品', tag='span')
        self.upload_file(key='LA9H4gwqRyTDS', file_path=self.file_path('inventory_scan_code_transfer'))
        self.click(key='XuqSEbtvBhfet', desc='确定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='物品导入')
        self.click(key='qBnCPbatTc1EW', desc='搜索', tag='span')
        self.tab_space(5)
        self.click(key='wLazZXeKhm6I7', desc='移交', tag='span')
        self.click(key='kiNOlRw8w1flf', desc='请选择接收人', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.down_enter()
        self.input(key='HRdmXOGHxYLv5', desc='请填写移交说明', text='备注', tag='textarea', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.click(key='KEm8x1jYZ4sQx', desc='确定', tag='span', index=2, p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='移交')
        return self


class Ki45mAxGxif(CommonPages):
    """库存管理|入库管理|物品签收入库"""

    def menu_manage(self):
        """菜单"""
        self.click(key='neHHxHD8B3Ht9', desc='库存管理', tag='span')
        self.click(key='T75pA7dLcwK0K', desc='入库管理', tag='span')
        self.click(key='JxWGpGeNBW5i7', desc='物品签收入库', tag='span')
        return self

    @reset_after_execution
    @doc(cDYaPc16prs1VtJEU8mr)
    def cDYaPc16prs1VtJEU8mr(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=1)[0]['imei'])
        self.click(key='dWqxqlRiOFbBB', tag='input')
        self.ctrl_v_enter()
        self.click(key='kJBKT1CXo1XPn', tag='span')
        self.click(key='RbHgD3cNZT0HR', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='选择流转仓')
        self.down_enter()
        self.click(key='m9RapX1zIBXHA', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='选择流转仓')
        self.capture_api_request(url_keyword=self.URL['ShqXAnyJL'])
        return self

    @reset_after_execution
    @doc(DT5V5CR292DoOcng4DEh)
    def DT5V5CR292DoOcng4DEh(self):
        self.menu_manage()
        self.file.get_inventory_data('inventory_item_sign_in_enter_warehouse', 'imei', i=1)
        self.click(key='sANoxLsUJ2BQL', desc='导入入库物品', tag='span')
        self.upload_file(key='xrV3JajVyTbbO', file_path=self.file_path('inventory_item_sign_in_enter_warehouse'))
        self.click(key='aP5zGpNueGuV4', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='导入入库物品')
        self.click(key='zovpzoONjVWms', tag='span')
        self.tab_space(6)
        self.click(key='rEBfjCszjnDf3', tag='span')
        self.click(key='TGfXsbeusBzvH', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='选择流转仓')
        self.down_enter()
        self.click(key='WFunFAEa7mH8j', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='选择流转仓')
        return self


class IYYCOpmCVZS(CommonPages):
    """库存管理|库存列表"""

    def menu_manage(self):
        """菜单"""
        self.click(key='ylYiiiIVgnpm5', desc='库存管理', tag='span')
        self.click(key='CK6OSsg3VBWei', desc='库存列表', tag='span')
        return self

    @reset_after_execution
    @doc(vwwTH7A96EyxcdnCteFb)
    def vwwTH7A96EyxcdnCteFb(self):
        self.menu_manage()
        self.click(key='D1Vh7QmLvXoLZ', desc='@物品编号超链接', tag='span', p_tag='td', p_name='el-table_1_column_2   el-table__cell')
        self.click(key='G4U1RDU8gbdBE', desc='销售信息', tag='div', p_tag='div', p_name='el-tabs__nav is-top')
        self.click(key='wFKRqjJ1lTxin', desc='销售出库', tag='span', p_tag='div', p_name='el-card__body')
        self.click(key='Fk4UfrqIp1LRc', desc='请选择销售客户', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售出库')
        self.down_enter(2)
        self.click(key='UAbyteUfSWHRV', desc='已收款', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售出库')
        self.input(key='dmP9rwZpN5XWW', desc='请输入物流单号', text=self.sf, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售出库')
        self.input(key='h9thgZRSA9tj4', desc='请输入物流费用', text='12', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售出库')
        self.input(key='VNjbBzSNDWS7B', desc='请输入销售价', text='200', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售出库')
        self.input(key='BPtqtLGXYVt10', desc='请输入平台物品编号(销售)', text=self.serial, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售出库')
        self.input(key='up7zUVdGPxWzA', desc='请输入平台销售单号', text=self.serial, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售出库')
        self.scroll(element='')
        self.click(key='OPkDkF3u7trzU', desc='确定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='销售出库')
        self.capture_api_request(url_keyword=self.URL['JKSmt0DQk'])
        return self

    @reset_after_execution
    @doc(ZUfg9nnQSfSaV9zvenlZ)
    def ZUfg9nnQSfSaV9zvenlZ(self):
        self.menu_manage()
        self.click(key='MEkUslH4zgiZg', desc='@物品编号超链接', tag='span', p_tag='td', p_name='el-table_1_column_2   el-table__cell')
        self.click(key='unv7NAhSssb8H', desc='销售信息', tag='div', p_tag='div', p_name='el-tabs__nav is-top')
        self.click(key='Y0jSgD54oG5lF', desc='销售出库', tag='span', p_tag='div', p_name='el-card__body')
        self.click(key='OVPZqoG78j4N0', desc='请选择销售客户', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售出库')
        self.down_enter(2)
        self.click(key='R3ZQKPik7WDcH', desc='未收款', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售出库')
        self.input(key='pEbbLvTPDvlnz', desc='请输入物流单号', text=self.sf, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售出库')
        self.input(key='Q89T01eDyAAuY', desc='请输入物流费用', text='12', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售出库')
        self.input(key='TnYC4OcHj9PoX', desc='请输入销售价', text='200', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售出库')
        self.input(key='O5IsY8RpDwPqO', desc='请输入平台物品编号(销售)', text=self.serial, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售出库')
        self.input(key='x5VG3FgsSaahs', desc='请输入平台销售单号', text=self.serial, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售出库')
        self.scroll(element='')
        self.click(key='OTm8v0ZS5tn5d', desc='确定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='销售出库')
        self.capture_api_request(url_keyword=self.URL['JKSmt0DQk'])
        return self

    @reset_after_execution
    @doc(YyjrBFFVlBe4IC7IrZyD)
    def YyjrBFFVlBe4IC7IrZyD(self):
        self.menu_manage()
        self.click(key='RTdwQVVtw0A05', desc='请选择物品状态', tag='input')
        self.down_enter(9)
        self.click(key='JHTpUgZTeOmMS', desc='请选择库存状态', tag='input')
        self.up_enter()
        self.click(key='QUOTthQddyBGf', desc='搜索', tag='span')
        self.click(key='big9UfobBTkyv', desc='@物品编号超链接', tag='span', p_tag='td', p_name='el-table_1_column_2   el-table__cell')
        self.click(key='KM7ZDFoYmuAz1', desc='销售信息', tag='div', p_tag='div', p_name='el-tabs__nav is-top')
        self.click(key='RJ67V8HeYBl7l', desc='销售售后', tag='span', p_tag='div', p_name='el-card__body')
        self.click(key='U9mZlKIINLyaM', desc='退货', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.click(key='SPOti7fYg4mqM', desc='请选择入库流转仓', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.down_enter()
        self.input(key='X3dehfXc7BINf', desc='请输入', tag='textarea', text='备注', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.scroll(element='')
        self.click(key='zKAHOnkVQUy4Q', desc='确 定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='销售售后')
        self.capture_api_request(url_keyword=self.URL['NeFj1qYw3'])
        return self

    @reset_after_execution
    @doc(AAfxCTv9LmUzH4gFJKoE)
    def AAfxCTv9LmUzH4gFJKoE(self):
        self.menu_manage()
        self.click(key='MCU9rFEOF0z0t', desc='请选择物品状态', tag='input')
        self.down_enter(9)
        self.click(key='IBJt4rqASIB5t', desc='请选择库存状态', tag='input')
        self.up_enter()
        self.click(key='C8kcp40tcyOo5', desc='搜索', tag='span')
        self.click(key='pAWlEgeeyq1Bz', desc='@物品编号超链接', tag='span', p_tag='td', p_name='el-table_1_column_2   el-table__cell')
        self.click(key='suodkdG0Eu86d', desc='销售信息', tag='div', p_tag='div', p_name='el-tabs__nav is-top')
        self.click(key='bE99VSfn1sfUN', desc='销售售后', tag='span', p_tag='div', p_name='el-card__body')
        self.click(key='qlIAC6EEsRoMq', desc='退货', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.click(key='AU5l8JmYVRXp1', desc='自提', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.click(key='G5kNRxhZAa28F', desc='请选择入库流转仓', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.down_enter()
        self.input(key='zZXJnyGIZcMJb', desc='请输入', tag='textarea', text='备注', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.scroll(element='')
        self.click(key='HSBndMt54MmFL', desc='确 定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='销售售后')
        self.capture_api_request(url_keyword=self.URL['NeFj1qYw3'])
        return self

    @reset_after_execution
    @doc(kzLjwWovXH0gNxfbTWCC)
    def kzLjwWovXH0gNxfbTWCC(self):
        self.menu_manage()
        self.click(key='t2ln69Jl8lvzY', desc='请选择物品状态', tag='input')
        self.down_enter(9)
        self.click(key='P4J7ni3RbiNTu', desc='请选择库存状态', tag='input')
        self.up_enter()
        self.click(key='wT9XnjQLCUX8v', desc='搜索', tag='span')
        self.click(key='YMhW6dDAiGvSG', desc='@物品编号超链接', tag='span', p_tag='td', p_name='el-table_1_column_2   el-table__cell')
        self.click(key='OEY3FPltPP0ii', desc='销售信息', tag='div', p_tag='div', p_name='el-tabs__nav is-top')
        self.click(key='xXvYeF4wnCCcL', desc='销售售后', tag='span', p_tag='div', p_name='el-card__body')
        self.click(key='W3Ee1WUeBW2Dw', desc='退货', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.click(key='isbmnZkc9OXaG', desc='未收货', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.input(key='Bm9Pi74J0Ye5B', desc='请填写物流单号', tag='input', text=self.sf, p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.input(key='VcrERmMvqb1H8', desc='请输入', tag='textarea', text='备注', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.scroll(element='')
        self.click(key='xtvqRJnZG6Cjj', desc='确 定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='销售售后')
        self.capture_api_request(url_keyword=self.URL['NeFj1qYw3'])
        return self

    @reset_after_execution
    @doc(SyHpEVSfWeSWPDH9hcUa)
    def SyHpEVSfWeSWPDH9hcUa(self):
        self.menu_manage()
        self.click(key='XUh3k6MxuZ7E7', desc='请选择物品状态', tag='input')
        self.down_enter(9)
        self.click(key='Fg1U5UPrOZbfN', desc='请选择库存状态', tag='input')
        self.up_enter()
        self.click(key='dHNzYzrCHpi52', desc='搜索', tag='span')
        self.click(key='srRATfZPSF5Ru', desc='@物品编号超链接', tag='span', p_tag='td', p_name='el-table_1_column_2   el-table__cell')
        self.click(key='ORaD4BPyUkKG7', desc='销售信息', tag='div', p_tag='div', p_name='el-tabs__nav is-top')
        self.click(key='Seb5rjMfmTAJb', desc='销售售后', tag='span', p_tag='div', p_name='el-card__body')
        self.click(key='nE8gADNVNcPF4', desc='退货', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.click(key='P0aNusil6Yrw0', desc='自提', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.click(key='pQa3fJQOX4CNW', desc='未收货', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.input(key='smRgn7kCmDC5E', desc='请输入', tag='textarea', text='备注', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.scroll(element='')
        self.click(key='BVxiR2Sle6IUf', desc='确 定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='销售售后')
        self.capture_api_request(url_keyword=self.URL['NeFj1qYw3'])
        return self

    @reset_after_execution
    @doc(VCS0Uc7dtvSPIuHtNbaI)
    def VCS0Uc7dtvSPIuHtNbaI(self):
        self.menu_manage()
        self.click(key='f2Mz25kPbpcdp', desc='请选择物品状态', tag='input')
        self.down_enter(9)
        self.click(key='hXYBreUNJtSGq', desc='请选择库存状态', tag='input')
        self.up_enter()
        self.click(key='LY3VAXK9At6zb', desc='搜索', tag='span')
        self.click(key='dh6GMo9STzlAK', desc='@物品编号超链接', tag='span', p_tag='td', p_name='el-table_1_column_2   el-table__cell')
        self.click(key='KRW2CGpZOKO7B', desc='销售信息', tag='div', p_tag='div', p_name='el-tabs__nav is-top')
        self.click(key='AyNRDLcN6Jewl', desc='销售售后', tag='span', p_tag='div', p_name='el-card__body')
        self.click(key='AfSKLEh3UQjYg', desc='仅退配件', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.input(key='wZYoM8Om8ODIj', desc='请输入新销售结算价', text='230', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.click(key='jCuqdrIoyixck', desc='请选择配件分类', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.down_enter(2)
        self.click(key='NMuqmxHoArPXn', desc='请选择配件名称', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.down_enter(2)
        self.click(key='eyWm8vJdfhTjs', desc='请选择品牌', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.down_enter()
        self.click(key='CigCjNPFekO97', desc='请选择型号', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.down_enter()
        self.input(key='QMBa1a1k5BTog', desc='请输入配件价值', text='300', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.click(key='eL40nRyWMAcgV', desc='请选择入库流转仓', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.down_enter()
        self.input(key='v4xwhzDXIUj7R', desc='请输入', tag='textarea', text='备注', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.scroll(element='')
        self.click(key='x4k6FulNA9oIU', desc='确 定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='销售售后')
        self.capture_api_request(url_keyword=self.URL['NeFj1qYw3'])
        return self

    @reset_after_execution
    @doc(HNDvVgQsF5uXmqKb3obN)
    def HNDvVgQsF5uXmqKb3obN(self):
        self.menu_manage()
        self.click(key='nGMYIijdWwJvS', desc='请选择物品状态', tag='input')
        self.down_enter(9)
        self.click(key='SGqu6LPqEf6Mo', desc='请选择库存状态', tag='input')
        self.up_enter()
        self.click(key='k4tvB0fyx5Hcn', desc='搜索', tag='span')
        self.click(key='gjbQQGAmHsad2', desc='@物品编号超链接', tag='span', p_tag='td', p_name='el-table_1_column_2   el-table__cell')
        self.click(key='raNhP0L7DhpKz', desc='销售信息', tag='div', p_tag='div', p_name='el-tabs__nav is-top')
        self.click(key='xul6QHHBryG27', desc='销售售后', tag='span', p_tag='div', p_name='el-card__body')
        self.click(key='BwncaUfIdo2Ez', desc='仅退配件', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.input(key='pdOVSvWY5kFEG', desc='请输入新销售结算价', text='230', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.click(key='jmFfjt8OmM2K8', desc='请选择配件分类', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.down_enter(2)
        self.click(key='QOJFfmui4nHe4', desc='请选择配件名称', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.down_enter(2)
        self.click(key='rwcfe35bL5SqC', desc='请选择品牌', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.down_enter()
        self.click(key='kuPUDoMLN1LRY', desc='请选择型号', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.down_enter()
        self.input(key='lapjAyCt92g2Z', desc='请输入配件价值', text='300', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.click(key='tgPeSV4C91hEw', desc='未收货', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.input(key='VUxgIriUlnKMv', desc='请填写物流单号', text=self.sf, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.input(key='v0TL4MPwkWcEw', desc='请输入', tag='textarea', text='备注', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.scroll(element='')
        self.click(key='efQIqmKr7yXA4', desc='确 定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='销售售后')
        self.capture_api_request(url_keyword=self.URL['NeFj1qYw3'])
        return self

    @reset_after_execution
    @doc(Nk7bVBssIb2JEsWwVc2R)
    def Nk7bVBssIb2JEsWwVc2R(self):
        self.menu_manage()
        self.click(key='RRHk6nmFup7vA', desc='请选择物品状态', tag='input')
        self.down_enter(9)
        self.click(key='mXpD1YnUh24F9', desc='请选择库存状态', tag='input')
        self.up_enter()
        self.click(key='QaNhJv5zbbI9K', desc='搜索', tag='span')
        self.click(key='pe9OVk5rySh7G', desc='@物品编号超链接', tag='span', p_tag='td', p_name='el-table_1_column_2   el-table__cell')
        self.click(key='Kgwafb8eyBeuW', desc='销售信息', tag='div', p_tag='div', p_name='el-tabs__nav is-top')
        self.click(key='bRLUBXVCdgJyp', desc='销售售后', tag='span', p_tag='div', p_name='el-card__body')
        self.click(key='vFLJTQBeqkEn1', desc='调价', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.input(key='tWH6lD3Ekrkph', desc='请输入新销售结算价', text='221', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.input(key='H3vSBJ3EwCO6D', desc='请输入', tag='textarea', text='备注', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='销售售后')
        self.scroll(element='')
        self.click(key='TQrjaCWJAHdvH', desc='确 定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='销售售后')
        self.capture_api_request(url_keyword=self.URL['NeFj1qYw3'])
        return self

    @reset_after_execution
    @doc(D60ATnrNOPRjZtH7QJQv)
    def D60ATnrNOPRjZtH7QJQv(self):
        self.menu_manage()
        self.click(key='diX5llbFClFXZ', desc='请选择物品状态', tag='input')
        self.down_enter(2)
        self.click(key='oBv0s9ilbpl4L', desc='请选择库存状态', tag='input')
        self.down_enter()
        self.click(key='tF0l6Au73l1kF', desc='搜索', tag='span')
        self.click(key='LhlQyZlyX3FGG', desc='@物品编号超链接', tag='span', p_tag='td', p_name='el-table_1_column_2   el-table__cell')
        self.click(key='dJ2YoSacwrLft', desc='采购信息', tag='div', p_tag='div', p_name='el-tabs__nav is-top')
        self.click(key='jBPTWX8e6tiKX', desc='采购售后', tag='span', p_tag='div', p_name='el-card__body')
        self.input(key='wodHGzzSqf8Jf', desc='请输入备注', tag='textarea', text='备注', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='采购售后')
        self.click(key='PVaj34qaErm0J', desc='确 定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='采购售后')
        self.capture_api_request(url_keyword=self.URL['R7HA7rwAV'])
        return self

    @reset_after_execution
    @doc(KgeXqOhDT97S9ajhSDxB)
    def KgeXqOhDT97S9ajhSDxB(self):
        self.menu_manage()
        self.click(key='CbjIyDsWLeEjX', desc='@修改图标', tag='i', p_tag='td', p_name='el-table_1_column_7   el-table__cell')
        self.click(key='J7GFUCdgReMcI', desc='确 定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='物品信息修改')
        self.capture_api_request(url_keyword=self.URL['R31Db9DLe'])
        return self

    @reset_after_execution
    @doc(n6qVaJNnhR6yKFZDvMpU)
    def n6qVaJNnhR6yKFZDvMpU(self):
        self.menu_manage()
        self.click(key='U4I46U9eioVoJ', desc='搜索', tag='span', p_tag='div', p_name='flex-center formButtons')
        self.tab_space(7)
        self.click(key='PER07mVsH9aLv', desc='批量移交', tag='span')
        self.click(key='rhDEJ2Z9vjnlD', desc='采购售后', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.click(key='foeIz1Xupc4eU', desc='请选择接收人', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.down_enter(2)
        self.input(key='EH151J9nYsQJz', desc='请填写移交说明', tag='textarea', text='备注', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.click(key='cM4DxY34tJQV9', desc='确定', tag='span', p_tag='div', index=2, p_name='el-dialog__footer', o_tag='div', o_name='移交')
        self.capture_api_request(url_keyword=self.URL['ShqXAnyJL'])
        return self

    @reset_after_execution
    @doc(wWBLmKauWABXgA16zGq5)
    def wWBLmKauWABXgA16zGq5(self):
        self.menu_manage()
        self.click(key='WRrlCXBERXOeT', desc='搜索', tag='span', p_tag='div', p_name='flex-center formButtons')
        self.tab_space(7)
        self.click(key='wcuysCO0gKIkc', desc='批量移交', tag='span')
        self.click(key='jvTPzAZLVovBS', desc='质检', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.click(key='NiVA3wz2WBFEC', desc='请选择接收人', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.down_enter(2)
        self.input(key='LpKcJ30k5omSA', desc='请填写移交说明', tag='textarea', text='备注', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.click(key='pPxKWgs0CcIvS', desc='确定', tag='span', p_tag='div', index=2, p_name='el-dialog__footer', o_tag='div', o_name='移交')
        self.capture_api_request(url_keyword=self.URL['ShqXAnyJL'])
        return self

    @reset_after_execution
    @doc(D3dsNkrEsGlGWkoAbUvn)
    def D3dsNkrEsGlGWkoAbUvn(self):
        self.menu_manage()
        self.click(key='aerHADVSIxovP', desc='搜索', tag='span', p_tag='div', p_name='flex-center formButtons')
        self.tab_space(7)
        self.click(key='Jh7Y9PtfvmWaw', desc='批量移交', tag='span')
        self.click(key='qyEbP2iMtQuKy', desc='维修', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.click(key='K91fm1xeRFExu', desc='请选择接收人', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.down_enter(2)
        self.input(key='IyvV3XbVQI8hU', desc='请填写移交说明', tag='textarea', text='备注', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.click(key='d93lkwfh2XG7q', desc='确定', tag='span', p_tag='div', index=2, p_name='el-dialog__footer', o_tag='div', o_name='移交')
        self.capture_api_request(url_keyword=self.URL['ShqXAnyJL'])
        return self

    @reset_after_execution
    @doc(BqEQ0BTtXXYnqUFLxnUK)
    def BqEQ0BTtXXYnqUFLxnUK(self):
        self.menu_manage()
        self.click(key='cmfoqYmsnOdNE', desc='搜索', tag='span', p_tag='div', p_name='flex-center formButtons')
        self.tab_space(7)
        self.click(key='TgFXEIOLKTJyk', desc='批量移交', tag='span')
        self.click(key='jWF4jCQAgxShM', desc='销售', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.click(key='ZBoFlEN7SW9nY', desc='请选择接收人', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.down_enter(2)
        self.input(key='cmIDXENb4EpmM', desc='请填写移交说明', tag='textarea', text='备注', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.click(key='bJAGAUu7NVyfD', desc='确定', tag='span', p_tag='div', index=2, p_name='el-dialog__footer', o_tag='div', o_name='移交')
        self.capture_api_request(url_keyword=self.URL['ShqXAnyJL'])
        return self

    @reset_after_execution
    @doc(xrzuFX14hLZb53t2Dpl4)
    def xrzuFX14hLZb53t2Dpl4(self):
        self.menu_manage()
        self.click(key='BFw91ALiEug6Y', desc='搜索', tag='span', p_tag='div', p_name='flex-center formButtons')
        self.tab_space(7)
        self.click(key='ljM8L0lWThmOy', desc='批量移交', tag='span')
        self.click(key='SXRtm1m4EAbr0', desc='送修', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.click(key='v3vLCRIeJE3qo', desc='请选择接收人', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.down_enter(2)
        self.input(key='IqsfiALzkX0Zx', desc='请填写移交说明', tag='textarea', text='备注', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.click(key='wZl3lndt1xzKP', desc='确定', tag='span', p_tag='div', index=2, p_name='el-dialog__footer', o_tag='div', o_name='移交')
        self.capture_api_request(url_keyword=self.URL['ShqXAnyJL'])
        return self

    @reset_after_execution
    @doc(ELzKzsnP7DBzS58RhuRV)
    def ELzKzsnP7DBzS58RhuRV(self):
        self.menu_manage()
        self.click(key='vDdhzPlLW1LgH', desc='搜索', tag='span', p_tag='div', p_name='flex-center formButtons')
        self.tab_space(7)
        self.click(key='jFrJWzFDk4SYw', desc='批量移交', tag='span')
        self.click(key='I0gft00pKw6it', desc='采购售后', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.click(key='dwYNURvP9otmh', desc='请选择接收人', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.down_enter()
        self.input(key='ntNixVG2MMDSR', desc='请填写移交说明', tag='textarea', text='备注', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.click(key='sOtKi4upztehk', desc='确定', tag='span', p_tag='div', index=2, p_name='el-dialog__footer', o_tag='div', o_name='移交')
        self.capture_api_request(url_keyword=self.URL['ShqXAnyJL'])
        return self

    @reset_after_execution
    @doc(yPtmSmB6LgGBHuYKQex9)
    def yPtmSmB6LgGBHuYKQex9(self):
        self.menu_manage()
        self.click(key='S3C13cp37ydd7', desc='搜索', tag='span', p_tag='div', p_name='flex-center formButtons')
        self.tab_space(7)
        self.click(key='y2cB0K33KWbCN', desc='批量移交', tag='span')
        self.click(key='NiLT00mTDJGbB', desc='质检', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.click(key='pLYu6gnesDNDH', desc='请选择接收人', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.down_enter()
        self.input(key='bTAlTaA6BVYfB', desc='请填写移交说明', tag='textarea', text='备注', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.click(key='afBwz4ryRmJr4', desc='确定', tag='span', p_tag='div', index=2, p_name='el-dialog__footer', o_tag='div', o_name='移交')
        self.capture_api_request(url_keyword=self.URL['ShqXAnyJL'])
        return self

    @reset_after_execution
    @doc(cQRfPcjML2Pxryt529f9)
    def cQRfPcjML2Pxryt529f9(self):
        self.menu_manage()
        self.click(key='cYBLAs0Os6137', desc='搜索', tag='span', p_tag='div', p_name='flex-center formButtons')
        self.tab_space(7)
        self.click(key='KfhYd5RBzTMfT', desc='批量移交', tag='span')
        self.click(key='MTQXS0dwjvdQb', desc='维修', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.click(key='cYkqK0efSWVls', desc='请选择接收人', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.down_enter()
        self.input(key='iiTt4qCxYm1sh', desc='请填写移交说明', tag='textarea', text='备注', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.click(key='ziPeZdTV8gMAg', desc='确定', tag='span', p_tag='div', index=2, p_name='el-dialog__footer', o_tag='div', o_name='移交')
        self.capture_api_request(url_keyword=self.URL['ShqXAnyJL'])
        return self

    @reset_after_execution
    @doc(cZDVh5eyHxStC2Mli9DI)
    def cZDVh5eyHxStC2Mli9DI(self):
        self.menu_manage()
        self.click(key='zugrZnJOUlJEx', desc='搜索', tag='span', p_tag='div', p_name='flex-center formButtons')
        self.tab_space(7)
        self.click(key='DJLnzpzu79kBX', desc='批量移交', tag='span')
        self.click(key='lkNxccWUMM0rO', desc='销售', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.click(key='x4ljwMGny5dZt', desc='请选择接收人', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.down_enter()
        self.input(key='qQAvuf6ibQULL', desc='请填写移交说明', tag='textarea', text='备注', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.click(key='Y18YXaf1hODMV', desc='确定', tag='span', p_tag='div', index=2, p_name='el-dialog__footer', o_tag='div', o_name='移交')
        self.capture_api_request(url_keyword=self.URL['ShqXAnyJL'])
        return self

    @reset_after_execution
    @doc(OAvKjuICy5p7SX9qfvX4)
    def OAvKjuICy5p7SX9qfvX4(self):
        self.menu_manage()
        self.click(key='smHFxVctT0390', desc='搜索', tag='span', p_tag='div', p_name='flex-center formButtons')
        self.tab_space(7)
        self.click(key='rk91VncsKW95g', desc='批量移交', tag='span')
        self.click(key='bMwOuKzaJq3Lt', desc='送修', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.click(key='RV3c5MOkT3Vyb', desc='请选择接收人', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.down_enter()
        self.input(key='IdRmTQkivxlOs', desc='请填写移交说明', tag='textarea', text='备注', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='移交')
        self.click(key='nd0JF7kqC8VyB', desc='确定', tag='span', p_tag='div', index=2, p_name='el-dialog__footer', o_tag='div', o_name='移交')
        self.capture_api_request(url_keyword=self.URL['ShqXAnyJL'])
        return self


class RIG4KKAJOQP(CommonPages):
    """库存管理|入库管理|物流签收入库"""

    def menu_manage(self):
        """菜单"""
        self.click(key='Z1MVcuuBAilDZ', desc='库存管理', tag='span')
        self.click(key='D0JMNzrKAW3xy', desc='入库管理', tag='span')
        self.click(key='j3mKxRlEAjCZ6', desc='物流列表', tag='span', index=2)
        return self

    @reset_after_execution
    @doc(Jv79uDAMnGFSvRHesu0B)
    def Jv79uDAMnGFSvRHesu0B(self):
        self.menu_manage()
        self.scroll(element='')
        self.click(key='LtNaawnXrLGyN', desc='包裹详情', tag='span', p_tag='td', p_name='el-table_1_column_11   el-table__cell')
        self.click(key='rJTH066h3auQ6', tag='span')
        self.tab_space(6)
        self.click(key='JnrnrHVeF6L71', tag='span')
        self.click(key='ElsEbPFrStIhe', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='选择流转仓')
        self.down_enter()
        self.click(key='GfPF2tDVRa3oU', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='选择流转仓')
        self.capture_api_request(url_keyword=self.URL['DYbHAZqxU'])
        return self

    @reset_after_execution
    @doc(hhbi3Grk7w3kXVnHxfNE)
    def hhbi3Grk7w3kXVnHxfNE(self):
        self.menu_manage()
        self.scroll(element='')
        self.click(key='tsoNJClgaTUEm', desc='包裹详情', tag='span', p_tag='td', p_name='el-table_1_column_11   el-table__cell')
        self.click(key='nKugBMQGa9aUq', tag='span')
        self.tab_space(6)
        self.click(key='ELUufbAnMWdPF', tag='span')
        self.click(key='mQ7p69b1aW2J5', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='选择流转仓')
        self.down_enter()
        self.click(key='VdGCyv0ZDpr9Z', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='选择流转仓')
        self.capture_api_request(url_keyword=self.URL['DYbHAZqxU'])
        return self


class XgQm1C4a0op(CommonPages):
    """库存管理|出库管理|仅出库订单列表"""

    def menu_manage(self):
        """菜单"""
        self.click(key='qdZ0iWN2bQuEJ', desc='库存管理', tag='span')
        self.click(key='CxqlozhV6GNQN', desc='出库管理', tag='span')
        self.scroll(element='')
        self.click(key='Ub8yoGEdmgcaE', desc='仅出库订单列表', tag='span')
        return self

    @reset_after_execution
    @doc(e2AnAaVdqHxAw7jEV92t)
    def e2AnAaVdqHxAw7jEV92t(self):
        self.menu_manage()
        self.click(key='nVIxrzcpI7jSu', desc='搜索', tag='span')
        self.tab_space(8)
        self.click(key='HzetRQSJYQ96r', desc='出库物品退回', tag='span')
        self.input(key='sGNM2i0sVrkGb', desc='请输入物流单号', text=self.sf, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='出库物品退回')
        self.click(key='lVujsrHEpJjho', desc='请选择仓库', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='出库物品退回')
        self.down_enter()
        self.input(key='C0PVsE7GLfQPu', desc='请输入备注', text='备注', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='出库物品退回')
        self.click(key='yzIqqdjFlpAfe', desc='确定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='出库物品退回')
        self.capture_api_request(url_keyword=self.URL['gNp2tTkFA'])
        return self

    @reset_after_execution
    @doc(M04F4OTZMxDuTL4I0abo)
    def M04F4OTZMxDuTL4I0abo(self):
        self.menu_manage()
        self.click(key='cspD0zh9oiWrB', desc='搜索', tag='span')
        self.tab_space(8)
        self.click(key='SEkByuP0LxWCi', desc='出库物品退回', tag='span')
        self.click(key='D6njKStHqVuRa', desc='退回在途', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='出库物品退回')
        self.input(key='fYBJrDRzxHIgU', desc='请输入物流单号', text=self.sf, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='出库物品退回')
        self.input(key='U8q05QmfjN3Vb', desc='请输入备注', text='备注', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='出库物品退回')
        self.click(key='ykUBK3QkP3p4f', desc='确定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='出库物品退回')
        self.capture_api_request(url_keyword=self.URL['gNp2tTkFA'])
        return self

    @reset_after_execution
    @doc(AfpbFoR3N3DHrELC3fyQ)
    def AfpbFoR3N3DHrELC3fyQ(self):
        self.menu_manage()
        self.click(key='mAG27cqFDs0DA', desc='搜索', tag='span')
        self.tab_space(8)
        self.click(key='R6u7WrAdHpJUP', desc='仅出库销售', tag='span')
        self.click(key='MMMj0rl9L4mev', desc='请选择收款账户', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='物品销售')
        self.down_enter()
        self.input(key='vi7immkEAtTVQ', desc='请输入销售价', text='122', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='物品销售')
        self.input(key='L9oJyYt8KlvFk', desc='请输入平台销售订单号', text=self.serial, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='物品销售')
        self.click(key='axWzy572ooBQD', desc='确定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='物品销售')
        self.capture_api_request(url_keyword=self.URL['AXLzdlBvg'])
        return self

    @reset_after_execution
    @doc(x4yuI0I1abq0vQb0mI6o)
    def x4yuI0I1abq0vQb0mI6o(self):
        self.menu_manage()
        self.click(key='sIHNtVwBzhEcK', desc='搜索', tag='span')
        self.tab_space(8)
        self.click(key='Rc16n1To2tdln', desc='仅出库销售', tag='span')
        self.click(key='ANAn81vHdDqj5', desc='未收款', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='物品销售')
        self.input(key='R2HIzg5ziNXoD', desc='请输入销售价', text='122', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='物品销售')
        self.input(key='P6I3sOCdHc6il', desc='请输入平台销售订单号', text=self.serial, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='物品销售')
        self.click(key='hrua4jcpi84nA', desc='确定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='物品销售')
        self.capture_api_request(url_keyword=self.URL['AXLzdlBvg'])
        return self

    @reset_after_execution
    @doc(ZUdNkyxThIMbrQMjq4A0)
    def ZUdNkyxThIMbrQMjq4A0(self):
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2)[0]['imei'])
        self.menu_manage()
        self.click(key='hy1u0Z4eUxa1a', desc='新建订单', tag='span')
        self.click(key='PiKpuIXL5w9k0', desc='请选择客户', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新建仅出库订单')
        self.down_enter(2)
        self.input(key='wFo3FkPG9gahm', desc='请输入备注', text='备注', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新建仅出库订单')
        self.input(key='AJANlJhubnZz2', desc='请输入物流单号', text=self.sf, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新建仅出库订单')
        self.input(key='A3KjvUa2PSJUz', desc='请输入物流费用', text='22', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新建仅出库订单')
        self.click(key='BG5KhNxIPMxCd', desc='扫码物品编号/IMEI/平台物品编号', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新建仅出库订单')
        self.ctrl_v()
        self.click(key='Q1ZdSdidmxHX2', desc='添加', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新建仅出库订单')
        self.click(key='iuNUZPUJkoQgk', desc='确定', index=3, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='新建仅出库订单')
        self.capture_api_request(url_keyword=self.URL['hgftWOpCZ'])
        return self

    @reset_after_execution
    @doc(qawEHf7WaxftnDj1QxYR)
    def qawEHf7WaxftnDj1QxYR(self):
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2)[0]['imei'])
        self.menu_manage()
        self.click(key='LGqItLrjExIZg', desc='新建订单', tag='span')
        self.click(key='mpDLPnsRcccKS', desc='请选择客户', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新建仅出库订单')
        self.down_enter(2)
        self.input(key='XEC6kC4Y8cWnG', desc='请输入备注', text='备注', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新建仅出库订单')
        self.click(key='xOGkZ2BzBHorj', desc='扫码物品编号/IMEI/平台物品编号', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新建仅出库订单')
        self.ctrl_v()
        self.click(key='aAvcR99YeNM5C', desc='添加', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新建仅出库订单')
        self.click(key='OrqKB1m9STXLL', desc='@快递易图标开关', tag='span', p_tag='div', p_name='el-switch')
        self.click(key='jqPqKEHiSusn9', desc='计算运费', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新建仅出库订单')
        self.scroll(element='')
        self.click(key='iSReVUUZkkuwU', desc='确定', index=3, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='新建仅出库订单')
        self.capture_api_request(url_keyword=self.URL['hgftWOpCZ'])
        return self

    @reset_after_execution
    @doc(KYUijzA3uVmyde4KtozB)
    def KYUijzA3uVmyde4KtozB(self):
        self.file.get_inventory_data('inventory_out_of_the_warehouse', 'imei', i=2)
        self.menu_manage()
        self.click(key='wMN9umJussjWN', desc='新建订单', tag='span')
        self.click(key='WyRGdvws5zsuf', desc='导入添加', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新建仅出库订单')
        self.upload_file(key='DbCNFSvHQGR04', file_path=self.file_path('inventory_out_of_the_warehouse'))
        self.click(key='qmV7MfsnYts0y', desc='确定', tag='span', index=2, p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='物品信息导入')
        self.click(key='OfhNlSAB9regP', desc='请选择客户', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新建仅出库订单')
        self.down_enter(2)
        self.input(key='Cv5FK6k5yIUrA', desc='请输入备注', text='备注', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新建仅出库订单')
        self.input(key='Ptsh2YHVk6Yf8', desc='请输入物流单号', text=self.sf, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新建仅出库订单')
        self.input(key='JPwMQ6NK3BUBZ', desc='请输入物流费用', text='22', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新建仅出库订单')
        self.click(key='IPqcvOdJcLoG1', desc='确定', index=3, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='新建仅出库订单')
        return self


class GmJWeaS0RSp(CommonPages):
    """库存管理|出库管理|采购售后出库"""

    def menu_manage(self):
        """菜单"""
        self.click(key='YFAP3xcn52fNn', desc='库存管理', tag='span')
        self.click(key='bRUr4F3ELp78k', desc='出库管理', tag='span')
        self.click(key='Agwt5FdBf2my9', desc='采购售后出库', tag='span')
        return self

    @reset_after_execution
    @doc(DZpllRLFofze0dkHhqfW)
    def DZpllRLFofze0dkHhqfW(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2)[0]['imei'])
        self.input(key='F157W8Z62I6TB', desc='请填写物流单号', text=self.sf, tag='input')
        self.input(key='yxG2lpKBXaROa', desc='请输入物流费用', text='12', tag='input')
        self.click(key='z5W4DrGgdY5ul', desc='请输入物品编号或者IMEI', tag='input')
        self.ctrl_v()
        self.click(key='CyPvjbD15ajuX', desc='添加', tag='span')
        self.click(key='TzMPy9Gw9okBo', desc='确认出库', tag='span')
        self.capture_api_request(url_keyword=self.URL['TDNsMZDYJ'])
        return self

    @reset_after_execution
    @doc(I19nPSWAdkZLyMrB5dfG)
    def I19nPSWAdkZLyMrB5dfG(self):
        self.menu_manage()
        self.file.get_inventory_data('purchase_post_sale_out_warehouse', 'imei', i=2, j=10)
        self.input(key='xVu6JURAw0xGQ', desc='请填写物流单号', text=self.sf, tag='input')
        self.input(key='dpNMQ24yHITgF', desc='请输入物流费用', text='12', tag='input')
        self.click(key='ZJ5D1mL0nMBo7', desc='IMEI导入', tag='span')
        self.upload_file(key='AbJuju42JYmKx', file_path=self.file_path('purchase_post_sale_out_warehouse'))
        self.click(key='Setni2imWNTE2', desc='确定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='IMEI模板导入')
        self.click(key='UZLrxgIKxQXRZ', desc='确认出库', tag='span')
        return self


class GlsOxUhDpKZ(CommonPages):
    """库存管理|移交接收管理|接收物品"""

    def menu_manage(self):
        """菜单"""
        self.click(key='MXQARSc6hfPDf', desc='库存管理', tag='span')
        self.click(key='za3lvW40g0Pbl', desc='移交接收管理', tag='span')
        self.click(key='jg0jirh5Qrsh6', desc='接收物品', tag='span')
        return self

    @reset_after_execution
    @doc(Xj9FgGV65jL0Oi7nZXWg)
    def Xj9FgGV65jL0Oi7nZXWg(self):
        self.menu_manage()
        self.click(key='EXyyzBXmygzvE', desc='搜索', tag='span')
        self.tab_space(5)
        self.click(key='X0v9qTnhmxmfO', desc='接收', tag='span')
        self.click(key='UUvlUhRr5iuM1', desc='确定', tag='span', p_tag='div', p_name='el-message-box')
        self.capture_api_request(url_keyword=self.URL['WpZgDxZLH'])
        return self

    @reset_after_execution
    @doc(GvUiJ1UCIayox4CCu44j)
    def GvUiJ1UCIayox4CCu44j(self):
        self.menu_manage()
        self.click(key='Mpq1GafOFIZO1', desc='搜索', tag='span')
        self.tab_space(6)
        self.click(key='RyJxmfJ5LjWN3', desc='接收', tag='span')
        self.click(key='Bi050C2vCrgKM', desc='确定', tag='span', p_tag='div', p_name='el-message-box')
        self.capture_api_request(url_keyword=self.URL['WpZgDxZLH'])
        return self

    @reset_after_execution
    @doc(lwcE4sypSymkTNNFndKw)
    def lwcE4sypSymkTNNFndKw(self):
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2)[0]['imei'])
        self.menu_manage()
        self.click(key='Ueu0QazryoP5s', desc='扫码精确接收', tag='span')
        self.ctrl_v_enter()
        self.click(key='xMkebCFjWCSz4', desc='接收', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='扫码精确接收')
        self.click(key='dtrAyEynXIhku', desc='确定', tag='span', p_tag='div', p_name='el-message-box')
        return self


class RVYW5y5DPAq(CommonPages):
    """库存管理|出库管理|销售出库"""

    def menu_manage(self):
        """菜单"""
        self.click(key='JXxWxcwpqQ1Ud', desc='库存管理', tag='span')
        self.click(key='ZB6EiZMUpc71G', desc='出库管理', tag='span')
        self.click(key='XEjdMth9GoFpk', desc='销售出库', tag='span')
        return self

    @reset_after_execution
    @doc(sX84nolF0TRL5RWSl6zx)
    def sX84nolF0TRL5RWSl6zx(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2, j=13)[0]['imei'])
        self.click(key='KJomwuHqWblFR', desc='请选择客户', tag='input')
        self.down_enter(2)
        self.input(key='VTRMmTmpp3DPj', desc='请输入物流单号', text=self.sf, tag='input')
        self.input(key='qrJIfsMO6VkRX', desc='请输入物流费用', text='12', tag='input')
        self.click(key='BR7gNawdXOJT7', desc='请输入物品编号/IMEI/平台物品编号', tag='input')
        self.ctrl_v()
        self.click(key='EWFdNLswgn3TX', desc='添加', tag='span')
        self.scroll(element='')
        self.input(key='dp2TOG48Ym9kr', desc='请输入销售价', text='200', tag='input')
        self.scroll(element='')
        self.click(key='KOWAjQ9xBTZf6', desc='已收款', tag='span')
        self.input(key='jL48oWvYIwHaH', desc='请输入金额', text='10', tag='input')
        self.click(key='Mf3omJOlHyFrB', desc='确认', tag='span')
        self.capture_api_request(url_keyword=self.URL['JKSmt0DQk'])
        return self

    @reset_after_execution
    @doc(cuv4NM82E2Es3yAJkvoi)
    def cuv4NM82E2Es3yAJkvoi(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2, j=13)[0]['imei'])
        self.click(key='q7kCOb9lDv4Ia', desc='请选择客户', tag='input')
        self.down_enter(2)
        self.input(key='TGLqBl0FlRTtC', desc='请输入物流单号', text=self.sf, tag='input')
        self.input(key='gcn9qPLalXX8e', desc='请输入物流费用', text='12', tag='input')
        self.click(key='d6NbiikVZo4c4', desc='请输入物品编号/IMEI/平台物品编号', tag='input')
        self.ctrl_v()
        self.click(key='MHN6TyogNXSGI', desc='添加', tag='span')
        self.scroll(element='')
        self.input(key='w14Cs3LU3HHtZ', desc='请输入销售价', text='200', tag='input')
        self.scroll(element='')
        self.click(key='VBMoQfRdLHjqs', desc='未收款', tag='span')
        self.click(key='iAVU5YRDjhFAL', desc='确认', tag='span')
        self.capture_api_request(url_keyword=self.URL['JKSmt0DQk'])
        return self

    @reset_after_execution
    @doc(RbCSsdTsnVGk7P77B8ca)
    def RbCSsdTsnVGk7P77B8ca(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2, j=13)[0]['imei'])
        self.click(key='bjonnpdOfDBR8', desc='请选择客户', tag='input')
        self.down_enter(2)
        self.input(key='WYrtjXaQqakAi', desc='请输入物流单号', text=self.sf, tag='input')
        self.input(key='YSPThhR0nZW7I', desc='请输入物流费用', text='12', tag='input')
        self.click(key='YxmnVFpGSkork', desc='请输入物品编号/IMEI/平台物品编号', tag='input')
        self.ctrl_v()
        self.click(key='XMk1RypEB4xgB', desc='添加', tag='span')
        self.scroll(element='')
        self.input(key='cd9B3ahQhKQ2C', desc='请输入销售价', text='200', tag='input')
        self.click(key='tWYm7aAt305gH', desc='手动添加', tag='span')
        self.click(key='CC8ZlVxNvBGTx', desc='搜索', tag='span')
        self.tab_space(3)
        self.click(key='Y1AclMOAXrfSL', desc='确 定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='手动添加')
        self.scroll(element='')
        self.click(key='Ca2TBzxnnsGYf', desc='未收款', tag='span')
        self.click(key='Ic8pqkHkKPDno', desc='确认', tag='span')
        self.capture_api_request(url_keyword=self.URL['JKSmt0DQk'])
        return self

    @reset_after_execution
    @doc(o7rFfo1GQFC1QUtXg7UR)
    def o7rFfo1GQFC1QUtXg7UR(self):
        self.menu_manage()
        self.file.get_inventory_data('sell_sales_outbound', 'imei', i=2)
        self.click(key='V9szsZqKUtiev', desc='请选择客户', tag='input')
        self.down_enter(2)
        self.input(key='wtxXdKWtg3f62', desc='请输入物流单号', text=self.sf, tag='input')
        self.input(key='dDPNOGWjrMMwc', desc='请输入物流费用', text='12', tag='input')
        self.click(key='JX49WcZ93eOdb', desc='导入添加', tag='span')
        self.click(key='fQi7SLruCBhJC', desc='请选择模板', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='物品信息导入')
        self.up_enter()
        self.upload_file(key='NlAVDw1rTqdai', file_path=self.file_path('sell_sales_outbound'))
        self.click(key='HbOKQOPiAOhrb', desc='确定', index=2, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='物品信息导入')
        self.scroll(element='')
        self.input(key='XvcCjaIN4ef40', desc='请输入销售价', text='200', tag='input')
        self.scroll(element='')
        self.click(key='W7StrXK2sKB8h', desc='未收款', tag='span')
        self.click(key='faJNS7L9yhyrd', desc='确认', tag='span')
        return self

    @reset_after_execution
    @doc(B79xRAooA8OFtgTSsB20)
    def B79xRAooA8OFtgTSsB20(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2, j=13)[0]['imei'])
        self.click(key='DVFCjdPgaEkzU', desc='铺货/预售出库', tag='span')
        self.click(key='eqX9FXaNphcdk', desc='请选择客户', tag='input')
        self.down_enter(2)
        self.click(key='q26nYpk7po9w9', desc='已收款', tag='span')
        self.click(key='Xv49dhoaYl1ap', desc='请选择收款账户', tag='input')
        self.down_enter()
        self.input(key='tJpzGmMRcqnux', desc='请输入物流单号', text=self.sf, tag='input')
        self.input(key='R1dbpGPr4yY0y', desc='请输入物流费用', text='12', tag='input')
        self.click(key='DB5HMCp5lBEXM', desc='请输入物品编号/IMEI/平台物品编号', tag='input')
        self.ctrl_v()
        self.click(key='uQxVAzJBQep66', desc='添加', tag='span')
        self.scroll(element='')
        self.input(key='xLRh1MjkvuEoe', desc='请输入销售价', text='200', tag='input')
        self.click(key='k1bsWDJAoIB2G', desc='确认', tag='span')
        self.capture_api_request(url_keyword=self.URL['JKSmt0DQk'])
        return self

    @reset_after_execution
    @doc(AtZ5UcVuGXvujP2CO3AO)
    def AtZ5UcVuGXvujP2CO3AO(self):
        self.menu_manage()
        self.file.get_inventory_data('sell_pre_sale_only_outbound', 'imei', i=2)
        self.click(key='G6LmyQNZTmAXB', desc='铺货/预售出库', tag='span')
        self.click(key='Fn6yLISoYcS7W', desc='请选择客户', tag='input')
        self.down_enter(2)
        self.click(key='WJtPsKyo2PvGu', desc='已收款', tag='span')
        self.click(key='GsEkECDUejnsI', desc='请选择收款账户', tag='input')
        self.down_enter()
        self.input(key='ayAxQv7BM00gC', desc='请输入物流单号', text=self.sf, tag='input')
        self.input(key='uykIxE9QC34XK', desc='请输入物流费用', text='12', tag='input')
        self.click(key='ooIaPPH0pQneX', desc='导入添加', tag='span')
        self.upload_file(key='cnt0sw97ZXQ3u', file_path=self.file_path('sell_pre_sale_only_outbound'))
        self.click(key='OOYqh0INh06v6', desc='确定', index=2, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='物品信息导入')
        self.scroll(element='')
        self.input(key='keiLjVeijnDJu', desc='请输入销售价', text='200', tag='input')
        self.click(key='ywh9zLqkWzfob', desc='确认', tag='span')
        self.capture_api_request(url_keyword=self.URL['JKSmt0DQk'])
        return self

    @reset_after_execution
    @doc(Qimx5yME2xvTwfpxXDWH)
    def Qimx5yME2xvTwfpxXDWH(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2, j=13)[0]['imei'])
        self.click(key='w3yhsmD8C4Dsh', desc='铺货/预售出库', tag='span')
        self.click(key='SHSuBCpHRBEVO', desc='预售', tag='span')
        self.click(key='sAlZGujQ6iivm', desc='请选择客户', tag='input')
        self.down_enter(2)
        self.input(key='NsVX9sITDQRHd', desc='请输入物流单号', text=self.sf, tag='input')
        self.input(key='EFbSJgr1s5WEr', desc='请输入物流费用', text='12', tag='input')
        self.click(key='VWfarQgayt32P', desc='请输入物品编号/IMEI/平台物品编号', tag='input')
        self.ctrl_v()
        self.click(key='IGyx770OjRVnn', desc='添加', tag='span')
        self.click(key='Tt8wcd3D2o1Pm', desc='确认', tag='span')
        self.capture_api_request(url_keyword=self.URL['JKSmt0DQk'])
        return self

    @reset_after_execution
    @doc(iw9rGWgJCzuszvcAednw)
    def iw9rGWgJCzuszvcAednw(self):
        self.menu_manage()
        self.file.get_inventory_data('inventory_item_sign_in_enter_warehouse', 'imei', i=2)
        self.click(key='lbQ2vNVeWFOGL', desc='铺货/预售出库', tag='span')
        self.click(key='jSQWMG1Rpksi0', desc='预售', tag='span')
        self.click(key='SgzqebQcAlxH3', desc='请选择客户', tag='input')
        self.down_enter(2)
        self.input(key='XzFd3uv35tHWt', desc='请输入物流单号', text=self.sf, tag='input')
        self.input(key='TbJsGH7ThF6Y3', desc='请输入物流费用', text='12', tag='input')
        self.click(key='bInjW63Y5lvcG', desc='导入添加', tag='span')
        self.upload_file(key='b6kAoIov923B7', file_path=self.file_path('inventory_item_sign_in_enter_warehouse'))
        self.click(key='YA4kALCcOigXN', desc='确定', index=2, tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='物品信息导入')
        self.click(key='urPX9zwNB9U7F', desc='确认', tag='span')
        self.capture_api_request(url_keyword=self.URL['JKSmt0DQk'])
        return self


class F4wOAWthE6g(CommonPages):
    """库存管理|出库管理|销售售后出库"""

    def menu_manage(self):
        """菜单"""
        self.click(key='sinv46I9pLNf7', desc='库存管理', tag='span')
        self.click(key='p9GIziA8g20tL', desc='出库管理', tag='span')
        self.click(key='uW5PD1z4OFSel', desc='销售售后出库', tag='span')
        return self

    @reset_after_execution
    @doc(A9xC9JwOkl75SfoIqlTM)
    def A9xC9JwOkl75SfoIqlTM(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2, j=15)[0]['articlesNo'])
        self.input(key='CWvao7rO14VcK', desc='请输入物流单号', tag='input', text=self.sf)
        self.input(key='FWqi0ueiDvJFN', desc='请输入物流费用', tag='input', text='12')
        self.click(key='x8o7nisTw2sj6', desc='请输入物品编号或者IMEI', tag='input')
        self.ctrl_v()
        self.click(key='MAfU9jiZmxLgl', desc='添加', tag='span')
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2, j=3)[0]['articlesNo'])
        self.click(key='AT4W2k2qtj1bA', desc='请输入物品编号或者IMEI', index=2, tag='input')
        self.ctrl_v()
        self.click(key='xlvBfuGlDjPXE', desc='添加', tag='span', index=2)
        self.scroll(element='')
        self.input(key='NnOsiCSIg3gUk', desc='请输入', tag='input', text='15', p_tag='td', p_name='el-table_2_column_27   el-table__cell')
        self.click(key='CLROO2XNu12uK', desc='确认出库', tag='span')
        self.capture_api_request(url_keyword=self.URL['zuYSO5V1e'])
        return self

    @reset_after_execution
    @doc(FUNbZmjhH4ul2nZkvDV2)
    def FUNbZmjhH4ul2nZkvDV2(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2, j=15)[0]['articlesNo'])
        self.click(key='MaUCi1BaJQ6vI', desc='请选择售后类型', tag='input')
        self.down_enter(2)
        self.input(key='Q0TVh7jxIOt9n', desc='请输入物流单号', tag='input', text=self.sf)
        self.input(key='NeN0aQh8BzRJE', desc='请输入物流费用', tag='input', text='12')
        self.click(key='hu9zBT6ZaT08I', desc='请输入物品编号或者IMEI', tag='input')
        self.ctrl_v()
        self.click(key='Qqd8ET5ZiKFKG', desc='添加', tag='span')
        self.click(key='hugV8v33kg0Cf', desc='确认出库', tag='span')
        self.capture_api_request(url_keyword=self.URL['zuYSO5V1e'])
        return self

    @reset_after_execution
    @doc(teC3vcKAJkMnapeaIQEH)
    def teC3vcKAJkMnapeaIQEH(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2, j=15)[0]['articlesNo'])
        self.click(key='HvEKRTGwLSBlc', desc='请选择售后类型', tag='input')
        self.down_enter(3)
        self.input(key='Bx6a8jkYhquCQ', desc='请输入物流单号', tag='input', text=self.sf)
        self.input(key='swKBH4iNc3o0G', desc='请输入物流费用', tag='input', text='12')
        self.click(key='nLkxu94eT7rgs', desc='请输入物品编号或者IMEI', tag='input')
        self.ctrl_v()
        self.click(key='lFIXfDS5RoOtg', desc='添加', tag='span')
        self.click(key='NHgIhxv2Eb0im', desc='确认出库', tag='span')
        self.capture_api_request(url_keyword=self.URL['zuYSO5V1e'])
        return self

class Hqb2YxgNHpt(CommonPages):
    """库存管理|出库管理|送修出库"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='ATxpJCzGJD5yj', desc='库存管理')
         .step(key='MNtNH7cgc4KFk', desc='出库管理')
         .step(key='ulYDiH2JDwb2H', desc='送修出库')
         .wait())
        return self

    @reset_after_execution
    @doc(Qp71Bn8xqI3rvwuJ9xCr)
    def Qp71Bn8xqI3rvwuJ9xCr(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2)[0]['articlesNo'])
        (self.step(key='S1yLNk4tGEzCT', desc='供应商')
         .custom(lambda: self.up_enter())
         .step(key='Lmft5ehwsoRDP', value=self.jd, action='input', desc='物流单号')
         .step(key='fwB3U0IVFF4nP', value='12', action='input', desc='物流费用')
         .step(key='FTdoZ8YaHtc9F', desc='点击物品输入框')
         .custom(lambda: self.ctrl_v())
         .step(key='SFo6Z1Zi6saaT', desc='点击添加')
         .step(key='LMRtX5Nkt4YNO', value=self.serial, action='input', desc='送修原因')
         .step(key='XK3tc11Retwyy', desc='点击确认出库')
         .wait())
        return self

    @reset_after_execution
    @doc(wrTiHdwvBvcntC1U05Il)
    def wrTiHdwvBvcntC1U05Il(self):
        self.menu_manage()
        self.file.get_inventory_data('send_repair_out_warehouse', 'imei', i=2)
        (self.step(key='t5L5KvSNu6mFI', desc='供应商')
         .custom(lambda: self.up_enter())
         .step(key='JlIsk6iL1Sadv', value=self.jd, action='input', desc='物流单号')
         .step(key='jR8MqMfTHRkyZ', value='40', action='input', desc='物流费用')
         .step(key='CWhu9BMBDIZJD', desc='IMEI导入')
         .step(key='ZwfSat8kjpUqQ', value=self.file_path('excel'), action='upload', desc='上传文件')
         .step(key='kJ3XbZF4JgLZg', desc='确定')
         .step(key='cOI02nMVBOFKo', value=self.serial, action='input', desc='送修原因')
         .step(key='E6MW7xhREtZU6', desc='确认出库')
         .wait())
        return self


class ItZsYP2EEbM(CommonPages):
    """库存管理|库存盘点"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='xL52vt313CIYY', desc='库存管理')
         .step(key='MuUgLPRenwlHE', desc='库存盘点')
         .wait())
        return self

    @reset_after_execution
    @doc(yfkRUCxXwAxP0gqU85sU)
    def yfkRUCxXwAxP0gqU85sU(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2)[0]['articlesNo'])
        (self.step(key='kbOphwPCyj0n1', desc='新建盘点')
         .step(key='LLExhAEyDxymV', desc='盘点物品所属人')
         .custom(lambda: self.up_enter())
         .step(key='eDjm9KIKSixpm', desc='确认')
         .step(key='yj8rRa7BDY9jf', value=self.serial, action='input', desc='备注')
         .step(key='EJgUHdHSF8sLh', desc='开始盘点')
         .step(key='mvAQDyi4SGbiW', desc='物品输入框')
         .custom(lambda: self.ctrl_v_enter())
         .step(key='Si3GK6GU6myik', desc='提交盘点')
         .step(key='zx2GYAvpmEHPD', desc='完成盘点')
         .step(key='efuU63JuKBD3u', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(UUWSDzhkp1IyWEH6s65s)
    def UUWSDzhkp1IyWEH6s65s(self):
        self.menu_manage()
        (self.step(key='rW2VNYAaMcAtU', desc='删除')
         .step(key='HmWScgpeLOo2g', desc='确定')
         .wait())
        return self


class Sso5zWneHla(CommonPages):
    """库存管理|库存调拨"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='UmT4udm6NGwkP', desc='库存管理')
         .step(key='oUQZhJICaEelV', desc='库存调拨')
         .wait())
        return self

    @reset_after_execution
    @doc(TkJYyYtSzad1UKsgz33u)
    def TkJYyYtSzad1UKsgz33u(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2)[0]['articlesNo'])
        (self.step(key='QhS26nekcWdYM', desc='新增调拨')
         .step(key='EemKCJw9sGDil', desc='调出仓库')
         .custom(lambda: self.down_enter())
         .step(key='CKIhn88sRW8oD', desc='调入仓库')
         .custom(lambda: self.down_enter(2))
         .step(key='UjEz9qFJPm1ZF', value=self.serial, action='input', desc='备注')
         .step(key='lJYgS1rNv72an', value=self.jd, action='input', desc='物流单号')
         .step(key='ynDzm9ph0Ho81', desc='物品输入框')
         .custom(lambda: self.ctrl_v())
         .step(key='jCoqbMGHJfBd2', desc='添加')
         .step(key='tgpwmSy1KFLjj', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(xOKk4jVh1lMYTHUpQpnF)
    def xOKk4jVh1lMYTHUpQpnF(self):
        self.menu_manage()
        self.file.get_inventory_data('inventory_warehouse_allocation_menu', 'articles_no', i=2)
        (self.step(key='OVuP0WbuQDPIx', desc='新增调拨')
         .step(key='HggzOIxAzKrH7', desc='调出仓库')
         .custom(lambda: self.down_enter())
         .step(key='gp4eVygSOFFEl', desc='调入仓库')
         .custom(lambda: self.down_enter(2))
         .step(key='HLZ2bi3z6jFB9', value=self.serial, action='input', desc='备注')
         .step(key='zjBS8OiJK188z', value=self.jd, action='input', desc='物流单号')
         .step(key='FwLg8vbxUPQSh', desc='导入')
         .step(key='siV8UJWXiyjch', value=self.file_path('excel'), action='upload', desc='上传文件')
         .step(key='TqIm9dSiao5mT', desc='确定')
         .step(key='SrUY4xQp66jNf', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(xdMmMEyDlNQfeiWnQR8o)
    def xdMmMEyDlNQfeiWnQR8o(self):
        self.menu_manage()
        (self.step(key='qefyv42esoPDw', desc='新增调拨')
         .step(key='ZXEoGAsQqzqNf', desc='调出仓库')
         .custom(lambda: self.down_enter())
         .step(key='b2GDHsNDU0zIn', desc='调入仓库')
         .custom(lambda: self.down_enter(2))
         .step(key='GvO9xWjHHs5eu', value=self.serial, action='input', desc='备注')
         .step(key='L2Gp6KLdn9zms', value=self.jd, action='input', desc='物流单号')
         .step(key='kJX1jRCfe1bGs', desc='选择添加')
         .step(key='d0pJH2fQdfZEm', desc='重置')
         .custom(lambda: self.tab_space(2))
         .scroll(key='LezXVv8cuvMF0', desc='确定')
         .step(key='y1mCCv8loBJps', desc='确定')
         .step(key='PRgbknA2hXGy2', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(paab2hqQQJLuUeP31Y4e)
    def paab2hqQQJLuUeP31Y4e(self):
        self.menu_manage()
        (self.step(key='rYVaZbivcKt1F', desc='接收')
         .custom(lambda: self.wait_time())
         .step(key='OoNeXwVIh5KKv', desc='快捷操作')
         .custom(lambda: self.down_enter())
         .step(key='EdsBSjOIgUWzw', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(xurEsLRqBkTUszD8mRjE)
    def xurEsLRqBkTUszD8mRjE(self):
        self.menu_manage()
        (self.step(key='VTWCtO3ebhNkV', desc='撤销')
         .custom(lambda: self.wait_time())
         .step(key='eT14Tc6urYsfh', desc='确定')
         .wait())
        return self
