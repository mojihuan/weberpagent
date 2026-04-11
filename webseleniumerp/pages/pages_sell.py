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
            'excel': os.path.join(DATA_PATHS['excel'], 'sell_goods_listing_import.xlsx'),
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


class SHoWS2sIDk6(CommonPages):
    """商品销售|销售售后管理|销售售后处理"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='iEp3pZFGlnF7b', desc='商品销售')
         .step(key='gCgeJH2jFIuBG', desc='销售售后管理')
         .step(key='hJf341LHn9qQ9', desc='销售售后处理')
         .wait())
        return self

    @reset_after_execution
    @doc(DjkghfK5et2Z3KvN6d3n)
    def DjkghfK5et2Z3KvN6d3n(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=3, j=9)[0]['articleNo'])
        (self.step(key='JpXfzjdOI1Hd5', desc='物品编号输入框')
         .custom(lambda: self.ctrl_v_enter())
         .step(key='AUvCUYbR8EPiE', desc='销售售后处理')
         .step(key='UFaX3DH7jkTnF', desc='售后类型')
         .custom(lambda: self.down_enter())
         .step(key='h5bBNbd3l5PNg', desc='已收货')
         .step(key='NFmThTyIfsg1o', desc='流转仓库')
         .custom(lambda: self.down_enter())
         .step(key='VByyoUqOJWJb4', value=self.serial, action='input', desc='备注')
         .step(key='zoyWJZS3W8mKX', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(kveY9vSZiCveNHGRKZ5u)
    def kveY9vSZiCveNHGRKZ5u(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=3, j=9)[0]['articleNo'])
        (self.step(key='q92Ge8xrnDTn8', desc='物品编号输入框')
         .custom(lambda: self.ctrl_v_enter())
         .step(key='hGkW2tmov1AjS', desc='销售售后处理')
         .step(key='lgRWHzSNCA1MU', desc='售后类型')
         .custom(lambda: self.down_enter(2))
         .step(key='Pc3G7DZvQDQMe', value='2873', action='input', desc='新销售结算价')
         .step(key='DZpF6wDCFoLUJ', desc='配件分类')
         .custom(lambda: self.up_arrow_return(2))
         .step(key='srGkU1lLGGlMT', desc='配件分类')
         .step(key='PYuyg6n8h7ndW', desc='配件名称')
         .custom(lambda: self.up_enter())
         .step(key='rD07NBg4OMpWg', desc='品牌')
         .custom(lambda: self.up_enter())
         .step(key='tqqGqMXXbLZxG', desc='型号')
         .custom(lambda: self.up_enter())
         .step(key='zYpor3Uwkj6xq', desc='配件渠道')
         .custom(lambda: self.up_enter())
         .step(key='zOSfjg5jivslG', value='122', action='input', desc='配件价值')
         .step(key='hybgMKlzcB1XW', value=self.jd, action='input', desc='物流单号')
         .step(key='hyAHEWL0cEIhc', value=self.serial, action='input', desc='备注')
         .step(key='QvEhNli0gIgEK', desc='确定')
         .wait())
        return self


class JTc35i3PMbz(CommonPages):
    """商品销售|销售管理|销售上架"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='V1VUlm6LpgEBq', desc='商品销售')
         .step(key='CIez2uB8IPFRm', desc='销售管理')
         .step(key='S4YD7cNkIT29B', desc='销售上架')
         .wait())
        return self

    @reset_after_execution
    @doc(kiSivAHj3Vab5m78JpuW)
    def kiSivAHj3Vab5m78JpuW(self):
        self.menu_manage()
        self.file.get_inventory_data('excel', 'articles_no', i=2, j=13)
        (self.step(key='r6UJyy1WOREBX', desc='销售客户')
         .custom(lambda: self.down_enter())
         .step(key='lZmIKjs68WLJ0', desc='物品输入框')
         .custom(lambda: self.ctrl_v())
         .step(key='km9MsNB0OLAW4', desc='添加物品')
         .step(key='OnKyeCQ8am0jl', value='263', action='input', desc='设置销售价')
         .step(key='mF96A3wAzwnK7', value=self.serial, action='input', desc='平台物品编号')
         .step(key='u6yyfwqSeMu7O', value=self.serial, action='input', desc='备注')
         .step(key='xPpFeveu78l7a', desc='确认添加')
         .wait())
        return self


class EHPPgSmlpeU(CommonPages):
    """商品销售|销售管理|待接收物品"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='yfEJqRQCS8eWM', desc='商品销售')
         .step(key='WFG7KkZE4dnCc', desc='销售管理')
         .step(key='gNT4Ky1eQLMCh', desc='待接收物品')
         .wait())
        return self

    @reset_after_execution
    @doc(Hu4K5bokoTCxa0RXNIan)
    def Hu4K5bokoTCxa0RXNIan(self):
        self.menu_manage()
        (self.step(key='wMbmevfYnVuNV', desc='全选')
         .step(key='NyRhFGzJ2c90X', desc='接收')
         .step(key='GwRtIpxPgvuRL', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(hnFxpME7kKdGGlUyloly)
    def hnFxpME7kKdGGlUyloly(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2)[0]['articlesNo'])
        (self.step(key='gc66k3DtoCzQ6', desc='扫码精确接收')
         .custom(lambda: self.ctrl_v_enter())
         .step(key='LyPBNu7Y3RW3u', desc='接收')
         .step(key='yevOmVAR4rGIY', desc='确定')
         .wait())
        return self


class CR6FpKLnxxS(CommonPages):
    """商品销售|销售管理|销售中物品列表"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='gyA1B2I9wwJs1', desc='商品销售')
         .step(key='U4Blua9795Nzq', desc='销售管理')
         .step(key='IdaKsDCxociZd', desc='销售中物品列表')
         .wait())
        return self

    @reset_after_execution
    @doc(PJcVirkG5vjAdGnxgXpV)
    def PJcVirkG5vjAdGnxgXpV(self):
        self.menu_manage()
        self.file.get_inventory_data('excel', 'imei', i=2, j=13)
        (self.step(key='gQmZkmsYXJ3Gd', desc='修改销售信息')
         .step(key='f8y3JLTmZh6Oa', desc='导入添加')
         .step(key='FUddrLn2QARMQ', desc='导入模版')
         .custom(lambda: self.up_arrow_return(2))
         .step(key='lsS9hfOgUuu7b', value=self.file_paths['excel'], action='upload', desc='上传文件')
         .step(key='Ja6u5a5x4Ii9l', desc='确定')
         .step(key='X8Cfh80idSuFH', value=self.serial, action='input', desc='新平台物品编号')
         .scroll('edit_status_price', desc='新销售定价')
         .step(key='qpc9NGaUP5E9j', value=self.number, action='input', desc='新销售定价')
         .step(key='e83jcFqhNzOtz', desc='确认修改')
         .wait())
        return self

    @reset_after_execution
    @doc(rrBrdjBX494MEDd1GeWh)
    def rrBrdjBX494MEDd1GeWh(self):
        self.menu_manage()
        (self.step(key='Uifs0DrpO8t2U', desc='更新销售状态')
         .step(key='GkEoQiJAAMxti', desc='未收款')
         .step(key='EeAolD7JugQEn', value=self.jd, action='input', desc='物流单号')
         .step(key='iXAPWD5wfQB4m', value=self.number, action='input', desc='物流费用')
         .step(key='XiAl6AtAUkXKN', desc='确认销售')
         .wait())
        return self

    @reset_after_execution
    @doc(zGRElY85yjm7F6rhrCx3)
    def zGRElY85yjm7F6rhrCx3(self):
        self.menu_manage()
        (self.step(key='y1EWruoMXmGCS', desc='下架')
         .step(key='PLzUoUhmQBq9j', desc='添加')
         .custom(lambda: self.wait_time())
         .step(key='PVDI7hPRW7uEm', desc='确认下架')
         .wait())
        return self

    @reset_after_execution
    @doc(WWNIdAfb7nswviGGMLKI)
    def WWNIdAfb7nswviGGMLKI(self):
        self.menu_manage()
        (self.step(key='IOKYPflQwBL8Q', desc='销售中')
         .step(key='sTr5DdLCc3CpY', desc='单选')
         .step(key='ErA7dMvfqjepS', desc='批量下架')
         .step(key='FNBEIutBZX05l', desc='添加')
         .step(key='wnGKA49EWpONm', desc='确认下架')
         .wait())
        return self


class E2yktvttmCT(CommonPages):
    """商品销售|销售管理|待销售物品"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='lQRuKyK1z2RE4', desc='商品销售')
         .step(key='n75YpDpZUZZva', desc='销售管理')
         .step(key='b5yszVluNhbS0', desc='待销售物品')
         .wait())
        return self

    @reset_after_execution
    @doc(iqOJswY1Y3kNWO1jXmAc)
    def iqOJswY1Y3kNWO1jXmAc(self):
        self.menu_manage()
        (self.step(key='ZT6SFK2sMsSKs', desc='单选')
         .step(key='Dt27jcBzqxLb8', desc='上架')
         .step(key='fIXpsuLPWIsKk', desc='销售客户')
         .custom(lambda: self.up_enter())
         .step(key='CmoYIcovLpAup', value='299', action='input', desc='销售定价')
         .step(key='npVkQzkF3LaJi', value=self.serial, action='input', desc='平台物品编号')
         .step(key='A4XEYr83SFECz', value=self.serial, action='input', desc='备注')
         .step(key='izElI8ldv8W0q', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(psGTQePHRPXOVLvXlZU5)
    def psGTQePHRPXOVLvXlZU5(self):
        self.menu_manage()
        (self.step(key='JFCt4n1DBKHcX', desc='单选')
         .step(key='aPsVshclooxip', desc='出库')
         .step(key='QZlp9WbKUXy2t', desc='销售客户')
         .custom(lambda: self.up_enter())
         .step(key='rhvngZIvXf3au', value=self.jd, action='input', desc='物流单号')
         .step(key='SIvhEfanArZKn', value='12', action='input', desc='物流费用')
         .scroll('sell_sales_amount', desc='销售金额')
         .step(key='Oyv7wCmTyvDSL', value='263', action='input', desc='销售金额')
         .step(key='aEDXcXx0UOBrk', value=self.serial, action='input', desc='平台物品编号')
         .step(key='wIfTfIRNc0Ulr', value=self.serial, action='input', desc='平台销售订单号')
         .scroll('money_not_received', desc='未收款')
         .step(key='cS4uHAU3cUKiU', desc='未收款')
         .step(key='X7GvrzWaQMmU5', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(BjtCW4zAlmHFf4hnEsyK)
    def BjtCW4zAlmHFf4hnEsyK(self):
        self.menu_manage()
        (self.step(key='OCSVZgVFj7AR6', desc='单选')
         .step(key='Vk9gKh1BaXiy8', desc='出库')
         .step(key='yG9jDkvlpCbR5', desc='铺货预售出库')
         .step(key='IPo0huVctds9k', desc='销售客户')
         .custom(lambda: self.up_enter())
         .step(key='IvWM51xDa4STc', desc='预售')
         .step(key='ckhusdZ8VJLGf', value=self.jd, action='input', desc='物流单号')
         .step(key='QTzfiDlrmyVH1', value='21', action='input', desc='物流费用')
         .step(key='Av4eKulUj2olB', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(aMAnXMswO97RRUy2WDp5)
    def aMAnXMswO97RRUy2WDp5(self):
        self.menu_manage()
        (self.step(key='Z6P6ZSm2ugKN1', desc='单选')
         .step(key='rS45Z7EruS2Tn', desc='出库')
         .step(key='E3HRErNvb1z27', desc='铺货预售出库')
         .step(key='JRxJeZFAZPELr', desc='销售客户')
         .custom(lambda: self.up_enter())
         .step(key='GPITqWGhDKckN', desc='铺货')
         .step(key='eiz2EVJRoWOLa', desc='未收款')
         .step(key='HvTwTout8p2aY', desc='收款账户')
         .custom(lambda: self.up_enter())
         .step(key='fkhK56cK0B2Y7', value=self.jd, action='input', desc='物流单号')
         .step(key='uWmWC2LCds6P6', value='14', action='input', desc='物流费用')
         .scroll('remark_3', desc='备注')
         .step(key='WvB5U179EIpgg', value='115', action='input', desc='销售金额')
         .step(key='DUzCtwjDCUnic', value=self.serial, action='input', desc='备注')
         .step(key='aPiXpyQFbzioq', desc='确认')
         .wait())
        return self


class A16z5xHZdDb(CommonPages):
    """商品销售|销售管理|已销售物品列表"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='G5ZrwyklcfGMc', desc='商品销售')
         .step(key='ObTlmlD00aXxa', desc='销售管理')
         .step(key='QoCbI1wNgzveb', desc='已销售物品列表')
         .wait())
        return self

    @reset_after_execution
    @doc(J6LQWn0szGuyNJ0UuFq8)
    def J6LQWn0szGuyNJ0UuFq8(self):
        self.menu_manage()
        (self.step(key='ZHR4ByBs5hCV7', desc='单选')
         .step(key='AKVjlaabXPl0y', desc='销售售后')
         .step(key='sEWkgxyUqfpUk', desc='销售售后处理')
         .step(key='j9HA4tD823CzH', value='1982', action='input', desc='新销售结算价')
         .step(key='E1UqCVN3xKieV', value=self.serial, action='input', desc='备注')
         .step(key='RkZgfgRqZMSan', desc='确定')
         .wait())
        return self


    @reset_after_execution
    @doc(QBOIk1dLbtE83J6puWEy)
    def QBOIk1dLbtE83J6puWEy(self):
        self.menu_manage()
        (self.step(key='Oe7yryBZOd7OA', desc='单选')
         .step(key='shn0c7LvyMxCK', desc='销售售后')
         .step(key='rRjatdEsRxepU', desc='销售售后处理')
         .step(key='b9X6jGBlMKJ7U', desc='售后类型')
         .custom(lambda: self.down_enter())
         .step(key='pwe49OhQ9AQm5', desc='已收货')
         .step(key='foXo8EgE8o6M2', desc='流转仓库')
         .custom(lambda: self.down_enter())
         .step(key='claHSNlC2di5r', value=self.serial, action='input', desc='备注')
         .step(key='bEXJvsxYQONdc', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(JjVcGp9jSl8TI9nj2xVw)
    def JjVcGp9jSl8TI9nj2xVw(self):
        self.menu_manage()
        (self.step(key='HuCo0TzCPJWeG', desc='单选')
         .step(key='CkcNy1iFn74aN', desc='销售售后')
         .step(key='YGDw3zCZKGgwv', desc='销售售后处理')
         .step(key='RRFfFPkbkd7Ga', desc='售后类型')
         .custom(lambda: self.down_enter(2))
         .step(key='Z4sxhQ7LWjlK4', value='100', action='input', desc='新销售结算价')
         .step(key='VGqoFIeTu30Yk', desc='配件分类')
         .custom(lambda: self.up_arrow_return(2))
         .step(key='bTO3XeGYKE98W', desc='配件分类')
         .step(key='yG8SLOtGRQF3w', desc='配件名称')
         .custom(lambda: self.up_enter())
         .step(key='A5ZHkX8EMCRJp', desc='品牌')
         .custom(lambda: self.up_enter())
         .step(key='vrANWBkzMBNqm', desc='型号')
         .custom(lambda: self.up_enter())
         .step(key='vI5NUfXDx66rh', desc='配件渠道')
         .custom(lambda: self.up_enter())
         .step(key='i97ftiKM5HanG', value='23', action='input', desc='配件价值')
         .step(key='Cmjb49gCS5sPP', value=self.jd, action='input', desc='物流单号')
         .step(key='S8kNaxbRKyYOI', value=self.serial, action='input', desc='备注')
         .step(key='KXEYCf7yj5RYk', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(gVnbM599DimecmAZ6Xlg)
    def gVnbM599DimecmAZ6Xlg(self):
        self.menu_manage()
        (self.step(key='OiZR0JtAq2us8', desc='单选')
         .step(key='o7FH2eVxyuRE0', desc='销售售后')
         .step(key='NFy4MoFzwOsSt', desc='销售售后处理')
         .step(key='LfsAibvQfmowS', desc='售后类型')
         .custom(lambda: self.down_enter(4))
         .step(key='CcJWHpwbGAuVG', value=self.serial, action='input', desc='备注')
         .step(key='XALq9TrIUWVf0', desc='确定')
         .wait())
        return self


class YRaemFF1a0b(CommonPages):
    """商品销售|销售售后管理|销售售后列表"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='oosSuB1KnUg3s', desc='商品销售')
         .step(key='kJ8R6tAxCn1xN', desc='销售售后管理')
         .step(key='hPsFswgiOM4jm', desc='销售售后列表')
         .wait())
        return self

    @reset_after_execution
    @doc(GDdc1h1eADXbjk8ujR60)
    def GDdc1h1eADXbjk8ujR60(self):
        self.menu_manage()
        (self.step(key='AfHn3DwYW6hRE', desc='单选')
         .step(key='bmnMa0IUGCI6l', desc='更新售后状态')
         .step(key='Ygz2KLzpu5CQg', desc='流转仓库')
         .custom(lambda: self.up_enter())
         .step(key='EQ2al0YTC8DKg', desc='确认入库')
         .wait())
        return self

    @reset_after_execution
    @doc(xSQE9e6LbvvilOg9OMsy)
    def xSQE9e6LbvvilOg9OMsy(self):
        self.menu_manage()
        (self.step(key='vKtKfcZY03Gnl', desc='单选')
         .step(key='lozhRKEXu3brX', desc='更新售后状态')
         .step(key='r1grPEtvJvEIk', desc='退货退款')
         .step(key='f82dfEM0bK3zR', value='23', action='input', desc='平台售后罚款')
         .step(key='TZmdwOkqvmXV8', value=self.serial, action='input', desc='备注')
         .step(key='HCQF4TzvcKDVU', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(ebhsQ41HitCvjEsvMz0G)
    def ebhsQ41HitCvjEsvMz0G(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2, j=15)[0]['imei'])
        (self.step(key='HR7cCzq2jFl2V', desc='单选')
         .step(key='R1K7Gg98Qoi6w', desc='更新售后状态')
         .step(key='pBFFOb3jGEj8a', desc='换货')
         .step(key='NFAGDu6IvzmFn', desc='去出库')
         .step(key='HvjBACGytjPks', value=self.jd, action='input', desc='物流单号')
         .step(key='cmL8Q62CQ1mNp', value='23', action='input', desc='物流费用')
         .scroll('barter_item_input', desc='换货出库物品输入框')
         .step(key='zd8zPzvBWuXsP', desc='换货出库物品输入框')
         .custom(lambda: self.ctrl_v())
         .step(key='iydMsh03a9PKN', desc='添加')
         .scroll('barter_remark_2', desc='备注信息')
         .step(key='GCNvtOD1gOQnq', value='10', action='input', desc='销售结算价')
         .step(key='Edrbq9lkY9CgT', value=self.serial, action='input', desc='平台销售订单号')
         .step(key='JGOJHIvkCU9sd', value=self.serial, action='input', desc='备注信息')
         .step(key='MbxX6mAlt7shu', desc='确认出库')
         .wait())
        return self

    @reset_after_execution
    @doc(GdXpXPawmTeBaOha9VUo)
    def GdXpXPawmTeBaOha9VUo(self):
        self.menu_manage()
        (self.step(key='wJgV3DGsRQu7g', desc='单选')
         .step(key='UsVhXb7f7dAf5', desc='更新售后状态')
         .step(key='GUHFmQ7vh8AxW', desc='拒退退回')
         .step(key='pQS9YpdjgCJmV', desc='去出库')
         .step(key='k2cZWaEEy9J5J', value=self.jd, action='input', desc='物流单号')
         .step(key='NOcKw5m8gaPb8', value='11', action='input', desc='物流费用')
         .step(key='xIfYEMUNfz3Fh', desc='确认出库')
         .wait())
        return self

    @reset_after_execution
    @doc(pt4gIHCRgdVZv3FGKFVq)
    def pt4gIHCRgdVZv3FGKFVq(self):
        self.menu_manage()
        (self.step(key='mhM2V6M5PkIND', desc='单选')
         .step(key='cFTTT1uI2B5vE', desc='更新售后状态')
         .step(key='OwCzCGYkf8cZO', desc='返修')
         .step(key='ZyRvEGlvGnrXz', desc='去出库')
         .step(key='OZfMi2F7Pffwx', value=self.jd, action='input', desc='物流单号')
         .step(key='VsBofectXpq0S', value='14', action='input', desc='物流费用')
         .step(key='DrlpzE92JXNNL', desc='确认出库')
         .wait())
        return self
