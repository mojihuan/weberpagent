# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.import_case import *


class TestHelpGenerateOrder(BaseCase, unittest.TestCase):
    """帮卖管理|帮卖上架列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return help_r.HelpGenerateOrderRequest()
        else:
            return help_p.HelpGenerateOrderPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0self_dispatch(self):
        """[批次列表tab]-去发货-自行邮寄发货成功"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA4'])
        case = self.common_operations(login='main')
        case.self_dispatch()
        res = [lambda: self.pc.help_generate_order_assert(orderStateStr='待收货', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sf_express_delivery_is_easy(self):
        """[批次列表tab]-去发货-快递易发货成功"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA4'])
        case = self.common_operations()
        case.sf_express_delivery_is_easy()
        res = [lambda: self.pc.help_generate_order_assert(orderStateStr='待收货', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_send_it_yourself(self):
        """[订单列表tab]-去发货-自己送发货成功"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA4'])
        case = self.common_operations()
        case.send_it_yourself()
        res = [lambda: self.pc.help_generate_order_assert(orderStateStr='待收货', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_cancel_order(self):
        """[订单列表tab]-取消订单-取消成功"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA4'])
        case = self.common_operations()
        case.cancel_order()
        res = [lambda: self.pc.help_generate_order_assert(orderStateStr='已取消', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_manual_signature(self):
        """[订单列表tab]-来货去退机-手动签收成功"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA4', 'GA7', 'HA1', 'GA8', 'GB2'])
        case = self.common_operations()
        case.manual_signature()
        res = [lambda: self.pc.help_generate_order_assert(orderStateStr='已退机', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    @unittest.skip('')
    def test_logistics_signature(self):
        """[订单列表tab]-来货去退机-物流签收成功"""  # todo 物流签收入库后订单状态没改变
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA4', 'GA7', 'HA1', 'GA8', 'GB3'])
        case = self.common_operations()
        case.logistics_signature()
        res = [lambda: self.pc.help_generate_order_assert(orderStateStr='已退机', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_confirmation_bond(self):
        """[订单列表tab]-确认保卖-保卖买断订单保卖成功"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA9', 'GA6', 'HA1', 'GB1'])
        case = self.common_operations()
        case.confirmation_bond()
        res = [lambda: self.pc.help_generate_order_assert(orderStateStr='已结算', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_profit_sharing_was_successful(self):
        """[订单列表tab]-确认保卖-保卖分润订单保卖成功"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA10', 'GA6', 'HA1', 'GB1'])
        case = self.common_operations()
        case.profit_sharing_was_successful()
        res = [lambda: self.pc.help_generate_order_assert(orderStateStr='待售出', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_apply_for_bargaining(self):
        """[订单列表tab]-申请议价-保卖买断-议价成功"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA9', 'GA6', 'HA1', 'GB1'])
        case = self.common_operations()
        case.apply_for_bargaining()
        res = [lambda: self.pc.help_generate_order_assert(orderStateStr='待议价', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_apply_for_cancellation(self):
        """[订单列表tab]-申请退机-退机成功"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA4', 'GA7', 'HA1'])
        case = self.common_operations()
        case.apply_for_cancellation()
        res = [lambda: self.pc.help_generate_order_assert(orderStateStr='待退机', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_new_help_order(self):
        """[批次列表tab]-发起帮卖-添加-生成帮卖订单成功"""
        self.pre.operations(data=['FA1', 'GA1'])
        case = self.common_operations()
        case.new_help_order()
        res = [lambda: self.pc.help_generate_order_assert(orderStateStr='待发货', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_new_guaranteed_purchase_order(self):
        """[批次列表tab]-发起帮卖-我要保卖-保卖买断创建订单成功"""
        self.pre.operations(data=['FA1', 'GA1'])
        case = self.common_operations()
        case.new_guaranteed_purchase_order()
        res = [lambda: self.pc.help_generate_order_assert(orderStateStr='待发货', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_new_profit_sharing_order(self):
        """[批次列表tab]-发起帮卖-我要保卖-保卖分润创建订单成功"""
        self.pre.operations(data=['FA1', 'GA1'])
        case = self.common_operations()
        case.new_profit_sharing_order()
        res = [lambda: self.pc.help_generate_order_assert(orderStateStr='待发货', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_add_item(self):
        """[发起帮卖]-下单添加物品成功"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.add_item()
        res = [lambda: self.pc.help_generate_order_assert(data='b', createTime='now')]
        self.assert_all(*res)
        self.pre.operations(data=['GA2'])

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_place_an_order_to_add_items_delete_the_item(self):
        """[发起帮卖]-下单添加物品-删除商品"""
        self.pre.operations(data=['FA1', 'GA1'])
        case = self.common_operations()
        case.place_an_order_to_add_items_delete_the_item()


class TestHelpSellTheListOfGoods(BaseCase, unittest.TestCase):
    """帮卖管理|帮卖来货列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return help_r.HelpSellTheListOfGoodsRequest()
        else:
            return help_p.HelpSellTheListOfGoodsPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0the_flow_of_goods_is_signed(self):
        """[批次列表tab]-帮卖发货-物流签收成功"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA4', 'GA6'])
        case = self.common_operations(login='vice')
        case.the_flow_of_goods_is_signed()
        res = [lambda: self.pc.help_sell_list_of_goods_assert(headers='vice', orderStateStr='待质检', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_order_logistics_signature(self):
        """[订单列表tab]-帮卖发货-物流签收成功"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA4', 'GA6'])
        case = self.common_operations()
        case.order_logistics_signature()
        res = [lambda: self.pc.help_sell_list_of_goods_assert(headers='vice', orderStateStr='待质检', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_order_manual_signature(self):
        """[订单列表tab]-帮卖发货-手动签收成功"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA4', 'GA6'])
        case = self.common_operations()
        case.order_manual_signature()
        res = [lambda: self.pc.help_sell_list_of_goods_assert(headers='vice', orderStateStr='待质检', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_manual_settlement(self):
        """[订单列表tab]-手动结算-结算成功"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA4', 'GA7', 'HA1', 'GB1', 'HB1'])
        case = self.common_operations()
        case.manual_settlement()
        res = [lambda: self.pc.help_sell_list_of_goods_assert(headers='vice', orderStateStr='待结算', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_de_check(self):
        """[订单列表tab]-去复检-保卖分润订单-提交复检成功"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA10', 'GA6', 'HA1', 'GB1', 'GA12'])
        case = self.common_operations()
        case.de_check()
        res = [lambda: self.pc.help_sell_list_of_goods_assert(headers='vice', orderStateStr='待议价', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_audit_rejection(self):
        """[订单列表tab]-审核-保卖分润订单-审核拒绝成功"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA10', 'GA6', 'HA1', 'GB1', 'GA12'])
        case = self.common_operations()
        case.audit_rejection()
        res = [lambda: self.pc.help_sell_list_of_goods_assert(headers='vice', orderStateStr='待确认', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_go_to_quality(self):
        """[订单列表tab]-去质检-提交质检成功"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA4', 'GA7', 'HA1'])
        case = self.common_operations()
        case.go_to_quality()
        res = [lambda: self.pc.help_sell_list_of_goods_assert(headers='vice', orderStateStr='待售出', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_express_delivery_unit_set_return_machine(self):
        """[订单列表tab]-去退机-快递易-单台退-退机成功"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA4', 'GA7', 'HA1', 'GA8'])
        case = self.common_operations()
        case.express_delivery_unit_set_return_machine()
        res = [lambda: self.pc.help_sell_list_of_goods_assert(headers='vice', orderStateStr='退机中', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_express_delivery_same_batch_return_machine(self):
        """[订单列表tab]-去退机-快递易-同批次退-退机成功"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA4', 'GA7', 'HA1', 'GA8'])
        case = self.common_operations()
        case.express_delivery_same_batch_return_machine()
        res = [lambda: self.pc.help_sell_list_of_goods_assert(headers='vice', orderStateStr='退机中', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_mail_by_yourself(self):
        """[订单列表tab]-去退机-自行邮寄-同下单商家退-退机成功"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA4', 'GA7', 'HA1', 'GA8'])
        case = self.common_operations()
        case.mail_by_yourself()
        res = [lambda: self.pc.help_sell_list_of_goods_assert(headers='vice', orderStateStr='退机中', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_send_it_yourself_vice(self):
        """[订单列表tab]-去退机-自己送-退机成功"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA4', 'GA7', 'HA1', 'GA8'])
        case = self.common_operations()
        case.send_it_yourself_vice()
        res = [lambda: self.pc.help_sell_list_of_goods_assert(headers='vice', orderStateStr='退机中', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_go_to_sale(self):
        """[订单列表tab]-去销售成功"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA4', 'GA7', 'HA1', 'GB1'])
        case = self.common_operations()
        case.go_to_sale()
        res = [lambda: self.pc.help_sell_list_of_goods_assert(headers='vice', orderStateStr='待售出', updateTime='now')]
        self.assert_all(*res)


class TestHelpServiceConfiguration(BaseCase, unittest.TestCase):
    """帮卖管理|帮卖业务配置"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return help_r.HelpServiceConfigurationRequest()
        else:
            return help_p.HelpServiceConfigurationPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0edit_configuration_information(self):
        """[编辑]-修改配置信息"""
        case = self.common_operations(login='vice')
        case.edit_configuration_information()
        res = [lambda: self.pc.help_service_configuration_assert(headers='vice', sellTimeoutConfiguration=30)]
        self.assert_all(*res)


if __name__ == '__main__':
    unittest.main()
