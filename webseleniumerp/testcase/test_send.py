# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.import_case import *


class TestPiFfXpg1(BaseCase, unittest.TestCase):
    """送修管理|已送修物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return send_r.FU9FBZt4ek()
        else:
            return send_p.HxV90Wh2Jkw(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0oaxztsMnbnAXzAxWj6JK(self):
        """[送修完成]"""
        self.pre.operations(data=['ekBx', 'Y1eX', 'yhRO'])
        case = self.common_operations(login='main')
        case.oaxztsMnbnAXzAxWj6JK()
        res = [lambda: self.pc.send_been_sent_repair(repairStatusName='确认入库', repairSuccessTime='now')]
        self.assert_all(*res)


class TestteMDNclX(BaseCase, unittest.TestCase):
    """送修管理|送修单列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return send_r.KNGJBF1SxK()
        else:
            return send_p.B0rX5iYQN6L(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0woND08hYZ9lwms8Lse0i(self):
        """[送修工费结算]-已付款"""
        self.pre.operations(data=['ekBx', 'Y1eX', 'yhRO', 'pqYJ'])
        case = self.common_operations(login='main')
        case.woND08hYZ9lwms8Lse0i()
        res = [lambda: self.pc.WqPUcl(statusStr='已完成', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_k42ezJisaBTjBTBWBoXd(self):
        """[送修工费结算]-未付款"""
        self.pre.operations(data=['ekBx', 'Y1eX', 'yhRO', 'pqYJ'])
        case = self.common_operations()
        case.k42ezJisaBTjBTBWBoXd()
        res = [lambda: self.pc.WqPUcl(statusStr='已完成', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_MKKvPqQBfeXIBJT3V5Jl(self):
        """[导出]"""
        case = self.common_operations()
        case.MKKvPqQBfeXIBJT3V5Jl()
        res = [lambda: self.pc.T241Se(state=2, name='送修单列表导出', createTime='now')]
        self.assert_all(*res)


class TestS0cpMD5e(BaseCase, unittest.TestCase):
    """送修管理|待送修物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return send_r.DImzEKD7BR()
        else:
            return send_p.Xt1lLWcjOv9(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0FDe96kyUKHRoCJ6I7nfE(self):
        """[送修出库]"""
        self.pre.operations(data=['ekBx', 'Y1eX'])
        case = self.common_operations(login='main')
        case.FDe96kyUKHRoCJ6I7nfE()
        res = [lambda: self.pc.WqPUcl(statusStr='未完成', createTime='now')]
        self.assert_all(*res)


if __name__ == '__main__':
    unittest.main()
