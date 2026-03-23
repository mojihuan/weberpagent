# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.import_case import *


class TestMessageReleaseList(BaseCase, unittest.TestCase):
    """消息管理|消息发布列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return message_r.MessageReleaseListRequest()
        else:
            return message_p.MessageReleaseListPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0publish_the_message(self):
        """[发布新消息]-立即发布提交审核"""
        case = self.common_operations(login='main')
        case.publish_the_message()
        res = [lambda: self.pc.message_release_list_assert(publishStateDesc='待发布', internalAuditStateDesc='待审核', platformAuditStateDesc='未审核', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_release_new_news_timed_release_time(self):
        """[发布新消息]-定时发布提交审核"""
        case = self.common_operations()
        case.release_new_news_timed_release_time()
        res = [lambda: self.pc.message_release_list_assert(publishStateDesc='待发布', internalAuditStateDesc='待审核', platformAuditStateDesc='未审核', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_release_the_review_message(self):
        """[发布新消息]-审核并发布"""
        case = self.common_operations()
        case.release_the_review_message()
        res = [lambda: self.pc.message_release_list_assert(publishStateDesc='待发布', internalAuditStateDesc='审核通过', platformAuditStateDesc='待审核', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_release_new_news_save_the_draft(self):
        """[发布新消息]-保存草稿"""
        case = self.common_operations()
        case.release_new_news_save_the_draft()
        res = [lambda: self.pc.message_release_list_assert(publishStateDesc='草稿', internalAuditStateDesc='未审核', platformAuditStateDesc='未审核', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_release_new_news_preview_release(self):
        """[发布新消息]-预览-审核并发布"""
        case = self.common_operations()
        case.release_new_news_preview_release()
        res = [lambda: self.pc.message_release_list_assert(publishStateDesc='待发布', internalAuditStateDesc='审核通过', platformAuditStateDesc='待审核', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_refuse(self):
        """[审核]-商户审核拒绝"""
        self.pre.operations(data=['JA1'])
        case = self.common_operations()
        case.refuse()
        res = [lambda: self.pc.message_release_list_assert(publishStateDesc='待发布', internalAuditStateDesc='审核不通过', platformAuditStateDesc='-', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_approved(self):
        """[审核]-商户审核通过"""
        self.pre.operations(data=['JA1'])
        case = self.common_operations()
        case.approved()
        res = [lambda: self.pc.message_release_list_assert(publishStateDesc='待发布', internalAuditStateDesc='审核通过', platformAuditStateDesc='待审核', createTime='now')]
        self.assert_all(*res)


if __name__ == '__main__':
    unittest.main()
