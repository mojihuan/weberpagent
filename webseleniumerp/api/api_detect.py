# coding: utf-8
import json
from common.base_api import BaseApi


class UDPWJ42Fdke5cnO2Zzo2Y(BaseApi):
    """壹准验机管理|自定义检测列表"""

    def CKoXCQHldMya(self, headers=None):
        """自定义检测列表"""
        headers = headers or self.headers['main']
        data = {"level": 0, **self.get_page_params()}
        response = self.request_handle('post', self.urls['TADUznE32'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res


class L72tpa0sloxZTdmH8vh7R(BaseApi):
    """壹准验机管理|机型列表"""

    def FTrsMG5vZSaA(self, headers=None):
        """机型列表"""
        headers = headers or self.headers['main']
        data = {"machineDetectionSwitch": 2, "total": 0, **self.get_page_params()}
        response = self.request_handle('post', self.urls['iUkcjdebJ'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class Z1nj9K9rKRoJg9jtoq8HR(BaseApi):
    """壹准验机管理|检测管理"""

    def eYdRCdzmGHwJ(self, headers=None):
        """检测管理列表"""
        headers = headers or self.headers['main']
        data = {"templateId": 97}
        response = self.request_handle('post', self.urls['dNfWJ7EeQ'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res


class ZJ99wsztDZgRv5WpYFBq2(BaseApi):
    """壹准验机管理|质检订单列表"""

    def T18eaF48m9GV(self, headers=None):
        """质检订单列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['tM5xWQeqU'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class ObtzGp9dqCXhsCK1y2ymU(BaseApi):
    """壹准验机管理|质检报告导出"""

    def hcRfmHj042q7(self, headers=None):
        """质检报告导出列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "erpStartTime": self.get_the_date(-30), "erpEndTime": self.get_the_date()}
        response = self.request_handle('post', self.urls['tyDwziKiZ'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = ()
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
