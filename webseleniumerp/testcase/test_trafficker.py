# coding: utf-8
from common.decorators import cached
from common.base_case import BaseCase
from common.mini_base_case import MiniBaseCase
from common.decorators import test_mode_handler
from common.import_case import *


@test_mode_handler(trafficker_r.ZG6fRe5zTB, None)
class TestEMQEUtBN(MiniBaseCase):
    """二手通小程序|首页|帮卖"""

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_0gSy4Vk4VOP22wEagmKtu(self):
        """[一键帮卖]-从库存添加-我要帮卖"""
        self.pre.operations(data=['ekBx', 'x1dy'])
        self.case.gSy4Vk4VOP22wEagmKtu()
        res = [lambda: self.pc.jOTfI6(orderStateStr='待发货', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_T7vjIsc0mkOJLNIOlGHR(self):
        """[一键帮卖]-从库存添加-我要保卖买断"""
        self.pre.operations(data=['ekBx', 'x1dy'])
        self.case.T7vjIsc0mkOJLNIOlGHR()
        res = [lambda: self.pc.jOTfI6(orderStateStr='待发货', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_Q2CD7BU5QG3ce40zfWJ6(self):
        """[一键帮卖]-从库存添加-我要保卖分润"""
        self.pre.operations(data=['ekBx', 'x1dy'])
        self.case.Q2CD7BU5QG3ce40zfWJ6()
        res = [lambda: self.pc.jOTfI6(orderStateStr='待发货', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_Th8rhqqbFWasw2m5ca09(self):
        """[发货]快递易发货"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'AWj7'])
        self.case.Th8rhqqbFWasw2m5ca09()
        res = [lambda: self.pc.jOTfI6(orderStateStr='待收货', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_KcQ8VA99jSgpYr00tyLM(self):
        """[发货]自行邮寄发货"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'AWj7'])
        self.case.KcQ8VA99jSgpYr00tyLM()
        res = [lambda: self.pc.jOTfI6(orderStateStr='待收货', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_Zng3AfJbx2o0lS97ypXT(self):
        """[发货]自己送发货"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'AWj7'])
        self.case.Zng3AfJbx2o0lS97ypXT()
        res = [lambda: self.pc.jOTfI6(orderStateStr='待收货', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_wiM0WjiOzoeKyaTG2PrC(self):
        """[待质检]-申请退机"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'AWj7', 'ZA5N', 'WZaL'])
        self.case.wiM0WjiOzoeKyaTG2PrC()
        res = [lambda: self.pc.jOTfI6(orderStateStr='待退机', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_ABD3XVRJTfP5w1yu4jHp(self):
        """[待确认]-申请退机"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'ZyMU', 'BDSs', 'WZaL', 'Sh3x'])
        self.case.ABD3XVRJTfP5w1yu4jHp()
        res = [lambda: self.pc.jOTfI6(orderStateStr='待退机', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_q8V7X7imCb99t9ZvMfo8(self):
        """[待议价]-申请退机"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'ZyMU', 'BDSs', 'WZaL', 'Sh3x', 'UWBK'])
        self.case.q8V7X7imCb99t9ZvMfo8()
        res = [lambda: self.pc.jOTfI6(orderStateStr='待退机', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_LMDMfMzEmvr5s6wtfKmX(self):
        """[待议价]-申请退机"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'AWj7', 'ZA5N', 'WZaL', 'Sh3x'])
        self.case.LMDMfMzEmvr5s6wtfKmX()
        res = [lambda: self.pc.jOTfI6(orderStateStr='待退机', updateTime='now')]
        self.assert_all(*res)

    def test_vGclYeJDVchXH8anjkpV(self):
        """[待议价]-确认保卖"""

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_X6ssuFYCjqGxvThVflOf(self):
        """[待确认]-申请议价"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'ZyMU', 'BDSs', 'WZaL', 'Sh3x'])
        self.case.X6ssuFYCjqGxvThVflOf()
        res = [lambda: self.pc.jOTfI6(orderStateStr='待议价', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_bFv5K1H1hfIreNfxq0N7(self):
        """[待退机]-取消退机"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'ZyMU', 'BDSs', 'WZaL', 'Sh3x'])
        self.case.bFv5K1H1hfIreNfxq0N7()
        res = [lambda: self.pc.jOTfI6(orderStateStr='待确认', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_YmNQXNyn0cgOev94cyUn(self):
        """[退机中]-手动签收"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'AWj7', 'ZA5N', 'WZaL', 'Ez0X', 'RGCO'])
        self.case.YmNQXNyn0cgOev94cyUn()
        res = [lambda: self.pc.jOTfI6(orderStateStr='已退机', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_pEdX4tcJCCi2ANETDgLh(self):
        """[退机中]-物流签收入库"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'AWj7', 'ZA5N', 'WZaL', 'Ez0X', 'weY4'])
        self.case.pEdX4tcJCCi2ANETDgLh()
        res = [lambda: self.pc.jOTfI6(orderStateStr='退机中', updateTime='now')]
        self.assert_all(*res)


@test_mode_handler(trafficker_r.KUHmqHA6mE, None)
class Testu7WDm1zP(MiniBaseCase):
    """二手通小程序|首页|库存"""

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_0FpdSwapLHorzSgUTXzO3(self):
        """[流程]新建盘点-提交盘点-完成盘点"""
        self.case.FpdSwapLHorzSgUTXzO3()
        res = [lambda: self.pc.qOAsRC(updateTime='now', stockNo='PD')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_NolDGk9PEn4XYz8LrUgH(self):
        """[流程]移交物品-移交质检"""
        self.pre.operations(data=['ekBx'])
        self.case.NolDGk9PEn4XYz8LrUgH()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_AHeVie0Oup6y9tNMelfQ(self):
        """[流程]移交物品-移交维修"""
        self.pre.operations(data=['ekBx'])
        self.case.AHeVie0Oup6y9tNMelfQ()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_cj8y7BldKp6aX4lbkB29(self):
        """[流程]移交物品-移交送修"""
        self.pre.operations(data=['ekBx'])
        self.case.cj8y7BldKp6aX4lbkB29()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_B0dbkcikzi0su2qFAEqM(self):
        """[流程]移交物品-移交销售"""
        self.pre.operations(data=['ekBx'])
        self.case.B0dbkcikzi0su2qFAEqM()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_djAbq91arWjnM274GmSY(self):
        """[流程]移交物品-移交采购售后"""
        self.pre.operations(data=['ekBx'])
        self.case.djAbq91arWjnM274GmSY()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_wEfefFG7nEo3Kan0I3cY(self):
        """[流程]移交物品-移交库存"""
        self.pre.operations(data=['ekBx'])
        self.case.wEfefFG7nEo3Kan0I3cY()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_rOtk4WU5CRaxiuoJLvh6(self):
        """[流程]签收入库"""
        self.pre.operations(data=['XLBD'])
        self.case.rOtk4WU5CRaxiuoJLvh6()
        res = [lambda: self.pc.tTzybz(statusStr='已分拣', sortationTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_VDDb6S8keIp4qBsOIcxz(self):
        """[流程]签收入库-移交质检"""
        self.pre.operations(data=['XLBD'])
        self.case.VDDb6S8keIp4qBsOIcxz()
        res = [lambda: self.pc.tTzybz(statusStr='已分拣', sortationTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_PylpYfWMSCO7tb8yWDov(self):
        """[流程]签收入库-移交维修"""
        self.pre.operations(data=['XLBD'])
        self.case.PylpYfWMSCO7tb8yWDov()
        res = [lambda: self.pc.tTzybz(statusStr='已分拣', sortationTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_Bb6rtOhNILeRK1H3CswE(self):
        """[流程]签收入库-移交送修"""
        self.pre.operations(data=['XLBD'])
        self.case.Bb6rtOhNILeRK1H3CswE()
        res = [lambda: self.pc.tTzybz(statusStr='已分拣', sortationTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_gwkXCubQ6Kh0UhJCOUp6(self):
        """[流程]签收入库-移交销售"""
        self.pre.operations(data=['XLBD'])
        self.case.gwkXCubQ6Kh0UhJCOUp6()
        res = [lambda: self.pc.tTzybz(statusStr='已分拣', sortationTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_K9U0fcTlznz9x5lbCPxH(self):
        """[流程]签收入库-移交采购"""
        self.pre.operations(data=['XLBD'])
        self.case.K9U0fcTlznz9x5lbCPxH()
        res = [lambda: self.pc.tTzybz(statusStr='已分拣', sortationTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_wrfq9qJlYzprjxoG4WmO(self):
        """[流程]签收入库-移交库存"""
        self.pre.operations(data=['XLBD'])
        self.case.wrfq9qJlYzprjxoG4WmO()
        res = [lambda: self.pc.tTzybz(statusStr='已分拣', sortationTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_AXJg2IWq4WbiLzdWv6RK(self):
        """[流程]销售-接收物品"""
        self.pre.operations(data=['ekBx', 'DT6i'])
        self.case.AXJg2IWq4WbiLzdWv6RK()
        res = [lambda: self.pc.handover_record(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_gUlS03xcTzSc6opuoZXv(self):
        """[流程]签收入库"""
        self.pre.operations(data=['XLBD'])
        self.case.gUlS03xcTzSc6opuoZXv()
        res = [lambda: self.pc.tTzybz(statusStr='已分拣', businessTime='now')]
        self.assert_all(*res)


@test_mode_handler(trafficker_r.Htxslq7CN1, None)
class TestuLHUc7zc(MiniBaseCase):
    """二手通小程序|首页|采购"""

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_0N8ZYbEQ5wRbTFaYhk54m(self):
        """[流程]新增采购单-智能手表-已到货-未付款"""
        self.case.N8ZYbEQ5wRbTFaYhk54m()
        res = [lambda: self.pc.LXtfeb(purchaseTime='now', stateStr='已收货')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_KKVgCekmpYe0dXD1TQoP(self):
        """[流程]新增采购单-手机-已到货-未付款-入库移交维修"""
        self.case.KKVgCekmpYe0dXD1TQoP()
        res = [lambda: self.pc.LXtfeb(purchaseTime='now', stateStr='已收货')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_iuU1ZpZnIF2nfnGtBxhK(self):
        """[流程]采购入库"""
        self.pre.operations(data=['XLBD'])
        self.case.iuU1ZpZnIF2nfnGtBxhK()
        res = [lambda: self.pc.tTzybz(statusStr='已分拣', businessTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_LiiO1y6jvNGLbSiTWHmU(self):
        """[流程]采购入库-移交质检"""
        self.pre.operations(data=['XLBD'])
        self.case.LiiO1y6jvNGLbSiTWHmU()
        res = [lambda: self.pc.tTzybz(statusStr='已分拣', businessTime='now')]
        self.assert_all(*res)


@test_mode_handler(trafficker_r.JeJHxqrd7e, None)
class TestXS46W68s(MiniBaseCase):
    """二手通小程序|首页|质检"""

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_0GCcaGfhZIx5dmNXOGPoG(self):
        """[流程]提交质检结果"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        self.case.GCcaGfhZIx5dmNXOGPoG()
        res = [lambda: self.pc.RWfXxd(qualityFinishTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_TIdR7zy3q7gsA97wufMG(self):
        """[流程]快速质检-提交质检结果"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        self.case.TIdR7zy3q7gsA97wufMG()
        res = [lambda: self.pc.RWfXxd(qualityFinishTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_fRpQsQhibllGcUnGvL4b(self):
        """[流程]新增质检单"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        self.case.fRpQsQhibllGcUnGvL4b()
        res = [lambda: self.pc.RWfXxd(qualityFinishTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_frFIFPmzY5aUapx40XDq(self):
        """[流程]先质检后入库"""
        self.pre.operations(data=['Ufaw', 'oSUT', 'XaUk'])
        self.case.frFIFPmzY5aUapx40XDq()
        res = [lambda: self.pc.RWfXxd(qualityFinishTime='now')]
        self.assert_all(*res)


@test_mode_handler(trafficker_r.BGV1dswh7k, None)
class TesteTskpyLV(MiniBaseCase):
    """二手通小程序|首页|维修"""

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_0qS2uDNdC7LfquknU8HMF(self):
        """[流程]物品维修-移交维修"""
        self.pre.operations(data=['ekBx', 'LrYx'])
        self.case.qS2uDNdC7LfquknU8HMF()
        res = [lambda: self.pc.aP7LrV(auditStatusStr='待审核', consignerTime='now')]
        self.assert_all(*res)


@test_mode_handler(trafficker_r.UGpw1VZJZZ, None)
class TesteJzaIqlr(MiniBaseCase):
    """二手通小程序|首页|销售"""

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_0WyGu6Pcc1zlfEZUHYROZ(self):
        """[流程]销售出库-部分收款"""
        self.pre.operations(data=['ekBx', 'wQ7u'])
        self.case.WyGu6Pcc1zlfEZUHYROZ()
        res = [lambda: self.pc.bfCKxO(articlesStateStr='已销售', saleTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_I1mqk82QVzJNQKaTV6mz(self):
        """[流程]销售出库-全款收款"""
        self.pre.operations(data=['ekBx', 'wQ7u'])
        self.case.I1mqk82QVzJNQKaTV6mz()
        res = [lambda: self.pc.bfCKxO(articlesStateStr='已销售', saleTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_cjzeWBYzVIvAQsaSE5Uv(self):
        """[流程]销售出库-全款收款-赠送配件"""
        self.pre.operations(data=['ekBx', 'wQ7u'])
        self.case.cjzeWBYzVIvAQsaSE5Uv()
        res = [lambda: self.pc.bfCKxO(articlesStateStr='已销售', saleTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_ZuRvUQFLB6nCYNOzrUSt(self):
        """[流程]销售出库-未收款-新增销售客户"""
        self.pre.operations(data=['ekBx', 'wQ7u'])
        self.case.ZuRvUQFLB6nCYNOzrUSt()
        res = [lambda: self.pc.bfCKxO(articlesStateStr='已销售', saleTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_D7cyIB59qNYvDxKX9oXF(self):
        """[流程]销售出库-未收款-快递易"""
        self.pre.operations(data=['ekBx', 'wQ7u'])
        self.case.D7cyIB59qNYvDxKX9oXF()
        res = [lambda: self.pc.bfCKxO(articlesStateStr='已销售', saleTime='now')]
        self.assert_all(*res)
