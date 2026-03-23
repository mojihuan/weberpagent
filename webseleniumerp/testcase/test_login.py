# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.import_case import *


class TestLogin(BaseCase, unittest.TestCase):
    """登录|密码登录"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return login_r.LoginRequest()
        else:
            return login_p.LoginPages(self.driver)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_login_main(self):
        """[登录]-登录主账号"""
        case = self.common_operations()
        case.login_main()
        res = [lambda: self.pc.user_info_assert(nickName='杰克')]
        self.assert_all(*res)
        self.clear_browser_cache()


if __name__ == '__main__':
    unittest.main()
