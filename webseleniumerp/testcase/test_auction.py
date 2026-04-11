# coding: utf-8
from common.decorators import cached
from common.base_case import BaseCase
from common.mini_base_case import MiniBaseCase
from common.decorators import test_mode_handler
from common.import_case import *


@test_mode_handler(auction_r.ZTIxIMcZz7,auction_p.ZBkZG7Xjdy3)
class TestuVvojNGT(MiniBaseCase):
    """保卖小程序|首页"""

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    def test_0OUEyhYBkDqtcP7GO9DPa(self):
        """[快速发货]-创建订单"""
        self.case.OUEyhYBkDqtcP7GO9DPa()
        res = [lambda: self.pc.dKWl3w(i=1, statusDesc='待发货', placeOrderTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    def test_utX70draGUqBWb9xyAMA(self):
        """[精确发货]自动估价-创建订单"""
        self.case.utX70draGUqBWb9xyAMA()
        res = [lambda: self.pc.dKWl3w(i=1, statusDesc='待发货', placeOrderTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_BipQkv2GeGlQ96IF4MWs(self):
        """[快速发货]-创建订单"""
        self.case.BipQkv2GeGlQ96IF4MWs()
        res = [lambda: self.pc.dKWl3w(i=1, statusDesc='待发货', placeOrderTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_Ggf9HFpxeJakOskwG6Fo(self):
        """[快速发货]-数量最大值-创建订单"""
        self.case.Ggf9HFpxeJakOskwG6Fo()
        res = [lambda: self.pc.dKWl3w(i=1, statusDesc='待发货', placeOrderTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_Cb5TwEFeOGRjQqpsPYhX(self):
        """[精确发货]自动估价-创建订单"""
        self.case.Cb5TwEFeOGRjQqpsPYhX()
        res = [lambda: self.pc.dKWl3w(i=1, statusDesc='待发货', placeOrderTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_Sx6ZHoGa30GK1xH2QbdF(self):
        """[质检服务]创建订单"""
        self.case.Sx6ZHoGa30GK1xH2QbdF()
        res = [lambda: self.pc.dKWl3w(i=1, statusDesc='待发货', placeOrderTime='now')]
        self.assert_all(*res)


@test_mode_handler(auction_r.FoIA7X707t, None)
class TestwQEDRnwu(MiniBaseCase):
    """保卖小程序|我的"""

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_0IXznmT0bw7FbeHeJCKo6(self):
        """[待销售]-今日参考价-销售物品"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu'])
        self.case.IXznmT0bw7FbeHeJCKo6()
        res = [lambda: self.pc.platform_virtual_XtWLz8(headers='super', i=3, statusStr='销售中', signTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_fCa9uV4NiZ8jEqmYeUCb(self):
        """[待销售]-自主定价-销售物品"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu'])
        self.case.fCa9uV4NiZ8jEqmYeUCb()
        res = [lambda: self.pc.platform_virtual_XtWLz8(headers='super', i=3, statusStr='销售中', signTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_yFYRFwLu0JNJimcMK5sd(self):
        """[待销售]-平台定价-销售物品"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu'])
        self.case.yFYRFwLu0JNJimcMK5sd()
        res = [lambda: self.pc.platform_virtual_XtWLz8(headers='super', i=5, statusStr='待平台确认', signTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_D1O3SOVl05gD2Lts19A9(self):
        """[待销售]-复检"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu'])
        self.case.D1O3SOVl05gD2Lts19A9()
        res = [lambda: self.pc.BsGxx9(data='b', statusStr='待审核', applyTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_vSYI2uUTSCpcmhYjD9PL(self):
        """[待销售]-快递退货"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu'])
        self.case.vSYI2uUTSCpcmhYjD9PL()
        res = [lambda: self.pc.hnqSw4(data='a', i=1, logisticsTypeStr='快递', applyTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_opIdDf5eKi5IeleUQBrA(self):
        """[待销售]-自提退货"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu'])
        self.case.opIdDf5eKi5IeleUQBrA()
        res = [lambda: self.pc.hnqSw4(data='a', i=2, logisticsTypeStr='自提', applyTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_iGivKV5TSvAIvnbdwJRr(self):
        """[待销售]-无需质检-退货"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'Q7Xz', '@AB8'])
        self.case.iGivKV5TSvAIvnbdwJRr()
        res = [lambda: self.pc.hnqSw4(data='a', i=1, logisticsTypeStr='快递', applyTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_nFqNMqf4dIPEGjrwj8SB(self):
        """[销售中]-取消销售"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO'])
        self.case.nFqNMqf4dIPEGjrwj8SB()
        obj = cached('id')
        res = [lambda: self.pc.aY387y(j=1, i=2, id=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_c6MpT8xfZmLs5uZMq385(self):
        """[销售中]-改价"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO'])
        self.case.case.c6MpT8xfZmLs5uZMq385()
        obj = cached('id')
        obj_2 = cached('upbeatPrice')
        res = [lambda: self.pc.aY387y(j=1, i=3, id=obj, upbeatPrice=obj_2)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_O9TSVizVMFbBHj4PSQi5(self):
        """[待平台确认]-取消销售"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'Q7Xz'])
        self.case.O9TSVizVMFbBHj4PSQi5()
        obj = cached('id')
        res = [lambda: self.pc.aY387y(j=1, i=2, id=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_zYQJNPRNzQr7xEmj3Xov(self):
        """[退货中]-自提改快递-更改退货方式"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'fNXh'])
        self.case.zYQJNPRNzQr7xEmj3Xov()
        res = [lambda: self.pc.hnqSw4(data='a', i=1, logisticsTypeStr='快递', applyTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_Np66pyiMQJz6zbkMLvGH(self):
        """[退货中]-取消退货"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'fNXh'])
        self.case.Np66pyiMQJz6zbkMLvGH()
        res = [lambda: self.pc.hnqSw4(data='a', i=5, updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_CPBlWzLFLVwb7oz15BxA(self):
        """[退货已出库]-确认收货"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'xfzp', 'hkXQ'])
        self.case.CPBlWzLFLVwb7oz15BxA()
        res = [lambda: self.pc.hnqSw4(data='b', i=4, outboundTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_ONNJvxBz8YiF5nJbXEx9(self):
        """[报价确认]-确认销售"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'Q7Xz', 'KnkQ', 'q9eJ'])
        self.case.ONNJvxBz8YiF5nJbXEx9()
        res = [lambda: self.pc.platform_virtual_XtWLz8(headers='super', signTime='now', statusStr='销售待出库')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_cWki4FW4tSlwK63nwMDm(self):
        """[待发货]-立即发货-顺丰快递邮寄发货"""
        self.pre.operations(data=['spKR'])
        self.case.cWki4FW4tSlwK63nwMDm()
        res = [lambda: self.pc.dKWl3w(i=2, placeOrderTime='now', businessTypeDesc='壹准保卖', statusDesc='待取件', expressTypeDesc='快递邮寄')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_GWIqOqgj1k2cLGBWcfJP(self):
        """[待发货]-立即发货-自行邮寄-顺丰发货"""
        self.pre.operations(data=['spKR'])
        self.case.GWIqOqgj1k2cLGBWcfJP()
        res = [lambda: self.pc.dKWl3w(i=3, placeOrderTime='now', businessTypeDesc='壹准保卖', statusDesc='待收货', expressTypeDesc='自己送货/自取')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_fK0PREFRv2Msvl2flpXO(self):
        """[待发货]-立即发货-自己送货"""
        self.pre.operations(data=['spKR'])
        self.case.fK0PREFRv2Msvl2flpXO()
        res = [lambda: self.pc.dKWl3w(i=3, placeOrderTime='now', businessTypeDesc='壹准保卖', statusDesc='待收货', expressTypeDesc='自己送货/自取')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_JnMqTWMbAzexR3HQWbXB(self):
        """[待发货]-立即发货-自己送货"""
        self.pre.operations(data=['spKR'])
        self.case.JnMqTWMbAzexR3HQWbXB()
        res = [lambda: self.pc.dKWl3w(i=3, placeOrderTime='now', businessTypeDesc='壹准保卖', statusDesc='待收货', expressTypeDesc='自己送货/自取')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_jC7q178S4xk9JOlI2EUW(self):
        """[待发货]-立即发货-顺丰快递邮寄-次日发货"""
        self.pre.operations(data=['spKR'])
        self.case.jC7q178S4xk9JOlI2EUW()
        res = [lambda: self.pc.dKWl3w(i=2, placeOrderTime='now', businessTypeDesc='壹准保卖', statusDesc='待取件', expressTypeDesc='快递邮寄')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_axbH6Gue6hxYBUT7LOr0(self):
        """[待发货]-立即发货-顺丰快递邮寄-无收货地址"""
        self.pre.operations(data=['spKR'])
        self.case.axbH6Gue6hxYBUT7LOr0()
        res = [lambda: self.pc.dKWl3w(i=2, placeOrderTime='now', businessTypeDesc='壹准保卖', statusDesc='待取件', expressTypeDesc='快递邮寄')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_QVxsGMaLD5ww9O6KQQSe(self):
        """[待发货]-取消订单"""
        self.pre.operations(data=['spKR'])
        self.case.QVxsGMaLD5ww9O6KQQSe()
        res = [lambda: self.pc.dKWl3w(data='b', i=6, placeOrderTime='now', businessTypeDesc='壹准保卖', statusDesc='已取消')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_DE8blhh3n53JAyeZSU0m(self):
        """[待取件]-取消订单"""
        self.pre.operations(data=['spKR', '@AB6'])
        self.case.DE8blhh3n53JAyeZSU0m()
        obj = cached('id')
        res = [lambda: self.pc.aY387y(data='b', i=6, id=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_h6mvvkdQDZSeUdSoNi8W(self):
        """[待收货]-取消订单"""
        self.pre.operations(data=['spKR', 'VyCN'])
        self.case.h6mvvkdQDZSeUdSoNi8W()
        obj = cached('id')
        res = [lambda: self.pc.aY387y(data='b', i=6, id=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_dUwWvkoALcS9DZVO0Ldg(self):
        """[待收货]-重新发货-顺丰快递"""
        self.pre.operations(data=['spKR', 'VyCN'])
        self.case.dUwWvkoALcS9DZVO0Ldg()
        res = [lambda: self.pc.dKWl3w(i=2, placeOrderTime='now', businessTypeDesc='壹准保卖', statusDesc='待取件', expressTypeDesc='快递邮寄')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_POJtV9lZxRzUvoZMBNQB(self):
        """[待收货]-重新发货-自行邮寄"""
        self.pre.operations(data=['spKR', 'VyCN'])
        self.case.POJtV9lZxRzUvoZMBNQB()
        res = [lambda: self.pc.dKWl3w(i=3, placeOrderTime='now', businessTypeDesc='壹准保卖', statusDesc='待收货', expressTypeDesc='自己送货/自取')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_jHgDbDirasYNbKdklnIY(self):
        """[待收货]-重新发货-自己送"""
        self.pre.operations(data=['spKR', 'VyCN'])
        self.case.jHgDbDirasYNbKdklnIY()
        res = [lambda: self.pc.dKWl3w(i=3, placeOrderTime='now', businessTypeDesc='壹准保卖', statusDesc='待收货', expressTypeDesc='自己送货/自取')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_dkzE7aNehgS9qMzBIRzf(self):
        """[待发货]-质检服务-立即发货-顺丰快递邮寄发货"""
        self.pre.operations(data=['gpvd'])
        self.case.dkzE7aNehgS9qMzBIRzf()
        res = [lambda: self.pc.dKWl3w(i=2, placeOrderTime='now', businessTypeDesc='质检服务', statusDesc='待取件', expressTypeDesc='快递邮寄')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_oOoG2Yvd9naVzPCCZOBU(self):
        """[待发货]-质检服务-立即发货-自行邮寄-顺丰发货"""
        self.pre.operations(data=['gpvd'])
        self.case.oOoG2Yvd9naVzPCCZOBU()
        res = [lambda: self.pc.dKWl3w(i=3, placeOrderTime='now', businessTypeDesc='质检服务', statusDesc='待收货', expressTypeDesc='自己送货/自取')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_KDByBY1AXyw9jWoR1wVN(self):
        """[待发货]-质检服务-立即发货-自己送货"""
        self.pre.operations(data=['gpvd'])
        self.case.KDByBY1AXyw9jWoR1wVN()
        res = [lambda: self.pc.dKWl3w(i=3, placeOrderTime='now', businessTypeDesc='质检服务', statusDesc='待收货', expressTypeDesc='自己送货/自取')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_E0ZBM1bZ77yxxR0xKw5r(self):
        """[待发货]-质检服务-立即发货-顺丰快递邮寄-次日发货"""
        self.pre.operations(data=['gpvd'])
        self.case.E0ZBM1bZ77yxxR0xKw5r()
        res = [lambda: self.pc.dKWl3w(i=2, placeOrderTime='now', businessTypeDesc='质检服务', statusDesc='待取件', expressTypeDesc='快递邮寄')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_HU0PCydYlVIqdfWaGMjN(self):
        """[待发货]-质检服务-立即发货-顺丰快递邮寄-无发货地址"""
        self.pre.operations(data=['gpvd'])
        self.case.HU0PCydYlVIqdfWaGMjN()
        res = [lambda: self.pc.dKWl3w(i=3, placeOrderTime='now', businessTypeDesc='质检服务', statusDesc='自己送货/自取', expressTypeDesc='快递邮寄')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_PviYbAYqWAHOvqa557i4(self):
        """[待发货]-质检服务-立即发货-顺丰快递邮寄-无收货地址"""
        self.pre.operations(data=['gpvd'])
        self.case.PviYbAYqWAHOvqa557i4()
        res = [lambda: self.pc.dKWl3w(i=2, placeOrderTime='now', businessTypeDesc='质检服务', statusDesc='待取件', expressTypeDesc='快递邮寄')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_GG02SXVJvvxVfIaz5KPi(self):
        """[待发货]-质检服务-取消订单"""
        self.pre.operations(data=['gpvd'])
        self.case.GG02SXVJvvxVfIaz5KPi()
        res = [lambda: self.pc.dKWl3w(i=6, placeOrderTime='now', businessTypeDesc='质检服务', statusDesc='已取消')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_dnH26r9vPAzxPhrGlF4V(self):
        """[待取件]-质检服务-取消订单"""
        self.pre.operations(data=['gpvd', '@AB7'])
        self.case.dnH26r9vPAzxPhrGlF4V()
        res = [lambda: self.fulfillment.order_manage(data='b', i=6, receiptNum=0, placeOrderTime='now', businessTypeDesc='质检服务', statusDesc='已取消')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_t944F3rbr3phQU1rks2g(self):
        """[待收货]-质检服务-取消订单"""
        self.pre.operations(data=['gpvd', 'dKLc'])
        self.case.t944F3rbr3phQU1rks2g()
        res = [lambda: self.fulfillment.order_manage(data='b', i=6, receiptNum=0, placeOrderTime='now', businessTypeDesc='质检服务', statusDesc='已取消')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_N77Kx6zXsaGkusHouXhf(self):
        """[待收货]-质检服务-重新发货-顺丰快递"""
        self.pre.operations(data=['gpvd', 'dKLc'])
        self.case.N77Kx6zXsaGkusHouXhf()
        res = [lambda: self.pc.dKWl3w(i=3, placeOrderTime='now', businessTypeDesc='质检服务', statusDesc='待收货', expressTypeDesc='自己送货')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_P4olp9T5viFuNTxwILbU(self):
        """[待收货]-质检服务-重新发货-自行邮寄"""
        self.pre.operations(data=['gpvd', 'dKLc'])
        self.case.P4olp9T5viFuNTxwILbU()
        res = [lambda: self.pc.dKWl3w(i=3, placeOrderTime='now', businessTypeDesc='质检服务', statusDesc='待收货', expressTypeDesc='自己送货/自取')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_RZQfpgsxpRx4JZVtCxnq(self):
        """[待收货]-质检服务-重新发货-自己送"""
        self.pre.operations(data=['gpvd', 'dKLc'])
        self.case.RZQfpgsxpRx4JZVtCxnq()
        res = [lambda: self.pc.dKWl3w(i=3, placeOrderTime='now', businessTypeDesc='质检服务', statusDesc='待收货', expressTypeDesc='自己送货/自取')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_GgObI3IHddbUmzzKy0Ur(self):
        """[质检完成]-质检服务-快递退货"""
        self.pre.operations(data=['gpvd', 'dKLc', 'JIP9', 'XK30', 'BriN'])
        self.case.GgObI3IHddbUmzzKy0Ur()
        res = [lambda: self.pc.hnqSw4(data='a', i=1, logisticsTypeStr='快递', applyTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_tLLsyo9wcWyBHK8e8y0v(self):
        """[质检完成]-质检服务-自提退货"""
        self.pre.operations(data=['gpvd', 'dKLc', 'JIP9', 'XK30', 'BriN'])
        self.case.tLLsyo9wcWyBHK8e8y0v()
        res = [lambda: self.pc.hnqSw4(data='a', i=2, logisticsTypeStr='自提', applyTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_bfGgREVaLQ1o2fmtJMrE(self):
        """[质检完成]-质检服务-复检"""
        self.pre.operations(data=['gpvd', 'dKLc', 'JIP9', 'XK30', 'BriN'])
        self.case.bfGgREVaLQ1o2fmtJMrE()
        res = [lambda: self.pc.BsGxx9(data='b', statusStr='待审核', applyTime='now')]
        self.assert_all(*res)
