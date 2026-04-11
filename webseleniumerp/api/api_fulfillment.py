# coding: utf-8
import json
from common.base_api import BaseApi
from config.user_info import INFO


class RjVgo4LDzg4voonKUBXr1(BaseApi):
    """运营中心|待报价物品"""

    def vSNmU0ZwGwPu(self, headers=None, num=1, size=9999):
        """待报价物品列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['Cgkp2GLDz'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list, index=-1)


class VzruD2bzEUPV1JJY9d6vF(BaseApi):
    """运营中心|订单管理"""

    def G1ZATPtlzjWF(self, i=None, headers=None, num=1, size=9999):
        """订单列表
         i：订单状态 1待发货 2待取件 3待收货 4已收货 5已完成 6已取消 7已退货
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'status': i}
        response = self.request_handle('post', self.urls['ZTpQ2Sq97'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def k5vJMUZAXDOF(self, i=None, headers=None, num=1, size=9999):
        """订单列表
         i：订单状态 1待发货 2待取件 3待收货 4已收货 5已完成 6已取消 7已退货
        """
        headers = headers or self.headers['camera']
        data = {**self.get_page_params(num, size), 'status': i}
        response = self.request_handle('post', self.urls['ZTpQ2Sq97'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def hDleXL3IWX4c(self, index=None, i=None, headers=None):
        """
        获取订单列表中指定索引的数据
         index: 索引位置（从0开始）
         i：订单状态 1待发货 2待取件 3待收货 4已收货 5已完成 6已取消 7已退货
        指定索引的订单数据或None（如果索引超出范围）
        """
        obj = self.G1ZATPtlzjWF(i=i, headers=headers)
        if len(obj) > index:
            return obj[index]
        return None

    def URWCKM7vfuMg(self, headers=None):
        """物品列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['wKFkRVWzm'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def ipKPUn6OqOHR(self, index=0, i=None):
        """获取订单列表 订单号"""
        return self._get_field_copy_value('G1ZATPtlzjWF', 'main', 'orderNo', index=index, i=i)

    def pgML2TdmmKju(self, index=0, i=None):
        """获取订单列表 物流单号"""
        return self._get_field_copy_value('G1ZATPtlzjWF', 'main', 'expressNo', index=index, i=i)


class FYXRA4IxF49PvhUCLpp5Z(BaseApi):
    """运营中心|质检管理"""

    def KhNjoVcM4iuf(self, headers=None):
        """待领取物品列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['lLNjlBFwd'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def OHXGClp3BoJm(self, headers=None):
        """质检中物品列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['Fw8Yxg0Hl'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def eDr2hpq6xEBa(self, headers=None):
        """重验申请列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['Fwvafb0zd'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def oSzj9Md6vHyl(self, headers=None, num=1, size=9999):
        """已质检物品列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['TMHiA7cq7'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def YkybIUUCs2Dh(self, headers=None, i=None, num=1, size=9999):
        """商品图拍摄列表
        i类型 1未上传 2已上传
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'goodsImageStatus': i}
        response = self.request_handle('post', self.urls['vCrkCYa9l'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def AY6K1XbHNTzW(self, headers=None):
        """质检模版"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'brandId': 1, 'categoryId': 1}
        response = self.request_handle('post', self.urls['ioMf84yoL'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def lUNvxi3R9RxT(self):
        """获取物品编号"""
        return self._get_field_copy_value('oSzj9Md6vHyl', 'main', 'articlesNo')


class M4Xsay25almyg0RzXz4ui(BaseApi):
    """运营中心|退货管理"""

    def WCB6NcIMpsMe(self, i=None, headers=None):
        """商户明细列表
         i：订单状态 1待退货 2待取货 3退货已出库 4已退货 5已取消
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'status': i}
        response = self.request_handle('post', self.urls['vB1kYeyMt'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def ua4JlujLXZDP(self, i=None, headers=None):
        """物品明细列表
         i：订单状态 1待退货 2待取货 3退货已出库 4已退货 5已取消
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'status': i}
        response = self.request_handle('post', self.urls['LPDbrxAcE'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def VnssCpqfEIlk(self, i=None, headers=None):
        """批次明细列表
         i：订单状态 1待退货 2待取货 3退货已出库 4已退货 5已取消
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'status': i}
        response = self.request_handle('post', self.urls['vjV7bkTSW'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class KgbSrz63njmC8XfrU1jty(BaseApi):
    """运营中心|收货入库"""

    def __init__(self):
        super().__init__()
        self.obj = VzruD2bzEUPV1JJY9d6vF()
        self.obj_2 = CO4AXsbHeeFE7zOfrBooq()

    def skBKV5OKhyz7(self, headers=None):
        """搜索保卖订单号"""
        order_no = self.obj.G1ZATPtlzjWF(i=3)
        headers = headers or self.headers['main']
        data = {"consignmentOrderNo": order_no[0]['orderNo']}
        response = self.request_handle('post', self.urls['cy2zWx61q'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)

    def jxEKaglEujSi(self, headers=None):
        """搜索拍机订单号"""
        obj = self.obj_2.v9pReyiWxwdU()
        headers = headers or self.headers['main']
        data = {"consignmentOrderNo": obj}
        response = self.request_handle('post', self.urls['cy2zWx61q'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)

    def h1cdqp8AtfOD(self, headers=None):
        """搜索保卖物流单号"""
        obj = self.obj.G1ZATPtlzjWF(i=3)
        headers = headers or self.headers['main']
        data = {"expressNo": obj[0]['expressNo']}
        response = self.request_handle('post', self.urls['cy2zWx61q'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)


class PGuLxDEgVXFhGrj7xp60p(BaseApi):
    """运营中心|销售商品交易"""

    def ulF6xKNRe3LI(self, headers=None, num=1, size=10, i=None):
        """销售商品交易列表
         i：订单状态 1待支付 2待发货 3待收货 4已收货 5已售后 6已取消"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        if i is not None:
            data['articlesStatus'] = i
        response = self.request_handle('post', self.urls['LkwjB3Lu2'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class KsJkf77pdK7sRJY6s9lfO(BaseApi):
    """运营中心|bot订单管理"""

    def FTdfLz90lzeR(self, headers=None, num=1, size=9999):
        """bot订单管理列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['Vno40ta8N'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def DCWqFgYks8xB(self):
        """获取下单编号"""
        return self._get_field_copy_value('FTdfLz90lzeR', 'main', 'orderNo')


class Tx4NUJiUGgVdeyFoLPT4j(BaseApi):
    """运营中心|bot总订单号"""

    def qXygXo1h2FgH(self, headers=None, num=1, size=9999):
        """bot总订单号列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['lwF18c2BX'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class VnVeCrt7kNUg7iObK5ZBc(BaseApi):
    """运营中心|bot收货入库"""

    def __init__(self):
        super().__init__()
        self.obj = KsJkf77pdK7sRJY6s9lfO()

    def KdrTCtXRVAJ7(self, headers=None):
        """搜索订单号"""
        obj = self.obj.DCWqFgYks8xB()
        headers = headers or self.headers['main']
        data = {"orderNo": obj}
        response = self.request_handle('post', self.urls['mBXZyzKZC'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)


class P0pdI13R4ZjzxgCBkjFKl(BaseApi):
    """运营中心|虚拟库存列表"""

    def mChsU8Yn1eQe(self, headers=None, num=1, size=9999):
        """虚拟库存列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['x13DSAOB9'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class KmxOWBECeMnMqtP1qACyx(BaseApi):
    """运营中心|销售发货管理"""

    def Oqr9od3TrupA(self, headers=None):
        """待发货 按商户"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['BGeHJ0FaH'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def N3GKYzC6P5TZ(self, headers=None):
        """待发货 按物品"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'buyTenantId': INFO['camera_merchant_id']}
        response = self.request_handle('post', self.urls['a6pCe1MMk'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def fNSLGMFC7atc(self, headers=None):
        """待收货 按物品"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'buyTenantId': INFO['camera_merchant_id']}
        response = self.request_handle('post', self.urls['fVAcvbX08'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def clirkK4CTUj0(self, headers=None):
        """待收货 按包裹"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['JQUIwBdeP'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def uByZKczL88yQ(self, headers=None):
        """已收货 按包裹"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['WpjSbG9uV'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def ntnTnNcZjnPi(self, headers=None):
        """已收货 按物品"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'buyTenantId': INFO['camera_merchant_id']}
        response = self.request_handle('post', self.urls['rr6sFUMuf'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def aBsOwxaJzqX0(self):
        """获取平台物品编号"""
        return self._get_field_copy_value('fNSLGMFC7atc', 'main', 'articlesNo')


class M55r2pn7CkJ0DzgKvHhuX(BaseApi):
    """运营中心|物品出库"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = KmxOWBECeMnMqtP1qACyx()

    def OpUzgQkpwsBG(self, headers=None):
        """物品出库列表-销售出库
        """
        obj = self.obj.aBsOwxaJzqX0()
        headers = headers or self.headers['main']
        data = {"articlesNoList": [obj], "status": 1}
        response = self.request_handle('post', self.urls['wv4D6V6Hd'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)


class CO4AXsbHeeFE7zOfrBooq(BaseApi):
    """运营中心|壹准拍机|售后管理|售后订单"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def ZyxQLsb9tEjy(self, headers=None, i=None):
        """售后订单列表
        i 订单状态
        [2]待申诉 [1]线上审核 [3]线上拒退 [4]申诉中 [5]补差成功 [6]可补差
        [7]待寄回 [8]超时取消 [9]主动取消 [10]待接收 [11]实物复检 [12]实物拒退 [13]退货成功
        """
        if i is None:
            i = ['10']
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'centerId': INFO['check_the_center_id'], 'afterStatusList': i}
        response = self.request_handle('post', self.urls['s8YE5XZm5'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def v9pReyiWxwdU(self):
        """获取订单号"""
        return self._get_field_copy_value('ZyxQLsb9tEjy', 'main', 'orderNo')


class YBoIFlRaGyVtfzeObzsmf(BaseApi):
    """运营中心|壹准拍机|售后管理|售后退货管理"""

    def awpLxMlBWNtR(self, headers=None, i=None):
        """售后退货列表
        i 类型  1待退货 2退货已出库
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'returnStatus': i}
        response = self.request_handle('post', self.urls['DhbjKjLCU'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = ()
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
