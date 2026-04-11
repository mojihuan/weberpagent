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


class NdYPoyxA7Ut(CommonPages):
    """运营中心|待报价物品"""

    def menu_manage(self):
        """菜单"""
        (self.scroll('fulfillment_center_menu', desc='运营中心')
         .step(key='hOsI7Km3Kg7yq', desc='运营中心')
         .step(key='detagpzTs53tk', desc='待报价物品')
         .wait())
        return self

    @doc(h86Q9EJJuji9EAcwmnZd)
    @reset_after_execution
    def h86Q9EJJuji9EAcwmnZd(self):
        """商品报价"""
        self.menu_manage()
        self.copy(self.pc.RjVgo4LDzg4voonKUBXr1()[0]['articlesNo'])
        (self.step(key='Smd4btZmhmVgZ', desc='物品编号')
         .custom(lambda: self.ctrl_v())
         .step(key='CsZ6EaLhS0QZW', desc='搜索')
         .step(key='niy0SHOsP7bnD', desc='商品报价')
         .step(key='nfOdUGgDLMEKX', value=310, action='input', desc='输入价格')
         .step(key='xi57dmWMMZakG', desc='确定')
         .wait())

    @doc(HdVZdnVgjfeOetZQxl9C)
    @reset_after_execution
    def HdVZdnVgjfeOetZQxl9C(self):
        """重新报价"""
        self.menu_manage()
        self.copy(self.pc.RjVgo4LDzg4voonKUBXr1()[0]['articlesNo'])
        (self.step(key='fs9x2P1BlxNO1', desc='物品编号')
         .custom(lambda: self.ctrl_v())
         .step(key='ZovLshztuVzTh', desc='搜索')
         .step(key='D3LGqmVui0ThL', desc='重新报价')
         .step(key='H0TAuyvBArNuJ', value=310, action='input', desc='输入价格')
         .step(key='iBW67nD3z8YGm', desc='确定')
         .wait())
        return self


class HBW5NSrtWxI(CommonPages):
    """运营中心|质检管理"""

    def menu_manage(self):
        """菜单"""
        (self.scroll('fulfillment_center_menu', desc='运营中心')
         .step(key='WsqbpRhRchcre', desc='运营中心')
         .step(key='gsK6Efw7OTyyg', desc='质检管理')
         .wait())
        return self

    @reset_after_execution
    @doc(jN6h3HHrblYl6XRDrjRp)
    def jN6h3HHrblYl6XRDrjRp(self):
        self.menu_manage()
        self.copy(self.pc.FYXRA4IxF49PvhUCLpp5Z()[0]['imei'])
        (self.step(key='M6PCI3lxPywjH', desc='imei输入框')
         .custom(lambda: self.ctrl_v())
         .step(key='DVJNJWwE6woYO', desc='搜索')
         .custom(lambda: self.tab_space(5))
         .step(key='IRBMsEfEu648n', desc='批量接收')
         .step(key='svdvYo82dlKEt', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(CLRwZ9FXvcE5gCYCPdSF)
    def CLRwZ9FXvcE5gCYCPdSF(self):
        self.jN6h3HHrblYl6XRDrjRp()

    @reset_after_execution
    @doc(knHZe0CfAp1HXSNNW4nG)
    def knHZe0CfAp1HXSNNW4nG(self):
        self.jN6h3HHrblYl6XRDrjRp()

    @reset_after_execution
    @doc(eoidlhlWuLRCRQL3uNIN)
    def eoidlhlWuLRCRQL3uNIN(self):
        self.jN6h3HHrblYl6XRDrjRp()

    @reset_after_execution
    @doc(rqPmiTtsuecNOe8Qa0FW)
    def rqPmiTtsuecNOe8Qa0FW(self):
        self.menu_manage()
        self.copy(self.pc.FYXRA4IxF49PvhUCLpp5Z(data='a')[0]['imei'])
        (self.step(key='eHBxyPxPGepH8', desc='质检中物品')
         .step(key='xdBE6ot5KLlfM', desc='imei输入框')
         .custom(lambda: self.ctrl_v())
         .step(key='VPUgsfZwoTBtl', desc='搜索')
         .step(key='sk9YqG6V5tJil', desc='提交质检结果')
         .custom(lambda: self.wait_time())
         .step(key='GqyKLGbS8OWr5', desc='rom容量')
         .custom(lambda: self.down_enter(2))
         .scroll(key='lOKrEoNyQCQrR',desc='确定')
         .step(key='oSgVqt1AmZcsr', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(TJXWHGYpzVeCuC3cZjrH)
    def TJXWHGYpzVeCuC3cZjrH(self):
        self.rqPmiTtsuecNOe8Qa0FW()

    @reset_after_execution
    @doc(NGkklZ12l2IiB7qVbQxE)
    def NGkklZ12l2IiB7qVbQxE(self):
        self.rqPmiTtsuecNOe8Qa0FW()

    @reset_after_execution
    @doc(zBKyvA1lFKeRAKK0WXqg)
    def zBKyvA1lFKeRAKK0WXqg(self):
        self.rqPmiTtsuecNOe8Qa0FW()

    @reset_after_execution
    @doc(JO1O4Cu3NqUy2eHg71Sb)
    def JO1O4Cu3NqUy2eHg71Sb(self):
        self.rqPmiTtsuecNOe8Qa0FW()

    @reset_after_execution
    @doc(eL32NtimAkRJKwnmSauo)
    def eL32NtimAkRJKwnmSauo(self):
        self.menu_manage()
        self.copy(self.pc.FYXRA4IxF49PvhUCLpp5Z(data='c')[0]['imei'])
        (self.step(key='ZeiBL1SCUJyqD', desc='重验申请')
         .step(key='DxqJEdX2eFA2M', desc='imei输入框')
         .custom(lambda: self.ctrl_v())
         .scroll(key='QfTQuQAEgh8B1', desc='审核')
         .step(key='kvGuRiTSnpcsp', desc='审核')
         .step(key='v3twlVPEINRFq', desc='同意')
         .step(key='pT1jF7KGtmTCH', value='备注', action='input', desc='审核说明')
         .step(key='AekohEfQCmSeD', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(d6dbbDv54duJQhN6VKNl)
    def d6dbbDv54duJQhN6VKNl(self):
        self.menu_manage()
        self.copy(self.pc.FYXRA4IxF49PvhUCLpp5Z(data='c')[0]['imei'])
        (self.step(key='Q5pP3wPl2dNTc', desc='重验申请')
         .step(key='xXisqCRoCWrRn', desc='imei输入框')
         .custom(lambda: self.ctrl_v())
         .step(key='n7EV4YbTtp1jg', desc='搜索')
         .scroll(key='veHZYSO70VDuJ', desc='审核')
         .step(key='uXTHRb7YrMcVK', desc='审核')
         .step(key='pZ5fDSaOUtZYQ', desc='拒绝')
         .step(key='WiHlt0yZwIjYE', value='备注', action='input', desc='审核说明')
         .step(key='K9zvcm5sDHY3H', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(CLHIAAqc0GcsqVloSnnm)
    def CLHIAAqc0GcsqVloSnnm(self):
        self.menu_manage()
        self.copy(self.pc.FYXRA4IxF49PvhUCLpp5Z(data='b')[0]['imei'])
        (self.step(key='WjXami5JnM4JP', desc='已质检物品')
         .step(key='XPG8z9EaH7C0j', desc='imei输入框')
         .custom(lambda: self.ctrl_v())
         .step(key='TXIQvCDeILfdX', desc='搜索')
         .step(key='XrnudayELTVvL', desc='修改报告')
         .custom(lambda: self.wait_time())
         .scroll(key='ozO4Xo8mMgGS0',desc='确定')
         .step(key='zGh7xgCKq2Rxx', desc='确定')
         .step(key='rIYlj7lSKNxKO', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(M6cvV0SyzVBbb2kyvAYl)
    def M6cvV0SyzVBbb2kyvAYl(self):
        self.menu_manage()
        self.copy(self.pc.FYXRA4IxF49PvhUCLpp5Z(data='a')[0]['imei'])
        (self.step(key='S2nFF6QOIGfjQ', desc='质检中物品')
         .step(key='nbedb9fLuJfTz', desc='imei输入框')
         .custom(lambda: self.ctrl_v())
         .step(key='wYVI2qooa5fOi', desc='搜索')
         .custom(lambda: self.tab_space(5))
         .step(key='NSQIaKpNycEad', desc='未验移交')
         .step(key='r5tFPlKLBw2A5', desc='接收人')
         .custom(lambda: self.down_enter())
         .step(key='zE9wSGs4RnV0a', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(RXoB3Agr98ilYZlNb5FZ)
    def RXoB3Agr98ilYZlNb5FZ(self):
        self.menu_manage()
        (self.step(key='icvIsW2Rc2YEA', desc='质检中物品')
         .scroll('no_quality_inspection_required')
         .step(key='BXWbHxFufPpUc', desc='无需质检')
         .step(key='YKBpTFCme65kh', desc='质检项1')
         .step(key='U8a22Rx424CQG', desc='质检项2')
         .step(key='IsXYjGdebYKnW', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(y203S2h47mnZp3O3L8J9)
    def y203S2h47mnZp3O3L8J9(self):
        self.menu_manage()
        (self.step(key='ja0dtxzsDJo8X', desc='商品图拍摄')
         .step(key='lrKGrSN0wHsIb', desc='拍商品图')
         .step(key='taWWgYLtFLzrj', value=self.file_path('img'), action='upload', desc='拍商品图')
         .step(key='F2iSd9kr1R5Ci', desc='确认')
         .wait())
        return self


class AptiDaFra0u(CommonPages):
    """运营中心|退货管理"""

    def menu_manage(self):
        """菜单"""
        (self.scroll(key='Z5A6bdcIDg1ic', desc='运营中心')
         .step(key='MaBt7IQQqwgwz', desc='运营中心')
         .step(key='Pl6gEB8Jyin7k', desc='退货管理')
         .wait())
        return self

    @reset_after_execution
    @doc(BBIpXJ7xM3RSMC8Gh7uI)
    def BBIpXJ7xM3RSMC8Gh7uI(self):
        self.menu_manage()
        (self.step(key='oUMj1Hb4oUwlO', desc='待退货')
         .step(key='bGz7GphFwEFth', desc='物品明细')
         .custom(lambda: self.wait_time())
         .custom(lambda: self.tab_space(3))
         .step(key='b9n4oU9fXwLHb', desc='退货出库')
         .step(key='LFUMOYw47uvZe', desc='请选择物流公司')
         .step(key='kFFOOgD06VNrc', desc='选择顺丰速运')
         .step(key='pHuZUPQYhQ3wI', value=self.sf, action='input', desc='请输入物流单号')
         .step(key='oLkpz3M4C20rW', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(oUHwogXGLEfPAQHosTJh)
    def oUHwogXGLEfPAQHosTJh(self):
        self.menu_manage()
        (self.step(key='Co5KmoXbyZvdz', desc='待退货')
         .step(key='drcMGVUPSmCGq', desc='物品明细')
         .custom(lambda: self.wait_time())
         .custom(lambda: self.tab_space(3))
         .step(key='kSygZyxlUcU36', desc='退货出库')
         .step(key='lB1r5MIQQhYef', desc='请选择物流公司')
         .step(key='MGrEtiVIgTyiG', desc='选择京东快运')
         .step(key='NrGPnQGNQ306r', value=self.jd, action='input', desc='请输入物流单号')
         .step(key='TTVpu6VgMaLnt', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(YPSRB7uVXJNfxkNAC56C)
    def YPSRB7uVXJNfxkNAC56C(self):
        self.menu_manage()
        (self.step(key='vevpuKOAHkKVM', desc='待退货')
         .step(key='GJZYmVqq65Mqy', desc='物品明细')
         .custom(lambda: self.wait_time())
         .custom(lambda: self.tab_space(3))
         .custom(lambda: self.tab_space())
         .step(key='GDOR7997xGMb3', desc='导出信息')
         .wait())
        return self

    @reset_after_execution
    @doc(zdM1FoDt6AVwrkGz7nPX)
    def zdM1FoDt6AVwrkGz7nPX(self):
        self.copy(self.mg.D7NTmTMqMuHicClYboqMC(data='a')['pickupCode'])
        self.menu_manage()
        (self.step(key='ImUdYW2wEx6ud', desc='待取货')
         .step(key='tMv7VHxgJeMOW', desc='物品明细')
         .custom(lambda: self.wait_time())
         .custom(lambda: self.tab_space(4))
         .custom(lambda: self.wait_time())
         .step(key='Nn3njr9ZTQtVx', desc='自提出库')
         .step(key='f1vGUoFIXmUMB', desc='扫码或输入自提码')
         .custom(lambda: self.ctrl_v())
         .step(key='tO1FMrlYX3mqN', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(HfHJxVye6T1NL8mbDo1m)
    def HfHJxVye6T1NL8mbDo1m(self):
        self.menu_manage()
        (self.step(key='QYmAXNbk45lNP', desc='待取货')
         .custom(lambda: self.wait_time())
         .step(key='rs25EtC63cB0C', desc='导出信息')
         .wait())
        return self

    @reset_after_execution
    @doc(LvlPCF0VS3XPOtflUi4p)
    def LvlPCF0VS3XPOtflUi4p(self):
        self.menu_manage()
        (self.step(key='wQ45SghNSGtwV', desc='退货已出库')
         .step(key='Ywalwx31JrjeA', desc='批次明细')
         .step(key='rZ1C5CgaqVNEs', desc='更改物流')
         .step(key='VkXybvN1aXwio', desc='请选择物流公司')
         .step(key='ZDSG5giGdaOrl', desc='选择京东快运')
         .step(key='mGnCUeePoKK5F', value=self.jd, action='input', desc='请输入物流单号')
         .step(key='J0iUOWkGB4A1v', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(IYhXWSUAsFy2lcEEwgCS)
    def IYhXWSUAsFy2lcEEwgCS(self):
        self.menu_manage()
        (self.step(key='OFZeEiiTXJHf1', desc='退货已出库')
         .step(key='QxrZgx0f0qgg7', desc='物品明细')
         .step(key='KBVGnNZRpvH6U', desc='更改物流')
         .step(key='HMU0g0zVF0A2T', desc='请选择物流公司')
         .step(key='ISsbHYo6P04jL', desc='选择京东快运')
         .step(key='dJf7HF8uql9Ng', value=self.jd, action='input', desc='请输入物流单号')
         .step(key='isYLorFZjdP63', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(WhYRYd8hMok6D2xnSAXd)
    def WhYRYd8hMok6D2xnSAXd(self):
        self.menu_manage()
        (self.step(key='OBbwff53jdo54', desc='退货已出库')
         .step(key='R14PyzKs4Ka6A', desc='批次明细')
         .custom(lambda: self.wait_time())
         .step(key='zD1bqBb5JFWXj', desc='导出信息')
         .wait())
        return self

    @reset_after_execution
    @doc(tuxJhExUT8EwcOQ2r0od)
    def tuxJhExUT8EwcOQ2r0od(self):
        self.menu_manage()
        (self.step(key='uhd9B13Ly0qjS', desc='退货已出库')
         .step(key='rHPsKCUgBSLPK', desc='物品明细')
         .custom(lambda: self.wait_time())
         .step(key='Sk2Fj1rEnnQDY', desc='导出信息')
         .wait())
        return self

    @reset_after_execution
    @doc(bohSUkZbWonpQxFCek1n)
    def bohSUkZbWonpQxFCek1n(self):
        self.menu_manage()
        (self.step(key='SQl5PL4zUgy1K', desc='退货已出库')
         .step(key='ZbWYDZIKYna1v', desc='物品明细')
         .custom(lambda: self.wait_time())
         .step(key='lX2ZRUpZkS2vl', desc='导出信息')
         .wait())
        return self


class Bk9greLQOjM(CommonPages):
    """运营中心|收货入库"""

    def menu_manage(self):
        """菜单"""
        (self.scroll(key='shTzTeKnLL1JG', desc='运营中心')
         .step(key='zrPAukaFpPIW3', desc='运营中心')
         .step(key='KXr2ekBXoH5hY', desc='收货入库')
         .wait())
        return self

    @reset_after_execution
    @doc(JdFjESShYyLExa0NBUR4)
    def JdFjESShYyLExa0NBUR4(self):
        self.copy(self.pc.VzruD2bzEUPV1JJY9d6vF(i=3)[0]['orderNo'])
        self.menu_manage()
        (self.step(key='rOREsiRlwHhB4', desc='订单编号')
         .custom(lambda: self.ctrl_v())
         .step(key='FzOSyaaWxnjXb', desc='添加')
         .step(key='tFJVnf0zkFN1B', value=self.imei, action='input', desc='输入imei')
         .step(key='eIezO6WDR42cT', desc='录制拆包视频')
         .step(key='fQg6SSlizm1wM', value=self.file_path('video'), action='upload', desc='上传视频')
         .step(key='Ov1vwpFdXx3RI', desc='选择订单编号')
         .custom(lambda: self.down_enter())
         .step(key='ImuxG8YIQv65A', desc='确定')
         .step(key='yhbBDeyK7zn8v', desc='收货入库')
         .custom(lambda: self.wait_time())
         .step(key='X1UhbIsKFYeOG', desc='接收人')
         .custom(lambda: self.down_enter())
         .step(key='InWpK9S6bjCy5', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(IYU1aVy8aH3qWm62ZtJp)
    def IYU1aVy8aH3qWm62ZtJp(self):
        self.unpacking_and_receiving_goods_into_storage()

    @reset_after_execution
    @doc(cLMkHCV4xjRALsu6yfP5)
    def cLMkHCV4xjRALsu6yfP5(self):
        self.copy(self.pc.VzruD2bzEUPV1JJY9d6vF(i=3)[0]['orderNo'])
        self.menu_manage()
        (self.step(key='BCBbWKTRpQCWx', desc='订单编号')
         .custom(lambda: self.ctrl_v())
         .step(key='MKisvODAYexig', desc='添加')
         .step(key='rKvLJcUZb7q3H', desc='录制拆包视频')
         .step(key='lGzKgEJUDPidZ', value=self.file_path('video'), action='upload', desc='上传视频')
         .step(key='c9drbNrR8IKZS', desc='选择订单编号')
         .custom(lambda: self.down_enter())
         .step(key='uGHUizT4j5rcN', desc='确定')
         .step(key='NKRDZjvL9ToIV', desc='收货入库')
         .step(key='gLHaHSQTstjtX', desc='已打印')
         .custom(lambda: self.wait_time())
         .step(key='eUkfOlZ3HPjox', desc='请选择接收人')
         .step(key='A0fjNqBgBND1F', desc='选择admin')
         .step(key='CRoeMGfSZu9ea', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(SICaUhaAsw3CqQfqENpV)
    def SICaUhaAsw3CqQfqENpV(self):
        self.copy(self.pc.VzruD2bzEUPV1JJY9d6vF(i=3)[0]['orderNo'])
        self.menu_manage()
        (self.step(key='pIhst5VYEydx8', desc='订单编号')
         .custom(lambda: self.ctrl_v())
         .step(key='uiaVHe3qvM2E0', desc='添加')
         .step(key='TIe1I5RE70nS4', value=self.imei, action='input', desc='输入imei')
         .step(key='fXlWC8JS04sz8', desc='录制拆包视频')
         .step(key='ZI4GIbCejDYSw', desc='在线录制')
         .step(key='rcj1PWLfDAh28', desc='开始录制')
         .custom(lambda: self.wait_time(3))
         .step(key='za6teB12bOx3j', desc='结束录制')
         .step(key='gPkWqVOACTZMx', desc='确认')
         .custom(lambda: self.wait_time(2))
         .step(key='tENRoVogO5MSc', desc='选择订单编号')
         .custom(lambda: self.down_enter())
         .step(key='nG399QKMqHh70', desc='确定')
         .step(key='cUQntpx6q60D6', desc='收货入库')
         .custom(lambda: self.wait_time())
         .step(key='KaOe6mUuR7m3e', desc='请选择接收人')
         .step(key='iMFLXs7wQvKiq', desc='选择admin')
         .step(key='KfTxj5lIcENz4', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(I6mCUqWhps2B27kclbkx)
    def I6mCUqWhps2B27kclbkx(self):
        self.copy(self.pc.VzruD2bzEUPV1JJY9d6vF(i=3)[0]['expressNo'])
        self.menu_manage()
        (self.step(key='C32nRxV0xNGAX', desc='输入物流单号')
         .custom(lambda: self.ctrl_v())
         .step(key='ItQXUxR0i4CYO', desc='添加')
         .step(key='AVL3b3eQoon5G', value=self.imei, action='input', desc='输入imei')
         .step(key='Oe2ziB5r0rCsF', desc='录制拆包视频')
         .step(key='jJ6WoTNuGLONt', value=self.file_path('video'), action='upload', desc='上传视频')
         .step(key='pWnGvjT6N6oqd', desc='选择订单编号')
         .custom(lambda: self.down_enter())
         .step(key='y5m5gtQbUQAh3', desc='确定')
         .step(key='mVt8WkS7PXzsL', desc='收货入库')
         .custom(lambda: self.wait_time())
         .step(key='A1ZN0tPt16ubm', desc='接收人')
         .custom(lambda :self.down_enter())
         .step(key='mecrh6kp43RC3', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(A9k63GOKEgezsR7PmpCc)
    def A9k63GOKEgezsR7PmpCc(self):
        self.copy(self.pc.VzruD2bzEUPV1JJY9d6vF(i=3)[0]['orderNo'])
        self.menu_manage()
        (self.step(key='LA4kzcDZso1Mv', desc='订单编号')
         .custom(lambda: self.ctrl_v())
         .step(key='dXfTqXN9iSiM0', desc='添加')
         .custom(lambda: self.wait_time())
         .step(key='RiOLqVfVgthp5', desc='修改实收数量')
         .step(key='USiIQtkNAVPr3', value="2", action='input', desc='输入实收数量')
         .step(key='kCQqTlYLoSysG', desc='添加')
         .custom(lambda: self.wait_time())
         .custom(lambda: self.tab_space(3))
         .step(key='rikPC96K4q0s8', desc='批量修改IMEI')
         .step(key='u2EL5vC0LCVZV', value=f"{self.imei},{self.imei}", action='input', desc='输入多个imei')
         .step(key='mdhuqMSh1i84j', desc='确定')
         .step(key='XVOKy01MTOlM8', desc='录制拆包视频')
         .step(key='odTfvlPmk9NnR', value=self.file_path('video'), action='upload', desc='上传视频')
         .step(key='PqmwWPrdQXhfb', desc='选择订单编号')
         .custom(lambda: self.down_enter())
         .step(key='xnxqJFCltHfin', desc='确定')
         .step(key='qHhZlc6IuVYjI', desc='收货入库')
         .custom(lambda: self.wait_time())
         .step(key='P4zt4qcEwpmIT', desc='接收人')
         .custom(lambda: self.down_enter())
         .step(key='hdUSYHROpwJ1c', desc='确定')
         .wait())
        return self


class LULEvBu3aZW(CommonPages):
    """运营中心|订单管理"""

    def menu_manage(self):
        """菜单"""
        (self.scroll(key='rBtBaOUeuQ5Ei', desc='运营中心')
         .step(key='SrhSkOXyaVxqF', desc='运营中心')
         .step(key='OawVz3s6EczNP', desc='订单管理')
         .wait())
        return self


class WpnqXnFPR1X(CommonPages):
    """运营中心|物品出库"""

    def menu_manage(self):
        """菜单"""
        (self.scroll('fulfillment_center_menu', desc='运营中心')
         .step(key='klojMe46NIocM', desc='运营中心')
         .step(key='CmtEW5THS7Kd8', desc='物品出库')
         .wait())
        return self

    @reset_after_execution
    @doc(YtFzTr37KoEb6ObJhKgF)
    def YtFzTr37KoEb6ObJhKgF(self):
        self.copy(self.pc.KmxOWBECeMnMqtP1qACyx(data='a')[0]['articlesNo'])
        self.menu_manage()
        (self.step(key='ky4KnfkbCtdY7', desc='收货商户')
         .step(key='HKbD7m6Bkv8Rf', value=INFO['camera_username'], action='input', desc='收货商户')
         .custom(lambda: self.down_enter())
         .step(key='gzZYGgDt1Mwca', desc='物品编号输入框')
         .custom(lambda: self.ctrl_v_enter())
         .step(key='E6xi9wDagAkU3', desc='物流公司')
         .custom(lambda: self.down_enter())
         .step(key='ESkcGrrD1cFaq', value=self.sf, action='input', desc='物流单号')
         .step(key='Pd5aI1ECWm0HE', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(zGpyxwdonEj5rUxkbGDz)
    def zGpyxwdonEj5rUxkbGDz(self):
        self.copy(self.pc.KmxOWBECeMnMqtP1qACyx(data='a')[0]['articlesNo'])
        self.menu_manage()
        (self.step(key='USQormmt2WrOT', desc='收货商户')
         .step(key='n29WRgxZw9Dim', value=INFO['camera_username'], action='input', desc='收货商户')
         .custom(lambda: self.down_enter())
         .step(key='QmG8XIfZ30ZrG', desc='物品编号输入框')
         .custom(lambda: self.ctrl_v_enter())
         .step(key='yYvpmqm8B5AYQ', desc='物流公司')
         .custom(lambda: self.down_enter(2))
         .step(key='g8dzQCrkUtyIs', value=self.jd, action='input', desc='物流单号')
         .step(key='hPDAJpIqUBbP5', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(hVymbb8xmLoC1GpxmlSy)
    def hVymbb8xmLoC1GpxmlSy(self):
        self.copy(self.pc.KmxOWBECeMnMqtP1qACyx(data='a')[0]['articlesNo'])
        self.menu_manage()
        (self.step(key='L2tme28hBSKjp', desc='收货商户')
         .step(key='LNs2rR9W5ykz5', value=INFO['camera_username'], action='input', desc='收货商户')
         .custom(lambda: self.down_enter())
         .step(key='q1zISlztX88ru', desc='物品编号输入框')
         .custom(lambda: self.ctrl_v_enter())
         .step(key='n1xs6HOICqZ6S', desc='系统叫件')
         .step(key='BF3h12uiQu4z5', value=self.sf, action='input', desc='物流单号')
         .step(key='OVzTFRPMz0iIb', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(yTdtu0H22ya7KmgU59hG)
    def yTdtu0H22ya7KmgU59hG(self):
        self.copy(self.pc.KmxOWBECeMnMqtP1qACyx(data='a')[0]['articlesNo'])
        self.menu_manage()
        (self.step(key='bfjSVDloxhBnY', desc='收货商户')
         .step(key='LRp9LmQs12q7d', value=INFO['camera_username'], action='input', desc='收货商户')
         .custom(lambda: self.down_enter())
         .step(key='kmNN6QMYsPeek', desc='物品编号输入框')
         .custom(lambda: self.ctrl_v_enter())
         .step(key='MNUz6dJziz3F5', desc='系统叫件')
         .step(key='zV96fulOD7J5p', desc='京东')
         .step(key='QEnrGGQkod9FS', value=self.jd, action='input', desc='物流单号')
         .step(key='ANj3N7VL8qf0e', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(g4RyFUrC2BkjMHRKinuq)
    def g4RyFUrC2BkjMHRKinuq(self):
        self.copy(self.mc.UAPqxpSx1qiMwyQEcIPXb(i=3)[0]['articlesNo'])
        self.menu_manage()
        (self.step(key='ZVaMAAqd7sFX5', desc='自提')
         .step(key='cEXZYQNBkhDfY', action='input', desc='自提码')
         .custom(lambda: self.ctrl_v_enter())
         .step(key='adJCuZVlC6gIv', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(OP7wFFxaC2oDvVTeezXi)
    def OP7wFFxaC2oDvVTeezXi(self):
        self.copy(self.pc.YBoIFlRaGyVtfzeObzsmf(i=1)[0]['articlesNo'])
        self.menu_manage()
        (self.step(key='egkcN4RIxfEab', desc='物品输入框')
         .custom(lambda: self.ctrl_v_enter())
         .step(key='DNLvPNzeaprhI', desc='确认')
         .wait())
        return self


    @reset_after_execution
    @doc(TNLKcCWf408wxkwt8y53)
    def TNLKcCWf408wxkwt8y53(self):
        self.copy(self.pc.YBoIFlRaGyVtfzeObzsmf(i=1)[0]['articlesNo'])
        self.menu_manage()
        (self.step(key='PjS92uWXs2Cmf', desc='自提')
         .step(key='tgZFHX74i2qVy', desc='物品输入框')
         .custom(lambda: self.ctrl_v_enter())
         .step(key='kvPuJBu0y0Tih', desc='确认')
         .wait())
        return self
