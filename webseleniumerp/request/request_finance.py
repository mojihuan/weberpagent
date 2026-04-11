# coding: utf-8
import json
import time
from common.base_api import BaseApi
from common.base_params import InitializeParams
from common.import_desc import *
from config.user_info import INFO


class WnS8MVqkMl(InitializeParams):
    """财务管理|资金账户|账户列表"""

    @doc(EPKsvmKzhm7PJO1muKwj)
    @BaseApi.timing_decorator
    def EPKsvmKzhm7PJO1muKwj(self, nocheck=False):
        data = {
            "accountName": "账户名称" + self.imei,
            "accountType": 6,
            "accountBalance": 9999,
            "remark": "备注"
        }
        return self._make_request('post', 'HAUaZuczI', data, 'idle', nocheck)

    @doc(JWqdZElvJgNFFHaXqZRT)
    @BaseApi.timing_decorator
    def JWqdZElvJgNFFHaXqZRT(self, nocheck=False):
        res = self.pc.NQXuyZ5kySQBpsQJxR3vC()
        data = {
            "id": res[0]['id'],
            "accountName": res[0]['accountName'],
            "accountType": res[0]['accountType'],
            "rechargePrice": 5,
            "remark": "备注"
        }
        return self._make_request('put', 'Z6Mw8XcVM', data, 'idle', nocheck)

    @doc(uFTVSOsNXHqB5vxndsyu)
    @BaseApi.timing_decorator
    def uFTVSOsNXHqB5vxndsyu(self, nocheck=False):
        data = {
            "time": self.get_formatted_datetime(),
            "accountBalance": 5,
            "id": INFO['idle_account_no'],
            "rollId": INFO['idle_out_account_no']
        }
        return self._make_request('post', 'byK5puX6U', data, 'idle', nocheck)


class DISZcB8ZYA(InitializeParams):
    """财务管理|业务记账|账单审核"""

    @doc(B7RHH1KuhjdPrvwiHaID)
    @BaseApi.timing_decorator
    def B7RHH1KuhjdPrvwiHaID(self, nocheck=False):
        for _ in range(5):
            time.sleep(2)
            self.pc.VFy40VMBZGf8pQEkVFRor(i=1, j=0)
        res = self.pc.VFy40VMBZGf8pQEkVFRor(i=1, j=0)
        data = {
            "billNoList": [
                res[0]['billNo']
            ],
            "auditStatus": 1,
            "accountNo": INFO['main_account_no'],
            "ids": [
                res[0]['id']
            ],
            "oldAccountNoList": [
                INFO['main_account_no']
            ]
        }
        return self._make_request('put', 'NYfWyJWvz', data, 'main', nocheck)

    @doc(owv9tEsxrz0pHaC8wXtH)
    @BaseApi.timing_decorator
    def owv9tEsxrz0pHaC8wXtH(self, nocheck=False):
        res = self.pc.VFy40VMBZGf8pQEkVFRor(i=1, j=0)
        data = {
            "billNoList": [
                res[0]['billNo']
            ],
            "auditStatus": 2,
            "remark": "原因",
            "ids": [
                res[0]['id']
            ],
            "oldAccountNoList": [
                INFO['main_account_no']
            ]
        }
        return self._make_request('put', 'NYfWyJWvz', data, 'main', nocheck)

    @doc(u9n7DKzDxeT1rnv4h3tV)
    @BaseApi.timing_decorator
    def u9n7DKzDxeT1rnv4h3tV(self, nocheck=False):
        for _ in range(5):
            time.sleep(2)
            self.pc.VFy40VMBZGf8pQEkVFRor(i=2, j=0)
        res = self.pc.VFy40VMBZGf8pQEkVFRor(i=2, j=0)
        data = {
            "billNoList": [
                res[0]['billNo']
            ],
            "auditStatus": 1,
            "accountNo": INFO['main_account_no'],
            "ids": [
                res[0]['id']
            ],
            "oldAccountNoList": [
                INFO['main_account_no']
            ]
        }
        return self._make_request('put', 'NYfWyJWvz', data, 'main', nocheck)

    @doc(LDw1ORDeq57nUxfwqx8P)
    @BaseApi.timing_decorator
    def LDw1ORDeq57nUxfwqx8P(self, nocheck=False):
        res = self.pc.VFy40VMBZGf8pQEkVFRor(i=2, j=0)
        data = {
            "billNoList": [
                res[0]['billNo']
            ],
            "auditStatus": 2,
            "remark": "test",
            "ids": [
                res[0]['id']
            ],
            "oldAccountNoList": [
                INFO['main_account_no'],
            ]
        }
        return self._make_request('put', 'NYfWyJWvz', data, 'main', nocheck)

    @doc(BwTCKfib2nxArwfojqzu)
    @BaseApi.timing_decorator
    def BwTCKfib2nxArwfojqzu(self, nocheck=False):
        res = self.pc.VFy40VMBZGf8pQEkVFRor(data='a', i=2, j=0)
        data = {
            "billNoList": [
                res[0]['billNo']
            ],
            "auditStatus": 1,
            "accountNo": INFO['vice_account_no'],
            "ids": [
                res[0]['id']
            ],
            "oldAccountNoList": [
                INFO['vice_account_no']
            ]
        }
        return self._make_request('put', 'NYfWyJWvz', data, 'vice', nocheck)


class AgnH0XzSB2(InitializeParams):
    """财务管理|业务记账|往来应付"""

    @doc(EREYtlx2HerCU1zbpObk)
    @BaseApi.timing_decorator
    def EREYtlx2HerCU1zbpObk(self, nocheck=False):
        res = self.pc.MOyeqlzcgLqhqdWBrkyYg()
        data = {
            "accountNo": INFO['main_account_no'],
            "supplierId": INFO['main_supplier_id'],
            "userType": "2",
            "payType": "2",
            "remark": "备注",
            "accountName": INFO['main_account_name'],
            "supplierName": INFO['main_supplier_name'],
            "orderBills": [
                {
                    "billNo": res[0]['billNo'],
                    "settlementAmount": res[0]['payableAmount']
                }
            ]
        }
        return self._make_request('post', 'WMRxDiO0Y', data, 'main', nocheck)

    @doc(rN6o1ZUYdtDbm4jrcy5R)
    @BaseApi.timing_decorator
    def rN6o1ZUYdtDbm4jrcy5R(self, nocheck=False):
        data = {
            "supplierId": INFO['main_supplier_id'],
            "isReconciliationDetailPage": True,
            "userType": "2",
            "payType": "2",
            "payTime": self.get_formatted_datetime(),
            "accountNo": INFO['main_account_no'],
            "amount": 5,
            "supplierName": INFO['main_supplier_name'],
            "accountName": INFO['main_account_name']
        }
        return self._make_request('post', 'l22kgVIOn', data, 'main', nocheck)

    @doc(Hxs7NXz0FKtXSPkjcof8)
    @BaseApi.timing_decorator
    def Hxs7NXz0FKtXSPkjcof8(self, nocheck=False):
        res = self.pc.MOyeqlzcgLqhqdWBrkyYg(data='b')
        data = {
            "accountNo": INFO['main_account_no'],
            "supplierId": INFO['main_supplier_id'],
            "userType": "2",
            "payType": "2",
            "supplierName": INFO['main_supplier_name'],
            "accountName": INFO['main_account_name'],
            "articlesBills": [
                {
                    "billNo": None,
                    "type": None,
                    "articlesNo": res[0]['articlesNo'],
                    "paidAmount": 1,
                    "payableAmount": res[0]['amount']
                }
            ]
        }
        return self._make_request('post', 'WMRxDiO0Y', data, 'main', nocheck)

    @doc(D97tgtc9GTXE0vdXK6lA)
    @BaseApi.timing_decorator
    def D97tgtc9GTXE0vdXK6lA(self, nocheck=False):
        res = self.pc.MOyeqlzcgLqhqdWBrkyYg(data='d')
        data = {
            "supplierId": INFO['main_supplier_id'],
            "isReconciliationDetailPage": True,
            "userType": "2",
            "payType": "2",
            "amount": res[0]['amount'],
            "payTime": self.get_formatted_datetime(),
            "accountNo": INFO['main_account_no'],
            "supplierName": INFO['main_supplier_name'],
            "accountName": INFO['main_account_name']
        }
        return self._make_request('post', 'l22kgVIOn', data, 'main', nocheck)

    @doc(hciCQ89oHrPs7V8gpK2s)
    @BaseApi.timing_decorator
    def hciCQ89oHrPs7V8gpK2s(self, nocheck=False):
        res = self.pc.MOyeqlzcgLqhqdWBrkyYg(data='d')
        data = {
            "supplierId": INFO['main_supplier_id'],
            "isReconciliationDetailPage": True,
            "userType": "2",
            "payType": "2",
            "amount": res[0]['amount'],
            "payTime": self.get_formatted_datetime(),
            "accountNo": INFO['main_account_no'],
            "supplierName": INFO['main_supplier_name'],
            "accountName": INFO['main_account_name'],
            "deductionList": [
                {
                    "preId": res[0]["id"],
                    "deductionAmount": res[0]['userAmount']
                }
            ]
        }
        return self._make_request('post', 'l22kgVIOn', data, 'main', nocheck)

    @doc(euOyfYcWF0WoC0gVogWr)
    @BaseApi.timing_decorator
    def euOyfYcWF0WoC0gVogWr(self, nocheck=False):
        res = self.pc.MOyeqlzcgLqhqdWBrkyYg(data='d')
        data = {
            "supplierId": INFO['main_supplier_id'],
            "isReconciliationDetailPage": True,
            "userType": "2",
            "payType": "2",
            "amount": res[0]['amount'] / 2,
            "payTime": self.get_formatted_datetime(),
            "accountNo": INFO['main_account_no'],
            "supplierName": INFO['main_supplier_name'],
            "accountName": INFO['main_account_name'],
            "deductionList": [
                {
                    "preId": res[0]["id"],
                    "deductionAmount": res[0]['userAmount'] / 2
                }
            ]
        }
        return self._make_request('post', 'l22kgVIOn', data, 'main', nocheck)

    @doc(gSSx2ogkswH5sLVoUa56)
    @BaseApi.timing_decorator
    def gSSx2ogkswH5sLVoUa56(self, nocheck=False):
        res = self.pc.MOyeqlzcgLqhqdWBrkyYg()
        data = {
            "accountNo": INFO['main_account_no'],
            "supplierId": INFO['main_supplier_id'],
            "userType": "2",
            "payType": "2",
            "accountName": INFO['main_account_name'],
            "supplierName": INFO['main_supplier_name'],
            "orderBills": [
                {
                    "billNo": res[0]['billNo'],
                    "settlementAmount": res[0]['payableAmount'] / 2
                }
            ]
        }
        return self._make_request('post', 'WMRxDiO0Y', data, 'main', nocheck)

    @doc(tNULVYUnORNWpB5La3kh)
    @BaseApi.timing_decorator
    def tNULVYUnORNWpB5La3kh(self, nocheck=False):
        res = self.pc.MOyeqlzcgLqhqdWBrkyYg()
        res_2 = self.pc.MOyeqlzcgLqhqdWBrkyYg(data='d')
        data = {
            "accountNo": INFO['main_account_no'],
            "accountName": INFO['main_account_name'],
            "supplierId": INFO['main_supplier_id'],
            "userType": "2",
            "payType": "2",
            "supplierName": INFO['main_supplier_name'],
            "orderBills": [
                {
                    "billNo": res[0]['billNo'],
                    "settlementAmount": res[0]['payableAmount']
                }
            ],
            "deductionList": [
                {
                    "preId": res_2[0]["id"],
                    "deductionAmount": res_2[0]['userAmount'] / 2
                }
            ]
        }
        return self._make_request('post', 'WMRxDiO0Y', data, 'main', nocheck)

    @doc(VdFBXs16N2ZEhp4PqlbM)
    @BaseApi.timing_decorator
    def VdFBXs16N2ZEhp4PqlbM(self, nocheck=False):
        res = self.pc.MOyeqlzcgLqhqdWBrkyYg()
        res_2 = self.pc.MOyeqlzcgLqhqdWBrkyYg(data='d')
        data = {
            "accountNo": INFO['main_account_no'],
            "accountName": INFO['main_account_name'],
            "supplierId": INFO['main_supplier_id'],
            "userType": "2",
            "payType": "2",
            "supplierName": INFO['main_supplier_name'],
            "orderBills": [
                {
                    "billNo": res[0]['billNo'],
                    "settlementAmount": res[0]['payableAmount']
                }
            ],
            "deductionList": [
                {
                    "preId": res_2[0]["id"],
                    "deductionAmount": res_2[0]['userAmount']
                }
            ]
        }
        return self._make_request('post', 'WMRxDiO0Y', data, 'main', nocheck)

    @doc(N5qtlbV2nKad4orzWHDh)
    @BaseApi.timing_decorator
    def N5qtlbV2nKad4orzWHDh(self, nocheck=False):
        res = self.pc.MOyeqlzcgLqhqdWBrkyYg(data="b")
        data = {
            "accountNo": INFO['main_account_no'],
            "accountName": INFO['main_account_name'],
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "userType": "2",
            "payType": "2",
            "articlesBills": [
                {
                    "billNo": None,
                    "type": None,
                    "articlesNo": res[0]['articlesNo'],
                    "paidAmount": res[0]['unpaidAmount'],
                    "payableAmount": res[0]['amount']
                }
            ]
        }
        return self._make_request('post', 'WMRxDiO0Y', data, 'main', nocheck)

    @doc(SM3tdEQRoyKAUKE6Kjhu)
    @BaseApi.timing_decorator
    def SM3tdEQRoyKAUKE6Kjhu(self, nocheck=False):
        res = self.pc.MOyeqlzcgLqhqdWBrkyYg(data="b")
        res_2 = self.pc.MOyeqlzcgLqhqdWBrkyYg(data='d')
        data = {
            "accountNo": INFO['main_account_no'],
            "accountName": INFO['main_account_name'],
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "userType": "2",
            "payType": "2",
            "articlesBills": [
                {
                    "billNo": None,
                    "type": None,
                    "articlesNo": res[0]['articlesNo'],
                    "paidAmount": res[0]['unpaidAmount'],
                    "payableAmount": res[0]['amount']
                }
            ],
            "deductionList": [
                {
                    "preId": res_2[0]['id'],
                    "deductionAmount": res_2[0]['userAmount'] / 2
                }
            ]
        }
        return self._make_request('post', 'WMRxDiO0Y', data, 'main', nocheck)

    @doc(t9oHAeUXlbi3VyJNnJD4)
    @BaseApi.timing_decorator
    def t9oHAeUXlbi3VyJNnJD4(self, nocheck=False):
        res = self.pc.MOyeqlzcgLqhqdWBrkyYg(data="b")
        res_2 = self.pc.MOyeqlzcgLqhqdWBrkyYg(data='d')
        data = {
            "accountNo": INFO['main_account_no'],
            "accountName": INFO['main_account_name'],
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "userType": "2",
            "payType": "2",
            "articlesBills": [
                {
                    "billNo": None,
                    "type": None,
                    "articlesNo": res[0]['articlesNo'],
                    "paidAmount": res[0]['unpaidAmount'],
                    "payableAmount": res[0]['amount']
                }
            ],
            "deductionList": [
                {
                    "preId": res_2[0]["id"],
                    "deductionAmount": res_2[0]['userAmount']
                }
            ]
        }
        return self._make_request('post', 'WMRxDiO0Y', data, 'main', nocheck)


class QR58hbFLmz(InitializeParams):
    """财务管理|成本收入调整"""

    @doc(UuPR3hG2S8ND6eRZD6CU)
    @BaseApi.timing_decorator
    def UuPR3hG2S8ND6eRZD6CU(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2)
        data = {
            "adjustmentType": "1",
            "accountNo": INFO['main_account_no'],
            "adjustmentReason": 1,
            "articles": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "modelId": res[0]['modelId'],
                    "modelName": res[0]['modelName'],
                    "merchantId": INFO['main_supplier_id'],
                    "beforePrice": res[0]['purchasePrice'],
                    "afterPrice": 5,
                    "adjustmentPrice": 5,
                    "remark": "备注"
                }
            ]
        }
        return self._make_request('post', 'VoKxnNFFb', data, 'main', nocheck)

    @doc(L2MWh5RuYAnG54UuqEDd)
    @BaseApi.timing_decorator
    def L2MWh5RuYAnG54UuqEDd(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp()
        data = {
            "adjustmentType": "1",
            "adjustmentRemark": 750,
            "accountNo": INFO['main_account_no'],
            "adjustmentReason": 2,
            "articles": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "modelId": res[0]['modelId'],
                    "modelName": res[0]['modelName'],
                    "merchantId": INFO['main_supplier_id'],
                    "beforePrice": res[0]['purchasePrice'],
                    "afterPrice": 22,
                    "adjustmentPrice": 22,
                    "remark": "备注"
                }
            ]
        }
        return self._make_request('post', 'VoKxnNFFb', data, 'main', nocheck)

    @doc(ZOu34dViPFdE8YXvix3K)
    @BaseApi.timing_decorator
    def ZOu34dViPFdE8YXvix3K(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='3', j='9')
        res_2 = self.pc.JU8QYbNi3BDlSn2XaNZKe()
        data = {
            "adjustmentType": "2",
            "accountNo": INFO['main_account_no'],
            "adjustmentReason": 1,
            "articles": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "modelId": res[0]['modelId'],
                    "modelName": res[0]['modelName'],
                    "merchantId": INFO['main_supplier_id'],
                    "beforePrice": res_2[0]['salePrice'],
                    "afterPrice": 50,
                    "adjustmentPrice": 50,
                    "remark": "备注"
                }
            ]
        }
        return self._make_request('post', 'VoKxnNFFb', data, 'main', nocheck)

    @doc(JsHXjaPThXs1bk0gJW6L)
    @BaseApi.timing_decorator
    def JsHXjaPThXs1bk0gJW6L(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='3', j='9')
        res_2 = self.pc.JU8QYbNi3BDlSn2XaNZKe()
        data = {
            "adjustmentType": "2",
            "adjustmentRemark": 749,
            "accountNo": INFO['main_account_no'],
            "adjustmentReason": 2,
            "articles": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "modelId": res[0]['modelId'],
                    "modelName": res[0]['modelName'],
                    "merchantId": INFO['main_supplier_id'],
                    "beforePrice": res_2[0]['salePrice'],
                    "afterPrice": 50,
                    "adjustmentPrice": 50,
                    "remark": "test"
                }
            ]
        }
        return self._make_request('post', 'VoKxnNFFb', data, 'main', nocheck)

    @doc(I7JXB9egcS81B9M2KvPn)
    @BaseApi.timing_decorator
    def I7JXB9egcS81B9M2KvPn(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='3', j='9')
        res_2 = self.pc.JU8QYbNi3BDlSn2XaNZKe()
        data = {
            "adjustmentType": "2",
            "adjustmentRemark": 749,
            "accountNo": INFO['main_account_no'],
            "adjustmentReason": 2,
            "articles": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "modelId": res[0]['modelId'],
                    "modelName": res[0]['modelName'],
                    "merchantId": INFO['main_supplier_id'],
                    "beforePrice": res_2[0]['salePrice'],
                    "afterPrice": 22,
                    "adjustmentPrice": 22,
                    "remark": "test"
                },
                {
                    "articlesNo": res[1]['articlesNo'],
                    "imei": res[1]['imei'],
                    "modelId": res[1]['modelId'],
                    "modelName": res[1]['modelName'],
                    "merchantId": INFO['main_supplier_id'],
                    "beforePrice": res_2[1]['salePrice'],
                    "afterPrice": 11,
                    "adjustmentPrice": 11,
                    "remark": "test"
                }
            ]
        }
        return self._make_request('post', 'VoKxnNFFb', data, 'main', nocheck)


class HZwCxB8wAq(InitializeParams):
    """财务管理|业务记账|日常支出"""

    @doc(FayuY8TiAhpMWGjKj1UK)
    @BaseApi.timing_decorator
    def FayuY8TiAhpMWGjKj1UK(self, nocheck=False):
        data = {
            "type": 746,
            "amount": 100,
            "accountNo": INFO['main_account_no'],
            "time": self.get_formatted_datetime(),
            "userId": INFO['main_user_id'],
            "payType": "2",
            "accountName": INFO['main_account_name'],
            "userName": f"admin({INFO['main_account']})"
        }
        return self._make_request('post', 'goE4u9JEj', data, 'main', nocheck)

    @doc(voyc86f85IklIULStMSB)
    @BaseApi.timing_decorator
    def voyc86f85IklIULStMSB(self, nocheck=False):
        data = {
            "type": 746,
            "amount": -230,
            "accountNo": INFO['main_account_no'],
            "time": self.get_formatted_datetime(),
            "userId": INFO['main_user_id'],
            "payType": "2",
            "accountName": INFO['main_account_name'],
            "userName": f"admin({INFO['main_account']})"
        }
        return self._make_request('post', 'goE4u9JEj', data, 'main', nocheck)


class WK90Io3VHs(InitializeParams):
    """财务管理|业务记账|日常收入"""

    @doc(HGwxHVDLmqfBnulaegiO)
    @BaseApi.timing_decorator
    def HGwxHVDLmqfBnulaegiO(self, nocheck=False):
        data = {
            "type": 748,
            "amount": 1,
            "accountNo": INFO['main_account_no'],
            "time": self.get_formatted_datetime(),
            "userId": INFO['main_user_id'],
            "remark": "备注",
            "payType": "1",
            "accountName": INFO['main_account_name'],
            "userName": f"admin({INFO['main_account']})"
        }
        return self._make_request('post', 'JIKJUk54b', data, 'main', nocheck)

    @doc(ZB0P0AxSNEJ3bgjge7xl)
    @BaseApi.timing_decorator
    def ZB0P0AxSNEJ3bgjge7xl(self, nocheck=False):
        data = {
            "type": 748,
            "amount": -100,
            "accountNo": INFO['main_account_no'],
            "time": self.get_formatted_datetime(),
            "userId": INFO['main_user_id'],
            "remark": "备注",
            "payType": "1",
            "accountName": INFO['main_account_name'],
            "userName": f"admin({INFO['main_account']})"
        }
        return self._make_request('post', 'JIKJUk54b', data, 'main', nocheck)


class ERK6sz547k(InitializeParams):
    """财务管理|业务记账|往来应收"""

    @doc(fuzCuDjXSjYFn8gzpiBS)
    @BaseApi.timing_decorator
    def fuzCuDjXSjYFn8gzpiBS(self, nocheck=False):
        res = self.pc.A9mwkPeNc1x7YnLCF9jUk(data='b')
        data = {
            "accountNo": INFO['main_account_no'],
            "supplierId": INFO['main_sale_supplier_id'],
            "userType": "1",
            "payType": "1",
            "remark": "备注",
            "accountName": INFO['main_account_name'],
            "supplierName": INFO['vice_sales_customer_name'],
            "articlesBills": [
                {
                    "billNo": None,
                    "type": None,
                    "articlesNo": res[0]['articlesNo'],
                    "paidAmount": 5,
                    "payableAmount": res[0]['amount']
                }
            ]
        }
        return self._make_request('post', 'F9rKxzrEm', data, 'main', nocheck)

    @doc(REpw06TJaUceWaw86bTt)
    @BaseApi.timing_decorator
    def REpw06TJaUceWaw86bTt(self, nocheck=False):
        res = self.pc.A9mwkPeNc1x7YnLCF9jUk(data='b')
        data = {
            "accountNo": INFO['main_account_no'],
            "supplierId": INFO['main_sale_supplier_id'],
            "userType": "1",
            "payType": "1",
            "remark": "备注",
            "accountName": INFO['main_account_name'],
            "supplierName": INFO['vice_sales_customer_name'],
            "articlesBills": [
                {
                    "billNo": None,
                    "type": None,
                    "articlesNo": res[0]['articlesNo'],
                    "paidAmount": res[0]['unpaidAmount'],
                    "payableAmount": res[0]['amount']
                }
            ]
        }
        return self._make_request('post', 'F9rKxzrEm', data, 'main', nocheck)

    @doc(NnVNr1PtqWEZZG0qwyj0)
    @BaseApi.timing_decorator
    def NnVNr1PtqWEZZG0qwyj0(self, nocheck=False):
        res = self.pc.A9mwkPeNc1x7YnLCF9jUk(data='b')
        res_2 = self.pc.A9mwkPeNc1x7YnLCF9jUk(data='d')
        data = {
            "accountNo": INFO['main_account_no'],
            "supplierId": INFO['main_sale_supplier_id'],
            "userType": "1",
            "payType": "1",
            "accountName": INFO['main_account_name'],
            "supplierName": INFO['vice_sales_customer_name'],
            "articlesBills": [
                {
                    "billNo": None,
                    "type": None,
                    "articlesNo": res[0]['articlesNo'],
                    "paidAmount": res[0]['unpaidAmount'],
                    "payableAmount": res[0]['amount']
                }
            ],
            "deductionList": [
                {
                    "preId": res_2[0]['id'],
                    "deductionAmount": res_2[0]['userAmount'] / 2
                }
            ]
        }
        return self._make_request('post', 'F9rKxzrEm', data, 'main', nocheck)

    @doc(ZJ7XVXb9AG0TE9iIa6N4)
    @BaseApi.timing_decorator
    def ZJ7XVXb9AG0TE9iIa6N4(self, nocheck=False):
        data = {
            "supplierId": INFO['main_sale_supplier_id'],
            "isReconciliationDetailPage": True,
            "userType": "1",
            "payType": "1",
            "amount": 5,
            "payTime": self.get_formatted_datetime(),
            "remark": "备注",
            "accountNo": INFO['main_account_no'],
            "supplierName": INFO['vice_sales_customer_name'],
            "accountName": INFO['main_account_name']
        }
        return self._make_request('post', 'r3lH50xQO', data, 'main', nocheck)

    @doc(DNIPeuwYliXnuo8Lkc5X)
    @BaseApi.timing_decorator
    def DNIPeuwYliXnuo8Lkc5X(self, nocheck=False):
        res = self.pc.A9mwkPeNc1x7YnLCF9jUk(data='d')
        data = {
            "supplierId": INFO['main_sale_supplier_id'],
            "isReconciliationDetailPage": True,
            "userType": "1",
            "payType": "1",
            "amount": res[0]['amount'],
            "payTime": self.get_formatted_datetime(),
            "accountNo": INFO['main_account_no'],
            "supplierName": INFO['vice_sales_customer_name'],
            "accountName": INFO['main_account_name']
        }
        return self._make_request('post', 'r3lH50xQO', data, 'main', nocheck)

    @doc(akzhzMMfUHIInmvykkV5)
    @BaseApi.timing_decorator
    def akzhzMMfUHIInmvykkV5(self, nocheck=False):
        res = self.pc.A9mwkPeNc1x7YnLCF9jUk()
        data = {
            "accountNo": INFO['main_account_no'],
            "supplierId": INFO['main_sale_supplier_id'],
            "userType": "1",
            "payType": "1",
            "accountName": INFO['main_account_name'],
            "supplierName": INFO['vice_sales_customer_name'],
            "orderBills": [
                {
                    "billNo": res[0]['billNo'],
                    "settlementAmount": res[0]['payableAmount']
                }
            ]
        }
        return self._make_request('post', 'WMRxDiO0Y', data, 'main', nocheck)

    @doc(Mn5CphHorfpXIIk2meIv)
    @BaseApi.timing_decorator
    def Mn5CphHorfpXIIk2meIv(self, nocheck=False):
        res = self.pc.A9mwkPeNc1x7YnLCF9jUk()
        res_2 = self.pc.A9mwkPeNc1x7YnLCF9jUk(data='d')
        data = {
            "accountNo": INFO['main_account_no'],
            "supplierId": INFO['main_sale_supplier_id'],
            "userType": "1",
            "payType": "1",
            "remark": "备注",
            "accountName": INFO['main_account_name'],
            "supplierName": INFO['vice_sales_customer_name'],
            "orderBills": [
                {
                    "billNo": res[0]['billNo'],
                    "settlementAmount": res[0]['payableAmount']
                }
            ],
            "deductionList": [
                {
                    "preId": res_2[0]['id'],
                    "deductionAmount": res_2[0]['userAmount'] / 2
                }
            ]
        }
        return self._make_request('post', 'WMRxDiO0Y', data, 'main', nocheck)

    @doc(aRnzRjjFEkGwEOrhcsdE)
    @BaseApi.timing_decorator
    def aRnzRjjFEkGwEOrhcsdE(self, nocheck=False):
        res = self.pc.A9mwkPeNc1x7YnLCF9jUk()
        res_2 = self.pc.A9mwkPeNc1x7YnLCF9jUk(data='d')
        data = {
            "accountNo": INFO['main_account_no'],
            "supplierId": INFO['main_sale_supplier_id'],
            "userType": "1",
            "payType": "1",
            "remark": "备注",
            "accountName": INFO['main_account_name'],
            "supplierName": INFO['vice_sales_customer_name'],
            "orderBills": [
                {
                    "billNo": res[0]['billNo'],
                    "settlementAmount": res[0]['payableAmount']
                }
            ],
            "deductionList": [
                {
                    "preId": res_2[0]['id'],
                    "deductionAmount": res_2[0]['userAmount']
                }
            ]
        }
        return self._make_request('post', 'WMRxDiO0Y', data, 'main', nocheck)

    @doc(nsMAwLXUhDECtHFrGK01)
    @BaseApi.timing_decorator
    def nsMAwLXUhDECtHFrGK01(self, nocheck=False):
        res = self.pc.A9mwkPeNc1x7YnLCF9jUk(data='d')
        data = {
            "supplierId": INFO['main_sale_supplier_id'],
            "isReconciliationDetailPage": True,
            "userType": "1",
            "payType": "1",
            "payTime": self.get_formatted_datetime(),
            "accountNo": INFO['main_account_no'],
            "amount": res[0]['amount'] / 2,
            "accountName": INFO['main_account_name'],
            "supplierName": INFO['vice_sales_customer_name'],
            "deductionList": [
                {
                    "preId": res[0]['id'],
                    "deductionAmount": res[0]['userAmount'] / 2
                }
            ]
        }
        return self._make_request('post', 'r3lH50xQO', data, 'main', nocheck)

    @doc(vjiYpRgS61Jil8l1AIb1)
    @BaseApi.timing_decorator
    def vjiYpRgS61Jil8l1AIb1(self, nocheck=False):
        res = self.pc.A9mwkPeNc1x7YnLCF9jUk(data='d')
        data = {
            "supplierId": INFO['main_sale_supplier_id'],
            "isReconciliationDetailPage": True,
            "userType": "1",
            "payType": "1",
            "payTime": self.get_formatted_datetime(),
            "accountNo": INFO['main_account_no'],
            "amount": res[0]['amount'] / 2,
            "accountName": INFO['main_account_name'],
            "supplierName": INFO['vice_sales_customer_name'],
            "deductionList": [
                {
                    "preId": res[0]['id'],
                    "deductionAmount": res[0]['userAmount']
                }
            ]
        }
        return self._make_request('post', 'r3lH50xQO', data, 'main', nocheck)


class UjpqCZlmIK(InitializeParams):
    """财务管理|业务记账|预付预收"""

    @doc(f9xh8uqQHD61p0h46zFQ)
    @BaseApi.timing_decorator
    def f9xh8uqQHD61p0h46zFQ(self, nocheck=False):
        data = {
            "amount": 100,
            "preType": "2",
            "receiptTime": self.get_the_date(),
            "remark": "备注",
            "supplierId": INFO['main_supplier_id'],
            "accountNo": INFO['main_account_no'],
            "userId": INFO['main_user_id'],
            "supplierName": INFO['main_supplier_name'],
            "userName": INFO['main_account'],
        }
        return self._make_request('post', 'uXc65JPTQ', data, 'main', nocheck)

    @doc(A7yoyiFi7P8jDGNe67Y0)
    @BaseApi.timing_decorator
    def A7yoyiFi7P8jDGNe67Y0(self, nocheck=False):
        data = {
            "preType": "1",
            "receiptTime": self.get_the_date(),
            "remark": "备注",
            "amount": 100,
            "supplierId": INFO['main_sale_supplier_id'],
            "accountNo": INFO['main_account_no'],
            "userId": INFO['main_user_id'],
            "supplierName": INFO['vice_sales_customer_name'],
            "userName": INFO['main_manager']
        }
        return self._make_request('post', 'uXc65JPTQ', data, 'main', nocheck)


if __name__ == '__main__':
    api = None
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
