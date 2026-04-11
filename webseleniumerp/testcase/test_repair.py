# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.import_case import *


class TestTYjeCNx3(BaseCase, unittest.TestCase):
    """维修管理|维修审核列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return repair_r.QSG3XpHrLa()
        else:
            return repair_p.Ssjg8hIuEBI(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0InAnaHvFTy76b32mumFp(self):
        """[审核]-审核已通过"""
        self.pre.operations(data=['ekBx', 'LrYx', 'OAU3'])
        case = self.common_operations(login='main')
        case.InAnaHvFTy76b32mumFp()
        res = [lambda: self.pc.zyw2kH(auditTime='now', auditStatusStr='已通过')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_oxfkjSLPMvxmooiko075(self):
        """[审核]-审核未通过"""
        self.pre.operations(data=['ekBx', 'LrYx', 'OAU3'])
        case = self.common_operations()
        case.oxfkjSLPMvxmooiko075()
        res = [lambda: self.pc.zyw2kH(auditTime='now', auditStatusStr='未通过')]
        self.assert_all(*res)


class TestBLR6KqnP(BaseCase, unittest.TestCase):
    """维修管理|维修中物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return repair_r.W0EPs560MV()
        else:
            return repair_p.HDrV92hc5GF(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0PYrzOPhQBEGaXo51nyaY(self):
        """[提交维修结果]-移交库存"""
        self.pre.operations(data=['ekBx', 'LrYx'])
        case = self.common_operations(login='main')
        case.PYrzOPhQBEGaXo51nyaY()
        res = [lambda: self.pc.aP7LrV(auditStatusStr='待审核', consignerTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_bmPmqA7zguunIKgYInWf(self):
        """[快速维修]-移交库存"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.bmPmqA7zguunIKgYInWf()
        res = [lambda: self.pc.aP7LrV(auditStatusStr='待审核', consignerTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_kFFewUiXptz4lRt4hmYw(self):
        """[提交维修结果]-添加配件-移交库存"""
        self.pre.operations(data=['ekBx', 'LrYx'])
        case = self.common_operations()
        case.kFFewUiXptz4lRt4hmYw()
        res = [lambda: self.pc.aP7LrV(auditStatusStr='待审核', consignerTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_Xbfhk0aSUEnYlIVthPdi(self):
        """[提交维修结果]-扫码添加配件-移交库存"""
        self.pre.operations(data=['ekBx', 'LrYx'])
        case = self.common_operations()
        case.Xbfhk0aSUEnYlIVthPdi()
        res = [lambda: self.pc.aP7LrV(auditStatusStr='待审核', consignerTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_TwCDg8NuDSsEnMf1GPPT(self):
        """[批量提交维修结果]-移交库存"""
        self.pre.operations(data=['ekBx', 'LrYx'])
        case = self.common_operations()
        case.TwCDg8NuDSsEnMf1GPPT()
        res = [lambda: self.pc.aP7LrV(auditStatusStr='待审核', consignerTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_FzCP5d1Cyk04Rg7XdXWW(self):
        """[未修移交]-移交库存"""
        self.pre.operations(data=['ekBx', 'LrYx'])
        case = self.common_operations()
        case.FzCP5d1Cyk04Rg7XdXWW()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='待接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_Nk6CFDyXMFV3sMEXwPOA(self):
        """[扫码精确未修移交]-移交库存"""
        self.pre.operations(data=['ekBx', 'QKxH'])
        case = self.common_operations()
        case.Nk6CFDyXMFV3sMEXwPOA()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='待接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_i1XbL2CrIPwi6h2C6y1T(self):
        """[提交维修结果]-移交维修"""
        self.pre.operations(data=['ekBx', 'LrYx'])
        case = self.common_operations()
        case.i1XbL2CrIPwi6h2C6y1T()
        res = [lambda: self.pc.aP7LrV(auditStatusStr='待审核', consignerTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_XZsjWIGPtCtyCOxtxlJo(self):
        """[提交维修结果]-移交销售"""
        self.pre.operations(data=['ekBx', 'LrYx'])
        case = self.common_operations()
        case.XZsjWIGPtCtyCOxtxlJo()
        res = [lambda: self.pc.aP7LrV(auditStatusStr='待审核', consignerTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_XaqAzFHNZ0oHiACVcagS(self):
        """[物品拆件]-添加物品确认"""
        self.pre.operations(data=['ekBx', 'LrYx'])
        case = self.common_operations()
        case.XaqAzFHNZ0oHiACVcagS()
        res = [lambda: self.pc.tqIszF(apartNo='CJ', apartTime='now')]
        self.assert_all(*res)


class TesttmuGCB3b(BaseCase, unittest.TestCase):
    """维修管理|维修数据统计"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return None
        else:
            return repair_p.A0lyjFxl9Cw(self.driver)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0jgkToL04qhtLIicYNjr2(self):
        """[导出]"""
        case = self.common_operations(login='main')
        case.jgkToL04qhtLIicYNjr2()
        res = [lambda: self.pc.T241Se(name='维修数据统计导出', state=2, createTime='now')]
        self.assert_all(*res)


class TestuSf4PpKJ(BaseCase, unittest.TestCase):
    """维修管理|待接收物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return None
        else:
            return repair_p.ZdRLslkrxnz(self.driver)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0dtMnLD99xu70O75WPpZI(self):
        """[接收]-物品接收"""
        self.pre.operations(data=['ekBx', 'QKxH'])
        case = self.common_operations(login='special')
        case.dtMnLD99xu70O75WPpZI()
        res = [lambda: self.pc.handover_record(statusStr='待接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_Do71TcM8aJhiO9BlM30Q(self):
        """[扫码精确接收]-物品接收"""
        self.pre.operations(data=['ekBx', 'QKxH'])
        case = self.common_operations()
        case.Do71TcM8aJhiO9BlM30Q()
        res = [lambda: self.pc.handover_record(statusStr='已接收', createTime='now')]
        self.assert_all(*res)


class Testui2fP2rG(BaseCase, unittest.TestCase):
    """维修管理|维修项目列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return repair_r.KHgN9h3KO8()
        else:
            return repair_p.HAJk7yhq6D2(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0otRpL7YRWiPq6A7gGbBE(self):
        """[手机tab]-新增维修项目-品类手机"""
        case = self.common_operations(login='idle')
        case.otRpL7YRWiPq6A7gGbBE()
        res = [lambda: self.pc.DkaFca(i=1, headers='idle')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_SMnvY0RuPqjFoUNE8XAA(self):
        """[手机tab]-新增维修项目-品类平板电脑"""
        case = self.common_operations()
        case.SMnvY0RuPqjFoUNE8XAA()
        res = [lambda: self.pc.DkaFca(i=3, headers='idle')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_A3huxJD5Z6IGUspl0I6d(self):
        """[手机tab]-编辑-修改信息保存"""
        case = self.common_operations()
        case.A3huxJD5Z6IGUspl0I6d()
        res = [lambda: self.pc.DkaFca(i=1, headers='idle')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_z6Fij1duyB9APTQsy7SW(self):
        """[手机tab]-删除"""
        case = self.common_operations()
        case.z6Fij1duyB9APTQsy7SW()

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_V0LveJcsirDBPkbnoy5r(self):
        """[手机tab]-机型配置-新增品牌型号"""
        case = self.common_operations()
        case.V0LveJcsirDBPkbnoy5r()
        res = [lambda: self.pc.DkaFca(i=1, headers='idle')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_Q8t9eC7T5nzs0GLMTihp(self):
        """[手机tab]-机型配置-删除"""
        self.pre.operations(data=['cVtB'])
        case = self.common_operations()
        case.Q8t9eC7T5nzs0GLMTihp()

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_jCLIGsFOwpQqsIwpnxNc(self):
        """[平板电脑tab]-新增维修项目-品类平板电脑"""
        self.pre.operations(data=['cVtB'])
        case = self.common_operations()
        case.jCLIGsFOwpQqsIwpnxNc()
        res = [lambda: self.pc.DkaFca(headers='idle')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_Io7zWL7mncGGiczqV0j9(self):
        """[笔记本电脑tab]-新增维修项目-品类笔记本电脑"""
        self.pre.operations(data=['cVtB'])
        case = self.common_operations()
        case.Io7zWL7mncGGiczqV0j9()
        res = [lambda: self.pc.DkaFca(headers='idle')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_A8HudpWpzF5s1INr3oER(self):
        """[智能手表tab]-新增维修项目-品类智能手表"""
        self.pre.operations(data=['cVtB'])
        case = self.common_operations()
        case.A8HudpWpzF5s1INr3oER()
        res = [lambda: self.pc.DkaFca(headers='idle')]
        self.assert_all(*res)


if __name__ == '__main__':
    unittest.main()
