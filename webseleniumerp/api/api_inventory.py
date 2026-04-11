# coding: utf-8
import json
from common.base_api import BaseApi


class Ie1Dlx6hKL0xHjTgV7J4p(BaseApi):
    """库存管理|出库管理|地址管理"""

    def X41neJLZTAeU(self, headers=None, num=1, size=1000):
        """地址管理列表"""
        headers = headers or self.headers['idle']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['XMuPTimkX'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def gJorZjinv4G3(self):
        """获取id"""
        return self._get_field_copy_value('X41neJLZTAeU', 'idle', 'id')

    def kTPaZWqxyWsq(self):
        """获取壹准保卖id"""
        return self._get_field_copy_value('X41neJLZTAeU', 'main', 'id', index=2)

    def KwGZrW0yw6eZ(self):
        """获取通用业务id"""
        return self._get_field_copy_value('X41neJLZTAeU', 'main', 'id')

    def QMZr0EnpAFgz(self):
        """获取壹准拍机id"""
        return self._get_field_copy_value('X41neJLZTAeU', 'camera', 'id', index=3)


class Ux7lF2b6qktEytPTzyaQW(BaseApi):
    """库存管理|库存盘点"""

    def dGxdNvDrm0gW(self, headers=None, num=1, size=1000):
        """库存盘点列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['nW4OoHj4n'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def gLKuPaGShNTQ(self):
        """获取盘点单号"""
        return self._get_field_copy_value('dGxdNvDrm0gW', 'main', 'stockNo')

    def PdEoJVKJqJco(self):
        """获取盘点id"""
        return self._get_field_copy_value('dGxdNvDrm0gW', 'main', 'id')


class UYV6mZaVwDk4HHhyuWRRp(BaseApi):
    """库存管理|库存列表"""

    def I8TzeuUVWOYr(self, headers=None, i=None, j=None, num=1, size=1000, t=None):
        """库存列表
         i：库存状态 2库存中 1待入库 3已出库
         j：物品状态 2待收货 13待销售 3待分货 7维修中 5质检中 19销售预售中 14销售铺货中 16待送修 9已销售 15销售售后中 17送修中 11采购售后完成 12采购售后中 18仅出库 10待采购售后
         t: 品类id
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'inventoryStatus': i, 'articlesState': j, 'articlesTypeId': t}
        response = self.request_handle('post', self.urls['ipnnuHXAj'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def EbJ4mgpvdxWd(self, headers=None):
        """库存列表 总成本详情 统计"""
        headers = headers or self.headers['main']
        obj = self.hwHynYPMN64V()
        data = {**self.get_page_params()}
        response = self.request_handle('get', self.urls['QJDG7wBXf'] + '/' + obj, data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)

    def QPjBR7LSwxnq(self, headers=None, i=0):
        """库存列表 总成本详情"""
        headers = headers or self.headers['main']
        obj = self.hwHynYPMN64V()
        data = {**self.get_page_params(), 'articlesNo': obj}
        response = self.request_handle('post', self.urls['I7UwPdhw9'], data=json.dumps(data), headers=headers)
        rows = self.get_response_data(response, 'rows', list)
        if len(rows) > i >= 0:
            return rows[i]
        else:
            print("走这个逻辑了")
            return None

    def JGJO4DeQYuKZ(self, headers=None):
        """库存列表 总收入详情 统计"""
        headers = headers or self.headers['main']
        obj = self.hwHynYPMN64V()
        data = {**self.get_page_params()}
        response = self.request_handle('get', self.urls['Am4n24rP9'] + '/' + obj, data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)

    def MDmyPNWh4b2g(self, headers=None, i=0):
        """库存列表 总收入详情"""
        headers = headers or self.headers['main']
        obj = self.hwHynYPMN64V()
        data = {**self.get_page_params(), 'articlesNo': obj}
        response = self.request_handle('post', self.urls['Jvd9g14Oc'], data=json.dumps(data), headers=headers)
        rows = self.get_response_data(response, 'rows', list)
        if len(rows) > i >= 0:
            return rows[i]
        else:
            return None

    def DiPuR7wiWR9p(self, headers=None):
        """物品详情 销售信息"""
        headers = headers or self.headers['main']
        obj = self.hwHynYPMN64V()
        data = {'articlesNo': obj}
        response = self.request_handle('post', self.urls['GkKAGzHxf'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)

    def LtZxEhUVdwQS(self, headers=None):
        """物品详情 操作日志"""
        headers = headers or self.headers['main']
        obj = self.hwHynYPMN64V()
        data = {'articlesNoList': [obj]}
        response = self.request_handle('post', self.urls['dJ8r3vdbO'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)

    def hwHynYPMN64V(self, i=None, j=None, index=0):
        """获取库存列表 物品编号
         i：库存状态 2库存中 1待入库 3已出库
         j：物品状态 13待销售 3待分货 7维修中 5质检中 19销售预售中 14销售铺货中 16待送修 9已销售 15销售售后中 17送修中 11采购售后完成 12采购售后中 18仅出库 10待采购售后
         index: 下标
        """
        return self._get_field_copy_value('I8TzeuUVWOYr', 'main', 'articlesNo', i=i, j=j, index=index)


class Y4aFmqv9pBI4kE90s31Kj(BaseApi):
    """库存管理|入库管理|物流修改记录"""

    #
    def O5fTSpfSPAoZ(self, headers=None, num=1, size=1000):
        """物流修改记录列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['GbZ6p4ew4'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class WbrwTMcyqVsFRjRMcUD9e(BaseApi):
    """库存管理|入库管理|物流签收入库"""

    def __init__(self):
        super().__init__()
        self.obj = D2grXOWzOv0I5f5rFGf6A()

    def joJXaZxu9B1W(self, headers=None, num=1, size=1000):
        """物流签收入库"""
        headers = headers or self.headers['main']
        obj = self.obj.dwmf2AQ8xpIP()
        data = {**self.get_page_params(num, size), 'logisticsNo': obj}
        response = self.request_handle('post', self.urls['qSJp57Vg0'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def SCRnoTvUvLxT(self):
        """获取物品编号"""
        return self._get_field_copy_value('joJXaZxu9B1W', 'main', 'articlesNo')


class D2grXOWzOv0I5f5rFGf6A(BaseApi):
    """库存管理|入库管理|物流列表"""

    def bI2yFNa61M9Q(self, headers=None, num=1, size=1000, i=None, j=None, k=None):
        """物流列表
        i imei
        j 平台物品编号
        k 状态
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'imei': i, 'platformArticlesNo': j, 'sortationStatus': k}
        response = self.request_handle('post', self.urls['uTaRhDofB'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def t9tSA8AX8kJj(self, headers=None):
        """物流列表详情"""
        headers = headers or self.headers['main']
        logistics_no = self.dwmf2AQ8xpIP()
        data = {**self.get_page_params(), "logisticsNo": logistics_no}
        response = self.request_handle('post', self.urls['qSJp57Vg0'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def dwmf2AQ8xpIP(self):
        """获取物流编号"""
        return self._get_field_copy_value('bI2yFNa61M9Q', 'main', 'logisticsNo')


class ZAmvXnrvwr5eb8QWmgfEi(BaseApi):
    """库存管理|库存统计|库存型号分布"""

    def EOR9zOMj0PM6(self, headers=None, num=1, size=1000):
        """库存型号分布列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'articlesTypeId': "1"}
        response = self.request_handle('post', self.urls['EgxbiOGo3'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class FPzFtRyRp6MMELtWkCL74(BaseApi):
    """库存管理|出库管理|出库物流记录"""

    def pisUbUMkKyba(self, headers=None, num=1, size=1000):
        """出库物流记录列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['AHXHaskTV'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class QYSFzOWmZ2zYnize8ppKN(BaseApi):
    """库存管理|出库管理|仅出库订单列表"""

    def ORF5PGdo8vkp(self, headers=None, num=1, size=1000):
        """仅出库列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['AA9mGFXdb'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def jkCbj4E7lnmd(self, headers=None, num=1, size=1000):
        """退回单列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['r62raRuAZ'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def FlBn7VEIrt0P(self, headers=None):
        """仅出库订单详情"""
        headers = headers or self.headers['main']
        obj = self.zFvTaV1HisT0()
        data = {'id': obj, **self.get_page_params(), 'total': 0, 'type': 1}
        response = self.request_handle('post', self.urls['CvrTwP6A1'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)

    def zFvTaV1HisT0(self):
        """获取id"""
        return self._get_field_copy_value('ORF5PGdo8vkp', 'main', 'id')


class OYpwrGPUzEGu4UKFy4D3k(BaseApi):
    """库存管理|库存统计|库存人员分布"""

    def u4wUUjovCaXi(self, headers=None, num=1, size=1000):
        """库存人员分布列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['vBYrJCEG0'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class LWT9dymUmXdvWqLk1qEeA(BaseApi):
    """库存管理|移交接收管理|接收物品"""

    def wX85yA1a0yOb(self, i=None, j=None, headers=None, k=None):
        """物品接收
         i：物品状态 1待维修 2待收货 3待分货 4待质检 5质检中 6待维修 7维修中
         j: 品类 1手机
        """
        headers = headers or self.headers['main']
        data = {'articlesType': 1, **self.get_page_params(), 'articlesState': i, 'articlesTypeId': j, 'reasonType': k}
        response = self.request_handle('post', self.urls['RbZZfqC2S'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res

    def XbUs4Xjcx1eU(self, headers=None, num=1, size=1000, i=None):
        """移交单接收"""
        headers = headers or self.headers['main']
        data = {'articlesType': '1', **self.get_page_params(num, size), 'reasonType': i}
        response = self.request_handle('post', self.urls['ZspzD8hZ0'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def fPKMGLwa2uJG(self, headers=None, j=1):
        """移交单接收详情"""
        headers = headers or self.headers['main']
        obj = self.XbUs4Xjcx1eU()
        data = {"articlesType": j, "orderNo": obj[0]['orderNo']}
        response = self.request_handle('post', self.urls['HltehqYGD'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)


class SuZBsKiCxZh6bvOywIAer(BaseApi):
    """库存管理|出库管理|送修出库"""


class PzpwGb0gERxw3s5t4WiGd(BaseApi):
    """库存管理|移交接收管理|移交记录"""

    def YsmsUS99q8Mf(self, headers=None, num=1, size=1000, i=None, j=None):
        """移交记录列表
        i 状态
        j 原因
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'articlesType': 1, 'status': i, 'reasonType': j}
        response = self.request_handle('post', self.urls['QD32hq4Lp'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def O2cpz6NJM1Ql(self, headers=None):
        """移交记录列表详情"""
        headers = headers or self.headers['main']
        order_no = self.F8owV7A0wK51()
        data = {"orderNo": order_no, "articlesType": 1}
        response = self.request_handle('post', self.urls['HltehqYGD'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)

    def F8owV7A0wK51(self):
        """获取单号"""
        return self._get_field_copy_value('YsmsUS99q8Mf', 'main', 'orderNo')


class AgsSpo5TPaF3SeCAMUzGn(BaseApi):
    """库存管理|入库管理|待接收物品"""

    def hytiDSEbbu3r(self, headers=None, num=1, size=1000):
        """待接收物品列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), "erpStartTime": self.get_the_date(-7), "erpEndTime": self.get_the_date()}
        response = self.request_handle('post', self.urls['RbZZfqC2S'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class XHyhIffDlKvRSMGo6DlG2(BaseApi):
    """库存管理|库存调拨"""

    def scIEFidBwtZs(self, headers=None, num=1, size=1000):
        """仓库调拨列表"""
        headers = headers or self.headers['main']
        data = {'articlesType': '1', **self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['Vqx4RAgDI'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def pbck8gdOUVzz(self, headers=None):
        """调拨详情"""
        headers = headers or self.headers['main']
        obj = self.wgrSh0ilkBGV()
        data = {'articlesType': '1', 'id': obj}
        response = self.request_handle('post', self.urls['mMiwJEj2a'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)

    def wgrSh0ilkBGV(self):
        """获取id"""
        return self._get_field_copy_value('scIEFidBwtZs', 'main', 'id')


class Y1KM3RQrEIg4DDdfeQQYl(BaseApi):
    """库存管理|库存统计|库龄预警"""

    def UsgUvVUsoiQq(self, headers=None, num=1, size=1000):
        """库龄预警列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'articlesTypeId': 1}
        response = self.request_handle('post', self.urls['B0JybhojP'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = UYV6mZaVwDk4HHhyuWRRp()
    result = api.EbJ4mgpvdxWd()
    print(json.dumps(result, indent=4, ensure_ascii=False))
