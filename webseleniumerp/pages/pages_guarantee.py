# coding: utf-8
import os
from common.base_page import BasePage, ImportDataEdit, reset_after_execution
from common.base_params import InitializeParams
from common.import_desc import *
from config.settings import DATA_PATHS


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


class X9UYAKxbu2B(CommonPages):
    """保卖管理|订单列表"""

    def menu_manage(self):
        """菜单"""
        (self.scroll('guarantee_menu', desc='保卖管理')
         .step(key='ZB08dwCRpCZFS', desc='保卖管理')
         .step(key='T1Fn5DLM4TQmv', desc='订单列表')
         .wait())
        return self

    @reset_after_execution
    @doc(GIh2R4s4U7in3JVtx4Fh)
    def GIh2R4s4U7in3JVtx4Fh(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2, j=3)[0]['articlesNo'])
        (self.step(key='INefSEcuKHThe', desc='快速保卖')
         .step(key='oW8Ugdi7VKXba', desc='物品编号输入框')
         .step(key='m46HH0XJgfYt5', desc='物品编号输入框')
         .custom(lambda: self.ctrl_v())
         .step(key='cYpkUT17u57RR', desc='确认输入')
         .step(key='xbwWC6dWY4pZi', value=998, action='input', desc='期望卖出价')
         .step(key='fJgO5AtzoLjzB', desc='提交')
         .wait())
        return self

    @reset_after_execution
    @doc(RhI0OGk9VBc64gZxM8di)
    def RhI0OGk9VBc64gZxM8di(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2, j=3)[0]['articlesNo'])
        (self.step(key='QUUNgsOBS1MAd', desc='快速保卖')
         .step(key='cvdFkosDtdOCd', desc='物品编号输入框')
         .step(key='QwTP1lK3sZdGH', desc='物品编号输入框')
         .custom(lambda: self.ctrl_v())
         .step(key='T5CwU9qQPX819', desc='确认输入')
         .step(key='ig2y9kY6LLORA', value=998, action='input', desc='期望卖出价')
         .step(key='sAiOR34rmGHZh', desc='提交并发货')
         .step(key='VSpWsT3Vh2GUb', desc='选择顺丰')
         .step(key='iBz5IZf8dsw50', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(bPbBryEdt8zpTVH8jCsI)
    def bPbBryEdt8zpTVH8jCsI(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2, j=3)[0]['articlesNo'])
        (self.step(key='rdvV4snjnlpSk', desc='快速保卖')
         .step(key='GDJFYrgkCjwZT', desc='物品编号输入框')
         .step(key='HXwUYjzORtyC8', desc='物品编号输入框')
         .custom(lambda: self.ctrl_v())
         .step(key='t6IIDwAxAs1fB', desc='确认输入')
         .step(key='lAQY5DwSHyWPB', value=998, action='input', desc='期望卖出价')
         .step(key='M8cyEqF9dWs28', desc='提交并发货')
         .step(key='iZX11hR9JCWpT', desc='选择京东')
         .step(key='la56QcmBDdt84', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(tJ9cjeZUkU75SEVnk6wT)
    def tJ9cjeZUkU75SEVnk6wT(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2, j=3)[0]['articlesNo'])
        (self.step(key='DBJyOOTWG2lN1', desc='快速保卖')
         .step(key='SwwY4FjKRhKbk', desc='物品编号输入框')
         .step(key='Ir37d058ssl36', desc='物品编号输入框')
         .custom(lambda: self.ctrl_v())
         .step(key='UvGS4efxwM4kf', desc='确认输入')
         .step(key='JGO4lmUbWDAPn', value=998, action='input', desc='期望卖出价')
         .step(key='adrxzFkuU6Rda', desc='提交并发货')
         .step(key='Tp5sCxgjQ3wiN', desc='选择自行邮寄')
         .step(key='jhDdFz9pP6Qvu', value=self.jd, action='input', desc='物流单号')
         .step(key='UDjBZs6CeUuWw', desc='选择物流公司')
         .custom(lambda: self.down_enter(6))
         .step(key='sir7IEzSQx4uH', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(gh0hljAZOag10KerWd2i)
    def gh0hljAZOag10KerWd2i(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2, j=3)[0]['articlesNo'])
        (self.step(key='VlTlfeTDIFybG', desc='快速保卖')
         .step(key='MEtBGGEXFFZzA', desc='物品编号输入框')
         .step(key='VoOs8HeTFJtMR', desc='物品编号输入框')
         .custom(lambda: self.ctrl_v())
         .step(key='NYzX39IuMnFva', desc='确认输入')
         .step(key='EDUDC9DmOTrx7', value=998, action='input', desc='期望卖出价')
         .step(key='MHUOYzVJDYUq7', desc='提交并发货')
         .step(key='yfS2FVXU7KyeC', desc='选择自己送货')
         .step(key='tPz5A7RFSxAid', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(UxlDI72fkMivOA7TlGvw)
    def UxlDI72fkMivOA7TlGvw(self):
        self.menu_manage()
        (self.step(key='oM5OLjukm0FoO', desc='立即发货')
         .step(key='RmMsBJT5VVESs', desc='选择顺丰')
         .step(key='XXXzwQgbRT47M', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(BSo6LUJtzBWcj6edgXxU)
    def BSo6LUJtzBWcj6edgXxU(self):
        self.menu_manage()
        (self.step(key='LHR3EVNFGoRdg', desc='立即发货')
         .step(key='FeLgw4ejb2i39', desc='提交并发货')
         .step(key='tyKHGEwPnsfN8', desc='选择京东')
         .step(key='iP5seSQPNhF7U', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(LPxZ1LIoEgSsdKTXRL2C)
    def LPxZ1LIoEgSsdKTXRL2C(self):
        self.menu_manage()
        (self.step(key='zMyiX2EKWTh9u', desc='立即发货')
         .step(key='HkqItC8s184Xa', desc='选择自行邮寄')
         .step(key='W9GiESieELs4Z', value=self.jd, action='input', desc='输入物流单号')
         .step(key='ZgeesNII2YCDd', desc='选择物流公司')
         .custom(lambda: self.down_enter(6))
         .step(key='S3E7NxpjmJ3cc', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(NEZ4KVsoQr6AgkUVtSBE)
    def NEZ4KVsoQr6AgkUVtSBE(self):
        self.menu_manage()
        (self.step(key='H7K4v5xeKDZWh', desc='取消订单')
         .step(key='f4Ig8RRjvzQtD', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(qAhAnnHA7i5RWoR9HPAf)
    def qAhAnnHA7i5RWoR9HPAf(self):
        self.menu_manage()
        (self.step(key='KeqlTY68HWLOt', desc='重新发货')
         .step(key='R1xqpampvBvwi', desc='选择顺丰')
         .step(key='QHu0uTjtOEPrI', desc='确定')
         .wait())
        return self


class T7ivLbBgHgV(CommonPages):
    """保卖管理|退货管理"""

    def menu_manage(self):
        """菜单"""
        (self.scroll('guarantee_menu', desc='保卖管理')
         .step(key='QbV3j1glBKd3v', desc='保卖管理')
         .step(key='iPklPgZ4VTtOX', desc='退货管理')
         .wait())
        return self

    @reset_after_execution
    @doc(uMfpb3JIBZ8oaq0US9Y7)
    def uMfpb3JIBZ8oaq0US9Y7(self):
        self.menu_manage()
        (self.step(key='AiXGoVfRc2kr8', desc='待退货')
         .step(key='z1gn8HlmGZaD9', desc='取消退货')
         .step(key='aFTX8pnyoMC0B', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(LFI07j6GScehS4q0GPNd)
    def LFI07j6GScehS4q0GPNd(self):
        self.menu_manage()
        (self.step(key='cBAQk8AcCvtuQ', desc='待退货')
         .step(key='mNTB9HYiwUYFP', desc='更改退货方式')
         .step(key='uiUw9pYjRAQ4Z', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(sbzcNzKjCNBmnqXBUAZP)
    def sbzcNzKjCNBmnqXBUAZP(self):
        self.menu_manage()
        (self.step(key='koixk9sQdzRoD', desc='待取货')
         .step(key='T6JhKRzJhhbsF', desc='取消退货')
         .step(key='tzf00tiD62kGn', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(WkJbfcCwi0eL85pLx7Hw)
    def WkJbfcCwi0eL85pLx7Hw(self):
        self.menu_manage()
        (self.step(key='KAPU0zEU0UJgA', desc='待取货')
         .step(key='XzRI1xOWmGv5V', desc='更改退货方式')
         .step(key='D49MX8515lxPu', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(K4TenJe5ql1CTH4mOryF)
    def K4TenJe5ql1CTH4mOryF(self):
        self.menu_manage()
        (self.step(key='Tx677FfYjzx72', desc='退货已出库')
         .step(key='gLse1A6mzT6Tv', desc='确认收货')
         .wait())
        return self


class QDeWfd8HC8U(CommonPages):
    """保卖管理|商品管理"""

    def menu_manage(self):
        """菜单"""
        (self.scroll('guarantee_menu', desc='保卖管理')
         .step(key='wI6aS8Omo4qOR', desc='保卖管理')
         .step(key='q5055J75UnIJp', desc='商品管理')
         .wait())
        return self

    @reset_after_execution
    @doc(wyRAHLmyY7udk5keYovB)
    def wyRAHLmyY7udk5keYovB(self):
        self.menu_manage()
        (self.step(key='AIQjL8jbyiKSf', desc='退货')
         .step(key='v64In6h6v4WsD', desc='下一步')
         .step(key='HgOURFhLhhmPi', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(DaKhYSFHyjQUhftVcT2W)
    def DaKhYSFHyjQUhftVcT2W(self):
        self.menu_manage()
        (self.step(key='ahNCOLxWAt2bC', desc='退货')
         .step(key='TlWFmabeU6LVp', desc='下一步')
         .step(key='sryvKHKnWkUBZ', desc='自提')
         .step(key='pG9EYtNBK3rt8', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(bEf5Mp7G2xinW35U9v4n)
    def bEf5Mp7G2xinW35U9v4n(self):
        self.menu_manage()
        (self.step(key='ctLmChTmgrtJn', desc='销售')
         .step(key='M9cSt7qTxcfrw', desc='今日参考价')
         .step(key='bC3dLiQZeFr5r', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(ecdR9lamw6zn0y9vyNRF)
    def ecdR9lamw6zn0y9vyNRF(self):
        self.menu_manage()
        (self.step(key='xn0hYTUcEi7sZ', desc='取消销售')
         .step(key='DGzuAw11eDbjo', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(LrCC4svDp0JANhnDhJZH)
    def LrCC4svDp0JANhnDhJZH(self):
        self.menu_manage()
        (self.step(key='H9pgbxNKUfn2Q', desc='改价')
         .step(key='Ic8SSUD228PdY', value="50", action='input', desc='输入价格')
         .step(key='Cz3Gnoj0ZQDGB', desc='确认改价')
         .wait())
        return self
