# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.import_case import *


class TestLbCjZYZR(BaseCase, unittest.TestCase):
    """财务管理|资金账户|账户列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return finance_r.WnS8MVqkMl()
        else:
            return finance_p.LHNzSM9GeBa(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_EPKsvmKzhm7PJO1muKwj(self):
        """[新建账户]其他-默认初始余额"""
        case = self.common_operations(login='idle')
        case.EPKsvmKzhm7PJO1muKwj()

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_JWqdZElvJgNFFHaXqZRT(self):
        """[修改]修改账户类型为微信-充值"""
        case = self.common_operations()
        case.JWqdZElvJgNFFHaXqZRT()

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_uFTVSOsNXHqB5vxndsyu(self):
        """[账户间转账]互相转账"""
        case = self.common_operations()
        case.uFTVSOsNXHqB5vxndsyu()


class TestLMyYcX5f(BaseCase, unittest.TestCase):
    """财务管理|业务记账|账单审核"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return finance_r.DISZcB8ZYA()
        else:
            return finance_p.DkcYxrWLdQf(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0B7RHH1KuhjdPrvwiHaID(self):
        """[应付账单]审核-审核通过"""
        self.pre.operations(data=['CFo3'])
        case = self.common_operations(login='main')
        case.B7RHH1KuhjdPrvwiHaID()
        res = [lambda: self.pc.rfhFfE(i=1, type=1, auditStatus=1, billTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_owv9tEsxrz0pHaC8wXtH(self):
        """[应付账单]审核-审核拒绝"""
        self.pre.operations(data=['CFo3'])
        case = self.common_operations()
        case.owv9tEsxrz0pHaC8wXtH()
        res = [lambda: self.pc.rfhFfE(i=1, type=1, auditStatus=2, billTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_paKbZdNmtzqoFduDoh5X(self):
        """[应付账单]批量审核-审核通过"""
        self.pre.operations(data=['CFo3'])
        case = self.common_operations()
        case.paKbZdNmtzqoFduDoh5X()
        res = [lambda: self.pc.rfhFfE(i=1, type=1, auditStatus=1, billTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_u9n7DKzDxeT1rnv4h3tV(self):
        """[应收账单]审核-审核通过"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'boSK'])
        case = self.common_operations()
        case.u9n7DKzDxeT1rnv4h3tV()
        res = [lambda: self.pc.rfhFfE(i=2, type=2, auditStatus=1, billTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_LDw1ORDeq57nUxfwqx8P(self):
        """[应收账单]审核-审核拒绝"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'boSK'])
        case = self.common_operations()
        case.LDw1ORDeq57nUxfwqx8P()
        res = [lambda: self.pc.rfhFfE(i=2, type=2, auditStatus=2, billTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_IqFjOayhXYSUJpKpCd2B(self):
        """[应收账单]批量审核-审核通过"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'boSK'])
        case = self.common_operations()
        case.IqFjOayhXYSUJpKpCd2B()
        res = [lambda: self.pc.rfhFfE(i=2, type=2, auditStatus=1, billTime='now')]
        self.assert_all(*res)


class TestcHazPE1n(BaseCase, unittest.TestCase):
    """财务管理|业务记账|账单审核"""

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_0BwTCKfib2nxArwfojqzu(self):
        """[应收账单]批量审核-帮卖订单-审核通过"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'AWj7', 'ZA5N', 'WZaL', 'Sh3x', 'vhyj'])
        case = self.common_operations(login='vice')
        case.BwTCKfib2nxArwfojqzu()
        res = [lambda: self.pc.rfhFfE(headers='vice', i=2, type=2, auditStatus=1, billTime='now')]
        self.assert_all(*res)


@unittest.skip("暂时跳过整个类的执行")
class TestTEou8YiL(BaseCase, unittest.TestCase):
    """财务管理|业务记账|往来应付"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return finance_r.AgnH0XzSB2()
        else:
            return finance_p.YXRRMrHGZDD(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0rN6o1ZUYdtDbm4jrcy5R(self):
        """[按供应商结算]部分金额结算"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations(login='main')
        case.rN6o1ZUYdtDbm4jrcy5R()
        res = [lambda: self.pc.GaYl3w(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_Hxs7NXz0FKtXSPkjcof8(self):
        """[按机器批量结算]部分金额结算"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.Hxs7NXz0FKtXSPkjcof8()
        res = [lambda: self.pc.GaYl3w(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_Xl1WGAaWEyokRuH78976(self):
        """[按机器批量结算]导入物品-部分金额结算"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.Xl1WGAaWEyokRuH78976()
        res = [lambda: self.pc.GaYl3w(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_EREYtlx2HerCU1zbpObk(self):
        """[按订单批量结算]全部金额结算"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.EREYtlx2HerCU1zbpObk()
        res = [lambda: self.pc.GaYl3w(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_D97tgtc9GTXE0vdXK6lA(self):
        """[按供应商结算]全部金额结算"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.D97tgtc9GTXE0vdXK6lA()
        res = [lambda: self.pc.GaYl3w(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_hciCQ89oHrPs7V8gpK2s(self):
        """[按供应商结算]部分金额结算-预付款抵扣全部金额"""
        self.pre.operations(data=['ekBx', 'OBvm'])
        case = self.common_operations()
        case.hciCQ89oHrPs7V8gpK2s()
        res = [lambda: self.pc.GaYl3w(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_euOyfYcWF0WoC0gVogWr(self):
        """[按供应商结算]部分金额结算-预付款抵扣部分金额"""
        self.pre.operations(data=['ekBx', 'OBvm'])
        case = self.common_operations()
        case.euOyfYcWF0WoC0gVogWr()
        res = [lambda: self.pc.GaYl3w(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_gSSx2ogkswH5sLVoUa56(self):
        """[按订单批量结算]部分金额结算"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.gSSx2ogkswH5sLVoUa56()
        res = [lambda: self.pc.GaYl3w(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_tNULVYUnORNWpB5La3kh(self):
        """[按订单批量结算]全部金额结算-预付款抵扣部分金额"""
        self.pre.operations(data=['ekBx', 'OBvm'])
        case = self.common_operations()
        case.tNULVYUnORNWpB5La3kh()
        res = [lambda: self.pc.GaYl3w(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_VdFBXs16N2ZEhp4PqlbM(self):
        """[按订单批量结算]全部金额结算-预付款抵扣全部金额"""
        self.pre.operations(data=['ekBx', 'OBvm'])
        case = self.common_operations()
        case.VdFBXs16N2ZEhp4PqlbM()
        res = [lambda: self.pc.GaYl3w(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_N5qtlbV2nKad4orzWHDh(self):
        """[按机器批量结算]-全部金额结算"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.N5qtlbV2nKad4orzWHDh()
        res = [lambda: self.pc.GaYl3w(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_SM3tdEQRoyKAUKE6Kjhu(self):
        """[按机器批量结算]-部分金额结算-预付款抵扣部分金额"""
        self.pre.operations(data=['ekBx', 'OBvm'])
        case = self.common_operations()
        case.SM3tdEQRoyKAUKE6Kjhu()
        res = [lambda: self.pc.GaYl3w(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_t9oHAeUXlbi3VyJNnJD4(self):
        """[按机器批量结算]-全部金额结算-预付款抵扣全部金额"""
        self.pre.operations(data=['ekBx', 'OBvm'])
        case = self.common_operations()
        case.t9oHAeUXlbi3VyJNnJD4()
        res = [lambda: self.pc.GaYl3w(receiptTime='now')]
        self.assert_all(*res)


class TestIWZl8Ewd(BaseCase, unittest.TestCase):
    """财务管理|成本收入调整"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return finance_r.QR58hbFLmz()
        else:
            return finance_p.SZKNMopiXGS(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0UuPR3hG2S8ND6eRZD6CU(self):
        """[新增调整单]添加物品-成本调整-采购金额调整"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations(login='main')
        case.UuPR3hG2S8ND6eRZD6CU()
        res = [lambda: self.pc.zliHLE(adjustmentNum=1, adjustmentTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_L2MWh5RuYAnG54UuqEDd(self):
        """[新增调整单]添加物品-成本调整-其他成本调整"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.L2MWh5RuYAnG54UuqEDd()
        res = [lambda: self.pc.zliHLE(adjustmentNum=1, adjustmentTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_gwIYPyXMTCz3LKcov2in(self):
        """[新增调整单]成本调整-其他成本调整-按单据添加物品"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.gwIYPyXMTCz3LKcov2in()
        res = [lambda: self.pc.zliHLE(adjustmentNum=1, adjustmentTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_ZOu34dViPFdE8YXvix3K(self):
        """[新增调整单]添加物品-收入调整-销售金额调整"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        case = self.common_operations()
        case.ZOu34dViPFdE8YXvix3K()
        res = [lambda: self.pc.zliHLE(adjustmentNum=1, adjustmentTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_JsHXjaPThXs1bk0gJW6L(self):
        """[新增调整单]添加物品-收入调整-其他收入调整"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        case = self.common_operations()
        case.JsHXjaPThXs1bk0gJW6L()
        res = [lambda: self.pc.zliHLE(adjustmentNum=1, adjustmentTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_bYHTOqsimobeeyyy4NMk(self):
        """[新增调整单]收入调整-其他收入调整-按单据添加物品"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        case = self.common_operations()
        case.bYHTOqsimobeeyyy4NMk()
        res = [lambda: self.pc.zliHLE(adjustmentNum=1, adjustmentTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_I7JXB9egcS81B9M2KvPn(self):
        """[新增调整单]添加物品-收入调整-其他收入调整"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        case = self.common_operations()
        case.I7JXB9egcS81B9M2KvPn()
        res = [lambda: self.pc.zliHLE(adjustmentNum=2, adjustmentTime='now')]
        self.assert_all(*res)


class TestkcyBZG2E(BaseCase, unittest.TestCase):
    """财务管理|业务记账|日常支出"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return finance_r.HZwCxB8wAq()
        else:
            return finance_p.BEEPcrtPqRI(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0FayuY8TiAhpMWGjKj1UK(self):
        """[新增支出项]默认支出类型-金额正数"""
        case = self.common_operations(login='main')
        case.FayuY8TiAhpMWGjKj1UK()
        res = [lambda: self.pc.JedUWt(createTime='now', receiptNo='OT')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_voyc86f85IklIULStMSB(self):
        """[新增支出项]默认支出类型-金额负数"""
        case = self.common_operations()
        case.voyc86f85IklIULStMSB()
        res = [lambda: self.pc.JedUWt(createTime='now', receiptNo='OT')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_DXjNXH9tYTDU3RC6mwgg(self):
        """[新增支出项]新增支出日常单"""
        case = self.common_operations()
        case.DXjNXH9tYTDU3RC6mwgg()
        res = [lambda: self.pc.JedUWt(createTime='now', receiptNo='OT')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_fHKdXgxjrhTynQXVkJCy(self):
        """[新增支出项]新增支出调整单"""
        case = self.common_operations()
        case.fHKdXgxjrhTynQXVkJCy()
        res = [lambda: self.pc.JedUWt(createTime='now', receiptNo='OT')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_cspHMPPcFNfVjtAbiAw4(self):
        """[导出全部]"""
        case = self.common_operations()
        case.cspHMPPcFNfVjtAbiAw4()
        res = [lambda: self.pc.T241Se(state=2, createTime='now', name='日常费用单据信息导出')]
        self.assert_all(*res)


class TestzF9VmU14(BaseCase, unittest.TestCase):
    """财务管理|业务记账|日常收入"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return finance_r.WK90Io3VHs()
        else:
            return finance_p.WeMmSQ9tWMa(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0HGwxHVDLmqfBnulaegiO(self):
        """[新增收入项]-默认收入类型-金额正数"""
        case = self.common_operations(login='main')
        case.HGwxHVDLmqfBnulaegiO()
        res = [lambda: self.pc.nRHG7d(createTime='now', receiptNo='IN')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_ZB0P0AxSNEJ3bgjge7xl(self):
        """[新增支出项]默认收入类型-金额负数"""
        case = self.common_operations()
        case.ZB0P0AxSNEJ3bgjge7xl()
        res = [lambda: self.pc.nRHG7d(createTime='now', receiptNo='IN')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_aNr3DKkkiWeOO8RYAnfd(self):
        """[新增支出项]新增收入日常单"""
        case = self.common_operations()
        case.aNr3DKkkiWeOO8RYAnfd()
        res = [lambda: self.pc.nRHG7d(createTime='now', receiptNo='IN')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_gEJaRtUQ1U9s1GJx0FCI(self):
        """[新增支出项]新增收入调整单"""
        case = self.common_operations()
        case.gEJaRtUQ1U9s1GJx0FCI()
        res = [lambda: self.pc.nRHG7d(createTime='now', receiptNo='IN')]
        self.assert_all(*res)


@unittest.skip("暂时跳过整个类的执行")
class TestZ4F6vdGC(BaseCase, unittest.TestCase):
    """财务管理|业务记账|往来应收"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return finance_r.ERK6sz547k()
        else:
            return finance_p.Ig69JnPs8iR(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0ZJ7XVXb9AG0TE9iIa6N4(self):
        """[按客户结算]部分金额结算"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        case = self.common_operations(login='main')
        case.ZJ7XVXb9AG0TE9iIa6N4()
        res = [lambda: self.pc.CsnLYF(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_DNIPeuwYliXnuo8Lkc5X(self):
        """[按客户结算]全部金额结算"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        case = self.common_operations()
        case.DNIPeuwYliXnuo8Lkc5X()
        res = [lambda: self.pc.CsnLYF(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_nsMAwLXUhDECtHFrGK01(self):
        """[按客户结算]部分金额结算-预收款抵扣部分金额"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ', 'e5xB'])
        case = self.common_operations()
        case.nsMAwLXUhDECtHFrGK01()
        res = [lambda: self.pc.CsnLYF(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_vjiYpRgS61Jil8l1AIb1(self):
        """[按客户结算]部分金额结算-预收款抵扣全部金额"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ', 'e5xB'])
        case = self.common_operations()
        case.vjiYpRgS61Jil8l1AIb1()
        res = [lambda: self.pc.CsnLYF(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_akzhzMMfUHIInmvykkV5(self):
        """[按订单批量结算]全部金额结算"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        case = self.common_operations()
        case.akzhzMMfUHIInmvykkV5()
        res = [lambda: self.pc.CsnLYF(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_fT6q4WKrfaMumo1hu8bh(self):
        """[按订单批量结算]部分金额结算"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        case = self.common_operations()
        case.fT6q4WKrfaMumo1hu8bh()
        res = [lambda: self.pc.CsnLYF(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_iKi1BJo4BkgRrnQw07D5(self):
        """[按订单批量结算]结算最大金额"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        case = self.common_operations()
        case.iKi1BJo4BkgRrnQw07D5()
        res = [lambda: self.pc.CsnLYF(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_Mn5CphHorfpXIIk2meIv(self):
        """[按订单批量结算]全部金额结算-预收款抵扣部分金额"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ', 'e5xB'])
        case = self.common_operations()
        case.Mn5CphHorfpXIIk2meIv()
        res = [lambda: self.pc.CsnLYF(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_aRnzRjjFEkGwEOrhcsdE(self):
        """[按订单批量结算]全部金额结算-预收款抵扣全部金额"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ', 'e5xB'])
        case = self.common_operations()
        case.aRnzRjjFEkGwEOrhcsdE()
        res = [lambda: self.pc.CsnLYF(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_tfxkaybmapLMuR1pFqjY(self):
        """[导出]"""
        case = self.common_operations()
        case.tfxkaybmapLMuR1pFqjY()
        res = [lambda: self.pc.T241Se(name='应收对账详情导出', state=2, createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_fuzCuDjXSjYFn8gzpiBS(self):
        """[按机器批量结算]部分金额结算"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        case = self.common_operations()
        case.fuzCuDjXSjYFn8gzpiBS()
        res = [lambda: self.pc.CsnLYF(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_tRKpIUzOlA6X5zEFrDDX(self):
        """[按机器批量结算]导入物品-结算"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        case = self.common_operations()
        case.tRKpIUzOlA6X5zEFrDDX()
        res = [lambda: self.pc.CsnLYF(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_REpw06TJaUceWaw86bTt(self):
        """[按机器批量结算]全部金额结算"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        case = self.common_operations()
        case.REpw06TJaUceWaw86bTt()
        res = [lambda: self.pc.CsnLYF(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_NnVNr1PtqWEZZG0qwyj0(self):
        """[按机器批量结算]部分金额结算-预收款抵扣部分金额"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ', 'e5xB'])
        case = self.common_operations()
        case.NnVNr1PtqWEZZG0qwyj0()
        res = [lambda: self.pc.CsnLYF(receiptTime='now')]
        self.assert_all(*res)


class TestTNuWEuMS(BaseCase, unittest.TestCase):
    """财务管理|业务记账|预付预收"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return finance_r.UjpqCZlmIK()
        else:
            return finance_p.S8e0gGr58Sx(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0f9xh8uqQHD61p0h46zFQ(self):
        """[预付款tab]-新增预付款"""
        case = self.common_operations(login='main')
        case.f9xh8uqQHD61p0h46zFQ()
        res = [lambda: self.pc.Xji7fR(createTime='now', billNo='YF', i=2)]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_yCZnY4hUPXHhgriGFZFe(self):
        """[预付款tab]-导出"""
        case = self.common_operations()
        case.yCZnY4hUPXHhgriGFZFe()
        res = [lambda: self.pc.T241Se(name='预付/预收账单导出', state=2, createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_A7yoyiFi7P8jDGNe67Y0(self):
        """[预收款tab]-新增预收款"""
        case = self.common_operations()
        case.A7yoyiFi7P8jDGNe67Y0()
        res = [lambda: self.pc.Xji7fR(i=2, createTime='now', billNo='YF')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_DsovuKeVyEqIjHwsYRo0(self):
        """[预收款tab]-导出"""
        case = self.common_operations()
        case.DsovuKeVyEqIjHwsYRo0()
        res = [lambda: self.pc.T241Se(name='预付/预收账单导出', state=2, createTime='now')]
        self.assert_all(*res)


if __name__ == '__main__':
    unittest.main()
