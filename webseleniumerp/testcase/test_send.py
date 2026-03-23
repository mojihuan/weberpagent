# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.import_case import *


class TestSendBeenSentRepair(BaseCase, unittest.TestCase):
    """送修管理|已送修物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return send_r.SendBeenSentRepairRequest()
        else:
            return send_p.SendBeenSentRepairPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0repair_completed_route(self):
        """[送修完成]"""
        self.pre.operations(data=['FA1', 'HC9', 'HI1'])
        case = self.common_operations(login='main')
        case.repair_completed_route()
        res = [lambda: self.pc.send_been_sent_repair(repairStatusName='确认入库', repairSuccessTime='now')]
        self.assert_all(*res)


class TestSendRepairList(BaseCase, unittest.TestCase):
    """送修管理|送修单列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return send_r.SendRepairListRequest()
        else:
            return send_p.SendRepairListPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0repair_fee_settlement_paid(self):
        """[送修工费结算]-已付款"""
        self.pre.operations(data=['FA1', 'HC9', 'HI1', 'NA1'])
        case = self.common_operations(login='main')
        case.repair_fee_settlement_paid()
        res = [lambda: self.pc.send_list_of_repair_orders_assert(statusStr='已完成', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_repair_fee_settlement_non_payment(self):
        """[送修工费结算]-未付款"""
        self.pre.operations(data=['FA1', 'HC9', 'HI1', 'NA1'])
        case = self.common_operations()
        case.repair_fee_settlement_non_payment()
        res = [lambda: self.pc.send_list_of_repair_orders_assert(statusStr='已完成', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_derived_data(self):
        """[导出]"""
        case = self.common_operations()
        case.derived_data()
        res = [lambda: self.pc.system_export_list_assert(state=2, name='送修单列表导出', createTime='now')]
        self.assert_all(*res)


class TestSendStayRepair(BaseCase, unittest.TestCase):
    """送修管理|待送修物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return send_r.SendStayRepairRequest()
        else:
            return send_p.SendStayRepairPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0send_out_for_repair(self):
        """[送修出库]"""
        self.pre.operations(data=['FA1', 'HC9'])
        case = self.common_operations(login='main')
        case.send_out_for_repair()
        res = [lambda: self.pc.send_list_of_repair_orders_assert(statusStr='未完成', createTime='now')]
        self.assert_all(*res)


if __name__ == '__main__':
    unittest.main()
