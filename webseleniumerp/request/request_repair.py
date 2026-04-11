# coding: utf-8
import json
import random
from common.base_api import BaseApi
from common.base_params import InitializeParams
from common.import_desc import *
from config.user_info import INFO


class QSG3XpHrLa(InitializeParams):
    """维修管理|维修审核列表"""

    @doc(InAnaHvFTy76b32mumFp)
    @BaseApi.timing_decorator
    def InAnaHvFTy76b32mumFp(self, nocheck=False):
        res = self.pc.ZdhlTgRrRPGEMOegDrOfk(i=1)
        data = {
            "auditStatus": "2",
            "auditRemark": self.serial,
            "id": res[0]['id']
        }

        return self._make_request('post', 'gpadtMTQH', data, 'main', nocheck)

    @doc(oxfkjSLPMvxmooiko075)
    @BaseApi.timing_decorator
    def oxfkjSLPMvxmooiko075(self, nocheck=False):
        res = self.pc.ZdhlTgRrRPGEMOegDrOfk(i=1)
        data = {
            "auditStatus": "3",
            "auditRemark": self.serial,
            "id": res[0]['id']
        }
        return self._make_request('post', 'gpadtMTQH', data, 'main', nocheck)


class W0EPs560MV(InitializeParams):
    """维修管理|维修中物品"""

    @doc(PYrzOPhQBEGaXo51nyaY)
    @BaseApi.timing_decorator
    def PYrzOPhQBEGaXo51nyaY(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='7')
        data = {
            "status": "3",
            "sendTitle": "6",
            "repairPrice": 89,
            "repairRemark": "备注",
            "receiveId": INFO['main_user_id'],
            "repairItemId": "1958054203137277968,1958054203137277972",
            "articlesNoList": [
                res[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'QIDYpUMKK', data, 'main', nocheck)

    @doc(i1XbL2CrIPwi6h2C6y1T)
    @BaseApi.timing_decorator
    def i1XbL2CrIPwi6h2C6y1T(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='7')
        data = {
            "status": "3",
            "sendTitle": "2",
            "receiveId": INFO['main_user_id'],
            "repairRemark": "备注",
            "repairPrice": 54,
            "repairItemId": res[0]['id'],
            "articlesNoList": [
                res[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'QIDYpUMKK', data, 'main', nocheck)

    @doc(XZsjWIGPtCtyCOxtxlJo)
    @BaseApi.timing_decorator
    def XZsjWIGPtCtyCOxtxlJo(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='7')
        data = {
            "status": "3",
            "sendTitle": "4",
            "receiveId": INFO['main_user_id'],
            "repairPrice": 44,
            "repairRemark": "test",
            "repairItemId": res[0]['id'],
            "articlesNoList": [
                res[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'QIDYpUMKK', data, 'main', nocheck)

    @doc(FzCP5d1Cyk04Rg7XdXWW)
    @BaseApi.timing_decorator
    def FzCP5d1Cyk04Rg7XdXWW(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='7')
        data = {
            "type": "6",
            "userId": INFO['idle_user_id'],
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "createBy": INFO['customer_name']
        }
        return self._make_request('post', 'ShqXAnyJL', data, 'main', nocheck)

    @doc(kFFewUiXptz4lRt4hmYw)
    @BaseApi.timing_decorator
    def kFFewUiXptz4lRt4hmYw(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='7')
        res_2 = self.pc.CtRBRcFNn2LnUPfJF5Yhu(i='2')
        res_3 = self.pc.Gv7PVAqUJKoyfROzOacmx()
        data = {
            "status": "3",
            "sendTitle": "6",
            "repairPrice": 21,
            "repairRemark": "维修详情",
            "receiveId": INFO['main_user_id'],
            "repairItemId": res_3['tableData'][0]['id'],
            "articlesAndAccessoryJoinDTOS": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "accessoryNo": res_2[0]['articlesNo']
                }
            ],
            "articlesNoList": [
                res[0]['articlesNo'],
            ]
        }
        return self._make_request('post', 'QIDYpUMKK', data, 'main', nocheck)

    @doc(XaqAzFHNZ0oHiACVcagS)
    @BaseApi.timing_decorator
    def XaqAzFHNZ0oHiACVcagS(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i='2', j='7')
        data = {
            "apartInfoList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "accessoryNo": self.serial,
                    "articlesTypeId": 1,
                    "articlesTypeName": res[0]['articlesTypeName'],
                    "brandId": 1,
                    "brandName": res[0]['brandName'],
                    "modelId": res[0]['modelId'],
                    "modelName": res[0]['modelName'],
                    "baseAccessoryType": 2,
                    "baseAccessoryName": "主板铁片",
                    "accessoryType": 3,
                    "channelType": "1",
                    "warehouseId": INFO['main_warehouse_id'],
                    "warehouseName": INFO['main_warehouse_name'],
                    "reasonType": "2",
                    "remark": "物品维修拆件",
                    "receiveId": INFO['main_user_id'],
                    "receiveName": f"admin({INFO['main_account']})",
                    "reasonTypeStr": "维修"
                }
            ],
            "articlesNoList": [
                res[0]['articlesNo'],
            ]
        }
        return self._make_request('post', 'NfqIj1tge', data, 'main', nocheck)


class KHgN9h3KO8(InitializeParams):
    """维修管理|维修项目列表"""

    @doc(otRpL7YRWiPq6A7gGbBE)
    @BaseApi.timing_decorator
    def otRpL7YRWiPq6A7gGbBE(self, nocheck=False):
        res = self.pc.Gv7PVAqUJKoyfROzOacmx(i=1)
        data = {
            "name": "手机" + self.serial,
            "defaultPrice": 7,
            "categoryId": res['tableData'][0]['typeId'],
            "infoList": [
                {
                    "articlesTypeId": 1,
                    "articlesTypeName": "手机",
                    "defaultPrice": int(self.number)
                }
            ]
        }
        return self._make_request('post', 'FevaUyYbn', data, 'idle', nocheck)

    @doc(SMnvY0RuPqjFoUNE8XAA)
    @BaseApi.timing_decorator
    def SMnvY0RuPqjFoUNE8XAA(self, nocheck=False):
        res = self.pc.Gv7PVAqUJKoyfROzOacmx()
        data = {
            "name": "平板电脑" + self.serial,
            "defaultPrice": 0,
            "categoryId": res['tableData'][0]['typeId'],
            "infoList": [
                {
                    "articlesTypeId": 3,
                    "articlesTypeName": "平板电脑",
                    "defaultPrice": 0
                }
            ]
        }
        return self._make_request('post', 'FevaUyYbn', data, 'idle', nocheck)

    @doc(Io7zWL7mncGGiczqV0j9)
    @BaseApi.timing_decorator
    def Io7zWL7mncGGiczqV0j9(self, nocheck=False):
        res = self.pc.Gv7PVAqUJKoyfROzOacmx()
        data = {
            "name": "笔记本电脑" + self.serial,
            "defaultPrice": 0,
            "categoryId": res['tableData'][0]['typeId'],
            "infoList": [
                {
                    "articlesTypeId": 4,
                    "articlesTypeName": "笔记本电脑",
                    "defaultPrice": 0
                }
            ]
        }
        return self._make_request('post', 'FevaUyYbn', data, 'idle', nocheck)

    @doc(A8HudpWpzF5s1INr3oER)
    @BaseApi.timing_decorator
    def A8HudpWpzF5s1INr3oER(self, nocheck=False):
        res = self.pc.Gv7PVAqUJKoyfROzOacmx()
        data = {
            "name": "智能手表" + self.serial,
            "defaultPrice": 0,
            "categoryId": res['tableData'][0]['typeId'],
            "infoList": [
                {
                    "articlesTypeId": 5,
                    "articlesTypeName": "智能手表",
                    "defaultPrice": 0
                }
            ]
        }
        return self._make_request('post', 'FevaUyYbn', data, 'idle', nocheck)

    @doc(A3huxJD5Z6IGUspl0I6d)
    @BaseApi.timing_decorator
    def A3huxJD5Z6IGUspl0I6d(self, nocheck=False):
        res = self.pc.Gv7PVAqUJKoyfROzOacmx()
        data = {
            "name": res['tableData'][0]['name'],
            "defaultPrice": 0,
            "id": res['tableData'][0]['id'],
            "categoryId": res['tableData'][0]['typeId'],
        }
        return self._make_request('put', 'ncfR4CLDE', data, 'idle', nocheck)

    @doc(z6Fij1duyB9APTQsy7SW)
    @BaseApi.timing_decorator
    def z6Fij1duyB9APTQsy7SW(self, nocheck=False):
        res = self.pc.Gv7PVAqUJKoyfROzOacmx()
        data = [
            res['tableData'][0]['id'],
        ]
        return self._make_request('put', 'KZAoy8YVw', data, 'idle', nocheck)

    @doc(V0LveJcsirDBPkbnoy5r)
    @BaseApi.timing_decorator
    def V0LveJcsirDBPkbnoy5r(self, nocheck=False):
        model_names = ["iPhone 16 Pro Max", "iPhone 16 Pro", "iPhone 16", "iPhone 16 Plus"]
        model_id = [17569, 17568, 17567, 17566]
        data = {
            "modelName": random.choice(model_names),
            "brandName": "IPHONE",
            "modelId": random.choice(model_id),
            "brandId": 1,
            "articlesTypeId": "1",
            "articlesTypeName": "手机"
        }
        return self._make_request('post', 'CPWdm3YYp', data, 'idle', nocheck)


if __name__ == '__main__':
    api = None
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
