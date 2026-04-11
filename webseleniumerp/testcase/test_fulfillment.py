# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.decorators import cached
from common.import_case import *


class TestJzLSCg8n(BaseCase, unittest.TestCase):
    """运营中心|待报价物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return fulfillment_r.Qc3N4qmsX7()
        else:
            return fulfillment_p.NdYPoyxA7Ut(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0h86Q9EJJuji9EAcwmnZd(self):
        """[商品报价]"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'Q7Xz', 'KnkQ'])
        case = self.common_operations(login='main')
        case.commodity_quotes()
        res = [lambda: self.pc.scDt2J(reportTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_HdVZdnVgjfeOetZQxl9C(self):
        """[重新报价]"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'Q7Xz', 'KnkQ', 'q9eJ'])
        case = self.common_operations()
        case.HdVZdnVgjfeOetZQxl9C()
        res = [lambda: self.pc.scDt2J(reportTime='now')]
        self.assert_all(*res)


class TestxJ1pj3T4(BaseCase, unittest.TestCase):
    """运营中心|质检管理"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return fulfillment_r.LCfJXeE7Mf()
        else:
            return fulfillment_p.HBW5NSrtWxI(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0jN6h3HHrblYl6XRDrjRp(self):
        """[待领取物品tab]-批量接收"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm'])
        case = self.common_operations(login='main')
        case.jN6h3HHrblYl6XRDrjRp()
        res = [lambda: self.pc.BsGxx9(data='a', distributorTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_EqKnTwPFi7SMTAPIanzC(self):
        """[待领取物品tab]-批量接收"""
        self.pre.operations(data=['spKR', '@AB11', 'cCQZ'])
        case = self.common_operations()
        case.EqKnTwPFi7SMTAPIanzC()
        res = [lambda: self.pc.BsGxx9(headers='camera', data='a', distributorTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_CLRwZ9FXvcE5gCYCPdSF(self):
        """[待领取物品tab]-直拍-平台申诉通过-批量接收"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 'zEPV', 'INjZ', 'mw4N', 'GJ8B', 'NCSB'])
        case = self.common_operations()
        case.CLRwZ9FXvcE5gCYCPdSF()
        res = [lambda: self.pc.BsGxx9(data='a', distributorTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_knHZe0CfAp1HXSNNW4nG(self):
        """[待领取物品tab]-质检服务-批量接收"""
        self.pre.operations(data=['gpvd', 'dKLc', 'JIP9'])
        case = self.common_operations()
        case.knHZe0CfAp1HXSNNW4nG()
        res = [lambda: self.pc.BsGxx9(data='a', distributorTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_rqPmiTtsuecNOe8Qa0FW(self):
        """[质检中物品tab]-提交质检结果"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9'])
        case = self.common_operations()
        case.rqPmiTtsuecNOe8Qa0FW()
        res = [lambda: self.pc.BsGxx9(data='c', qualityFinishTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_oKZEC3OeI0tWc8WLWpY3(self):
        """[质检中物品tab]-提交质检结果"""
        self.pre.operations(data=['spKR', '@AB11', 'cCQZ', 'LLx3'])
        case = self.common_operations()
        case.oKZEC3OeI0tWc8WLWpY3()
        res = [lambda: self.pc.BsGxx9(headers='camera', data='c', qualityFinishTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_TJXWHGYpzVeCuC3cZjrH(self):
        """[质检中物品tab]-质检服务-提交质检结果"""
        self.pre.operations(data=['gpvd', 'dKLc', 'JIP9', 'XK30'])
        case = self.common_operations()
        case.TJXWHGYpzVeCuC3cZjrH()
        res = [lambda: self.pc.BsGxx9(data='c', qualityFinishTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_zBKyvA1lFKeRAKK0WXqg(self):
        """[质检中物品tab]-提交质检结果-不传图"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9'])
        case = self.common_operations()
        case.zBKyvA1lFKeRAKK0WXqg()
        res = [lambda: self.pc.BsGxx9(data='c', qualityFinishTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_eL32NtimAkRJKwnmSauo(self):
        """[重验申请tab]-审核通过"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', '@AB9'])
        case = self.common_operations()
        case.eL32NtimAkRJKwnmSauo()
        res = [lambda: self.pc.BsGxx9(data='b', reviewTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_d6dbbDv54duJQhN6VKNl(self):
        """[重验申请tab]-审核拒绝"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', '@AB9'])
        case = self.common_operations()
        case.d6dbbDv54duJQhN6VKNl()
        res = [lambda: self.pc.BsGxx9(data='b', reviewTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_CLHIAAqc0GcsqVloSnnm(self):
        """[已质检物品tab]-修改报告"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu'])
        case = self.common_operations()
        case.CLHIAAqc0GcsqVloSnnm()
        res = [lambda: self.pc.BsGxx9(data='c', qualityFinishTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_M6cvV0SyzVBbb2kyvAYl(self):
        """[质检中物品tab]-未验移交"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9'])
        case = self.common_operations()
        case.M6cvV0SyzVBbb2kyvAYl()
        res = [lambda: self.pc.BsGxx9(distributorTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_RXoB3Agr98ilYZlNb5FZ(self):
        """[质检中物品tab]-无需质检"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9'])
        case = self.common_operations()
        case.RXoB3Agr98ilYZlNb5FZ()
        res = [lambda: self.pc.aY387y(j=1, status=5)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_y203S2h47mnZp3O3L8J9(self):  # todo 差异图未上传不知道怎么造数据
        """[商品图拍摄tab]-拍商品图"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'Rbd1'])
        case = self.common_operations()
        case.y203S2h47mnZp3O3L8J9()
        # res = [lambda: self.pc.BsGxx9(data='d', goodsImageStatusStr='已上传')]
        # self.assert_all(*res)  

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_eoidlhlWuLRCRQL3uNIN(self):
        """[待领取物品tab]-直拍-实物复检-批量接收"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 's522', 'Y61c', 'EuOa'])
        case = self.common_operations()
        case.eoidlhlWuLRCRQL3uNIN()
        res = [lambda: self.pc.BsGxx9(data='a', distributorTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_NGkklZ12l2IiB7qVbQxE(self):
        """[质检中物品tab]-直拍-实物复检-提交质检结果"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 's522', 'GJ8B', 'EuOa', 'UXXj'])
        case = self.common_operations()
        case.NGkklZ12l2IiB7qVbQxE()
        res = [lambda: self.pc.BsGxx9(data='c', qualityFinishTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_JO1O4Cu3NqUy2eHg71Sb(self):
        """[质检中物品tab]-直拍-平台申诉通过-提交质检结果"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 'zEPV', 'INjZ', 'mw4N', 'GJ8B', 'NCSB', 'FYzF'])
        case = self.common_operations()
        case.JO1O4Cu3NqUy2eHg71Sb()
        res = [lambda: self.pc.BsGxx9(data='c', qualityFinishTime='now')]
        self.assert_all(*res)


class TestgAtlCQiv(BaseCase, unittest.TestCase):
    """运营中心|退货管理"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return fulfillment_r.PrpdxJpu3k()
        else:
            return fulfillment_p.AptiDaFra0u(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0BBIpXJ7xM3RSMC8Gh7uI(self):
        """[待退货tab]-物品明细-邮寄退货出库"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'xfzp'])
        case = self.common_operations(login='main')
        case.BBIpXJ7xM3RSMC8Gh7uI()
        res = [lambda: self.pc.hnqSw4(data='a', i=3, outboundTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_oUHwogXGLEfPAQHosTJh(self):
        """[待退货tab]-物品明细-京东邮寄-退货出库"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'xfzp'])
        case = self.common_operations()
        case.oUHwogXGLEfPAQHosTJh()
        res = [lambda: self.pc.hnqSw4(data='a', i=3, outboundTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_YPSRB7uVXJNfxkNAC56C(self):
        """[待退货tab]-物品明细-导出信息"""
        case = self.common_operations()
        case.YPSRB7uVXJNfxkNAC56C()
        res = [lambda: self.pc.T241Se(state=2, name='送修单列表导出', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_zdM1FoDt6AVwrkGz7nPX(self):
        """[待取货tab]-自提退货出库"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'fNXh'])
        case = self.common_operations()
        case.zdM1FoDt6AVwrkGz7nPX()
        res = [lambda: self.pc.hnqSw4(data='a', i=4, outboundTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_HfHJxVye6T1NL8mbDo1m(self):
        """[待取货tab]-物品明细-导出信息"""
        case = self.common_operations()
        case.HfHJxVye6T1NL8mbDo1m()
        res = [lambda: self.pc.T241Se(state=2, name='送修单列表导出', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_LvlPCF0VS3XPOtflUi4p(self):
        """[退货已出库tab]-批次明细-更改物流"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'xfzp', 'hkXQ'])
        case = self.common_operations()
        case.LvlPCF0VS3XPOtflUi4p()
        res = [lambda: self.pc.hnqSw4(data='批次明细列表', i=3, outboundTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_IYhXWSUAsFy2lcEEwgCS(self):
        """[退货已出库tab]-物品明细-更改物流"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'xfzp', 'hkXQ'])
        case = self.common_operations()
        case.IYhXWSUAsFy2lcEEwgCS()
        res = [lambda: self.pc.hnqSw4(data='a', i=3, outboundTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_WhYRYd8hMok6D2xnSAXd(self):
        """[退货已出库tab]-批次明细-导出信息"""
        case = self.common_operations()
        case.WhYRYd8hMok6D2xnSAXd()
        res = [lambda: self.pc.T241Se(state=2, name='送修单列表导出', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_tuxJhExUT8EwcOQ2r0od(self):
        """[已退货tab]-物品明细-导出信息"""
        case = self.common_operations()
        case.tuxJhExUT8EwcOQ2r0od()
        res = [lambda: self.pc.T241Se(state=2, name='送修单列表导出', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_bohSUkZbWonpQxFCek1n(self):
        """[已取消tab]-输入正确查询自提码-自提退货出库"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'xfzp', 'hkXQ', '@AB10'])
        case = self.common_operations()
        case.bohSUkZbWonpQxFCek1n()
        res = [lambda: self.pc.hnqSw4(data='a', i=4, outboundTime='now')]
        self.assert_all(*res)


class TestEjuYLOpj(BaseCase, unittest.TestCase):
    """运营中心|收货入库"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return fulfillment_r.NDafRJuz1F()
        else:
            return fulfillment_p.Bk9greLQOjM(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0JdFjESShYyLExa0NBUR4(self):
        """[收货入库]上传视频入库"""
        self.pre.operations(data=['spKR', 'VyCN'])
        case = self.common_operations(login='main')
        case.JdFjESShYyLExa0NBUR4()
        res = [lambda: self.pc.dKWl3w(signTime='now', statusDesc='已收货')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_zd9DnAScYux2tHzIRjJT(self):
        """[收货入库]拍机-上传视频入库"""
        self.pre.operations(data=['spKR', '@AB11'])
        case = self.common_operations()
        case.zd9DnAScYux2tHzIRjJT()
        res = [lambda: self.pc.dKWl3w(headers='camera', signTime='now', statusDesc='已收货')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_IYU1aVy8aH3qWm62ZtJp(self):
        """[收货入库]质检服务-上传视频入库"""
        self.pre.operations(data=['gpvd', 'dKLc'])
        case = self.common_operations()
        case.IYU1aVy8aH3qWm62ZtJp()
        res = [lambda: self.pc.dKWl3w(signTime='now', statusDesc='已收货')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_cLMkHCV4xjRALsu6yfP5(self):
        """[收货入库]无imei-已打印"""
        self.pre.operations(data=['spKR', 'VyCN'])
        case = self.common_operations()
        case.cLMkHCV4xjRALsu6yfP5()
        res = [lambda: self.pc.dKWl3w(signTime='now', statusDesc='已收货')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_SICaUhaAsw3CqQfqENpV(self):
        """[收货入库]在线录制包裹视频"""
        self.pre.operations(data=['spKR', 'VyCN'])
        case = self.common_operations()
        case.SICaUhaAsw3CqQfqENpV()
        res = [lambda: self.pc.dKWl3w(signTime='now', statusDesc='已收货')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_I6mCUqWhps2B27kclbkx(self):
        """[收货入库]物流单号添加物品"""
        self.pre.operations(data=['spKR', 'VyCN'])
        case = self.common_operations()
        case.I6mCUqWhps2B27kclbkx()
        res = [lambda: self.pc.dKWl3w(signTime='now', statusDesc='已收货')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_A9k63GOKEgezsR7PmpCc(self):
        """[收货入库]批量修改imei"""
        self.pre.operations(data=['spKR', 'VyCN'])
        case = self.common_operations()
        case.A9k63GOKEgezsR7PmpCc()
        res = [lambda: self.pc.dKWl3w(signTime='now', statusDesc='已收货')]
        self.assert_all(*res)


class TestQhuEBwPg(BaseCase, unittest.TestCase):
    """运营中心|订单管理"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return fulfillment_r.I7YRIi2RnR()
        else:
            return fulfillment_p.LULEvBu3aZW(self.driver)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0zHywULjwAZbQYE4tEyui(self):
        """[快速保卖]-选择物品-确定"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations(login='main')
        case.zHywULjwAZbQYE4tEyui()
        res = [lambda: self.pc.dKWl3w(placeOrderTime='now', statusDesc='已收货')]
        self.assert_all(*res)


class TestiL1jfEji(BaseCase, unittest.TestCase):
    """运营中心|物品出库"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return fulfillment_r.Pzx3xU1ulY()
        else:
            return fulfillment_p.WpnqXnFPR1X(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0YtFzTr37KoEb6ObJhKgF(self):
        """[销售出库]-直拍-顺丰快递-销售出库"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB'])
        self.wait_default()
        case = self.common_operations(login='main')
        case.YtFzTr37KoEb6ObJhKgF()
        res = [lambda: self.pc.uZ6Nyg(data='b', sendTime='now', sendTypeDesc='快递邮寄')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_zGpyxwdonEj5rUxkbGDz(self):
        """[销售出库]-直拍-京东快递-销售出库"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB'])
        self.wait_default()
        case = self.common_operations()
        case.zGpyxwdonEj5rUxkbGDz()
        res = [lambda: self.pc.uZ6Nyg(data='b', sendTime='now', sendTypeDesc='快递邮寄')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_hVymbb8xmLoC1GpxmlSy(self):
        """[销售出库]-直拍-系统叫件顺丰-销售出库"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB'])
        self.wait_default()
        case = self.common_operations()
        case.hVymbb8xmLoC1GpxmlSy()
        res = [lambda: self.pc.uZ6Nyg(data='b', sendTime='now', sendTypeDesc='快递邮寄')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_yTdtu0H22ya7KmgU59hG(self):
        """[销售出库]-直拍-系统叫件京东-销售出库"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB'])
        self.wait_default()
        case = self.common_operations()
        case.yTdtu0H22ya7KmgU59hG()
        res = [lambda: self.pc.uZ6Nyg(data='b', sendTime='now', sendTypeDesc='快递邮寄')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_g4RyFUrC2BkjMHRKinuq(self):
        """[销售出库]-直拍-自提-销售出库"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'WShX'])
        case = self.common_operations()
        case.g4RyFUrC2BkjMHRKinuq()
        res = [lambda: self.pc.uZ6Nyg(data='b', sendTime='now', sendTypeDesc='快递邮寄')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_OP7wFFxaC2oDvVTeezXi(self):
        """[拍机售后出库]-直拍-快递顺丰-售后出库"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 'C17D'])
        case = self.common_operations()
        case.OP7wFFxaC2oDvVTeezXi()
        obj = cached('articlesNo')
        res = [lambda: self.pc.wWf0eg(outboundTime='now', articlesNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_q4HsL6oaiZ29NvrH0p4P(self):
        """[拍机售后出库]-直拍-快递京东-售后出库"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 'C17D'])
        case = self.common_operations()
        case.q4HsL6oaiZ29NvrH0p4P()
        obj = cached('articlesNo')
        res = [lambda: self.pc.wWf0eg(outboundTime='now', articlesNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_TNLKcCWf408wxkwt8y53(self):
        """[拍机售后出库]-直拍-自提-售后出库"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 'C17D'])
        case = self.common_operations()
        case.TNLKcCWf408wxkwt8y53()
        obj = cached('articlesNo')
        res = [lambda: self.pc.wWf0eg(outboundTime='now', articlesNo=obj)]
        self.assert_all(*res)


class TestYjgvqjRX(BaseCase, unittest.TestCase):
    """运营中心|壹准拍机|售后管理|售后订单"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return fulfillment_r.ADixIQYwld()
        else:
            return None

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0nAYT9Iv7RAHKUiNICWDZ(self):
        """[线上审核]-直拍-仅退差-审核通过"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu'])
        case = self.common_operations(login='main')
        case.nAYT9Iv7RAHKUiNICWDZ()
        res = [lambda: self.pc.bijXOp(i=['5'], afterStatusStr='补差成功', firstAuditResultStr='通过', firstAuditTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_yCDOX9xAevVaoqLEO8Xh(self):
        """[线上审核]-直拍-优先补差-审核通过"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu'])
        case = self.common_operations()
        case.yCDOX9xAevVaoqLEO8Xh()
        res = [lambda: self.pc.bijXOp(i=['6'], afterStatusStr='补差成功', firstAuditResultStr='通过', firstAuditTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_SLVYtmn8n4nMwNGpeuK5(self):
        """[线上审核]-直拍-退货退款-审核通过"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu'])
        case = self.common_operations()
        case.SLVYtmn8n4nMwNGpeuK5()
        res = [lambda: self.pc.bijXOp(i=['7'], afterStatusStr='待寄回', firstAuditResultStr='通过', firstAuditTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_oUd1bU9wcVj8ujL9j9cI(self):
        """[线上审核]-直拍-审核拒绝"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu'])
        case = self.common_operations()
        case.oUd1bU9wcVj8ujL9j9cI()
        res = [lambda: self.pc.bijXOp(i=['2'], afterStatusStr='待申诉', firstAuditResultStr='通过', firstAuditTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_m2P7xHJlv31GMBi1Qzjb(self):
        """[待接收]-直拍-签收入库"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 's522', 'GJ8B'])
        case = self.common_operations()
        case.m2P7xHJlv31GMBi1Qzjb()
        obj = cached('order_no')
        res = [lambda: self.pc.bijXOp(i=['11'], afterStatusStr='实物复检', orderNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_nt1WLIYZKQBXObcXSO3i(self):
        """[实物复检]-直拍-复检审核-仅退差"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 's522', 'GJ8B', 'EuOa', 'UXXj', 'KXoh'])
        case = self.common_operations()
        case.nt1WLIYZKQBXObcXSO3i()
        res = [lambda: self.pc.bijXOp(i=['5'], afterStatusStr='补差成功', recheckAuditResultStr='通过', recheckAuditTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_ZZ2zZAyUsP0T3BsHmyIR(self):
        """[实物复检]-直拍-平台申诉通过-复检审核-仅退差"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 'zEPV', 'INjZ', 'mw4N', 'GJ8B', 'NCSB', 'FYzF', 'ACKg'])
        case = self.common_operations()
        case.ZZ2zZAyUsP0T3BsHmyIR()
        res = [lambda: self.pc.bijXOp(i=['5'], afterStatusStr='补差成功', recheckAuditResultStr='通过', recheckAuditTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_Om4GtulmnevZNOlqppff(self):
        """[实物复检]-直拍-复检审核-优先补差"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 's522', 'GJ8B', 'EuOa', 'UXXj', 'KXoh'])
        case = self.common_operations()
        case.Om4GtulmnevZNOlqppff()
        res = [lambda: self.pc.bijXOp(i=['6'], afterStatusStr='补差成功', firstAuditResultStr='通过', firstAuditTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_o8uJrB3BoBE3UlDBpUhK(self):
        """[实物复检]-直拍-平台申诉通过-复检审核-优先补差"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 'zEPV', 'INjZ', 'mw4N', 'GJ8B', 'NCSB', 'FYzF', 'ACKg'])
        case = self.common_operations()
        case.o8uJrB3BoBE3UlDBpUhK()
        res = [lambda: self.pc.bijXOp(i=['6'], afterStatusStr='补差成功', firstAuditResultStr='通过', firstAuditTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_hjEKlIzRRSYkSa8yshVM(self):
        """[待接收]-直拍-平台申诉通过-签收入库"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 'zEPV', 'INjZ', 'mw4N', 'pNX9'])
        case = self.common_operations()
        case.hjEKlIzRRSYkSa8yshVM()
        obj = cached('order_no')
        res = [lambda: self.pc.bijXOp(i=['11'], afterStatusStr='实物复检', orderNo=obj)]
        self.assert_all(*res)


class TestoWB7mHyz(BaseCase, unittest.TestCase):
    """运营中心|壹准拍机|售后管理|售后退货管理"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return fulfillment_r.BCCqGPByjj()
        else:
            return None


if __name__ == '__main__':
    unittest.main()
