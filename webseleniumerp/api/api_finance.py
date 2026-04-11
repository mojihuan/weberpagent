# coding: utf-8
import json
from common.base_api import BaseApi
from config.user_info import INFO


class NQXuyZ5kySQBpsQJxR3vC(BaseApi):
    """财务管理|资金账户|账户列表"""

    def xsn47jtSUiZ8(self, headers=None, num=1, size=1000):
        """账户列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['JvDC6PWG4'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def dBMS1qAcYEzH(self, headers=None):
        """账户列表 统计"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['JvDC6PWG4'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)

    def wUybbFZAc1F0(self):
        """获取账户编号"""
        return self._get_field_copy_value('xsn47jtSUiZ8', 'main', 'accountNo')

    def QIaTbZQd4c2R(self):
        """获取账户编号"""
        return self._get_field_copy_value('xsn47jtSUiZ8', 'vice', 'accountNo')

    def JRy7c5gNjU5D(self):
        """获取账户名称"""
        return self._get_field_copy_value('xsn47jtSUiZ8', 'main', 'accountName')

    def NDv9JRmcGNSo(self):
        """获取账户id"""
        return self._get_field_copy_value('xsn47jtSUiZ8', 'idle', 'id')

    def CRx8SuT6pM8C(self):
        """获取账户id"""
        return self._get_field_copy_value('xsn47jtSUiZ8', 'idle', 'id', index=1)


class L4HyUAwaneDzrwe1REUd7(BaseApi):
    """财务管理|财务报表|经营分析表"""

    def IvqTyEaHW26G(self, headers=None):
        """统计"""
        headers = headers or self.headers['main']
        year = self.get_the_date().split('-')[0]
        response = self.request_handle('get', self.urls['H47hT7L0C'] + year, headers=headers)
        return self.get_response_data(response, 'data', list)


class VFy40VMBZGf8pQEkVFRor(BaseApi):
    """财务管理|业务记账|账单审核"""

    def zS2mEs09Al0d(self, headers=None, i=None, j=None, num=1, size=1000):
        """应付账单
        i：1应付 2应收
        j: 0待审核 1审核通过 2未通过
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'bill_type': i, 'auditStatus': j}
        response = self.request_handle('post', self.urls['rYq6rx5rs'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class H9Xjv30kk5a6ul7sNOTeg(BaseApi):
    """财务管理|业务记账|收款结算单"""

    def dRsMaRuoo4vp(self, headers=None, num=1, size=1000):
        """收款结算单列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'userType': '1'}
        response = self.request_handle('post', self.urls['lfj66nHdx'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class A13uxi3ZgFLvq4bXHCbVE(BaseApi):
    """财务管理|财务设置|分佣付款设置"""

    def CAorxNLNPM4l(self, headers=None):
        """分佣付款设置"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "payType": "1"}
        response = self.request_handle('post', self.urls['NnfhdunHg'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)


class BF8Qli4PzmMYad6sgj32n(BaseApi):
    """财务管理|财务设置|分佣收款设置"""

    def jgPFnRwKX8zQ(self, headers=None):
        """分佣收款设置"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "payType": "1"}
        response = self.request_handle('post', self.urls['NnfhdunHg'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)


class MOyeqlzcgLqhqdWBrkyYg(BaseApi):
    """财务管理|业务记账|往来应付"""

    def VPtqPg96V4bb(self, headers=None, num=1, size=1000):
        """对账详情"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'supplierId': str(INFO['main_supplier_id']), 'userType': "2", 'startTime': self.get_the_date(-181), 'endTime': self.get_the_date()}
        response = self.request_handle('post', self.urls['fv8gP6xvX'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def aXD0ILNAtA0v(self, headers=None):
        """按机器结算 添加机器 机器列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'supplierId': str(INFO['main_supplier_id']), 'userType': 2, 'payType': '2'}
        response = self.request_handle('post', self.urls['fsPQs2Ojb'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def NrrYfPEfdJwE(self, headers=None, num=1, size=1000):
        """往来应付列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), "billOff": 0, "userType": "2", "payType": "2", 'supplierId': INFO['main_supplier_id']}
        response = self.request_handle('post', self.urls['CbdRT6U6Y'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def rRW8valbixkj(self, headers=None):
        """按供应商结算 列表"""
        headers = headers or self.headers['main']
        data = {"supplierId": INFO['main_supplier_id'], "preType": "2"}
        response = self.request_handle('post', self.urls['kzPtUOA6C'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res

    def Anlk8HQ08DoN(self, headers=None):
        """对账详情 单据详情"""
        headers = headers or self.headers['main']
        obj = self.edmOCxHV7j1T()
        data = {**self.get_page_params(), 'total': 0, 'billNo': obj}
        response = self.request_handle('post', self.urls['QYiIgqis0'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def edmOCxHV7j1T(self):
        """获取单据编号"""
        return self._get_field_copy_value('VPtqPg96V4bb', 'main', 'billNo')


class CxWYtVbPEgBMsAbMB1sNz(BaseApi):
    """财务管理|成本收入调整"""

    def R7ocRWn8F0VR(self, headers=None, num=1, size=1000):
        """单据列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['VdjIBIvP7'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def tJdw1dzjQNC9(self, headers=None):
        """单据列表 详情"""
        headers = headers or self.headers['main']
        obj = self.WwUe9qcddPbR()
        data = {**self.get_page_params()}
        response = self.request_handle('get', self.urls['zxYQFwBFr'] + '/' + obj, data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)

    def oIoZoEJlkHmY(self, headers=None, num=1, size=1000):
        """物品列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['C18p5xJTq'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def WwUe9qcddPbR(self):
        """获取单据编号"""
        return self._get_field_copy_value('R7ocRWn8F0VR', 'main', 'adjustmentNo')


class VuQB5fbYnrZcz4kwyRlA6(BaseApi):
    """财务管理|财务设置|客户收款设置"""

    def e0Jc866jA4lp(self, headers=None):
        """客户收款设置"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['qc7tESkN3'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)


class OApuzLHbCS388IVB9m2c9(BaseApi):
    """财务管理|业务记账|日常支出"""

    def StQZwBU9k4GX(self, headers=None, num=1, size=1000):
        """日常支出列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'payType': '2'}
        response = self.request_handle('post', self.urls['mO85Zzhgc'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def z91RXolcKAt2(self, headers=None):
        """统计金额"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'payType': '2'}
        response = self.request_handle('post', self.urls['yQiaANVrW'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)


class LgTsekFh4kT1Jm0Xt5UhY(BaseApi):
    """财务管理|业务记账|日常收入"""

    def xZn2CBfoX85Y(self, headers=None, num=1, size=1000):
        """日常收入列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'payType': '1'}
        response = self.request_handle('post', self.urls['mO85Zzhgc'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def BXqoSGwoTjgD(self, headers=None):
        """统计金额"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'payType': '1'}
        response = self.request_handle('post', self.urls['yQiaANVrW'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)


class A9mwkPeNc1x7YnLCF9jUk(BaseApi):
    """财务管理|业务记账|往来应收"""

    def onzqxhWPmd6i(self, headers=None, num=1, size=1000):
        """对账详情"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'supplierId': str(INFO['main_sale_supplier_id']), 'userType': 1, 'startTime': self.get_the_date(), 'endTime': self.get_the_date()}
        response = self.request_handle('post', self.urls['sbvSOImQ6'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def iL6f7yggjwGo(self, headers=None):
        """按机器结算-添加机器-机器列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'supplierId': str(INFO['main_sale_supplier_id']), 'userType': 1, 'payType': '1'}
        response = self.request_handle('post', self.urls['fsPQs2Ojb'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def bWw7A4mK6xtK(self, headers=None, num=1, size=1000):
        """往来应收列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), "billOff": 0, "userType": "1", "payType": "1", 'supplierId': INFO['main_sale_supplier_id']}
        response = self.request_handle('post', self.urls['CbdRT6U6Y'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def uznhxIKxB5lv(self, headers=None):
        """按客户结算 列表"""
        headers = headers or self.headers['main']
        data = {"preType": "1", 'supplierId': INFO['main_sale_supplier_id']}
        response = self.request_handle('post', self.urls['kzPtUOA6C'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res

    def oIkWBNgsRuRQ(self, headers=None):
        """对账详情 单据详情"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'total': 0, 'billNo': self.TmHNz5UovhBA()}
        response = self.request_handle('post', self.urls['QYiIgqis0'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def TmHNz5UovhBA(self):
        """获取单据号"""
        return self._get_field_copy_value('onzqxhWPmd6i', 'main', 'billNo')

    def YDHYJyJBtDFv(self):
        """获取未收金额合计"""
        return self._get_field_copy_value('bWw7A4mK6xtK', 'main', 'periodicEndAmount')


class JUWG98MXNVNGQf93x5CwI(BaseApi):
    """财务管理|财务设置|费用项目类型设置"""

    def f9L0xWiuFdex(self, headers=None):
        """费用项目类型设置"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['pmbGw2e7l'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)


class TLt2NsvdRPrlyXBduaMZ4(BaseApi):
    """财务管理|业务记账|付款结算单"""

    def bIUbOOYwwkaD(self, headers=None, num=1, size=1000):
        """付款结算单列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'userType': '2'}
        response = self.request_handle('post', self.urls['lfj66nHdx'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class ZDGSH9p2RLv5QuD68Ivi9(BaseApi):
    """财务管理|业务记账|预收预付"""

    def poj74krsYufe(self, i=None, headers=None, num=1, size=1000):
        """预付、预收列表
        i：1 预付 2预收
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'preType': i}
        response = self.request_handle('post', self.urls['ynbeJ7bOo'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def X9F8g7436ipH(self, headers=None):
        """预收/预付详情"""
        headers = headers or self.headers['main']
        response = self.request_handle('get', self.urls['xFuNsanYB'] + self.eg1lVyhLMwSP(), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def eg1lVyhLMwSP(self):
        """获取预付id"""
        return self._get_field_copy_value('poj74krsYufe', 'main', 'id')


class ZPHs2hurgrDXzLGQr8WqW(BaseApi):
    """财务管理|财务设置|供应商付款设置"""

    def wRQMH8F0kbh5(self, headers=None):
        """供应商付款设置"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['qc7tESkN3'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)


class KkU8jJZhRGbWRP2ZjHKyg(BaseApi):
    """财务管理|资金账户|交易明细"""

    def ChMjJGNgwb2P(self, headers=None, num=1, size=1000):
        """交易明细"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['K51XBu4Xp'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def KOfZrjbCYKDG(self):
        return self._get_field_copy_value('ChMjJGNgwb2P', 'main', 'merchantName')


if __name__ == '__main__':
    api = ()
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
