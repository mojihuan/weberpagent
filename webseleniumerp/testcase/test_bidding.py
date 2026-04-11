# coding: utf-8
import unittest

from common.decorators import cached
from common.base_case import BaseCase
from common.mini_base_case import MiniBaseCase
from common.decorators import test_mode_handler
from common.import_case import *


@test_mode_handler(bidding_r.DuLudPwrAY, None)
class TestehTofQ2A(MiniBaseCase):
    """拍机小程序|竞拍"""

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_0ooh8smtEbSrtOuUNqjJa(self):
        """[竞拍]暗拍-出价"""
        # self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'naBM','xNAC'])
        self.pre.operations(data=['spKR', '@AB11', 'cCQZ', 'LLx3', 'CqTl', 'HfWO'])
        self.wait_default()
        self.case.ooh8smtEbSrtOuUNqjJa()
        obj = cached('articlesNo')
        obj_2 = cached('bidPrice')
        res = [lambda: self.pc.jEJvoj(headers='camera', data='a', autoBidPrice=obj_2, articlesNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_YvnI8JFogJKDJyevymIw(self):
        """[竞拍]暗拍-修改价格"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'naBM', 'xNAC', 'OAqF'])
        self.wait_default()
        self.case.YvnI8JFogJKDJyevymIw()
        obj = cached('articlesNo')
        obj_2 = cached('bidPrice')
        res = [lambda: self.pc.jEJvoj(headers='camera', data='a', autoBidPrice=obj_2, articlesNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_SAnRSrq1160pZali4yIf(self):
        """[竞拍]直拍-出价"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU'])
        self.wait_default()
        self.case.SAnRSrq1160pZali4yIf()
        obj = cached('articlesNo')
        obj_2 = cached('bidPrice')
        res = [lambda: self.pc.jEJvoj(headers='camera', autoBidPrice=obj_2, articlesNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_MdM1073dpYo2D4xRtbN4(self):
        """[竞拍]直拍-改价"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB'])
        self.wait_default()
        self.case.MdM1073dpYo2D4xRtbN4()
        obj = cached('articlesNo')
        obj_2 = cached('bidPrice')
        res = [lambda: self.pc.jEJvoj(headers='camera', autoBidPrice=obj_2, articlesNo=obj)]
        self.assert_all(*res)


@test_mode_handler(bidding_r.RQTYlCj2X9, None)
class TestqK0kgBw7(MiniBaseCase):
    """拍机小程序|我的"""

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_0Ly41cUm9R4N75FqquckG(self):
        """[待发货]直拍-改自提"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB'])
        self.wait_default()
        self.case.Ly41cUm9R4N75FqquckG()
        obj = cached('articlesNo')
        res = [lambda: self.pc.Alrd2T(headers='camera', i=3, articlesNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @unittest.skip('没按最新的数据排序，测不了')
    def test_wOMYzQailIlwneqp3YqQ(self):
        """[待收货]直拍-改邮寄"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv'])
        self.case.wOMYzQailIlwneqp3YqQ()
        obj = cached('articlesNo')
        res = [lambda: self.pc.Alrd2T(headers='camera', i=2, articlesNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_c71cLTyRLuY4tAw5OBlV(self):
        """[待收货]直拍-确认收货"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv'])
        self.case.c71cLTyRLuY4tAw5OBlV()
        obj = cached('articlesNo')
        res = [lambda: self.pc.Alrd2T(headers='camera', i=4, articlesNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_aVXdmJVbK9wjjXJCBjst(self):
        """[已收货]直拍-申请售后"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm'])
        self.case.aVXdmJVbK9wjjXJCBjst()
        res = [lambda: self.pc.bijXOp(headers='camera', applyTime='now', afterDesc='售后', afterStatusStr='线上审核', tradeCategoryStr='直拍')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_BPBCQmGYcAgtwQuFgbaO(self):
        """[可补差]直拍-接收补差"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 'NiF8'])
        self.case.BPBCQmGYcAgtwQuFgbaO()
        obj = cached('id')
        res = [lambda: self.pc.Alrd2T(data='c', i=[5], headers='camera', id=obj, afterStatus=5)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_XFuplSfvhfY3pPN3q60t(self):
        """[可补差]直拍-拒绝补差"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 'NiF8'])
        self.case.XFuplSfvhfY3pPN3q60t()
        obj = cached('id')
        res = [lambda: self.pc.Alrd2T(data='c', i=[7], headers='camera', id=obj, afterStatus=7)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_jw92LPqmCSgtAgFxlGVO(self):
        """[可补差]直拍-结束售后"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 'NiF8'])
        self.case.jw92LPqmCSgtAgFxlGVO()
        obj = cached('id')
        res = [lambda: self.pc.Alrd2T(i=4, headers='camera', id=obj, articlesStatus=4)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_UfKqlNZ2jFR6rFZUiH8v(self):
        """[待寄回]直拍-去发货-预约上门"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 's522'])
        self.case.UfKqlNZ2jFR6rFZUiH8v()
        obj = cached('id')
        res = [lambda: self.pc.fulfillment_bijXOp(id=obj, afterStatus=10, buyerReturnModeStr='预约上门', afterStatusStr='待接收', tradeCategoryStr='直拍')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_fujEfOlXIMCY3oXrDNVd(self):
        """[待寄回]直拍-去发货-自叫物流"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 's522'])
        self.case.fujEfOlXIMCY3oXrDNVd()
        obj = cached('id')
        res = [lambda: self.pc.fulfillment_bijXOp(id=obj, afterStatus=10, buyerReturnModeStr='自叫物流', afterStatusStr='待接收', tradeCategoryStr='直拍')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_ZLMjQKplgxx6Krvopxg7(self):
        """[待寄回]直拍-去发货-自行送货"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 's522'])
        self.case.ZLMjQKplgxx6Krvopxg7()
        obj = cached('id')
        res = [lambda: self.pc.fulfillment_bijXOp(id=obj, afterStatus=10, buyerReturnModeStr='自行送货', afterStatusStr='待接收', tradeCategoryStr='直拍')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_J62o1YNEgyQUVrUfzEs3(self):
        """[可补差]-直拍-复检审核-接收补差"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 's522', 'GJ8B', 'EuOa', 'UXXj', 'KXoh', 'trt4'])
        self.case.J62o1YNEgyQUVrUfzEs3()
        obj = cached('id')
        res = [lambda: self.pc.Alrd2T(data='c', i=[5], headers='camera', id=obj, afterStatus=5)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_zd1jfkpdiIAy1G9RVrIq(self):
        """[可补差]-直拍-复检审核-拒绝补差"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 's522', 'GJ8B', 'EuOa', 'UXXj', 'KXoh', 'trt4'])
        self.case.zd1jfkpdiIAy1G9RVrIq()
        obj = cached('id')
        res = [lambda: self.pc.Alrd2T(data='c', i=[7], headers='camera', id=obj, afterStatus=7)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_G8mzJPJPK9gNaeIm9U7P(self):
        """[可补差]-直拍-复检审核-结束售后"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 'zEPV'])
        self.case.G8mzJPJPK9gNaeIm9U7P()
        obj = cached('id')
        res = [lambda: self.pc.Alrd2T(data='c', i=[9], headers='camera', id=obj, afterStatus=9)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_xYF6VMP7gVBubHHeRksW(self):
        """[待申诉]-直拍-我要申诉"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 'zEPV'])
        self.case.xYF6VMP7gVBubHHeRksW()
        obj = cached('id')
        res = [lambda: self.pc.Alrd2T(data='c', i=[4], headers='camera', id=obj, afterStatus=4)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_qy2BOyYcjRZCMRxmI1HJ(self):
        """[待申诉]-直拍-结束售后"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 'zEPV'])
        self.case.qy2BOyYcjRZCMRxmI1HJ()
        obj = cached('id')
        res = [lambda: self.pc.Alrd2T(data='c', i=[4], headers='camera', id=obj, afterStatus=4)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_GUCbnylR1i5xvkHG84Lq(self):
        """[可补差]-直拍-平台申诉通过-接收补差"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 'zEPV', 'INjZ', 'r1GJ'])
        self.case.GUCbnylR1i5xvkHG84Lq()
        obj = cached('id')
        res = [lambda: self.pc.Alrd2T(data='c', i=[5], headers='camera', id=obj, afterStatus=5)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_HOPKwhJtyDRx8zxTdh7S(self):
        """[可补差]-直拍-平台申诉通过-拒绝补差"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 'zEPV', 'INjZ', 'r1GJ'])
        self.case.HOPKwhJtyDRx8zxTdh7S()
        obj = cached('id')
        res = [lambda: self.pc.Alrd2T(data='c', i=[7], headers='camera', id=obj, afterStatus=7)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_SXKFMEeSoPN01IP9Lwlp(self):
        """[可补差]-直拍-平台申诉通过-结束售后"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 'zEPV', 'INjZ', 'r1GJ'])
        self.case.SXKFMEeSoPN01IP9Lwlp()
        obj = cached('id')
        res = [lambda: self.pc.Alrd2T(data='c', i=[9], headers='camera', id=obj, afterStatus=9)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_aSUFM1IQg6Qn99K4na0b(self):
        """[待寄回]-直拍-平台申诉通过-去发货-预约上门"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 'zEPV', 'INjZ', 'mw4N'])
        self.case.aSUFM1IQg6Qn99K4na0b()
        obj = cached('id')
        res = [lambda: self.pc.fulfillment_bijXOp(id=obj, afterStatus=10, buyerReturnModeStr='预约上门', afterStatusStr='待接收', tradeCategoryStr='直拍')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_nKqLT6q8XX9QYiJ26jms(self):
        """[待寄回]-直拍-平台申诉通过-去发货-自叫物流"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 'zEPV', 'INjZ', 'mw4N'])
        self.case.nKqLT6q8XX9QYiJ26jms()
        obj = cached('id')
        res = [lambda: self.pc.fulfillment_bijXOp(id=obj, afterStatus=10, buyerReturnModeStr='自叫物流', afterStatusStr='待接收', tradeCategoryStr='直拍')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    def test_FFK90vpcso9aPNnQyAWS(self):
        """[待寄回]-直拍-平台申诉通过-去发货-自行送货"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 'zEPV', 'INjZ', 'mw4N'])
        self.case.FFK90vpcso9aPNnQyAWS()
        obj = cached('id')
        res = [lambda: self.pc.fulfillment_bijXOp(id=obj, afterStatus=10, buyerReturnModeStr='自行送货', afterStatusStr='待接收', tradeCategoryStr='直拍')]
        self.assert_all(*res)


if __name__ == '__main__':
    unittest.main()
