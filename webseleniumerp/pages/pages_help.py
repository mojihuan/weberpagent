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
            'excel': os.path.join(DATA_PATHS['excel'], 'help_sell_orders_import.xlsx')
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


class Qofwr8xFsgu(CommonPages):
    """帮卖管理|帮卖上架列表"""

    def menu_manage(self):
        """菜单"""
        (self.scroll(key='t3OMQNdItKEv0', desc='帮卖管理')
         .step(key='IZ5eSwaqVCY8S', desc='帮卖管理')
         .step(key='Xle4YOX86JRBK', desc='帮卖上架列表')
         .wait())
        return self

    @reset_after_execution
    @doc(x2Ue8YzUHAdfE5e1ah2B)
    def x2Ue8YzUHAdfE5e1ah2B(self):
        self.menu_manage()
        (self.step(key='k4rKOd9vNxQNW', desc='发起帮卖')
         .step(key='fBr8bVEElCDqD', desc='从库存列表添加')
         .step(key='OcBWfE8YCNAwK', desc='搜索')
         .custom(lambda: self.tab_space(3))
         .scroll('confirm_select', desc='确认选择')
         .step(key='M8CpyOVVxSOp8', desc='确认选择')
         .custom(lambda: self.wait_time(2))
         .wait())
        return self

    @reset_after_execution
    def place_a_help_order(self):
        self.menu_manage()
        (self.step(key='qa2WnN5MiNOld', desc='发起帮卖')
         .step(key='LrwKVtNDwWpZc', desc='从库存列表添加')
         .step(key='gcuonClSlnq3X', desc='搜索')
         .custom(lambda: self.tab_space(3))
         .scroll('confirm_select', desc='确认选择')
         .step(key='Jri4N0kr9PWmf', desc='确认选择')
         .step(key='E1B5o5oepMd50', value=self.number, action='input', desc='期望价格')
         .step(key='Td0CraLnKGhuN', desc='添加')
         .custom(lambda: self.tab_space(3))
         .step(key='bs88EjffGXXCP', value=self.serial, action='input', desc='批次备注')
         .step(key='AAeQlG06m4XeI', desc='生成帮卖订单')
         .step(key='tCCJhESypdAZW', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(gHXYe9nXDQKo8k2pCpHF)
    def gHXYe9nXDQKo8k2pCpHF(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2)[0]['imei'])
        (self.step(key='I6Pbo2kwzCUQv', desc='发起帮卖')
         .step(key='ob9JJiCrFZ6rn', desc='物品编号')
         .custom(lambda: self.ctrl_v())
         .step(key='cynkyGlBm2lVT', desc='添加')
         .step(key='fYJkT6vOXXusr', value=self.number, action='input', desc='期望价格')
         .step(key='ZmYE9juoSg3Hx', desc='添加')
         .custom(lambda: self.tab_space(3))
         .step(key='SKnYfMkIxwEsD', value=self.serial, action='input', desc='批次备注')
         .step(key='AswWtwVTTMMIx', desc='生成帮卖订单')
         .step(key='ybZ3sOSfyPaGL', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(sf_express_delivery_is_easy)
    def sf_express_delivery_is_easy(self):
        self.menu_manage()
        (self.step(key='kInu3eV3j7Fc5', desc='去发货')
         .step(key='D4XT9rSHm6eGW', desc='计算运费')
         .step(key='iOyin5Pq9t6Ri', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(CtZUckEy9Xr7Q9rhDgM9)
    def CtZUckEy9Xr7Q9rhDgM9(self):
        self.menu_manage()
        (self.step(key='wfOk7EdBu1SEp', desc='去发货')
         .step(key='qEWFpy7Qc19Va', desc='自行邮寄')
         .step(key='w59IBOCm0mWIj', value=self.jd, action='input', desc='快递单号')
         .step(key='hGUeaizKrG6cd', value='京东快递', action='input', desc='快递公司')
         .step(key='bLqJg2Qi8tIXp', value=self.phone, action='input', desc='手机号码')
         .step(key='DxA8byKLE69Yg', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(lUGAPOtEUoXAYtTaa2Jb)
    def lUGAPOtEUoXAYtTaa2Jb(self):
        self.menu_manage()
        (self.step(key='I5oL0kjoLDOhm', desc='去发货')
         .step(key='vZYMQUpYAVYrd', desc='自己送')
         .step(key='Xo0qai9UEWhWc', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(qWL5r2tvJ34XBHF8SvNA)
    def qWL5r2tvJ34XBHF8SvNA(self):
        self.menu_manage()
        (self.step(key='ZoVGSdrfG2Fa3', desc='订单列表')
         .step(key='Y6rud4auDIjjX', desc='取消订单')
         .step(key='GgmYH9OXycvLF', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(fBkRLU5PnvGYpBfZdMYx)
    def fBkRLU5PnvGYpBfZdMYx(self):
        self.menu_manage()
        (self.step(key='xqXPWAdTACIos', desc='订单列表')
         .step(key='Vh3La7Wps8o1H', desc='申请退机')
         .step(key='axAHm58CtLjog', desc='确认申请退机')
         .wait())
        return self

    @reset_after_execution
    @doc(xzJ4vjMEgys2mrV0XE7B)
    def xzJ4vjMEgys2mrV0XE7B(self):
        self.menu_manage()
        (self.step(key='OYwlP40la25Gs', desc='订单列表')
         .step(key='H90zANN7qZvzz', desc='手动签收')
         .step(key='GCnl3Rl4istp6', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(KWGxLZFsVSdw6Fh5ZbAA)
    def KWGxLZFsVSdw6Fh5ZbAA(self):
        self.menu_manage()
        (self.step(key='xOkVOWHgQcxpg', desc='订单列表')
         .step(key='yUETQcqDh7WSh', desc='物流签收')
         .step(key='BNbNyZq8xoCpU', desc='搜索')
         .custom(lambda: self.tab_space(6))
         .step(key='YqkhM91NU1ZXR', desc='签收入库')
         .step(key='FK1CyJ2AE1v2x', desc='流转仓库')
         .custom(lambda: self.up_enter())
         .step(key='JrbaWBGI1gv6o', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(fNG49PWF3oUJGnsMAIuf)
    def fNG49PWF3oUJGnsMAIuf(self):
        self.menu_manage()
        (self.step(key='gRkxUlOKXriQL', desc='订单列表')
         .step(key='EIAidGr5BBqQp', desc='确认保卖')
         .step(key='SSky1RaypmKBi', desc='确定')
         .custom(lambda: self.wait_time(5))
         .custom(lambda: self.refresh_page())
         .wait())
        return self

    @reset_after_execution
    @doc(EjR5pz1y2L10GHnV2z4v)
    def EjR5pz1y2L10GHnV2z4v(self):
        self.menu_manage()
        (self.step(key='wODQcZrEqTrdW', desc='订单列表')
         .step(key='WOv2TNiY4yMil', desc='申请议价')
         .step(key='mEbWPVKALAErD', value=self.serial, action='input', desc='申请说明')
         .step(key='wgjBFAlrxEyTi', desc='确定')
         .wait())
        return self


class Q1DeeKQy46a(CommonPages):
    """帮卖管理|帮卖来货列表"""

    def menu_manage(self):
        """菜单"""
        (self.scroll(key='EC0mSdFuRMZXH', desc='帮卖管理')
         .step(key='cUwiTehH4IZ5H', desc='帮卖管理')
         .step(key='SXIm7Ks3enFaC', desc='帮卖来货列表')
         .wait())
        return self

    @reset_after_execution
    @doc(rE4s2MubKTarhv1LX8Ps)
    def rE4s2MubKTarhv1LX8Ps(self):
        self.menu_manage()
        (self.step(key='h8f2WLpasFvYz', desc='物流签收')
         .custom(lambda: self.wait_time())
         .step(key='SWFqtzalyLs02', desc='搜索')
         .custom(lambda: self.tab_space(6))
         .step(key='H3OLRoy68lXRZ', desc='签收入库')
         .step(key='XdaqtHb83IFPJ', desc='流转仓库')
         .custom(lambda: self.up_enter())
         .step(key='MGo5LzOrVUHCl', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(manual_signature)
    def manual_signature(self):
        self.menu_manage()
        (self.step(key='UMNOCBOEXLETZ', desc='手动签收')
         .step(key='cyUxrYFKZ57TT', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(UEgbcBjQGEn3BLntI6lb)
    def UEgbcBjQGEn3BLntI6lb(self):
        self.menu_manage()
        (self.step(key='VbZmXZa2ZI5Ys', desc='订单列表')
         .step(key='MuVMaHbSjZ5Ap', desc='去质检')
         .step(key='Q5VeLX6Es4L43', desc='成色')
         .custom(lambda: self.up_enter())
         .step(key='ng1ELqSDeT7HQ', value='质检备注', action='input', desc='备注')
         .step(key='xZFz957C5Kstt', value=self.number, action='input', desc='预售保卖价')
         .step(key='lNed7hEvyN4or', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(LB9ycxycPTRF4K0JdDw7)
    def LB9ycxycPTRF4K0JdDw7(self):
        self.menu_manage()
        (self.step(key='SxJghFJFphUQy', desc='订单列表')
         .step(key='OsJSAYaM1gdTs', desc='去复检')
         .scroll('guaranteed_price', desc='预售保卖价')
         .step(key='a2pLV6O2G6Mwv', value=self.number, action='input', desc='预售保卖价')
         .step(key='XxzehwmrD2hUV', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(zHbBDAztWlR3wrimNxlj)
    def zHbBDAztWlR3wrimNxlj(self):
        self.menu_manage()
        (self.step(key='Z9yBCY8FUkoJw', desc='订单列表')
         .step(key='DOmhZ4KvFHJYk', desc='审核拒绝')
         .step(key='ruTtOXgAPAreU', value=self.serial, action='input', desc='拒绝原因')
         .step(key='HTDnWK6wkvjD0', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(OKe7y8uCYv26BcVNtvU6)
    def OKe7y8uCYv26BcVNtvU6(self):
        self.menu_manage()
        (self.step(key='PwmrZXDtzGeRS', desc='订单列表')
         .step(key='SowMMg1UhLlBc', desc='去销售')
         .step(key='KkSQoa11Gp4NM', desc='确认跳转')
         .custom(lambda: self.wait_time())
         .step(key='AZw04WazFRpj5', desc='单选')
         .step(key='RuZQRoU7BEHR2', desc='出库')
         .step(key='j9yqtNakQCNIy', desc='销售客户')
         .custom(lambda: self.up_enter())
         .step(key='MYU5cg0ViOTDD', value=self.jd, action='input', desc='物流单号')
         .step(key='ctQhBb45Eh2tG', value=self.number, action='input', desc='物流费用')
         .scroll('sell_sales_order_number', desc='销售金额')
         .step(key='KBJ1Xyvo3auih', value='5', action='input', desc='销售金额')
         .step(key='bGaE3NOkKqlFS', value=self.serial, action='input', desc='平台物品编号')
         .step(key='SuIAIy3C5JNkL', value=self.serial, action='input', desc='平台销售订单号')
         .scroll('the_amount_of_the_payout', desc='收款金额')
         .step(key='oGBiIke2beqqQ', desc='已收款')
         .step(key='MlNvjmNUv1vaZ', desc='收款账户')
         .custom(lambda: self.up_enter())
         .step(key='x0yO9eWODdARZ', value='5', action='input', desc='收款金额')
         .step(key='lwXOdyVl5MAeR', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(yhsanR53oCT3E0y79Pkt)
    def yhsanR53oCT3E0y79Pkt(self):
        self.menu_manage()
        (self.step(key='fJL9lKiFRe0M2', desc='订单列表')
         .step(key='zkrkYhwQmwpLS', desc='手动结算')
         .step(key='H6SEo1AvXhYja', desc='确定')
         .step(key='atu7UYLBkh3Ax', desc='手动结算')
         .step(key='HpUsf9pvNsfJU', desc='确定')
         .custom(lambda: self.wait_time())
         .wait())
        return self

    @reset_after_execution
    @doc(vCZ8TzDFnPROV6Oo072B)
    def vCZ8TzDFnPROV6Oo072B(self):
        self.menu_manage()
        (self.step(key='Upsje1vrLtFdW', desc='订单列表')
         .step(key='kJioWIlOM3Yd5', desc='去退机')
         .scroll('go_to_the_retirement_machine_ok', desc='确定')
         .step(key='BJgGDEMiLHesN', desc='计算运费')
         .custom(lambda: self.wait_time())
         .step(key='gnrQYKIGHtERo', desc='确定')
         .wait())
        return self


class ZXokM9zOq0v(CommonPages):
    """帮卖管理|帮卖业务配置"""

    def menu_manage(self):
        """菜单"""
        (self.scroll(key='TxaOO5Msl4Kyf', desc='帮卖管理')
         .step(key='Rlj8CDIF72jX1', desc='帮卖管理')
         .step(key='r26CO5Iyd2VcV', desc='帮卖业务配置')
         .wait())
        return self

    @reset_after_execution
    @doc(lnEVAUkilhXnv8b0GZtm)
    def lnEVAUkilhXnv8b0GZtm(self):
        self.menu_manage()
        (self.step(key='f8CmzNqvL5Gin', desc='编辑')
         .scroll('selling_days', desc='销售天数')
         .step(key='WSLM803GP0T4F', value='30', action='input', desc='销售天数')
         .step(key='UBUXotAQvPsiF', value='10', action='input', desc='退机回寄天数')
         .step(key='gE5PNImtUQ90O', value='10', action='input', desc='自动结算天数')
         .step(key='aF2kLuRwZD1AR', desc='确认')
         .wait())
        return self
