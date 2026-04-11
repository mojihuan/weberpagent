# coding: utf-8
import json
from common.base_api import BaseApi
from common.base_params import InitializeParams
from common.file_cache_manager import ParamCache
from common.import_desc import *
from config.user_info import INFO


class MTI16ub3xa(InitializeParams):
    """库存管理|出库管理|地址管理"""

    @doc(SJlFNv1wjIprgodoi79t)
    @BaseApi.timing_decorator
    def SJlFNv1wjIprgodoi79t(self, nocheck=False):
        data = {
            "detailMsg": "和平路" + self.serial + "号",
            "deliverName": "杰克" + self.serial,
            "phone": self.phone,
            "type": "1",
            "provinceId": 1100,
            "cityId": 11010,
            "countyId": 1104,
            "offDefault": 0
        }
        return self._make_request('post', 'uyaeF0TZA', data, 'idle', nocheck)

    @doc(VqptzJXhFGbWdaK6jWAT)
    @BaseApi.timing_decorator
    def VqptzJXhFGbWdaK6jWAT(self, nocheck=False):
        res = self.pc.Ie1Dlx6hKL0xHjTgV7J4p()
        data = {
            "createBy": res[0]['createBy'],
            "createTime": res[0]['createTime'],
            "pageSize": 10,
            "pageNum": 1,
            "orderByColumn": "create_time",
            "isAsc": "desc",
            "id": res[0]['id'],
            "type": "1",
            "typeName": "通用业务",
            "provinceId": INFO['province_id'],
            "provinceName": INFO['province_name'],
            "cityId": INFO['city_id'],
            "cityName": INFO['city_name'],
            "countyId": INFO['county_id'],
            "countyName": INFO['county_name'],
            "detailMsg": INFO['detailed_address'],
            "deliverName": INFO['address_creator'],
            "phone": INFO['receiving_phone'],
            "userId": INFO['main_user_id'],
            "isDelete": 0,
            "tenantId": res[0]['tenantId'],
            "editBool": "false",
            "offDefault": 0
        }
        return self._make_request('put', 'uyaeF0TZA', data, 'idle', nocheck)

    @doc(CLneoMv0agHMlOvAteqD)
    @BaseApi.timing_decorator
    def CLneoMv0agHMlOvAteqD(self, nocheck=False):
        res = self.pc.Ie1Dlx6hKL0xHjTgV7J4p()
        data = [
            res[0]['id']
        ]
        return self._make_request('post', 'IrUQf3u3u', data, 'idle', nocheck)


class G8bx2b1n15(InitializeParams):
    """库存管理|移交接收管理|移交记录"""


class Lm0iuO4IIK(InitializeParams):
    """库存管理|移交接收管理|移交物品"""

    @doc(fcMGsTQ8oTnZfsCSP4CV)
    @BaseApi.timing_decorator
    def fcMGsTQ8oTnZfsCSP4CV(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='3')
        data = {
            "type": "6",
            "userId": INFO['main_user_id'],
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "createBy": INFO['super_admin_account']
        }
        return self._make_request('post', 'ShqXAnyJL', data, 'main', nocheck)


class TbhHz8UAvI(InitializeParams):
    """库存管理|入库管理|物品签收入库"""

    @doc(cDYaPc16prs1VtJEU8mr)
    @BaseApi.timing_decorator
    def cDYaPc16prs1VtJEU8mr(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='1')
        data = {
            "warehouseId": INFO['main_item_warehouse_id'],
            "articlesList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "logisticsNo": res[0]['logisticsNo']
                }
            ],
            "quickOperation": 0,
            "purchaseOrdersArticlesDTO": {
                "articlesNoList": [
                    res[0]['articlesNo']
                ],
                "createBy": "",
                "type": "",
                "userId": ""
            }
        }
        return self._make_request('post', 'Ufjrec0ya', data, 'main', nocheck)


class HSA1BkiNHU(InitializeParams):
    """库存管理|库存列表"""

    @doc(BqEQ0BTtXXYnqUFLxnUK)
    @BaseApi.timing_decorator
    def BqEQ0BTtXXYnqUFLxnUK(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='3')
        data = {
            "type": "4",
            "userId": INFO['special_user_id'],
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "remark": "备注",
            "createBy": INFO['special_account_name']
        }
        return self._make_request('post', 'ShqXAnyJL', data, 'main', nocheck)

    @doc(D3dsNkrEsGlGWkoAbUvn)
    @BaseApi.timing_decorator
    def D3dsNkrEsGlGWkoAbUvn(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='3')
        data = {
            "type": "2",
            "userId": INFO['special_user_id'],
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "remark": "备注",
            "createBy": INFO['special_account_name']
        }
        return self._make_request('post', 'ShqXAnyJL', data, 'main', nocheck)

    @doc(n6qVaJNnhR6yKFZDvMpU)
    @BaseApi.timing_decorator
    def n6qVaJNnhR6yKFZDvMpU(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='3')
        data = {
            "type": "5",
            "userId": INFO['special_user_id'],
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "remark": "备注",
            "createBy": INFO['special_account_name']
        }
        return self._make_request('post', 'ShqXAnyJL', data, 'main', nocheck)

    @doc(wWBLmKauWABXgA16zGq5)
    @BaseApi.timing_decorator
    def wWBLmKauWABXgA16zGq5(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='3')
        data = {
            "type": "1",
            "userId": INFO['special_user_id'],
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "remark": "备注",
            "createBy": INFO['special_account_name']
        }
        return self._make_request('post', 'ShqXAnyJL', data, 'main', nocheck)

    @doc(xrzuFX14hLZb53t2Dpl4)
    @BaseApi.timing_decorator
    def xrzuFX14hLZb53t2Dpl4(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='3')
        data = {
            "type": "3",
            "userId": INFO['special_user_id'],
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "remark": "备注",
            "createBy": INFO['special_account_name']
        }
        return self._make_request('post', 'ShqXAnyJL', data, 'main', nocheck)

    @doc(ELzKzsnP7DBzS58RhuRV)
    @BaseApi.timing_decorator
    def ELzKzsnP7DBzS58RhuRV(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='3')
        data = {
            "type": "5",
            "userId": INFO['main_user_id'],
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "remark": "备注",
            "createBy": INFO['main_account']
        }
        return self._make_request('post', 'ShqXAnyJL', data, 'main', nocheck)

    @doc(cZDVh5eyHxStC2Mli9DI)
    @BaseApi.timing_decorator
    def cZDVh5eyHxStC2Mli9DI(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='3')
        data = {
            "type": "4",
            "userId": INFO['main_user_id'],
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "remark": "备注",
            "createBy": INFO['main_account']
        }
        return self._make_request('post', 'ShqXAnyJL', data, 'main', nocheck)

    @doc(yPtmSmB6LgGBHuYKQex9)
    @BaseApi.timing_decorator
    def yPtmSmB6LgGBHuYKQex9(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='3')
        data = {
            "type": "1",
            "userId": INFO['main_user_id'],
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "remark": "备注",
            "createBy": INFO['main_account']
        }
        return self._make_request('post', 'ShqXAnyJL', data, 'main', nocheck)

    @doc(cQRfPcjML2Pxryt529f9)
    @BaseApi.timing_decorator
    def cQRfPcjML2Pxryt529f9(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='3')
        data = {
            "type": "2",
            "userId": INFO['main_user_id'],
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "remark": "备注",
            "createBy": INFO['main_account']
        }
        return self._make_request('post', 'ShqXAnyJL', data, 'main', nocheck)

    @doc(OAvKjuICy5p7SX9qfvX4)
    @BaseApi.timing_decorator
    def OAvKjuICy5p7SX9qfvX4(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='13')
        data = {
            "type": "3",
            "userId": INFO['main_user_id'],
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "remark": "备注",
            "createBy": INFO['main_account']
        }
        return self._make_request('post', 'ShqXAnyJL', data, 'main', nocheck)

    @doc(vwwTH7A96EyxcdnCteFb)
    @BaseApi.timing_decorator
    def vwwTH7A96EyxcdnCteFb(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='13')
        data = {
            "offExpressage": "0",
            "saleType": "1",
            "deliveryTime": self.get_formatted_datetime(),
            "clientName": INFO['vice_help_sale_supplier_name'],
            "salePrice": "10",
            "refundMethod": 1,
            "receiveState": 1,
            "status": 1,
            "buyReturn": 1,
            "newSalePrice": 0,
            "newPurchasePrice": 0,
            "saleTime": self.get_formatted_datetime(),
            "userId": INFO['main_user_id'],
            "clientId": INFO['vice_help_sale_supplier_id'],
            "accountNo": INFO['main_account_no'],
            "logisticsOrder": self.jd,
            "logisticsNoPrice": "10",
            "platformArticlesNo": self.serial,
            "platformOrderNo": self.serial,
            "purchaseOrdersArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 3,
                    "id": res[0]['id'],
                    "imei": res[0]['imei'],
                    "platformArticlesNo": self.serial,
                    "platformOrderNo": self.serial,
                    "salePrice": "10",
                    "saleSettlePrice": "10",
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1
                    }
                }
            ]
        }
        return self._make_request('post', 'JKSmt0DQk', data, 'main', nocheck)

    @doc(ZUfg9nnQSfSaV9zvenlZ)
    @BaseApi.timing_decorator
    def ZUfg9nnQSfSaV9zvenlZ(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='13')
        data = {
            "offExpressage": "0",
            "saleType": "1",
            "deliveryTime": self.get_formatted_datetime(),
            "clientName": INFO['vice_help_sale_supplier_name'],
            "salePrice": "10",
            "refundMethod": 1,
            "receiveState": 1,
            "status": 2,
            "buyReturn": 1,
            "newSalePrice": 0,
            "newPurchasePrice": 0,
            "saleTime": self.get_formatted_datetime(),
            "userId": INFO['main_user_id'],
            "clientId": INFO['vice_help_sale_supplier_id'],
            "accountNo": INFO['main_account_no'],
            "logisticsOrder": self.jd,
            "logisticsNoPrice": "10",
            "platformArticlesNo": self.serial,
            "platformOrderNo": self.serial,
            "purchaseOrdersArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 3,
                    "id": res[0]['id'],
                    "imei": res[0]['imei'],
                    "platformArticlesNo": self.serial,
                    "platformOrderNo": self.serial,
                    "salePrice": "10",
                    "saleSettlePrice": "10",
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1
                    }
                }
            ]
        }
        return self._make_request('post', 'JKSmt0DQk', data, 'main', nocheck)

    @doc(YyjrBFFVlBe4IC7IrZyD)
    @BaseApi.timing_decorator
    def YyjrBFFVlBe4IC7IrZyD(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='3', j='9')
        res_2 = self.pc.UYV6mZaVwDk4HHhyuWRRp(data='b')
        data = {
            "status": 2,
            "newSalePrice": 0,
            "warehouseId": INFO['main_item_warehouse_id'],
            "saleType": "1",
            "returnType": 1,
            "sellSaleOrderArticlesDTOList": [
                {
                    "accessoryNoList": [],
                    "articlesNo": res[0]['articlesNo'],
                    "newSalePrice": 0,
                    "imei": res[0]['imei'],
                    "saleOrderNo": res[0]['salesOrder'],
                    "saleSettlePrice": res_2[0]['saleOrderInfo']['salePrice'],
                }
            ]
        }
        return self._make_request('post', 'NeFj1qYw3', data, 'main', nocheck)

    @doc(AAfxCTv9LmUzH4gFJKoE)
    @BaseApi.timing_decorator
    def AAfxCTv9LmUzH4gFJKoE(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='3', j='9')
        res_2 = self.pc.UYV6mZaVwDk4HHhyuWRRp(data='b')
        data = {
            "status": 2,
            "newSalePrice": 0,
            "warehouseId": INFO['main_item_warehouse_id'],
            "saleType": "1",
            "returnType": 2,
            "sellSaleOrderArticlesDTOList": [
                {
                    "accessoryNoList": [],
                    "articlesNo": res[0]['articlesNo'],
                    "newSalePrice": 0,
                    "imei": res[0]['imei'],
                    "saleOrderNo": res[0]['salesOrder'],
                    "saleSettlePrice": res_2[0]['saleOrderInfo']['salePrice'],
                }
            ]
        }
        return self._make_request('post', 'NeFj1qYw3', data, 'main', nocheck)

    @doc(kzLjwWovXH0gNxfbTWCC)
    @BaseApi.timing_decorator
    def kzLjwWovXH0gNxfbTWCC(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='3', j='9')
        res_2 = self.pc.UYV6mZaVwDk4HHhyuWRRp(data='b')
        data = {
            "status": 1,
            "newSalePrice": 0,
            "logisticsNo": self.jd,
            "saleType": "1",
            "returnType": 1,
            "remark": "test",
            "sellSaleOrderArticlesDTOList": [
                {
                    "accessoryNoList": [],
                    "articlesNo": res[0]['articlesNo'],
                    "newSalePrice": 0,
                    "imei": res[0]['imei'],
                    "saleOrderNo": res[0]['salesOrder'],
                    "saleSettlePrice": res_2[0]['saleOrderInfo']['salePrice'],
                }
            ]
        }
        return self._make_request('post', 'NeFj1qYw3', data, 'main', nocheck)

    @doc(SyHpEVSfWeSWPDH9hcUa)
    @BaseApi.timing_decorator
    def SyHpEVSfWeSWPDH9hcUa(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='3', j='9')
        res_2 = self.pc.UYV6mZaVwDk4HHhyuWRRp(data='b')
        data = {
            "status": 1,
            "newSalePrice": 0,
            "saleType": "1",
            "returnType": 2,
            "remark": "备注",
            "sellSaleOrderArticlesDTOList": [
                {
                    "accessoryNoList": [],
                    "articlesNo": res[0]['articlesNo'],
                    "newSalePrice": 0,
                    "imei": res[0]['imei'],
                    "saleOrderNo": res[0]['salesOrder'],
                    "saleSettlePrice": res_2[0]['saleOrderInfo']['salePrice'],
                }
            ]
        }
        return self._make_request('post', 'NeFj1qYw3', data, 'main', nocheck)

    @doc(VCS0Uc7dtvSPIuHtNbaI)
    @BaseApi.timing_decorator
    def VCS0Uc7dtvSPIuHtNbaI(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='3', j='9')
        res_2 = self.pc.UYV6mZaVwDk4HHhyuWRRp(data='b')
        data = {
            "status": 2,
            "newSalePrice": 20,
            "warehouseId": INFO['main_in_warehouse_id'],
            "accessoryType": 3,
            "accessoryNo": "PJ0140",
            "saleType": "2",
            "returnType": 1,
            "sellSaleOrderArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "platformArticlesNo": self.serial,
                    "newSalePrice": 20,
                    "saleOrderNo": res[0]['salesOrder'],
                    "saleSettlePrice": res_2[0]['saleOrderInfo']['salePrice'],
                    "accessoryNoList": [
                        {
                            "brandId": 2,
                            "brandName": "三星",
                            "modelId": 7792,
                            "modelName": "W2015",
                            "accessoryType": 3,
                            "accessoryNo": "PJ0140",
                            "accessoryQuality": 3,
                            "accessoryPrice": 20,
                            "articlesTypeId": 1,
                            "articlesTypeName": "手机",
                            "channelType": 1,
                            "purchasePrice": 20
                        }
                    ]
                }
            ]
        }
        return self._make_request('post', 'NeFj1qYw3', data, 'main', nocheck)

    @doc(HNDvVgQsF5uXmqKb3obN)
    @BaseApi.timing_decorator
    def HNDvVgQsF5uXmqKb3obN(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='3', j='9')
        res_2 = self.pc.UYV6mZaVwDk4HHhyuWRRp(data='b')
        data = {
            "status": 1,
            "newSalePrice": 30,
            "logisticsNo": self.jd,
            "accessoryType": 3,
            "accessoryNo": "PJ0170",
            "saleType": "2",
            "returnType": 1,
            "remark": "test",
            "sellSaleOrderArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "platformArticlesNo": "16200143",
                    "newSalePrice": 30,
                    "saleOrderNo": res[0]['salesOrder'],
                    "saleSettlePrice": res_2[0]['saleOrderInfo']['salePrice'],
                    "accessoryNoList": [
                        {
                            "brandId": 313,
                            "brandName": "VIVO",
                            "modelId": 6668,
                            "modelName": "Y67",
                            "accessoryType": 3,
                            "accessoryNo": "PJ0170",
                            "accessoryQuality": 3,
                            "accessoryPrice": 40,
                            "articlesTypeId": 1,
                            "articlesTypeName": "手机",
                            "channelType": 1,
                            "purchasePrice": 40
                        }
                    ]
                }
            ]
        }
        return self._make_request('post', 'NeFj1qYw3', data, 'main', nocheck)

    @doc(Nk7bVBssIb2JEsWwVc2R)
    @BaseApi.timing_decorator
    def Nk7bVBssIb2JEsWwVc2R(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='3', j='9')
        res_2 = self.pc.UYV6mZaVwDk4HHhyuWRRp(data='b')
        data = {
            "status": 2,
            "newSalePrice": 50,
            "saleType": "5",
            "returnType": 1,
            "remark": "备注",
            "sellSaleOrderArticlesDTOList": [
                {
                    "accessoryNoList": [],
                    "articlesNo": res[0]['articlesNo'],
                    "newSalePrice": 50,
                    "imei": res[0]['imei'],
                    "saleOrderNo": res[0]['salesOrder'],
                    "saleSettlePrice": res_2[0]['saleOrderInfo']['salePrice']
                }
            ]
        }
        return self._make_request('post', 'NeFj1qYw3', data, 'main', nocheck)

    @doc(D60ATnrNOPRjZtH7QJQv)
    @BaseApi.timing_decorator
    def D60ATnrNOPRjZtH7QJQv(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='1')
        data = {
            "articlesNo": res[0]['articlesNo'],
            "remark": "备注"
        }
        return self._make_request('post', 'R7HA7rwAV', data, 'main', nocheck)

    @doc(KgeXqOhDT97S9ajhSDxB)
    @BaseApi.timing_decorator
    def KgeXqOhDT97S9ajhSDxB(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='3')
        data = {
            "id": res[0]['id'],
            "articlesNo": res[0]['articlesNo'],
            "purchaseArticlesInfoDTO": {
                "id": res[0]['id'],
                "articlesNo": res[0]['articlesNo'],
                "articlesTypeName": res[0]['articlesTypeName'],
                "brandId": res[0]['brandId'],
                "brandName": res[0]['brandName'],
                "modelId": res[0]['modelId'],
                "modelName": res[0]['modelName'],
                "smallModelId": 75,
                "smallModelName": "A1699",
                "buyChannelId": 16,
                "buyChannelName": "国行",
                "colorId": 49,
                "colorName": "金色",
                "romId": 37,
                "romName": "16G",
                "batteryHealthId": 23024,
                "batteryHealthName": "电池健康度100%",
                "warrantyDurationId": 23005,
                "warrantyDurationName": "保修时长≥330天",
                "machineTypeId": 862,
                "machineTypeName": "二手优品",
                "finenessId": 1,
                "finenessName": "全新仅拆封"
            }
        }
        return self._make_request('post', 'R31Db9DLe', data, 'main', nocheck)


class M1swfi30oc(InitializeParams):
    """库存管理|入库管理|物流列表"""


class IPBU7G33xP(InitializeParams):
    """库存管理|入库管理|物流签收入库"""

    @doc(Jv79uDAMnGFSvRHesu0B)
    @BaseApi.timing_decorator
    def Jv79uDAMnGFSvRHesu0B(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='1')
        data = {
            "warehouseId": INFO['main_item_warehouse_id'],
            "articlesList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "warehouseId": ""
                }
            ],
            "logisticsNo": res[0]['logisticsNo'],
            "quickOperation": 0,
            "purchaseOrdersArticlesDTO": {
                "articlesNoList": [
                    res[0]['articlesNo'],
                ],
                "createBy": "",
                "type": "",
                "userId": "",
                "remark": ""
            }
        }
        return self._make_request('post', 'DYbHAZqxU', data, 'main', nocheck)

    @doc(hhbi3Grk7w3kXVnHxfNE)
    @BaseApi.timing_decorator
    def hhbi3Grk7w3kXVnHxfNE(self, nocheck=False):
        res = self.pc.Jc9Odo2T6JqvbWDRSsDXy()
        data = {
            "warehouseId": INFO['main_item_warehouse_id'],
            "articlesList": [
                {
                    "articlesNo": res[0]['helpSellArticlesNo'],
                    "warehouseId": ""
                }
            ],
            "logisticsNo": res[0]['deliverExpressNo'],
            "quickOperation": 0,
            "purchaseOrdersArticlesDTO": {
                "articlesNoList": [],
                "createBy": "",
                "type": "",
                "userId": "",
                "remark": ""
            }
        }
        return self._make_request('post', 'DYbHAZqxU', data, 'vice', nocheck)


class MLkZRHOuRf(InitializeParams):
    """库存管理|出库管理|仅出库订单列表"""

    @doc(e2AnAaVdqHxAw7jEV92t)
    @BaseApi.timing_decorator
    def e2AnAaVdqHxAw7jEV92t(self, nocheck=False):
        res = self.pc.QYSFzOWmZ2zYnize8ppKN()
        res_2 = self.pc.QYSFzOWmZ2zYnize8ppKN(data='a')
        data = {
            "returnMethod": "1",
            "logisticsOrder": self.jd,
            "returnTime": self.get_formatted_datetime(),
            "warehouseId": INFO['main_in_warehouse_id'],
            "articlesList": [
                {
                    "articlesNo": res_2[0]['articlesNo'],
                    "orderNo": res[0]['orderNo']
                }
            ]
        }
        return self._make_request('post', 'gNp2tTkFA', data, 'main', nocheck)

    @doc(M04F4OTZMxDuTL4I0abo)
    @BaseApi.timing_decorator
    def M04F4OTZMxDuTL4I0abo(self, nocheck=False):
        res = self.pc.QYSFzOWmZ2zYnize8ppKN()
        res_2 = self.pc.QYSFzOWmZ2zYnize8ppKN(data='a')
        data = {
            "returnMethod": "2",
            "logisticsOrder": self.jd,
            "returnTime": self.get_formatted_datetime(),
            "articlesList": [
                {
                    "articlesNo": res_2[0]['articlesNo'],
                    "orderNo": res[0]['orderNo']
                }
            ]
        }
        return self._make_request('post', 'gNp2tTkFA', data, 'main', nocheck)

    @doc(AfpbFoR3N3DHrELC3fyQ)
    @BaseApi.timing_decorator
    def AfpbFoR3N3DHrELC3fyQ(self, nocheck=False):
        res = self.pc.QYSFzOWmZ2zYnize8ppKN()
        res_2 = self.pc.QYSFzOWmZ2zYnize8ppKN(data='a')
        res_3 = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='3', j='18')
        data = {
            "saleType": "1",
            "clientId": INFO['main_sale_supplier_id'],
            "clientName": INFO['vice_sales_customer_name'],
            "status": "1",
            "accountNo": INFO['main_account_no'],
            "accountName": INFO['main_account_name'],
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res_3[0]['id'],
                    "articlesNo": res_2[0]['articlesNo'],
                    "articlesState": 18,
                    "salePrice": 11,
                    "platformOrderNo": self.serial,
                    "remark": "仅出库备注",
                    "saleSettlePrice": 11,
                    "outboundOrderNo": res[0]['orderNo']
                }
            ]
        }
        return self._make_request('post', 'AXLzdlBvg', data, 'main', nocheck)

    @doc(x4yuI0I1abq0vQb0mI6o)
    @BaseApi.timing_decorator
    def x4yuI0I1abq0vQb0mI6o(self, nocheck=False):
        res = self.pc.QYSFzOWmZ2zYnize8ppKN()
        res_2 = self.pc.QYSFzOWmZ2zYnize8ppKN(data='a')
        res_3 = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='3', j='18')
        data = {
            "saleType": "1",
            "clientId": INFO['main_sale_supplier_id'],
            "clientName": INFO['vice_sales_customer_name'],
            "status": "2",
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res_3[0]['id'],
                    "articlesNo": res_2[0]['articlesNo'],
                    "articlesState": 18,
                    "salePrice": 120,
                    "platformOrderNo": self.serial,
                    "remark": "备注1",
                    "saleSettlePrice": 120,
                    "outboundOrderNo": res[0]['orderNo']
                }
            ]
        }
        return self._make_request('post', 'AXLzdlBvg', data, 'main', nocheck)

    @doc(ZUdNkyxThIMbrQMjq4A0)
    @BaseApi.timing_decorator
    def ZUdNkyxThIMbrQMjq4A0(self, nocheck=False):
        time = self.get_current_timestamp_ms()
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp()
        data = {
            "saleTime": self.get_formatted_datetime(),
            "saleType": "4",
            "clientId": INFO['main_sale_supplier_id'],
            "clientName": INFO['vice_sales_customer_name'],
            "accountNo": INFO['main_account_no'],
            "accountName": INFO['main_account_name'],
            "userId": INFO['main_user_id'],
            "deliveryId": INFO['main_user_id'],
            "deliveryTime": self.get_formatted_datetime(),
            "status": 1,
            "logisticsOrder": self.jd,
            "logisticsNoPrice": 11,
            "remark": "备注",
            "isEexpress": "0",
            "offExpressage": "0",
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res[0]['id'],
                    "imei": res[0]['imei'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 3,
                    "salePrice": None,
                    "platformArticlesNo": res[0]['platformArticlesNo'],
                    "platformOrderNo": None,
                    "remark": "备注",
                    "finenessId": None,
                    "articlesInfoId": time,
                    "purchaseArticlesInfoDTO": {
                        "finenessId": None,
                        "id": time
                    },
                    "saleSettlePrice": ""
                }
            ]
        }
        return self._make_request('post', 'hgftWOpCZ', data, 'main', nocheck)

    @doc(qawEHf7WaxftnDj1QxYR)
    @BaseApi.timing_decorator
    def qawEHf7WaxftnDj1QxYR(self, nocheck=False):
        time = self.get_current_timestamp_ms()
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp()
        data = {
            "saleTime": self.get_formatted_datetime(),
            "saleType": "4",
            "clientId": INFO['main_sale_supplier_id'],
            "clientName": INFO['vice_sales_customer_name'],
            "accountNo": INFO['main_account_no'],
            "accountName": INFO['main_account_name'],
            "userId": INFO['main_user_id'],
            "deliveryId": INFO['main_user_id'],
            "deliveryTime": self.get_formatted_datetime(),
            "status": 1,
            "logisticsNoPrice": 10,
            "walletAccountNo": INFO['main_wallet_account_no'],
            "remark": "备注",
            "isEexpress": "1",
            "payWay": 2,
            "pickUpType": 1,
            "logisticsCompanyType": 1,
            "userAddressId": INFO['main_user_address_id'],
            "offExpressage": "1",
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res[0]['id'],
                    "imei": res[0]['imei'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 3,
                    "salePrice": None,
                    "platformArticlesNo": res[0]['platformArticlesNo'],
                    "platformOrderNo": None,
                    "remark": "备注",
                    "finenessId": 2,
                    "articlesInfoId": time,
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 2,
                        "id": time
                    },
                    "saleSettlePrice": ""
                }
            ]
        }
        return self._make_request('post', 'hgftWOpCZ', data, 'main', nocheck)


class GrqUVUXI3u(InitializeParams):
    """库存管理|出库管理|采购售后出库"""

    @doc(DZpllRLFofze0dkHhqfW)
    @BaseApi.timing_decorator
    def DZpllRLFofze0dkHhqfW(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='10')
        data = {
            "saleState": 5,
            "offExpressage": "0",
            "logisticsNoPrice": 11,
            "logisticsOrder": self.jd,
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "purchaseOrdersArticlesDTOList": [
                {
                    "purchaseNo": res[0]['purchaseNo'],
                    "articlesNo": res[0]['articlesNo'],
                    "id": res[0]['id'],
                    "purchasePrice": res[0]['purchasePrice'],
                    "saleRemake": "备注"
                }
            ],
            "deliveryTime": self.get_formatted_datetime(),
        }
        return self._make_request('post', 'TDNsMZDYJ', data, 'main', nocheck)


class XmR5kBz1S1(InitializeParams):
    """库存管理|移交接收管理|接收物品"""

    @doc(Xj9FgGV65jL0Oi7nZXWg)
    def Xj9FgGV65jL0Oi7nZXWg(self, nocheck=False):
        res = self.pc.LWT9dymUmXdvWqLk1qEeA(i='6')
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'WpZgDxZLH', data, 'main', nocheck)

    @doc(GvUiJ1UCIayox4CCu44j)
    def GvUiJ1UCIayox4CCu44j(self, nocheck=False):
        res = self.pc.LWT9dymUmXdvWqLk1qEeA(i='6')
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'WpZgDxZLH', data, 'main', nocheck)


class XwUhCCnV8j(InitializeParams):
    """库存管理|出库管理|销售出库"""

    def item_number(self, nocheck=False):
        res = self.pc.XTk41pUDr28xCf1YL17uR()
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'QBZVuqz0S', data, 'main', nocheck)

    @doc(sX84nolF0TRL5RWSl6zx)
    def sX84nolF0TRL5RWSl6zx(self, nocheck=False):
        time = self.get_current_timestamp_ms()
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='13')
        data = {
            "saleTime": self.get_formatted_datetime(),
            "saleType": "1",
            "clientId": INFO['main_sale_supplier_id'],
            "clientName": INFO['vice_sales_customer_name'],
            "accountNo": INFO['main_account_no'],
            "accountName": INFO['main_account_name'],
            "userId": INFO['main_user_id'],
            "deliveryId": INFO['main_user_id'],
            "deliveryTime": self.get_formatted_datetime(),
            "status": 1,
            "logisticsOrder": self.jd,
            "logisticsNoPrice": 10,
            "isEexpress": "0",
            "offExpressage": "0",
            "orderPayInfoList": [
                {
                    "accountNo": INFO['main_account_no'],
                    "voucherImg": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com//erp-imgfiles/%2Fepbox-erp/20250820/WIehcT%2B7sg/I4FjLToJM%2Bw%3D%3D.jpg",
                    "payPrice": 10,
                    "accountName": INFO['main_account_name'],
                }
            ],
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res[0]['id'],
                    "imei": res[0]['imei'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 13,
                    "salePrice": 10,
                    "platformArticlesNo": self.serial,
                    "platformOrderNo": self.serial,
                    "remark": self.serial,
                    "finenessId": 1,
                    "articlesInfoId": time,
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1,
                        "id": time
                    },
                    "saleSettlePrice": 10
                }
            ]
        }
        return self._make_request('post', 'JKSmt0DQk', data, 'main', nocheck)

    @doc(cuv4NM82E2Es3yAJkvoi)
    def cuv4NM82E2Es3yAJkvoi(self, nocheck=False):
        time = self.get_current_timestamp_ms()
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='13')
        data = {
            "saleTime": self.get_formatted_datetime(),
            "saleType": "1",
            "clientId": INFO['main_sale_supplier_id'],
            "clientName": INFO['vice_sales_customer_name'],
            "accountNo": INFO['main_account_no'],
            "accountName": INFO['main_account_name'],
            "userId": INFO['main_user_id'],
            "deliveryId": INFO['main_user_id'],
            "deliveryTime": self.get_formatted_datetime(),
            "status": 2,
            "logisticsOrder": self.jd,
            "logisticsNoPrice": 10,
            "isEexpress": "0",
            "offExpressage": "0",
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res[0]['id'],
                    "imei": res[0]['imei'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 13,
                    "salePrice": 501,
                    "platformArticlesNo": self.serial,
                    "platformOrderNo": self.serial,
                    "remark": self.serial,
                    "finenessId": None,
                    "articlesInfoId": time,
                    "purchaseArticlesInfoDTO": {
                        "finenessId": None,
                        "id": time
                    },
                    "saleSettlePrice": 501
                }
            ]
        }
        return self._make_request('post', 'JKSmt0DQk', data, 'main', nocheck)

    @doc(P7mmCcwk64F1knIdDObr)
    def P7mmCcwk64F1knIdDObr(self, nocheck=False):
        time = self.get_current_timestamp_ms()
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(data='a', i='2', j='13')
        res_2 = self.pc.Jc9Odo2T6JqvbWDRSsDXy()
        data = {
            "saleTime": self.get_formatted_datetime(),
            "saleType": "1",
            "clientId": INFO['vice_help_sale_supplier_id'],
            "clientName": INFO['vice_help_sale_supplier_name'],
            "accountNo": INFO['vice_account_no'],
            "accountName": INFO['main_account_name'],
            "userId": INFO['vice_user_id'],
            "deliveryId": INFO['vice_user_id'],
            "deliveryTime": self.get_formatted_datetime(),
            "status": 1,
            "logisticsOrder": self.jd,
            "logisticsNoPrice": 11,
            "isEexpress": "0",
            "offExpressage": "0",
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res[0]['id'],
                    "imei": res_2[0]['imei'],
                    "articlesNo": res_2[0]['helpSellArticlesNo'],
                    "articlesState": 13,
                    "salePrice": 11,
                    "platformArticlesNo": self.serial,
                    "platformOrderNo": self.serial,
                    "remark": self.serial,
                    "finenessId": 1,
                    "articlesInfoId": time,
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1,
                        "id": time
                    },
                    "saleSettlePrice": 11
                }
            ]
        }
        return self._make_request('post', 'JKSmt0DQk', data, 'vice', nocheck)

    @doc(B79xRAooA8OFtgTSsB20)
    def B79xRAooA8OFtgTSsB20(self, nocheck=False):
        self.item_number()
        time = self.get_current_timestamp_ms()
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='13')
        data = {
            "saleTime": self.get_formatted_datetime(),
            "saleType": "3",
            "clientId": INFO['main_sale_supplier_id'],
            "clientName": INFO['vice_sales_customer_name'],
            "accountNo": INFO['main_account_no'],
            "accountName": INFO['main_account_name'],
            "userId": INFO['main_user_id'],
            "deliveryId": INFO['main_user_id'],
            "deliveryTime": self.get_formatted_datetime(),
            "status": 1,
            "logisticsOrder": self.jd,
            "logisticsNoPrice": 11,
            "isEexpress": "0",
            "offExpressage": "0",
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res[0]['id'],
                    "imei": res[0]['imei'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 13,
                    "salePrice": 11,
                    "platformArticlesNo": self.serial,
                    "platformOrderNo": self.serial,
                    "remark": self.serial,
                    "finenessId": 1,
                    "articlesInfoId": time,
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1,
                        "id": time
                    },
                    "saleSettlePrice": ""
                }
            ]
        }
        return self._make_request('post', 'JKSmt0DQk', data, 'main', nocheck)

    @doc(Qimx5yME2xvTwfpxXDWH)
    def Qimx5yME2xvTwfpxXDWH(self, nocheck=False):
        time = self.get_current_timestamp_ms()
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='13')
        data = {
            "saleTime": self.get_formatted_datetime(),
            "saleType": "5",
            "clientId": INFO['main_sale_supplier_id'],
            "clientName": INFO['vice_sales_customer_name'],
            "accountNo": INFO['main_account_no'],
            "accountName": INFO['main_account_name'],
            "userId": INFO['main_user_id'],
            "deliveryId": INFO['main_user_id'],
            "deliveryTime": self.get_formatted_datetime(),
            "status": 1,
            "logisticsOrder": self.jd,
            "logisticsNoPrice": 11,
            "isEexpress": "0",
            "offExpressage": "0",
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res[0]['id'],
                    "imei": res[0]['imei'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 3,
                    "salePrice": None,
                    "platformArticlesNo": self.serial,
                    "platformOrderNo": None,
                    "remark": "备注",
                    "finenessId": 1,
                    "articlesInfoId": time,
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1,
                        "id": time
                    },
                    "saleSettlePrice": ""
                }
            ]
        }
        return self._make_request('post', 'JKSmt0DQk', data, 'main', nocheck)

    @doc(RbCSsdTsnVGk7P77B8ca)
    def RbCSsdTsnVGk7P77B8ca(self, nocheck=False):
        time = self.get_current_timestamp_ms()
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='13')
        res_2 = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i='2')
        data = {
            "saleTime": self.get_formatted_datetime(),
            "saleType": "1",
            "clientId": INFO['main_sale_supplier_id'],
            "clientName": INFO['vice_sales_customer_name'],
            "accountNo": INFO['main_account_no'],
            "accountName": INFO['main_account_name'],
            "userId": INFO['main_user_id'],
            "deliveryId": INFO['main_user_id'],
            "deliveryTime": self.get_formatted_datetime(),
            "status": 2,
            "logisticsOrder": self.jd,
            "logisticsNoPrice": 11,
            "isEexpress": "0",
            "offExpressage": "0",
            "giveAccessoryArticlesNoList": [
                res_2[0]['articlesNo']
            ],
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res[0]['id'],
                    "imei": res[0]['imei'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 3,
                    "salePrice": 100,
                    "platformArticlesNo": self.serial,
                    "platformOrderNo": self.serial,
                    "remark": "备注",
                    "finenessId": 1,
                    "articlesInfoId": time,
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1,
                        "id": time
                    },
                    "saleSettlePrice": 100
                }
            ]
        }
        return self._make_request('post', 'JKSmt0DQk', data, 'main', nocheck)


class HKYbWELZop(InitializeParams):
    """库存管理|出库管理|销售售后出库"""

    @BaseApi.timing_decorator
    def item_number(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='15')
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'QBZVuqz0S', data, 'main', nocheck)

    @doc(A9xC9JwOkl75SfoIqlTM)
    @BaseApi.timing_decorator
    def A9xC9JwOkl75SfoIqlTM(self, nocheck=False):
        self.item_number()
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='15')
        res_2 = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='3')
        data = {
            "saleUserId": INFO['main_sale_supplier_id'],
            "offExpressage": "0",
            "logisticsNo": self.jd,
            "logisticsPrice": "11",
            "saleType": "7",
            "purchaseOrdersArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "remark": self.serial,
                    "saleSettlePrice": res[0]['totalRevenue']
                }
            ],
            "newPurchaseOrdersArticlesDTO": {
                "articlesNo": res_2[0]['articlesNo'],
                "imei": res_2[0]['imei'],
                "newSalePrice": 11,
                "platformArticlesNo": res_2[0]['platformArticlesNo'],
                "platformOrderNo": self.serial,
                "remark": self.serial,
                "costPrice": res_2[0]['sumCost']
            },
            "isSaleType": True
        }
        return self._make_request('post', 'zuYSO5V1e', data, 'main', nocheck)

    @doc(FUNbZmjhH4ul2nZkvDV2)
    @BaseApi.timing_decorator
    def FUNbZmjhH4ul2nZkvDV2(self, nocheck=False):
        self.item_number()
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='15')
        data = {
            "saleUserId": INFO['main_sale_supplier_id'],
            "logisticsNo": self.jd,
            "logisticsPrice": "11",
            "saleType": "6",
            "purchaseOrdersArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "remark": None,
                    "saleSettlePrice": 40
                }
            ],
            "newPurchaseOrdersArticlesDTO": {
                "articlesNo": "",
                "imei": "",
                "newSalePrice": "",
                "platformArticlesNo": "",
                "platformOrderNo": "",
                "remark": "",
                "costPrice": 0
            },
            "isSaleType": True
        }
        return self._make_request('post', 'zuYSO5V1e', data, 'main', nocheck)

    @doc(teC3vcKAJkMnapeaIQEH)
    @BaseApi.timing_decorator
    def teC3vcKAJkMnapeaIQEH(self, nocheck=False):
        self.item_number()
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='15')
        data = {
            "logisticsNo": self.jd,
            "logisticsPrice": "40",
            "saleUserId": INFO['main_sale_supplier_id'],
            "saleType": "3",
            "purchaseOrdersArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "remark": None,
                    "saleSettlePrice": 42
                }
            ],
            "newPurchaseOrdersArticlesDTO": {
                "articlesNo": "",
                "imei": "",
                "newSalePrice": "",
                "platformArticlesNo": "",
                "platformOrderNo": "",
                "remark": "",
                "costPrice": 0
            },
            "isSaleType": True
        }
        return self._make_request('post', 'zuYSO5V1e', data, 'main', nocheck)


class S9pHfGlZA1(InitializeParams):
    """库存管理|出库管理|送修出库"""

    @doc(Qp71Bn8xqI3rvwuJ9xCr)
    @BaseApi.timing_decorator
    def Qp71Bn8xqI3rvwuJ9xCr(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='16')
        data = {
            "saleState": 13,
            "offExpressage": "0",
            "logisticsNoPrice": 11,
            "logisticsNo": self.sf,
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "purchaseOrdersArticlesDTOList": [
                {
                    "purchaseNo": res[0]['purchaseNo'],
                    "articlesNo": res[0]['articlesNo'],
                    "id": res[0]['id'],
                    "purchasePrice": res[0]['purchasePrice'],
                    "saleRemake": "备注",
                    "imei": res[0]['imei'],
                    "articlesType": 1,
                    "platformArticlesNo": res[0]['platformArticlesNo'],
                    "articlesTypeId": 1,
                    "articlesTypeName": res[0]['articlesTypeName']
                }
            ],
            "deliveryTime": self.get_formatted_datetime(),
        }
        return self._make_request('post', 'MQ0HvcES5', data, 'main', nocheck)


class F0teh65lah(InitializeParams):
    """库存管理|库存盘点"""

    @doc(completed_inventory_count)
    @BaseApi.timing_decorator
    def add_inventory_count(self, nocheck=False):
        data = {
            "stockUserId": INFO['main_user_id']
        }
        return self._make_request('post', 'HZAtPzJab', data, 'main', nocheck)

    @doc(completed_inventory_count)
    @BaseApi.timing_decorator
    def submit_inventory_count(self, nocheck=False):
        res = self.pc.Ux7lF2b6qktEytPTzyaQW()
        res_2 = self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2)
        data = {
            "stockNo": res[0]['stockNo'],
            "articlesNoList": [
                res_2[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'w7tDFnhQH', data, 'main', nocheck)

    @doc(yfkRUCxXwAxP0gqU85sU)
    @BaseApi.timing_decorator
    def yfkRUCxXwAxP0gqU85sU(self, nocheck=False):
        self.add_inventory_count()
        self.submit_inventory_count()
        res = self.pc.Ux7lF2b6qktEytPTzyaQW()
        data = {
            "stockNo": res[0]['stockNo'],
            "remark": "备注"
        }
        return self._make_request('post', 'pFdaHkDL4', data, 'main', nocheck)


class InLEWxc2tL(InitializeParams):
    """库存管理|库存调拨"""

    @doc(TkJYyYtSzad1UKsgz33u)
    @BaseApi.timing_decorator
    def TkJYyYtSzad1UKsgz33u(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='3')
        data = {
            "outWarehouseId": INFO['main_item_warehouse_id'],
            "inWarehouseId": INFO['main_item_in_warehouse_id'],
            "remark": "备注",
            "articlesType": "1",
            "articles": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei']
                }
            ],
            "expressInfo": {
                "walletAccountNo": INFO['main_wallet_account_no'],
                "isEexpress": 0,
                "estimateFreight": None,
                "expressNo": self.jd
            }
        }
        return self._make_request('post', 'xqlOfxcj4', data, 'main', nocheck)

    @doc(paab2hqQQJLuUeP31Y4e)
    @BaseApi.timing_decorator
    def paab2hqQQJLuUeP31Y4e(self, nocheck=False):
        res = self.pc.XHyhIffDlKvRSMGo6DlG2()
        res_2 = self.pc.XHyhIffDlKvRSMGo6DlG2(data='a')
        data = {
            "id": res[0]['id'],
            "quickOperation": 0,
            "purchaseOrdersArticlesDTO": {
                "articlesNoList": [
                    res_2['itemList'][0]['articlesNo']
                ],
                "userId": None,
                "type": None,
                "remark": None
            }
        }
        return self._make_request('post', 'E0q5Zy8t6', data, 'main', nocheck)

    @doc(xurEsLRqBkTUszD8mRjE)
    @BaseApi.timing_decorator
    def xurEsLRqBkTUszD8mRjE(self, nocheck=False):
        res = self.pc.XHyhIffDlKvRSMGo6DlG2()
        res_2 = self.pc.XHyhIffDlKvRSMGo6DlG2(data='a')
        data = {
            "id": res[0]['id'],
            "articlesNoList": [
                res_2['itemList'][0]['articlesNo']
            ]
        }
        return self._make_request('post', 'kvtboyOVX', data, 'main', nocheck)


if __name__ == '__main__':
    api = ()
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
