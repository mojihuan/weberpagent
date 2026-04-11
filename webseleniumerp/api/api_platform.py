# coding: utf-8
import json
from common.base_api import BaseApi
from config.user_info import INFO


class VvIs5cfbQJsDekJKZZOr1(BaseApi):
    """平台管理|虚拟库存|虚拟库存列表"""

    def ppkzpNKKe2Vc(self, i=None, headers=None):
        """虚拟库存列表
         i：物品状态 1质检中 2待销售 3销售中 4已销售 5待平台确认 6报价确认 7质检完成 8退货中 9退货已出库 10已退货
        """
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'status': i, 'inspectionCenterCode': INFO['merchant_id']}
        response = self.request_handle('post', self.urls['tAKgvfLvB'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def XFXlf5bIC1O5(self):
        """获取id"""
        return self._get_field_copy_value('ppkzpNKKe2Vc', 'super', 'id')

    def A22N4FgvPpHd(self):
        """ 获取物品编号"""
        return self._get_field_copy_value('ppkzpNKKe2Vc', 'super', 'articlesNo')


class HnlUtAPz07JtZRXny3Ogs(BaseApi):
    """平台管理|虚拟库存|上拍商品管理"""

    def FgMfvbUdU4qZ(self, headers=None, i=None):
        """上拍商品管理列表
         i：类型 1可上拍商品 2已上拍商品 0待定价物品
        """
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'type': i, 'centerId': INFO['check_the_center_id']}
        response = self.request_handle('post', self.urls['uV8Nj8RVH'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def LWfPhO8u3XJv(self, headers=None, i=None):
        """选择场次列表
        i：类型 1暗拍 2直拍
        """
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'marketCategory': i}
        response = self.request_handle('post', self.urls['mPv6oZCRH'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class VqmFuQKXRJ3TARMX1GAfs(BaseApi):
    """平台管理|配置中心|拍机业务设置"""

    def I9pgV4Dd3Wgu(self, headers=None):
        """基础配置-参数配置"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'businessType': 2}
        response = self.request_handle('post', self.urls['S0bWhpj4F'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def CrwHoYGUYpuu(self, headers=None):
        """基础配置-字典配置"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'businessType': 1}
        response = self.request_handle('post', self.urls['iIToR3jDm'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class T89hWigwbvtFYDRF2euou(BaseApi):
    """平台管理|配置中心|费用配置"""

    def njgdULIGWCxB(self, headers=None):
        """费用配置列表"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['L97maiVGY'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class MtD5iVefHiu23ZJ4o2jBd(BaseApi):
    """平台管理|配置中心|保证金配置"""

    def xjCwrNtAQMsv(self, headers=None):
        """保证金配置列表"""
        headers = headers or self.headers['super']
        data = {}
        response = self.request_handle('post', self.urls['Jj2fOjYCF'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res


class Oo2tySvRkxOQdjcwVsPry(BaseApi):
    """平台管理|壹准拍机|售后管理|售后订单"""

    def LCazQKpPMzmB(self, i=None, headers=None):
        """售后订单列表,：
        i 订单状态
        [2]待申诉 [1]线上审核 [3]线上拒退 [4]申诉中 [5]补差成功 [6]可补差
        [7]待寄回 [8]超时取消 [9]主动取消 [10]待接收 [11]实物复检 [12]实物拒退 [13]退货成功
        """
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), "afterStatusList": i}
        response = self.request_handle('post', self.urls['ddaMclybo'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def dFbRzwmcHQRf(self):
        """获取售后物品编号"""
        return self._get_field_copy_value('LCazQKpPMzmB', 'super', 'articlesNo')


class NLUkzWtFzjZSO2vR8Yhhb(BaseApi):
    """平台管理|壹准拍机|售后管理|申诉管理"""

    def nG1FaeCsMOtb(self, i=None, headers=None):
        """申述管理列表,：
         i订单类型 0待处理 2申诉成功 2申诉失败 3申诉取消
        """
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), "status": i}
        response = self.request_handle('post', self.urls['eWq0C2yoz'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class LHYy8CC7VJiSyR9H29WgO(BaseApi):
    """平台管理|壹准拍机|售后管理|售后退货管理"""

    def we6Ef70NV5qS(self, headers=None):
        """可售后属性列表"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['dLqTKKRGg'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class JnF4aHEwtkuKPhtUYGWbt(BaseApi):
    """平台管理|壹准拍机|售后管理|可售后属性"""

    def LKvaVBaInsWa(self, headers=None):
        """可售后属性列表"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['dLqTKKRGg'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class VXQYCDSIeRducn3qAERck(BaseApi):
    """平台管理|分销管理|分销商管理"""

    def bnN0B9o9JzSF(self, headers=None):
        """分销商管理"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['Vk2g3rn5q'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class Ytfk1ZdYSOkWNYvSBQapC(BaseApi):
    """平台管理|分销管理|分销商业绩"""

    def r8JT4wfYZtDC(self, headers=None):
        """分销商业绩"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['w7H2hlCaw'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class YXBfeAUatPGzdHgCjYWrZ(BaseApi):
    """平台管理|分销管理|分销商角色"""

    def nYlU4exxleK0(self, headers=None):
        """分销商角色"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['AWj5ltFYH'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class XbCT74c5w1sqFk7I7vMKO(BaseApi):
    """平台管理|帮卖管理|帮卖商家配置"""

    def qoCQrZuPqjvr(self, headers=None):
        """帮卖商家配置"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['Gp04EyJh4'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class Hqy4rq1tglWDYR9RHDaRw(BaseApi):
    """平台管理|帮卖管理|帮卖交易列表"""

    def MSuPibOGvfyY(self, headers=None):
        """帮卖交易列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['II5MugGsC'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class EYMR4spDlh51z47tfy9AL(BaseApi):
    """平台管理|运营中心|订单管理"""

    def yUDjnTJ2lpoZ(self, i=None, headers=None):
        """订单管理列表
         i订单状态 1：待发货2：待取件3：待收货4：已收货5：已完成6：已取消7：已退货
        """
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'status': i}
        response = self.request_handle('post', self.urls['TdwSRYY7R'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class ZhDuvKCTZQ9pe3cXB6OmY(BaseApi):
    """平台管理|运营中心|退货管理"""

    def d2lxrrfwdb7O(self, headers=None):
        """待退货 商户明细"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'status': "1"}
        response = self.request_handle('post', self.urls['EJD6NTpl7'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def uuZoy57lInAn(self, headers=None):
        """待退货 物品明细"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'status': "1"}
        response = self.request_handle('post', self.urls['qVupO6Qqs'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def SO58avAIlL7g(self, headers=None):
        """待取货 物品明细"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'status': "2"}
        response = self.request_handle('post', self.urls['qVupO6Qqs'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def ZdXIkw9sxZAk(self, headers=None):
        """退货已出库 批次明细"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'status': "3"}
        response = self.request_handle('post', self.urls['MHQy0WxZt'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def h3uuaYt8WaR2(self, headers=None):
        """退货已出库 物品明细"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'status': "3"}
        response = self.request_handle('post', self.urls['qVupO6Qqs'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def Us3WaJ4K0n9A(self, headers=None):
        """已退货 批次明细"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'status': "4"}
        response = self.request_handle('post', self.urls['MHQy0WxZt'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def stWA8uYaeMMm(self, headers=None):
        """已退货 物品明细"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'status': "4"}
        response = self.request_handle('post', self.urls['qVupO6Qqs'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def mxoe4reprVZE(self, headers=None):
        """取消退货 物品明细"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'status': "5"}
        response = self.request_handle('post', self.urls['qVupO6Qqs'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class YVqIQus8roZWysBseaMP0(BaseApi):
    """平台管理|运营中心|待指定物品"""

    def DSpcSKcA7pw5(self, headers=None):
        """待指定物品列表"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params(num=1, size=999999), 'inspectionCenterCode': INFO['merchant_id']}
        response = self.request_handle('post', self.urls['SOp0BpTwW'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list, index=-1)
        self.make_pkl_file(res)
        return res


class LynR3DTFTfRXNn8sQhsvK(BaseApi):
    """平台管理|运营中心|规则管理"""

    def nCckhPtRwXxG(self, headers=None):
        """规则管理列表"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['VogF63A70'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class EEdalTouEaLL3VEx3wMnz(BaseApi):
    """平台管理|卖场管理|暗拍卖场列表"""

    def pzCWj3Ksrd4P(self, i=1, headers=None):
        """暗拍卖场列表
        i；1-已上架；2-待上架；3-已下架
        """
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), "marketCategory": "1", "status": i}
        response = self.request_handle('post', self.urls['tKeaCloea'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def TezdhkF6QXGQ(self, headers=None):
        """编辑详情"""
        obj = self.JeJHA3LbooLc()
        headers = headers or self.headers['super']
        data = {"id": obj}
        response = self.request_handle('post', self.urls['BGdSAuriF'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)

    def i2hsWJeCQxKo(self, headers=None):
        """查看场次详情 场次列表"""
        obj = self.JeJHA3LbooLc()
        headers = headers or self.headers['super']
        data = {'erpEndTime': self.get_the_date(days=2), 'erpStartTime': self.get_the_date(), 'marketId': obj}
        response = self.request_handle('post', self.urls['mfzdItiJh'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def q5mIVNB1zQPk(self, headers=None):
        """查看场次详情 商品列表"""
        obj = self.JeJHA3LbooLc()
        obj_2 = self.afxWrJz45Gw3()
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'marketId': obj, 'sessionId': obj_2}
        response = self.request_handle('post', self.urls['uV8Nj8RVH'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def JeJHA3LbooLc(self):
        """获取id"""
        return self._get_field_copy_value('pzCWj3Ksrd4P', 'super', 'id')

    def afxWrJz45Gw3(self):
        """获取查看场次详情 场次列表id"""
        return self._get_field_copy_value('i2hsWJeCQxKo', 'super', 'id')


class BaxRsHzRpoNsTb8fnSa9e(BaseApi):
    """平台管理|卖场管理|直拍卖场列表"""

    def gXHSWafumwCe(self, headers=None, i=None):
        """直拍卖场列表
         i: 上架状态 1已上架 2待上架 3已下架
        """
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'marketCategory': 2, 'status': i}
        response = self.request_handle('post', self.urls['tKeaCloea'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def wpfOmsjWdkny(self, headers=None):
        """编辑详情"""
        obj = self.KnWU9OyLrgrD()
        headers = headers or self.headers['super']
        data = {"id": obj}
        response = self.request_handle('post', self.urls['BGdSAuriF'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)

    def oTwifIq7ER6o(self, headers=None):
        """查看场次详情 场次列表"""
        obj = self.KnWU9OyLrgrD()
        headers = headers or self.headers['super']
        data = {'erpEndTime': self.get_the_date(days=2), 'erpStartTime': self.get_the_date(), 'marketId': obj}
        response = self.request_handle('post', self.urls['mfzdItiJh'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def sh3cTsLUbzwu(self, headers=None):
        """查看场次详情 商品列表"""
        obj = self.KnWU9OyLrgrD()
        obj_2 = self.R8sRFGd5S7dQ()
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'marketId': obj, 'sessionId': obj_2}
        response = self.request_handle('post', self.urls['uV8Nj8RVH'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def KnWU9OyLrgrD(self):
        """获取id"""
        return self._get_field_copy_value('gXHSWafumwCe', 'super', 'id')

    def R8sRFGd5S7dQ(self):
        """获取查看场次详情 场次列表id"""
        return self._get_field_copy_value('oTwifIq7ER6o', 'super', 'id')


class Hh5PvL58jP16yZeEgRm1c(BaseApi):
    """平台管理|卖场管理|销售看板数据"""

    def BsXn59thmbp9(self, headers=None):
        """今日竞拍实时数据"""
        headers = headers or self.headers['super']
        response = self.request_handle('get', self.urls['udXx7AJaG'], headers=headers)
        return self.get_response_data(response, 'data', dict)

    def sMyMF5ETv83R(self, headers=None):
        """规则管理列表"""
        headers = headers or self.headers['super']
        data = {"pageNum": 1, "pageSize": 999}
        response = self.request_handle('post', self.urls['Bkw34z3HH'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def Oo2xQxelpoiH(self):
        """获取进行中的场次"""
        return self._get_field_copy_value('BsXn59thmbp9', 'super', 'auctionCount')

    def kyF9SxkEVrV3(self):
        """获取进行中的场次"""
        return self._get_field_copy_value('BsXn59thmbp9', 'super', 'waitCount')


class QzSOsqMQEUO1fdepLsWr2(BaseApi):
    """平台管理|物流折扣配置"""

    def c1tR3rvjp8bS(self, headers=None):
        """物流折扣配置"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['wcx9hP4XN'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class EXielc1Ue5RSZHZmlF8kr(BaseApi):
    """平台管理|订单管理|商户物流订单"""

    def AU9wEnZZksLz(self, headers=None):
        """商户物流订单列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['AS8qQMjCV'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class IyY9m4jNrW6D0vQNpkgVH(BaseApi):
    """平台管理|消息管理|消息发布列表"""

    def cCF5oVBu3uHW(self, headers=None):
        """回收商发布列表"""
        headers = headers or self.headers['platform']
        data = {"publishSource": "2", "selectType": "1", **self.get_page_params()}
        response = self.request_handle('post', self.urls['W6umEZcEP'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def fJguQW48NLCH(self, headers=None):
        """平台发布列表"""
        headers = headers or self.headers['platform']
        data = {"selectType": "1", "publishSource": "1", **self.get_page_params()}
        response = self.request_handle('post', self.urls['W6umEZcEP'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def TtANqjKOor4M(self, headers=None):
        """消息发布记录"""
        headers = headers or self.headers['platform']
        data = {"selectType": "1", **self.get_page_params()}
        response = self.request_handle('post', self.urls['W6umEZcEP'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class A9zDd08nxZUQb9YOQEpNw(BaseApi):
    """平台管理|同售管理|95分商品列表(运营)"""

    def NvYpczu1AAs6(self, headers=None):
        """95分商品列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params(), "platformType": "2"}
        response = self.request_handle('post', self.urls['R7Q5WFBoA'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class V3LpfoN0H354ztNVHPWtf(BaseApi):
    """平台管理|订单管理|订单审核"""

    def TdbQGLoDJMFo(self, headers=None):
        """订单审核"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['yU8PseXLe'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class JzWIonT4ru2daU1uIX7tu(BaseApi):
    """平台管理|订单管理|商户订单"""

    def cnjj3mi7iYuP(self, headers=None):
        """商户订单列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['AS8qQMjCV'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class Nfy2c8myIXt01fkNbYzIH(BaseApi):
    """平台管理|产品管理"""

    def LJ9a2QOYDxTG(self, headers=None):
        """产品管理"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params(), "menuCheckStrictly": True}
        response = self.request_handle('post', self.urls['w559A9DPS'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class AlZdueYspz0c2CHbT7D29(BaseApi):
    """平台管理|同售管理|商品审核"""

    def eOv7DqFBIwVc(self, headers=None):
        """商品审核"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['uq6Ghpj1Y'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def ILGktF8orGlt(self, headers=None):
        """商品审核-待审核列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params(), "auditState": "1"}
        response = self.request_handle('post', self.urls['uq6Ghpj1Y'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class VzF4todMPF4UN7aNpYfCs(BaseApi):
    """平台管理|商户管理"""

    def LZRK5ZWFXGxQ(self, headers=None, i=None):
        """商户管理列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params(), "name": i}
        response = self.request_handle('post', self.urls['WKWODuXca'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)

    def eXKDs5mfSsmy(self):
        """获取vice账号手机号"""
        return self._get_field_copy_value('LZRK5ZWFXGxQ', 'platform', 'phone', i=INFO['vice_sales_customer_name'])

    def OebN1M0GCfbt(self):
        """获取主账号手机号"""
        return self._get_field_copy_value('LZRK5ZWFXGxQ', 'platform', 'phone', i=INFO['main_username'])

    def nB1TOOFzla57(self):
        """获取主账号商户id"""
        return self._get_field_copy_value('LZRK5ZWFXGxQ', 'super', 'code', i=INFO['main_username'])

    def HQFhRAOshzqB(self):
        """获取拍机账号商户id"""
        return self._get_field_copy_value('LZRK5ZWFXGxQ', 'super', 'code', i=INFO['camera_username'])

    def TqsIFsirS5UH(self):
        """获取拍机账号手机号"""
        return self._get_field_copy_value('LZRK5ZWFXGxQ', 'platform', 'phone', i=INFO['camera_username'])


class Ia8TAeTwpzSbMJhMqMGeP(BaseApi):
    """平台管理|报价管理|报价单列表"""

    def XMhYksAZ31Sj(self, headers=None):
        """报价单列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['U9rlFOTjS'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class Cx03iG0b0HffBc6QIybob(BaseApi):
    """平台管理|报价管理|酷换机计算规则"""

    def zzKGcGU9R6QS(self, headers=None):
        """酷换机计算规则"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['w591cTaDN'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class VV6MEAkoARZ3tJkxrgAJQ(BaseApi):
    """平台管理|报价管理|配置管理|扣费项管理"""

    def Aj4G89358vHj(self, headers=None):
        """扣费项管理"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['CPWrIwu1G'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class Fo9i3p1gbYnMbfcoKO4Ab(BaseApi):
    """平台管理|报价管理|配置管理|等级说明"""

    def kIjoyh41xtRo(self, headers=None):
        """等级说明"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['rc8HhZLou'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class Mrn5mkXrQtUxGX77fKlLG(BaseApi):
    """平台管理|报价管理|配置管理|成色等级"""

    def srFImFxB07lw(self, headers=None):
        """成色等级列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['jpphWrRHi'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class RsUEZaX7uPLdqTLqahbEF(BaseApi):
    """平台管理|报价管理|配置管理|回收菜单"""

    def sS7vh5QFledx(self, headers=None):
        """回收菜单"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['Y0DF5XgXm'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class VPmXLVY9qUyo0MquqQM5l(BaseApi):
    """平台管理|报价管理|发布记录"""

    def oyBmABjvNLyJ(self, headers=None):
        """发布记录"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['Fvzd81qMU'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class CzsfSvKVWVl8smuDsm9oo(BaseApi):
    """平台管理|报价管理|回收商报价单"""

    def eMzceqVzVn1j(self, headers=None):
        """回收商报价单"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['VpsvKLidA'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PBHSYRzyH8n7CGHzQ32rt(BaseApi):
    """平台管理|同售管理|同售账号管理"""

    def bJgr1cdPXnyC(self, headers=None):
        """同售账号列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['Modqr5GuV'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class VkDFQL4P7JV5zlqJvTkW4(BaseApi):
    """平台管理|同售管理|得物95分|95分商品列表"""

    def K8HcZzWnfFKA(self, headers=None):
        """95分商品列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params(), "platformType": 2}
        response = self.request_handle('post', self.urls['rA17OKgRP'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class MzJDKTXQINE9ccFuK4sRv(BaseApi):
    """平台管理|同售管理|得物95分|95分订单列表"""

    def GZ55wWMkxBLQ(self, headers=None):
        """95分订单列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['rA17OKgRP'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class G60ABTFGxfLhcUe1XGcts(BaseApi):
    """平台管理|得物95分|后验回退列表"""

    def iDcK9DRXViv7(self, headers=None):
        """后验回退列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['EgOi1Fk39'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class Uhjrkj6laYG9czKf8q58N(BaseApi):
    """平台管理|同售管理|得物95分|售后列表"""

    def X9VCRMczplTY(self, headers=None):
        """售后列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params(), "platformType": 2}
        response = self.request_handle('post', self.urls['upfrtrvip'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class IDf9xXzZBNkyUKz988lfE(BaseApi):
    """平台管理|同售管理|服务费管理"""

    def K5BCL3d8BkOH(self, headers=None):
        """服务费管理"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['goV7j5LRI'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class I19JTCjpiWeUghsgi1Ipn(BaseApi):
    """平台管理|同售管理|同售托管|物流列表"""

    def VIm8WPUVCbYl(self, headers=None):
        """物流列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['n6LlUm9hZ'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class XDZnMlIwjNIzNaEf5sAdS(BaseApi):
    """平台管理|商户基础数据管理|日常费用管理"""

    def wLqvf42V9qak(self, headers=None):
        """日常费用管理"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['cEb6e4iyX'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class EVDuJGBUgp01Bc6BoPZad(BaseApi):
    """平台管理|同售管理|同售托管|95分订单列表"""

    def EBbpwfsykAWI(self, headers=None):
        """95分订单列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['rA17OKgRP'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class BCYtt2LfzDKfUwMV47CkL(BaseApi):
    """平台管理|同售管理|同售托管|95分售后列表"""

    def gSPOro9nhRSD(self, headers=None):
        """95分售后列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params(), "platformType": 2}
        response = self.request_handle('post', self.urls['upfrtrvip'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class ALFIj1WUIA9rUMDESzmJb(BaseApi):
    """平台管理|同售管理|赔付订单列表"""

    def AuZUnO6UOD9N(self, headers=None):
        """赔付订单列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params(), "orderStatus": "0"}
        response = self.request_handle('post', self.urls['pFQqICBq5'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class Eof6pcUoS4KaKwBODptvM(BaseApi):
    """平台管理|同售管理|同售托管|质检记录"""

    def bQbdp9CUkLbf(self, headers=None):
        """质检记录"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['Zb5DJdOLj'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class Y7RTFS6JaQgVNexKIQk0X(BaseApi):
    """平台管理|同售管理|同售发货地址管理"""

    def xjbll69BHvB4(self, headers=None):
        """同售发货地址管理"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['pFQqICBq5'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class D3IOEiKYJhokqxB9wyPuB(BaseApi):
    """平台管理|发送短信记录"""

    def JCWg0gbCaA2O(self, headers=None):
        """服务费管理"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['发送短信记录'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class Jq5leU3IZJ4Ju5wWEYBPW(BaseApi):
    """平台管理|同售管理|闲鱼订单列表(运营)"""

    def oAGyCTK1ZbOq(self, headers=None):
        """闲鱼订单列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['aaAvwoYHE'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class E9yM7zpEVVWYKvAO8pwPI(BaseApi):
    """平台管理|钱包配置"""

    def mXw74NvYjIrt(self, headers=None):
        """钱包配置"""
        headers = headers or self.headers['platform']
        response = self.request_handle('post', self.urls['NOiVlKtsQ'], data=json.dumps({}), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class ZbEgGzV6hU7xnVY1Vi2k1(BaseApi):
    """平台管理|同售管理|闲鱼严选|商品列表"""

    def KeLiuIhf52Qx(self, headers=None):
        """商品列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['XvPw32gT0'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class O5nfF9pTAqR1kRn1a1Ql4(BaseApi):
    """平台管理|同售管理|闲鱼严选|订单列表"""

    def gWTxQ5SCndH7(self, headers=None):
        """订单列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['aaAvwoYHE'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class B6ZQNG4fsbM7Csackosvr(BaseApi):
    """平台管理|同售管理|闲鱼严选|售后列表"""

    def IEGMiWSvlQ05(self, headers=None):
        """售后列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['upfrtrvip'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class VERu1xLXu1M9TXV9BXB8X(BaseApi):
    """平台管理|壹准APP功能管理"""

    def FdilbeKD2ojN(self, headers=None):
        """壹准APP功能管理"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['zHhryYCn7'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class KX0k4AlvPF24ByDxyBo28(BaseApi):
    """平台管理|壹准速收|横幅配置"""

    def C5sBkrvwumHi(self, headers=None):
        """横幅配置"""
        if headers is None:
            headers = self.headers['platform']
        data = {**self.get_page_params(), "configType": "1"}
        response = self.request_handle('post', self.urls['ekSQK4qAH'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class NbVb8wzwK4ddsxGHdOhH7(BaseApi):
    """平台管理|壹准速收|会话管理|聊天记录列表"""

    def wvVYytumYUJG(self, headers=None):
        """聊天记录列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['AuaaGweXz'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class RTZJGjcQh5CsFix4WL7o0(BaseApi):
    """平台管理|壹准速收|回收商管理"""

    def fyFdCyDNK6RE(self, headers=None):
        """商家管理"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params(), "selectType": "2"}
        response = self.request_handle('post', self.urls['Sv7Uyua0R'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class Fgy0WqxEK0gtV68ujoqKy(BaseApi):
    """平台管理|壹准速收|回收订单"""

    def eUDwBxLeg49P(self, headers=None):
        """回收订单"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params(), "userType": "1"}
        response = self.request_handle('post', self.urls['Oby8T6NsQ'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class Xa8F6wAwU5kZf4ozr94Pq(BaseApi):
    """平台管理|壹准速收|回收商管理"""

    def m3IgRHgAuJ2B(self, headers=None):
        """回收商管理"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['UQSfsbjGf'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class Qx3W1mlHq0O86FbxsqVd6(BaseApi):
    """平台管理|壹准速收|服务费配置"""

    def AFw9MA8oyK0r(self, headers=None):
        """服务费配置"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['JByvkmYei'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class SQnk0n1M9pDW8nxiq45A7(BaseApi):
    """平台管理|壹准速收|到货签收"""

    def PaGR7cZteeFu(self, headers=None):
        """到货签收"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['Ktt6XhtcD'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class B63gyanXogW9NpUu1Gr1K(BaseApi):
    """平台管理|运营中心|验机中心管理"""

    def cQkBD5in87Ys(self, headers=None, num=1, size=1000, i=INFO['merchant_id']):
        """验机中心管理列表"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params(num, size), 'operationCenterTenantId': i}
        response = self.request_handle('post', self.urls['FNpafJID0'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def t25mwHNJH3Is(self):
        """获取验机中心id"""
        return self._get_field_copy_value('cQkBD5in87Ys', 'super', 'id')

    def O26J15oTsTAs(self):
        """获取验机中心code"""
        return self._get_field_copy_value('cQkBD5in87Ys', 'super', 'operationCenterTenantId')

    def gMPvjk57y0hb(self):
        """获取验机中心名称"""
        return self._get_field_copy_value('cQkBD5in87Ys', 'super', 'operationCenterName')

    def UoR79Z3TA8yQ(self):
        """获取验机中心id"""
        return self._get_field_copy_value('cQkBD5in87Ys', 'super', 'id', i=INFO['camera_merchant_id'])

    def CTfDozPTnUaw(self):
        """获取验机中心code"""
        return self._get_field_copy_value('cQkBD5in87Ys', 'super', 'operationCenterTenantId', i=INFO['camera_merchant_id'])

    def tfLR31KkCRRN(self):
        """获取验机中心名称"""
        return self._get_field_copy_value('cQkBD5in87Ys', 'super', 'operationCenterName', i=INFO['camera_merchant_id'])


class O8pQKRWQmOd9o1cvDbdUk(BaseApi):
    """平台管理|机型价格|Tob保卖|价格列表"""

    def __init__(self):
        super().__init__()
        self.obj = MJGUWnFcIoUVUzhQ9aF1f()

    def oGpWQ5mcWZks(self, headers=None):
        """价格列表"""
        res = self.obj.bfeSgTrgWEw9()
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'productType': "1", 'quotationPriceTemplateId': res}
        response = self.request_handle('post', self.urls['DL0CXNPEq'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class Be8HREFOSd1KIsxYdCk03(BaseApi):
    """平台管理|机型价格|ToC速收|价格列表"""

    def __init__(self):
        super().__init__()
        self.obj = MJGUWnFcIoUVUzhQ9aF1f()

    def sgQxP77G16dB(self, headers=None):
        """价格列表"""
        res = self.obj.bfeSgTrgWEw9()
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'productType': "1", 'quotationPriceTemplateId': res}
        response = self.request_handle('post', self.urls['kCUWc9znM'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class MJGUWnFcIoUVUzhQ9aF1f(BaseApi):
    """平台管理|机型价格|价格模板"""

    def PuRX9X2tuZTq(self, headers=None):
        """价格模板列表"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['Gp0yyXjAx'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def bfeSgTrgWEw9(self):
        """获取id"""
        return self._get_field_copy_value('PuRX9X2tuZTq', 'super', 'id', index=2)


class MbEOJOMeeNK8Bh8ID3wjC(BaseApi):
    """平台管理|机型价格|发布记录|加盟商发布记录"""


class GQCMOd03lD9AA0GAC8qlK(BaseApi):
    """平台管理|机型价格|发布记录|平台发布记录"""


class Px772lOpt0hHK2VCtjpyi(BaseApi):
    """平台管理|机型价格|Tob保卖|计算规则"""


class CcFJHvyyWJPc0qXidiPDN(BaseApi):
    """平台管理|机型价格|Tob保卖|增扣项管理"""


class HWay2sEuMajwUXwsYw1bs(BaseApi):
    """平台管理|交易中心"""

    def HtoIMIElF6hz(self, headers=None, i=None):
        """销售商品交易"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params()}
        if i:
            data['articlesStatus'] = i
        response = self.request_handle('post', self.urls['BBekIPpOf'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = BaxRsHzRpoNsTb8fnSa9e()
    result = api.oTwifIq7ER6o()
    print(json.dumps(result, indent=4, ensure_ascii=False))
