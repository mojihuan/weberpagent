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
            'financial_settlement': os.path.join(DATA_PATHS['excel'], 'financial_settlement_import.xlsx')
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


class LHNzSM9GeBa(CommonPages):
    """财务管理|资金账户|账户列表"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='YZ4i6gNiS0bpI', desc='财务管理')
         .step(key='bCcvwro4OFKQA', desc='资金账户')
         .step(key='a5hUTueBGb73U', desc='账户列表')
         .wait())
        return self

    @reset_after_execution
    @doc(EPKsvmKzhm7PJO1muKwj)
    def EPKsvmKzhm7PJO1muKwj(self):
        self.menu_manage()
        (self.step(key='DKIl4LJMKjoGU', desc='新建账户')
         .step(key='reeUF5KM0MaiE', desc='账户类型')
         .custom(lambda: self.up_enter())
         .step(key='NGzJZ606xrkSS', value='名称' + self.get_time_stamp(), action='input', desc='账户名称')
         .step(key='lTKYJuCPtZ2Py', value='1', action='input', desc='初始余额')
         .step(key='XDaVOTCO1oJEO', value='备注信息', action='input', desc='备注')
         .step(key='rBNSPbF7XQY9J', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(uFTVSOsNXHqB5vxndsyu)
    def uFTVSOsNXHqB5vxndsyu(self):
        self.menu_manage()
        (self.step(key='nF41sBxM8nLcM', desc='账户间转账')
         .step(key='lXJRQq8LOkoPJ', desc='日期')
         .step(key='Kv2pnpSIbBU7O', desc='确定')
         .step(key='YDtcW1tF4pX4b', value='5', action='input', desc='金额')
         .step(key='LxjkKpY4CXvPY', desc='转出账户')
         .custom(lambda: self.down_enter())
         .step(key='f4AALw7EG2xt4', desc='转入账户')
         .custom(lambda: self.up_enter())
         .step(key='kbIdqJ7EKdSoH', desc='确认')
         .wait())
        return self


class DkcYxrWLdQf(CommonPages):
    """财务管理|业务记账|账单审核"""

    def menu_manage(self):
        """菜单"""
        (self.scroll(key='LgAdgT8lZlsn9', desc='财务管理')
         .step(key='slPFCWvUcupkk', desc='财务管理')
         .step(key='RHPuf5VNrynLU', desc='业务记账')
         .step(key='h59LdAyA98OCF', desc='账单审核')
         .wait())
        return self

    @reset_after_execution
    @doc(B7RHH1KuhjdPrvwiHaID)
    def B7RHH1KuhjdPrvwiHaID(self):
        self.menu_manage()
        (self.step(key='F22R6eTJbUEgI', desc='审核')
         .step(key='r5dB8BIpSwZ6G', value=self.serial, action='input', desc='说明')
         .step(key='Lo3ashf73kA4m', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(owv9tEsxrz0pHaC8wXtH)
    def owv9tEsxrz0pHaC8wXtH(self):
        self.menu_manage()
        (self.step(key='IZpv8RBNIJWbj', desc='审核')
         .step(key='X6H0d5Dduk4J4', desc='未通过')
         .step(key='u7KxSxGNWtbQq', value=self.serial, action='input', desc='说明')
         .step(key='b3JxD7YZvhbte', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(paKbZdNmtzqoFduDoh5X)
    def paKbZdNmtzqoFduDoh5X(self):
        self.menu_manage()
        (self.step(key='VcX3uLPCSQjOQ', desc='搜索')
         .custom(lambda: self.tab_space(2))
         .step(key='y8YgIQ2FF8IpE', desc='批量审核')
         .step(key='A4xpeKic3urSq', desc='付款账户')
         .custom(lambda: self.down_enter())
         .step(key='ma43hGLCfiq5f', value=self.serial, action='input', desc='说明')
         .step(key='rODgVZrRLi7Mc', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(u9n7DKzDxeT1rnv4h3tV)
    def u9n7DKzDxeT1rnv4h3tV(self):
        self.menu_manage()
        (self.step(key='PaQMUWFE5m1IO', desc='应收账单')
         .step(key='SVa5pkTlaTUdP', desc='审核')
         .step(key='dmz4gjxY1Z7CT', value=self.serial, action='input', desc='说明')
         .step(key='wpBZ523b93rvj', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(LDw1ORDeq57nUxfwqx8P)
    def LDw1ORDeq57nUxfwqx8P(self):
        self.menu_manage()
        (self.step(key='J5FImYFJnBqRy', desc='应收账单')
         .step(key='Z4iuPRx6LEm6y', desc='审核')
         .step(key='HYzkqiJGp5ZNy', desc='未通过')
         .step(key='ay4VrZaB4y7mA', value=self.serial, action='input', desc='说明')
         .step(key='m7yFPiyKZNeYr', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(IqFjOayhXYSUJpKpCd2B)
    def IqFjOayhXYSUJpKpCd2B(self):
        self.menu_manage()
        (self.step(key='xpQBgm0mk2dKq', desc='应收账单')
         .step(key='XUzJ7gs0KNzAR', desc='搜索')
         .custom(lambda: self.tab_space(2))
         .step(key='CsTBsh7AKwYbl', desc='批量审核')
         .step(key='nItvptjkWChm8', desc='收款账户')
         .custom(lambda: self.down_enter())
         .step(key='zfqlFuRnOUGTH', value=self.serial, action='input', desc='说明')
         .step(key='OOCMa6g7man0m', desc='确定')
         .wait())
        return self


class YXRRMrHGZDD(CommonPages):
    """财务管理|业务记账|往来应付"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='vaSPF7HnAyGeK', desc='财务管理')
         .step(key='my64aYMp2zzCN', desc='业务记账')
         .step(key='adfgJLIGKPY5X', desc='往来应付')
         .wait())
        return self

    @reset_after_execution
    @doc(rN6o1ZUYdtDbm4jrcy5R)
    def rN6o1ZUYdtDbm4jrcy5R(self):
        self.menu_manage()
        (self.step(key='n038yZ2RdOtCT', desc='供应商')
         .step(key='QyzoGaD21b8R5', value=INFO['main_supplier_name'], action='input', desc='供应商')
         .custom(lambda: self.up_enter())
         .step(key='EG46uCQafYgIU', desc='搜索')
         .step(key='ApilQbCRcfHZa', desc='对账')
         .step(key='WrSsyxegbYL9z', desc='按供应商结算')
         .step(key='yVBSM3LVhhCTv', desc='付款时间')
         .step(key='BleVLACtr2Bqs', desc='确定')
         .step(key='AIB5bsFCZB0af', value=self.serial, action='input', desc='备注')
         .step(key='JeePOZHWTpOFh', desc='付款账户')
         .custom(lambda: self.up_enter())
         .step(key='T5ptN66YuS3OG', value='5', action='input', desc='结算金额')
         .step(key='n25BJIvSHZtkO', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(Xl1WGAaWEyokRuH78976)
    def Xl1WGAaWEyokRuH78976(self):
        self.menu_manage()
        self.file.get_inventory_data('financial_settlement', 'imei', i=2, j=3)
        (self.step(key='wXro1Gg950zAP', desc='供应商')
         .step(key='i20nSAup6IjQh', value=INFO['main_supplier_name'], action='input', desc='供应商')
         .custom(lambda: self.up_enter())
         .step(key='qK2m92gbef6eP', desc='搜索')
         .step(key='T2ZwG8gkxpZ80', desc='对账')
         .custom(lambda: self.wait_time(2))
         .step(key='MvjhzF7h722XU', desc='按机器批量结算')
         .custom(lambda: self.wait_time(3))
         .step(key='u39v2T1Lp233b', desc='导入机器')
         .step(key='HZ6kvbcfJL3uu', value=self.file_path('financial_settlement'), action='upload', desc='上传文件')
         .step(key='sN6sbhX84xYCI', desc='确定')
         .step(key='Pnsk5qcBjkOK5', desc='付款账户')
         .custom(lambda: self.up_enter())
         .scroll('machine_settlement_amount', desc='结算金额')
         .step(key='QwYss7RU1UefN', value='3', action='input', desc='结算金额')
         .step(key='F7W41i3wM7Iru', desc='提交结算')
         .wait())
        return self


class SZKNMopiXGS(CommonPages):
    """财务管理|成本收入调整"""

    def menu_manage(self):
        """菜单"""
        (self.scroll(key='PM86qNNUz7zjV', desc='财务管理')
         .step(key='bil2F3amUrYik', desc='财务管理')
         .step(key='rKo7KPfhBHiXc', desc='成本收入调整')
         .wait())
        return self

    @reset_after_execution
    @doc(UuPR3hG2S8ND6eRZD6CU)
    def UuPR3hG2S8ND6eRZD6CU(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2)[0]['articlesNo'])
        (self.step(key='WRMEriSlAruqZ', desc='新增调整单')
         .step(key='TCD3kXiG8Zxup', desc='物品输入框')
         .custom(lambda: self.ctrl_v())
         .step(key='W8WJKSKGlyAaK', desc='添加')
         .custom(lambda: self.wait_time())
         .step(key='PO49LyycvyEPO', value='14', action='input', desc='新采购金额')
         .step(key='KqmLLSRSHGZ3B', desc='确认')
         .step(key='jWXuSzYZxlwdI', desc='付款账户')
         .custom(lambda: self.up_enter())
         .step(key='rL5LpsFhvHLAZ', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(gwIYPyXMTCz3LKcov2in)
    def gwIYPyXMTCz3LKcov2in(self):
        self.menu_manage()
        self.copy(self.pc.MOyeqlzcgLqhqdWBrkyYg()[0]['billNo'])
        (self.step(key='zZp3ZDyZCzYrX', desc='新增调整单')
         .step(key='KqrLyhTRRVSkf', desc='其他成本')
         .step(key='uuYko8s8PFbsE', desc='调整原因')
         .custom(lambda: self.down_enter())
         .step(key='W3rNocDYNESrW', desc='按单据添加物品')
         .step(key='G0pdeAEcoQV3u', desc='单据号输入框')
         .custom(lambda: self.ctrl_v())
         .step(key='qCDgNBmitq1gU', desc='搜索')
         .step(key='v2NakgiMqXxs1', desc='确认选择')
         .scroll('new_purchase_amount', desc='调整后金额')
         .step(key='jbIfSpSQke4c1', value='16', action='input', desc='调整后金额')
         .step(key='BfRWZonnY9ZnU', desc='确认')
         .step(key='h1W0YO5kYK0QV', desc='付款账户')
         .custom(lambda: self.up_enter())
         .step(key='mrotRW6kMARXb', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(ZOu34dViPFdE8YXvix3K)
    def ZOu34dViPFdE8YXvix3K(self):
        self.menu_manage()
        self.copy(self.pc.UYV6mZaVwDk4HHhyuWRRp(i=3, j=9)[0]['imei'])
        (self.step(key='C3toHed54sZOX', desc='新增调整单')
         .step(key='QteXc5satuvn2', desc='收入调整')
         .step(key='MVMe7E5KfCCXE', desc='物品输入框')
         .custom(lambda: self.ctrl_v())
         .step(key='KZ4ey2yVCOcYk', desc='添加')
         .scroll('amount_of_sales', desc='最新销售金额')
         .step(key='f5j2rSxx10OPh', value='18', action='input', desc='最新销售金额')
         .step(key='O106DJajHivB2', desc='确认')
         .step(key='aQhC3dUGXD0q6', desc='收款账户')
         .custom(lambda: self.up_enter())
         .step(key='L4SzST6KGMZWk', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(bYHTOqsimobeeyyy4NMk)
    def bYHTOqsimobeeyyy4NMk(self):
        self.menu_manage()
        self.copy(self.pc.A9mwkPeNc1x7YnLCF9jUk()[0]['billNo'])
        (self.step(key='yQJ85qp6DstAg', desc='新增调整单')
         .step(key='nV7aEZyQXdLhg', desc='收入调整')
         .step(key='sYGQbDXLQN4UA', desc='其他收入')
         .step(key='wDk92Ixx1HVnf', desc='调整原因')
         .custom(lambda: self.down_enter())
         .step(key='zBglVoMMEHYa2', desc='按单据添加物品')
         .step(key='jmGew6dDmI58N', desc='单据号输入框')
         .custom(lambda: self.ctrl_v())
         .step(key='xrXKOqmzTRfBp', desc='搜索')
         .step(key='yUrdZdYtKGJUZ', desc='确认选择')
         .scroll('amount_of_sales', desc='调整后金额')
         .custom(lambda: self.wait_time())
         .step(key='VSCzCIpk7YyvM', value='7', action='input', desc='调整后金额')
         .step(key='bJwDJgYLUmyeL', desc='确认')
         .step(key='nwLI3ToYUeUnG', desc='收款账户')
         .custom(lambda: self.up_enter())
         .step(key='GuYWovaTRvYxa', desc='确定')
         .wait())
        return self


class BEEPcrtPqRI(CommonPages):
    """财务管理|业务记账|日常支出"""

    def menu_manage(self):
        """菜单"""
        (self.scroll(key='yAbAfqKf5MTxw', desc='财务管理')
         .step(key='a9ezc9AsjHW9T', desc='财务管理')
         .step(key='WfM5aYfpvluGp', desc='业务记账')
         .step(key='OV7wWNLl3shiT', desc='日常支出')
         .wait())
        return self

    @reset_after_execution
    @doc(FayuY8TiAhpMWGjKj1UK)
    def FayuY8TiAhpMWGjKj1UK(self):
        self.menu_manage()
        (self.step(key='SD7aFtfYOjlGy', desc='新增支出项')
         .step(key='zAlxrsmeRj37V', desc='支出类型')
         .custom(lambda: self.down_enter())
         .step(key='EtKwtodhYaYZm', value='234', action='input', desc='支出价格')
         .step(key='dvxg4wXL6bBJ4', desc='支出账户')
         .custom(lambda: self.down_enter())
         .step(key='UoZblQ2ZDViGB', desc='经办人')
         .custom(lambda: self.down_enter())
         .step(key='RRR0FciSau5ni', value=self.serial, action='input', desc='备注')
         .step(key='nVje42b31oV7G', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(DXjNXH9tYTDU3RC6mwgg)
    def DXjNXH9tYTDU3RC6mwgg(self):
        self.menu_manage()
        (self.step(key='oMFD6sDhGjsew', desc='新增支出项')
         .step(key='Kadq2NJ4vW6fr', desc='新增类型')
         .step(key='YuKLpPSNi7iig', desc='交易类型')
         .custom(lambda: self.down_enter(2))
         .step(key='OLCu4Y40StWAW', value='充话费' + self.serial, action='input', desc='日常费用类型')
         .step(key='y6EdMLcFvnLOF', desc='用途类型')
         .custom(lambda: self.down_enter())
         .step(key='DQxOTexJNnWDQ', desc='确定')
         .step(key='vZdnSCvRqRbCj', desc='支出类型')
         .custom(lambda: self.down_enter())
         .step(key='bX0NHBh0qjFM7', value='100', action='input', desc='支出价格')
         .step(key='ts8X83PF16d9V', desc='支出账户')
         .custom(lambda: self.down_enter())
         .step(key='gl0gP4SAkFIlT', desc='经办人')
         .custom(lambda: self.down_enter())
         .step(key='UyOsMgYgrurxv', value=self.serial, action='input', desc='备注')
         .step(key='oOyugdxKEzccG', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(fHKdXgxjrhTynQXVkJCy)
    def fHKdXgxjrhTynQXVkJCy(self):
        self.menu_manage()
        (self.step(key='GMhGd0MpEFCeF', desc='新增支出项')
         .step(key='Tc7ucfjyaUy4f', desc='新增类型')
         .step(key='sIDRX3KkvO72e', desc='交易类型')
         .custom(lambda: self.down_enter(2))
         .step(key='btlGXgvBquIfA', value='充话费' + self.serial, action='input', desc='日常费用类型')
         .step(key='RoirztxnzCuEA', desc='用途类型')
         .custom(lambda: self.down_enter(2))
         .step(key='I3jqJ5hpRyINh', desc='确定')
         .step(key='xNA0sdqQujqBM', desc='支出类型')
         .custom(lambda: self.down_enter())
         .step(key='O3N0o51nqq9Ki', value='125', action='input', desc='支出价格')
         .step(key='s3u28ml19KOTr', desc='支出账户')
         .custom(lambda: self.down_enter())
         .step(key='hPE31OlCpqy2X', desc='经办人')
         .custom(lambda: self.down_enter())
         .step(key='HseMSgoAe9vYQ', value=self.serial, action='input', desc='备注')
         .step(key='a3Ef9vK2Etk0h', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(cspHMPPcFNfVjtAbiAw4)
    def cspHMPPcFNfVjtAbiAw4(self):
        self.menu_manage()
        (self.step(key='kGqKLLuHHOUpj', desc='导出全部')
         .wait())
        return self


class WeMmSQ9tWMa(CommonPages):
    """财务管理|业务记账|日常收入"""

    def menu_manage(self):
        """菜单"""
        (self.scroll(key='BrEydfDzGG1kW', desc='财务管理')
         .step(key='Lc4RpAjhLKl8F', desc='财务管理')
         .step(key='BeYvfa4Jc1RmY', desc='业务记账')
         .step(key='hcWwuJbUoI1HQ', desc='日常收入')
         .wait())
        return self

    @reset_after_execution
    @doc(HGwxHVDLmqfBnulaegiO)
    def HGwxHVDLmqfBnulaegiO(self):
        self.menu_manage()
        (self.step(key='yVy6rSAUO4EMO', desc='新增收入项')
         .step(key='PtJF4lrT4xbxD', desc='收入类型')
         .custom(lambda: self.down_enter())
         .step(key='sDnhTytCTYYPp', value='21', action='input', desc='收入价格')
         .step(key='vSzXTurUyNopQ', desc='收入账户')
         .custom(lambda: self.down_enter())
         .step(key='HpciNhHbtVQJd', desc='经办人')
         .custom(lambda: self.down_enter())
         .step(key='MYe5j30cQnQ9J', value='新增收入项备注', action='input', desc='备注')
         .step(key='Qqconp5VucQI7', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(aNr3DKkkiWeOO8RYAnfd)
    def aNr3DKkkiWeOO8RYAnfd(self):
        self.menu_manage()
        (self.step(key='d8Pqi7895rmxP', desc='新增收入项')
         .step(key='NMiHBEfRP6u4k', desc='新增类型')
         .step(key='odKBEuGjlc8gN', desc='交易类型')
         .custom(lambda: self.down_enter(2))
         .step(key='hJbZVtaUFy6qy', value='充话费' + self.serial, action='input', desc='日常费用类型')
         .step(key='GcOCYWIqIr4fu', desc='用途类型')
         .custom(lambda: self.down_enter())
         .step(key='oxtytrf7zKeSo', desc='确定')
         .custom(lambda: self.wait_time())
         .step(key='HlQHIKNpIevbU', desc='收入类型')
         .custom(lambda: self.down_enter())
         .step(key='j9DtnTsQIqqqn', value='100', action='input', desc='收入价格')
         .step(key='wWB8ZJm0kcrKI', desc='收入账户')
         .custom(lambda: self.down_enter())
         .step(key='PWLXlkZ9Iwd5P', desc='经办人')
         .custom(lambda: self.down_enter())
         .step(key='pYbOaK4MXwdEJ', value=self.serial, action='input', desc='备注')
         .step(key='SFMcRW4A0Nmo8', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(gEJaRtUQ1U9s1GJx0FCI)
    def gEJaRtUQ1U9s1GJx0FCI(self):
        self.menu_manage()
        (self.step(key='OMFJw4rd1XeQ5', desc='新增收入项')
         .step(key='PUs3UKSahri13', desc='新增类型')
         .step(key='VLnYs5paXCjkZ', desc='交易类型')
         .custom(lambda: self.down_enter(2))
         .step(key='SVLzaGqwrDQQN', value='充话费' + self.serial, action='input', desc='日常费用类型')
         .step(key='DT2t5rOzEsI6z', desc='用途类型')
         .custom(lambda: self.down_enter())
         .step(key='YJQVMsBptL73x', desc='确定')
         .custom(lambda: self.wait_time())
         .step(key='wiZo2P4dJD16D', desc='收入类型')
         .custom(lambda: self.down_enter())
         .step(key='X8TKcYN4WbMNJ', value='100', action='input', desc='收入价格')
         .step(key='M27Dvh9mrCiW3', desc='收入账户')
         .custom(lambda: self.down_enter())
         .step(key='erV75RJTq5Aeq', desc='经办人')
         .custom(lambda: self.down_enter())
         .step(key='uqO7ykYSvEiOW', value=self.serial, action='input', desc='备注')
         .step(key='tBFMytggTAzAP', desc='确定')
         .wait())
        return self


class Ig69JnPs8iR(CommonPages):
    """财务管理|业务记账|往来应收"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='nqLnoat6PnBv3', desc='财务管理')
         .step(key='jlTsHV1xRdvBk', desc='业务记账')
         .step(key='rdBXxYS4gpJh0', desc='往来应收')
         .wait())
        return self

    @reset_after_execution
    @doc(ZJ7XVXb9AG0TE9iIa6N4)
    def ZJ7XVXb9AG0TE9iIa6N4(self):
        self.menu_manage()
        (self.step(key='yl4MvnlLhCV2F', desc='客户')
         .step(key='H3Ep1tYzloshL', value=INFO['vice_sales_customer_name'], action='input', desc='客户')
         .custom(lambda: self.up_enter())
         .step(key='fWfZz9JAETolv', desc='搜索')
         .step(key='d4XJn8eQNKY3n', desc='对账')
         .custom(lambda: self.wait_time())
         .step(key='cD59o82AVXxvA', desc='按客户结算')
         .step(key='VkwoTQgCy6JDB', desc='收款时间')
         .step(key='BcXApMYunIfDN', desc='确定')
         .step(key='Pj5yHpaWioux4', desc='收款账户')
         .custom(lambda: self.up_enter())
         .step(key='dw4ShJQ7jWHIM', value='8', action='input', desc='结算金额')
         .step(key='WhcYX9CKZBWJ6', value=self.serial, action='input', desc='备注')
         .step(key='yLMhTl9KhV1Z1', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(tRKpIUzOlA6X5zEFrDDX)
    def tRKpIUzOlA6X5zEFrDDX(self):
        self.menu_manage()
        self.file.get_inventory_data('financial_settlement', 'imei', i=3, j=9)
        (self.step(key='GP04HTkpIcq9K', desc='客户')
         .step(key='nNJ1jVZivBVPl', value=INFO['vice_sales_customer_name'], action='input', desc='客户')
         .custom(lambda: self.up_enter())
         .step(key='vP2UY08gm9atG', desc='搜索')
         .step(key='M6HIn9b0HT3nU', desc='对账')
         .custom(lambda: self.wait_time())
         .step(key='ZfKSpZXtpDvkH', desc='按机器批量结算')
         .step(key='n9JvVjIHZLfTQ', desc='导入机器')
         .step(key='GnuwtKkcszG4H', value=self.file_path('financial_settlement'), action='upload', desc='上传文件')
         .step(key='mNFWrRvwRPuXo', desc='确定')
         .step(key='rJXVjQh6ZW4aa', desc='收款账户')
         .custom(lambda: self.up_enter())
         .scroll('machine_settlement_input_amount', desc='结算金额')
         .step(key='cLRRRw2ca1t3r', value='11', action='input', desc='结算金额')
         .step(key='be3sCEhBEFve7', desc='提交结算')
         .wait())
        return self

    @reset_after_execution
    @doc(fT6q4WKrfaMumo1hu8bh)
    def fT6q4WKrfaMumo1hu8bh(self):
        self.menu_manage()
        (self.step(key='qxinTc7Ddq7AF', desc='客户')
         .step(key='yh4DcAuxiu2Ea', value=INFO['vice_sales_customer_name'], action='input', desc='客户')
         .custom(lambda: self.up_enter())
         .step(key='zBWB2bZnVOXfl', desc='搜索')
         .step(key='W5zXPHujrawOw', desc='对账')
         .custom(lambda: self.wait_time())
         .step(key='wpL6BTOB29WJb', desc='搜索')
         .custom(lambda: self.tab_space(7))
         .step(key='OqBqblhGQqQJm', desc='按订单批量结算')
         .step(key='wLdtuRNF10ztJ', desc='收款账号')
         .custom(lambda: self.down_enter())
         .step(key='WSCtRs3wx3uUs', value='2', action='input', desc='结算金额')
         .step(key='typoGmvSml5CN', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(iKi1BJo4BkgRrnQw07D5)
    def iKi1BJo4BkgRrnQw07D5(self):
        self.menu_manage()
        (self.step(key='MgRZ4VHfHI4nI', desc='客户')
         .step(key='cvCpsYVhDQLAR', value=INFO['vice_sales_customer_name'], action='input', desc='客户')
         .custom(lambda: self.up_enter())
         .step(key='gBsTR5RvjsI9C', desc='搜索')
         .step(key='H1XCfxylqZuOk', desc='对账')
         .custom(lambda: self.wait_time())
         .step(key='p0CNA5z7qwK7z', desc='结算')
         .step(key='CQmrUoZGsVOKq', desc='收款账号')
         .custom(lambda: self.down_enter())
         .step(key='LB75ZlZehA3di', value='99999', action='input', desc='结算金额')
         .step(key='SHsMuoQ9Hb1Gt', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(tfxkaybmapLMuR1pFqjY)
    def tfxkaybmapLMuR1pFqjY(self):
        self.menu_manage()
        (self.step(key='pS1rYm2Dq4rbe', desc='客户')
         .step(key='vkvQeCXYVR9R2', value=INFO['vice_sales_customer_name'], action='input', desc='客户')
         .custom(lambda: self.up_enter())
         .step(key='OtpfasXEmh1MF', desc='搜索')
         .step(key='HUDkCgozgO9OT', desc='对账')
         .step(key='dcY8F8wmYQNBd', desc='导出')
         .wait())
        return self


class S8e0gGr58Sx(CommonPages):
    """财务管理|业务记账|预付预收"""

    def menu_manage(self):
        """菜单"""
        (self.scroll(key='h3twKVtv6BdSj', desc='财务管理')
         .step(key='LWE26LpdC1CqH', desc='财务管理')
         .step(key='DlLtNGzC6oYTp', desc='业务记账')
         .step(key='e96qnUmk6j4nq', desc='预付/预收')
         .wait())
        return self

    @reset_after_execution
    @doc(f9xh8uqQHD61p0h46zFQ)
    def f9xh8uqQHD61p0h46zFQ(self):
        self.menu_manage()
        (self.step(key='PX9dsPWOAa0WC', desc='预付款tab')
         .step(key='bVRAZnKzePFwO', desc='新增预付款')
         .step(key='Qtnl9ZSXIxDjh', desc='供应商')
         .custom(lambda: self.down_enter())
         .step(key='NuFGzdx2iM7hI', value=16, action='input', desc='金额')
         .step(key='l6v89DEqh15gA', desc='预付账户')
         .custom(lambda: self.down_enter())
         .step(key='r2Ajmb8PPvJoo', value=self.date_time, action='input', desc='日期')
         .custom(lambda: self.enter())
         .step(key='SG0qSJ3OChbcZ', desc='经办人')
         .custom(lambda: self.down_enter())
         .step(key='DDMwAKsf3KHau', value=self.serial, action='input', desc='备注')
         .step(key='lTAPBRkD3UfP5', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(yCZnY4hUPXHhgriGFZFe)
    def yCZnY4hUPXHhgriGFZFe(self):
        self.menu_manage()
        (self.step(key='h65moCifshaAU', desc='预付款tab')
         .step(key='J4WUumcpx2iSt', desc='导出')
         .wait())
        return self

    @reset_after_execution
    @doc(DsovuKeVyEqIjHwsYRo0)
    def DsovuKeVyEqIjHwsYRo0(self):
        self.menu_manage()
        (self.step(key='VifWd9P70pR9i', desc='预收款tab')
         .step(key='mKx0d7qZ7mUMM', desc='新增预收款')
         .step(key='j6lFrJfPhcMqP', desc='供应商')
         .custom(lambda: self.down_enter())
         .step(key='It0J1zJRwsvWb', value=13, action='input', desc='金额')
         .step(key='F1qFvkrVfcK0l', desc='预收账户')
         .custom(lambda: self.down_enter())
         .step(key='uHMAaw9Nd3DvR', value=self.date_time, action='input', desc='日期')
         .custom(lambda: self.enter())
         .step(key='Yq8sNXdkYmoPu', desc='经办人')
         .custom(lambda: self.down_enter())
         .step(key='Ho8pZnrfF8vyr', value=self.serial, action='input', desc='备注')
         .step(key='Ja7QXgxdUzwmD', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(yCZnY4hUPXHhgriGFZFe)
    def yCZnY4hUPXHhgriGFZFe(self):
        self.menu_manage()
        (self.step(key='lGb5IVZpk4SyZ', desc='预收tab')
         .step(key='pCMPaL16IKRc1', desc='导出')
         .wait())
        return self
