# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.decorators import cached
from common.import_case import *


class TestUh1PpLY0(BaseCase, unittest.TestCase):
    """保卖管理|订单列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return guarantee_r.ZEvt5QWNey()
        else:
            return guarantee_p.X9UYAKxbu2B(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0GIh2R4s4U7in3JVtx4Fh(self):
        """[快速保卖]-输入物品编号-提交"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations(login='main')
        case.GIh2R4s4U7in3JVtx4Fh()
        res = [lambda: self.pc.XXAUcy(placeOrderTime='now', statusDesc='待发货')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_RhI0OGk9VBc64gZxM8di(self):
        """[快速保卖]-输入物品编号-提交并发货-快递sf"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.RhI0OGk9VBc64gZxM8di()
        res = [lambda: self.pc.XXAUcy(placeOrderTime='now', statusDesc='待收货')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_bPbBryEdt8zpTVH8jCsI(self):
        """[快速保卖]-输入物品编号-提交并发货-快递jd"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.bPbBryEdt8zpTVH8jCsI()
        res = [lambda: self.pc.XXAUcy(placeOrderTime='now', statusDesc='待收货')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_tJ9cjeZUkU75SEVnk6wT(self):
        """[快速保卖]-输入物品编号-提交并发货-快递自行邮寄"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.tJ9cjeZUkU75SEVnk6wT()
        res = [lambda: self.pc.XXAUcy(placeOrderTime='now', statusDesc='待收货')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_gh0hljAZOag10KerWd2i(self):
        """[快速保卖]-输入物品编号-提交并发货-自己送货"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.gh0hljAZOag10KerWd2i()
        res = [lambda: self.pc.XXAUcy(placeOrderTime='now', statusDesc='待取件')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_UxlDI72fkMivOA7TlGvw(self):
        """[立即发货]-快递sf"""
        self.pre.operations(data=['ekBx', 'PIGP'])
        case = self.common_operations()
        case.UxlDI72fkMivOA7TlGvw()
        res = [lambda: self.pc.XXAUcy(placeOrderTime='now', statusDesc='待取件')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_BSo6LUJtzBWcj6edgXxU(self):
        """[立即发货]-快递jd"""
        self.pre.operations(data=['ekBx', 'PIGP'])
        case = self.common_operations()
        case.BSo6LUJtzBWcj6edgXxU()
        res = [lambda: self.pc.XXAUcy(placeOrderTime='now', statusDesc='待收货')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_LPxZ1LIoEgSsdKTXRL2C(self):
        """[立即发货]-快递自行邮寄"""
        self.pre.operations(data=['ekBx', 'PIGP'])
        case = self.common_operations()
        case.LPxZ1LIoEgSsdKTXRL2C()
        res = [lambda: self.pc.XXAUcy(placeOrderTime='now', statusDesc='待收货')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_jhln7DhaP9NOD9X3azpU(self):
        """[立即发货]-自己送货"""
        self.pre.operations(data=['ekBx', 'PIGP'])
        case = self.common_operations()
        case.jhln7DhaP9NOD9X3azpU()
        res = [lambda: self.pc.XXAUcy(placeOrderTime='now', statusDesc='待收货')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_NEZ4KVsoQr6AgkUVtSBE(self):
        """[取消订单]-取消订单"""
        self.pre.operations(data=['ekBx', 'PIGP', 'XNaM'])
        case = self.common_operations()
        case.NEZ4KVsoQr6AgkUVtSBE()
        res = [lambda: self.pc.XXAUcy(placeOrderTime='now', statusDesc='已取消')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_qAhAnnHA7i5RWoR9HPAf(self):
        """[重新发货]-自己送改快递-重新发货"""
        self.pre.operations(data=['ekBx', 'PIGP', 'XNaM'])
        case = self.common_operations()
        case.qAhAnnHA7i5RWoR9HPAf()
        res = [lambda: self.pc.XXAUcy(placeOrderTime='now', statusDesc='待取件')]
        self.assert_all(*res)


class TestoygD9WEW(BaseCase, unittest.TestCase):
    """保卖管理|退货管理"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return guarantee_r.Sw9d3Jef89()
        else:
            return None

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0uMfpb3JIBZ8oaq0US9Y7(self):
        """[待退货tab]-邮寄退货-取消退货"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'xfzp'])
        case = self.common_operations(login='main')
        case.uMfpb3JIBZ8oaq0US9Y7()
        res = [lambda: self.pc.XXAUcy(placeOrderTime='now', statusDesc='已收货')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_LFI07j6GScehS4q0GPNd(self):
        """[待退货tab]-邮寄退货-更改退货方式"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'xfzp'])
        case = self.common_operations()
        case.LFI07j6GScehS4q0GPNd()
        res = [lambda: self.pc.OTblQj(applyTime='now', logisticsTypeStr='快递', i=1)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sbzcNzKjCNBmnqXBUAZP(self):
        """[待取货tab]-自提退货-取消退货"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'fNXh'])
        case = self.common_operations()
        case.sbzcNzKjCNBmnqXBUAZP()
        # res = [lambda: self.pc.XXAUcy(placeOrderTime='now', statusDesc='待退货')]
        # self.assert_all(*res)   todo 测试环境无法测试

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_WkJbfcCwi0eL85pLx7Hw(self):
        """[待取货tab]-自提退货-更改退货方式"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'fNXh'])
        case = self.common_operations()
        case.WkJbfcCwi0eL85pLx7Hw()
        res = [lambda: self.pc.XXAUcy(placeOrderTime='now', statusDesc='已收货')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_K4TenJe5ql1CTH4mOryF(self):
        """[退货已出库tab]-确认收货"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'xfzp', 'hkXQ'])
        case = self.common_operations()
        case.K4TenJe5ql1CTH4mOryF()
        res = [lambda: self.pc.XXAUcy(placeOrderTime='now', statusDesc='已收货')]
        self.assert_all(*res)


class TestqJcwlgeS(BaseCase, unittest.TestCase):
    """保卖管理|商品管理"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return guarantee_r.RETp2VmRwT()
        else:
            return guarantee_p.QDeWfd8HC8U(self.driver)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    @unittest.skip('')
    def test_0wyRAHLmyY7udk5keYovB(self):  # 缺api用例
        """[退货]-快递"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu'])
        case = self.common_operations(login='main')
        case.wyRAHLmyY7udk5keYovB()
        obj = cached('id')
        # res = [lambda: self.pc.XXAUcy(id=obj, statusStr='待销售')]
        # self.assert_all(*res)   todo 测试环境无法测试

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    @unittest.skip('')
    def test_DaKhYSFHyjQUhftVcT2W(self):  # 缺api用例
        """[退货]-自提"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu'])
        case = self.common_operations()
        case.DaKhYSFHyjQUhftVcT2W()
        # res = [lambda: self.pc.cJ1jYN(signTime='now', statusStr='待销售')]
        # self.assert_all(*res)   todo 测试环境无法测试

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_bEf5Mp7G2xinW35U9v4n(self):
        """[销售]-竞价拍机-今日参考价"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu'])
        case = self.common_operations()
        case.bEf5Mp7G2xinW35U9v4n()
        obj = cached('id')
        res = [lambda: self.pc.cJ1jYN(id=obj, statusStr='销售中', saleTypeStr='竞价拍机')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_CNaaAq7VSiFlTyYNGrfk(self):
        """[销售]-竞价拍机-自主定价"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu'])
        case = self.common_operations()
        case.CNaaAq7VSiFlTyYNGrfk()
        obj = cached('id')
        res = [lambda: self.pc.cJ1jYNt(id=obj, statusStr='销售中', saleTypeStr='竞价拍机')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_HG0qvmXGjLcEUjmJOKNy(self):
        """[销售]竞价拍机-平台定价"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu'])
        case = self.common_operations()
        case.HG0qvmXGjLcEUjmJOKNy()
        obj = cached('id')
        res = [lambda: self.pc.cJ1jYN(id=obj, statusStr='待平台确认', saleTypeStr='竞价拍机')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sUkAYaxto6tXXFUu1tyJ(self):
        """[销售]-第三方同售-今日参考价"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu'])
        case = self.common_operations()
        case.sUkAYaxto6tXXFUu1tyJ()
        obj = cached('id')
        res = [lambda: self.pc.cJ1jYN(id=obj, statusStr='销售中', saleTypeStr='同售')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_IpoZ907QoA7qXNUfox4T(self):
        """[销售]-第三方同售-自主定价"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu'])
        case = self.common_operations()
        case.IpoZ907QoA7qXNUfox4T()
        obj = cached('id')
        res = [lambda: self.pc.cJ1jYN(id=obj, statusStr='销售中', saleTypeStr='同售')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_uojb7cbGSWgC8zL5aCWL(self):
        """[销售]-第三方同售-平台定价"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu'])
        case = self.common_operations()
        case.uojb7cbGSWgC8zL5aCWL()
        obj = cached('id')
        res = [lambda: self.pc.cJ1jYN(id=obj, statusStr='待平台确认', saleTypeStr='同售')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_ecdR9lamw6zn0y9vyNRF(self):
        """[取消销售]-取消销售"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO'])
        case = self.common_operations()
        case.ecdR9lamw6zn0y9vyNRF()
        obj = cached('id')
        res = [lambda: self.guarantee.goods_list(id=obj, statusStr='待销售', saleTypeStr='竞价拍机')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_LrCC4svDp0JANhnDhJZH(self):
        """[改价]-改价"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO'])
        case = self.common_operations()
        case.LrCC4svDp0JANhnDhJZH()
        obj = cached('id')
        res = [lambda: self.guarantee.goods_list(id=obj, signTime='now', statusStr='销售中', saleTypeStr='竞价拍机')]
        self.assert_all(*res)


if __name__ == '__main__':
    unittest.main()
