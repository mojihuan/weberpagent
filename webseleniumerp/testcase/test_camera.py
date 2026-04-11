# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.decorators import cached
from common.import_case import *


class Testz3dPwWoW(BaseCase, unittest.TestCase):
    """拍机管理|售后管理|售后订单"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return camera_r.Qca9iy6PVm()
        else:
            return None

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0hmyGjNG7wkd0bhQUc2TE(self):
        """[待处理]-结束售后"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB', 'cahv', 'VMhm', 'kxvu'])
        case = self.common_operations(login='camera')
        case.hmyGjNG7wkd0bhQUc2TE()
        obj = cached('id')
        res = [lambda: self.pc.bijXOp(headers='camera', afterStatusStr='主动取消', id=obj)]
        self.assert_all(*res)


class TestYTiqew3h(BaseCase, unittest.TestCase):
    """拍机管理|拍机场次列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return camera_r.Cb5YB9WqSi()
        else:
            return None

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    @unittest.skip('')
    def test_0HX8VkOqbnv1J3lPVSFmm(self):
        """[竞拍中]-直拍-修改价格"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'IcRG', 'z2MU', 'dJeB'])
        case = self.common_operations(login='camera')
        case.HX8VkOqbnv1J3lPVSFmm()
        obj = cached('articlesNo')
        obj_2 = cached('bidPrice')
        res = [lambda: self.pc.CVkKoG(headers='camera', data='a', articlesNo=obj, bidPrice=obj_2)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    @unittest.skip('')
    def test_lPB3LMDCzxeHLnAzXMs9(self):
        """[竞拍中]-暗拍-修改价格"""
        self.pre.operations(data=['spKR', 'VyCN', 'cTZm', 'Kwz9', 'preu', 'HfWO', 'naBM', 'xNAC', 'OAqF'])
        case = self.common_operations()
        case.lPB3LMDCzxeHLnAzXMs9()
        obj = cached('articlesNo')
        obj_2 = cached('bidPrice')
        res = [lambda: self.pc.CVkKoG(headers='camera', data='a', articlesNo=obj, bidPrice=obj_2)]
        self.assert_all(*res)


if __name__ == '__main__':
    unittest.main()
