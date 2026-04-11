# coding: utf-8
import os
from common.base_params import InitializeParams
from common.file_cache_manager import ParamCache
from config.settings import DATA_PATHS
from common.base_page import BasePage, ImportDataEdit, reset_after_execution
from common.import_desc import *
from config.user_info import INFO


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


class Yum9T9OO7WP(CommonPages):
    """商品采购|采购管理|新增采购单"""

    def menu_manage(self):
        """菜单"""
        self.click(key='tfAWmjByLpXDw', desc='商品采购', tag='span')
        self.click(key='fvCoLD8EmM4du', desc='采购管理', tag='span')
        self.click(key='uIp4FLXWs5PMq', desc='新增采购单', tag='span')
        return self

    @reset_after_execution
    @doc(LTMkAl3mr9wdiYoATjak)
    def LTMkAl3mr9wdiYoATjak(self):
        self.menu_manage()
        self.click(key='YZwSVxND5l2G0', desc='请选择供应商名称', tag='input')
        self.down_enter()
        self.click(key='oKx2nNaLJU7cd', desc='请选择供应商名称', tag='input')
        self.down_enter()
        self.click(key='IUn2MqaY03GbH', desc='请选择采购账号', tag='input')
        self.up_enter()
        self.click(key='CwNeqAEY3OvSW', desc='请选择包裹状态', tag='input')
        self.up_enter(2)
        self.input(key='j9S3y5LLutNqg', desc='请输入物流单号', text=self.sf, tag='input')
        self.input(key='HCWabMWHn6vHw', desc='请输入物流费用', text='12', tag='input')
        self.input(key='QUrcErPVevQtR', desc='请输入备注', text='备注', tag='input')
        self.click(key='oryXvdcP3nrJa', desc='新增', tag='span')
        self.click(key='VuGAaHvpJWAFM', desc='确定', tag='span', o_tag='div', o_name='选择机器型号', p_tag='div', p_name='el-dialog__footer')
        self.scroll(element='')
        self.click(key='g4mNQxGIb9Fs0', desc='自动生成', tag='span', p_tag='div', p_name='el-dialog__body')
        self.input(key='l7MGfg0G1BPDU', desc='请输入物品描述', text=self.serial, tag='input', p_tag='div', p_name='el-dialog__body')
        self.input(key='KahDaC28I2ReZ', desc='请输入金额', text='50', tag='input', p_tag='div', p_name='el-dialog__body')
        self.input(key='vXTpKncpCrwtf', desc='请输入平台物品编号', text=self.serial, tag='input', p_tag='div', p_name='el-dialog__body')
        self.input(key='WBEeNm3DVMfiD', desc='请输入序列号', text=self.serial, tag='input', p_tag='div', p_name='el-dialog__body')
        self.input(key='AVGZXi1jZDyE1', desc='请输入平台订单号', text=self.serial, tag='input', p_tag='div', p_name='el-dialog__body')
        self.click(key='nSZM0LG0mtP6z', desc='确 定', tag='span', o_tag='div', o_name='手动录入机器', p_tag='div', p_name='el-dialog__footer')
        self.scroll(element='')
        self.click(key='CMK9er0yGdreu', desc='未付款', tag='span')
        self.click(key='aApuQ0cTBSyY1', desc='确定生成采购单', tag='span')
        self.capture_api_request(url_keyword=self.URL['km9X0jSmr'])
        return self

    @reset_after_execution
    @doc(N4CQUFEbAhA6O3SqB3ap)
    def N4CQUFEbAhA6O3SqB3ap(self):
        self.menu_manage()
        self.click(key='qOmLjARh2EoYG', desc='请选择供应商名称', tag='input')
        self.down_enter()
        self.click(key='X7UiZk8Rhymet', desc='请选择供应商名称', tag='input')
        self.down_enter()
        self.click(key='QOwyNKoZIzQHE', desc='请选择采购账号', tag='input')
        self.up_enter()
        self.click(key='XanviDZ2B7xHW', desc='请选择包裹状态', tag='input')
        self.up_enter()
        self.click(key='FRCT4FLncDVMw', desc='请选择流转仓库', tag='input')
        self.down_enter()
        self.input(key='eNUnfkvawUnn6', desc='请输入物流单号', text=self.sf, tag='input')
        self.input(key='DN4RWL5uG0aPI', desc='请输入物流费用', text='12', tag='input')
        self.input(key='bKQj053bZJ9KI', desc='请输入备注', text='备注', tag='input')
        self.click(key='oOer4wnuo4zbn', desc='新增', tag='span')
        self.click(key='FN77WnfMGlI9f', desc='确定', tag='span', o_tag='div', o_name='选择机器型号', p_tag='div', p_name='el-dialog__footer')
        self.scroll(element='')
        self.click(key='JDQrvkOA5H43u', desc='自动生成', tag='span', p_tag='div', p_name='el-dialog__body')
        self.input(key='zh6c1jumXe2eC', desc='请输入物品描述', text=self.serial, tag='input', p_tag='div', p_name='el-dialog__body')
        self.input(key='LBpKluREXpgHx', desc='请输入金额', text='50', tag='input', p_tag='div', p_name='el-dialog__body')
        self.input(key='stiSyMmmfW50o', desc='请输入平台物品编号', text=self.serial, tag='input', p_tag='div', p_name='el-dialog__body')
        self.input(key='GyKwhSgb5C9cP', desc='请输入序列号', text=self.serial, tag='input', p_tag='div', p_name='el-dialog__body')
        self.input(key='spFohaFuZCiYq', desc='请输入平台订单号', text=self.serial, tag='input', p_tag='div', p_name='el-dialog__body')
        self.click(key='ibE6YYkwa1Ndq', desc='确 定', tag='span', o_tag='div', o_name='手动录入机器', p_tag='div', p_name='el-dialog__footer')
        self.scroll(element='')
        self.click(key='choRZuUkAsCRZ', desc='未付款', tag='span')
        self.click(key='cVuKISFq5Avf8', desc='确定生成采购单', tag='span')
        self.click(key='IXPTgr6dBT4wP', desc='确定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='选择流转仓')
        self.capture_api_request(url_keyword=self.URL['km9X0jSmr'])
        return self

    @reset_after_execution
    @doc(UXWWtbpIHPQ9A7QMbtc9)
    def UXWWtbpIHPQ9A7QMbtc9(self):
        self.menu_manage()
        self.click(key='DDOYjOnM5YfgJ', desc='请选择供应商名称', tag='input')
        self.down_enter()
        self.click(key='TDOfCsUAEYFP9', desc='请选择供应商名称', tag='input')
        self.down_enter()
        self.click(key='Cm5v1EhzRTDHa', desc='请选择采购账号', tag='input')
        self.up_enter()
        self.click(key='YvQxq6Q7icE9W', desc='请选择包裹状态', tag='input')
        self.down_enter()
        self.input(key='RDmCZOin6YMJd', desc='请输入备注', text='备注', tag='input')
        self.click(key='MZ2jVpYoeenXh', desc='新增', tag='span')
        self.click(key='VrnPPBdEqGFiG', desc='确定', tag='span', o_tag='div', o_name='选择机器型号', p_tag='div', p_name='el-dialog__footer')
        self.scroll(element='')
        self.click(key='bECuw9Jp05fJQ', desc='自动生成', tag='span', p_tag='div', p_name='el-dialog__body')
        self.input(key='DabSXHmTFzLED', desc='请输入物品描述', text=self.serial, tag='input', p_tag='div', p_name='el-dialog__body')
        self.input(key='xkmDbByzgfYs3', desc='请输入金额', text='50', tag='input', p_tag='div', p_name='el-dialog__body')
        self.input(key='owf3rWGIjrwGn', desc='请输入平台物品编号', text=self.serial, tag='input', p_tag='div', p_name='el-dialog__body')
        self.input(key='dgf7R0F0oaOH1', desc='请输入序列号', text=self.serial, tag='input', p_tag='div', p_name='el-dialog__body')
        self.input(key='fjDVRbnIHSPDf', desc='请输入平台订单号', text=self.serial, tag='input', p_tag='div', p_name='el-dialog__body')
        self.click(key='NWkORkmz815oo', desc='确 定', tag='span', o_tag='div', o_name='手动录入机器', p_tag='div', p_name='el-dialog__footer')
        self.scroll(element='')
        self.click(key='QfpyfJblbJj3h', desc='未付款', tag='span')
        self.click(key='dPLKVc4OyrGy2', desc='确定生成采购单', tag='span')
        self.capture_api_request(url_keyword=self.URL['km9X0jSmr'])
        return self

    @reset_after_execution
    @doc(Iv2a1sAnyG1YRbkyU84V)
    def Iv2a1sAnyG1YRbkyU84V(self):
        self.menu_manage()
        self.click(key='D4XFTvYviWmlF', desc='请选择供应商名称', tag='input')
        self.down_enter()
        self.click(key='f8gduefJnRNz6', desc='请选择供应商名称', tag='input')
        self.down_enter()
        self.click(key='S0Of9UdlMDEC6', desc='请选择采购账号', tag='input')
        self.up_enter()
        self.click(key='xEMuMtEBtTSVf', desc='请选择包裹状态', tag='input')
        self.up_enter()
        self.click(key='ecJS4Oi1IjOQl', desc='请选择流转仓库', tag='input')
        self.down_enter()
        self.input(key='HhKaWQbmFY2Ju', desc='请输入物流单号', text=self.sf, tag='input')
        self.input(key='igFOvZv88v3G3', desc='请输入物流费用', text='12', tag='input')
        self.input(key='lVhqKRG81ZBW8', desc='请输入备注', text='备注', tag='input')
        self.click(key='Bgc3ND00tgG1i', desc='新增', tag='span')
        self.input(key='jMGpOQ2FdykNr', desc='请输入型号', tag='input', text='iPhone 16 Pro Max', o_tag='div', o_name='选择机器型号', p_tag='div', p_name='el-tabs__content')
        self.click(key='IDqvrjis1o4mB', desc='确定', tag='span', o_tag='div', o_name='选择机器型号', p_tag='div', p_name='el-dialog__footer')
        self.click(key='kTJmqLFRqLkVv', desc='A3297', tag='span', p_tag='form', p_name='el-form dialog-form')
        self.click(key='oW2GLR4Hdetsp', desc='国行', tag='span', p_tag='form', p_name='el-form dialog-form')
        self.click(key='AbIyoPzxTxnnj', desc='黑色钛金属', tag='span', p_tag='form', p_name='el-form dialog-form')
        self.click(key='pTkVKkqL9Wnh7', desc='256G', tag='span', p_tag='form', p_name='el-form dialog-form')
        self.click(key='wFntuMvAiFIem', desc='电池健康度100%', tag='span', p_tag='form', p_name='el-form dialog-form')
        self.click(key='nqSwBFREEFTBa', desc='保修时长≥330天', tag='span', p_tag='form', p_name='el-form dialog-form')
        self.click(key='PhrKE5wNrrnwm', desc='二手优品', tag='span', p_tag='form', p_name='el-form dialog-form')
        self.click(key='spzDIKihx6zhT', desc='99新', tag='span', p_tag='form', p_name='el-form dialog-form')
        self.scroll(element='')
        self.click(key='lo0z6EGLS2qOK', desc='批量无串号录入', tag='div', p_tag='div', p_name='el-dialog__body')
        self.input(key='CAll0mJbj3UDY', desc='请输入您想要录入的数量', text='2', tag='input', p_tag='div', p_name='el-dialog__body')
        self.input(key='Pdp3CCH4k4suj', desc='请输入金额', text='5', tag='input', p_tag='div', p_name='el-dialog__body')
        self.click(key='zkPguY0CPaSMQ', desc='确 定', tag='span', o_tag='div', o_name='手动录入机器', p_tag='div', p_name='el-dialog__footer')
        self.scroll(element='')
        self.input(key='g2YLjxk2J9GD4', desc='请输入金额', text='1', tag='input')
        self.enter()
        self.click(key='Va543YO9Iu3SL', desc='确定生成采购单', tag='span')
        self.click(key='rB78ojvwZfzBG', desc='确定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='选择流转仓')
        self.capture_api_request(url_keyword=self.URL['km9X0jSmr'])
        return self

    @reset_after_execution
    @doc(W8Tva7jFU0AkEqegXRnE)
    def W8Tva7jFU0AkEqegXRnE(self):
        self.menu_manage()
        self.click(key='D4XFTvYviWmlF', desc='请选择供应商名称', tag='input')
        self.down_enter()
        self.click(key='f8gduefJnRNz6', desc='请选择供应商名称', tag='input')
        self.down_enter()
        self.click(key='S0Of9UdlMDEC6', desc='请选择采购账号', tag='input')
        self.up_enter()
        self.click(key='xEMuMtEBtTSVf', desc='请选择包裹状态', tag='input')
        self.up_enter()
        self.click(key='ecJS4Oi1IjOQl', desc='请选择流转仓库', tag='input')
        self.down_enter()
        self.input(key='HhKaWQbmFY2Ju', desc='请输入物流单号', text=self.sf, tag='input')
        self.input(key='igFOvZv88v3G3', desc='请输入物流费用', text='12', tag='input')
        self.input(key='lVhqKRG81ZBW8', desc='请输入备注', text='备注', tag='input')
        self.click(key='Bgc3ND00tgG1i', desc='新增', tag='span')
        self.input(key='jMGpOQ2FdykNr', desc='请输入型号', tag='input', text='iPhone 16 Pro Max', o_tag='div', o_name='选择机器型号', p_tag='div', p_name='el-tabs__content')
        self.click(key='IDqvrjis1o4mB', desc='确定', tag='span', o_tag='div', o_name='选择机器型号', p_tag='div', p_name='el-dialog__footer')
        self.click(key='kTJmqLFRqLkVv', desc='A3297', tag='span', p_tag='form', p_name='el-form dialog-form')
        self.click(key='oW2GLR4Hdetsp', desc='国行', tag='span', p_tag='form', p_name='el-form dialog-form')
        self.click(key='AbIyoPzxTxnnj', desc='黑色钛金属', tag='span', p_tag='form', p_name='el-form dialog-form')
        self.click(key='pTkVKkqL9Wnh7', desc='256G', tag='span', p_tag='form', p_name='el-form dialog-form')
        self.click(key='wFntuMvAiFIem', desc='电池健康度100%', tag='span', p_tag='form', p_name='el-form dialog-form')
        self.click(key='nqSwBFREEFTBa', desc='保修时长≥330天', tag='span', p_tag='form', p_name='el-form dialog-form')
        self.click(key='PhrKE5wNrrnwm', desc='二手优品', tag='span', p_tag='form', p_name='el-form dialog-form')
        self.click(key='spzDIKihx6zhT', desc='99新', tag='span', p_tag='form', p_name='el-form dialog-form')
        self.scroll(element='')
        self.click(key='lo0z6EGLS2qOK', desc='批量无串号录入', tag='div', p_tag='div', p_name='el-dialog__body')
        self.input(key='CAll0mJbj3UDY', desc='请输入您想要录入的数量', text='2', tag='input', p_tag='div', p_name='el-dialog__body')
        self.input(key='Pdp3CCH4k4suj', desc='请输入金额', text='5', tag='input', p_tag='div', p_name='el-dialog__body')
        self.click(key='zkPguY0CPaSMQ', desc='确 定', tag='span', o_tag='div', o_name='手动录入机器', p_tag='div', p_name='el-dialog__footer')
        self.scroll(element='')
        self.input(key='g2YLjxk2J9GD4', desc='请输入金额', text='100', tag='input')
        self.enter()
        self.click(key='Va543YO9Iu3SL', desc='确定生成采购单', tag='span')
        self.click(key='rB78ojvwZfzBG', desc='确定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='选择流转仓')
        self.capture_api_request(url_keyword=self.URL['km9X0jSmr'])
        return self

    @reset_after_execution
    @doc(tkqeuQNKA9C86c8AQuHz)
    def tkqeuQNKA9C86c8AQuHz(self):
        self.menu_manage()
        self.file.update_and_modify_the_imei('new_purchase_order')
        self.click(key='qr848gqpkaAWU', desc='请选择供应商名称', tag='input')
        self.down_enter()
        self.click(key='PNeLZG51tgPWW', desc='请选择供应商名称', tag='input')
        self.down_enter()
        self.click(key='vhrgfA8fyTcDW', desc='请选择采购账号', tag='input')
        self.up_enter()
        self.click(key='cxOBfFnAdlpTt', desc='请选择包裹状态', tag='input')
        self.down_enter()
        self.input(key='Sc03rbYnMyufV', desc='请输入备注', text='备注', tag='input')
        self.click(key='WKkzo2w1ZumH5', desc='导入', tag='span')
        self.click(key='rIxCawZMLVx21', desc='请选择模板', tag='input')
        self.down_enter(4)
        self.upload_file(key='wWmj85jr1V7oi', file_path=self.file_path('new_purchase_order'))
        self.click(key='g1gR6Q1L0huy9', desc='确定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='物品信息导入')
        self.scroll(element='')
        self.click(key='AHabbUwFQICqW', desc='未付款', tag='span')
        self.click(key='VKRLAsLVW6hFG', desc='确定生成采购单', tag='span')
        return self

    @reset_after_execution
    @doc(K2g9gJbSU76WxYKMFL1A)
    def K2g9gJbSU76WxYKMFL1A(self):
        self.menu_manage()
        self.click(key='aQdhHx3DAjvUX', desc='请选择供应商名称', tag='input')
        self.down_enter()
        self.click(key='EtUxyOPnus7Vy', desc='请选择供应商名称', tag='input')
        self.down_enter()
        self.click(key='t2G1UiMCNCa2G', desc='请选择采购账号', tag='input')
        self.up_enter()
        self.click(key='fQm3PQlQ2JKvP', desc='请选择包裹状态', tag='input')
        self.up_enter()
        self.click(key='RVpM5aYTHbfnh', desc='请选择流转仓库', tag='input')
        self.down_enter()
        self.input(key='SoTR4Vvunugj2', desc='请输入物流单号', text=self.sf, tag='input')
        self.input(key='ztG9vJ9iUIMXP', desc='请输入物流费用', text='12', tag='input')
        self.input(key='GJVv2How8yDdT', desc='请输入备注', text='备注', tag='input')
        self.click(key='LN4HArAHCjIu4', desc='新增', tag='span')
        self.click(key='wGmxG9UnaKwUc', desc='确定', tag='span', o_tag='div', o_name='选择机器型号', p_tag='div', p_name='el-dialog__footer')
        self.scroll(element='')
        self.click(key='XotLf7QKiQnvn', desc='自动生成', tag='span', p_tag='div', p_name='el-dialog__body')
        self.input(key='b1uzIUuqTUsQh', desc='请输入物品描述', text=self.serial, tag='input', p_tag='div', p_name='el-dialog__body')
        self.input(key='Yzb8M0Dm9Lad6', desc='请输入金额', text='50', tag='input', p_tag='div', p_name='el-dialog__body')
        self.input(key='p3WoL6HItB3Cu', desc='请输入平台物品编号', text=self.serial, tag='input', p_tag='div', p_name='el-dialog__body')
        self.input(key='Vvd0m9VeypwqS', desc='请输入序列号', text=self.serial, tag='input', p_tag='div', p_name='el-dialog__body')
        self.input(key='S8aOBBjgbSEfC', desc='请输入平台订单号', text=self.serial, tag='input', p_tag='div', p_name='el-dialog__body')
        self.click(key='TIxfTPxpY2TLl', desc='确 定', tag='span', o_tag='div', o_name='手动录入机器', p_tag='div', p_name='el-dialog__footer')
        self.scroll(element='')
        self.click(key='JEHJeJd86zouu', desc='未付款', tag='span')
        self.click(key='wdogExlmo4F8E', desc='确定生成采购单', tag='span')
        self.click(key='LPniMh8nXWuGS', desc='确定生成采购单', tag='span')
        self.click(key='CXBHCYHRXagPb', desc='请选择快捷操作', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='选择流转仓')
        self.down_enter(2)
        self.click(key='jpTwLd7pHQqsC', desc='质检', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='选择流转仓')
        self.click(key='lmrpjMohvBpJD', desc='请选择接收人', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='选择流转仓')
        self.down_enter(2)
        self.input(key='VJPXWtryO7Qew', desc='请填写移交说明', text='备注', tag='textarea', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='选择流转仓')
        self.click(key='Pg2DTFW6xynII', desc='确定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='选择流转仓')
        self.capture_api_request(url_keyword=self.URL['km9X0jSmr'])
        return self

    @reset_after_execution
    @doc(BB4DySLMjyQ0zFNVq9sj)
    def BB4DySLMjyQ0zFNVq9sj(self):
        self.menu_manage()
        self.file.update_and_modify_the_imei('new_purchase_order')
        self.click(key='coiPHfqhj3yxQ', desc='@+', tag='i', p_tag='div', p_name='flex flex-col-center')
        self.input(key='K1p8CzakTvUrS', desc='请输入采购供应商名称', text='供应商' + self.serial, tag='input', p_tag='div', p_name='el-dialog__body')
        self.click(key='sz8zZ7FDBWju4', desc='请选择货源类型', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter()
        self.tab()
        self.down_enter()
        self.input(key='TgkjH30UYaFEw', desc='请输入联系方式', text=self.phone, tag='input', p_tag='div', p_name='el-dialog__body')
        self.tab()
        self.down_enter()
        self.click(key='FRGzjkgiy7wn4', desc='请选择省份', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter()
        self.click(key='Y3NVPtXmbIbma', desc='请选择市', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter()
        self.click(key='iaj7fCMyj0sRc', desc='请选择区/县', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter()
        self.input(key='rrs0AaGVzSAFu', desc='请输入详细地址', text='高速路1号', tag='input', p_tag='div', p_name='el-dialog__body')
        self.click(key='TZcF89hwNPSPK', desc='确定', tag='span', p_tag='div', p_name='dialog-footer')
        self.click(key='VCybJAqvRMje0', desc='请选择供应商名称', tag='input')
        self.down_enter()
        self.click(key='O2bKsFpZJVdXA', desc='请选择供应商名称', tag='input')
        self.up_enter()
        self.click(key='NjjLK1dYAZSSp', desc='请选择采购账号', tag='input')
        self.up_enter()
        self.click(key='XGCClvx3kbOgK', desc='请选择包裹状态', tag='input')
        self.down_enter()
        self.input(key='fI6VxUVUODVyR', desc='请输入备注', text='备注', tag='input')
        self.click(key='qp6nrnpE3OQct', desc='导入', tag='span')
        self.click(key='kqXA4G1c3XoZ5', desc='请选择模板', tag='input')
        self.down_enter(4)
        self.upload_file(key='HDnV095kWgLb8', file_path=self.file_path('new_purchase_order'))
        self.click(key='a73NOiK6t1SF4', desc='确定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='物品信息导入')
        self.scroll(element='')
        self.click(key='JbKNos3sg46Aj', desc='未付款', tag='span')
        self.click(key='v0l3ooceGutWI', desc='确定生成采购单', tag='span')
        self.capture_api_request(url_keyword=self.URL['km9X0jSmr'])
        return self


class Sd1EWjfzgR1(CommonPages):
    """商品采购|采购售后管理|采购售后列表"""

    def menu_manage(self):
        """菜单"""
        self.click(key='b0eVRzbVjGfxi', desc='商品采购', tag='span')
        self.click(key='xYV2hph8o5RSM', desc='采购售后管理', tag='span')
        self.click(key='R803z5IfVPYyC', desc='采购售后列表', tag='span')
        return self

    @reset_after_execution
    @doc(phfsqPqFesHVfgjiWNer)
    def phfsqPqFesHVfgjiWNer(self):
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=2)
        ParamCache.cache_object({"i": obj[0]['id']})
        self.menu_manage()
        self.click(key='Lvt7QU1DSDTMw', desc='采购售后中', tag='span', p_tag='div', p_name='body-content-top')
        self.click(key='VAK3MQ6mX2x0e', desc='更新售后状态', index=2, tag='span', p_tag='td', p_name='el-table_2_column_20   el-table__cell')
        self.input(key='vL7kvdpPmNf1N', desc='请输入备注', tag='textarea', text='备注', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='LC9JNTms4tqGB', desc='确认', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='售后操作')
        self.capture_api_request(url_keyword=self.URL['xGS6K1sGm'])
        return self

    @reset_after_execution
    @doc(jVgd53LQsvnwXfUXRRgq)
    def jVgd53LQsvnwXfUXRRgq(self):
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=2)
        ParamCache.cache_object({"i": obj[0]['id']})
        self.menu_manage()
        self.click(key='QZV81QTG0g7QK', desc='采购售后中', tag='span', p_tag='div', p_name='body-content-top')
        self.click(key='frmfmQuidZm27', desc='更新售后状态', index=2, tag='span', p_tag='td', p_name='el-table_2_column_20   el-table__cell')
        self.click(key='CaMWR4xT6kuNI', desc='已结算', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='qp3IFtvgWH4lx', desc='请选择结算账户', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.down_enter()
        self.input(key='PX6d61JpPaGJj', desc='请输入备注', tag='textarea', text='备注', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='VRNo4qPgJKdPx', desc='确认', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='售后操作')
        self.capture_api_request(url_keyword=self.URL['xGS6K1sGm'])
        return self

    @reset_after_execution
    @doc(pHj61cDnzOd8FgCqMVW5)
    def pHj61cDnzOd8FgCqMVW5(self):
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=2)
        ParamCache.cache_object({"i": obj[0]['id']})
        self.menu_manage()
        self.click(key='Lp1yDBPZWuSZX', desc='采购售后中', tag='span', p_tag='div', p_name='body-content-top')
        self.click(key='gECrvTgmaDZdh', desc='更新售后状态', index=2, tag='span', p_tag='td', p_name='el-table_2_column_20   el-table__cell')
        self.click(key='lvfZmLl2Pk95R', desc='拒退退回', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='vJoQPau2wgELj', desc='直接入库', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='bwSnQiPvkEyI2', desc='请选择入库流转仓', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.down_enter()
        self.input(key='vtC7pgCPQuxkD', desc='请输入备注', tag='textarea', text='备注', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='aBH0rsRAeuVG5', desc='确认', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='售后操作')
        self.capture_api_request(url_keyword=self.URL['xGS6K1sGm'])
        return self

    @reset_after_execution
    @doc(Z4SuqHs6Y2LaV2QZa5Ir)
    def Z4SuqHs6Y2LaV2QZa5Ir(self):
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=2)
        ParamCache.cache_object({"i": obj[0]['id']})
        self.menu_manage()
        self.click(key='oqMbpioAhlQLt', desc='采购售后中', tag='span', p_tag='div', p_name='body-content-top')
        self.click(key='pddQMiL4O1gMS', desc='更新售后状态', index=2, tag='span', p_tag='td', p_name='el-table_2_column_20   el-table__cell')
        self.click(key='bfk04RFOjXthB', desc='拒退退回', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.input(key='KPIS2uFKxXJy3', desc='请输入物流单号', text=self.sf, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.input(key='QuiNYFNAgMqoL', desc='请输入备注', tag='textarea', text='备注', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='mCO6QsQ0BHsuj', desc='确认', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='售后操作')
        self.capture_api_request(url_keyword=self.URL['xGS6K1sGm'])
        return self

    @reset_after_execution
    @doc(tTRW133mzbKPeCd8m40H)
    def tTRW133mzbKPeCd8m40H(self):
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=2)
        ParamCache.cache_object({"i": obj[0]['id']})
        self.menu_manage()
        self.click(key='LZ2UxTkw8P1hE', desc='采购售后中', tag='span', p_tag='div', p_name='body-content-top')
        self.click(key='BiiGpS5d6rUlQ', desc='更新售后状态', index=2, tag='span', p_tag='td', p_name='el-table_2_column_20   el-table__cell')
        self.click(key='oTo3f4c35E9FY', desc='换货', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.input(key='VDR9uxDP4OwwR', desc='请输入物流单号', tag='input', text=self.sf, p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='N2EAlVYVWvEJD', desc='录入新机', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='JnthRWqQQxYie', desc='请选择成色', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='采购售后操作')
        self.down_enter()
        self.tab()
        self.input(text=self.imei)
        self.tab()
        self.input(text='100')
        self.click(key='bHoFg0rQMV9ds', desc='确定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='采购售后操作')
        self.click(key='fM2X1yux3m0wt', desc='确认', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='售后操作')
        self.capture_api_request(url_keyword=self.URL['xGS6K1sGm'])
        return self

    @reset_after_execution
    @doc(J5gqPGgMCU66iUGcjVkX)
    def J5gqPGgMCU66iUGcjVkX(self):
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=2)
        ParamCache.cache_object({"i": obj[0]['id']})
        self.menu_manage()
        self.click(key='xdLDXbmHfHBG3', desc='采购售后中', tag='span', p_tag='div', p_name='body-content-top')
        self.click(key='DvE22wfc0QqvV', desc='更新售后状态', index=2, tag='span', p_tag='td', p_name='el-table_2_column_20   el-table__cell')
        self.click(key='G2pnjuEBKKUpZ', desc='换货', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='V1DoRFtA7AU7H', desc='直接入库', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='K5v7JvYRvfQJw', desc='请选择入库流转仓', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.down_enter()
        self.click(key='atiMdxQshrg8l', desc='录入新机', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='Nj1lndCAsbXBO', desc='请选择成色', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='采购售后操作')
        self.down_enter()
        self.tab()
        self.input(text=self.imei)
        self.tab()
        self.input(text='100')
        self.click(key='RI5KBpnyPoZYQ', desc='确定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='采购售后操作')
        self.click(key='SsMNHG149a8g6', desc='确认', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='售后操作')
        self.capture_api_request(url_keyword=self.URL['xGS6K1sGm'])
        return self

    @reset_after_execution
    @doc(OrOE57gtX6xtqaXXMsPi)
    def OrOE57gtX6xtqaXXMsPi(self):
        self.menu_manage()
        self.click(key='qhWEFqjsFaKuw', desc='导出', tag='span')
        return self

    @reset_after_execution
    @doc(Bht5FveIIJwsO1nzrSou)
    def Bht5FveIIJwsO1nzrSou(self):
        self.menu_manage()
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=1)
        ParamCache.cache_object({"i": obj[0]['imei']})
        self.click(key='rhMFNAV4jbSsD', desc='请输入物品编号/IMEI', tag='input')
        self.ctrl_v()
        self.click(key='Y73sFbDJ8zzQ7', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['y03duzqXb'])
        return self

    @reset_after_execution
    @doc(CfF5rsovr6q1eXvK89E3)
    def CfF5rsovr6q1eXvK89E3(self):
        self.menu_manage()
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=2)
        ParamCache.cache_object({"i": obj[0]['imei']})
        self.click(key='KuWGI2PQQ87hj', desc='请输入物品编号/IMEI', tag='input')
        self.ctrl_v()
        self.click(key='qNQgVndcO2tMF', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['y03duzqXb'])
        return self

    @reset_after_execution
    @doc(k39WRkcNXmAaALC0Vslr)
    def k39WRkcNXmAaALC0Vslr(self):
        self.menu_manage()
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=1)
        ParamCache.cache_object({"i": obj[0]['imei']})
        self.click(key='MCniAvWhvdY6x', desc='请选择采购供应商', tag='input')
        self.down_enter()
        self.click(key='MUDf8jkQaytND', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['y03duzqXb'])
        return self

    @reset_after_execution
    @doc(NqFHiIZhsGNUUdvC6h2P)
    def NqFHiIZhsGNUUdvC6h2P(self):
        self.menu_manage()
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=2)
        ParamCache.cache_object({"i": obj[0]['imei']})
        self.click(key='fFTmVl5WAhkFD', desc='请选择采购供应商', tag='input')
        self.down_enter()
        self.click(key='P5CcPkvdmxd5j', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['y03duzqXb'])
        return self

    @reset_after_execution
    @doc(WGIFhMXGjLDYNdHFNmZ6)
    def WGIFhMXGjLDYNdHFNmZ6(self):
        self.menu_manage()
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=1)
        ParamCache.cache_object({"i": obj[0]['platformArticlesNo']})
        self.click(key='NScmhGXffkQxm', desc='请输入平台物品编号', tag='input')
        self.ctrl_v()
        self.click(key='TI11Ai2NcRq7Z', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['y03duzqXb'])
        return self

    @reset_after_execution
    @doc(nwM5r4G3gxMKFkY7vCkS)
    def nwM5r4G3gxMKFkY7vCkS(self):
        self.menu_manage()
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=2)
        ParamCache.cache_object({"i": obj[0]['platformArticlesNo']})
        self.click(key='bpxeGRqtYhSk8', desc='请输入平台物品编号', tag='input')
        self.ctrl_v()
        self.click(key='CfA0BtFQ16IlF', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['y03duzqXb'])
        return self

    @reset_after_execution
    @doc(SdxPSZvsxDBQFJmoq0sn)
    def SdxPSZvsxDBQFJmoq0sn(self):
        self.menu_manage()
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=1)
        ParamCache.cache_object({"i": obj[0]['billNo']})
        self.click(key='RqmAiDkzzucxb', desc='请输入售后订单号', tag='input')
        self.ctrl_v()
        self.click(key='sAwqmLYROb4GW', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['y03duzqXb'])
        return self

    @reset_after_execution
    @doc(xKOkW569Bn2xL0RXmnEZ)
    def xKOkW569Bn2xL0RXmnEZ(self):
        self.menu_manage()
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=2)
        ParamCache.cache_object({"i": obj[0]['saleNo']})
        self.click(key='OQQJaLECpXDvr', desc='请输入售后订单号', tag='input')
        self.ctrl_v()
        self.click(key='gqbkVEkLh024R', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['y03duzqXb'])
        return self

    @reset_after_execution
    @doc(XEQ3tAQnMxJ6mC5Z3zSu)
    def XEQ3tAQnMxJ6mC5Z3zSu(self):
        self.menu_manage()
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=1)
        ParamCache.cache_object({"i": obj[0]['billNo']})
        self.input(key='m24ZQDIS3Eau4', desc='开始时间', text=self.get_the_date(), tag='input')
        self.input(key='Ba3XOt1QjNbDJ', desc='结束时间', text=self.get_the_date(), tag='input')
        self.esc()
        self.click(key='Oe7vr9UqHCS4G', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['y03duzqXb'])
        return self

    @reset_after_execution
    @doc(PhchxOyoBh6ZBZxAR8B5)
    def PhchxOyoBh6ZBZxAR8B5(self):
        self.menu_manage()
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=2)
        ParamCache.cache_object({"i": obj[0]['saleNo']})
        self.input(key='OBY69oxsA9YL7', desc='开始时间', text=self.get_the_date(), tag='input')
        self.input(key='vn23YfjhNqXAX', desc='结束时间', text=self.get_the_date(), tag='input')
        self.esc()
        self.click(key='tL0Qu7336F53c', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['y03duzqXb'])
        return self

    @reset_after_execution
    @doc(cJyOkQvyQsMExyu5Vt45)
    def cJyOkQvyQsMExyu5Vt45(self):
        self.menu_manage()
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=1)
        ParamCache.cache_object({"i": obj[0]['logisticsNo']})
        self.click(key='lIgqG6jvVSaN8', desc='请输入出库物流单号', tag='input')
        self.ctrl_v()
        self.click(key='YaL4lAFMZkY5j', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['y03duzqXb'])
        return self

    @reset_after_execution
    @doc(y4THlC3ekhRh4iae3DtD)
    def y4THlC3ekhRh4iae3DtD(self):
        self.menu_manage()
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=2)
        ParamCache.cache_object({"i": obj[0]['logisticsNo']})
        self.click(key='i1a5pAv5UJcAF', desc='请输入出库物流单号', tag='input')
        self.ctrl_v()
        self.click(key='EvfRbk0JCrfGs', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['y03duzqXb'])
        return self

    @reset_after_execution
    @doc(dhBbO6TlYXaCCyMti4Sf)
    def dhBbO6TlYXaCCyMti4Sf(self):
        self.menu_manage()
        obj = self.pc.Jz32tuIMNM7geguh5D8TF(i=1)
        ParamCache.cache_object({"i": obj[0]['billNo']})
        self.click(key='Byhl00KdRmHwA', desc='请选择售后状态', tag='input')
        self.down_enter()
        self.click(key='GPPn7fPhH6ASY', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['y03duzqXb'])
        return self


class ZrnG6O3xUlf(CommonPages):
    """商品采购|采购售后管理|待售后列表"""

    def menu_manage(self):
        """菜单"""
        self.click(key='npauzZsp9U2sU', desc='商品采购', tag='span')
        self.click(key='n5AckyRBQDPFj', desc='采购售后管理', tag='span')
        self.click(key='BVORFlFahl6l5', desc='待售后列表', tag='span')
        return self

    @reset_after_execution
    @doc(Zd7znz6pdWwciZ4zhv18)
    def Zd7znz6pdWwciZ4zhv18(self):
        obj = self.pc.XHVW0IhQgPnb63fnaqTdN()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.menu_manage()
        self.click(key='wwklgqt8PlyIt', desc='售后操作', tag='button', p_tag='td', p_name='el-table_1_column_19   el-table__cell')
        self.input(key='CkDvUiO93Ngnw', desc='请输入', text='55', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='Uyo73wzlAptxs', desc='确认', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='售后操作')
        self.capture_api_request(url_keyword=self.URL['MgU31VbHk'])
        return self

    @reset_after_execution
    @doc(iWItsJtwj5CLc0GYimGA)
    def iWItsJtwj5CLc0GYimGA(self):
        obj = self.pc.XHVW0IhQgPnb63fnaqTdN()
        self.menu_manage()
        self.click(key='t3DEqSanip338', desc='请输入物品编号/IMEI号/平台物品编号', tag='input')
        self.tab_space(5)
        self.click(key='Eu41FWxkrEFPP', desc='批量售后', tag='span')
        self.input(key='FJowbn7R0LRaE', desc='请输入', text='55', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='yOdIMcxdilkTE', desc='确认', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='售后操作')
        self.capture_api_request(url_keyword=self.URL['MgU31VbHk'])
        return self

    @reset_after_execution
    @doc(Mlllk8zWuMbryTvo07YA)
    def Mlllk8zWuMbryTvo07YA(self):
        obj = self.pc.XHVW0IhQgPnb63fnaqTdN()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.menu_manage()
        self.click(key='Bch5hXMf9Iqqu', desc='售后操作', tag='button', p_tag='td', p_name='el-table_1_column_19   el-table__cell')
        self.input(key='h2hjA6B02vx42', desc='请输入', text='55', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='ziXqjDoeyFjDb', desc='已结算', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='hjhvu103Mmfy6', desc='请选择结算账户', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.down_enter()
        self.click(key='UJhTXMKOosV9i', desc='确认', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='售后操作')
        self.capture_api_request(url_keyword=self.URL['MgU31VbHk'])
        return self

    @reset_after_execution
    @doc(mtmZ9ns5g8nanblESlTR)
    def mtmZ9ns5g8nanblESlTR(self):
        obj = self.pc.XHVW0IhQgPnb63fnaqTdN()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.menu_manage()
        self.click(key='aNNlVwmsz6cJr', desc='售后操作', tag='button', p_tag='td', p_name='el-table_1_column_19   el-table__cell')
        self.click(key='inHCmTeutl6sa', desc='售后出库', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.input(key='wC4bskuEs3lyS', desc='请填写物流单号', text=self.sf, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.input(key='L7GD5TnYaMqaj', desc='请输入物流费用', text='12', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='VKBOxYL7MZtaF', desc='确认', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='售后操作')
        self.capture_api_request(url_keyword=self.URL['TDNsMZDYJ'])
        return self

    @reset_after_execution
    @doc(gXtFuS2Icw1FTTfLvWC0)
    def gXtFuS2Icw1FTTfLvWC0(self):
        obj = self.pc.XHVW0IhQgPnb63fnaqTdN()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.menu_manage()
        self.click(key='WinAUg9XDgCX9', desc='售后操作', tag='button', p_tag='td', p_name='el-table_1_column_19   el-table__cell')
        self.click(key='Qrxom16yCCebc', desc='售后出库', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='pIdVkdy4Pz2Fz', desc='@快递易图标', tag='span', p_tag='div', p_name='el-switch')
        self.click(key='P75aDNTUjz8Qb', desc='计算运费', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='zN2HoFyaj9Xw2', desc='确认', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='售后操作')
        self.capture_api_request(url_keyword=self.URL['TDNsMZDYJ'])
        return self

    @reset_after_execution
    @doc(nFSWCuNM4gli2yRB2dwD)
    def nFSWCuNM4gli2yRB2dwD(self):
        obj = self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2, j=3)
        self.menu_manage()
        self.click(key='sQ2mmopjeR0F5', desc='请输入物品编号/IMEI号/平台物品编号', tag='input')
        self.ctrl_v()
        self.click(key='fYx7F92Kamdux', desc='添加物品', tag='span')
        self.capture_api_request(url_keyword=self.URL['RoVc0CTIT'])
        return self

    @reset_after_execution
    @doc(uq01dOZeO9ByThGMfj4w)
    def uq01dOZeO9ByThGMfj4w(self):
        obj = self.pc.XHVW0IhQgPnb63fnaqTdN()
        ParamCache.cache_object({"i": obj[1]['articlesNo']})
        self.menu_manage()
        self.click(key='dWLRUnpIuQ2Mw', desc='请输入物品编号/IMEI号/平台物品编号', tag='input')
        self.tab_space(5)
        self.click(key='OHTL32GIKK7Sq', desc='批量售后', tag='span')
        self.click(key='ArWBPgmUqK8Tm', desc='售后出库', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.input(key='opAtGHXebHQob', desc='请填写物流单号', text=self.sf, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.input(key='RtzjIjCqqRUY2', desc='请输入物流费用', text='12', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='Q8hmYfv33n29h', desc='确认', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='售后操作')
        self.capture_api_request(url_keyword=self.URL['TDNsMZDYJ'])
        return self

    @reset_after_execution
    @doc(EXJN6Kfs99I6kkD0lNX2)
    def EXJN6Kfs99I6kkD0lNX2(self):
        obj = self.pc.XHVW0IhQgPnb63fnaqTdN()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.menu_manage()
        self.click(key='ixh4y2ozGZqqs', desc='售后操作', tag='button', p_tag='td', p_name='el-table_1_column_19   el-table__cell')
        self.click(key='ZEzuXNk7UtNPV', desc='售后出库', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.input(key='ha2EEcU60PxYB', desc='请填写物流单号', text=self.sf, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.input(key='GLvyzWz8ssKHP', desc='请输入物流费用', text='12', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='xC8MWGY84PTqo', desc='退货退款', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.input(key='h4T7v87zb8v4z', desc='请输入备注', text='备注', tag='textarea', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='J05uimPmsqKRJ', desc='确认', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='售后操作')
        self.capture_api_request(url_keyword=self.URL['TDNsMZDYJ'])
        return self

    @reset_after_execution
    @doc(r3no6VL2SjqT3qCMSXsF)
    def r3no6VL2SjqT3qCMSXsF(self):
        obj = self.pc.XHVW0IhQgPnb63fnaqTdN()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.menu_manage()
        self.click(key='NKfSbgAplaNam', desc='售后操作', tag='button', p_tag='td', p_name='el-table_1_column_19   el-table__cell')
        self.click(key='WBURZpgKDTXi2', desc='售后出库', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.input(key='p20IYYwzj2EH9', desc='请填写物流单号', text=self.sf, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.input(key='lJYeH9DCX3ehk', desc='请输入物流费用', text='12', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='bvfMrEsdvWk6j', desc='退货退款', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='r0oC90GhINYSn', desc='已结算', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='QzrciE8IMFcsY', desc='请选择结算账户', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.down_enter()
        self.input(key='JegrCxNURlLWn', desc='请输入备注', text='备注', tag='textarea', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='C0L4NqVmw4jqR', desc='确认', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='售后操作')
        self.capture_api_request(url_keyword=self.URL['TDNsMZDYJ'])
        return self

    @reset_after_execution
    @doc(WCIspC62VSOcHhuvk6oH)
    def WCIspC62VSOcHhuvk6oH(self):
        obj = self.pc.XHVW0IhQgPnb63fnaqTdN()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.menu_manage()
        self.click(key='JXdEUfiUjXOET', desc='售后操作', tag='button', p_tag='td', p_name='el-table_1_column_19   el-table__cell')
        self.click(key='U4CzaEwHIOH6z', desc='售后出库', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.input(key='BeLbVHT62ewz2', desc='请填写物流单号', text=self.sf, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.input(key='nws6xnPtKo2zA', desc='请输入物流费用', text='12', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='U146wNPoRgKXD', desc='拒退退回', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.input(key='gotRcvKF0DAqd', desc='请输入物流单号', text=self.sf, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.input(key='QhZHLqTgHiIK4', desc='请输入备注', text='备注', tag='textarea', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='hYGjWUB00ED6f', desc='确认', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='售后操作')
        self.capture_api_request(url_keyword=self.URL['TDNsMZDYJ'])
        return self

    @reset_after_execution
    @doc(bRT8qBZ1qzcsOegIVUiL)
    def bRT8qBZ1qzcsOegIVUiL(self):
        obj = self.pc.XHVW0IhQgPnb63fnaqTdN()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.menu_manage()
        self.click(key='h86wJALIAXOJ8', desc='售后操作', tag='button', p_tag='td', p_name='el-table_1_column_19   el-table__cell')
        self.click(key='H2NBOR19JsGUc', desc='售后出库', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.input(key='iwbRTyecVRbCx', desc='请填写物流单号', text=self.sf, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.input(key='nUnRhZkkefFxK', desc='请输入物流费用', text='12', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='FCnk0ymMW0pC0', desc='拒退退回', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='rDLCLqDyqino6', desc='直接入库', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='t8Tqc3IsAlMHr', desc='请选择入库流转仓', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.down_enter()
        self.input(key='uPbRvbOAmr62S', desc='请输入备注', text='备注', tag='textarea', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='TqvQR3jHGZKPt', desc='确认', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='售后操作')
        self.capture_api_request(url_keyword=self.URL['TDNsMZDYJ'])
        return self

    @reset_after_execution
    @doc(p2NxayPBZqnmytlhtjEy)
    def p2NxayPBZqnmytlhtjEy(self):
        obj = self.pc.XHVW0IhQgPnb63fnaqTdN()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.menu_manage()
        self.click(key='Av7j4pKk9gP1w', desc='售后操作', tag='button', p_tag='td', p_name='el-table_1_column_19   el-table__cell')
        self.click(key='BpSyDz0Ppsdj2', desc='售后出库', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.input(key='cIRxXeFHc8p0X', desc='请填写物流单号', text=self.sf, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.input(key='i2iWZVvIXbZnN', desc='请输入物流费用', text='12', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='GHdZ6a7oinaEN', desc='换货', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.input(key='oXjsIBSHsSkak', desc='请输入物流单号', text=self.sf, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.input(key='tliHt96Sd2ZSU', desc='请输入备注', text='备注', tag='textarea', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='X9H1Bxob9cEa3', desc='录入新机', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='odwVDZCIJYa72', desc='请选择成色', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='采购售后操作')
        self.down_enter()
        self.tab()
        self.input(text=self.imei)
        self.tab()
        self.input(text='100')
        self.click(key='Qq042VaQrY9QC', desc='确定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='采购售后操作')
        self.click(key='I465yhrX39D3H', desc='确认', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='售后操作')
        self.capture_api_request(url_keyword=self.URL['TDNsMZDYJ'])
        return self

    @reset_after_execution
    @doc(HR074UMjBJ9KgEckp0hD)
    def HR074UMjBJ9KgEckp0hD(self):
        obj = self.pc.XHVW0IhQgPnb63fnaqTdN()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.menu_manage()
        self.click(key='UXZ44hQpSLfeC', desc='售后操作', tag='button', p_tag='td', p_name='el-table_1_column_19   el-table__cell')
        self.click(key='T3B9wl5AlZW2n', desc='售后出库', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.input(key='v2xZlImkWOune', desc='请填写物流单号', text=self.sf, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.input(key='OICIKJSRTl2kw', desc='请输入物流费用', text='12', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='nutBRdGnMuR18', desc='换货', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='sxJ4OiPGBKGgp', desc='直接入库', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='ZnPF0gL5NtkZs', desc='请选择入库流转仓', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.input(key='yiEMGlwaAIZvv', desc='请输入备注', text='备注', tag='textarea', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='c01tCE9Qi3LtK', desc='录入新机', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='售后操作')
        self.click(key='Wpe6iDWGDr10W', desc='请选择成色', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='采购售后操作')
        self.down_enter()
        self.tab()
        self.input(text=self.imei)
        self.tab()
        self.input(text='100')
        self.click(key='GhiHHJJg47biV', desc='确定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='采购售后操作')
        self.click(key='oQAG6LmEKUTIg', desc='确认', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='售后操作')
        self.capture_api_request(url_keyword=self.URL['TDNsMZDYJ'])
        return self

    @reset_after_execution
    @doc(AObSRgmEGYVIgbuCw6h4)
    def AObSRgmEGYVIgbuCw6h4(self):
        self.menu_manage()
        self.click(key='EULR2o0edeAh9', desc='取消售后', tag='button', p_tag='td', p_name='el-table_1_column_19   el-table__cell')
        self.input(key='cghTrgS6BZHWH', desc='请输入取消售后原因', text='备注', tag='input', p_tag='div', p_name='el-dialog__body')
        self.click(key='VzNjAUXeJBr0l', desc='确认取消', tag='span', p_tag='div', p_name='el-dialog__footer')
        self.capture_api_request(url_keyword=self.URL['BegcMvuP1'])
        return self


class Am1rGtH5Djz(CommonPages):
    """商品采购|采购售后管理|待接收物品"""

    def menu_manage(self):
        """菜单"""
        self.click(key='csHFD4LKmZusL', desc='商品采购', tag='span')
        self.click(key='fQhlEUwejIGNW', desc='采购售后管理', tag='span')
        self.click(key='lbX5WNnKif2U6', desc='待接收物品', tag='span')
        return self

    @reset_after_execution
    @doc(kDYL6B67bVRYqDohXGBm)
    def kDYL6B67bVRYqDohXGBm(self):
        obj = self.pc.Rwpqef340gYUd4Hgkbq8l()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.menu_manage()
        self.click(key='siHJPp9jWfxWy', desc='搜索', tag='span')
        self.tab_space(6)
        self.click(key='HgHqXU9kgm0lS', desc='接收', tag='span')
        self.click(key='BCh3Xo0Ng9FdX', desc='确定', tag='span', p_tag='div', p_name='el-message-box')
        self.capture_api_request(url_keyword=self.URL['WpZgDxZLH'])
        return self

    @reset_after_execution
    @doc(rf4cDB3LPxVAKj6lhBRy)
    def rf4cDB3LPxVAKj6lhBRy(self):
        self.menu_manage()
        obj = self.pc.Rwpqef340gYUd4Hgkbq8l()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        self.click(key='ecZHlxBiyXJmr', desc='扫码精确接收', tag='span')
        self.ctrl_v_enter()
        self.click(key='MQErGjAHddkZg', desc='接收', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='扫码精确接收')
        return self

    @reset_after_execution
    @doc(gXbPXTa8tODEWzcuCWKK)
    def gXbPXTa8tODEWzcuCWKK(self):
        self.menu_manage()
        obj = self.pc.Rwpqef340gYUd4Hgkbq8l()
        ParamCache.cache_object({"i": obj[0]['imei']})
        self.click(key='K3Alw0f8xY9Fx', desc='请输入物品编号/IMEI', tag='input')
        self.ctrl_v()
        self.click(key='UZovyPV54P8fu', desc='搜索', tag='span')
        return self

    @reset_after_execution
    @doc(GK9UcuLcY440l6QirME6)
    def GK9UcuLcY440l6QirME6(self):
        self.menu_manage()
        obj = self.pc.Rwpqef340gYUd4Hgkbq8l()
        ParamCache.cache_object({"i": obj[0]['imei']})
        self.input(key='ePZ9mAPjlegY1', desc='开始日期', text=self.get_the_date(), tag='input')
        self.input(key='RLCAXocf55bx6', desc='结束日期', text=self.get_the_date(), tag='input')
        self.esc()
        self.click(key='SfxvnNqvanw6N', desc='搜索', tag='span')
        return self


class EDzjBdrUqTJ(CommonPages):
    """商品采购|采购管理|采购订单列表"""

    def menu_manage(self):
        """菜单"""
        self.click(key='V2OxStal6fitx', desc='商品采购', tag='span')
        self.click(key='DBF6vlwpqJwFV', desc='采购管理', tag='span')
        self.click(key='hNUB5SCtZhQth', desc='采购订单列表', tag='span')
        return self

    @reset_after_execution
    @doc(V3OaBTTJgYrJQyoMmypY)
    def V3OaBTTJgYrJQyoMmypY(self):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP()
        ParamCache.cache_object({"i": obj[0]['articlesNoList'][0]})
        self.menu_manage()
        self.click(key='z3PtKygH1WESt', desc='@采购单号超链接', tag='span', p_tag='td', p_name='el-table_1_column_2   el-table__cell')
        self.scroll(element='')
        self.click(key='mF9Krc3vfQPss', desc='售后处理', tag='span', p_tag='tr', p_name='el-table__row')
        self.click(key='NA1NJz7R2ZbZd', desc='确认售后', tag='span', p_tag='div', p_name='el-dialog__footer')
        self.capture_api_request(url_keyword=self.URL['R7HA7rwAV'])
        return self

    @reset_after_execution
    @doc(ZaJnjFDN816Yj39HvvTA)
    def ZaJnjFDN816Yj39HvvTA(self):
        self.menu_manage()
        self.click(key='k1KJVgtnTC9WH', desc='@收货按钮', tag='div', p_tag='td', p_name='el-table_1_column_12   el-table__cell')
        self.click(key='B3JiKsVALGFzG', desc='搜索', tag='span')
        self.tab_space(6)
        self.click(key='AYo23W5Ju2Ueg', desc='签收/入库', tag='span')
        self.click(key='IxB6UvPAhIDcI', desc='请选择入库流转仓', tag='input', p_tag='div', p_name='el-dialog__body')
        self.down_enter()
        self.click(key='gJbSPMQ5bGdnd', desc='确定', tag='span', p_tag='div', p_name='el-dialog__footer')
        return self

    @reset_after_execution
    @doc(FxIuRXAgm25KpkG1vYdL)
    def FxIuRXAgm25KpkG1vYdL(self):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP()
        ParamCache.cache_object({"i": obj[0]['articlesNoList'][0]})
        self.menu_manage()
        self.click(key='FJxg7mWPtuYwl', desc='发货', tag='span', p_tag='td', p_name='el-table_1_column_23   el-table__cell')
        self.input(key='SrnXLv6O0BITx', desc='请输入物流单号', tag='input', text=self.sf, p_tag='div', p_name='el-dialog__body')
        self.click(key='oj58tkXD3a1xo', desc='确 认', tag='span', p_tag='div', p_name='el-dialog__footer')
        self.capture_api_request(url_keyword=self.URL['iUOg847fP'])
        return self

    @reset_after_execution
    @doc(onkEdLesfyWSOGVCSZdB)
    def onkEdLesfyWSOGVCSZdB(self):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP()
        ParamCache.cache_object({"i": obj[0]['imei']})
        self.menu_manage()
        self.click(key='HnI59b6FpD954', desc='物流发货', tag='span')
        self.click(key='Qbz6pLOWlfEw5', desc='请输入IMEI', tag='input', p_tag='div', p_name='el-dialog__body')
        self.ctrl_v()
        self.click(key='ridkBAOgs2Bcm', desc='添加', tag='span', p_tag='div', p_name='el-dialog__body')
        self.click(key='j12Ed2xl5rvaS', desc='确 认', tag='span', p_tag='div', p_name='el-dialog__footer')
        self.capture_api_request(url_keyword=self.URL['iUOg847fP'])
        return self

    @reset_after_execution
    @doc(IOHuxRCgSyddeY0Uw98C)
    def IOHuxRCgSyddeY0Uw98C(self):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP()
        ParamCache.cache_object({"i": obj[0]['imei']})
        self.menu_manage()
        self.file.get_inventory_data('logistics_delivery', 'imei', i=1, j=1)
        self.click(key='DCe7yMEEFRQPx', desc='物流发货', tag='span')
        self.click(key='aSAlzaotTP5mK', desc='导入物品', tag='span', p_tag='div', p_name='el-dialog__body')
        self.upload_file(key='XYpPnqNJu7SlA', file_path=self.file_path('logistics_delivery'))
        self.click(key='BmNrqV54DoYoX', desc='导入物品', tag='span', p_tag='div', p_name='el-dialog__body')
        self.click(key='TvE0y2RDhXGZ3', desc='确定', tag='span', p_tag='div', p_name='el-dialog__footer')
        self.input(key='qAz8CxiV1G2lE', desc='请输入物流单号', tag='input', text=self.sf, p_tag='div', p_name='el-dialog__body')
        self.click(key='nuLuyT1IkFGiI', desc='确 认', tag='span', p_tag='div', p_name='el-dialog__footer')
        return self

    @reset_after_execution
    @doc(X9AzyILbQOMXUGnTTHIW)
    def X9AzyILbQOMXUGnTTHIW(self):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP()
        ParamCache.cache_object({"i": obj[0]['articlesNoList'][0]})
        self.menu_manage()
        self.click(key='lJmJzycmzdgik', desc='请输入编号/IMEI号', tag='input')
        self.ctrl_v()
        self.click(key='hN0acvO7sPI2a', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['k90OkSeBm'])
        return self

    @reset_after_execution
    @doc(UBQunveHStNfKk7VC1MY)
    def UBQunveHStNfKk7VC1MY(self):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='cq1SsxIEazLgT', desc='请输入采购单号', tag='input')
        self.ctrl_v()
        self.click(key='JbOYPo7MwIhXS', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['k90OkSeBm'])
        return self

    @reset_after_execution
    @doc(CIlgrf4csxjqTWz7KBW8)
    def CIlgrf4csxjqTWz7KBW8(self):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='w9kseQVCwiKlS', desc='请选择供应商名称', tag='input')
        self.down_enter()
        self.click(key='Z6s8N7R8kqAri', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['k90OkSeBm'])
        return self

    @reset_after_execution
    @doc(SEQRfhZPQLSks8OIHSUp)
    def SEQRfhZPQLSks8OIHSUp(self):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='kCwpIuuLDcP1E', desc='请选择采购单状态', tag='input')
        self.down_enter()
        self.click(key='U3NFVjbtb8vJg', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['k90OkSeBm'])
        return self

    @reset_after_execution
    @doc(RHW76Y60nHIiwxzfeZNR)
    def RHW76Y60nHIiwxzfeZNR(self):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP()
        ParamCache.cache_object({"i": obj[0]['logisticsNo']})
        self.menu_manage()
        self.click(key='WZs2htiAo1Dr2', desc='请输入物流单号', tag='input')
        self.ctrl_v()
        self.click(key='m8ZEghRGJAKeq', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['k90OkSeBm'])
        return self

    @reset_after_execution
    @doc(ZQ8ruPTDvW7q2hXTRV77)
    def ZQ8ruPTDvW7q2hXTRV77(self):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='ROXi1GLiJnjOd', desc='请选择付款状态', tag='input')
        self.down_enter()
        self.click(key='Rx7kr5WHU2V6N', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['k90OkSeBm'])
        return self

    @reset_after_execution
    @doc(gwoujeJsaB3onqINz3vL)
    def gwoujeJsaB3onqINz3vL(self):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.menu_manage()
        self.input(key='K6xS7BovQj0gn', desc='开始日期', text=self.get_the_date(), tag='input')
        self.input(key='H44xIRfepIa1X', desc='结束日期', text=self.get_the_date(), tag='input')
        self.esc()
        self.click(key='pPLNRHlBYQl1q', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['k90OkSeBm'])
        return self

    @reset_after_execution
    @doc(JB7S4POKRpjesx1Q32J0)
    def JB7S4POKRpjesx1Q32J0(self):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='iYkqChD56GBfo', desc='请选择采购人', tag='input')
        self.down_enter()
        self.click(key='VlUEeaupbjuqm', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['k90OkSeBm'])
        return self

    @reset_after_execution
    @doc(FysimTUmjHi3FisKVbsM)
    def FysimTUmjHi3FisKVbsM(self):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP(data='a')
        ParamCache.cache_object({"i": obj[0]['platformArticlesNo']})
        self.menu_manage()
        self.click(key='wYxsrVXBwmQK3', desc='@采购单号超链接', tag='span', p_tag='td', p_name='el-table_1_column_2   el-table__cell')
        self.click(key='Yy3LYIS9YJL7M', desc='请输入平台物品编号', tag='input')
        self.ctrl_v()
        self.click(key='cAFwJlZJp8mOq', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['k90OkSeBm'])
        return self

    @reset_after_execution
    @doc(KjmhjLfM7YrFQNE6NiZG)
    def KjmhjLfM7YrFQNE6NiZG(self):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP(data='a')
        ParamCache.cache_object({"i": obj[0]['imei']})
        self.menu_manage()
        self.click(key='eFRbY9uQfTNqj', desc='@采购单号超链接', tag='span', p_tag='td', p_name='el-table_1_column_2   el-table__cell')
        self.click(key='Pfsw5ZdaXHm7T', desc='请输入IMEI号', tag='input')
        self.ctrl_v()
        self.click(key='bwEflzIci868C', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['k90OkSeBm'])
        return self

    @reset_after_execution
    @doc(D1M3VTxNoTROnlErwIkd)
    def D1M3VTxNoTROnlErwIkd(self):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP(data='a')
        ParamCache.cache_object({"i": obj[0]['platformOrderNo']})
        self.menu_manage()
        self.click(key='jlwgTSaMlfrlv', desc='@采购单号超链接', tag='span', p_tag='td', p_name='el-table_1_column_2   el-table__cell')
        self.click(key='g7vGIBTBdULVt', desc='请输入平台订单号', tag='input')
        self.ctrl_v()
        self.click(key='Ekopp78VXPyNv', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['k90OkSeBm'])
        return self

    @reset_after_execution
    @doc(Nu2xob41mVQX0Uwyv77c)
    def Nu2xob41mVQX0Uwyv77c(self):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP(data='a')
        ParamCache.cache_object({"i": obj[0]['serialNo']})
        self.menu_manage()
        self.click(key='i96l2whgTAO1m', desc='@采购单号超链接', tag='span', p_tag='td', p_name='el-table_1_column_2   el-table__cell')
        self.click(key='ySdMA6yRSEhdf', desc='请输入序列号', tag='input')
        self.ctrl_v()
        self.click(key='eSny1JuBzhihL', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['k90OkSeBm'])
        return self


class O5TxXs1xP4q(CommonPages):
    """商品采购|供应商管理"""

    def menu_manage(self):
        """菜单"""
        self.click(key='mwsAlh3FK5vEK', desc='商品采购', tag='span')
        self.click(key='fQDNekQFSBSMC', desc='供应商管理', tag='span')
        return self

    @reset_after_execution
    @doc(h0V1zMfjLKSd4odY9NU2)
    def h0V1zMfjLKSd4odY9NU2(self):
        self.menu_manage()
        self.click(key='XJlaIcjolUpYV', desc='新增', tag='span')
        self.click(key='dK6jTQGsMIRXW', desc='请输入采购供应商名称', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新增采购供应商')
        self.down_enter()
        self.click(key='vrNNTJvngaV77', desc='平台拍货', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新增采购供应商')
        self.click(key='TbfNAn6cxNR6g', desc='请选择货源类型', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新增采购供应商')
        self.down_enter(2)
        self.tab()
        self.down_enter()
        self.input(key='T5wGvq5KZAhZM', desc='请输入联系方式', text=self.phone, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新增采购供应商')
        self.click(key='cMfhuGp62adxD', desc='不选中', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新增采购供应商')
        self.tab()
        self.down_enter()
        self.click(key='dQa5awQNEaWOk', desc='请选择省份', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新增采购供应商')
        self.down_enter()
        self.click(key='Le3NnVW4Nx1t3', desc='请选择市', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新增采购供应商')
        self.down_enter()
        self.click(key='B8tkxYjSUR1VE', desc='请选择区/县', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新增采购供应商')
        self.down_enter()
        self.input(key='UooBkqIOw12rQ', desc='请输入详细地址', text='高速路1号', tag='input', p_tag='div', p_name='el-dialog__body')
        self.click(key='iMQKr9pmVV8gr', desc='确定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='新增采购供应商')
        self.capture_api_request(url_keyword=self.URL['Gw9nFt0kw'])
        return self

    @reset_after_execution
    @doc(VUZzvXlURvWP4b43uTRg)
    def VUZzvXlURvWP4b43uTRg(self):
        self.menu_manage()
        self.click(key='U0unMnooo9le5', desc='新增', tag='span')
        self.click(key='qEctIk209l8so', desc='请输入采购供应商名称', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新增采购供应商')
        self.down_enter()
        self.click(key='X9XpGTiASKOUb', desc='同行贸易', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新增采购供应商')
        self.click(key='Aclht5qrJjpui', desc='请选择货源类型', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新增采购供应商')
        self.down_enter(2)
        self.tab()
        self.down_enter()
        self.input(key='TiS9dtI22EMFJ', desc='请输入联系方式', text=self.phone, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新增采购供应商')
        self.click(key='ZbkUaUnOjfjRb', desc='已付款', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新增采购供应商')
        self.tab()
        self.down_enter()
        self.click(key='Yb7Ld84gi9faY', desc='请选择省份', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新增采购供应商')
        self.down_enter()
        self.click(key='JFbnBibjBkXEc', desc='请选择市', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新增采购供应商')
        self.down_enter()
        self.click(key='HpjlETB3UwBnb', desc='请选择区/县', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新增采购供应商')
        self.down_enter()
        self.input(key='TL5e7sVw9y8wr', desc='请输入详细地址', text='高速路1号', tag='input', p_tag='div', p_name='el-dialog__body')
        self.click(key='bpp8RqpBTTbaw', desc='确定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='新增采购供应商')
        self.capture_api_request(url_keyword=self.URL['Gw9nFt0kw'])
        return self

    @reset_after_execution
    @doc(ZwXnGe8s67ZogrbVkpxf)
    def ZwXnGe8s67ZogrbVkpxf(self):
        self.menu_manage()
        self.click(key='D84bbtSakVVg9', desc='编辑', tag='span', p_tag='td', p_name='el-table_1_column_12   el-table__cell')
        self.input(key='SB48PTrYmC1vr', desc='请输入联系方式', text=self.phone, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='编辑采购供应商')
        self.click(key='Nq1njyZfgUchv', desc='确定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='编辑采购供应商')
        self.capture_api_request(url_keyword=self.URL['qYK5c6Rpi'])
        return self

    @reset_after_execution
    @doc(AO2AZxYBELIUmcGqLQlG)
    def AO2AZxYBELIUmcGqLQlG(self):
        self.menu_manage()
        self.input(key='gYVK6x4wzswJk', desc='请输入供应商名称', text=INFO['main_supplier_name'], tag='input')
        self.click(key='GUDYoEE87cEX7', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['jj0Esnp8n'])
        return self


class YylKNDKVlLq(CommonPages):
    """商品采购|采购管理|采购工单"""

    def menu_manage(self):
        """菜单"""
        self.click(key='PY5tVZbyVsu4z', desc='商品采购', tag='span')
        self.click(key='x2bjzEVnJ1VK8', desc='采购管理', tag='span')
        self.click(key='shegA6f3nyolT', desc='采购工单', tag='span')
        return self

    @reset_after_execution
    @doc(rfP03M51AR6P1V5a2zV9)
    def rfP03M51AR6P1V5a2zV9(self):
        self.menu_manage()
        self.click(key='iS0Mm8Y0eSIBL', desc='新增', tag='span')
        self.click(key='KTANREp2tM58m', desc='@+图标', tag='i', p_tag='button', p_name='el-button el-button--primary el-button--mini is-circle')
        self.click(key='cHPjy8aiQAiWm', desc='确 定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='选择机器型号')
        self.click(key='jjugTstqMmGMh', desc='确 定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='手动录入机器')
        self.input(key='OhDJhcNLBTNAF', desc='请输入计划数量', text='1', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新建工单')
        self.click(key='M7KO69xGNLSYK', desc='请选择供应商', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新建工单')
        self.down_enter()
        self.click(key='pTzqQfWNanXcx', desc='添加工序', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新建工单')
        self.click(key='B7wq9Ks5eYQh9', desc='查询', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='添加工序')
        self.tab_space(2)
        self.click(key='do7HdL48CsTAV', desc='确认', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='添加工序')
        self.click(key='gDtd89Y3gM3Tx', desc='确 认', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='新建工单')
        self.capture_api_request(url_keyword=self.URL['IMz1mtWm1'])
        return self

    @reset_after_execution
    @doc(plgZg761v9pgtz1l53NY)
    def plgZg761v9pgtz1l53NY(self):
        self.menu_manage()
        self.click(key='fANTLQtyZGbrc', desc='新增', tag='span')
        self.click(key='QD143jomFH17e', desc='@+图标', tag='i', p_tag='button', p_name='el-button el-button--primary el-button--mini is-circle')
        self.click(key='QelkncoH876JX', desc='确 定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='选择机器型号')
        self.click(key='hc0XnSulWcQqO', desc='确 定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='手动录入机器')
        self.input(key='GwmrpEVC3JTmw', desc='请输入计划数量', text='1', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新建工单')
        self.click(key='tNfQQ8zHvs0ME', desc='请选择供应商', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新建工单')
        self.down_enter()
        self.click(key='UqtrCnNMRNxvX', desc='按报工数计算', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新建工单')
        self.click(key='trzGdaLMbc1L5', desc='添加工序', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新建工单')
        self.click(key='dPMDq5y6rfKsJ', desc='查询', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='添加工序')
        self.tab_space(2)
        self.click(key='x8BWjWQJ3JtpM', desc='确认', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='添加工序')
        self.click(key='Nj11rT2BYelXr', desc='确 认', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='新建工单')
        self.capture_api_request(url_keyword=self.URL['IMz1mtWm1'])
        return self

    @reset_after_execution
    @doc(pQejvS83KhwLmhztGkIZ)
    def pQejvS83KhwLmhztGkIZ(self):
        obj = self.pc.WmKG9OkI9OlJlOENUzgNu()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='OUJVLjgLpcDFG', desc='更多', tag='span', p_tag='td', p_name='el-table_1_column_12   el-table__cell')
        self.click(key='kRcggLMJXOVBi', desc='编辑', tag='li', p_tag='ul', p_name='el-dropdown-menu el-popper el-dropdown-menu--medium', o_tag='td', o_name='el-table_1_column_12   el-table__cell')
        self.input(key='pe3rSGmPn0Yra', desc='请输入计划数量', text='2', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='新建工单')
        self.click(key='bhSJoBZq9wXCd', desc='确 认', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='新建工单')
        self.capture_api_request(url_keyword=self.URL['Evx1QWKUp'])
        return self

    @reset_after_execution
    @doc(v7dp0gZaBk5c5dnae7G3)
    def v7dp0gZaBk5c5dnae7G3(self):
        obj = self.pc.WmKG9OkI9OlJlOENUzgNu()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='Q0IZv0HGq12us', desc='开始任务', tag='span', p_tag='td', p_name='el-table_1_column_12   el-table__cell')
        self.capture_api_request(url_keyword=self.URL['ZlYpQhYLf'])
        return self

    @reset_after_execution
    @doc(RB3GNQ8IJqAeegDYmA32)
    def RB3GNQ8IJqAeegDYmA32(self):
        self.menu_manage()
        self.click(key='UeUDJvk0mEE2U', desc='结束任务', tag='span', p_tag='td', p_name='el-table_1_column_12   el-table__cell')
        self.capture_api_request(url_keyword=self.URL['ZlYpQhYLf'])
        return self

    @reset_after_execution
    @doc(FNyrgjsFJzK3B4902iHy)
    def FNyrgjsFJzK3B4902iHy(self):
        obj = self.pc.WmKG9OkI9OlJlOENUzgNu()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='GQnnRr6JrpQtr', desc='恢复任务', tag='span', p_tag='td', p_name='el-table_1_column_12   el-table__cell')
        self.capture_api_request(url_keyword=self.URL['ZlYpQhYLf'])
        return self

    @reset_after_execution
    @doc(q7pI3tL3zRqZ67pGHnxf)
    def q7pI3tL3zRqZ67pGHnxf(self):
        self.menu_manage()
        self.click(key='X4CPEd6TutmdP', desc='更多', tag='span', p_tag='td', p_name='el-table_1_column_12   el-table__cell')
        self.click(key='q2iZdKEzIXO5W', desc='删除', tag='li', p_tag='ul', p_name='el-dropdown-menu el-popper el-dropdown-menu--medium')
        self.click(key='nbRtXJbnGa8vB', desc='确定', tag='span', p_tag='div', p_name='el-message-box')
        self.capture_api_request(url_keyword=self.URL['NSoJocsGm'])
        return self

    @reset_after_execution
    @doc(HTjf6RsIbsSIfYSwsXzv)
    def HTjf6RsIbsSIfYSwsXzv(self):
        obj = self.pc.WmKG9OkI9OlJlOENUzgNu()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='CAz5Egccj0K0Q', desc='业务报工', tag='span', p_tag='td', p_name='el-table_1_column_12   el-table__cell')
        self.click(key='WUE1zJQ0rPUtt', desc='进行中', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='业务报工')
        self.tab(3)
        self.input(text='24')
        self.click(key='EV4jrLnKuvhLr', desc='请选择业务人员', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='业务报工')
        self.down_enter()
        self.tab()
        self.input(text='50')
        self.tab()
        self.input(text='25')
        self.tab()
        self.input(text='12')
        self.tab()
        self.input(text='13')
        self.input(key='IN9ovCwohDfKn', desc='请输入备注', text='备注', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='业务报工')
        self.click(key='w0ESI90MD1nVs', desc='确 认', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='业务报工')
        self.capture_api_request(url_keyword=self.URL['p3u6vvLZS'])
        return self

    @reset_after_execution
    @doc(sruAfwpM3knh3URDgVTd)
    def sruAfwpM3knh3URDgVTd(self):
        obj = self.pc.WmKG9OkI9OlJlOENUzgNu()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='WctQ3XY03TG1Q', desc='业务报工', tag='span', p_tag='td', p_name='el-table_1_column_12   el-table__cell')
        self.click(key='SjEwHY6ompZDj', desc='请选择业务工序', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='业务报工')
        self.down_enter(2)
        self.click(key='o1A202VYEGgJU', desc='进行中', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='业务报工')
        self.tab(3)
        self.input(text='24')
        self.click(key='WueEifseB8TEd', desc='请选择业务人员', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='业务报工')
        self.down_enter()
        self.tab()
        self.input(text='100')
        self.input(key='ZrS4hEy6pBGb5', desc='请输入备注', text='备注', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='业务报工')
        self.click(key='ICvNsHZ3Nu99h', desc='确 认', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='业务报工')
        self.capture_api_request(url_keyword=self.URL['p3u6vvLZS'])
        return self

    @reset_after_execution
    @doc(IBx6SkNmcqoSeAqgrxkF)
    def IBx6SkNmcqoSeAqgrxkF(self):
        obj = self.pc.WmKG9OkI9OlJlOENUzgNu()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='rCxSKFCbNpbKV', desc='业务报工', tag='span', p_tag='td', p_name='el-table_1_column_12   el-table__cell')
        self.click(key='tYb3K7INHsbWx', desc='请选择业务工序', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='业务报工')
        self.down_enter(3)
        self.click(key='uBqj8flADfdad', desc='进行中', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='业务报工')
        self.tab(3)
        self.input(text='24')
        self.click(key='hqSnJucxPBoQe', desc='请选择业务人员', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='业务报工')
        self.down_enter()
        self.tab()
        self.input(text='100')
        self.input(key='ce4juuipByQmd', desc='请输入备注', text='备注', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='业务报工')
        self.click(key='ivBQHSHgIie8R', desc='确 认', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='业务报工')
        self.capture_api_request(url_keyword=self.URL['p3u6vvLZS'])
        return self

    @reset_after_execution
    @doc(vkKizyCO3AYcLb15f5j2)
    def vkKizyCO3AYcLb15f5j2(self):
        obj = self.pc.WmKG9OkI9OlJlOENUzgNu()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='CxRQHdQnzNV1c', desc='业务报工', tag='span', p_tag='td', p_name='el-table_1_column_12   el-table__cell')
        self.click(key='Ky2mihw379VX1', desc='请选择业务工序', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='业务报工')
        self.down_enter(4)
        self.click(key='wJp9q7stcfbwc', desc='进行中', tag='span', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='业务报工')
        self.tab(3)
        self.input(text='24')
        self.click(key='wNPi3YBmfYpxv', desc='请选择业务人员', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='业务报工')
        self.down_enter()
        self.tab()
        self.input(text='100')
        self.input(key='qAnvKO67IQ2cs', desc='请输入备注', text='备注', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='业务报工')
        self.click(key='DsHYwJg2Yyp03', desc='确 认', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='业务报工')
        self.capture_api_request(url_keyword=self.URL['p3u6vvLZS'])
        return self

    @reset_after_execution
    @doc(KOF9RCucwpiZtv3KYptu)
    def KOF9RCucwpiZtv3KYptu(self):
        obj = self.pc.WmKG9OkI9OlJlOENUzgNu()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='ukeawgT0pn3Dd', desc='请输入工单编号', tag='input')
        self.ctrl_v()
        self.click(key='tfxQShLTTTl1X', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['zaz3DUWFs'])
        return self

    @reset_after_execution
    @doc(D198Z7vIR4WbkTl36hHI)
    def D198Z7vIR4WbkTl36hHI(self):
        obj = self.pc.WmKG9OkI9OlJlOENUzgNu()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        self.menu_manage()
        self.input(key='LTutUjjYFeAVQ', desc='开始日期', text=self.get_the_date(), tag='input')
        self.input(key='HfQvhnIFgPGek', desc='结束日期', text=self.get_the_date(days=1), tag='input')
        self.esc()
        self.click(key='P6bw9AyZh5LTs', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['zaz3DUWFs'])
        return self

    @reset_after_execution
    @doc(GlZThKYcHMLtYtD6WFjf)
    def GlZThKYcHMLtYtD6WFjf(self):
        obj = self.pc.WmKG9OkI9OlJlOENUzgNu()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='d8BzzPEdWHC9C', desc='请选择供应商', tag='input')
        self.down_enter()
        self.click(key='EnfbNNSaViTle', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['zaz3DUWFs'])
        return self

    @reset_after_execution
    @doc(ZfNPiUkcpGxXUTMsfG0n)
    def ZfNPiUkcpGxXUTMsfG0n(self):
        obj = self.pc.WmKG9OkI9OlJlOENUzgNu()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='COHzMjHbwwFVq', desc='请选择状态', tag='input')
        self.down_enter()
        self.click(key='N3Daa3OTf80z3', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['zaz3DUWFs'])
        return self


class TsxUzXRsZ5y(CommonPages):
    """商品采购|采购管理|未发货订单列表"""

    def menu_manage(self):
        """菜单"""
        self.click(key='edYXEWx5Xo88p', desc='商品采购', tag='span')
        self.click(key='NfZhXMULUQWzb', desc='采购管理', tag='span')
        self.click(key='ZgiWKTTRZN3FW', desc='未发货订单列表', tag='span')
        return self

    @reset_after_execution
    @doc(uXCn7JV8wWVKBqpjkPz1)
    def uXCn7JV8wWVKBqpjkPz1(self):
        obj = self.pc.Y6hDdvp1tY9uk0H51cn91()
        ParamCache.cache_object({'i': obj[0]['purchaseNo']})
        self.menu_manage()
        self.click(key='cSvVBIKrF6rNn', desc='请选择供应商名称', tag='input')
        self.down_enter()
        self.click(key='Icy83tM8ikpha', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['NQuaSyCwg'])
        return self

    @reset_after_execution
    @doc(NApBGCWJXaD8TCr8oG0O)
    def NApBGCWJXaD8TCr8oG0O(self):
        obj = self.pc.Y6hDdvp1tY9uk0H51cn91()
        ParamCache.cache_object({'i': obj[0]['platformOrderNo']})
        self.menu_manage()
        self.click(key='hAYho8eJFfTbf', desc='请输入平台订单号', tag='input')
        self.ctrl_v()
        self.click(key='FY0yQnXahYdS4', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['NQuaSyCwg'])
        return self

    @reset_after_execution
    @doc(gEvHUJODc2blQ0T3B8vs)
    def gEvHUJODc2blQ0T3B8vs(self):
        obj = self.pc.Y6hDdvp1tY9uk0H51cn91()
        ParamCache.cache_object({'i': obj[0]['platformArticlesNo']})
        self.menu_manage()
        self.click(key='bf3NXVxHmrdlB', desc='请输入平台物品编号', tag='input')
        self.ctrl_v()
        self.click(key='xPCmtE4WPf6gZ', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['NQuaSyCwg'])
        return self

    @reset_after_execution
    @doc(tg0itP0B1fKeUwbew3bL)
    def tg0itP0B1fKeUwbew3bL(self):
        obj = self.pc.Y6hDdvp1tY9uk0H51cn91()
        ParamCache.cache_object({'i': obj[0]['imei']})
        self.menu_manage()
        self.click(key='TMATtFjb8k9jO', desc='请输入IMEI号', tag='input')
        self.ctrl_v()
        self.click(key='eI1T25NYUgXmY', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['NQuaSyCwg'])
        return self

    @reset_after_execution
    @doc(Ol6cW1DJGyj0f1eaoFJB)
    def Ol6cW1DJGyj0f1eaoFJB(self):
        self.menu_manage()
        self.click(key='vqUldD6aqaE2Y', desc='导出', tag='span')
        return self


class UyQmHapMXQU(CommonPages):
    """商品采购|采购管理|到货通知单列表"""

    def menu_manage(self):
        """菜单"""
        self.click(key='j3PoewwZ2WAw6', desc='商品采购', tag='span')
        self.click(key='LSwDYOe48Khxh', desc='采购管理', tag='span')
        self.click(key='NkZsHN84O3gO2', desc='到货通知单列表', tag='span')
        return self

    @reset_after_execution
    @doc(EY8ajeO8hDESQhWV9p4d)
    def EY8ajeO8hDESQhWV9p4d(self):
        obj = self.pc.THtT7YW545kAG73W2gHDj()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='Zos1r1wLP3wx9', desc='请输入采购单号', tag='input')
        self.ctrl_v()
        self.click(key='ghf8TiELTa3WB', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['LDvQ06cIg'])
        return self

    @reset_after_execution
    @doc(yUfJVOWNNm8e1oZ0AOli)
    def yUfJVOWNNm8e1oZ0AOli(self):
        obj = self.pc.Z6BEKs3GvdIWf6a1Dj2uP()
        ParamCache.cache_object({'i': obj[0]['logisticsNoList'][0]})
        self.menu_manage()
        self.click(key='yqqLctrNqgBjR', desc='请输入物流单号', tag='input')
        self.ctrl_v()
        self.click(key='BB8VVzqogght5', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['LDvQ06cIg'])
        return self

    @reset_after_execution
    @doc(KbYnHWYarqIZt0JaCFuZ)
    def KbYnHWYarqIZt0JaCFuZ(self):
        obj = self.pc.THtT7YW545kAG73W2gHDj()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        self.menu_manage()
        self.click(key='pVOSUPdYWEisT', desc='请选择供应商名称', tag='input')
        self.down_enter()
        self.click(key='T4Drr4Wp16bGl', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['LDvQ06cIg'])
        return self

    @reset_after_execution
    @doc(W62QpkNGF7aGdL8UtHlh)
    def W62QpkNGF7aGdL8UtHlh(self):
        obj = self.pc.THtT7YW545kAG73W2gHDj()
        ParamCache.cache_object({'i': obj[0]['orderNo']})
        self.menu_manage()
        self.input(key='AdskBMCTUPrlq', desc='开始日期', text=self.get_the_date(), tag='input')
        self.input(key='dP5O8DbNvRlhS', desc='结束日期', text=self.get_the_date(days=1), tag='input')
        self.esc()
        self.click(key='rQSX7eHk9DSaD', desc='搜索', tag='span')
        self.capture_api_request(url_keyword=self.URL['LDvQ06cIg'])
        return self


class JlYj7UfDcRG(CommonPages):
    """商品采购|采购任务"""

    def menu_manage(self):
        """菜单"""
        self.click(key='qBYVeFqdkYtFR', desc='商品采购', tag='span')
        self.click(key='Fg0uaPEXHd9I8', desc='采购任务', tag='span')
        return self

    @reset_after_execution
    @doc(tuGormTpYPA2aELsOzkM)
    def tuGormTpYPA2aELsOzkM(self):
        self.menu_manage()
        self.click(key='wC3oWY7xoejka', desc='新建任务', tag='span')
        self.input(key='mx3iPhBN9l6MM', desc='请输入任务名称', text='任务名称' + self.serial, tag='input')
        self.click(key='PnV9TPTEpr7YV', desc='请选择供应商（多选）', tag='input')
        self.down_enter()
        self.input(key='WYGLs7mNJ8QxZ', desc='开始日期', text=self.get_the_date(), tag='input')
        self.input(key='SRS7EBOHVUUE0', desc='结束日期', text=self.get_the_date(days=1), tag='input')
        self.esc()
        self.click(key='lva0AWQbcJMbc', desc='请选择采购人', tag='input')
        self.down_enter()
        self.input(key='KQNmGNhsFHjze', desc='请输入备注', text='备注', tag='input')
        self.click(key='MuStieatqgkCu', desc='添加物品', tag='span')
        self.click(key='dWojCKBVwAAj2', desc='确 定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='选择机器型号')
        self.scroll(element='')
        self.input(key='fDf6YQhVudlEv', desc='请输入任务数量', text='1', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='手动录入机器')
        self.click(key='KY5Ug4KQZfBch', desc='确 定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='手动录入机器')
        self.click(key='uryyRL0dWDU9E', desc='确认', tag='span')
        self.capture_api_request(url_keyword=self.URL['OeEzn1U3T'])
        return self

    @reset_after_execution
    @doc(Vax4XBiddBZJvUZ7eKdV)
    def Vax4XBiddBZJvUZ7eKdV(self):
        self.menu_manage()
        self.click(key='agI4C6q6Gmxdb', desc='新建任务', tag='span')
        self.input(key='kMOAVEofTw0km', desc='请输入任务名称', text='任务名称' + self.serial, tag='input')
        self.click(key='GSMvUq8WzNREe', desc='请选择供应商（多选）', tag='input')
        self.down_enter()
        self.input(key='j90ZCiZyFiA2b', desc='开始日期', text=self.get_the_date(), tag='input')
        self.input(key='z5S2oefTJPGyt', desc='结束日期', text=self.get_the_date(days=1), tag='input')
        self.esc()
        self.click(key='kBQCeS7TuM2HS', desc='请选择采购人', tag='input')
        self.down_enter()
        self.input(key='r80bCzkUX1wzh', desc='请输入备注', text='备注', tag='input')
        self.click(key='kcPkebMOniTtd', desc='添加物品', tag='span')
        self.click(key='MbATH8eBMcnSX', desc='平板电脑', tag='div', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='选择机器型号')
        self.click(key='Op2yvUN3tF62g', desc='确 定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='选择机器型号')
        self.scroll(element='')
        self.input(key='VjPOeUnMpauiJ', desc='请输入任务数量', text='1', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='手动录入机器')
        self.click(key='gzuyY2XBz7ahj', desc='确 定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='手动录入机器')
        self.click(key='mdkNqcmD3Cd8h', desc='确认', tag='span')
        self.capture_api_request(url_keyword=self.URL['OeEzn1U3T'])
        return self

    @reset_after_execution
    @doc(XBHUgvj186aUw4Sixsaa)
    def XBHUgvj186aUw4Sixsaa(self):
        self.menu_manage()
        self.click(key='ldbdEvebfhYiL', desc='新建任务', tag='span')
        self.input(key='r89OAq3vdwGPI', desc='请输入任务名称', text='任务名称' + self.serial, tag='input')
        self.click(key='SOl5kGg27sEoB', desc='请选择供应商（多选）', tag='input')
        self.down_enter()
        self.input(key='XAe5wV4uayO9t', desc='开始日期', text=self.get_the_date(), tag='input')
        self.input(key='HkRLo36YtICkU', desc='结束日期', text=self.get_the_date(days=1), tag='input')
        self.esc()
        self.click(key='XB9ORE7jgMmtS', desc='请选择采购人', tag='input')
        self.down_enter()
        self.input(key='OSSp75CWOv26V', desc='请输入备注', text='备注', tag='input')
        self.click(key='m7LJzirjs1vZf', desc='添加物品', tag='span')
        self.click(key='Gcfw2f6t167HL', desc='笔记本电脑', tag='div', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='选择机器型号')
        self.click(key='btn6TnDw84XlC', desc='确 定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='选择机器型号')
        self.scroll(element='')
        self.input(key='Qk7xMgO51xpMZ', desc='请输入任务数量', text='1', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='手动录入机器')
        self.click(key='yupnZt1EFQjVB', desc='确 定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='手动录入机器')
        self.click(key='d6t1gbsjqMYx9', desc='确认', tag='span')
        self.capture_api_request(url_keyword=self.URL['OeEzn1U3T'])
        return self

    @reset_after_execution
    @doc(IlyTw4WbHlrGhJIXjQNt)
    def IlyTw4WbHlrGhJIXjQNt(self):
        self.menu_manage()
        self.click(key='OIZMlHgDwksf9', desc='新建任务', tag='span')
        self.input(key='ofgNVnA2Fy8dH', desc='请输入任务名称', text='任务名称' + self.serial, tag='input')
        self.click(key='ajbefSUPRceQ6', desc='请选择供应商（多选）', tag='input')
        self.down_enter()
        self.input(key='CAb7eVe4Bfku9', desc='开始日期', text=self.get_the_date(), tag='input')
        self.input(key='oc02emoKk6lrq', desc='结束日期', text=self.get_the_date(days=1), tag='input')
        self.esc()
        self.click(key='qxkMq1L4O9Azq', desc='请选择采购人', tag='input')
        self.down_enter()
        self.input(key='Vu3Mk1ItJJ1ry', desc='请输入备注', text='备注', tag='input')
        self.click(key='t6l3NgRWpCXID', desc='添加物品', tag='span')
        self.click(key='fhBB8MgSQB3ry', desc='智能手表', tag='div', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='选择机器型号')
        self.click(key='EyRtNHiO8u0EO', desc='确 定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='选择机器型号')
        self.scroll(element='')
        self.input(key='YJ9iUSQnvvKdV', desc='请输入任务数量', text='1', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='手动录入机器')
        self.click(key='yVxoSb7MyqSpx', desc='确 定', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='手动录入机器')
        self.click(key='CPPZKiOQuzj1p', desc='确认', tag='span')
        self.capture_api_request(url_keyword=self.URL['OeEzn1U3T'])
        return self

    @reset_after_execution
    @doc(Jo3v4QXhq0GyXeDDjAG8)
    def Jo3v4QXhq0GyXeDDjAG8(self):
        self.menu_manage()
        self.click(key='KYnWDi20SeqU3', desc='更新到货/初验', tag='span', p_tag='td', p_name='el-table_1_column_16   el-table__cell')
        self.input(key='p2nfTnEZfo812', desc='@到货数量输入框', text='10', tag='input', p_tag='td', p_name='el-table_1_column_21   el-table__cell')
        self.input(key='pvVOByXxp9SNN', desc='@初验合格数量输入框', text='5', tag='input', p_tag='td', p_name='el-table_1_column_22   el-table__cell')
        self.input(key='F3RkKh4cx9VHN', desc='请输入备注', text='备注', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='更新信息')
        self.click(key='rYXf98aq88qPB', desc='确认', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='更新信息')
        self.capture_api_request(url_keyword=self.URL['qJGogY0tt'])
        return self

    @reset_after_execution
    @doc(QlWxSfpR4xrTDauwyHLD)
    def QlWxSfpR4xrTDauwyHLD(self):
        self.menu_manage()
        self.click(key='xnF5RHPiu91OU', desc='退货', tag='span', p_tag='td', p_name='el-table_1_column_16   el-table__cell')
        self.click(key='UkBca13jL6Bgy', desc='请选择供应商', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='退货')
        self.down_enter()
        self.input(key='xNGyJC4x0yZvK', desc='请输入退货数量', text='2', tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='退货')
        self.input(key='ZLl7XBGfX9SKP', desc='请输退货物流', text=self.sf, tag='input', p_tag='div', p_name='el-dialog__body', o_tag='div', o_name='退货')
        self.click(key='DoOzymntKCo4y', desc='确认', tag='span', p_tag='div', p_name='el-dialog__footer', o_tag='div', o_name='退货')
        self.capture_api_request(url_keyword=self.URL['IZyPme0A0'])
        return self

    @reset_after_execution
    @doc(WYBiBGE7VdR3njn7NPom)
    def WYBiBGE7VdR3njn7NPom(self):
        self.menu_manage()
        self.click(key='iWCNGHxaxNTow', desc='退货', tag='span', p_tag='td', p_name='el-table_1_column_16   el-table__cell')
        self.click(key='', desc='更多', tag='span', p_tag='td', p_name='el-table_1_column_16   el-table__cell')
        self.capture_api_request(url_keyword=self.URL[''])
        return self
