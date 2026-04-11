# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.decorators import cached
from common.import_case import *


class TestwPCeBiRP(BaseCase, unittest.TestCase):
    """平台管理|虚拟库存|上拍商品管理"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return platform_r.ONWaZZcZFp()
        else:
            return None

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0fSkueYEb8y8LbP6qtAqN(self):
        """[可上拍物品tab]选择场次-暗拍卖场-添加商品上架"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'naBM'])
        case = self.common_operations(login='super')
        case.fSkueYEb8y8LbP6qtAqN()
        res = [lambda: self.pc.ieulBh(headers='super', i=2, updateTime='now', statusStr='销售中', auctionMarketSession='暗拍')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_qCFRqyBkOvZyZ960KoJp(self):
        """[可上拍物品tab]-选择场次-直拍卖场-添加商品上架"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG'])
        case = self.common_operations()
        case.qCFRqyBkOvZyZ960KoJp()
        res = [lambda: self.pc.ieulBh(headers='super', i=2, updateTime='now', statusStr='销售中', auctionMarketSession='直拍')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_vVyPEQRdLSOkYnwvSH3o(self):
        """[可上拍物品tab]-取消销售"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO'])
        case = self.common_operations()
        case.vVyPEQRdLSOkYnwvSH3o()
        obj = cached('id')
        res = [lambda: self.pc.aY387y(j=1, i=2, id=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sGNrdfZH3A7fxgKXDlng(self):
        """[可上拍物品tab]-修改场次-暗拍修改场次"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'naBM', 'F0Hr'])
        case = self.common_operations()
        case.sGNrdfZH3A7fxgKXDlng()
        res = [lambda: self.pc.ieulBh(headers='super', i=2, updateTime='now', statusStr='销售中', auctionMarketSession='暗拍')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_HeRVQcjIj8Kd5Ue1KUfT(self):
        """[可上拍物品tab]-取消上拍"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'naBM', 'F0Hr'])
        case = self.common_operations()
        case.HeRVQcjIj8Kd5Ue1KUfT()
        res = [lambda: self.pc.ieulBh(headers='super', i=1, updateTime='now')]
        self.assert_all(*res)


class Testa7G4eELN(BaseCase, unittest.TestCase):
    """平台管理|运营中心|待指定物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return platform_r.X7hPGKXTGz()
        else:
            return platform_p.G9Xb1VIa3XI(self.driver)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0cz1GOzhkNTwJrIaMIvqG(self):
        """[指定回收商]"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'Q7Xz'])
        case = self.common_operations(login='platform')
        case.cz1GOzhkNTwJrIaMIvqG()
        res = [lambda: self.pc.eTpj8W(headers='platform', assignTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_TCteXSkve0Oznurlnztw(self):
        """[修改回收商]"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'Q7Xz'])
        case = self.common_operations()
        case.TCteXSkve0Oznurlnztw()
        res = [lambda: self.pc.eTpj8W(headers='platform', assignTime='now')]
        self.assert_all(*res)


class TestPVeFTsjs(BaseCase, unittest.TestCase):
    """平台管理|卖场管理|暗拍卖场列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return platform_r.G4BNkqhL40()
        else:
            return platform_p.ZbWaTtRLQPH(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0oQ4T86fmEaH8KwhBSxP3(self):
        """[创建卖场]指定日期-场次频率每天-无保证金-手机-保存并上架"""
        case = self.common_operations(login='super')
        case.oQ4T86fmEaH8KwhBSxP3()
        res = [lambda: self.pc.EtRRIT(headers='super', createTime='now', statusStr='已上架')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_MLwLbgD1GL9V7rRzU5DF(self):
        """[创建卖场]暗拍-仅保存"""
        case = self.common_operations()
        case.MLwLbgD1GL9V7rRzU5DF()
        res = [lambda: self.pc.EtRRIT(i=2, headers='super', createTime='now', statusStr='待上架')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_O4GTsiJ6xj3TEtnNe5vS(self):
        """[创建卖场]指定5分钟一场-保存并上架"""
        case = self.common_operations()
        case.O4GTsiJ6xj3TEtnNe5vS()
        res = [lambda: self.pc.EtRRIT(headers='super', createTime='now', statusStr='已上架')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_Bkz45n2kH6kLSep0tdDB(self):
        """[已下架tab]暗拍卖场-编辑-保存并上架"""
        self.pre.operations(data=['naBM', 'e8Bq'])
        case = self.common_operations()
        case.Bkz45n2kH6kLSep0tdDB()
        res = [lambda: self.pc.EtRRIT(headers='super', updateTime='now', statusStr='已上架')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_Qbf3jYdHG3h4d8NIxgTa(self):
        """[已下架tab]暗拍卖场-重新上架"""
        self.pre.operations(data=['naBM', 'e8Bq'])
        case = self.common_operations()
        case.Qbf3jYdHG3h4d8NIxgTa()
        res = [lambda: self.pc.EtRRIT(headers='super', updateTime='now', statusStr='已上架')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_SML4kMf2uJffhQbwtUx6(self):
        """[下架]已上架状态-下架卖场"""
        self.pre.operations(data=['Lmb4'])
        case = self.common_operations()
        case.SML4kMf2uJffhQbwtUx6()
        res = [lambda: self.pc.EtRRIT(headers='super', createTime='now', statusStr='已下架')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_gnlGXVVK4aiBrYlOX6oB(self):
        """[查看场次详情]-已上架状态-添加商品-手机"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'naBM'])
        case = self.common_operations()
        case.gnlGXVVK4aiBrYlOX6oB()
        res = [lambda: self.pc.EtRRIT(headers='super', data='a', totalMum=1)]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_rWYreYEUUn6guCfMIcjL(self):
        """[查看场次详情]关闭开放查看商品"""
        self.pre_platform.every_day_on_a_specified_date_phone()
        case = self.common_operations()
        case.rWYreYEUUn6guCfMIcjL()

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_ZAkeZYaFKKXvRIOgPLOU(self):
        """[待上架tab]-上架"""
        self.pre.operations(data=['TBmR'])
        case = self.common_operations()
        case.ZAkeZYaFKKXvRIOgPLOU()
        res = [lambda: self.pc.EtRRIT(headers='super', statusStr='已上架', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_zWLMV5RXaVG7XxYhtEn2(self):
        """[待上架tab]-编辑-保存并上架"""
        self.pre.operations(data=['TBmR'])
        case = self.common_operations()
        case.zWLMV5RXaVG7XxYhtEn2()
        res = [lambda: self.pc.EtRRIT(headers='super', statusStr='已上架', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_pf1dNwfGdkEBsdL4SZfG(self):
        """[待上架tab]-删除"""
        self.pre.operations(data=['TBmR'])
        case = self.common_operations()
        case.pf1dNwfGdkEBsdL4SZfG()

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_TcjguVZWjalBPkIgMgk2(self):
        """[已下架tab]-编辑-保存并上架"""
        self.pre.operations(data=['naBM', 'e8Bq'])
        case = self.common_operations()
        case.TcjguVZWjalBPkIgMgk2()
        res = [lambda: self.pc.EtRRIT(headers='super', statusStr='已上架', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_jinaFo1BfuHnHIiDdZPE(self):
        """[调整广告位]多选-显示已上架和待上架-保存并更新"""
        case = self.common_operations()
        case.jinaFo1BfuHnHIiDdZPE()

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_iArGbfUX5RsDKrB8KgZN(self):
        """[调整广告位]多选-显示已上架和待上架和已下架-保存并更新"""
        case = self.common_operations()
        case.iArGbfUX5RsDKrB8KgZN()

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_KPvNzeTk3NvDtpqKWlVb(self):
        """[查看日志]"""
        case = self.common_operations()
        case.KPvNzeTk3NvDtpqKWlVb()

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_I1S9lui6I0jHXse8gVcc(self):
        """[导出]"""
        case = self.common_operations()
        case.I1S9lui6I0jHXse8gVcc()


class TesthufeywrZ(BaseCase, unittest.TestCase):
    """平台管理|卖场管理|直拍卖场列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return platform_r.UVTJ3GwNrM()
        else:
            return platform_p.YAKR9LJejV2(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0dkzcGVBC4f0eOkX7psWu(self):
        """[创建卖场]指定日期-场次频率每天-手机-保存并上架"""
        case = self.common_operations(login='super')
        case.dkzcGVBC4f0eOkX7psWu()
        res = [lambda: self.pc.rkNFDq(headers='super', createTime='now', statusStr='已上架')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_YOZXR96FA6wK0SgiwgLh(self):
        """[创建卖场]仅保存"""
        case = self.common_operations()
        case.YOZXR96FA6wK0SgiwgLh()
        res = [lambda: self.pc.rkNFDq(headers='super', createTime='now', statusStr='待上架')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_QfMsQBRWh1m3ZmMdtjh1(self):
        """[已下架tab]-编辑-保存并上架"""
        self.pre.operations(data=['IcRG', 'DpA7'])
        case = self.common_operations()
        case.QfMsQBRWh1m3ZmMdtjh1()
        res = [lambda: self.pc.rkNFDq(headers='super', updateTime='now', statusStr='已上架')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_S9rWKvQ89U7Uknx1aXeR(self):
        """[已上架tab]-下架"""
        self.pre.operations(data=['IcRG'])
        case = self.common_operations()
        case.S9rWKvQ89U7Uknx1aXeR()
        res = [lambda: self.pc.rkNFDq(headers='super', updateTime='now', statusStr='已下架')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_i2PADX8AIUDmt1eH6XmL(self):
        """[查看场次详情]已上架状态-添加商品-手机"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG'])
        case = self.common_operations()
        case.i2PADX8AIUDmt1eH6XmL()
        res = [lambda: self.pc.rkNFDq(headers='super', data='a', totalMum=1),
               lambda: self.pc.rkNFDq(headers='super', data='b', updateTime='now', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_icBZPN1P562alvUYw9qv(self):
        """[查看场次详情]关闭开放查看商品"""
        self.pre.operations(data=['IcRG'])
        case = self.common_operations()
        case.icBZPN1P562alvUYw9qv()

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_w7Q9iTIZZFL6IeAt7EDA(self):
        """[调整广告位]多选-显示已上架和待上架-保存并更新"""
        case = self.common_operations()
        case.w7Q9iTIZZFL6IeAt7EDA()

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_E9V5GboJRLQOhqmn6ZP0(self):
        """[调整广告位]多选-显示已上架和待上架和已下架-保存并更新"""
        case = self.common_operations()
        case.E9V5GboJRLQOhqmn6ZP0()

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_VCvQ9C6taFx1IE4yFXlK(self):
        """[查看日志]"""
        case = self.common_operations()
        case.VCvQ9C6taFx1IE4yFXlK()

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_xGvapPmmNaRHIGh8Hi7I(self):
        """[导出]"""
        case = self.common_operations()
        case.xGvapPmmNaRHIGh8Hi7I()


class TestQYogENo7(BaseCase, unittest.TestCase):
    """平台管理|消息管理|消息发布列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return platform_r.SMtCxoJnmP()
        else:
            return platform_p.QE6VcNFjGEj(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0pj4bj85GPh759JlXB1ir(self):
        """[审核]-平台审核拒绝"""
        self.pre.operations(data=['qVoK'])
        case = self.common_operations(login='platform')
        case.pj4bj85GPh759JlXB1ir()
        res = [lambda: self.pc.dbii4b(publishStateDesc='待发布', internalAuditStateDesc='审核通过', platformAuditStateDesc='审核不通过', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_G9C97BkpOngHG41cgA0L(self):
        """[审核]-平台审核通过"""
        self.pre.operations(data=['qVoK'])
        case = self.common_operations()
        case.G9C97BkpOngHG41cgA0L()
        res = [lambda: self.pc.dbii4b(publishStateDesc='已发布', internalAuditStateDesc='审核通过', platformAuditStateDesc='审核通过', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_pdEsg1lHJfR191fcMim5(self):
        """[审核]-平台撤回"""
        self.pre.operations(data=['qVoK', 'xblM'])
        case = self.common_operations()
        case.pdEsg1lHJfR191fcMim5()
        res = [lambda: self.pc.dbii4b(publishStateDesc='已撤回', internalAuditStateDesc='审核通过', platformAuditStateDesc='审核通过', createTime='now')]
        self.assert_all(*res)


class TestiLGmLucZ(BaseCase, unittest.TestCase):
    """平台管理|同售管理|商品审核"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return platform_r.RzBsOiNk4l()
        else:
            return platform_p.TvMioJovFR2(self.driver)


class TestbEamAQ8C(BaseCase, unittest.TestCase):
    """平台管理|订单管理|订单审核"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return platform_r.WlAFVePJlH()
        else:
            return platform_p.AjSkA6klpCA(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0BBiltLX4GA5cpSCyECIP(self):
        """[审核]-快递易-对公充值-平台审核通过"""
        self.pre.operations(data=['Ufaw'])
        case = self.common_operations(login='platform')
        case.BBiltLX4GA5cpSCyECIP()
        res = [lambda: self.pc.czuDPA(headers='platform', orderBusinessTypeStr='钱包充值', auditStatusStr='已通过', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_FMRI6lTSPPbGRqorxtkt(self):
        """[审核]-快递易-对公充值-平台审核拒绝"""
        self.pre.operations(data=['Ufaw'])
        case = self.common_operations()
        case.FMRI6lTSPPbGRqorxtkt()
        res = [lambda: self.pc.czuDPA(headers='platform', orderBusinessTypeStr='钱包充值', auditStatusStr='未通过', createTime='now')]
        self.assert_all(*res)


class TestOVERgq9N(BaseCase, unittest.TestCase):
    """平台管理|壹准拍机|售后管理|申诉管理"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return platform_r.V35pu3YhqH()
        else:
            return None

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0X4Qg6ocEen8r1SwVi5GT(self):
        """[待处理]-直拍-审核通过-仅补差"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 'zEPV', 'INjZ'])
        case = self.common_operations()
        case.X4Qg6ocEen8r1SwVi5GT()
        res = [lambda: self.pc.z91bun(i=1, headers='platform', statusStr='申诉成功', auditTime='now'),
               lambda: self.pc.VU8ebM(i=[5], headers='platform', afterStatusStr='补差成功', firstAppealAuditTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_Ms6Xyable2b9S87LhPZd(self):
        """[待处理]-直拍-审核通过-优先补差"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 'zEPV', 'INjZ'])
        case = self.common_operations()
        case.Ms6Xyable2b9S87LhPZd()
        obj = cached('afterOrderNo')
        res = [lambda: self.pc.z91bun(i=1, headers='platform', statusStr='申诉成功', auditTime='now'),
               lambda: self.pc.Alrd2T(data='c', i=[6], headers='camera', orderNo=obj, afterStatus=6)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_Or5VGbcLZ6drxl8wkMSR(self):
        """[待处理]-直拍-审核通过-退货退款"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu', 'zEPV', 'INjZ'])
        case = self.common_operations()
        case.Or5VGbcLZ6drxl8wkMSR()
        obj = cached('afterOrderNo')
        res = [lambda: self.pc.z91bun(i=1, headers='platform', statusStr='申诉成功', auditTime='now'),
               lambda: self.pc.Alrd2T(data='c', i=[7], headers='camera', orderNo=obj, afterStatus=7)]
        self.assert_all(*res)


if __name__ == '__main__':
    unittest.main()
