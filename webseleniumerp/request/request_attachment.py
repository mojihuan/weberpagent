# coding: utf-8
import json
from common.base_api import BaseApi
from common.base_params import InitializeParams, is_performance_close
from common.file_cache_manager import ParamCache
from common.import_desc import *
from config.user_info import INFO


class GGZectTPpu(InitializeParams):
    """配件管理|入库管理|待接收物品"""

    @doc(do56fxxjyrxq3jf44spl)
    @BaseApi.timing_decorator
    def do56fxxjyrxq3jf44spl(self, nocheck=False):
        obj = (self.pc.BF3x3lYIzbEHMnrvr80JO()
               if is_performance_close else self.get_list_data('list_of_items_to_be_received'))
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "accessoryList": [
                {
                    "articlesNo": obj[0]['articlesNo'],
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'Sm7yLloyr', data, 'special', nocheck)

    @doc(wkocqx1u2ihsf32i7co1)
    @BaseApi.timing_decorator
    def wkocqx1u2ihsf32i7co1(self, nocheck=False):
        obj = self.pc.BF3x3lYIzbEHMnrvr80JO()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesNo": obj[0]['articlesNo']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'JKjPTfATh', data, 'special', nocheck)

    @doc(a33hoz47yc05hmc4n7jw)
    @BaseApi.timing_decorator
    def a33hoz47yc05hmc4n7jw(self, nocheck=False):
        obj = self.pc.BF3x3lYIzbEHMnrvr80JO()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "deliveryStartTime": self.get_the_date(),
            "deliveryEndTime": self.get_the_date(days=1),
        }
        self.validate_request_data(data)
        return self._make_request('post', 'JKjPTfATh', data, 'special', nocheck)


class O7NTx8CXpa(InitializeParams):
    """配件管理|移交接收管理|移交物品"""

    @doc(pxx47rbom8j1ul0o5otk)
    @BaseApi.timing_decorator
    def pxx47rbom8j1ul0o5otk(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "accessoryList": [
                {
                    "articlesNo": obj[0]['articlesNo']
                }
            ],
            "deliveryType": "6",
            "userId": INFO['main_user_id'],
            "deliveryRemark": "备注"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'EgcsFMe1T', data, 'main', nocheck)

    @doc(bq9jhuudug0bycyitdho)
    @BaseApi.timing_decorator
    def bq9jhuudug0bycyitdho(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "accessoryList": [
                {
                    "articlesNo": obj[0]['articlesNo']
                }
            ],
            "deliveryType": "5",
            "userId": INFO['main_user_id'],
            "deliveryRemark": "备注"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'EgcsFMe1T', data, 'main', nocheck)

    @doc(qnig8uaqhu0cma5jwmjd)
    @BaseApi.timing_decorator
    def qnig8uaqhu0cma5jwmjd(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "accessoryList": [
                {
                    "articlesNo": obj[0]['articlesNo']
                }
            ],
            "deliveryType": "4",
            "userId": INFO['main_user_id'],
            "deliveryRemark": "备注"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'EgcsFMe1T', data, 'main', nocheck)

    @doc(p0su9g9hxgnbgmkfhw8b)
    @BaseApi.timing_decorator
    def p0su9g9hxgnbgmkfhw8b(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "accessoryList": [
                {
                    "articlesNo": obj[0]['articlesNo']
                }
            ],
            "deliveryType": "3",
            "userId": INFO['main_user_id'],
            "deliveryRemark": "备注"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'EgcsFMe1T', data, 'main', nocheck)

    @doc(vicvey7gwzlidkxk2756)
    @BaseApi.timing_decorator
    def vicvey7gwzlidkxk2756(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "accessoryList": [
                {
                    "articlesNo": obj[0]['articlesNo']
                }
            ],
            "deliveryType": "2",
            "userId": INFO['main_user_id'],
            "deliveryRemark": "备注"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'EgcsFMe1T', data, 'main', nocheck)

    @doc(tvl7rnnvwpmaivcnflho)
    @BaseApi.timing_decorator
    def tvl7rnnvwpmaivcnflho(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "accessoryList": [
                {
                    "articlesNo": obj[0]['articlesNo']
                }
            ],
            "deliveryType": "1",
            "userId": INFO['main_user_id'],
            "deliveryRemark": "备注"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'EgcsFMe1T', data, 'main', nocheck)

    @doc(y1f0go3apyd2gpjhtp6e)
    @BaseApi.timing_decorator
    def y1f0go3apyd2gpjhtp6e(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "accessoryList": [
                {
                    "articlesNo": obj[0]['articlesNo']
                }
            ],
            "deliveryType": "1",
            "userId": INFO['special_user_id'],
            "deliveryRemark": "备注"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'EgcsFMe1T', data, 'main', nocheck)

    @doc(cwwg81c7fuxew6ohcyna)
    @BaseApi.timing_decorator
    def cwwg81c7fuxew6ohcyna(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "articlesNo": obj[0]['articlesNo']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'WfRN4FHg5', data, 'main', nocheck)


class BVA8mmtbcT(InitializeParams):
    """配件管理|移交接收管理|移交记录"""

    @doc(z36rbt8nuevvk5zw0ev1)
    @BaseApi.timing_decorator
    def z36rbt8nuevvk5zw0ev1(self, nocheck=False):
        obj = self.pc.BFOjFKv6ZxII7V5LzQcr4(data='a')
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "articlesNoList": [
                obj[0]['articlesNo']
            ],
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'qaZzLXfvX', data, 'main', nocheck)

    @doc(sdl1o9ghd61tojp5ap48)
    @BaseApi.timing_decorator
    def sdl1o9ghd61tojp5ap48(self, nocheck=False):
        obj = self.pc.BFOjFKv6ZxII7V5LzQcr4(data='a')
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesNo": obj[0]['articlesNo'],
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'zbE7yOZvu', data, 'main', nocheck)

    @doc(evbb4ktxeipdare0ybrf)
    @BaseApi.timing_decorator
    def evbb4ktxeipdare0ybrf(self, nocheck=False):
        obj = self.pc.BFOjFKv6ZxII7V5LzQcr4()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "orderNo": obj[0]['orderNo'],
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'zbE7yOZvu', data, 'main', nocheck)

    @doc(v3j4micfjps17busi402)
    @BaseApi.timing_decorator
    def v3j4micfjps17busi402(self, nocheck=False):
        obj = self.pc.BFOjFKv6ZxII7V5LzQcr4()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "distributorId": INFO['main_user_id'],
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'zbE7yOZvu', data, 'main', nocheck)

    @doc(pudb09khr1ozo3wwci4a)
    @BaseApi.timing_decorator
    def pudb09khr1ozo3wwci4a(self, nocheck=False):
        obj = self.pc.BFOjFKv6ZxII7V5LzQcr4()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "userId": INFO['special_user_id'],
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'zbE7yOZvu', data, 'main', nocheck)

    @doc(rf7nygh1xebifff8bl22)
    @BaseApi.timing_decorator
    def rf7nygh1xebifff8bl22(self, nocheck=False):
        obj = self.pc.BFOjFKv6ZxII7V5LzQcr4()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "erpStartTime": self.get_the_date(),
            "erpEndTime": self.get_the_date(days=1),
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'zbE7yOZvu', data, 'main', nocheck)

    @doc(hpjacvh5iwz7rzgwap4)
    @BaseApi.timing_decorator
    def hpjacvh5iwz7rzgwap4(self, nocheck=False, status=None):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "status": status,
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'zbE7yOZvu', data, 'main', nocheck)


class NccuqXjU5C(InitializeParams):
    """配件管理|配件库存|库存列表"""

    @doc(r5gxaxtpflvd7qfj153k)
    @BaseApi.timing_decorator
    def r5gxaxtpflvd7qfj153k(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "id": obj[0]['id'],
            "articlesNo": obj[0]['articlesNo'],
            "skuInfo": obj[0]['skuInfo'],
            "accessoryType": 1,
            "channelType": 1,
            "baseAccessoryDTO": {
                "accessoryNo": "PJ0216",
                "accessoryName": "铁片",
                "brandId": 8,
                "modelId": 18107,
                "accessoryType": 1,
                "modelName": "Pura 80 Pro",
                "brandName": "华为"
            }
        }
        self.validate_request_data(data)
        return self._make_request('post', 'PSwyXMyag', data, 'main', nocheck)

    @doc(oqmc5nwi0399dzltytx2)
    @BaseApi.timing_decorator
    def oqmc5nwi0399dzltytx2(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "accessoryList": [
                {
                    "articlesNo": obj[0]['articlesNo']
                }
            ],
            "deliveryType": 6,
            "userId": INFO['special_user_id'],
            "deliveryRemark": "备注"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'EgcsFMe1T', data, 'main', nocheck)

    @doc(saaotn9359y5rsz0php1)
    @BaseApi.timing_decorator
    def saaotn9359y5rsz0php1(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "accessoryList": [
                {
                    "articlesNo": obj[0]['articlesNo']
                }
            ],
            "deliveryType": 5,
            "userId": INFO['special_user_id'],
            "deliveryRemark": "备注"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'EgcsFMe1T', data, 'main', nocheck)

    @doc(lrfqyoilnhzw2ejk659d)
    @BaseApi.timing_decorator
    def lrfqyoilnhzw2ejk659d(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "accessoryList": [
                {
                    "articlesNo": obj[0]['articlesNo']
                }
            ],
            "deliveryType": 4,
            "userId": INFO['special_user_id'],
            "deliveryRemark": "备注"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'EgcsFMe1T', data, 'main', nocheck)

    @doc(v60oxil51ddo2si7jl7x)
    @BaseApi.timing_decorator
    def v60oxil51ddo2si7jl7x(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "accessoryList": [
                {
                    "articlesNo": obj[0]['articlesNo']
                }
            ],
            "deliveryType": 3,
            "userId": INFO['special_user_id'],
            "deliveryRemark": "备注"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'EgcsFMe1T', data, 'main', nocheck)

    @doc(p3vluvp1sur9pfwpeyrh)
    @BaseApi.timing_decorator
    def p3vluvp1sur9pfwpeyrh(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "accessoryList": [
                {
                    "articlesNo": obj[0]['articlesNo']
                }
            ],
            "deliveryType": 2,
            "userId": INFO['special_user_id'],
            "deliveryRemark": "备注"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'EgcsFMe1T', data, 'main', nocheck)

    @doc(icdh72iujmalc7gukwol)
    @BaseApi.timing_decorator
    def icdh72iujmalc7gukwol(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "accessoryList": [
                {
                    "articlesNo": obj[0]['articlesNo']
                }
            ],
            "deliveryType": 1,
            "userId": INFO['special_user_id'],
            "deliveryRemark": "备注"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'EgcsFMe1T', data, 'main', nocheck)

    @doc(abuhabsmqfhq1ut9qc3c)
    @BaseApi.timing_decorator
    def abuhabsmqfhq1ut9qc3c(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "id": obj[0]['id'],
            "articlesNo": obj[0]['articlesNo'],
            "skuInfo": obj[0]['skuInfo'],
            "accessoryType": 1,
            "channelType": 1,
            "baseAccessoryDTO": {
                "accessoryNo": "PJ0216",
                "accessoryName": "铁片",
                "brandId": 8,
                "modelId": 18111,
                "accessoryType": 1,
                "modelName": "Hi MatePad 11.5寸 2024款 柔光版",
                "brandName": "华为"
            }
        }
        self.validate_request_data(data)
        return self._make_request('post', 'PSwyXMyag', data, 'main', nocheck)

    @doc(oohakdwo34k03yybh9s8)
    @BaseApi.timing_decorator
    def oohakdwo34k03yybh9s8(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesNo": obj[0]['articlesNo']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'QARwOTuPY', data, 'main', nocheck)

    @doc(pn81zph6ujrzvf8p5qxw)
    @BaseApi.timing_decorator
    def pn81zph6ujrzvf8p5qxw(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "supplierId": INFO['main_supplier_id']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'QARwOTuPY', data, 'main', nocheck)

    @doc(fiy75muh6gz6nsyhyah6)
    @BaseApi.timing_decorator
    def fiy75muh6gz6nsyhyah6(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "userId": INFO['main_user_id']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'QARwOTuPY', data, 'main', nocheck)

    @doc(lqdftflzdi25uvz52b4z)
    @BaseApi.timing_decorator
    def lqdftflzdi25uvz52b4z(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu()
        ParamCache.cache_object({"i": obj[0]['purchaseNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "purchaseNo": obj[0]['purchaseNo']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'QARwOTuPY', data, 'main', nocheck)

    @doc(j4r6o9x82lrhfgn7houk)
    @BaseApi.timing_decorator
    def j4r6o9x82lrhfgn7houk(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu()
        ParamCache.cache_object({"i": obj[0]['purchaseNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "purchaseId": ['main_user_id']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'QARwOTuPY', data, 'main', nocheck)

    @doc(awfdfgrvu5yt8ocg4om9)
    @BaseApi.timing_decorator
    def awfdfgrvu5yt8ocg4om9(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu()
        ParamCache.cache_object({"i": obj[0]['purchaseNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "purchaseEndTime": self.get_the_date(),
            "purchaseStartTime": self.get_the_date(days=1)
        }
        self.validate_request_data(data)
        return self._make_request('post', 'QARwOTuPY', data, 'main', nocheck)

    @doc(ie8fsxmabji7a7q54r1w)
    @BaseApi.timing_decorator
    def ie8fsxmabji7a7q54r1w(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "accessoryType": 2,
        }
        self.validate_request_data(data)
        return self._make_request('post', 'QARwOTuPY', data, 'main', nocheck)

    @doc(tje23q2s5q19u1i0r264)
    @BaseApi.timing_decorator
    def tje23q2s5q19u1i0r264(self, nocheck=False, status=None):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "inventoryStatus": status,
        }
        self.validate_request_data(data)
        return self._make_request('post', 'QARwOTuPY', data, 'main', nocheck)

    @doc(utqrzheihgso0dngmplj)
    @BaseApi.timing_decorator
    def utqrzheihgso0dngmplj(self, nocheck=False, type_id=None):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesTypeId": type_id,
        }
        self.validate_request_data(data)
        return self._make_request('post', 'QARwOTuPY', data, 'main', nocheck)

    @doc(je9vs9v7ryk65bgnpnrt)
    @BaseApi.timing_decorator
    def je9vs9v7ryk65bgnpnrt(self, nocheck=False, color=None):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "accessoryQuality": color,
        }
        self.validate_request_data(data)
        return self._make_request('post', 'QARwOTuPY', data, 'main', nocheck)

    @doc(is3591xz3eohk67pi7h9)
    @BaseApi.timing_decorator
    def is3591xz3eohk67pi7h9(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu()
        ParamCache.cache_object({"i": obj[0]['accessoryNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "accessoryNo": obj[0]['accessoryNo'],
        }
        self.validate_request_data(data)
        return self._make_request('post', 'QARwOTuPY', data, 'main', nocheck)

    @doc(d41766ll2lal2a6qly54)
    @BaseApi.timing_decorator
    def d41766ll2lal2a6qly54(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "inventoryTime": 1,
        }
        self.validate_request_data(data)
        return self._make_request('post', 'QARwOTuPY', data, 'main', nocheck)

    @doc(wuufeqpw5tq8hy6290ce)
    @BaseApi.timing_decorator
    def wuufeqpw5tq8hy6290ce(self, nocheck=False, channel=None):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "channelType": channel,
        }
        self.validate_request_data(data)
        return self._make_request('post', 'QARwOTuPY', data, 'main', nocheck)

    @doc(vfi204ksnbxzyybqadvh)
    @BaseApi.timing_decorator
    def vfi204ksnbxzyybqadvh(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "pageSize": 10,
            "pageNum": 1,
            "articlesTypeId": "1",
            "brandId": 8,
            "modelId": 18111
        }
        self.validate_request_data(data)
        return self._make_request('post', 'QARwOTuPY', data, 'main', nocheck)

    @doc(x1coaubd9r45peqs8hua)
    @BaseApi.timing_decorator
    def x1coaubd9r45peqs8hua(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "pageSize": 10,
            "pageNum": 1,
            "warehouseId": INFO['main_warehouse_id']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'QARwOTuPY', data, 'main', nocheck)

    @doc(tlfu0zq3fcj6qj4k4v02)
    @BaseApi.timing_decorator
    def tlfu0zq3fcj6qj4k4v02(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu()
        ParamCache.cache_object({"i": obj[0]['accessoryName']})
        data = {
            "pageSize": 10,
            "pageNum": 1,
            "accessoryName": obj[0]['accessoryName']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'QARwOTuPY', data, 'main', nocheck)

    @doc(u6a07svx0rwzn93bn54o)
    @BaseApi.timing_decorator
    def u6a07svx0rwzn93bn54o(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "status": "1",
            "accountNo": INFO['main_account_no'],
            "isEexpress": "1",
            "logisticsNoPrice": 10,
            "saleSupplierId": INFO['main_sale_supplier_id'],
            "supplierName": INFO['vice_sales_customer_name'],
            "walletAccountNo": INFO['main_wallet_account_no'],
            "payWay": 1,
            "pickUpType": 1,
            "remark": "备注",
            "logisticsCompanyType": 1,
            "userAddressId": INFO['main_user_address_id'],
            "saleOrderAccessoryList": [
                {
                    "accessoryNo": obj[0]['articlesNo'],
                    "accessoryId": obj[0]['id'],
                    "salePrice": "123",
                    "costPrice": obj[0]['totalCost']
                }
            ],
            "deliveryNum": 1,
            "accountName": INFO['main_account_name']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'kyVzUMNcM', data, 'main', nocheck)

    @doc(s4ix3uhl32fhg96aeiis)
    @BaseApi.timing_decorator
    def s4ix3uhl32fhg96aeiis(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "status": "2",
            "accountNo": INFO['main_account_no'],
            "isEexpress": "0",
            "logisticsNo": self.jd,
            "logisticsNoPrice": "10",
            "saleSupplierId": INFO['main_sale_supplier_id'],
            "supplierName": INFO['vice_sales_customer_name'],
            "remark": "备注",
            "saleOrderAccessoryList": [
                {
                    "accessoryNo": obj[0]['articlesNo'],
                    "accessoryId": obj[0]['id'],
                    "salePrice": "70",
                    "costPrice": obj[0]['totalCost']
                }
            ],
            "deliveryNum": 1,
            "accountName": INFO['main_account_name']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'kyVzUMNcM', data, 'main', nocheck)


class A3AKRuhANY(InitializeParams):
    """配件管理|配件维护"""

    @doc(vnsg549qqo4e8la9pvyz)
    @BaseApi.timing_decorator
    def vnsg549qqo4e8la9pvyz(self, nocheck=False):
        data = {
            "accessoryName": "配件名称" + self.imei,
            "accessoryType": "3",
            "status": 1
        }
        self.validate_request_data(data)
        return self._make_request('post', 'KbfOfrq4k', data, 'idle', nocheck)

    @doc(sk6ol090tlyb6qyetwl2)
    @BaseApi.timing_decorator
    def sk6ol090tlyb6qyetwl2(self, nocheck=False):
        data = {
            "accessoryName": "配件名称" + self.imei,
            "accessoryType": "2",
            "status": 0
        }
        self.validate_request_data(data)
        return self._make_request('post', 'KbfOfrq4k', data, 'idle', nocheck)

    @doc(e8rzsfkgsktqcjm31vfu)
    @BaseApi.timing_decorator
    def e8rzsfkgsktqcjm31vfu(self, nocheck=False):
        obj = self.pc.Ln0faZ5CGpaYmkrcCVg4X()
        ParamCache.cache_object({"i": obj[0]['accessoryNo']})
        data = {
            "createBy": "杰克",
            "createTime": obj[0]['createTime'],
            "pageSize": 10,
            "pageNum": 1,
            "orderByColumn": "create_time",
            "isAsc": "desc",
            "id": obj[0]['id'],
            "accessoryNo": obj[0]['accessoryNo'],
            "accessoryName": '名称' + self.serial,
            "accessoryType": "3",
            "price": 0,
            "status": 1,
            "tenantId": 573448,
            "isDelete": 0
        }
        return self._make_request('put', 'VFgNtfVfH', data, 'idle', nocheck)

    @doc(u8m46ujx2im1noarlsmu)
    @BaseApi.timing_decorator
    def u8m46ujx2im1noarlsmu(self, nocheck=False):
        obj = self.pc.Ln0faZ5CGpaYmkrcCVg4X()
        data = {
            "id": obj[0]['id']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'M3mcL0BDw', data, 'idle', nocheck)

    @doc(fd2dzuppjfcy0vc68osp)
    @BaseApi.timing_decorator
    def fd2dzuppjfcy0vc68osp(self, nocheck=False):
        obj = self.pc.Ln0faZ5CGpaYmkrcCVg4X()
        ParamCache.cache_object({"i": obj[0]['accessoryNo']})
        data = {
            "accessoryNo": obj[0]['accessoryNo'],
            "pageSize": 10,
            "pageNum": 1
        }
        self.validate_request_data(data)
        return self._make_request('post', 'GTZ0UOiDK', data, 'idle', nocheck)

    @doc(oqclfc811pbxjb1ydmtf)
    @BaseApi.timing_decorator
    def oqclfc811pbxjb1ydmtf(self, nocheck=False):
        obj = self.pc.Ln0faZ5CGpaYmkrcCVg4X()
        ParamCache.cache_object({"i": obj[0]['accessoryName']})
        data = {
            "accessoryName": obj[0]['accessoryName'],
            "pageSize": 10,
            "pageNum": 1
        }
        self.validate_request_data(data)
        return self._make_request('post', 'GTZ0UOiDK', data, 'idle', nocheck)

    @doc(uxs5seo7otyrzfugdqsl)
    @BaseApi.timing_decorator
    def uxs5seo7otyrzfugdqsl(self, nocheck=False, status=None):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "status": status,
        }
        self.validate_request_data(data)
        return self._make_request('post', 'GTZ0UOiDK', data, 'main', nocheck)


class HkVg66f8Mk(InitializeParams):
    """配件管理|入库管理|旧配件入库"""

    @doc(sPBqvfYc9boVR4rGIL4w)
    @BaseApi.timing_decorator
    def sPBqvfYc9boVR4rGIL4w(self, nocheck=False):
        data = {
            "warehouseId": INFO['main_in_warehouse_id'],
            "userId": INFO['special_user_id'],
            "storageTime": self.get_formatted_datetime(),
            "remark": "备注",
            "warehouseName": INFO['main_in_warehouse_name'],
            "accessoryDTOList": [
                {
                    "accessoryNum": "1",
                    "purchasePrice": "12",
                    "accessoryType": "2",
                    "articlesTypeId": "1",
                    "channelType": "1",
                    "baseAccessoryDTO": {
                        "accessoryName": "SIA8109",
                        "accessoryType": "3",
                        "brandId": 1,
                        "brandName": "苹果",
                        "modelId": 7692,
                        "modelName": "iPhone 5S",
                        "accessoryNo": "PJ0211"
                    }
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'AowpSZBva', data, 'main', nocheck)

    @doc(zq8av7DX7E15sOdOA5na)
    @BaseApi.timing_decorator
    def zq8av7DX7E15sOdOA5na(self, nocheck=False):
        data = {
            "warehouseId": INFO['main_in_warehouse_id'],
            "userId": INFO['special_user_id'],
            "storageTime": self.get_formatted_datetime(),
            "warehouseName": INFO['main_in_warehouse_name'],
            "accessoryDTOList": [
                {
                    "accessoryNum": "1000",
                    "purchasePrice": "345",
                    "accessoryType": "2",
                    "articlesTypeId": "1",
                    "channelType": "1",
                    "baseAccessoryDTO": {
                        "accessoryName": "铁片",
                        "accessoryType": "2",
                        "brandId": 1,
                        "brandName": "苹果",
                        "modelId": 7693,
                        "modelName": "iPhone 6",
                        "accessoryNo": "PJ0216"
                    }
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'AowpSZBva', data, 'main', nocheck)

    @doc(NIg8OImrULuxaaLnvprF)
    @BaseApi.timing_decorator
    def NIg8OImrULuxaaLnvprF(self, nocheck=False):
        data = {
            "warehouseId": INFO['main_in_warehouse_id'],
            "userId": INFO['special_user_id'],
            "storageTime": self.get_formatted_datetime(),
            "remark": "备注",
            "warehouseName": INFO['main_in_warehouse_name'],
            "accessoryDTOList": [
                {
                    "accessoryNum": "1",
                    "purchasePrice": "123",
                    "accessoryType": "2",
                    "articlesTypeId": "3",
                    "channelType": "1",
                    "baseAccessoryDTO": {
                        "accessoryName": "HI1102",
                        "accessoryType": "3",
                        "brandId": 802,
                        "brandName": "荣耀",
                        "modelId": 18031,
                        "modelName": "平板 10",
                        "accessoryNo": "PJ0171"
                    }
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'AowpSZBva', data, 'main', nocheck)

    @doc(V7VzYOhxyeCqh4OaUKh3)
    @BaseApi.timing_decorator
    def V7VzYOhxyeCqh4OaUKh3(self, nocheck=False):
        data = {
            "warehouseId": INFO['main_in_warehouse_id'],
            "userId": INFO['special_user_id'],
            "storageTime": self.get_formatted_datetime(),
            "remark": "备注",
            "warehouseName": INFO['main_in_warehouse_name'],
            "accessoryDTOList": [
                {
                    "accessoryNum": "1",
                    "purchasePrice": "12",
                    "accessoryType": "2",
                    "articlesTypeId": "4",
                    "channelType": "1",
                    "baseAccessoryDTO": {
                        "accessoryName": "HI1102",
                        "accessoryType": "3",
                        "brandId": 8,
                        "brandName": "华为",
                        "modelId": 15420,
                        "modelName": "MateBook X Pro 2018款",
                        "accessoryNo": "PJ0171"
                    }
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'AowpSZBva', data, 'main', nocheck)

    @doc(PMcmyjds8q4To8x1WYWe)
    @BaseApi.timing_decorator
    def PMcmyjds8q4To8x1WYWe(self, nocheck=False):
        data = {
            "warehouseId": INFO['main_in_warehouse_id'],
            "userId": INFO['special_user_id'],
            "storageTime": self.get_formatted_datetime(),
            "remark": "备注",
            "warehouseName": INFO['main_in_warehouse_name'],
            "accessoryDTOList": [
                {
                    "accessoryNum": "1",
                    "purchasePrice": "20",
                    "accessoryType": "2",
                    "articlesTypeId": "5",
                    "channelType": "1",
                    "baseAccessoryDTO": {
                        "accessoryName": "HI1102",
                        "accessoryType": "3",
                        "brandId": 802,
                        "brandName": "荣耀",
                        "modelId": 11923,
                        "modelName": "GS 3",
                        "accessoryNo": "PJ0171"
                    }
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'AowpSZBva', data, 'main', nocheck)

    @doc(rXmtCESQnyljezY5hqQF)
    @BaseApi.timing_decorator
    def rXmtCESQnyljezY5hqQF(self, nocheck=False):
        obj = self.pc.RjB1dOTFUrlGReUmemgQr(data='a')
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "articlesNo": obj[0]['articlesNo'],
            "pageSize": 10,
            "pageNum": 1,
        }
        self.validate_request_data(data)
        return self._make_request('post', 'icqD4B9Rk', data, 'main', nocheck)

    @doc(BBRaKuLnfUAs23bBdW7L)
    @BaseApi.timing_decorator
    def BBRaKuLnfUAs23bBdW7L(self, nocheck=False):
        obj = self.pc.RjB1dOTFUrlGReUmemgQr()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "orderNo": obj[0]['orderNo'],
            "pageSize": 10,
            "pageNum": 1,
        }
        self.validate_request_data(data)
        return self._make_request('post', 'icqD4B9Rk', data, 'main', nocheck)

    @doc(whT4XzVC2HWmjrLwPGbu)
    @BaseApi.timing_decorator
    def whT4XzVC2HWmjrLwPGbu(self, nocheck=False):
        obj = self.pc.RjB1dOTFUrlGReUmemgQr()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "warehouseId": INFO['main_in_warehouse_id'],
            "pageSize": 10,
            "pageNum": 1,
        }
        self.validate_request_data(data)
        return self._make_request('post', 'icqD4B9Rk', data, 'main', nocheck)

    @doc(sJy6JWqmmKyM7r2DjLiS)
    @BaseApi.timing_decorator
    def sJy6JWqmmKyM7r2DjLiS(self, nocheck=False):
        obj = self.pc.RjB1dOTFUrlGReUmemgQr()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "userId": INFO['special_user_id'],
            "pageSize": 10,
            "pageNum": 1,
        }
        self.validate_request_data(data)
        return self._make_request('post', 'icqD4B9Rk', data, 'main', nocheck)

    @doc(WbSFKLvOUocIJPFJCwVb)
    @BaseApi.timing_decorator
    def WbSFKLvOUocIJPFJCwVb(self, nocheck=False):
        obj = self.pc.RjB1dOTFUrlGReUmemgQr()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "pageSize": 10,
            "pageNum": 1,
            "startTime": self.get_the_date(),
            "endTime": self.get_the_date(days=1),
        }
        self.validate_request_data(data)
        return self._make_request('post', 'icqD4B9Rk', data, 'main', nocheck)


class ZgkiOAdiZt(InitializeParams):
    """配件管理|入库管理|分拣列表"""

    @doc(x2I7I6LSgnOWJ5UfzkPs)
    @BaseApi.timing_decorator
    def x2I7I6LSgnOWJ5UfzkPs(self, nocheck=False, status=None):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "sortationStatus": status,
        }
        self.validate_request_data(data)
        return self._make_request('post', 'QTembQdXx', data, 'main', nocheck)

    @doc(kieRlhO7K2AGuSdQH9b3)
    @BaseApi.timing_decorator
    def kieRlhO7K2AGuSdQH9b3(self, nocheck=False):
        obj = self.pc.LnfQBDqBvleaE2O0412qk()
        ParamCache.cache_object({"i": obj[0]['logisticsNo']})
        data = {
            "pageSize": 10,
            "pageNum": 1,
            "logisticsNo": obj[0]['logisticsNo'],
        }
        self.validate_request_data(data)
        return self._make_request('post', 'QTembQdXx', data, 'main', nocheck)

    @doc(bOxmYfGUFrevxZUW1A6G)
    @BaseApi.timing_decorator
    def bOxmYfGUFrevxZUW1A6G(self, nocheck=False):
        obj = self.pc.KFkHdZyASZRhMrmNKfHiQ()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "pageSize": 10,
            "pageNum": 1,
            "articlesNo": obj[0]['articlesNo'],
        }
        self.validate_request_data(data)
        return self._make_request('post', 'QTembQdXx', data, 'main', nocheck)

    @doc(gMjMJ10FSSvSiwf8JbsW)
    @BaseApi.timing_decorator
    def gMjMJ10FSSvSiwf8JbsW(self, nocheck=False):
        obj = self.pc.KFkHdZyASZRhMrmNKfHiQ()
        ParamCache.cache_object({"i": obj[0]['businessNo']})
        data = {
            "pageSize": 10,
            "pageNum": 1,
            "businessNo": obj,
        }
        self.validate_request_data(data)
        return self._make_request('post', 'QTembQdXx', data, 'main', nocheck)

    @doc(BnQQG1HUn8tvq1ZjDMCV)
    @BaseApi.timing_decorator
    def BnQQG1HUn8tvq1ZjDMCV(self, nocheck=False):
        obj = self.pc.LnfQBDqBvleaE2O0412qk()
        ParamCache.cache_object({"i": obj[0]['logisticsNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "sortationStartTime": self.get_the_date(),
            "sortationEndTime": self.get_the_date(days=1),
        }
        self.validate_request_data(data)
        return self._make_request('post', 'QTembQdXx', data, 'main', nocheck)


class EdqL4NE5hk(InitializeParams):
    """配件管理|配件采购|新增采购单"""

    @doc(nBfEGGe1LJguXHi6aesS)
    @BaseApi.timing_decorator
    def nBfEGGe1LJguXHi6aesS(self, nocheck=False):
        data = {
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "state": "3",
            "logisticsNo": self.jd,
            "payState": "2",
            "accountNo": INFO['main_account_no'],
            "purchaseSource": "2",
            "logisticsPrice": 20,
            "userId": INFO['main_user_id'],
            "purchaseTime": self.get_formatted_datetime(),
            "remark": "备注",
            "accessoryDTOList": [
                {
                    "purchasePrice": "10",
                    "accessoryNum": "1",
                    "baseAccessoryDTO": {
                        "accessoryName": "OXO",
                        "accessoryType": "2",
                        "purchasePrice": "10",
                        "accessoryNo": "PJ0215",
                        "brandId": 802,
                        "brandName": "荣耀",
                        "modelId": 11402,
                        "modelName": "MagicBook 14 Pro 2023款",
                        "colorId": "",
                        "colorName": "",
                        "fineness": "1",
                        "channelType": "1",
                        "articlesTypeName": "配件",
                        "articlesRemake": "",
                        "articlesTypeId": "4"
                    },
                    "warehouseId": "",
                    "articlesTypeId": "4",
                    "accessoryType": "1",
                    "channelType": "1"
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'qg5Cp2gXr', data, 'main', nocheck)

    @doc(niKwILpBHogDvGt52uEB)
    @BaseApi.timing_decorator
    def niKwILpBHogDvGt52uEB(self, nocheck=False):
        data = {
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "state": "4",
            "logisticsNo": self.jd,
            "payState": "2",
            "accountNo": INFO['main_account_no'],
            "purchaseSource": "2",
            "logisticsPrice": 10,
            "userId": INFO['main_user_id'],
            "purchaseTime": self.get_formatted_datetime(),
            "warehouseId": INFO['main_warehouse_id'],
            "remark": "备注",
            "accessoryDTOList": [
                {
                    "purchasePrice": "10",
                    "accessoryNum": "1",
                    "baseAccessoryDTO": {
                        "accessoryName": "铁片",
                        "accessoryType": "2",
                        "purchasePrice": "111",
                        "accessoryNo": "PJ0216",
                        "brandId": 8,
                        "brandName": "华为",
                        "modelId": 18111,
                        "modelName": "Pocket 2 优享版",
                        "colorId": "",
                        "colorName": "",
                        "fineness": "1",
                        "channelType": "1",
                        "articlesTypeName": "配件",
                        "articlesRemake": "",
                        "articlesTypeId": "1"
                    },
                    "warehouseId": INFO['main_warehouse_id'],
                    "articlesTypeId": "1",
                    "accessoryType": "1",
                    "channelType": "1"
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'qg5Cp2gXr', data, 'main', nocheck)

    @doc(fi51E5jCFUxE1nLYPO7w)
    @BaseApi.timing_decorator
    def fi51E5jCFUxE1nLYPO7w(self, nocheck=False):
        data = {
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "state": "4",
            "payState": "1",
            "accountNo": INFO['main_account_no'],
            "purchaseSource": "2",
            "userId": INFO['main_user_id'],
            "purchaseTime": self.get_formatted_datetime(),
            "warehouseId": INFO['main_warehouse_id'],
            "remark": "备注",
            "accessoryDTOList": [
                {
                    "purchasePrice": "12214",
                    "accessoryNum": "1",
                    "baseAccessoryDTO": {
                        "accessoryName": "漏液屏",
                        "accessoryType": "3",
                        "purchasePrice": "12214",
                        "accessoryNo": "PJ0143",
                        "brandId": 27,
                        "brandName": "OPPO",
                        "modelId": 13372,
                        "modelName": "Watch 4 Pro",
                        "colorId": "",
                        "colorName": "",
                        "fineness": "1",
                        "channelType": "1",
                        "articlesTypeName": "配件",
                        "articlesRemake": "",
                        "articlesTypeId": "5"
                    },
                    "warehouseId": INFO['main_warehouse_id'],
                    "articlesTypeId": "3",
                    "accessoryType": "1",
                    "channelType": "1"
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'qg5Cp2gXr', data, 'main', nocheck)

    @doc(rYvpUsdluGutOhIhm7af)
    @BaseApi.timing_decorator
    def rYvpUsdluGutOhIhm7af(self, nocheck=False):
        data = {
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "state": "3",
            "logisticsNo": self.jd,
            "payState": "1",
            "accountNo": INFO['main_account_no'],
            "purchaseSource": "2",
            "logisticsPrice": "11",
            "userId": INFO['main_user_id'],
            "purchaseTime": self.get_formatted_datetime(),
            "remark": "备注",
            "accessoryDTOList": [
                {
                    "purchasePrice": 77,
                    "accessoryNum": "1",
                    "baseAccessoryDTO": {
                        "accessoryName": "HI1102",
                        "accessoryType": "3",
                        "purchasePrice": "10",
                        "accessoryNo": "PJ0171",
                        "brandId": 802,
                        "brandName": "荣耀",
                        "modelId": 18031,
                        "modelName": "平板 10",
                        "colorId": "",
                        "colorName": "",
                        "fineness": "2",
                        "channelType": "2",
                        "articlesTypeName": "配件",
                        "articlesRemake": "",
                        "articlesTypeId": "3"
                    },
                    "warehouseId": "",
                    "articlesTypeId": "3",
                    "accessoryType": "2",
                    "channelType": "2"
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'qg5Cp2gXr', data, 'main', nocheck)

    @doc(qyeHP1UKtW02kXOihCU1)
    @BaseApi.timing_decorator
    def qyeHP1UKtW02kXOihCU1(self, nocheck=False):
        data = {
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "state": "4",
            "logisticsNo": self.jd,
            "payState": "2",
            "accountNo": INFO['main_account_no'],
            "purchaseSource": "2",
            "logisticsPrice": 20,
            "userId": INFO['main_user_id'],
            "purchaseTime": self.get_formatted_datetime(),
            "remark": "备注",
            "accessoryDTOList": [
                {
                    "purchasePrice": "10",
                    "accessoryNum": "1000",
                    "baseAccessoryDTO": {
                        "accessoryName": "摄像头1",
                        "accessoryType": "2",
                        "purchasePrice": "121",
                        "accessoryNo": "PJ0217",
                        "brandId": 1,
                        "brandName": "苹果",
                        "modelId": 7692,
                        "modelName": "iPhone 5S",
                        "colorId": "",
                        "colorName": "",
                        "fineness": "2",
                        "channelType": "1",
                        "articlesTypeName": "配件",
                        "articlesRemake": "",
                        "articlesTypeId": "1"
                    },
                    "warehouseId": INFO['main_warehouse_id'],
                    "articlesTypeId": "1",
                    "accessoryType": "2",
                    "channelType": "1"
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'qg5Cp2gXr', data, 'main', nocheck)

    @doc(Cd8pPBeDJMVuZBrTbFXN)
    @BaseApi.timing_decorator
    def Cd8pPBeDJMVuZBrTbFXN(self, nocheck=False):
        data = {
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "state": "3",
            "logisticsNo": self.jd,
            "payState": "2",
            "accountNo": INFO['main_account_no'],
            "purchaseSource": "2",
            "logisticsPrice": "11",
            "userId": INFO['main_user_id'],
            "purchaseTime": self.get_formatted_datetime(),
            "remark": "备注",
            "accessoryDTOList": [
                {
                    "purchasePrice": "1",
                    "accessoryNum": "1",
                    "baseAccessoryDTO": {
                        "accessoryName": "摄像头",
                        "accessoryType": "2",
                        "purchasePrice": "1",
                        "accessoryNo": "PJ0217",
                        "brandId": 1,
                        "brandName": "苹果",
                        "modelId": 7692,
                        "modelName": "iPhone 5S",
                        "colorId": "",
                        "colorName": "",
                        "fineness": "1",
                        "channelType": "1",
                        "articlesTypeName": "配件",
                        "articlesRemake": "",
                        "articlesTypeId": "1"
                    },
                    "warehouseId": "",
                    "articlesTypeId": "1",
                    "accessoryType": "1",
                    "channelType": "1"
                },
                {
                    "purchasePrice": "22",
                    "accessoryNum": "1",
                    "baseAccessoryDTO": {
                        "accessoryName": "摄像头",
                        "accessoryType": "2",
                        "purchasePrice": "22",
                        "accessoryNo": "PJ0217",
                        "brandId": 8,
                        "brandName": "华为",
                        "modelId": 18111,
                        "modelName": "Pocket 2 优享版",
                        "colorId": "",
                        "colorName": "",
                        "fineness": "1",
                        "channelType": "1",
                        "articlesTypeName": "配件",
                        "articlesRemake": "",
                        "articlesTypeId": "1"
                    },
                    "warehouseId": "",
                    "articlesTypeId": "1",
                    "accessoryType": "1",
                    "channelType": "1"
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'qg5Cp2gXr', data, 'main', nocheck)


class Kxg46XEPdY(InitializeParams):
    """配件管理|配件采购|采购列表"""

    @doc(ytFlEaPZYL2krOQHCL4y)
    @BaseApi.timing_decorator
    def ytFlEaPZYL2krOQHCL4y(self, nocheck=False):
        obj = self.pc.OiUAWoPURtS5QdkSFauge(data='a')
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "saleState": "1",
            "payState": "2",
            "offExpressage": "1",
            "logisticsNoPrice": 10,
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "remark": "备注",
            "walletAccountNo": INFO['main_wallet_account_no'],
            "payWay": 1,
            "pickUpType": 1,
            "logisticsCompanyType": 1,
            "userAddressId": INFO['main_user_address_id'],
            "purchaseAccessoryDTOList": [
                {
                    "purchasePrice": obj[0]['purchasePrice'],
                    "purchaseNo": obj[0]['purchaseNo'],
                    "newPurchasePrice": obj[0]['returnAblePrice'],
                    "articlesNo": obj[0]['articlesNo'],
                    "salePrice": 0,
                    "id": obj[0]['id']
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'fed411lAJ', data, 'main', nocheck)

    @doc(DUKh4wv9QHERfWyZo08U)
    @BaseApi.timing_decorator
    def DUKh4wv9QHERfWyZo08U(self, nocheck=False):
        obj = self.pc.OiUAWoPURtS5QdkSFauge(data='a')
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "saleState": "1",
            "payState": "2",
            "offExpressage": "0",
            "logisticsOrder": self.jd,
            "logisticsNoPrice": "11",
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "remark": "备注",
            "walletAccountNo": INFO['main_wallet_account_no'],
            "purchaseAccessoryDTOList": [
                {
                    "purchasePrice": obj[0]['purchasePrice'],
                    "purchaseNo": obj[0]['purchaseNo'],
                    "newPurchasePrice": obj[0]['returnAblePrice'],
                    "articlesNo": obj[0]['articlesNo'],
                    "salePrice": 0,
                    "id": obj[0]['id']
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'fed411lAJ', data, 'main', nocheck)

    @doc(kuo3zYG5OY6r1J5GFLwS)
    @BaseApi.timing_decorator
    def kuo3zYG5OY6r1J5GFLwS(self, nocheck=False):
        obj = self.pc.OiUAWoPURtS5QdkSFauge(data='a')
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "saleState": "7",
            "payState": "2",
            "offExpressage": 0,
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "remark": "备注",
            "purchaseAccessoryDTOList": [
                {
                    "purchasePrice": obj[0]['purchasePrice'],
                    "purchaseNo": obj[0]['purchaseNo'],
                    "newPurchasePrice": 1,
                    "articlesNo": obj[0]['articlesNo'],
                    "salePrice": 0,
                    "id": obj[0]['id']
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'fed411lAJ', data, 'main', nocheck)

    @doc(rNxmjG3kaLQP30Voi9tR)
    @BaseApi.timing_decorator
    def rNxmjG3kaLQP30Voi9tR(self, nocheck=False):
        obj = self.pc.OiUAWoPURtS5QdkSFauge(data='a')
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "saleState": "7",
            "payState": "2",
            "offExpressage": 0,
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "remark": "备注",
            "purchaseAccessoryDTOList": [
                {
                    "purchasePrice": obj[0]['purchasePrice'],
                    "purchaseNo": obj[0]['purchaseNo'],
                    "newPurchasePrice": obj[0]['returnAblePrice'],
                    "articlesNo": obj[0]['articlesNo'],
                    "salePrice": 0,
                    "id": obj[0]['id']
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'fed411lAJ', data, 'main', nocheck)

    @doc(OCChvTOX3BOwhsZ3x1Vk)
    @BaseApi.timing_decorator
    def OCChvTOX3BOwhsZ3x1Vk(self, nocheck=False):
        obj = self.pc.OiUAWoPURtS5QdkSFauge()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "articlesType": 2,
            "pageNum": 1,
            "pageSize": 10,
            "orderNo": obj[0]['orderNo']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'fRokl0vv2', data, 'main', nocheck)

    @doc(YHUNy8WSwZqIFfM88jqk)
    @BaseApi.timing_decorator
    def YHUNy8WSwZqIFfM88jqk(self, nocheck=False):
        obj = self.pc.OiUAWoPURtS5QdkSFauge()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "articlesType": 2,
            "pageNum": 1,
            "pageSize": 10,
            "supplierId": INFO['main_supplier_id']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'fRokl0vv2', data, 'main', nocheck)

    @doc(uTH0rGcq6USIvzBzwnqn)
    @BaseApi.timing_decorator
    def uTH0rGcq6USIvzBzwnqn(self, nocheck=False):
        obj = self.pc.OiUAWoPURtS5QdkSFauge()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "articlesType": 2,
            "pageNum": 1,
            "pageSize": 10,
            "userId": INFO['main_user_id']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'fRokl0vv2', data, 'main', nocheck)

    @doc(Q66Jftlrzxz0MflmYaRr)
    @BaseApi.timing_decorator
    def Q66Jftlrzxz0MflmYaRr(self, nocheck=False):
        obj = self.pc.OiUAWoPURtS5QdkSFauge()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "articlesType": 2,
            "pageNum": 1,
            "pageSize": 10,
            "erpEndTime": self.get_the_date(days=1),
            "erpStartTime": self.get_the_date()
        }
        self.validate_request_data(data)
        return self._make_request('post', 'fRokl0vv2', data, 'main', nocheck)

    @doc(art1lLuMH6tdwDoJNCVF)
    @BaseApi.timing_decorator
    def art1lLuMH6tdwDoJNCVF(self, nocheck=False, state=None):
        obj = self.pc.OiUAWoPURtS5QdkSFauge()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "articlesType": 2,
            "pageNum": 1,
            "pageSize": 10,
            "state": state
        }
        self.validate_request_data(data)
        return self._make_request('post', 'fRokl0vv2', data, 'main', nocheck)

    @doc(aa4ufzsTKdxHRDOhwcsN)
    @BaseApi.timing_decorator
    def aa4ufzsTKdxHRDOhwcsN(self, nocheck=False, pay=None):
        obj = self.pc.OiUAWoPURtS5QdkSFauge()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "articlesType": 2,
            "pageNum": 1,
            "pageSize": 10,
            "payState": pay
        }
        self.validate_request_data(data)
        return self._make_request('post', 'fRokl0vv2', data, 'main', nocheck)

    @doc(L2C0xDrhKPDjvib6JES4)
    @BaseApi.timing_decorator
    def L2C0xDrhKPDjvib6JES4(self, nocheck=False):
        obj = self.pc.OiUAWoPURtS5QdkSFauge()
        ParamCache.cache_object({"i": obj[0]['logisticsNo']})
        data = {
            "articlesType": 2,
            "pageNum": 1,
            "pageSize": 10,
            "logisticsNo": obj[0]['logisticsNo']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'fRokl0vv2', data, 'main', nocheck)


class TYqfRUwK8U(InitializeParams):
    """配件管理|移交接收管理|接收物品"""

    @doc(YGHj7l8L8BkOXk1wxK6L)
    @BaseApi.timing_decorator
    def YGHj7l8L8BkOXk1wxK6L(self, nocheck=False):
        obj = self.pc.AMaXd2PkDsrT5cj1SArOe(data='a')
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "accessoryList": [
                {
                    "articlesNo": obj[0]["articlesNo"]
                }
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'Sm7yLloyr', data, 'main', nocheck)

    @doc(J8ahGmCVn2GdPlK8RMlj)
    @BaseApi.timing_decorator
    def J8ahGmCVn2GdPlK8RMlj(self, nocheck=False):
        obj = self.pc.AMaXd2PkDsrT5cj1SArOe()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "orderNoList": [
                obj[0]['orderNo']
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'Sm7yLloyr', data, 'main', nocheck)

    @doc(wJXR0rLyC9FiD2Hab2GK)
    @BaseApi.timing_decorator
    def wJXR0rLyC9FiD2Hab2GK(self, nocheck=False):
        obj = self.pc.AMaXd2PkDsrT5cj1SArOe(data='a')
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesNo": obj[0]['articlesNo'],
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'JKjPTfATh', data, 'main', nocheck)

    @doc(vKg2HxGmBKyPPtp6kJf7)
    @BaseApi.timing_decorator
    def vKg2HxGmBKyPPtp6kJf7(self, nocheck=False):
        obj = self.pc.AMaXd2PkDsrT5cj1SArOe(data='a')
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesTypeId": "1",
            "brandId": 8,
            "modelId": 18111,
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'JKjPTfATh', data, 'main', nocheck)

    @doc(gyC9dbIGUhd7LCpcYvDF)
    @BaseApi.timing_decorator
    def gyC9dbIGUhd7LCpcYvDF(self, nocheck=False):
        obj = self.pc.AMaXd2PkDsrT5cj1SArOe(data='a')
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "distributorId": INFO['main_user_id'],
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'JKjPTfATh', data, 'main', nocheck)

    @doc(L4sWT7EPZcuwuxZX1mLK)
    @BaseApi.timing_decorator
    def L4sWT7EPZcuwuxZX1mLK(self, nocheck=False):
        obj = self.pc.AMaXd2PkDsrT5cj1SArOe(data='a')
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "userId": INFO['special_user_id'],
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'JKjPTfATh', data, 'main', nocheck)

    @doc(ZitlblU4lMp7BYK8ANyM)
    @BaseApi.timing_decorator
    def ZitlblU4lMp7BYK8ANyM(self, nocheck=False):
        obj = self.pc.AMaXd2PkDsrT5cj1SArOe(data='a')
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "erpStartTime": self.get_the_date(),
            "erpEndTime": self.get_the_date(days=1),
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'JKjPTfATh', data, 'main', nocheck)

    @doc(vRCdl2fqoKNJpFGdRzRD)
    @BaseApi.timing_decorator
    def vRCdl2fqoKNJpFGdRzRD(self, nocheck=False):
        obj = self.pc.AMaXd2PkDsrT5cj1SArOe(data='a')
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "orderNo": obj[0]['orderNo'],
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'JKjPTfATh', data, 'main', nocheck)

    @doc(Vzw0lwBx2ZAyHWSrX6RQ)
    @BaseApi.timing_decorator
    def Vzw0lwBx2ZAyHWSrX6RQ(self, nocheck=False):
        obj = self.pc.AMaXd2PkDsrT5cj1SArOe(data='a')
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesNo": obj[0]['articlesNo'],
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'ZspzD8hZ0', data, 'main', nocheck)

    @doc(UF6kXeN3uHtmuNDjeKwu)
    @BaseApi.timing_decorator
    def UF6kXeN3uHtmuNDjeKwu(self, nocheck=False):
        obj = self.pc.AMaXd2PkDsrT5cj1SArOe()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "orderNo": obj[0]['orderNo'],
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'ZspzD8hZ0', data, 'main', nocheck)

    @doc(un6reo9grtxgYp8gEDjc)
    @BaseApi.timing_decorator
    def un6reo9grtxgYp8gEDjc(self, nocheck=False, status=None):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "status": status,
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'ZspzD8hZ0', data, 'main', nocheck)

    @doc(byg7MwSRAnzhwUDcj1Wk)
    @BaseApi.timing_decorator
    def byg7MwSRAnzhwUDcj1Wk(self, nocheck=False):
        obj = self.pc.AMaXd2PkDsrT5cj1SArOe()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesType": 2,
            "distributorId": INFO['main_user_id']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'ZspzD8hZ0', data, 'main', nocheck)

    @doc(stvghsNX2dN5itJABNYT)
    @BaseApi.timing_decorator
    def stvghsNX2dN5itJABNYT(self, nocheck=False):
        obj = self.pc.AMaXd2PkDsrT5cj1SArOe()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "userId": INFO['special_user_id'],
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'ZspzD8hZ0', data, 'main', nocheck)

    @doc(sn75xNW4A5LGaJtgZiQV)
    @BaseApi.timing_decorator
    def sn75xNW4A5LGaJtgZiQV(self, nocheck=False):
        obj = self.pc.AMaXd2PkDsrT5cj1SArOe()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "erpStartTime": self.get_the_date(),
            "erpEndTime": self.get_the_date(days=1),
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'ZspzD8hZ0', data, 'main', nocheck)


class R3Xo25O7tV(InitializeParams):
    """配件管理|配件销售|销售列表"""

    @doc(btbwOSZldzzeYBn6qsYo)
    @BaseApi.timing_decorator
    def btbwOSZldzzeYBn6qsYo(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "status": "1",
            "accountNo": INFO['main_account_no'],
            "isEexpress": "0",
            "logisticsNo": self.jd,
            "logisticsNoPrice": "11",
            "saleSupplierId": INFO['main_sale_supplier_id'],
            "supplierName": INFO['vice_sales_customer_name'],
            "remark": "备注",
            "saleOrderAccessoryList": [
                {
                    "accessoryNo": obj[0]['articlesNo'],
                    "accessoryId": obj[0]['id'],
                    "salePrice": "70",
                    "costPrice": obj[0]['totalCost']
                }
            ],
            "deliveryNum": 1,
            "accountName": INFO['main_account_name']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'kyVzUMNcM', data, 'main', nocheck)

    @doc(H4KdZEXetFlTiBVp1fME)
    @BaseApi.timing_decorator
    def H4KdZEXetFlTiBVp1fME(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "status": "2",
            "accountNo": INFO['main_account_no'],
            "isEexpress": "1",
            "logisticsNoPrice": 10,
            "saleSupplierId": INFO['main_sale_supplier_id'],
            "supplierName": INFO['vice_sales_customer_name'],
            "remark": "备注",
            "walletAccountNo": INFO['main_wallet_account_no'],
            "payWay": 1,
            "pickUpType": 1,
            "logisticsCompanyType": 1,
            "userAddressId": INFO['main_user_address_id'],
            "saleOrderAccessoryList": [
                {
                    "accessoryNo": obj[0]['articlesNo'],
                    "accessoryId": obj[0]['id'],
                    "salePrice": "70",
                    "costPrice": obj[0]['totalCost']
                }
            ],
            "deliveryNum": 1,
            "accountName": INFO['main_account_name']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'kyVzUMNcM', data, 'main', nocheck)

    @doc(ye7ARAsQ9uacwEptFiSV)
    @BaseApi.timing_decorator
    def ye7ARAsQ9uacwEptFiSV(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "status": "2",
            "accountNo": INFO['main_account_no'],
            "isEexpress": "1",
            "logisticsNoPrice": 10,
            "saleSupplierId": INFO['main_sale_supplier_id'],
            "supplierName": INFO['vice_sales_customer_name'],
            "remark": "备注",
            "walletAccountNo": INFO['main_wallet_account_no'],
            "payWay": 1,
            "pickUpType": 1,
            "logisticsCompanyType": 1,
            "userAddressId": INFO['main_user_address_id'],
            "saleOrderAccessoryList": [
                {
                    "accessoryNo": obj[0]['articlesNo'],
                    "accessoryId": obj[0]['id'],
                    "salePrice": "99999",
                    "costPrice": obj[0]['totalCost']
                }
            ],
            "deliveryNum": 1,
            "accountName": INFO['main_account_name']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'kyVzUMNcM', data, 'main', nocheck)

    @doc(ivhxLmwFUYJ160MKBThl)
    @BaseApi.timing_decorator
    def ivhxLmwFUYJ160MKBThl(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "status": "2",
            "accountNo": INFO['main_account_no'],
            "isEexpress": "0",
            "logisticsNo": self.jd,
            "logisticsNoPrice": "11",
            "saleSupplierId": INFO['main_sale_supplier_id'],
            "supplierName": INFO['vice_sales_customer_name'],
            "remark": "备注",
            "saleOrderAccessoryList": [
                {
                    "accessoryNo": obj[0]['articlesNo'],
                    "accessoryId": obj[0]['id'],
                    "salePrice": "644",
                    "costPrice": obj[0]['totalCost']
                }
            ],
            "deliveryNum": 1,
            "accountName": INFO['main_account_name']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'kyVzUMNcM', data, 'main', nocheck)

    @doc(bovLHIlzJSfrRryibqyF)
    @BaseApi.timing_decorator
    def bovLHIlzJSfrRryibqyF(self, nocheck=False):
        obj = self.pc.IW1UwaP9R0hojKPOJQSH4(data='b')
        ParamCache.cache_object({"i": obj[0]['accessoryNo']})
        data = {
            "sellType": "1",
            "sellSupplierId": INFO['main_sale_supplier_id'],
            "status": 2,
            "receiveState": 1,
            "logisticsNo": self.jd,
            "logisticsNoPrice": "10",
            "remark": "备注",
            "isEexpress": "0",
            "afterSaleOrderAccessoryList": [
                {
                    "salePrice": obj[0]['salePrice'],
                    "accessoryNo": obj[0]['accessoryNo'],
                    "accessoryId": obj[0]['id'],
                    "saleReturnPrice": obj[0]['returnAblePrice'],
                    "saleOrderNo": obj[0]['saleOrderNo']
                }
            ],
            "deliveryNum": 1,
            "supplierName": INFO['vice_sales_customer_name'],
        }
        self.validate_request_data(data)
        return self._make_request('post', 'Kuc4ZIm7H', data, 'main', nocheck)

    @doc(oe82ledRfRK4B7jiOSVc)
    @BaseApi.timing_decorator
    def oe82ledRfRK4B7jiOSVc(self, nocheck=False):
        obj = self.pc.IW1UwaP9R0hojKPOJQSH4(data='b')
        ParamCache.cache_object({"i": obj[0]['accessoryNo']})
        data = {
            "sellType": "1",
            "sellSupplierId": INFO['main_sale_supplier_id'],
            "status": 2,
            "receiveState": "2",
            "remark": "备注",
            "isEexpress": "0",
            "afterSaleOrderAccessoryList": [
                {
                    "salePrice": obj[0]['salePrice'],
                    "accessoryNo": obj[0]['accessoryNo'],
                    "accessoryId": obj[0]['id'],
                    "saleReturnPrice": obj[0]['returnAblePrice'],
                    "saleOrderNo": obj[0]['saleOrderNo'],
                    "warehouseId": INFO['main_warehouse_id'],
                }
            ],
            "deliveryNum": 1,
            "supplierName": INFO['vice_sales_customer_name'],
        }
        self.validate_request_data(data)
        return self._make_request('post', 'Kuc4ZIm7H', data, 'main', nocheck)

    @doc(hBh7ycF1AumEt4nXwMyZ)
    @BaseApi.timing_decorator
    def hBh7ycF1AumEt4nXwMyZ(self, nocheck=False):
        obj = self.pc.IW1UwaP9R0hojKPOJQSH4()
        obj_2 = self.pc.IW1UwaP9R0hojKPOJQSH4(data='a')
        obj_3 = self.pc.IW1UwaP9R0hojKPOJQSH4(data='b')
        ParamCache.cache_object({"i": obj_3[0]['accessoryNo']})
        data = {
            "sellType": "2",
            "sellSupplierId": INFO['main_sale_supplier_id'],
            "status": 2,
            "remark": "备注",
            "isEexpress": "0",
            "afterSaleOrderAccessoryList": [
                {
                    "salePrice": obj_2[0]['salePrice'],
                    "accessoryNo": obj_2[0]['accessoryNo'],
                    "accessoryId": obj[0]['id'],
                    "saleReturnPrice": obj_3[0]['returnAblePrice'],
                    "saleOrderNo": obj[0]['orderNo'],
                    "newSellPrice": "1"
                }
            ],
            "deliveryNum": 1,
            "supplierName": INFO['vice_sales_customer_name']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'Kuc4ZIm7H', data, 'main', nocheck)

    @doc(dvDaOWftNEncBuIMeo7h)
    @BaseApi.timing_decorator
    def dvDaOWftNEncBuIMeo7h(self, nocheck=False):
        obj = self.pc.IW1UwaP9R0hojKPOJQSH4()
        obj_2 = self.pc.IW1UwaP9R0hojKPOJQSH4(data='a')
        obj_3 = self.pc.IW1UwaP9R0hojKPOJQSH4(data='b')
        ParamCache.cache_object({"i": obj_3[0]['accessoryNo']})
        data = {
            "sellType": "2",
            "sellSupplierId": INFO['main_sale_supplier_id'],
            "status": 2,
            "remark": "备注",
            "isEexpress": "0",
            "afterSaleOrderAccessoryList": [
                {
                    "salePrice": obj_2[0]['salePrice'],
                    "accessoryNo": obj_2[0]['accessoryNo'],
                    "accessoryId": obj[0]['id'],
                    "saleReturnPrice": obj_3[0]['returnAblePrice'],
                    "saleOrderNo": obj[0]['orderNo'],
                    "newSellPrice": obj[0]['salePrice']
                }
            ],
            "deliveryNum": 1,
            "supplierName": INFO['vice_sales_customer_name']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'Kuc4ZIm7H', data, 'main', nocheck)

    @doc(JufIUEkkoghm3ZPziz11)
    @BaseApi.timing_decorator
    def JufIUEkkoghm3ZPziz11(self, nocheck=False):
        obj = self.pc.IW1UwaP9R0hojKPOJQSH4()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "orderNo": obj[0]['orderNo'],
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'm9MsjRh7V', data, 'main', nocheck)

    @doc(U9NQEB15gOzUs1kWPzHL)
    @BaseApi.timing_decorator
    def U9NQEB15gOzUs1kWPzHL(self, nocheck=False):
        obj = self.pc.IW1UwaP9R0hojKPOJQSH4()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "saleSupplierId": INFO['main_sale_supplier_id'],
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'm9MsjRh7V', data, 'main', nocheck)

    @doc(hVsGoqqW3itUAfALyFs8)
    @BaseApi.timing_decorator
    def hVsGoqqW3itUAfALyFs8(self, nocheck=False, status=None):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesType": 2,
            "status": status
        }
        self.validate_request_data(data)
        return self._make_request('post', 'm9MsjRh7V', data, 'main', nocheck)

    @doc(aSQHqjds3CGl32QrMMgp)
    @BaseApi.timing_decorator
    def aSQHqjds3CGl32QrMMgp(self, nocheck=False):
        obj = self.pc.IW1UwaP9R0hojKPOJQSH4()
        ParamCache.cache_object({"i": obj[0]['logisticsNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "logisticsNo": obj[0]['logisticsNo'],
            "articlesType": 2
        }
        self.validate_request_data(data)
        return self._make_request('post', 'm9MsjRh7V', data, 'main', nocheck)

    @doc(Rd9OUwhBuPlpGWYEzDoo)
    @BaseApi.timing_decorator
    def Rd9OUwhBuPlpGWYEzDoo(self, nocheck=False):
        obj = self.pc.IW1UwaP9R0hojKPOJQSH4()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesType": 2,
            "erpStartTime": self.get_the_date(),
            "erpEndTime": self.get_the_date(days=1),
        }
        self.validate_request_data(data)
        return self._make_request('post', 'm9MsjRh7V', data, 'main', nocheck)


class OS9qwvYXb5(InitializeParams):
    """配件管理|入库管理|新到货入库"""

    @doc(Jslqnx0TJYAcPWsTNgWG)
    @BaseApi.timing_decorator
    def Jslqnx0TJYAcPWsTNgWG(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=1)
        ParamCache.cache_object({"i": obj[0]['purchaseLogisticsNo']})
        data = {
            "accessoryList": [
                {
                    "articlesNo": obj[0]['articlesNo'],
                    "warehouseId": INFO['main_warehouse_id']
                }
            ],
            "quickOperation": 1,
            "purchaseOrdersArticlesDTO": {
                "articlesNoList": [
                    obj[0]['articlesNo']
                ],
                "createBy": INFO['special_account_name'],
                "type": "",
                "userId": INFO['special_user_id'],
                "remark": "备注"
            }
        }
        self.validate_request_data(data)
        return self._make_request('post', 'Wgwpc3mTg', data, 'main', nocheck)

    @doc(k75gfpU0uyhS1aEhcD2Y)
    @BaseApi.timing_decorator
    def k75gfpU0uyhS1aEhcD2Y(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=1)
        ParamCache.cache_object({"i": obj[0]['purchaseLogisticsNo']})
        data = {
            "accessoryList": [
                {
                    "articlesNo": obj[0]['articlesNo'],
                    "warehouseId": INFO['main_warehouse_id']
                }
            ],
            "quickOperation": 0,
            "purchaseOrdersArticlesDTO": {
                "articlesNoList": [
                    obj[0]['articlesNo']
                ],
                "createBy": "",
                "type": "",
                "userId": "",
                "remark": ""
            }
        }
        self.validate_request_data(data)
        return self._make_request('post', 'Wgwpc3mTg', data, 'main', nocheck)

    @doc(pZnZ4E4EWsok60VOwAt0)
    @BaseApi.timing_decorator
    def pZnZ4E4EWsok60VOwAt0(self, nocheck=False):
        obj = self.pc.KFkHdZyASZRhMrmNKfHiQ()
        ParamCache.cache_object({"i": obj[0]['logisticsNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "logisticsNo": obj[0]['logisticsNo'],
        }
        self.validate_request_data(data)
        return self._make_request('post', 'apFM5LAR2', data, 'main', nocheck)

    @doc(ddwluOeEUDWfjvQcXtFf)
    @BaseApi.timing_decorator
    def ddwluOeEUDWfjvQcXtFf(self, nocheck=False):
        obj = self.pc.KFkHdZyASZRhMrmNKfHiQ()
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesNo": obj[0]['articlesNo'],
        }
        self.validate_request_data(data)
        return self._make_request('post', 'apFM5LAR2', data, 'main', nocheck)

    @doc(ZHplaC78vCAAs9nTV3tu)
    @BaseApi.timing_decorator
    def ZHplaC78vCAAs9nTV3tu(self, nocheck=False):
        obj = self.pc.KFkHdZyASZRhMrmNKfHiQ()
        ParamCache.cache_object({"i": obj[0]['businessNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesNo": obj[0]['businessNo'],
        }
        self.validate_request_data(data)
        return self._make_request('post', 'apFM5LAR2', data, 'main', nocheck)


class KofyeHTY2V(InitializeParams):
    """配件管理|配件库存|库存调拨"""

    @doc(AdqaPYO38jf7TVM9akKm)
    @BaseApi.timing_decorator
    def AdqaPYO38jf7TVM9akKm(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "outWarehouseId": INFO['main_warehouse_id'],
            "inWarehouseId": INFO['main_item_in_warehouse_id'],
            "remark": "备注",
            "articlesType": "2",
            "articles": [
                {
                    "articlesNo": obj[0]['articlesNo'],
                    "imei": None
                }
            ],
            "expressInfo": {
                "walletAccountNo": INFO['main_wallet_account_no'],
                "isEexpress": 1,
                "estimateFreight": 10,
                "expressCompanyId": "1",
                "expressCompanyName": "顺丰",
                "expectPostTimeStart": self.get_formatted_datetime(),
                "payWay": 1,
                "senderName": "admin",
                "senderPhone": INFO['receiving_phone'],
                "senderProvinceId": INFO['province_id'],
                "senderProvinceName": INFO['city_name'],
                "senderCityId": INFO['city_id'],
                "senderCityName": INFO['city_name'],
                "senderCountyId": INFO['county_id'],
                "senderCountyName": INFO['detailed_address'],
                "senderAddress": INFO['detailed_address'],
                "recipientName": INFO['shipping_address_creator'],
                "recipientPhone": INFO['receiving_phone'],
                "recipientProvinceId": INFO['province_id'],
                "recipientProvinceName": INFO['province_name'],
                "recipientCityId": INFO['city_id'],
                "recipientCityName": INFO['city_name'],
                "recipientCountyId": INFO['county_id'],
                "recipientCountyName": INFO['county_name'],
                "recipientAddress": INFO['detailed_address'],
            }
        }
        self.validate_request_data(data)
        return self._make_request('post', 'x79aTjjzc', data, 'main', nocheck)

    @doc(UXuoreny4UjWmENBXQgX)
    @BaseApi.timing_decorator
    def UXuoreny4UjWmENBXQgX(self, nocheck=False):
        obj = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i=2)
        ParamCache.cache_object({"i": obj[0]['articlesNo']})
        data = {
            "outWarehouseId": INFO['main_warehouse_id'],
            "inWarehouseId": INFO['main_item_in_warehouse_id'],
            "remark": "备注",
            "articlesType": "2",
            "articles": [
                {
                    "articlesNo": obj[0]['articlesNo'],
                    "imei": None
                },
                {
                    "articlesNo": obj[1]['articlesNo'],
                    "imei": None
                }
            ],
            "expressInfo": {
                "walletAccountNo": INFO['main_wallet_account_no'],
                "isEexpress": 0,
                "estimateFreight": None,
                "expressNo": self.sf
            }
        }
        self.validate_request_data(data)
        return self._make_request('post', 'x79aTjjzc', data, 'main', nocheck)

    @doc(vy4GQrC9c2PByhpKlKX7)
    @BaseApi.timing_decorator
    def vy4GQrC9c2PByhpKlKX7(self, nocheck=False):
        obj = self.pc.DgyYP8ygDMIIeEEXHuLbW()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "id": obj[0]['id'],
            "quickOperation": 0
        }
        self.validate_request_data(data)
        return self._make_request('post', 'qIZUVHhiB', data, 'main', nocheck)

    @doc(SfRJFEo1omEqQEMXCt1A)
    @BaseApi.timing_decorator
    def SfRJFEo1omEqQEMXCt1A(self, nocheck=False):
        obj = self.pc.DgyYP8ygDMIIeEEXHuLbW()
        obj_2 = self.pc.DgyYP8ygDMIIeEEXHuLbW(data='b')
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "id": obj[0]['id'],
            "articlesNoList": [
                obj_2[0]['articlesNo']
            ]
        }
        self.validate_request_data(data)
        return self._make_request('post', 'lBPBIvUgX', data, 'main', nocheck)

    @doc(irVf881IgnSudhdqrzNT)
    @BaseApi.timing_decorator
    def irVf881IgnSudhdqrzNT(self, nocheck=False):
        obj = self.pc.DgyYP8ygDMIIeEEXHuLbW()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "orderNo": obj[0]['orderNo'],
            "pageNum": 1,
            "pageSize": 10,
            "articlesType": "2"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'Vqx4RAgDI', data, 'main', nocheck)

    @doc(uxleDdCbgv5xe0Yh9ihY)
    @BaseApi.timing_decorator
    def uxleDdCbgv5xe0Yh9ihY(self, nocheck=False):
        obj = self.pc.DgyYP8ygDMIIeEEXHuLbW()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "outWarehouseId": INFO['main_warehouse_id'],
            "pageNum": 1,
            "pageSize": 10,
            "articlesType": "2"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'Vqx4RAgDI', data, 'main', nocheck)

    @doc(GEzDUNHZDHJGT31d5arP)
    @BaseApi.timing_decorator
    def GEzDUNHZDHJGT31d5arP(self, nocheck=False):
        obj = self.pc.DgyYP8ygDMIIeEEXHuLbW()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "inWarehouseId": INFO['main_item_in_warehouse_id'],
            "pageNum": 1,
            "pageSize": 10,
            "articlesType": "2"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'Vqx4RAgDI', data, 'main', nocheck)

    @doc(ykbpvOAyRCpcWTc8FTo0)
    @BaseApi.timing_decorator
    def ykbpvOAyRCpcWTc8FTo0(self, nocheck=False):
        obj = self.pc.DgyYP8ygDMIIeEEXHuLbW()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "userId": INFO['main_user_id'],
            "pageNum": 1,
            "pageSize": 10,
            "articlesType": "2"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'Vqx4RAgDI', data, 'main', nocheck)

    @doc(N7hyMWrgBhZs95uhMTfo)
    @BaseApi.timing_decorator
    def N7hyMWrgBhZs95uhMTfo(self, nocheck=False, status=None):
        obj = self.pc.DgyYP8ygDMIIeEEXHuLbW()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "status": status,
            "pageNum": 1,
            "pageSize": 10,
            "articlesType": "2"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'Vqx4RAgDI', data, 'main', nocheck)

    @doc(gMOD5rLLkrIFYE4i7uWv)
    @BaseApi.timing_decorator
    def gMOD5rLLkrIFYE4i7uWv(self, nocheck=False):
        obj = self.pc.DgyYP8ygDMIIeEEXHuLbW()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "receiveUserId": INFO['main_user_id'],
            "pageNum": 1,
            "pageSize": 10,
            "articlesType": "2"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'Vqx4RAgDI', data, 'main', nocheck)

    @doc(qUeEiqtgrjyltpAB3WwJ)
    @BaseApi.timing_decorator
    def qUeEiqtgrjyltpAB3WwJ(self, nocheck=False):
        obj = self.pc.DgyYP8ygDMIIeEEXHuLbW()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "startCreateTime": self.get_the_date(),
            "endCreateTime": self.get_the_date(days=1),
            "articlesType": "2"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'Vqx4RAgDI', data, 'main', nocheck)

    @doc(boCbPTo0KQQbybfPC7Dp)
    @BaseApi.timing_decorator
    def boCbPTo0KQQbybfPC7Dp(self, nocheck=False):
        obj = self.pc.DgyYP8ygDMIIeEEXHuLbW()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "startUpdateTime": self.get_the_date(),
            "endUpdateTime": self.get_the_date(days=1),
            "articlesType": "2"
        }
        self.validate_request_data(data)
        return self._make_request('post', 'Vqx4RAgDI', data, 'main', nocheck)


class A1SFjHxpUV(InitializeParams):
    """配件管理|配件销售|销售售后列表"""

    @doc(fQ4Cx53aMDNueSRTtdCt)
    @BaseApi.timing_decorator
    def fQ4Cx53aMDNueSRTtdCt(self, nocheck=False):
        obj = self.pc.Nd81xbVVnxevE1Oy8yXcy()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "orderNo": obj[0]['orderNo']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'r9ytswUaJ', data, 'main', nocheck)

    @doc(M2uPO43Gwj1MxRNJdmCn)
    @BaseApi.timing_decorator
    def M2uPO43Gwj1MxRNJdmCn(self, nocheck=False, status=None):
        obj = self.pc.Nd81xbVVnxevE1Oy8yXcy()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "sellType": status
        }
        self.validate_request_data(data)
        return self._make_request('post', 'r9ytswUaJ', data, 'main', nocheck)

    @doc(cUNSieph0X3TfNdfkcSr)
    @BaseApi.timing_decorator
    def cUNSieph0X3TfNdfkcSr(self, nocheck=False):
        obj = self.pc.Nd81xbVVnxevE1Oy8yXcy()
        ParamCache.cache_object({"i": obj[0]['orderNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "sellSupplierId": INFO['main_sale_supplier_id']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'r9ytswUaJ', data, 'main', nocheck)

    @doc(okQmkaKm4xMprd8BtEc3)
    @BaseApi.timing_decorator
    def okQmkaKm4xMprd8BtEc3(self, nocheck=False):
        obj = self.pc.Nd81xbVVnxevE1Oy8yXcy()
        ParamCache.cache_object({"i": obj[0]['logisticsNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "logisticsNo": obj[0]['logisticsNo']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'r9ytswUaJ', data, 'main', nocheck)

    @doc(S5HIKmlK3427TT3VXmlV)
    @BaseApi.timing_decorator
    def S5HIKmlK3427TT3VXmlV(self, nocheck=False):
        obj = self.pc.Nd81xbVVnxevE1Oy8yXcy()
        ParamCache.cache_object({"i": obj[0]['logisticsNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "userId": INFO['main_user_id']
        }
        self.validate_request_data(data)
        return self._make_request('post', 'r9ytswUaJ', data, 'main', nocheck)

    @doc(XODp5acGT6jdcx10I682)
    @BaseApi.timing_decorator
    def XODp5acGT6jdcx10I682(self, nocheck=False):
        obj = self.pc.Nd81xbVVnxevE1Oy8yXcy()
        ParamCache.cache_object({"i": obj[0]['logisticsNo']})
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "erpStartTime": self.get_the_date(),
            "erpEndTime": self.get_the_date(days=1)
        }
        self.validate_request_data(data)
        return self._make_request('post', 'r9ytswUaJ', data, 'main', nocheck)


if __name__ == '__main__':
    api = ()
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
