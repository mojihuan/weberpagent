# coding: utf-8
import json
from common.base_api import BaseApi
from common.base_params import InitializeParams
from common.file_cache_manager import ParamCache
from common.import_desc import *
from config.user_info import INFO


class Sw9d3Jef89(InitializeParams):
    """保卖管理|退货管理"""

    @doc(uMfpb3JIBZ8oaq0US9Y7)
    @BaseApi.timing_decorator
    def uMfpb3JIBZ8oaq0US9Y7(self, nocheck=False):
        res = self.pc.TD9Y1EebwgkWWw4gbKGII(i=1)
        data = {
            "articlesNo": res[0]['articlesNo']
        }
        return self._make_request('post', 'X6YV0aF4q', data, 'main', nocheck)

    @doc(sbzcNzKjCNBmnqXBUAZP)
    @BaseApi.timing_decorator
    def sbzcNzKjCNBmnqXBUAZP(self, nocheck=False):
        res = self.pc.TD9Y1EebwgkWWw4gbKGII(i=2)
        data = {
            "articlesNo": res[0]['articlesNo']
        }
        return self._make_request('post', 'X6YV0aF4q', data, 'main', nocheck)

    @doc(WkJbfcCwi0eL85pLx7Hw)
    @BaseApi.timing_decorator
    def WkJbfcCwi0eL85pLx7Hw(self, nocheck=False):
        res = self.pc.TD9Y1EebwgkWWw4gbKGII(i=2)
        data = {
            "articlesNo": res[0]['articlesNo'],
            "logisticsType": 1,
            "addressId": INFO['main_user_address_id']
        }
        return self._make_request('post', 'QfEosa6DF', data, 'main', nocheck)

    @doc(LFI07j6GScehS4q0GPNd)
    @BaseApi.timing_decorator
    def LFI07j6GScehS4q0GPNd(self, nocheck=False):
        res = self.pc.TD9Y1EebwgkWWw4gbKGII(i=1)
        data = {
            "articlesNo": res[0]['articlesNo'],
            "logisticsType": 2,
            "addressId": 100
        }
        return self._make_request('post', 'QfEosa6DF', data, 'main', nocheck)

    @doc(K4TenJe5ql1CTH4mOryF)
    @BaseApi.timing_decorator
    def K4TenJe5ql1CTH4mOryF(self, nocheck=False):
        res = self.pc.TD9Y1EebwgkWWw4gbKGII(i=3)
        data = {
            "articlesNo": res[0]['articlesNo'],
        }
        return self._make_request('post', 'gDObOQ7Xg', data, 'main', nocheck)


class ZEvt5QWNey(InitializeParams):
    """保卖管理|订单列表"""

    @doc(GIh2R4s4U7in3JVtx4Fh)
    @BaseApi.timing_decorator
    def GIh2R4s4U7in3JVtx4Fh(self, nocheck=False):
        res = self.pc.BAc7o7mzTE8oACvyeArJW(data='a')
        data = {
            "quickList": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "articlesTypeName": res[0]['articlesTypeName'],
                    "brandName": res[0]['brandName'],
                    "modelName": res[0]['modelName'],
                    "skuInfo": res[0]['skuInfo'],
                    "finenessId": res[0]['finenessId'],
                    "finenessName": res[0]['finenessName'],
                    "supplierName": INFO['main_supplier_name'],
                    "warehouseId": INFO['main_item_warehouse_id'],
                    "warehouseName": INFO['main_item_warehouse_name'],
                    "articlesState": res[0]['articlesState'],
                    "inventoryStatus": res[0]['inventoryStatus'],
                    "articlesInfo": {
                        "createBy": res[0]['articlesInfo']['createBy'],
                        "createTime": res[0]['articlesInfo']['createTime'],
                        "updateBy": None,
                        "updateTime": None,
                        "remark": None,
                        "pageSize": 10,
                        "pageNum": 1,
                        "orderByColumn": "create_time",
                        "isAsc": "desc",
                        "erpStartTime": None,
                        "erpEndTime": None,
                        "id": res[0]['articlesInfo']['id'],
                        "articlesNo": res[0]['articlesInfo']['articlesNo'],
                        "articlesTypeId": res[0]['articlesInfo']['articlesTypeId'],
                        "articlesTypeName": res[0]['articlesInfo']['articlesTypeName'],
                        "brandId": res[0]['articlesInfo']['brandId'],
                        "brandName": res[0]['articlesInfo']['brandName'],
                        "modelId": res[0]['articlesInfo']['modelId'],
                        "modelName": res[0]['articlesInfo']['modelName'],
                        "romId": res[0]['articlesInfo']['romId'],
                        "romName": res[0]['articlesInfo']['romName'],
                        "ramId": None,
                        "ramName": "",
                        "colorId": res[0]['articlesInfo']['colorId'],
                        "colorName": res[0]['articlesInfo']['colorName'],
                        "buyChannelId": res[0]['articlesInfo']['buyChannelId'],
                        "buyChannelName": res[0]['articlesInfo']['buyChannelName'],
                        "smallModelId": res[0]['articlesInfo']['smallModelId'],
                        "smallModelName": res[0]['articlesInfo']['smallModelName'],
                        "warrantyDurationId": res[0]['articlesInfo']['warrantyDurationId'],
                        "warrantyDurationName": res[0]['articlesInfo']['warrantyDurationName'],
                        "batteryHealthId": res[0]['articlesInfo']['batteryHealthId'],
                        "batteryHealthName": res[0]['articlesInfo']['batteryHealthName'],
                        "finenessId": res[0]['articlesInfo']['finenessId'],
                        "finenessName": res[0]['articlesInfo']['finenessName'],
                        "networkStandardId": None,
                        "networkStandardName": None,
                        "machineTypeId": res[0]['articlesInfo']['machineTypeId'],
                        "machineTypeName": res[0]['articlesInfo']['machineTypeName'],
                        "mobileNetworkId": None,
                        "mobileNetworkName": None,
                        "unicomNetworkId": None,
                        "unicomNetworkName": None,
                        "telecomNetworkId": None,
                        "telecomNetworkName": None,
                        "lockedId": None,
                        "lockedName": None,
                        "ssdId": None,
                        "ssdName": None,
                        "caseSizeId": None,
                        "caseSizeName": None,
                        "mechanicalHardDriveId": None,
                        "mechanicalHardDriveName": None,
                        "processorId": None,
                        "processorName": None,
                        "graphicsCardModelId": None,
                        "graphicsCardModelName": None,
                        "caseMaterialId": None,
                        "caseMaterialName": None,
                        "connectId": None,
                        "connectName": None,
                        "isDelete": 0,
                        "assessParam": None,
                        "assessTitle": None,
                        "detailId": None,
                        "serialNo": res[0]['articlesInfo']['serialNo'],
                    },
                    "isQualityReport": False,
                    "expectationPrice": 800
                }
            ]
        }
        return self._make_request('post', 'LmcfcAJW5', data, 'main', nocheck)

    @doc(UxlDI72fkMivOA7TlGvw)
    @BaseApi.timing_decorator
    def UxlDI72fkMivOA7TlGvw(self, nocheck=False):
        res = self.pc.BAc7o7mzTE8oACvyeArJW(i=1)
        res_2 = self.pc.B63gyanXogW9NpUu1Gr1K()
        data = {
            "businessNo": res[0]['orderNo'],
            "type": 1,
            "childType": 1,
            "expectPostTimeStart": self.get_formatted_datetime(),
            "expressType": 1,
            "senderProvinceName": INFO['province_name'],
            "senderCityName": INFO['city_name'],
            "senderCountyName": INFO['county_name'],
            "senderProvinceId": INFO['province_id'],
            "senderCityId": INFO['city_id'],
            "senderCountyId": INFO['county_id'],
            "senderAddress": INFO['detailed_address'],
            "senderName": res_2[0]['name'],
            "senderPhone": res_2[0]['phone'],
            "recipientProvinceName": res_2[0]['provinceName'],
            "recipientCityName": res_2[0]['cityName'],
            "recipientCountyName": res_2[0]['countyName'],
            "recipientProvinceId": res_2[0]['provinceId'],
            "recipientCityId": res_2[0]['cityId'],
            "recipientCountyId": res_2[0]['countyId'],
            "recipientAddress": res_2[0]['address'],
            "recipientName": INFO['customer_name'],
            "recipientPhone": INFO['receiving_phone'],
            "expectPostTimeStartEnd": self.get_formatted_datetime(),
            "inspectionCenterId": INFO['check_the_center_id'],
        }
        return self._make_request('post', 'ikFrerqDh', data, 'main', nocheck)

    @doc(BSo6LUJtzBWcj6edgXxU)
    @BaseApi.timing_decorator
    def BSo6LUJtzBWcj6edgXxU(self, nocheck=False):
        res = self.pc.BAc7o7mzTE8oACvyeArJW(i=1)
        res_2 = self.pc.B63gyanXogW9NpUu1Gr1K()
        data = {
            "businessNo": res[0]['orderNo'],
            "type": 1,
            "childType": 2,
            "expectPostTimeStart": self.get_formatted_datetime(),
            "expressType": 2,
            "senderProvinceName": INFO['province_name'],
            "senderCityName": INFO['city_name'],
            "senderCountyName": INFO['county_name'],
            "senderProvinceId": INFO['province_id'],
            "senderCityId": INFO['city_id'],
            "senderCountyId": INFO['county_id'],
            "senderAddress": INFO['detailed_address'],
            "senderName": res_2[0]['name'],
            "senderPhone": res_2[0]['phone'],
            "recipientProvinceName": res_2[0]['provinceName'],
            "recipientCityName": res_2[0]['cityName'],
            "recipientCountyName": res_2[0]['countyName'],
            "recipientProvinceId": res_2[0]['provinceId'],
            "recipientCityId": res_2[0]['cityId'],
            "recipientCountyId": res_2[0]['countyId'],
            "recipientAddress": res_2[0]['address'],
            "recipientName": INFO['customer_name'],
            "recipientPhone": INFO['receiving_phone'],
            "expectPostTimeStartEnd": self.get_formatted_datetime(),
            "inspectionCenterId": INFO['check_the_center_id'],
        }
        return self._make_request('post', 'ikFrerqDh', data, 'main', nocheck)

    @doc(LPxZ1LIoEgSsdKTXRL2C)
    @BaseApi.timing_decorator
    def LPxZ1LIoEgSsdKTXRL2C(self, nocheck=False):
        res = self.pc.BAc7o7mzTE8oACvyeArJW(i=1)
        data = {
            "businessNo": res[0]['orderNo'],
            "type": 1,
            "childType": 3,
            "expectPostTimeStart": self.get_formatted_datetime(),
            "expressCompanyId": "shunfeng",
            "expressNo": self.sf,
            "expressCompanyName": "顺丰速运",
            "inspectionCenterId": INFO['check_the_center_id'],
        }
        return self._make_request('post', 'ikFrerqDh', data, 'main', nocheck)

    @doc(jhln7DhaP9NOD9X3azpU)
    @BaseApi.timing_decorator
    def ship_now_by_express_send_it_jhln7DhaP9NOD9X3azpUyourself(self, nocheck=False):
        res = self.pc.BAc7o7mzTE8oACvyeArJW(i=1)
        data = {
            "businessNo": res[0]['orderNo'],
            "type": "2",
            "childType": 3,
            "inspectionCenterId": INFO['check_the_center_id'],
        }
        return self._make_request('post', 'ikFrerqDh', data, 'main', nocheck)

    @doc(NEZ4KVsoQr6AgkUVtSBE)
    @BaseApi.timing_decorator
    def NEZ4KVsoQr6AgkUVtSBE(self, nocheck=False):
        res = self.pc.BAc7o7mzTE8oACvyeArJW(i=2)
        data = {
            "id": res[0]['id']
        }
        return self._make_request('post', 'yxUItLkk8', data, 'main', nocheck)

    @doc(qAhAnnHA7i5RWoR9HPAf)
    @BaseApi.timing_decorator
    def qAhAnnHA7i5RWoR9HPAf(self, nocheck=False):
        res = self.pc.BAc7o7mzTE8oACvyeArJW(i=3)
        res_2 = self.pc.B63gyanXogW9NpUu1Gr1K()
        data = {
            "businessNo": res[0]['orderNo'],
            "type": "1",
            "childType": 1,
            "expectPostTimeStart": self.get_formatted_datetime(),
            "expressType": 1,
            "senderProvinceName": INFO['province_name'],
            "senderCityName": INFO['city_name'],
            "senderCountyName": INFO['county_name'],
            "senderProvinceId": INFO['province_id'],
            "senderCityId": INFO['city_id'],
            "senderCountyId": INFO['county_id'],
            "senderAddress": INFO['detailed_address'],
            "senderName": res_2[0]['name'],
            "senderPhone": res_2[0]['phone'],
            "recipientProvinceName": res_2[0]['provinceName'],
            "recipientCityName": res_2[0]['cityName'],
            "recipientCountyName": res_2[0]['countyName'],
            "recipientProvinceId": res_2[0]['provinceId'],
            "recipientCityId": res_2[0]['cityId'],
            "recipientCountyId": res_2[0]['countyId'],
            "recipientAddress": res_2[0]['address'],
            "recipientName": INFO['customer_name'],
            "recipientPhone": INFO['receiving_phone'],
            "expectPostTimeStartEnd": self.get_formatted_datetime(),
            "inspectionCenterId": INFO['check_the_center_id'],
        }
        return self._make_request('post', 'nMM7fu8WE', data, 'main', nocheck)


class RETp2VmRwT(InitializeParams):
    """保卖管理|商品管理"""

    @doc(bEf5Mp7G2xinW35U9v4n)
    @BaseApi.timing_decorator
    def bEf5Mp7G2xinW35U9v4n(self, nocheck=False):
        res = self.pc.Krj5gFvH88BTJJo3iWzJX(i=2)
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = [
            {
                "id": obj,
                "saleType": "1",
                "salePricingType": 1,
                "upbeatPrice": 0
            }
        ]
        return self._make_request('post', 'VUNzXGZLo', data, 'main', nocheck)

    @doc(CNaaAq7VSiFlTyYNGrfk)
    @BaseApi.timing_decorator
    def CNaaAq7VSiFlTyYNGrfk(self, nocheck=False):
        res = self.pc.Krj5gFvH88BTJJo3iWzJX(i=2)
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = [
            {
                "id": obj,
                "saleType": "1",
                "salePricingType": 2,
                "upbeatPrice": 50
            }
        ]
        return self._make_request('post', 'VUNzXGZLo', data, 'main', nocheck)

    @doc(HG0qvmXGjLcEUjmJOKNy)
    @BaseApi.timing_decorator
    def HG0qvmXGjLcEUjmJOKNy(self, nocheck=False):
        res = self.pc.Krj5gFvH88BTJJo3iWzJX(i=2)
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = [
            {
                "id": obj,
                "saleType": "1",
                "salePricingType": 3
            }
        ]
        return self._make_request('post', 'VUNzXGZLo', data, 'main', nocheck)

    @doc(sUkAYaxto6tXXFUu1tyJ)
    @BaseApi.timing_decorator
    def sUkAYaxto6tXXFUu1tyJ(self, nocheck=False):
        res = self.pc.Krj5gFvH88BTJJo3iWzJX(i=2)
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = [
            {
                "id": obj,
                "saleType": "2",
                "salePricingType": 1,
                "upbeatPrice": 0
            }
        ]
        return self._make_request('post', 'VUNzXGZLo', data, 'main', nocheck)

    @doc(IpoZ907QoA7qXNUfox4T)
    @BaseApi.timing_decorator
    def IpoZ907QoA7qXNUfox4T(self, nocheck=False):
        res = self.pc.Krj5gFvH88BTJJo3iWzJX(i=2)
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = [
            {
                "id": obj,
                "saleType": "2",
                "salePricingType": 2,
                "upbeatPrice": 50
            }
        ]
        return self._make_request('post', 'VUNzXGZLo', data, 'main', nocheck)

    @doc(uojb7cbGSWgC8zL5aCWL)
    @BaseApi.timing_decorator
    def uojb7cbGSWgC8zL5aCWL(self, nocheck=False):
        res = self.pc.Krj5gFvH88BTJJo3iWzJX(i=2)
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = [
            {
                "id": obj,
                "saleType": "2",
                "salePricingType": 3
            }
        ]
        return self._make_request('post', 'VUNzXGZLo', data, 'main', nocheck)


    @doc(ecdR9lamw6zn0y9vyNRF)
    @BaseApi.timing_decorator
    def ecdR9lamw6zn0y9vyNRF(self, nocheck=False):
        res = self.pc.Krj5gFvH88BTJJo3iWzJX(i=3)
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id": obj
        }
        return self._make_request('post', 'Qdor1qV6S', data, 'main', nocheck)

    @doc(LrCC4svDp0JANhnDhJZH)
    @BaseApi.timing_decorator
    def LrCC4svDp0JANhnDhJZH(self, nocheck=False):
        res = self.pc.Krj5gFvH88BTJJo3iWzJX(i=3)
        obj = res[0]['id']
        ParamCache.cache_object({"id": obj}, 'practical.json')
        data = {
            "id":obj,
            "upbeatPrice": "50"
        }
        return self._make_request('post', 'xN6HW83XP', data, 'main', nocheck)


if __name__ == '__main__':
    api = ()
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
