# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.import_case import *


class TestRBXuX2jX(BaseCase, unittest.TestCase):
    """质检管理|质检中物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return quality_r.BN75aoC3Ic()
        else:
            return quality_p.QykEu6IoOjB(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0TyClpwIrykofhqf4laif(self):
        """[提交质检结果]-默认检测项-移交库存"""
        self.pre.operations(data=['ekBx', 'oSUT'])
        case = self.common_operations(login='main')
        case.TyClpwIrykofhqf4laif()
        res = [lambda: self.pc.RWfXxd(qualityFinishTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_RMOcTd2L2tS32gouvcPO(self):
        """[提交质检结果]-无移交"""
        self.pre.operations(data=['ekBx', 'oSUT'])
        case = self.common_operations()
        case.RMOcTd2L2tS32gouvcPO()
        res = [lambda: self.pc.RWfXxd(qualityFinishTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_aKblpEyB7wculAa6At1D(self):
        """[快速质检]-添加物品-提交质检结果"""
        self.pre.operations(data=['ekBx', 'oSUT'])
        case = self.common_operations()
        case.aKblpEyB7wculAa6At1D()
        res = [lambda: self.pc.RWfXxd(qualityFinishTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_DvC4kRy5eVWdWGN9cPXB(self):
        """[未验移交]-移交库存"""
        self.pre.operations(data=['ekBx', 'oSUT'])
        case = self.common_operations()
        case.DvC4kRy5eVWdWGN9cPXB()
        res = [lambda: self.pc.XtWLz8(data='b', typeStr='移交', time='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_BHQX5vbmOfBJ4z8CzdvG(self):
        """[扫码批量未验移交]-未验移交采购售后"""
        self.pre.operations(data=['ekBx', 'oSUT'])
        case = self.common_operations()
        case.BHQX5vbmOfBJ4z8CzdvG()
        res = [lambda: self.pc.XtWLz8(data='b', typeStr='移交', time='now')]
        self.assert_all(*res)


class TestKVInw0t5(BaseCase, unittest.TestCase):
    """质检管理|质检内容模版"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return quality_r.GEh4rKFYZs()
        else:
            return quality_p.ZykOkDKuSN0(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0GySsTzThuG7Y0qU4dr6w(self):
        """[新增]-默认选项"""
        case = self.common_operations(login='idle')
        case.GySsTzThuG7Y0qU4dr6w()
        res = [lambda: self.pc.qjDA2x(headers='idle', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_giRhsRX1en0Lx6jNhHwp(self):
        """[编辑]-默认选项"""
        self.pre.operations(data=['ZyCo'])
        case = self.common_operations()
        case.giRhsRX1en0Lx6jNhHwp()
        res = [lambda: self.pc.qjDA2x(headers='idle', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_fFy1TGBgZDGQp4384V92(self):
        """[删除]"""
        self.pre.operations(data=['ZyCo'])
        case = self.common_operations()
        case.fFy1TGBgZDGQp4384V92()


class TestpPng8rjy(BaseCase, unittest.TestCase):
    """质检管理|待接收物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return quality_r.JPtRHdbeHo()
        else:
            return quality_p.ImDO8pXuDcy(self.driver)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0I3DHz0up0R0FCJ93wYgX(self):
        """[接收]-单个物品接收"""
        self.pre.operations(data=['ekBx', 'aMWA'])
        case = self.common_operations(login='special')
        case.I3DHz0up0R0FCJ93wYgX()
        res = [lambda: self.pc.handover_record(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_jWTmru3WQNlJkhaj32WL(self):
        """[扫码精确接收]-单个物品接收"""
        self.pre.operations(data=['ekBx', 'aMWA'])
        case = self.common_operations()
        case.jWTmru3WQNlJkhaj32WL()
        res = [lambda: self.pc.handover_record(statusStr='已接收', createTime='now')]
        self.assert_all(*res)


class Testh2j7wRb0(BaseCase, unittest.TestCase):
    """质检管理|先质检后入库"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return quality_r.DItqmHbtYn()
        else:
            return quality_p.Nr0ncfVwUUT(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0cKaXogneNjTTTmAdUTcW(self):
        """[非库存物品tab]-人工快速质检-选择苹果手机-提交质检报告"""
        self.pre.operations(data=['ekBx', 'oSUT'])
        case = self.common_operations(login='main')
        case.cKaXogneNjTTTmAdUTcW()
        res = [lambda: self.pc.J9mkzk(updateTime='now', articlesStatusStr='非库内物品', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_m1SZEHq9GOLysyiwTJhR(self):
        """[非库内物品tab]-批量采购入库-采购入库成功"""
        self.pre.operations(data=['Ufaw', 'oSUT', 'XaUk'])
        case = self.common_operations()
        case.m1SZEHq9GOLysyiwTJhR()
        res = [lambda: self.pc.LXtfeb(purchaseTime='now', stateStr='已发货')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_QkyLf7Jg3kvDyadrrVeA(self):
        """[非库内物品tab]-采购入库-采购入库成功"""
        self.pre.operations(data=['Ufaw', 'oSUT', 'XaUk'])
        case = self.common_operations()
        case.QkyLf7Jg3kvDyadrrVeA()
        res = [lambda: self.pc.LXtfeb(purchaseTime='now', stateStr='已发货')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_F89aoKW4uHkSuyvilmhi(self):
        """[非库内物品tab]-采购入库-采购入库上架商城"""
        self.pre.operations(data=['Ufaw', 'oSUT', 'XaUk'])
        case = self.common_operations()
        case.F89aoKW4uHkSuyvilmhi()

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_YXbGCNN4QmspmmrgyGE1(self):
        """[非库内物品tab]-编辑报告-重新生成质检报告"""
        case = self.common_operations()
        case.YXbGCNN4QmspmmrgyGE1()
        res = [lambda: self.pc.J9mkzk(updateTime='now', articlesStatusStr='非库内物品', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_KlvURYJReV7HI5zUM2ZK(self):
        """[非库内物品tab]-编辑报告-修改当前报告"""
        case = self.common_operations()
        case.KlvURYJReV7HI5zUM2ZK()
        res = [lambda: self.pc.J9mkzk(updateTime='now', articlesStatusStr='非库内物品', createTime='now')]
        self.assert_all(*res)


class TestS1iMHraD(BaseCase, unittest.TestCase):
    """质检管理|待移交物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return quality_r.DItqmHbtYn()
        else:
            return quality_p.Nr0ncfVwUUT(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0j8LwPxK1SoYZffAVSK0E(self):
        """[复检]-移交质检"""
        self.pre.operations(data=['Ufaw', 'oSUT', 'wOOy'])
        case = self.common_operations(login='main')
        case.j8LwPxK1SoYZffAVSK0E()
        res = [lambda: self.pc.RWfXxd(qualityTypeStr='人工选择', qualityFinishTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_cnBfO0w1V0T7Puy4uF3I(self):
        """[移交]-移交库存"""
        self.pre.operations(data=['Ufaw', 'oSUT', 'wOOy'])
        case = self.common_operations()
        case.cnBfO0w1V0T7Puy4uF3I()
        res = [lambda: self.pc.RWfXxd(qualityTypeStr='人工选择', qualityFinishTime='now')]
        self.assert_all(*res)


if __name__ == '__main__':
    unittest.main()
