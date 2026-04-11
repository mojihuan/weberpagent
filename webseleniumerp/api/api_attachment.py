# coding: utf-8
import json
from common.base_api import BaseApi
from config.user_info import INFO


class Nd81xbVVnxevE1Oy8yXcy(BaseApi):
    """配件管理|配件销售|销售售后列表"""

    def VGeFY2YzIHzc(self, headers=None, num=1, size=1000, i=None):
        """销售售后列表
        i: 售后类型 1退货退款 2退差价
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'sellType': i}
        response = self.request_handle('post', self.urls['r9ytswUaJ'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def FOLBxm2fXcoW(self, headers=None):
        """销售售后详情"""
        headers = headers or self.headers['main']
        obj = self.VGeFY2YzIHzc()
        data = {**self.get_page_params(), 'orderNo': obj[0]['orderNo']}
        response = self.request_handle('post', self.urls['zyeN8gswZ'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class Gwz4FEbJD7duHFXM43CTo(BaseApi):
    """配件管理|配件统计|赠送明细"""

    def t3GVi2bbFIzs(self, headers=None, num=1, size=1000):
        """赠送明细列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['yydFmDz2D'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class BF3x3lYIzbEHMnrvr80JO(BaseApi):
    """配件管理|入库管理|待接收物品"""

    def iigq4MszOhe3(self, headers=None, num=1, size=1):
        """待接收物品列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['JKjPTfATh'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class BFOjFKv6ZxII7V5LzQcr4(BaseApi):
    """配件管理|移交接收管理|移交记录"""

    def pvspNI89ooNR(self, headers=None, num=1, size=1000, i=None):
        """移交记录"""
        headers = headers or self.headers['main']
        data = {'articlesType': 2, 'status': i, **self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['zbE7yOZvu'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def ABCpFCzCuSNt(self, headers=None):
        """移交记录详情"""
        headers = headers or self.headers['main']
        data = {"orderNo": self.fiNWNRpni7P6(), "articlesType": 2}
        response = self.request_handle('post', self.urls['HltehqYGD'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res

    def fiNWNRpni7P6(self):
        """获取订单号"""
        return self._get_field_copy_value('pvspNI89ooNR', 'main', 'orderNo')


class Jv7ADErQkdUSgRBqXT5qz(BaseApi):
    """配件管理|配件库存|库存明细"""

    def vdzd03TVxB8g(self, headers=None, num=1, size=1000):
        """库存明细列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'total': 0}
        response = self.request_handle('post', self.urls['hEtBXn55f'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def WlKyKGm5zDPh(self, headers=None):
        """库存明细统计"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'total': 0}
        response = self.request_handle('post', self.urls['HVMZS71CQ'], data=json.dumps(data), headers=headers)
        return response.json()["data"]


class CtRBRcFNn2LnUPfJF5Yhu(BaseApi):
    """配件管理|配件库存|库存列表"""

    def H2lnntBLD8A3(self, i=None, j=None, k=None, l=None, m=None, a=None, headers=None, num=1, size=1000):
        """库存列表
        i: 库存状态 2库存中 1待入库 3已出库
        j: 品类
        k：品牌
        l：型号
        m：配件成色 1新配件 2旧配件采购
        a：配件渠道 1原厂 2非原厂
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'inventoryStatus': i, 'articlesTypeId': j, 'brandId': k, 'modelId': l, 'accessoryQuality': m, 'channelType': a}
        response = self.request_handle('post', self.urls['QARwOTuPY'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def OS0dslt8oIW6(self, headers=None):
        """物品详情"""
        headers = headers or self.headers['main']
        data = {'articlesNo': self.Ja2f73XKPwQz()}
        response = self.request_handle('post', self.urls['yuX8ASRLX'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)

    def ryjErEJrLvhi(self, headers=None):
        """物品详情-采购信息"""
        headers = headers or self.headers['main']
        data = {'articlesNo': self.Ja2f73XKPwQz()}
        response = self.request_handle('post', self.urls['vJIP1KwBo'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)

    def X2VJTiwTrgcC(self, headers=None):
        """物品详情-销售信息"""
        headers = headers or self.headers['main']
        data = {'articlesNo': self.Ja2f73XKPwQz()}
        response = self.request_handle('post', self.urls['MdXnAHnec'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)

    def Wo6IwyvOfpNM(self, headers=None):
        """物品详情-操作日志"""
        headers = headers or self.headers['main']
        data = {'articlesNoList': [self.Ja2f73XKPwQz()]}
        response = self.request_handle('post', self.urls['dJ8r3vdbO'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)

    def Ja2f73XKPwQz(self):
        """获取物品编号"""
        return self._get_field_copy_value('H2lnntBLD8A3', 'main', 'articlesNo')


class Ln0faZ5CGpaYmkrcCVg4X(BaseApi):
    """配件管理|配件维护"""

    def c69L92JCEAfA(self, headers=None, i=None, num=1, size=1000):
        """配件维护列表
        i：状态 0开启用 1停用
        """
        headers = headers or self.headers['idle']
        data = {**self.get_page_params(num, size), 'status': i}
        response = self.request_handle('post', self.urls['GTZ0UOiDK'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class KFkHdZyASZRhMrmNKfHiQ(BaseApi):
    """配件管理|入库管理|新到货入库"""

    def __init__(self):
        super().__init__()
        self.obj = LnfQBDqBvleaE2O0412qk()

    def aYrCZLAaSxA7(self, headers=None, num=1, size=1000):
        """新到货入库"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'logisticsNo': self.obj.YwVSc3Nv5QU3()}
        response = self.request_handle('post', self.urls['apFM5LAR2'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, '', list)
        self.make_pkl_file(res)
        return res


class RjB1dOTFUrlGReUmemgQr(BaseApi):
    """配件管理|入库管理|旧配件入库"""

    def U6Xw8Ui8Ti9x(self, headers=None, num=1, size=1000):
        """旧配件入库列表"""
        headers = headers or self.headers['main']
        data = {'total': 0, **self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['icqD4B9Rk'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def eGKYE973IfbO(self, headers=None):
        """旧配件入库列表 详情"""
        headers = headers or self.headers['main']
        res = self.U6Xw8Ui8Ti9x()
        data = {'total': 0, **self.get_page_params(), "orderNo": res[0]['orderNo']}
        response = self.request_handle('post', self.urls['WhJckIuHl'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)


class OiUAWoPURtS5QdkSFauge(BaseApi):
    """配件管理|配件采购|采购列表"""

    def PA6i54jUEr6x(self, headers=None, num=1, size=1000, i=None, j=None):
        """采购列表
        i: 采购单状态 3已发货 4已收货
        j: 付款状态 1已付款 2未付款
        """
        headers = headers or self.headers['main']
        data = {'articlesType': 2, **self.get_page_params(num, size), 'state': i, 'payState': j}
        response = self.request_handle('post', self.urls['fRokl0vv2'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def NOWFR2ysZMiz(self, headers=None):
        """采购列表详情"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'purchaseNo': self.DJF7CiNjGRTC()}
        response = self.request_handle('post', self.urls['NWi2CZbYk'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)

    def lJHIDIvQhKow(self, headers=None):
        """采购售后详情"""
        headers = headers or self.headers['main']
        data = {"supplierId": INFO['main_supplier_id'], "purchaseNoList": [self.DJF7CiNjGRTC()]}
        response = self.request_handle('post', self.urls['XKp5SlLCE'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)

    def DJF7CiNjGRTC(self):
        """获取采购单号"""
        return self._get_field_copy_value('PA6i54jUEr6x', 'main', 'orderNo')


class KjMTctZhHuOMIT0xd1AP3(BaseApi):
    """配件管理|配件采购|采购售后列表"""

    def G5wHf1sqe1zu(self, headers=None, num=1, size=1000):
        """采购售后列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['gnqQCdDTa'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def osRwiAV9t4QT(self, headers=None):
        """采购售后列表详情"""
        headers = headers or self.headers['main']
        obj = self.G5wHf1sqe1zu()
        data = {"saleNo": obj[0]['saleNo'], **self.get_page_params()}
        response = self.request_handle('post', self.urls['LVVrmH10p'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class AMaXd2PkDsrT5cj1SArOe(BaseApi):
    """配件管理|移交接收管理|接收物品"""

    def mfaVZuvBLcri(self, headers=None, num=1, size=1000):
        """物品接收列表"""
        headers = headers or self.headers['main']
        data = {'articlesType': '2', **self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['JKjPTfATh'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def s3Ycs7Oyt5DL(self, headers=None, i=None, num=1, size=1000):
        """移交单接收列表
        i：移交单状态 1待接收 2已接收 3已取消
        """
        headers = headers or self.headers['main']
        data = {'articlesType': '2', **self.get_page_params(num, size), 'status': i}
        response = self.request_handle('post', self.urls['ZspzD8hZ0'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def NPp0AJ9kG7cr(self, headers=None):
        """移交单接收详情"""
        headers = headers or self.headers['main']
        data = {'articlesType': '2', 'orderNo': self.DhUI624oh7bX()}
        response = self.request_handle('post', self.urls['HltehqYGD'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res

    def DhUI624oh7bX(self):
        """获取采购单号"""
        return self._get_field_copy_value('s3Ycs7Oyt5DL', 'main', 'orderNo')


class Yitlwlf3LfoaHccm1J6mF(BaseApi):
    """配件管理|移交接收管理|移交物品"""

    def __init__(self):
        super().__init__()
        self.obj = CtRBRcFNn2LnUPfJF5Yhu()

    def pk3yPDL8mWlJ(self, headers=None):
        """移交物品列表"""
        headers = headers or self.headers['main']
        data = {"articlesNo": self.obj.Ja2f73XKPwQz()}
        response = self.request_handle('post', self.urls['WfRN4FHg5'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', dict)
        self.make_pkl_file(res)
        return res


class Y9pPmEIVBiqj7NBb64Jy4(BaseApi):
    """配件管理|配件统计|销售明细"""

    def acB0a2Y5bfRO(self, i=1, headers=None):
        """销售明细列表
         i：1本月 2上月
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "total": 99, "month": i}
        response = self.request_handle('post', self.urls['RtfOH9UEB'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)

    def jWnUAmYy0V7w(self, i=1, headers=None):
        """销售明细统计-本月
         i：1本月 2上月
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "total": 99, "month": i}
        response = self.request_handle('post', self.urls['HQBxA0jMJ'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)


class IW1UwaP9R0hojKPOJQSH4(BaseApi):
    """配件管理|配件销售|销售列表"""

    def xTgxXhKIdF5f(self, headers=None, num=1, size=1000, i=None):
        """销售列表
        i: 收款状态 1已收款 2未收款
        """
        headers = headers or self.headers['main']
        data = {'articlesType': 2, **self.get_page_params(num, size), 'status': i}
        response = self.request_handle('post', self.urls['m9MsjRh7V'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def iVaMuxcu6FrP(self, headers=None):
        """销售详情"""
        headers = headers or self.headers['main']
        data = {'orderNo': self.JXbPQwCVMKBn(), **self.get_page_params()}
        response = self.request_handle('post', self.urls['to9GfL6Bk'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)

    def q83zbqHUQwKT(self, headers=None):
        """销售售后"""
        headers = headers or self.headers['main']
        data = {"saleOrderNoList": [self.JXbPQwCVMKBn()]}
        response = self.request_handle('post', self.urls['Hb55WHGTZ'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)

    def JXbPQwCVMKBn(self):
        """获取销售单号"""
        return self._get_field_copy_value('xTgxXhKIdF5f', 'main', 'orderNo')


class LnfQBDqBvleaE2O0412qk(BaseApi):
    """配件管理|入库管理|分拣列表"""

    def IB3TfKONJp2x(self, headers=None, i=None, num=1, size=1000):
        """分拣列表
        i: 分拣状态 1未分拣 2已分拣
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'sortationStatus': i}
        response = self.request_handle('post', self.urls['QTembQdXx'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def PaJDXqH7P5A0(self, headers=None):
        """包裹视频"""
        headers = headers or self.headers['main']
        data = {'articlesType': 2, 'logisticsNo': self.YwVSc3Nv5QU3()}
        response = self.request_handle('post', self.urls['GVeaSBtQu'], data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            return response.json()
        return None

    def YwVSc3Nv5QU3(self):
        """获取物流单号"""
        return self._get_field_copy_value('IB3TfKONJp2x', 'main', 'logisticsNo')


class Ved7inYORAmtB67RNFcCG(BaseApi):
    """配件管理|配件统计|维修明细"""

    def tHXpLoSvaDSH(self, month=1, headers=None, num=1, size=1000):
        """维修明细列表
         month：1本月 2上月
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), "month": month}
        response = self.request_handle('post', self.urls['tzNKqu20B'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def AHDIlJyWnSd1(self, headers=None):
        """维修消耗 详情"""
        headers = headers or self.headers['main']
        statics = self.tHXpLoSvaDSH()
        data = {**self.get_page_params(), "modelId": statics[0]['modelId'], "brandId": statics[0]['brandId'], "accessoryNo": statics[0]['accessoryNo']}
        response = self.request_handle('post', self.urls['vwDBMHEOa'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class DgyYP8ygDMIIeEEXHuLbW(BaseApi):
    """配件管理|配件库存|库存调拨"""

    def QGOxnhn1YW7x(self, headers=None, num=1, size=1000, i=None):
        """库存调拨列表
        i: 接收状态 1待接收 2部分接收 3已完成 4已撤销
        """
        headers = headers or self.headers['main']
        data = {'articlesType': '2', **self.get_page_params(num, size), 'status': i}
        response = self.request_handle('post', self.urls['Vqx4RAgDI'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def ZT5PSTjrth3p(self, headers=None):
        """库存调拨详情"""
        headers = headers or self.headers['main']
        obj = self.QGOxnhn1YW7x()
        data = {'articlesType': '2', 'id': obj[0]['id']}
        response = self.request_handle('post', self.urls['mMiwJEj2a'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)

    def rpHRNtqAmFV0(self, headers=None):
        """撤销调拨详情"""
        headers = headers or self.headers['main']
        obj = self.QGOxnhn1YW7x()
        data = {'articlesType': '2', 'id': obj[0]['id']}
        response = self.request_handle('post', self.urls['IRy0rknua'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)


if __name__ == '__main__':
    api = AMaXd2PkDsrT5cj1SArOe()
    result = api.NPp0AJ9kG7cr()
    print(json.dumps(result, indent=4, ensure_ascii=False))
