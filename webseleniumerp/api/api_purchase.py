# coding: utf-8
import json
from common.base_api import BaseApi
from config.user_info import INFO


class Jz32tuIMNM7geguh5D8TF(BaseApi):
    """商品采购|采购售后管理|采购售后列表"""

    def a3xoH8PZvyPQ(self, headers=None, num=1, size=1000, i=None, j=None):
        """采购售后列表
        i: 售后类型 1采购售后完成 2采购售后中
        j: 售后状态 1采购退货退款 2采购拒退 3采购换货 5采购售后中 7采购退差价
        """
        headers = headers or self.headers['main']
        data = {'type': i, **self.get_page_params(num, size), 'saleState': j}
        response = self.request_handle('post', self.urls['y03duzqXb'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def WXQJQaZicxQh(self, headers=None):
        """采购售后订单详情"""
        headers = headers or self.headers['main']
        obj = self.J8AECFd0r3C5()
        response = self.request_handle('get', self.urls['xGS6K1sGm'] + '/' + obj, headers=headers)
        return self.get_response_data(response, 'data', dict)

    def J8AECFd0r3C5(self):
        """获取id"""
        return self._get_field_copy_value('a3xoH8PZvyPQ', 'main', 'id')

    def sQK5vcoxbgou(self):
        """获取imei"""
        return self._get_field_copy_value('a3xoH8PZvyPQ', 'main', 'imei')


class THtT7YW545kAG73W2gHDj(BaseApi):
    """商品采购|采购管理|到货通知单列表"""

    def Yf0yiomYxwUn(self, headers=None):
        """到货通知单列表"""
        headers = headers or self.headers['main']
        data = {"stateList": [2, 3], **self.get_page_params()}
        response = self.request_handle('post', self.urls['LDvQ06cIg'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class Rwpqef340gYUd4Hgkbq8l(BaseApi):
    """商品采购|采购售后管理|待接收物品"""

    def JsXBVOMtGANq(self, headers=None, num=1, size=1000):
        """待接收物品列表"""
        headers = headers or self.headers['main']
        data = {'articlesState': 10, 'articlesType': 1, **self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['RbZZfqC2S'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res


class A2B69SM9fkokLmjSGKvha(BaseApi):
    """商品采购|绿怡来货列表"""

    def Lq16GuRNatqC(self, headers=None):
        """绿怡来货列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['DcVKwLRC1'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class Z6BEKs3GvdIWf6a1Dj2uP(BaseApi):
    """商品采购|采购管理|采购订单列表"""

    def QYMK9r8Zx1lb(self, headers=None, num=1, size=1000, i=None, j=None):
        """采购订单列表
        i 采购单状态 1未发货 3已发货 4已收货 5已取消
        j 付款状态  1已付款 2未付款 3部分付款
        """
        headers = headers or self.headers['main']
        data = {'articlesType': 1, **self.get_page_params(num, size), 'state': i, 'payState': j}
        response = self.request_handle('post', self.urls['k90OkSeBm'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def ua4pZjFEITx3(self, headers=None):
        """采购单详情"""
        headers = headers or self.headers['main']
        obj = self.LTfBcJv11Yws()
        data = {'purchaseNo': obj, **self.get_page_params()}
        response = self.request_handle('post', self.urls['FXdRKVJv9'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)

    def LTfBcJv11Yws(self):
        """获取采购单号"""
        return self._get_field_copy_value('QYMK9r8Zx1lb', 'main', 'orderNo')

    def E2qQy9qFAyui(self):
        """获取imei"""
        return self._get_field_copy_value('ua4pZjFEITx3', 'main', 'imei')

    def wnq7ocm1WM7D(self, headers=None):
        """获取物流单号"""
        return self._get_field_copy_value('QYMK9r8Zx1lb', 'main', 'logisticsNoList')[0]

    def b79nkKcYqUhD(self, headers=None):
        """ 获取物品编号"""
        return self._get_field_copy_value('QYMK9r8Zx1lb', 'main', 'articlesNoList')[0]


class XHVW0IhQgPnb63fnaqTdN(BaseApi):
    """商品采购|采购售后管理|待售后列表"""

    def gx9ALZDTXtyL(self, headers=None, num=1, size=1000):
        """采购待售后列表"""
        headers = headers or self.headers['main']
        data = {'type': 1, **self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['Npkbsubce'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class UCpwX0dlRXRmKVzfDX5dd(BaseApi):
    """商品采购|供应商管理"""

    def q9RXyfc2X1UG(self, headers=None):
        """供应商管理"""
        headers = headers or self.headers['main']
        data = {'type': 2, **self.get_page_params()}
        response = self.request_handle('post', self.urls['jj0Esnp8n'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)

    def sqbiUoeq8gU6(self):
        """获取供应商名称"""
        return self._get_field_copy_value('q9RXyfc2X1UG', 'idle', 'supplierName')

    def VrxuOJtwagsZ(self):
        """获取供应商名称"""
        return self._get_field_copy_value('q9RXyfc2X1UG', 'main', 'supplierName')

    def WJ1hPxxMWpfI(self):
        """获取供应商id"""
        return self._get_field_copy_value('q9RXyfc2X1UG', 'main', 'id')


class Y6hDdvp1tY9uk0H51cn91(BaseApi):
    """商品采购|采购管理|未发货订单列表"""

    def B2HBJYTnnYyI(self, headers=None):
        """未发货订单列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['NQuaSyCwg'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class WmKG9OkI9OlJlOENUzgNu(BaseApi):
    """商品采购|采购管理|采购工单"""

    def b1R30NI8UzKR(self, headers=None, num=1, size=1000, i=None):
        """采购工单列表
        i: 状态 1待开始 2进行中 3已结束
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'state': i}
        response = self.request_handle('post', self.urls['zaz3DUWFs'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def O4zibjbjN1p4(self, headers=None):
        """报工明细详情
        index: 工序索引，默认 0
        """
        headers = headers or self.headers['main']
        data = {"workId": self.get_id()}
        response = self.request_handle('post', self.urls['RN0cPdOBl'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res

    def OM0oLdLrEBPV(self):
        """获取报价工序 id"""
        return self._get_field_copy_value('b1R30NI8UzKR', 'main', 'taskProgressList.id')

    def get_id(self):
        """获取id"""
        return self._get_field_copy_value('b1R30NI8UzKR', 'main', 'id')


class ZzpxfXbO9fEmLG1gxxzjP(BaseApi):
    """商品采购|采购任务"""

    def we5YUPreA4h0(self, headers=None, num=1, size=1000, i=None):
        """采购任务列表
        i: 任务状态 1未完成 2部分完成 3已取消 4已完成
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'status': i}
        response = self.request_handle('post', self.urls['uq3xxE6qc'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def sOOabMKgYnDs(self, headers=None):
        """更新到货详情"""
        headers = headers or self.headers['main']
        data = {}
        response = self.request_handle('get', self.urls['ooRhqoYOb'] + '/' + self.G4XKHgMGbUtx(), data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res

    def i13Vwm2s7hDn(self, headers=None):
        """采购录入详情"""
        order_no = self.G4XKHgMGbUtx()
        headers = headers or self.headers['main']
        data = {"supplierId": INFO['main_supplier_id'], "taskOrderNo": order_no}
        response = self.request_handle('post', self.urls['CiYjGB6ia'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res

    def u0vCCOCkGc1P(self, headers=None):
        """采购退货信息"""
        headers = headers or self.headers['main']
        data = {}
        response = self.request_handle('get', self.urls['El53WHDKp'] + '/' + self.G4XKHgMGbUtx(), data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res

    def G4XKHgMGbUtx(self):
        """获取采购单号"""
        return self._get_field_copy_value('we5YUPreA4h0', 'main', 'orderNo')


if __name__ == '__main__':
    api = ()
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
