# coding: utf-8
import json
from common.base_api import BaseApi
from common.base_params import InitializeParams, is_performance_close
from common.file_cache_manager import ParamCache
from common.import_desc import *
from config.user_info import INFO


class EPSnRVHPCS(InitializeParams):
    """商品销售|销售售后管理|销售售后处理"""

    @doc(DjkghfK5et2Z3KvN6d3n)
    @BaseApi.timing_decorator
    def DjkghfK5et2Z3KvN6d3n(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='3', j='9')
        data = {
            "saleType": "1",
            "remark": "备注",
            "status": 2,
            "payState": "2",
            "returnType": 1,
            "warehouseId": INFO['main_item_warehouse_id'],
            "sellSaleOrderArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "platformArticlesNo": res[0]['platformArticlesNo'],
                    "newSalePrice": 0,
                    "saleSettlePrice": res[0]['sumCost'],
                    "saleOrderNo": res[0]['salesOrder'],
                    "accountNo": None,
                    "accessoryNoList": []
                }
            ]
        }
        return self._make_request('post', 'NeFj1qYw3', data, 'main', nocheck)

    @doc(w2XcfZ42REixTHsF0D6w)
    @BaseApi.timing_decorator
    def w2XcfZ42REixTHsF0D6w(self, nocheck=False):
        res = self.pc.JU8QYbNi3BDlSn2XaNZKe()
        data = {
            "saleType": "2",
            "remark": "备注",
            "status": 2,
            "payState": "2",
            "warehouseId": INFO['main_item_warehouse_id'],
            "sellSaleOrderArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "platformArticlesNo": res[0]['platformArticlesNo'],
                    "newSalePrice": int(self.number),
                    "saleSettlePrice": res[0]['saleSettlePrice'],
                    "saleOrderNo": res[0]['salesOrder'],
                    "accountNo": None,
                    "accessoryNoList": [
                        {
                            "brandId": res[0]['brandId'],
                            "brandName": res[0]['brandName'],
                            "modelId": res[0]['modelId'],
                            "modelName": res[0]['modelName'],
                            "accessoryType": 2,
                            "accessoryNo": "PJ0216",
                            "accessoryQuality": 3,
                            "accessoryPrice": int(self.number),
                            "articlesTypeId": 1,
                            "articlesTypeName": res[0]['articlesTypeName'],
                            "channelType": 1,
                            "purchasePrice": int(self.number)
                        }
                    ]
                }
            ]
        }
        return self._make_request('post', 'NeFj1qYw3', data, 'main', nocheck)

    @doc(kveY9vSZiCveNHGRKZ5u)
    @BaseApi.timing_decorator
    def kveY9vSZiCveNHGRKZ5u(self, nocheck=False):
        res = self.pc.JU8QYbNi3BDlSn2XaNZKe()
        data = {
            "saleType": "2",
            "remark": "备注",
            "status": 1,
            "logisticsNo": str(self.jd),
            "payState": "2",
            "sellSaleOrderArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "platformArticlesNo": res[0]['platformArticlesNo'],
                    "newSalePrice": int(self.number),
                    "saleSettlePrice": res[0]['saleSettlePrice'],
                    "saleOrderNo": res[0]['salesOrder'],
                    "accountNo": None,
                    "accessoryNoList": [
                        {
                            "brandId": res[0]['brandId'],
                            "brandName": res[0]['brandName'],
                            "modelId": res[0]['modelId'],
                            "modelName": res[0]['modelName'],
                            "accessoryType": 2,
                            "accessoryNo": "PJ0215",
                            "accessoryQuality": 3,
                            "accessoryPrice": int(self.number),
                            "articlesTypeId": 1,
                            "articlesTypeName": res[0]['articlesTypeName'],
                            "channelType": 1,
                            "purchasePrice": int(self.number)
                        }
                    ]
                }
            ]
        }
        return self._make_request('post', 'NeFj1qYw3', data, 'main', nocheck)


class JhWPhXjKbY(InitializeParams):
    """商品销售|销售管理|销售上架"""

    @doc(kiSivAHj3Vab5m78JpuW)
    @BaseApi.timing_decorator
    def kiSivAHj3Vab5m78JpuW(self, nocheck=False):
        time = self.get_current_timestamp_ms()
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='13')
        data = {
            "saleTime": self.get_formatted_datetime(),
            "saleType": 2,
            "clientId": INFO['main_sale_supplier_id'],
            "clientName": INFO['vice_sales_customer_name'],
            "accountNo": INFO['main_account_no'],
            "userId": INFO['main_user_id'],
            "offExpressage": "0",
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res[0]['id'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 13,
                    "salePrice": 100,
                    "platformArticlesNo": res[0]['platformArticlesNo'],
                    "platformOrderNo": None,
                    "remark": res[0]['remark'],
                    "finenessId": 1,
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1,
                        "id": time
                    }
                }
            ]
        }
        return self._make_request('post', 'XmMhypsCX', data, 'main', nocheck)


class G4HwM9EjFQ(InitializeParams):
    """商品销售|销售管理|销售中物品列表"""

    @BaseApi.timing_decorator
    def item_number(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='15')
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'QBZVuqz0S', data, 'main', nocheck)

    @doc(htCvd4xY1c0JleADicMq)
    @BaseApi.timing_decorator
    def htCvd4xY1c0JleADicMq(self, nocheck=False):
        self.item_number()
        res = self.pc.Ez77PXDybIrSTaH32RHsz()
        res_2 = self.pc.Ez77PXDybIrSTaH32RHsz(data='a')
        data = {
            "saleTime": self.get_formatted_datetime(),
            "saleType": "1",
            "clientId": res[0]['saleSupplierId'],
            "accountNo": INFO['main_account_no'],
            "accountName": INFO['main_account_name'],
            "userId": INFO['main_user_id'],
            "deliveryId": INFO['main_user_id'],
            "deliveryTime": self.get_formatted_datetime(),
            "status": 1,
            "logisticsOrder": self.jd,
            "logisticsNoPrice": 0,
            "offExpressage": "0",
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res_2[0]['id'],
                    "imei": res[0]['imei'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 13,
                    "salePrice": res[0]['salePrice'],
                    "platformArticlesNo": res[0]['platformArticlesNo'],
                    "platformOrderNo": None,
                    "remark": "备注",
                    "finenessId": 1,
                    "articlesInfoId": res_2[0]['articlesInfoId'],
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1,
                        "id": res_2[0]['articlesInfoId'],
                    },
                    "saleSettlePrice": res[0]['saleSettlePrice']
                }
            ]
        }
        return self._make_request('post', 'JKSmt0DQk', data, 'main', nocheck)

    @doc(rrBrdjBX494MEDd1GeWh)
    @BaseApi.timing_decorator
    def rrBrdjBX494MEDd1GeWh(self, nocheck=False):
        self.item_number()
        res = self.pc.Ez77PXDybIrSTaH32RHsz()
        res_2 = self.pc.Ez77PXDybIrSTaH32RHsz(data='a')
        data = {
            "saleTime": self.get_formatted_datetime(),
            "saleType": "1",
            "clientId": res[0]['saleSupplierId'],
            "userId": INFO['main_user_id'],
            "deliveryId": INFO['main_user_id'],
            "status": 2,
            "logisticsOrder": 0,
            "logisticsNoPrice": 0,
            "offExpressage": "0",
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res_2[0]['id'],
                    "imei": res[0]['imei'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 13,
                    "salePrice": res[0]['salePrice'],
                    "platformArticlesNo": res[0]['platformArticlesNo'],
                    "platformOrderNo": None,
                    "remark": "备注",
                    "finenessId": 1,
                    "articlesInfoId": res_2[0]['articlesInfoId'],
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1,
                        "id": res_2[0]['articlesInfoId'],
                    },
                    "saleSettlePrice": res[0]['saleSettlePrice']
                }
            ]
        }
        return self._make_request('post', 'JKSmt0DQk', data, 'main', nocheck)

    @doc(zGRElY85yjm7F6rhrCx3)
    @BaseApi.timing_decorator
    def zGRElY85yjm7F6rhrCx3(self, nocheck=False):
        res = self.pc.Ez77PXDybIrSTaH32RHsz(data='b')
        data = {
            "articlesList": [
                {
                    "id": res[0]['id'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 13,
                    "saleRecordId": res[0]['saleRecordId'],
                    "remark": ""
                }
            ]
        }
        return self._make_request('post', 'dyEwhLq1w', data, 'main', nocheck)

    @doc(ooNlz00UWyMoRIn0Nq8E)
    @BaseApi.timing_decorator
    def ooNlz00UWyMoRIn0Nq8E(self, nocheck=False):
        res = self.pc.Ez77PXDybIrSTaH32RHsz(i='1', j='5')
        res_2 = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='3', j='19')
        data = [
            {
                "id": res[0]['id'],
                "articlesId": res_2[0]['id'],
                "supplierId": INFO['main_sale_supplier_id'],
                "accountNo": INFO['main_account_no'],
                "accountName": INFO['main_account_name'],
                "articlesNo": res[0]['articlesNo'],
                "status": "1",
                "articlesState": 19,
                "saleSettlePrice": 11,
                "salePrice": 100,
                "platformOrderNo": "",
                "saleType": 5
            }
        ]
        return self._make_request('put', 'bRNJDSKP5', data, 'main', nocheck)

    @doc(bLvgAVe5W8UHtELDxMfB)
    @BaseApi.timing_decorator
    def bLvgAVe5W8UHtELDxMfB(self, nocheck=False):
        res = self.pc.Ez77PXDybIrSTaH32RHsz(i='1', j='5')
        res_2 = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='3', j='19')
        data = {
            "articlesList": [
                {
                    "id": res[0]['id'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 14,
                    "saleRecordId": res_2[0]['id'],
                    "receiveStatus": 1,
                    "remark": "备注"
                }
            ],
            "logisticsPrice": 11,
            "logisticsNo": self.sf,
            "warehouseId": INFO['main_item_warehouse_id']
        }
        return self._make_request('put', 'ARuPJm52s', data, 'main', nocheck)

    @doc(asfN7GBuig1lB2JTFGbz)
    @BaseApi.timing_decorator
    def asfN7GBuig1lB2JTFGbz(self, nocheck=False):
        res = self.pc.Ez77PXDybIrSTaH32RHsz(i='1', j='5')
        res_2 = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='3', j='19')
        data = [
            {
                "id": res[0]['id'],
                "articlesId": res_2[0]['id'],
                "supplierId": INFO['main_sale_supplier_id'],
                "accountNo": INFO['main_account_no'],
                "accountName": INFO['main_account_name'],
                "articlesNo": res[0]['articlesNo'],
                "status": "1",
                "articlesState": 14,
                "saleSettlePrice": 100,
                "salePrice": res[0]['salePrice'],
                "platformOrderNo": None,
                "saleType": 3
            }
        ]
        return self._make_request('put', 'bRNJDSKP5', data, 'main', nocheck)


class K840BKXUBB(InitializeParams):
    """商品销售|销售管理|待销售物品"""

    @BaseApi.timing_decorator
    def item_number(self, nocheck=False):
        res = self.pc.Mb5NtymgNZq58BhIE7Umz()
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'QBZVuqz0S', data, 'main', nocheck)

    @doc(iqOJswY1Y3kNWO1jXmAc)
    @BaseApi.timing_decorator
    def iqOJswY1Y3kNWO1jXmAc(self, nocheck=False):
        res = self.pc.XTk41pUDr28xCf1YL17uR()
        res_2 = self.pc.XTk41pUDr28xCf1YL17uR(data='a')
        data = {
            "clientId": INFO['main_sale_supplier_id'],
            "clientName": INFO['vice_sales_customer_name'],
            "accountNo": INFO['main_account_no'],
            "saleTime": self.get_formatted_datetime(),
            "saleType": 2,
            "userId": INFO['main_user_id'],
            "offExpressage": "0",
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res_2[0]['id'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 13,
                    "salePrice": 100,
                    "platformArticlesNo": res[0]['platformArticlesNo'],
                    "platformOrderNo": None,
                    "remark": None,
                    "finenessId": 1,
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1,
                        "id": res_2[0]['articlesInfoId']
                    }
                }
            ]
        }
        return self._make_request('post', 'XmMhypsCX', data, 'main', nocheck)

    @doc(psGTQePHRPXOVLvXlZU5)
    @BaseApi.timing_decorator
    def psGTQePHRPXOVLvXlZU5(self, nocheck=False):
        res = self.pc.XTk41pUDr28xCf1YL17uR()
        res_2 = self.pc.XTk41pUDr28xCf1YL17uR(data='a')
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
            "logisticsNoPrice": 30,
            "isEexpress": "0",
            "offExpressage": "0",
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res_2[0]['id'],
                    "imei": res[0]['imei'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 13,
                    "salePrice": 30,
                    "platformArticlesNo": res[0]['platformArticlesNo'],
                    "platformOrderNo": self.serial,
                    "remark": None,
                    "finenessId": 1,
                    "articlesInfoId": res_2[0]['articlesInfoId'],
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1,
                        "id": res_2[0]['articlesInfoId']
                    },
                    "saleSettlePrice": 30
                }
            ]
        }
        return self._make_request('post', 'JKSmt0DQk', data, 'main', nocheck)

    @doc(BjtCW4zAlmHFf4hnEsyK)
    @BaseApi.timing_decorator
    def BjtCW4zAlmHFf4hnEsyK(self, nocheck=False):
        self.item_number()
        res = self.pc.XTk41pUDr28xCf1YL17uR()
        res_2 = self.pc.XTk41pUDr28xCf1YL17uR(data='a')
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
            "logisticsNoPrice": 123,
            "isEexpress": "0",
            "offExpressage": "0",
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res_2[0]['id'],
                    "imei": res[0]['imei'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 13,
                    "salePrice": 0,
                    "platformArticlesNo": res[0]['platformArticlesNo'],
                    "platformOrderNo": None,
                    "remark": None,
                    "finenessId": 1,
                    "articlesInfoId": res_2[0]['articlesInfoId'],
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1,
                        "id": res_2[0]['articlesInfoId'],
                    },
                    "saleSettlePrice": ""
                }
            ]
        }
        return self._make_request('post', 'JKSmt0DQk', data, 'main', nocheck)

    @doc(aMAnXMswO97RRUy2WDp5)
    @BaseApi.timing_decorator
    def aMAnXMswO97RRUy2WDp5(self, nocheck=False):
        self.item_number()
        res = self.pc.XTk41pUDr28xCf1YL17uR()
        res_2 = self.pc.XTk41pUDr28xCf1YL17uR(data='a')
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
            "status": 2,
            "logisticsOrder": self.jd,
            "logisticsNoPrice": 30,
            "isEexpress": "0",
            "offExpressage": "0",
            "purchaseOrdersArticlesDTOList": [
                {
                    "id": res_2[0]['id'],
                    "imei": res[0]['imei'],
                    "articlesNo": res[0]['articlesNo'],
                    "articlesState": 13,
                    "salePrice": 30,
                    "platformArticlesNo": res[0]['platformArticlesNo'],
                    "platformOrderNo": self.serial,
                    "remark": None,
                    "finenessId": 1,
                    "articlesInfoId": res_2[0]['articlesInfoId'],
                    "purchaseArticlesInfoDTO": {
                        "finenessId": 1,
                        "id": res_2[0]['articlesInfoId'],
                    },
                    "saleSettlePrice": 30
                }
            ]
        }
        return self._make_request('post', 'JKSmt0DQk', data, 'main', nocheck)


class A87tiuwVRI(InitializeParams):
    """商品销售|销售管理|已销售订单列表"""


class H48MfRLnYT(InitializeParams):
    """商品销售|销售管理|已销售物品列表"""

    @doc(J6LQWn0szGuyNJ0UuFq8)
    @BaseApi.timing_decorator
    def J6LQWn0szGuyNJ0UuFq8(self, nocheck=False):
        res = self.pc.JU8QYbNi3BDlSn2XaNZKe()
        data = {
            "saleType": "5",
            "status": 1,
            "payState": "2",
            "sellSaleOrderArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "platformArticlesNo": res[0]['sellPlatformOrderNo'],
                    "newSalePrice": 60,
                    "saleSettlePrice": res[0]['saleSettlePrice'],
                    "saleOrderNo": res[0]['salesOrder'],
                    "accountNo": None,
                    "accessoryNoList": []
                }
            ]
        }
        return self._make_request('post', 'NeFj1qYw3', data, 'main', nocheck)

    @doc(mZBEQDHNTjeSAXBWx11z)
    @BaseApi.timing_decorator
    def mZBEQDHNTjeSAXBWx11z(self, nocheck=False):
        res = self.pc.JU8QYbNi3BDlSn2XaNZKe()
        data = {
            "saleType": "1",
            "remark": "test",
            "status": 2,
            "payState": "2",
            "returnType": 1,
            "warehouseId": INFO['main_item_in_warehouse_id'],
            "sellSaleOrderArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "platformArticlesNo": res[0]['sellPlatformOrderNo'],
                    "newSalePrice": 0,
                    "saleSettlePrice": res[0]['saleSettlePrice'],
                    "saleOrderNo": res[0]['salesOrder'],
                    "accountNo": None,
                    "accessoryNoList": []
                }
            ]
        }
        return self._make_request('post', 'NeFj1qYw3', data, 'main', nocheck)

    @doc(JjVcGp9jSl8TI9nj2xVw)
    @BaseApi.timing_decorator
    def JjVcGp9jSl8TI9nj2xVw(self, nocheck=False):
        res = self.pc.JU8QYbNi3BDlSn2XaNZKe()
        data = {
            "saleType": "2",
            "status": 1,
            "logisticsNo": self.jd,
            "payState": "2",
            "returnType": 1,
            "sellSaleOrderArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "platformArticlesNo": res[0]['sellPlatformOrderNo'],
                    "newSalePrice": 100,
                    "saleSettlePrice": res[0]['saleSettlePrice'],
                    "saleOrderNo": res[0]['salesOrder'],
                    "accountNo": None,
                    "accessoryNoList": [
                        {
                            "brandId": 905,
                            "brandName": "柔宇",
                            "modelId": 13578,
                            "modelName": "FlexPai",
                            "accessoryType": 2,
                            "accessoryNo": "PJ0001",
                            "accessoryQuality": 3,
                            "accessoryPrice": 40,
                            "articlesTypeId": 1,
                            "articlesTypeName": "手机",
                            "channelType": 2,
                            "purchasePrice": 40
                        }
                    ]
                }
            ]
        }
        return self._make_request('post', 'NeFj1qYw3', data, 'main', nocheck)

    @doc(XfB5KTH8vn0wDw6a9KJQ)
    @BaseApi.timing_decorator
    def XfB5KTH8vn0wDw6a9KJQ(self, nocheck=False):
        res = self.pc.JU8QYbNi3BDlSn2XaNZKe()
        data = {
            "saleType": "2",
            "remark": "123",
            "status": 2,
            "payState": "2",
            "returnType": 1,
            "warehouseId": INFO['main_in_warehouse_id'],
            "sellSaleOrderArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "platformArticlesNo": res[0]['sellPlatformOrderNo'],
                    "newSalePrice": 100,
                    "saleSettlePrice": res[0]['saleSettlePrice'],
                    "saleOrderNo": res[0]['salesOrder'],
                    "accountNo": None,
                    "accessoryNoList": [
                        {
                            "brandId": 905,
                            "brandName": "柔宇",
                            "modelId": 13578,
                            "modelName": "FlexPai",
                            "accessoryType": 2,
                            "accessoryNo": "PJ0001",
                            "accessoryQuality": 3,
                            "accessoryPrice": 40,
                            "articlesTypeId": 1,
                            "articlesTypeName": "手机",
                            "channelType": 2,
                            "purchasePrice": 40
                        }
                    ]
                }
            ]
        }
        return self._make_request('post', 'NeFj1qYw3', data, 'main', nocheck)

    @doc(gVnbM599DimecmAZ6Xlg)
    @BaseApi.timing_decorator
    def gVnbM599DimecmAZ6Xlg(self, nocheck=False):
        res = self.pc.JU8QYbNi3BDlSn2XaNZKe()
        data = {
            "saleType": "8",
            "remark": "test",
            "sellSaleOrderArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "platformArticlesNo": res[0]['sellPlatformOrderNo'],
                    "newSalePrice": 50,
                    "saleSettlePrice": res[0]['saleSettlePrice'],
                    "saleOrderNo": res[0]['salesOrder'],
                    "accountNo": None,
                    "accessoryNoList": []
                }
            ]
        }
        return self._make_request('post', 'NeFj1qYw3', data, 'main', nocheck)



class UkltE3HM8G(InitializeParams):
    """商品销售|客户管理"""


class LwtGu0p14m(InitializeParams):
    """商品销售|数据统计"""


class AHdZ4hW3TP(InitializeParams):
    """商品销售|销售售后管理|销售售后列表"""

    @BaseApi.timing_decorator
    def item_number(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='15')
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'QBZVuqz0S', data, 'main', nocheck)

    @doc(GDdc1h1eADXbjk8ujR60)
    @BaseApi.timing_decorator
    def GDdc1h1eADXbjk8ujR60(self, nocheck=False):
        res = self.pc.Kw5nIo3WQBrH2BPScRj1B(data='a')
        data = {
            "saleType": 2,
            "orderNo": res[0]['orderNo'],
            "saleUserId": INFO['main_sale_supplier_id'],
            "saleUserName": INFO['vice_sales_customer_name'],
            "sellSaleOrderArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo']
                }
            ],
            "ids": [
                res[0]['id']
            ],
            "articlesNoOrImei": res[0]['articlesNo'],
            "logisticsNo": res[0]['logisticsNo'],
            "warehouseId": INFO['main_in_warehouse_id']
        }
        return self._make_request('post', 'NvlOrpxv0', data, 'main', nocheck)

    @doc(xSQE9e6LbvvilOg9OMsy)
    @BaseApi.timing_decorator
    def xSQE9e6LbvvilOg9OMsy(self, nocheck=False):
        res = self.pc.Kw5nIo3WQBrH2BPScRj1B(data='a')
        data = {
            "fineSalePrice": 100,
            "saleType": 4,
            "remark": "备注",
            "orderNo": res[0]['orderNo'],
            "saleUserId": INFO['main_sale_supplier_id'],
            "saleUserName": INFO['vice_sales_customer_name'],
            "sellSaleOrderArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo']
                }
            ],
            "ids": [
                res[0]['id']
            ],
            "articlesNoOrImei": res[0]['articlesNo']
        }
        return self._make_request('post', 'NvlOrpxv0', data, 'main', nocheck)

    @doc(ebhsQ41HitCvjEsvMz0G)
    @BaseApi.timing_decorator
    def ebhsQ41HitCvjEsvMz0G(self, nocheck=False):
        res = self.pc.Kw5nIo3WQBrH2BPScRj1B(data='a')
        res_2 = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='3')
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "saleUserId": INFO['main_sale_supplier_id'],
            "offExpressage": "0",
            "saleType": "7",
            "purchaseOrdersArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "remark": None,
                    "saleSettlePrice": 21
                }
            ],
            "newPurchaseOrdersArticlesDTO": {
                "articlesNo": res_2[0]['articlesNo'],
                "imei": res_2[0]['imei'],
                "newSalePrice": 60,
                "platformArticlesNo": self.serial,
                "platformOrderNo": self.serial,
                "remark": "",
                "costPrice": 130
            },
            "isSaleType": True
        }
        return self._make_request('post', 'zuYSO5V1e', data, 'main', nocheck)

    @doc(GdXpXPawmTeBaOha9VUo)
    @BaseApi.timing_decorator
    def GdXpXPawmTeBaOha9VUo(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='15')
        data = {
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "saleUserId": INFO['main_sale_supplier_id'],
            "offExpressage": "0",
            "logisticsNo": self.jd,
            "logisticsPrice": "11",
            "saleType": "6",
            "purchaseOrdersArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "remark": None,
                    "saleSettlePrice": 24
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


    @doc(pt4gIHCRgdVZv3FGKFVq)
    @BaseApi.timing_decorator
    def pt4gIHCRgdVZv3FGKFVq(self, nocheck=False):
        res = self.pc.Kw5nIo3WQBrH2BPScRj1B(data='a')
        data = {
            "articlesNoList": [
                res[0]['articlesNo'],
            ],
            "saleUserId": INFO['main_sale_supplier_id'],
            "offExpressage": "0",
            "logisticsNo": self.jd,
            "logisticsPrice": "321",
            "saleType": "3",
            "purchaseOrdersArticlesDTOList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "remark": None,
                    "saleSettlePrice": 34
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


class BLHu01CRzs(InitializeParams):
    """商品销售|销售管理|待接收物品"""

    @doc(TjFLeMzswpHGeziySvFD)
    @BaseApi.timing_decorator
    def TjFLeMzswpHGeziySvFD(self):
        res = self.pc.Mb5NtymgNZq58BhIE7Umz()
        obj = res[0]['imei']
        ParamCache.cache_object({"imei": obj}, 'practical.json')
        data = {"pageNum": 1, "pageSize": 10, "articlesState": 13, "articlesType": "1", "articlesNo": obj}
        return self._make_request('post', 'RbZZfqC2S', data, 'main')

    @doc(gRGlwNpXR7APhkJ0lUaA)
    @BaseApi.timing_decorator
    def gRGlwNpXR7APhkJ0lUaA(self):
        data = {
            "pageNum": 1,
            "pageSize": 10,
            "articlesState": 13,
            "articlesType": "1",
            "erpStartTime": self.get_the_date(-1),
            "erpEndTime": self.get_the_date()
        }
        return self._make_request('post', 'RbZZfqC2S', data, 'main')


class WS1s1EqRY2(InitializeParams):
    """商品销售|销售管理|销售中订单列表"""


if __name__ == '__main__':
    api = None
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
