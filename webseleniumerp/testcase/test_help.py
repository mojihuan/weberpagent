# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.import_case import *


class TestdZJwkuH9(BaseCase, unittest.TestCase):
    """帮卖管理|帮卖上架列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return help_r.N1bdBTU6wm()
        else:
            return help_p.Qofwr8xFsgu(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0CtZUckEy9Xr7Q9rhDgM9(self):
        """[批次列表tab]-去发货-自行邮寄发货成功"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'AWj7'])
        case = self.common_operations(login='main')
        case.CtZUckEy9Xr7Q9rhDgM9()
        res = [lambda: self.pc.jOTfI6(orderStateStr='待收货', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_PatKHW4ZM1AOnRz4wYCa(self):
        """[批次列表tab]-去发货-快递易发货成功"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'AWj7'])
        case = self.common_operations()
        case.PatKHW4ZM1AOnRz4wYCa()
        res = [lambda: self.pc.jOTfI6(orderStateStr='待收货', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_lUGAPOtEUoXAYtTaa2Jb(self):
        """[订单列表tab]-去发货-自己送发货成功"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'AWj7'])
        case = self.common_operations()
        case.lUGAPOtEUoXAYtTaa2Jb()
        res = [lambda: self.pc.jOTfI6(orderStateStr='待收货', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_qWL5r2tvJ34XBHF8SvNA(self):
        """[订单列表tab]-取消订单-取消成功"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'AWj7'])
        case = self.common_operations()
        case.qWL5r2tvJ34XBHF8SvNA()
        res = [lambda: self.pc.jOTfI6(orderStateStr='已取消', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_xzJ4vjMEgys2mrV0XE7B(self):
        """[订单列表tab]-来货去退机-手动签收成功"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'AWj7', 'ZA5N', 'WZaL', 'Ez0X', 'RGCO'])
        case = self.common_operations()
        case.xzJ4vjMEgys2mrV0XE7B()
        res = [lambda: self.pc.jOTfI6(orderStateStr='已退机', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    @unittest.skip('物流签收入库后订单状态没改变')
    def test_KWGxLZFsVSdw6Fh5ZbAA(self):
        """[订单列表tab]-来货去退机-物流签收成功"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'AWj7', 'ZA5N', 'WZaL', 'Ez0X', 'weY4'])
        case = self.common_operations()
        case.KWGxLZFsVSdw6Fh5ZbAA()
        res = [lambda: self.pc.jOTfI6(orderStateStr='已退机', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_fNG49PWF3oUJGnsMAIuf(self):
        """[订单列表tab]-确认保卖-保卖买断订单保卖成功"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'ZyMU', 'BDSs', 'WZaL', 'Sh3x'])
        case = self.common_operations()
        case.fNG49PWF3oUJGnsMAIuf()
        res = [lambda: self.pc.jOTfI6(orderStateStr='已结算', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_giHmrq7UpbJoAn7MEMOJ(self):
        """[订单列表tab]-确认保卖-保卖分润订单保卖成功"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'pA7y', 'BDSs', 'WZaL', 'Sh3x'])
        case = self.common_operations()
        case.giHmrq7UpbJoAn7MEMOJ()
        res = [lambda: self.pc.jOTfI6(orderStateStr='待售出', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_EjR5pz1y2L10GHnV2z4v(self):
        """[订单列表tab]-申请议价-保卖买断-议价成功"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'ZyMU', 'BDSs', 'WZaL', 'Sh3x'])
        case = self.common_operations()
        case.EjR5pz1y2L10GHnV2z4v()
        res = [lambda: self.pc.jOTfI6(orderStateStr='待议价', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_fBkRLU5PnvGYpBfZdMYx(self):
        """[订单列表tab]-申请退机-退机成功"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'AWj7', 'ZA5N', 'WZaL'])
        case = self.common_operations()
        case.fBkRLU5PnvGYpBfZdMYx()
        res = [lambda: self.pc.jOTfI6(orderStateStr='待退机', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_gHXYe9nXDQKo8k2pCpHF(self):
        """[批次列表tab]-发起帮卖-添加-生成帮卖订单成功"""
        self.pre.operations(data=['ekBx', 'x1dy'])
        case = self.common_operations()
        case.gHXYe9nXDQKo8k2pCpHF()
        res = [lambda: self.pc.jOTfI6(orderStateStr='待发货', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_iCbN7kUssvEHLZtMSh1V(self):
        """[批次列表tab]-发起帮卖-我要保卖-保卖买断创建订单成功"""
        self.pre.operations(data=['ekBx', 'x1dy'])
        case = self.common_operations()
        case.iCbN7kUssvEHLZtMSh1V()
        res = [lambda: self.pc.jOTfI6(orderStateStr='待发货', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_iPBfiMFiHxZjY3ZEwdIp(self):
        """[批次列表tab]-发起帮卖-我要保卖-保卖分润创建订单成功"""
        self.pre.operations(data=['ekBx', 'x1dy'])
        case = self.common_operations()
        case.iPBfiMFiHxZjY3ZEwdIp()
        res = [lambda: self.pc.jOTfI6(orderStateStr='待发货', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_x2Ue8YzUHAdfE5e1ah2B(self):
        """[发起帮卖]-下单添加物品成功"""
        self.pre.operations(data=['ekBx'])
        case = self.common_operations()
        case.x2Ue8YzUHAdfE5e1ah2B()
        res = [lambda: self.pc.jOTfI6(data='b', createTime='now')]
        self.assert_all(*res)
        self.pre.operations(data=['VrYn'])

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_YehoAEPuerEeCRCU2qEI(self):
        """[发起帮卖]-下单添加物品-删除商品"""
        self.pre.operations(data=['ekBx', 'x1dy'])
        case = self.common_operations()
        case.YehoAEPuerEeCRCU2qEI()


class TesttHQJ9LlX(BaseCase, unittest.TestCase):
    """帮卖管理|帮卖来货列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return help_r.KtEAxo6C4B()
        else:
            return help_p.Q1DeeKQy46a(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0rE4s2MubKTarhv1LX8Ps(self):
        """[批次列表tab]-帮卖发货-物流签收成功"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'AWj7', 'BDSs'])
        case = self.common_operations(login='vice')
        case.rE4s2MubKTarhv1LX8Ps()
        res = [lambda: self.pc.help_sell_list_of_goods_assert(headers='vice', orderStateStr='待质检', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_s8ZT0XEbPTqi9X6O3C4D(self):
        """[订单列表tab]-帮卖发货-物流签收成功"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'AWj7', 'BDSs'])
        case = self.common_operations()
        case.s8ZT0XEbPTqi9X6O3C4D()
        res = [lambda: self.pc.help_sell_list_of_goods_assert(headers='vice', orderStateStr='待质检', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_bpeTVApfqf4ysIlGh0d1(self):
        """[订单列表tab]-帮卖发货-手动签收成功"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'AWj7', 'BDSs'])
        case = self.common_operations()
        case.bpeTVApfqf4ysIlGh0d1()
        res = [lambda: self.pc.help_sell_list_of_goods_assert(headers='vice', orderStateStr='待质检', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_yhsanR53oCT3E0y79Pkt(self):
        """[订单列表tab]-手动结算-结算成功"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'AWj7', 'ZA5N', 'WZaL', 'Sh3x', 'vhyj'])
        case = self.common_operations()
        case.yhsanR53oCT3E0y79Pkt()
        res = [lambda: self.pc.help_sell_list_of_goods_assert(headers='vice', orderStateStr='待结算', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_LB9ycxycPTRF4K0JdDw7(self):
        """[订单列表tab]-去复检-保卖分润订单-提交复检成功"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'pA7y', 'BDSs', 'WZaL', 'Sh3x', 'UWBK'])
        case = self.common_operations()
        case.LB9ycxycPTRF4K0JdDw7()
        res = [lambda: self.pc.help_sell_list_of_goods_assert(headers='vice', orderStateStr='待议价', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_zHbBDAztWlR3wrimNxlj(self):
        """[订单列表tab]-审核-保卖分润订单-审核拒绝成功"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'pA7y', 'BDSs', 'WZaL', 'Sh3x', 'UWBK'])
        case = self.common_operations()
        case.zHbBDAztWlR3wrimNxlj()
        res = [lambda: self.pc.help_sell_list_of_goods_assert(headers='vice', orderStateStr='待确认', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_UEgbcBjQGEn3BLntI6lb(self):
        """[订单列表tab]-去质检-提交质检成功"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'AWj7', 'ZA5N', 'WZaL'])
        case = self.common_operations()
        case.UEgbcBjQGEn3BLntI6lb()
        res = [lambda: self.pc.help_sell_list_of_goods_assert(headers='vice', orderStateStr='待售出', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_vCZ8TzDFnPROV6Oo072B(self):
        """[订单列表tab]-去退机-快递易-单台退-退机成功"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'AWj7', 'ZA5N', 'WZaL', 'Ez0X'])
        case = self.common_operations()
        case.vCZ8TzDFnPROV6Oo072B()
        res = [lambda: self.pc.help_sell_list_of_goods_assert(headers='vice', orderStateStr='退机中', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_v7U6luxQobBYtqeXdMG0(self):
        """[订单列表tab]-去退机-快递易-同批次退-退机成功"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'AWj7', 'ZA5N', 'WZaL', 'Ez0X'])
        case = self.common_operations()
        case.v7U6luxQobBYtqeXdMG0()
        res = [lambda: self.pc.help_sell_list_of_goods_assert(headers='vice', orderStateStr='退机中', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_puhf4ZwCo9hIo0rzm7zd(self):
        """[订单列表tab]-去退机-自行邮寄-同下单商家退-退机成功"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'AWj7', 'ZA5N', 'WZaL', 'Ez0X'])
        case = self.common_operations()
        case.puhf4ZwCo9hIo0rzm7zd()
        res = [lambda: self.pc.help_sell_list_of_goods_assert(headers='vice', orderStateStr='退机中', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_aR4vvS8nfanSGlBbfKzT(self):
        """[订单列表tab]-去退机-自己送-退机成功"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'AWj7', 'ZA5N', 'WZaL', 'Ez0X'])
        case = self.common_operations()
        case.aR4vvS8nfanSGlBbfKzT()
        res = [lambda: self.pc.help_sell_list_of_goods_assert(headers='vice', orderStateStr='退机中', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_OKe7y8uCYv26BcVNtvU6(self):
        """[订单列表tab]-去销售成功"""
        self.pre.operations(data=['ekBx', 'x1dy', 'SbHY', 'AWj7', 'ZA5N', 'WZaL', 'Sh3x'])
        case = self.common_operations()
        case.OKe7y8uCYv26BcVNtvU6()
        res = [lambda: self.pc.help_sell_list_of_goods_assert(headers='vice', orderStateStr='待售出', updateTime='now')]
        self.assert_all(*res)


class TestkfZOjrVB(BaseCase, unittest.TestCase):
    """帮卖管理|帮卖业务配置"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return help_r.Z2DMQfvumu()
        else:
            return help_p.ZXokM9zOq0v(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0lnEVAUkilhXnv8b0GZtm(self):
        """[编辑]-修改配置信息"""
        case = self.common_operations(login='vice')
        case.lnEVAUkilhXnv8b0GZtm()
        res = [lambda: self.pc.v3jQpR(headers='vice', sellTimeoutConfiguration=30)]
        self.assert_all(*res)


if __name__ == '__main__':
    unittest.main()
