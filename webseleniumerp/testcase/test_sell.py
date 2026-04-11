# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.decorators import cached
from common.import_case import *


class TestpmeNITg3(BaseCase, unittest.TestCase):
    """商品销售|销售售后管理|销售售后处理"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return sell_r.EPSnRVHPCS()
        else:
            return sell_p.SHoWS2sIDk6(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0kveY9vSZiCveNHGRKZ5u(self):
        """[销售售后处理]-仅退配件未收货"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        case = self.common_operations(login='main')
        case.kveY9vSZiCveNHGRKZ5u()
        res = [lambda: self.pc.rv5p3j(data='a', saleTypeStr='仅退配件', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_w2XcfZ42REixTHsF0D6w(self):
        """[销售售后处理]-仅退配件已收货"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        case = self.common_operations()
        case.w2XcfZ42REixTHsF0D6w()
        res = [lambda: self.pc.rv5p3j(saleTypeStr='仅退配件', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_DjkghfK5et2Z3KvN6d3n(self):
        """[销售售后处理]-退货-邮寄已收货"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        case = self.common_operations()
        case.DjkghfK5et2Z3KvN6d3n()
        res = [lambda: self.pc.rv5p3j(data='a', saleTypeStr='退货', createTime='now')]
        self.assert_all(*res)


class TestukuIKU5Q(BaseCase, unittest.TestCase):
    """商品销售|销售管理|销售上架"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return sell_r.JhWPhXjKbY()
        else:
            return sell_p.JTc35i3PMbz(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0kiSivAHj3Vab5m78JpuW(self):
        """[添加物品]-销售上架"""
        self.pre.operations(data=['ekBx', 'wQ7u'])
        case = self.common_operations(login='main')
        case.kiSivAHj3Vab5m78JpuW()
        res = [lambda: self.pc.x9ZGyS(typeRes='上架', orderStateStr='未完结', shelfTime='now')]
        self.assert_all(*res)


class TestDw5VrDAz(BaseCase, unittest.TestCase):
    """商品销售|销售管理|待接收物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return sell_r.BLHu01CRzs()
        else:
            return sell_p.EHPPgSmlpeU(self.driver)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0Hu4K5bokoTCxa0RXNIan(self):
        """[接收]-全部物品接收"""
        self.pre.operations(data=['ekBx', 'DT6i'])
        case = self.common_operations(login='special')
        case.Hu4K5bokoTCxa0RXNIan()
        res = [lambda: self.pc.handover_record(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_hnFxpME7kKdGGlUyloly(self):
        """[扫码精确接收]-单个物品接收"""
        self.pre.operations(data=['ekBx', 'DT6i'])
        case = self.common_operations()
        case.hnFxpME7kKdGGlUyloly()
        res = [lambda: self.pc.handover_record(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_TjFLeMzswpHGeziySvFD(self):
        """[搜索]-imei查询"""
        case = self.common_operations()
        case.TjFLeMzswpHGeziySvFD()
        obj = cached('imei')
        res = [lambda: self.pc.WlmTfF(imei=obj, deliveryTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_gRGlwNpXR7APhkJ0lUaA(self):
        """[搜索]-date查询"""
        case = self.common_operations()
        case.gRGlwNpXR7APhkJ0lUaA()
        res = [lambda: self.pc.WlmTfF(deliveryTime='now')]
        self.assert_all(*res)


class TestkeoF0fMP(BaseCase, unittest.TestCase):
    """商品销售|销售管理|销售中物品列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return sell_r.G4HwM9EjFQ()
        else:
            return sell_p.CR6FpKLnxxS(self.driver)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0PJcVirkG5vjAdGnxgXpV(self):
        """[全部tab]销售类型上架-修改销售信息-导入添加物品修改"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'In7Z'])
        case = self.common_operations(login='main')
        case.PJcVirkG5vjAdGnxgXpV()
        res = [lambda: self.pc.x9ZGyS(createTime='now', typeRes='上架')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_rrBrdjBX494MEDd1GeWh(self):
        """[全部tab]-销售类型上架-修改销售状态-普通快递-未收款-确认销售"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'In7Z'])
        case = self.common_operations()
        case.rrBrdjBX494MEDd1GeWh()
        res = [lambda: self.pc.bfCKxO(articlesStateStr='已销售', saleTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_htCvd4xY1c0JleADicMq(self):
        """[全部tab]-销售类型上架-修改销售状态-普通快递-已收款-确认销售"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'In7Z'])
        case = self.common_operations()
        case.htCvd4xY1c0JleADicMq()
        res = [lambda: self.pc.bfCKxO(articlesStateStr='已销售', saleTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_zGRElY85yjm7F6rhrCx3(self):
        """[全部tab]-销售类型上架-下架-确认下架"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'In7Z'])
        case = self.common_operations()
        case.zGRElY85yjm7F6rhrCx3()
        res = [lambda: self.pc.x9ZGyS(createTime='now', typeRes='上架')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_WWNIdAfb7nswviGGMLKI(self):
        """[销售中tab]-销售类型上架-批量下架-确认下架"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'In7Z'])
        case = self.common_operations()
        case.WWNIdAfb7nswviGGMLKI()
        res = [lambda: self.pc.x9ZGyS(createTime='now', typeRes='上架')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_ooNlz00UWyMoRIn0Nq8E(self):
        """[销售中tab]-销售类型预售-更改销售状态-确认销售"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'In7Z'])
        case = self.common_operations()
        case.ooNlz00UWyMoRIn0Nq8E()
        res = [lambda: self.pc.x9ZGyS(createTime='now', typeRes='上架')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_bLvgAVe5W8UHtELDxMfB(self):
        """[销售中tab]-销售类型铺货-铺货退回"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'In7Z'])
        case = self.common_operations()
        case.bLvgAVe5W8UHtELDxMfB()
        res = [lambda: self.pc.x9ZGyS(createTime='now', typeRes='上架')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_asfN7GBuig1lB2JTFGbz(self):
        """[销售中tab]-销售类型铺货-铺货销售出库"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'In7Z'])
        case = self.common_operations()
        case.asfN7GBuig1lB2JTFGbz()
        res = [lambda: self.pc.x9ZGyS(createTime='now', typeRes='上架')]
        self.assert_all(*res)


class TestzAYm14Ob(BaseCase, unittest.TestCase):
    """商品销售|销售管理|待销售物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return sell_r.K840BKXUBB()
        else:
            return sell_p.E2yktvttmCT(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0BjtCW4zAlmHFf4hnEsyK(self):
        """销售预售出库"""
        self.pre.operations(data=['ekBx', 'wQ7u'])
        case = self.common_operations(login='main')
        case.BjtCW4zAlmHFf4hnEsyK()
        res = [lambda: self.pc.x9ZGyS(createTime='now', typeRes='预售')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_psGTQePHRPXOVLvXlZU5(self):
        """[出库]-销售出库"""
        self.pre.operations(data=['ekBx', 'wQ7u'])
        case = self.common_operations()
        case.psGTQePHRPXOVLvXlZU5()
        res = [lambda: self.pc.bfCKxO(articlesStateStr='已销售', saleTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_aMAnXMswO97RRUy2WDp5(self):
        """[出库]-销售铺货出库"""
        self.pre.operations(data=['ekBx', 'wQ7u'])
        case = self.common_operations()
        case.aMAnXMswO97RRUy2WDp5()
        res = [lambda: self.pc.x9ZGyS(createTime='now', typeRes='铺货')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_iqOJswY1Y3kNWO1jXmAc(self):
        """[上架]-销售上架"""
        self.pre.operations(data=['ekBx', 'wQ7u'])
        case = self.common_operations()
        case.iqOJswY1Y3kNWO1jXmAc()
        res = [lambda: self.pc.x9ZGyS(createTime='now', typeRes='上架')]
        self.assert_all(*res)


class Testf4lJIPzr(BaseCase, unittest.TestCase):
    """商品销售|销售管理|销售中订单列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return sell_r.WS1s1EqRY2()
        else:
            return None


class TesttsUzlwgV(BaseCase, unittest.TestCase):
    """商品销售|销售管理|已销售订单列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return sell_r.A87tiuwVRI()
        else:
            return None


class Testq3F9c8Bf(BaseCase, unittest.TestCase):
    """商品销售|销售管理|已销售物品列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return sell_r.H48MfRLnYT()
        else:
            return sell_p.A16z5xHZdDb(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0J6LQWn0szGuyNJ0UuFq8(self):
        """[销售售后]-销售售后处理-调价"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        case = self.common_operations(login='main')
        case.J6LQWn0szGuyNJ0UuFq8()
        res = [lambda: self.pc.rv5p3j(saleTime='now', saleTypeStr='调价', articlesStatusStr='已销售')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_JjVcGp9jSl8TI9nj2xVw(self):
        """[销售售后]-销售售后处理-仅退配件未收货"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        case = self.common_operations()
        case.JjVcGp9jSl8TI9nj2xVw()
        res = [lambda: self.pc.rv5p3j(data='a', createTime='now', saleTypeStr='仅退配件')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_XfB5KTH8vn0wDw6a9KJQ(self):
        """[销售售后]-销售售后处理-仅退配件已收货"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        case = self.common_operations()
        case.XfB5KTH8vn0wDw6a9KJQ()
        res = [lambda: self.pc.rv5p3j(data='a', createTime='now', saleTypeStr='仅退配件')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_mZBEQDHNTjeSAXBWx11z(self):
        """[销售售后]-销售售后处理-退货-邮寄未收货"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        case = self.common_operations()
        case.mZBEQDHNTjeSAXBWx11z()
        res = [lambda: self.pc.rv5p3j(data='a', createTime='now', saleTypeStr='退货')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_QBOIk1dLbtE83J6puWEy(self):
        """[销售售后]-销售售后处理-退货-邮寄已收货"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        case = self.common_operations()
        case.QBOIk1dLbtE83J6puWEy()
        res = [lambda: self.pc.rv5p3j(saleTime='now', saleTypeStr='仅退款', articlesStatusStr='已销售')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_gVnbM599DimecmAZ6Xlg(self):
        """[销售售后]-销售售后处理-仅退款"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ'])
        case = self.common_operations()
        case.gVnbM599DimecmAZ6Xlg()
        res = [lambda: self.pc.rv5p3j(saleTime='now', saleTypeStr='仅退款', articlesStatusStr='已销售')]
        self.assert_all(*res)


class TestMMFRhZRZ(BaseCase, unittest.TestCase):
    """商品销售|销售售后管理|销售售后列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return sell_r.AHdZ4hW3TP()
        else:
            return sell_p.YRaemFF1a0b(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0ebhsQ41HitCvjEsvMz0G(self):
        """[更新售后状态]-换货-普通快递-确认出库"""
        self.pre.operations(data=['ekBx', 'ekBx', 'wQ7u', 'HRTZ', 'jw4U'])
        case = self.common_operations(login='main')
        case.ebhsQ41HitCvjEsvMz0G()
        res = [lambda: self.pc.rv5p3j(updateTime='now', saleTypeStr='换货', articlesStatusStr='待分货')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_GDdc1h1eADXbjk8ujR60(self):
        """[更新售后状态]-仅退配件-确认入库"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ', 'NIMm'])
        case = self.common_operations()
        case.GDdc1h1eADXbjk8ujR60()
        res = [lambda: self.pc.rv5p3j(updateTime='now', saleTypeStr='仅退配件', articlesStatusStr='已销售')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_pt4gIHCRgdVZv3FGKFVq(self):
        """[更新售后状态]-返修-普通快递-确认出库"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ', 'jw4U'])
        case = self.common_operations()
        case.pt4gIHCRgdVZv3FGKFVq()
        res = [lambda: self.pc.rv5p3j(updateTime='now', saleTypeStr='返修', articlesStatusStr='已销售', )]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_xSQE9e6LbvvilOg9OMsy(self):
        """[更新售后状态]-退货退款-无平台售后罚款"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ', 'jw4U'])
        case = self.common_operations()
        case.xSQE9e6LbvvilOg9OMsy()
        res = [lambda: self.pc.rv5p3j(updateTime='now', saleTypeStr='退货退款', articlesStatusStr='待分货')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_GdXpXPawmTeBaOha9VUo(self):
        """[更新售后状态]-拒退退回-普通快递-确认出库"""
        self.pre.operations(data=['ekBx', 'wQ7u', 'HRTZ', 'jw4U'])
        case = self.common_operations()
        case.GdXpXPawmTeBaOha9VUo()
        res = [lambda: self.pc.rv5p3j(updateTime='now', saleTypeStr='拒退退回', articlesStatusStr='已销售')]
        self.assert_all(*res)


class TestH7mJOyQg(BaseCase, unittest.TestCase):
    """商品销售|客户管理"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return sell_r.UkltE3HM8G()
        else:
            return None


class TestUX9Kz0FM(BaseCase, unittest.TestCase):
    """商品销售|数据统计"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return sell_r.LwtGu0p14m()
        else:
            return None


if __name__ == '__main__':
    unittest.main()
