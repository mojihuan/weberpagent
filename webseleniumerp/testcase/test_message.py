# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.import_case import *


class TestCHLZlzWz(BaseCase, unittest.TestCase):
    """消息管理|消息发布列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return message_r.QRSsWbYWV1()
        else:
            return message_p.Alkolwr5Vbg(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0p2KvndGL0zVJEDKHGIPU(self):
        """[发布新消息]-立即发布提交审核"""
        case = self.common_operations(login='main')
        case.p2KvndGL0zVJEDKHGIPU()
        res = [lambda: self.pc.dbii4b(publishStateDesc='待发布', internalAuditStateDesc='待审核', platformAuditStateDesc='未审核', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_fNGpyQ3gggozz0uW4Ko0(self):
        """[发布新消息]-定时发布提交审核"""
        case = self.common_operations()
        case.fNGpyQ3gggozz0uW4Ko0()
        res = [lambda: self.pc.dbii4b(publishStateDesc='待发布', internalAuditStateDesc='待审核', platformAuditStateDesc='未审核', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_qJP3yR1nymSHmVoKgKFz(self):
        """[发布新消息]-审核并发布"""
        case = self.common_operations()
        case.qJP3yR1nymSHmVoKgKFz()
        res = [lambda: self.pc.dbii4b(publishStateDesc='待发布', internalAuditStateDesc='审核通过', platformAuditStateDesc='待审核', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_ELqbuERMQsawGlkE9Ala(self):
        """[发布新消息]-保存草稿"""
        case = self.common_operations()
        case.ELqbuERMQsawGlkE9Ala()
        res = [lambda: self.pc.dbii4b(publishStateDesc='草稿', internalAuditStateDesc='未审核', platformAuditStateDesc='未审核', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_JERvfLXoEn18N8nGDyMd(self):
        """[发布新消息]-预览-审核并发布"""
        case = self.common_operations()
        case.JERvfLXoEn18N8nGDyMd()
        res = [lambda: self.pc.dbii4b(publishStateDesc='待发布', internalAuditStateDesc='审核通过', platformAuditStateDesc='待审核', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_yNFy3et5XdWwF0gE1VJQ(self):
        """[审核]-商户审核拒绝"""
        self.pre.operations(data=['IBY2'])
        case = self.common_operations()
        case.yNFy3et5XdWwF0gE1VJQ()
        res = [lambda: self.pc.dbii4b(publishStateDesc='待发布', internalAuditStateDesc='审核不通过', platformAuditStateDesc='-', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_FAEFTmKmDM49LcbTv3tL(self):
        """[审核]-商户审核通过"""
        self.pre.operations(data=['IBY2'])
        case = self.common_operations()
        case.FAEFTmKmDM49LcbTv3tL()
        res = [lambda: self.pc.dbii4b(publishStateDesc='待发布', internalAuditStateDesc='审核通过', platformAuditStateDesc='待审核', createTime='now')]
        self.assert_all(*res)


if __name__ == '__main__':
    unittest.main()
