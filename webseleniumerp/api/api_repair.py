# coding: utf-8
import json
from common.base_api import BaseApi
from config.user_info import INFO


class ZAMtQ4KJqvZUBTAc0PR9C(BaseApi):
    """维修管理|已维修物品"""

    def EfbrT89zLBmF(self, headers=None, num=1, size=1000):
        """已维修物品列表"""
        headers = headers or self.headers['main']
        data = {'repairEndTime': self.get_the_date(), 'repairStartTime': self.get_the_date(),
                **self.get_page_params(num, size), 'statusList': ['3', '4']}
        response = self.request_handle('post', self.urls['QFy83ZguP'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def Ra1PPAjRiXqA(self, headers=None):
        """维修记录"""
        headers = headers or self.headers['main']
        obj = self.p2XlJfcnkpKM()
        data = {'articlesNo': obj}
        response = self.request_handle('post', self.urls['I42cjnX3e'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def p2XlJfcnkpKM(self):
        """获取物品编号"""
        return self._get_field_copy_value('EfbrT89zLBmF', 'main', 'articlesNo')


class DWcWzlMTzkfWaD2Gzlfh4(BaseApi):
    """维修管理|维修中物品列表"""

    def OWRYXo8QsITm(self, headers=None, num=1, size=1000):
        """维修中物品列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['orddk8kMq'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PjQrObCdCglLnCtpMNnBl(BaseApi):
    """维修管理|拆件管理"""

    def aEYHWNFkQu3e(self, headers=None):
        """拆件管理列表-按单据"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['NNdAgV0DI'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def KwSgyqc8esAa(self, headers=None):
        """拆件管理列表-按明细"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['TL1w762zE'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class Gv7PVAqUJKoyfROzOacmx(BaseApi):
    """维修管理|维修项目列表"""

    def bltCvd8b8uHx(self, i=None, headers=None):
        """维修项目列表
         i: 品类 1手机 2平板 3电脑 4手表
        """
        headers = headers or self.headers['main']
        data = {'articlesTypeId': i}
        response = self.request_handle('post', self.urls['dqr0tJaP9'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)

    def UsdOQX8s4QX3(self, i=None, headers=None):
        """机型配置列表
         i: 品类 1手机 3平板 4电脑 5手表
        """
        headers = headers or self.headers['main']
        data = {'articlesTypeId': i}
        response = self.request_handle('post', self.urls['HdEaRCtoQ'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)


class Lcknx2hvjZ0Wb3X0xpPAQ(BaseApi):
    """维修管理|待接收物品"""

    def QlnK2i3mvzrc(self, headers=None):
        """待接收物品"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "articlesState": 6, "articlesType": "1"}
        response = self.request_handle('post', self.urls['Sm7yLloyr'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)

    def WLqjEJ7MOyzJ(self, headers=None):
        """待接收配件"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "articlesState": 18, "articlesType": "2"}
        response = self.request_handle('post', self.urls['warehousing_receive_items'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)

    def BV4PE3DpkzDf(self):
        """获取物品编号"""
        return self._get_field_copy_value('repair_wait_receive', 'main', 'articlesNo')


class ZdhlTgRrRPGEMOegDrOfk(BaseApi):
    """维修管理|维修审核列表"""

    def dUaU2azQ6FGY(self, i=None, headers=None, num=1, size=1000):
        """维修审核列表
         i：审核状态 1待审核 2已通过 3未通过
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'statusList': ['3', '4'], 'auditStatus': i}
        response = self.request_handle('post', self.urls['oAqwtPGk9'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class UWAIk0bTSjwruaIoaUmEI(BaseApi):
    """维修管理|维修数据统计"""

    def WcTTUqK8ZUm8(self, headers=None):
        """维修数据统计"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "statusList": ["3", "4"], "userId": INFO['main_user_id']}
        response = self.request_handle('post', self.urls['RoeoWDdFc'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = None
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
