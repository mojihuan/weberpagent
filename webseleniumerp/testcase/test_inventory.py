# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.decorators import cached
from common.import_case import *
from config.constant import DICT_DATA


class TestgcyWTobn(BaseCase, unittest.TestCase):
    """库存管理|出库管理|地址管理"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.MTI16ub3xa()
        else:
            return inventory_p.P5fs2CfGvgd(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0SJlFNv1wjIprgodoi79t(self):
        """[新增]-通用业务新增地址"""
        case = self.common_operations(login='idle')
        case.SJlFNv1wjIprgodoi79t()
        res = [lambda: self.pc.ZJX008(headers='idle', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_CLneoMv0agHMlOvAteqD(self):
        """[删除]-删除地址"""
        self.pre.operations(data=['vyTx'])
        case = self.common_operations()
        case.CLneoMv0agHMlOvAteqD()

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_VqptzJXhFGbWdaK6jWAT(self):
        """[编辑]-修改地址信息"""
        self.pre.operations(data=['vyTx'])
        case = self.common_operations()
        case.VqptzJXhFGbWdaK6jWAT()
        res = [lambda: self.pc.ZJX008(headers='idle', createTime='now')]
        self.assert_all(*res)


class TestzADbghUN(BaseCase, unittest.TestCase):
    """库存管理|移交接收管理|移交记录"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.G8bx2b1n15()
        else:
            return None


class TestADZUaGVg(BaseCase, unittest.TestCase):
    """库存管理|移交接收管理|移交物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.Lm0iuO4IIK()
        else:
            return inventory_p.TkKTB87MJyz(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0fcMGsTQ8oTnZfsCSP4CV(self):
        """[移交]-移交物品给库存"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations(login='main')
        case.fcMGsTQ8oTnZfsCSP4CV()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_RHctu5vyliQtE3nHTEWH(self):
        """[导入物品]-移交物品给库存"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.RHctu5vyliQtE3nHTEWH()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)


class TestFdPEYjHE(BaseCase, unittest.TestCase):
    """库存管理|入库管理|物品签收入库"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.TbhHz8UAvI()
        else:
            return inventory_p.Ki45mAxGxif(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0cDYaPc16prs1VtJEU8mr(self):
        """[签收入库]-暂不移交"""
        self.pre.operations(data=['XLBD'])
        case = self.common_operations(login='main')
        case.cDYaPc16prs1VtJEU8mr()
        res = [lambda: self.pc.tTzybz(statusStr='已分拣', businessTime='now', sortationTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_DT5V5CR292DoOcng4DEh(self):
        """[导入入库物品]-暂不移交"""
        self.pre.operations(data=['XLBD'])
        case = self.common_operations()
        case.DT5V5CR292DoOcng4DEh()
        res = [lambda: self.pc.tTzybz(statusStr='已分拣', businessTime='now', sortationTime='now')]
        self.assert_all(*res)


class TestQHf5O7H7(BaseCase, unittest.TestCase):
    """库存管理|入库管理|物流列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.M1swfi30oc()
        else:
            return None


class TestgNXohIzn(BaseCase, unittest.TestCase):
    """库存管理|库存列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.HSA1BkiNHU()
        else:
            return inventory_p.IYYCOpmCVZS(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0vwwTH7A96EyxcdnCteFb(self):
        """[物品详情]-销售出库-已收款"""
        self.pre.operations(data=['ekBx', 'wQ7u'])
        case = self.common_operations(login='main')
        case.vwwTH7A96EyxcdnCteFb()
        res = [lambda: self.pc.bfCKxO(saleTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_ZUfg9nnQSfSaV9zvenlZ(self):
        """[物品详情]-销售出库-未收款"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.ZUfg9nnQSfSaV9zvenlZ()
        res = [lambda: self.pc.bfCKxO(saleTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_YyjrBFFVlBe4IC7IrZyD(self):
        """[物品详情]-销售售后-退货邮寄-已收货"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        case = self.common_operations()
        case.YyjrBFFVlBe4IC7IrZyD()
        res = [lambda: self.pc.rv5p3j(data='a', createTime='now', saleTypeStr='退货')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_kzLjwWovXH0gNxfbTWCC(self):
        """[物品详情]-销售售后-退货邮寄-未收货"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        case = self.common_operations()
        case.kzLjwWovXH0gNxfbTWCC()
        res = [lambda: self.pc.rv5p3j(data='a', createTime='now', saleTypeStr='退货')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_AAfxCTv9LmUzH4gFJKoE(self):
        """[物品详情]-销售售后-自提-已收货"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        case = self.common_operations()
        case.AAfxCTv9LmUzH4gFJKoE()
        res = [lambda: self.pc.rv5p3j(data='a', createTime='now', saleTypeStr='退货')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_SyHpEVSfWeSWPDH9hcUa(self):
        """[物品详情]-销售售后-自提-未收货"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        case = self.common_operations()
        case.SyHpEVSfWeSWPDH9hcUa()
        res = [lambda: self.pc.rv5p3j(data='a', createTime='now', saleTypeStr='退货')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_VCS0Uc7dtvSPIuHtNbaI(self):
        """[物品详情]-销售售后-仅退配件-已收货"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        case = self.common_operations()
        case.VCS0Uc7dtvSPIuHtNbaI()
        res = [lambda: self.pc.rv5p3j(createTime='now', saleTypeStr='仅退配件')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_HNDvVgQsF5uXmqKb3obN(self):
        """[物品详情]-销售售后-仅退配件-未收货"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        case = self.common_operations()
        case.HNDvVgQsF5uXmqKb3obN()
        res = [lambda: self.pc.rv5p3j(data='a', createTime='now', saleTypeStr='仅退配件')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_Nk7bVBssIb2JEsWwVc2R(self):
        """[物品详情]-销售售后-调价"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        case = self.common_operations()
        case.Nk7bVBssIb2JEsWwVc2R()
        res = [lambda: self.pc.rv5p3j(createTime='now', saleTypeStr='调价')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    @unittest.skip('提交有bug还没写')
    def test_mpD87jFny26qKWr3IX13(self):
        """[物品详情]-销售售后-仅退款"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        case = self.common_operations()
        case.mpD87jFny26qKWr3IX13()
        res = [lambda: self.pc.rv5p3j(createTime='now', saleTypeStr='调价')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_D60ATnrNOPRjZtH7QJQv(self):
        """[物品详情]-采购信息-仅退款"""
        self.pre.operations(data=['XLBD'])
        case = self.common_operations()
        case.D60ATnrNOPRjZtH7QJQv()
        res = [lambda: self.pc.LXtfeb(stateStr='已取消', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_KgeXqOhDT97S9ajhSDxB(self):
        """[物品详情]-编辑-物品信息修改"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.KgeXqOhDT97S9ajhSDxB()
        res = [lambda: self.pc.XtWLz8(data='b', time='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_n6qVaJNnhR6yKFZDvMpU(self):
        """[移交]移交采购售后-其他人"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.n6qVaJNnhR6yKFZDvMpU()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='待接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_wWBLmKauWABXgA16zGq5(self):
        """[移交]移交质检-其他人"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.wWBLmKauWABXgA16zGq5()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='待接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_D3dsNkrEsGlGWkoAbUvn(self):
        """[移交]移交维修-其他人"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.D3dsNkrEsGlGWkoAbUvn()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='待接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_BqEQ0BTtXXYnqUFLxnUK(self):
        """[移交]移交销售-其他人"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.BqEQ0BTtXXYnqUFLxnUK()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='待接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_xrzuFX14hLZb53t2Dpl4(self):
        """[移交]移交送修-其他人"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.xrzuFX14hLZb53t2Dpl4()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='待接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_ELzKzsnP7DBzS58RhuRV(self):
        """[移交]移交采购售后-自己"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.ELzKzsnP7DBzS58RhuRV()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_yPtmSmB6LgGBHuYKQex9(self):
        """[移交]移交质检-自己"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.yPtmSmB6LgGBHuYKQex9()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_cQRfPcjML2Pxryt529f9(self):
        """[移交]移交维修-自己"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.cQRfPcjML2Pxryt529f9()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_cZDVh5eyHxStC2Mli9DI(self):
        """[移交]移交销售-自己"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.cZDVh5eyHxStC2Mli9DI()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_OAvKjuICy5p7SX9qfvX4(self):
        """[移交]移交送修-自己"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.OAvKjuICy5p7SX9qfvX4()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)


class TestpqUBS18k(BaseCase, unittest.TestCase):
    """库存管理|入库管理|物流签收入库"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.IPBU7G33xP()
        else:
            return inventory_p.RIG4KKAJOQP(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0Jv79uDAMnGFSvRHesu0B(self):
        """[签收入库]-暂不移交入库"""
        self.pre.operations(data=['XLBD'])
        case = self.common_operations(login='main')
        case.Jv79uDAMnGFSvRHesu0B()
        res = [lambda: self.pc.tTzybz(statusStr='已分拣', businessTime='now', sortationTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_hhbi3Grk7w3kXVnHxfNE(self):
        """[签收入库]-帮卖订单-暂不移交入库"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'AWj7', 'xPPm'])
        case = self.common_operations()
        case.hhbi3Grk7w3kXVnHxfNE()
        res = [lambda: self.pc.tTzybz(headers='vice', statusStr='已分拣', businessTime='now', sortationTime='now')]
        self.assert_all(*res)


class TestLKhE53ov(BaseCase, unittest.TestCase):
    """库存管理|出库管理|仅出库订单列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.MLkZRHOuRf()
        else:
            return inventory_p.XgQm1C4a0op(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_0ZUdNkyxThIMbrQMjq4A0(self):
        """[新建订单]-普通物流"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.ZUdNkyxThIMbrQMjq4A0()
        res = [lambda: self.pc.ABgSE1(outTime='now', orderNo='Ck')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_qawEHf7WaxftnDj1QxYR(self):
        """[新建订单]-快递易"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.qawEHf7WaxftnDj1QxYR()
        res = [lambda: self.pc.ABgSE1(outTime='now', orderNo='Ck')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_KYUijzA3uVmyde4KtozB(self):
        """[新建订单]-导入物品"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.KYUijzA3uVmyde4KtozB()
        res = [lambda: self.pc.ABgSE1(outTime='now', orderNo='Ck')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_e2AnAaVdqHxAw7jEV92t(self):
        """[出库物品退回]-直接入库"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'mL8f'])
        case = self.common_operations(login='main')
        case.e2AnAaVdqHxAw7jEV92t()
        res = [lambda: self.pc.ABgSE1(data='a', returnTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_M04F4OTZMxDuTL4I0abo(self):
        """[出库物品退回]-退回在途"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'mL8f'])
        case = self.common_operations()
        case.M04F4OTZMxDuTL4I0abo()
        res = [lambda: self.pc.ABgSE1(data='a', returnTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_AfpbFoR3N3DHrELC3fyQ(self):
        """[仅出库销售]-已收款"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'mL8f'])
        case = self.common_operations()
        case.AfpbFoR3N3DHrELC3fyQ()
        res = [lambda: self.pc.ABgSE1(outTime='now', orderNo='Ck')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_x4yuI0I1abq0vQb0mI6o(self):
        """[仅出库销售]-未收款"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'mL8f'])
        case = self.common_operations()
        case.x4yuI0I1abq0vQb0mI6o()
        res = [lambda: self.pc.ABgSE1(outTime='now', orderNo='Ck')]
        self.assert_all(*res)


class TestwRTSU94t(BaseCase, unittest.TestCase):
    """库存管理|出库管理|采购售后出库"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.GrqUVUXI3u()
        else:
            return inventory_p.GmJWeaS0RSp(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0DZpllRLFofze0dkHhqfW(self):
        """[采购售后出库]-普通快递-添加物品出库"""
        self.pre.operations(data=['ekBx', 'Fv9l'])
        case = self.common_operations(login='main')
        case.DZpllRLFofze0dkHhqfW()
        res = [lambda: self.pc.BtoGb1(saleStateStr='采购售后中', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_I19nPSWAdkZLyMrB5dfG(self):
        """[采购售后出库]-普通快递-导入物品出库"""
        self.pre.operations(data=['ekBx', 'Fv9l'])
        case = self.common_operations()
        case.I19nPSWAdkZLyMrB5dfG()
        res = [lambda: self.pc.BtoGb1(saleStateStr='采购售后中', createTime='now')]
        self.assert_all(*res)


class TestJZpGS7gM(BaseCase, unittest.TestCase):
    """库存管理|移交接收管理|接收物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.XmR5kBz1S1()
        else:
            return inventory_p.GlsOxUhDpKZ(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0Xj9FgGV65jL0Oi7nZXWg(self):
        """[物品接收]-接收"""
        self.pre.operations(data=['ekBx', 'QKxH'])
        case = self.common_operations(login='main')
        case.Xj9FgGV65jL0Oi7nZXWg()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_lwcE4sypSymkTNNFndKw(self):
        """[物品接收]-扫码接收"""
        self.pre.operations(data=['ekBx', 'QKxH'])
        case = self.common_operations(login='main')
        case.lwcE4sypSymkTNNFndKw()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_GvUiJ1UCIayox4CCu44j(self):
        """[移交单接收]-接收"""
        self.pre.operations(data=['ekBx', 'QKxH'])
        case = self.common_operations(login='main')
        case.GvUiJ1UCIayox4CCu44j()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)


class TestTrBe32n5(BaseCase, unittest.TestCase):
    """库存管理|出库管理|销售出库"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.XwUhCCnV8j()
        else:
            return inventory_p.RVYW5y5DPAq(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0sX84nolF0TRL5RWSl6zx(self):
        """[销售出库]-普通快递-已收款"""
        self.pre.operations(data=['ekBx', 'wQ7u'])
        case = self.common_operations(login='main')
        case.sX84nolF0TRL5RWSl6zx()
        res = [lambda: self.pc.bfCKxO(salesOrder='SA', articlesStateStr='已销售', saleTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_cuv4NM82E2Es3yAJkvoi(self):
        """[销售出库]-普通快递-未收款"""
        self.pre.operations(data=['ekBx', 'wQ7u'])
        case = self.common_operations()
        case.cuv4NM82E2Es3yAJkvoi()
        res = [lambda: self.pc.bfCKxO(salesOrder='SA', articlesStateStr='已销售', saleTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_o7rFfo1GQFC1QUtXg7UR(self):
        """[销售出库]-导入物品出库"""
        self.pre.operations(data=['ekBx', 'wQ7u'])
        case = self.common_operations()
        case.o7rFfo1GQFC1QUtXg7UR()
        res = [lambda: self.pc.bfCKxO(salesOrder='SA', articlesStateStr='已销售', saleTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_B79xRAooA8OFtgTSsB20(self):
        """[铺货出库]-普通快递-已收款"""
        self.pre.operations(data=['ekBx', 'wQ7u'])
        case = self.common_operations()
        case.B79xRAooA8OFtgTSsB20()
        res = [lambda: self.pc.x9ZGyS(batchNo='SJ', shelfTime='now', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_AtZ5UcVuGXvujP2CO3AO(self):
        """[铺货出库]-导入物品出库"""
        self.pre.operations(data=['ekBx', 'wQ7u'])
        case = self.common_operations()
        case.AtZ5UcVuGXvujP2CO3AO()
        res = [lambda: self.pc.x9ZGyS(batchNo='SJ', shelfTime='now', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_Qimx5yME2xvTwfpxXDWH(self):
        """[预售出库]-预售-普通快递"""
        self.pre.operations(data=['ekBx', 'wQ7u'])
        case = self.common_operations()
        case.Qimx5yME2xvTwfpxXDWH()
        res = [lambda: self.pc.x9ZGyS(batchNo='SJ', shelfTime='now', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_iw9rGWgJCzuszvcAednw(self):
        """[预售出库]-导入物品出库"""
        self.pre.operations(data=['ekBx', 'wQ7u'])
        case = self.common_operations()
        case.iw9rGWgJCzuszvcAednw()
        res = [lambda: self.pc.x9ZGyS(batchNo='SJ', shelfTime='now', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_RbCSsdTsnVGk7P77B8ca(self):
        """[销售出库tab]-添加赠送配件-添加物品出库"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'bAym'])
        case = self.common_operations()
        case.RbCSsdTsnVGk7P77B8ca()
        res = [lambda: self.pc.A5MvUv(createTime='now', orderNo='SA')]
        self.assert_all(*res)  # 配件管理|配件统计|赠送明细

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_P7mmCcwk64F1knIdDObr(self):
        """[销售出库]-帮卖订单"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'AWj7', 'ZA5N', 'WZaL', 'Sh3x'])
        case = self.common_operations()
        case.P7mmCcwk64F1knIdDObr()
        res = [lambda: self.pc.bfCKxO(headers='vice', salesOrder='SA', saleTime='now')]
        self.assert_all(*res)


class TestVzG10HZe(BaseCase, unittest.TestCase):
    """库存管理|出库管理|销售售后出库"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.HKYbWELZop()
        else:
            return inventory_p.F4wOAWthE6g(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0A9xC9JwOkl75SfoIqlTM(self):
        """[换货]-普通快递-出库"""
        self.pre.operations(data=['ekBx', 'ekBx', 'wQ7u', 'HRTZ', 'jw4U'])
        case = self.common_operations(login='main')
        case.A9xC9JwOkl75SfoIqlTM()
        res = [lambda: self.pc.rv5p3j(updateTime='now', saleTypeStr='换货', articlesStatusStr='待分货')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_FUNbZmjhH4ul2nZkvDV2(self):
        """[拒退]-普通快递-出库"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ', 'jw4U'])
        case = self.common_operations()
        case.FUNbZmjhH4ul2nZkvDV2()
        res = [lambda: self.pc.rv5p3j(updateTime='now', saleTypeStr='拒退退回', articlesStatusStr='已销售')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_teC3vcKAJkMnapeaIQEH(self):
        """[返修]-普通快递-出库"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ', 'jw4U'])
        case = self.common_operations()
        case.teC3vcKAJkMnapeaIQEH()
        res = [lambda: self.pc.rv5p3j(updateTime='now', saleTypeStr='返修', articlesStatusStr='已销售')]
        self.assert_all(*res)


class Testo1EvIjCN(BaseCase, unittest.TestCase):
    """库存管理|出库管理|送修出库"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.S9pHfGlZA1()
        else:
            return inventory_p.Hqb2YxgNHpt(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0Qp71Bn8xqI3rvwuJ9xCr(self):
        """[送修出库]-普通快递-添加物品出库"""
        self.pre.operations(data=['ekBx', 'Y1eX'])
        case = self.common_operations(login='main')
        case.Qp71Bn8xqI3rvwuJ9xCr()
        res = [lambda: self.pc.send_been_sent_repair(repairStatusName='送修中', repairTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_wrTiHdwvBvcntC1U05Il(self):
        """[送修出库]-普通快递-导入物品出库"""
        self.pre.operations(data=['ekBx', 'Y1eX'])
        case = self.common_operations()
        case.wrTiHdwvBvcntC1U05Il()
        res = [lambda: self.pc.send_been_sent_repair(repairStatusName='送修中', repairTime='now')]
        self.assert_all(*res)


@unittest.skip('没写完')
class TestwBOrYHQ7(BaseCase, unittest.TestCase):
    """库存管理|库存盘点"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.F0teh65lah()
        else:
            return inventory_p.ItZsYP2EEbM(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0yfkRUCxXwAxP0gqU85sU(self):
        """[新建盘点]-开始盘点-添加物品完成盘点"""
        case = self.common_operations(login='main')
        case.yfkRUCxXwAxP0gqU85sU()
        res = [lambda: self.pc.qOAsRC(stockResult=1, updateTime='now', stockNo='PD')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_UUWSDzhkp1IyWEH6s65s(self):
        """[删除]-删除盘点"""
        self.pre.operations(data=['vVf7'])
        case = self.common_operations()
        case.UUWSDzhkp1IyWEH6s65s()


@unittest.skip('没写完')
class TestFYF7l6TG(BaseCase, unittest.TestCase):
    """库存管理|库存调拨"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.InLEWxc2tL()
        else:
            return inventory_p.Sso5zWneHla(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0TkJYyYtSzad1UKsgz33u(self):
        """[新增调拨]-普通快递-搜索添加物品调拨"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations(login='main')
        case.TkJYyYtSzad1UKsgz33u()
        res = [lambda: self.pc.c0oQwY(createTime='now', statusStr='待接收')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_xOKk4jVh1lMYTHUpQpnF(self):
        """[新增调拨]-普通快递-导入物品调拨"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.xOKk4jVh1lMYTHUpQpnF()
        res = [lambda: self.pc.c0oQwY(createTime='now', statusStr='待接收')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_xdMmMEyDlNQfeiWnQR8o(self):
        """[新增调拨]-普通快递-选择添加物品调拨"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.xdMmMEyDlNQfeiWnQR8o()
        res = [lambda: self.pc.c0oQwY(createTime='now', statusStr='待接收')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_paab2hqQQJLuUeP31Y4e(self):
        """[接收]-暂不操作接收"""
        self.pre.operations(data=['ekBx', 'psOC'])
        case = self.common_operations()
        case.paab2hqQQJLuUeP31Y4e()
        res = [lambda: self.pc.c0oQwY(createTime='now', statusStr='已完成')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_xurEsLRqBkTUszD8mRjE(self):
        """[撤销]-确认撤销"""
        self.pre.operations(data=['ekBx', 'psOC'])
        case = self.common_operations()
        case.xurEsLRqBkTUszD8mRjE()
        res = [lambda: self.pc.c0oQwY(createTime='now', statusStr='已撤销')]
        self.assert_all(*res)


if __name__ == '__main__':
    unittest.main()
