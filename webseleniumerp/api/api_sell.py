# coding: utf-8
import json
from common.base_api import BaseApi


class VqEvejbpK4kaxGc8KQymZ(BaseApi):
    """商品销售|销售售后管理|销售售后处理"""


class Kw5nIo3WQBrH2BPScRj1B(BaseApi):
    """商品销售|销售售后管理|销售售后列表"""

    def CfIRP7WqVPD0(self, headers=None, num=1, size=1000):
        """销售售后完成"""
        headers = headers or self.headers['main']
        data = {'saleStatus': '5', **self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['ia8hPCPU9'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def TB2VQJLBUDje(self, headers=None, num=1, size=1000):
        """销售售后中"""
        headers = headers or self.headers['main']
        data = {'saleStatus': '4', **self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['ia8hPCPU9'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PaCOjaNKGGuX7m5M6knOA(BaseApi):
    """商品销售|客户管理"""

    def BWkrNYN6KI65(self, headers=None):
        """客户管理"""
        headers = headers or self.headers['main']
        data = {"type": 1, **self.get_page_params()}
        response = self.request_handle('post', self.urls['jj0Esnp8n'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def Dr0F7PV8ZEXi(self):
        """获取id"""
        return self._get_field_copy_value('BWkrNYN6KI65', 'main', 'id', index=1)

    def X2OzrVJcQf2u(self):
        """获取id"""
        return self._get_field_copy_value('BWkrNYN6KI65', 'vice', 'id')


class Mb5NtymgNZq58BhIE7Umz(BaseApi):
    """商品销售|销售管理|待接收物品"""

    def z8Q8CdTAeeYa(self, headers=None):
        """待接收物品列表"""
        headers = headers or self.headers['main']
        data = {"articlesState": 13, "articlesType": "1", **self.get_page_params()}
        response = self.request_handle('post', self.urls['RbZZfqC2S'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)

    def K3BimDHtN4Wm(self):
        """获取物品编号"""
        return self._get_field_copy_value('z8Q8CdTAeeYa', 'main', 'articlesNo')


class XTk41pUDr28xCf1YL17uR(BaseApi):
    """商品销售|销售管理|待销售物品"""

    def CSDYFXdhL7n5(self, headers=None, num=1, size=1000):
        """待销售物品列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['aoTTb5SV6'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def enB0x369cbFt(self, headers=None):
        """待销售物品详情"""
        headers = headers or self.headers['main']
        obj = self.YmkWFo8i8lsJ()
        response = self.request_handle('get', self.urls['EuHHS09oD'] + obj, headers=headers)
        return self.get_response_data(response, 'data', dict)

    def YmkWFo8i8lsJ(self):
        """获取物品编号"""
        return self._get_field_copy_value('CSDYFXdhL7n5', 'main', 'articlesNo')


class Ez77PXDybIrSTaH32RHsz(BaseApi):
    """商品销售|销售管理|销售中物品列表"""

    def TyFTRRkgcx28(self, i=None, j=None, headers=None, num=1, size=1000):
        """销售中物品列表
         i：销售状态 2已销售 3已取消 1销售中
         j：销售类型 1销售 3铺货 5预售
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'saleStatus': i, 'saleType': j}
        response = self.request_handle('post', self.urls['Dj1kQUUk9'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def fReTQwlPp5ig(self, headers=None):
        """销售物品详情"""
        headers = headers or self.headers['main']
        obj = self.mVtqOxQxQW2k()
        data = {"code": obj, "saleType": 2}
        response = self.request_handle('post', self.urls['F6KRfR2sB'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)

    def JPomkBOsk0MN(self, headers=None):
        """下架详情"""
        headers = headers or self.headers['main']
        obj = self.mVtqOxQxQW2k()
        data = {'code': obj, 'saleType': 2}
        response = self.request_handle('post', self.urls['F6KRfR2sB'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res

    def mVtqOxQxQW2k(self):
        """获取物品编号"""
        return self._get_field_copy_value('TyFTRRkgcx28', 'main', 'articlesNo')


class PvQWvJ1ETZicFTZpXHiQa(BaseApi):
    """商品销售|销售管理|销售中订单列表"""

    def lZHWz7XAePfb(self, headers=None, num=1, size=1000):
        """销售中订单列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['MRyx7Q3Y7'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class JU8QYbNi3BDlSn2XaNZKe(BaseApi):
    """商品销售|销售管理|已销售物品列表"""

    def L6IQgdpG4iaP(self, headers=None, num=1, size=1000):
        """已销售物品列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['RMIZIc17j'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class OY2fdbdieaa3seD31U6ZQ(BaseApi):
    """商品销售|销售管理|已销售订单列表"""

    def B37xGAx8rLVJ(self, headers=None, num=1, size=1000):
        """已销售订单列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['yst2PxBzE'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class RCRdrY38amwbJyUzKuJcM(BaseApi):
    """商品销售|销售数据统计"""

    def oatZoHAFV0w1(self, headers=None, i=None):
        """统计"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "startTime": self.get_the_date(-30), "endTime": self.get_the_date(), 'saleSupplierId': i}
        response = self.request_handle('post', self.urls['zT60feze1'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = ()
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
