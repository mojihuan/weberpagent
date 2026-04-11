# coding: utf-8
import json
import time
from common.base_api import BaseApi
from common.base_params import InitializeParams
from common.file_cache_manager import ParamCache
from common.import_desc import *
from config.user_info import INFO

qualityCategoryList = BaseApi.load_json_file('request_fulfillment.json')['qualityCategoryList']
optionIdList = BaseApi.load_json_file('request_fulfillment.json')['optionIdList']
backfillList = BaseApi.load_json_file('request_fulfillment.json')['backfillList']


class Qc3N4qmsX7(InitializeParams):
    """运营中心|待报价物品"""

    @doc(h86Q9EJJuji9EAcwmnZd)
    @BaseApi.timing_decorator
    def h86Q9EJJuji9EAcwmnZd(self, nocheck=False):
        res = self.pc.RjVgo4LDzg4voonKUBXr1()
        data = {
            "reportAmount": self.number,
            "id": res[-1]['id']
        }
        return self._make_request('post', 'uJOhpQMHc', data, 'main', nocheck)

    @doc(HdVZdnVgjfeOetZQxl9C)
    @BaseApi.timing_decorator
    def HdVZdnVgjfeOetZQxl9C(self, nocheck=False):
        res = self.pc.RjVgo4LDzg4voonKUBXr1()
        data = {
            "reportAmount": self.number,
            "id": res[0]['id']
        }
        return self._make_request('post', 'uJOhpQMHc', data, 'main', nocheck)


class LCfJXeE7Mf(InitializeParams):
    """运营中心|质检管理"""

    @doc(EqKnTwPFi7SMTAPIanzC)
    @BaseApi.timing_decorator
    def EqKnTwPFi7SMTAPIanzC(self, nocheck=False):
        res = self.pc.FYXRA4IxF49PvhUCLpp5Z(data='f')
        data = {
            "distributorIds": [
                res[0]['id']
            ]
        }
        return self._make_request('post', 'SniiRehD4', data, 'camera', nocheck)

    @doc(jN6h3HHrblYl6XRDrjRp)
    @BaseApi.timing_decorator
    def jN6h3HHrblYl6XRDrjRp(self, nocheck=False):
        res = self.pc.FYXRA4IxF49PvhUCLpp5Z()
        data = {
            "distributorIds": [
                res[0]['id']
            ]
        }
        return self._make_request('post', 'SniiRehD4', data, 'main', nocheck)

    @doc(CLRwZ9FXvcE5gCYCPdSF)
    @BaseApi.timing_decorator
    def CLRwZ9FXvcE5gCYCPdSF(self, nocheck=False):
        res = self.pc.FYXRA4IxF49PvhUCLpp5Z()
        data = {
            "distributorIds": [
                res[0]['id']
            ]
        }
        return self._make_request('post', 'SniiRehD4', data, 'main', nocheck)

    @doc(eoidlhlWuLRCRQL3uNIN)
    @BaseApi.timing_decorator
    def eoidlhlWuLRCRQL3uNIN(self, nocheck=False):
        res = self.pc.FYXRA4IxF49PvhUCLpp5Z()
        data = {
            "distributorIds": [
                res[0]['id']
            ]
        }
        return self._make_request('post', 'SniiRehD4', data, 'main', nocheck)

    @doc(knHZe0CfAp1HXSNNW4nG)
    @BaseApi.timing_decorator
    def knHZe0CfAp1HXSNNW4nG(self, nocheck=False):
        res = self.pc.FYXRA4IxF49PvhUCLpp5Z()
        data = {
            "distributorIds": [
                res[0]['id']
            ]
        }
        return self._make_request('post', 'SniiRehD4', data, 'main', nocheck)

    @doc(oKZEC3OeI0tWc8WLWpY3)
    @BaseApi.timing_decorator
    def oKZEC3OeI0tWc8WLWpY3(self, nocheck=False):
        self.wait_default()
        res = self.pc.FYXRA4IxF49PvhUCLpp5Z(data='g')
        res_2 = self.pc.FYXRA4IxF49PvhUCLpp5Z(data='h')
        data = {
            "qualityCategoryList": qualityCategoryList,
            "articlesInfo": {
                "imei": res[0]['imei'],
                "brandName": res[0]['brandName'],
                "modelName": res[0]['modelName'],
                "modelId": res[0]['modelId'],
                "brandId": res[0]['brandId'],
                "colorId": 1712,
                "colorName": "黑色钛金属",
                "warrantyDurationId": 600,
                "warrantyDurationName": "保修≥331天",
                "buyChannelId": 16,
                "buyChannelName": "国行",
                "romId": 41,
                "romName": "256G",
                "smallModelId": 72,
                "smallModelName": "其他型号",
                "regionInfoId": "CH/A",
                "regionInfoName": "国行",
                "articlesTypeId": 1,
                "articlesTypeName": "手机"
            },
            "articlesNo": res[0]['articlesNo'],
            "optionIdList": optionIdList,
            "articlesImageVideoList": [
                {
                    "imageVideoUrl": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com/erp-video/1770362981772.jpeg",
                    "id": ""
                }
            ],
            "templateId": res_2[0]['id'],
            "isOther": 1,
            "finenessId": 130,
            "finenessName": "靓机",
            "functionGradeId": 114,
            "functionGrade": "A",
            "finenessSort": 1,
            "qualityCentreId": res[0]['id']
        }
        return self._make_request('post', 'yqBmQRl4A', data, 'camera', nocheck)

    @doc(rqPmiTtsuecNOe8Qa0FW)
    @BaseApi.timing_decorator
    def rqPmiTtsuecNOe8Qa0FW(self, nocheck=False):
        self.wait_default()
        res = self.pc.FYXRA4IxF49PvhUCLpp5Z(data='a')
        res_2 = self.pc.FYXRA4IxF49PvhUCLpp5Z(data='e')
        data = {
            "qualityCategoryList": qualityCategoryList,
            "articlesInfo": {
                "imei": res[0]['imei'],
                "brandName": res[0]['brandName'],
                "modelName": res[0]['modelName'],
                "modelId": res[0]['modelId'],
                "brandId": res[0]['brandId'],
                "colorId": 1712,
                "colorName": "黑色钛金属",
                "warrantyDurationId": 600,
                "warrantyDurationName": "保修≥331天",
                "buyChannelId": 16,
                "buyChannelName": "国行",
                "romId": 41,
                "romName": "256G",
                "smallModelId": 72,
                "smallModelName": "其他型号",
                "regionInfoId": "CH/A",
                "regionInfoName": "国行",
                "articlesTypeId": 1,
                "articlesTypeName": "手机"
            },
            "articlesNo": res[0]['articlesNo'],
            "optionIdList": optionIdList,
            "articlesImageVideoList": [
                {
                    "imageVideoUrl": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com/erp-video/1770362981772.jpeg",
                    "id": ""
                }
            ],
            "templateId": res_2[0]['id'],
            "isOther": 1,
            "finenessId": 130,
            "finenessName": "靓机",
            "functionGradeId": 114,
            "functionGrade": "A",
            "finenessSort": 1,
            "qualityCentreId": res[0]['id']
        }
        return self._make_request('post', 'yqBmQRl4A', data, 'main', nocheck)

    @doc(NGkklZ12l2IiB7qVbQxE)
    @BaseApi.timing_decorator
    def NGkklZ12l2IiB7qVbQxE(self, nocheck=False):
        self.wait_default()
        res = self.pc.FYXRA4IxF49PvhUCLpp5Z(data='a')
        res_2 = self.pc.FYXRA4IxF49PvhUCLpp5Z(data='e')
        data = {
            "qualityCategoryList": qualityCategoryList,
            "articlesInfo": {
                "imei": res[0]['imei'],
                "brandName": res[0]['brandName'],
                "modelName": res[0]['modelName'],
                "modelId": res[0]['modelId'],
                "brandId": res[0]['brandId'],
                "romId": 41,
                "romName": "256G",
                "colorId": 1712,
                "colorName": "黑色钛金属",
                "warrantyDurationId": 600,
                "warrantyDurationName": "保修≥331天",
                "smallModelId": 1743,
                "smallModelName": "A3297",
                "regionInfoId": "CH/A",
                "regionInfoName": "国行",
                "buyChannelId": 16,
                "buyChannelName": "国行",
                "articlesTypeId": 1,
                "articlesTypeName": "手机"
            },
            "articlesNo": res[0]['articlesNo'],
            "optionIdList": optionIdList,
            "articlesImageVideoList": [
                {
                    "imageVideoUrl": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com/erp-video/1770013221718.jpeg",
                    "id": ""
                }
            ],
            "templateId": res_2[0]['id'],
            "isOther": 1,
            "finenessId": 130,
            "finenessName": "靓机",
            "functionGradeId": 114,
            "functionGrade": "A",
            "finenessSort": 1,
            "qualityCentreId": res[0]['id'],
        }
        return self._make_request('post', 'yqBmQRl4A', data, 'main', nocheck)

    @doc(JO1O4Cu3NqUy2eHg71Sb)
    @BaseApi.timing_decorator
    def JO1O4Cu3NqUy2eHg71Sb(self, nocheck=False):
        self.wait_default()
        res = self.pc.FYXRA4IxF49PvhUCLpp5Z(data='a')
        res_2 = self.pc.FYXRA4IxF49PvhUCLpp5Z(data='e')
        data = {
            "qualityCategoryList": qualityCategoryList,
            "articlesInfo": {
                "imei": res[0]['imei'],
                "brandName": res[0]['brandName'],
                "modelName": res[0]['modelName'],
                "modelId": res[0]['modelId'],
                "brandId": res[0]['brandId'],
                "romId": 41,
                "romName": "256G",
                "colorId": 1712,
                "colorName": "黑色钛金属",
                "warrantyDurationId": 600,
                "warrantyDurationName": "保修≥331天",
                "smallModelId": 1743,
                "smallModelName": "A3297",
                "regionInfoId": "CH/A",
                "regionInfoName": "国行",
                "buyChannelId": 16,
                "buyChannelName": "国行",
                "articlesTypeId": 1,
                "articlesTypeName": "手机"
            },
            "articlesNo": res[0]['articlesNo'],
            "optionIdList": optionIdList,
            "articlesImageVideoList": [
                {
                    "imageVideoUrl": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com/erp-video/1770013221718.jpeg",
                    "id": ""
                }
            ],
            "templateId": res_2[0]['id'],
            "isOther": 1,
            "finenessId": 130,
            "finenessName": "靓机",
            "functionGradeId": 114,
            "functionGrade": "A",
            "finenessSort": 1,
            "qualityCentreId": res[0]['id'],
        }
        return self._make_request('post', 'yqBmQRl4A', data, 'main', nocheck)

    @doc(TJXWHGYpzVeCuC3cZjrH)
    @BaseApi.timing_decorator
    def TJXWHGYpzVeCuC3cZjrH(self, nocheck=False):
        self.wait_default()
        res = self.pc.FYXRA4IxF49PvhUCLpp5Z(data='a')
        data = {
            "articlesNo": res[0]['articlesNo'],
            "qualityCategoryList": qualityCategoryList,
            "articlesInfo": {
                "imei": res[0]['imei'],
                "brandId": 1,
                "modelId": 17569,
                "modelName": "iPhone 16 Pro Max",
                "romId": 41,
                "romName": "256G",
                "colorId": 1712,
                "colorName": "黑色钛金属",
                "warrantyDurationId": 600,
                "warrantyDurationName": "保修≥331天",
                "smallModelId": 72,
                "smallModelName": "其他型号",
                "regionInfoId": "CH/A",
                "regionInfoName": "国行",
                "buyChannelId": 16,
                "buyChannelName": "国行",
                "articlesTypeId": 1,
                "articlesTypeName": "手机",
                "brandName": "苹果"
            },
            "optionIdList": optionIdList,
            "articlesImageVideoList": [
                {
                    "imageVideoUrl": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com/erp-video/1770434613905.jpeg",
                    "id": ""
                }
            ],
            "templateId": 2,
            "isOther": 1,
            "finenessId": 130,
            "finenessName": "靓机",
            "functionGradeId": 114,
            "functionGrade": "A",
            "finenessSort": 1,
            "qualityCentreId": res[0]['id']
        }
        return self._make_request('post', 'yqBmQRl4A', data, 'main', nocheck)

    @doc(zBKyvA1lFKeRAKK0WXqg)
    @BaseApi.timing_decorator
    def zBKyvA1lFKeRAKK0WXqg(self, nocheck=False):
        self.wait_default()
        res = self.pc.FYXRA4IxF49PvhUCLpp5Z(data='a')
        data = {
            "articlesNo": res[0]['articlesNo'],
            "qualityCategoryList": qualityCategoryList,
            "articlesInfo": {
                "imei": res[0]['imei'],
                "brandId": res[0]['brandId'],
                "modelId": res[0]['modelId'],
                "modelName": res[0]['modelName'],
                "romId": 41,
                "romName": "256G",
                "smallModelId": 72,
                "smallModelName": "其他型号",
                "regionInfoId": "CH/A",
                "regionInfoName": "国行",
                "colorId": 1712,
                "colorName": "黑色钛金属",
                "warrantyDurationId": 600,
                "warrantyDurationName": "保修≥331天",
                "buyChannelId": 16,
                "buyChannelName": "国行",
                "articlesTypeId": 1,
                "articlesTypeName": "手机",
                "brandName": res[0]['brandName']
            },
            "optionIdList": optionIdList,
            "articlesImageVideoList": [
                {
                    "imageVideoUrl": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com/erp-video/1770433163696.jpeg",
                    "id": ""
                }
            ],
            "templateId": 2,
            "isOther": 1,
            "finenessId": 130,
            "finenessName": "靓机",
            "functionGradeId": 114,
            "functionGrade": "A",
            "finenessSort": 1,
            "qualityCentreId": res[0]['id']
        }
        return self._make_request('post', 'yqBmQRl4A', data, 'main', nocheck)

    @doc(eL32NtimAkRJKwnmSauo)
    @BaseApi.timing_decorator
    def eL32NtimAkRJKwnmSauo(self, nocheck=False):
        res = self.pc.FYXRA4IxF49PvhUCLpp5Z(data='c')
        data = {
            "recheckId": res[0]['id'],
            "recheckStatus": "2",
            "reviewReason": "审核说明"
        }
        return self._make_request('post', 'djxv8tLOX', data, 'main', nocheck)

    @doc(d6dbbDv54duJQhN6VKNl)
    @BaseApi.timing_decorator
    def d6dbbDv54duJQhN6VKNl(self, nocheck=False):
        res = self.pc.FYXRA4IxF49PvhUCLpp5Z(data='c')
        data = {
            "recheckId": res[0]['id'],
            "recheckStatus": "3",
            "reviewReason": "审核说明"
        }
        return self._make_request('post', 'djxv8tLOX', data, 'main', nocheck)

    @doc(CLHIAAqc0GcsqVloSnnm)
    @BaseApi.timing_decorator
    def CLHIAAqc0GcsqVloSnnm(self, nocheck=False):
        res = self.pc.FYXRA4IxF49PvhUCLpp5Z(data='b')
        res_2 = self.pc.FYXRA4IxF49PvhUCLpp5Z(data='e')
        data = {
            "articlesNo": res[0]['articlesNo'],
            "qualityCategoryList": qualityCategoryList,
            "articlesInfo": {
                "imei": res[0]['imei'],
                "brandName": res[0]['brandName'],
                "modelName": res[0]['modelName'],
                "modelId": res[0]['modelId'],
                "brandId": res[0]['brandId'],
                "smallModelId": 72,
                "buyChannelId": 16,
                "colorId": 1712,
                "romId": 41,
                "warrantyDurationId": 600,
                "regionInfoId": "CH/A",
                "romName": "256G",
                "smallModelName": "其他型号",
                "colorName": "黑色钛金属",
                "regionInfoName": "国行",
                "warrantyDurationName": "保修≥331天",
                "buyChannelName": "国行",
                "articlesTypeId": 1,
                "articlesTypeName": "手机"
            },
            "backfillList": backfillList,
            "optionIdList": optionIdList,
            "articlesImageVideoList": [
                {
                    "id": res[0]['id'],
                    "articlesNo": res[0]['articlesNo'],
                    "imageVideoUrl": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com/erp-video/1770362981772.jpeg",
                    "imageVideoName": "20260207000045",
                    "type": 1
                }
            ],
            "templateId": res_2[0]['id'],
            "isOther": 1,
            "finenessId": 130,
            "finenessName": "靓机",
            "functionGradeId": 114,
            "functionGrade": "A",
            "finenessSort": 1,
            "qualityRecordId": res[0]['id']
        }
        return self._make_request('post', 'o9r97kThA', data, 'main', nocheck)

    @doc(M6cvV0SyzVBbb2kyvAYl)
    @BaseApi.timing_decorator
    def M6cvV0SyzVBbb2kyvAYl(self, nocheck=False):
        res = self.pc.FYXRA4IxF49PvhUCLpp5Z(data='a')
        data = {
            "reasonType": 1,
            "userId": INFO['main_user_id'],
            "qualityIds": [
                res[0]['id']
            ]
        }
        return self._make_request('post', 'EExTYvo1M', data, 'main', nocheck)

    @doc(RXoB3Agr98ilYZlNb5FZ)
    @BaseApi.timing_decorator
    def RXoB3Agr98ilYZlNb5FZ(self, nocheck=False):
        res = self.pc.FYXRA4IxF49PvhUCLpp5Z(data='a')
        data = {
            "qualityId": res[0]['id'],
            "reasonTypeList": [
                1,
                2
            ]
        }
        return self._make_request('post', 'wDhxYplw5', data, 'main', nocheck)

    @doc(y203S2h47mnZp3O3L8J9)
    @BaseApi.timing_decorator
    def y203S2h47mnZp3O3L8J9(self, nocheck=False):
        res = self.pc.FYXRA4IxF49PvhUCLpp5Z(data='d', i=1)
        data = {
            "articlesNo": res[0]['articlesNo'],
            "type": 1,
            "imageVideoUrls": [
                "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com/erp-video/1767608255124.jpeg"
            ]
        }
        return self._make_request('post', 'biZihRUEH', data, 'main', nocheck)


class PrpdxJpu3k(InitializeParams):
    """运营中心|退货管理"""

    @doc(BBIpXJ7xM3RSMC8Gh7uI)
    @BaseApi.timing_decorator
    def BBIpXJ7xM3RSMC8Gh7uI(self, nocheck=False):
        res = self.pc.M4Xsay25almyg0RzXz4ui(data='a', i=1)
        data = {
            "type": "1",
            "expressCompanyId": "shunfengkuaiyun",
            "expressNo": self.sf,
            "childType": 2,
            "tenantId": INFO['merchant_id'],
            "expressCompanyName": "顺丰快运",
            "returnGoodsItem": [
                {
                    "returnOrderNo": res[0]['returnOrderNo'],
                    "batchNo": None,
                    "articlesNo": res[0]['articlesNo']
                }
            ]
        }
        return self._make_request('post', 'Pdcg1Tx6w', data, 'main', nocheck)

    @doc(zdM1FoDt6AVwrkGz7nPX)
    @BaseApi.timing_decorator
    def zdM1FoDt6AVwrkGz7nPX(self, nocheck=False):
        res = self.pc.D7NTmTMqMuHicClYboqMC(data='a')
        data = [
            res['pickupCode']
        ]
        return self._make_request('post', 'M90t3nNxs', data, 'main', nocheck)


class NDafRJuz1F(InitializeParams):
    """运营中心|收货入库"""

    # 搜索订单号
    @BaseApi.timing_decorator
    def search_tracking_numbers(self, nocheck=False):
        res = self.pc.VzruD2bzEUPV1JJY9d6vF(i=3)
        data = {
            "consignmentOrderNo": res[0]['orderNo']
        }
        return self._make_request('post', 'cy2zWx61q', data, 'main', nocheck)

    @doc(JdFjESShYyLExa0NBUR4)
    @BaseApi.timing_decorator
    def JdFjESShYyLExa0NBUR4(self, nocheck=False):
        res = self.pc.KgbSrz63njmC8XfrU1jty()
        data = {
            "reasonType": 1,
            "userId": INFO['main_user_id'],
            "consignmentReceiptStoreVOList": [
                {
                    "id": None,
                    "articlesNo": res[0]['articlesNo'],
                    "imei": self.imei,
                    "erpArticlesNo": None,
                    "erpImei": None,
                    "articlesTypeId": res[0]['articlesTypeId'],
                    "articlesTypeName": res[0]['articlesTypeName'],
                    "brandId": res[0]['brandId'],
                    "brandName": res[0]['brandName'],
                    "modelId": res[0]['modelId'],
                    "modelName": res[0]['modelName'],
                    "finenessId": None,
                    "finenessName": None,
                    "skuInfo": None,
                    "businessType": res[0]['businessType'],
                    "businessTypeStr": res[0]['businessTypeStr'],
                    "consignmentOrderNo": res[0]['consignmentOrderNo'],
                    "tenantId": res[0]['tenantId'],
                    "tenantStr": INFO['main_username'],
                    "userId": INFO['main_user_id'],
                    "inspectionCenterId": INFO['check_the_center_id'],
                    "inspectionCenterCode": INFO['merchant_id'],
                    "expressNo": None,
                    "auctionAfterSales": None
                }
            ],
            "orderVideoItemDTOList": [
                {
                    "videoUrl": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com/erp-video/1767147017529.mp4",
                    "orderNo": res[0]['consignmentOrderNo'],
                    "videoName": "收货视频01"
                }
            ],
            "auctionAfterSales": False
        }
        return self._make_request('post', 'q6kIpVZXv', data, 'main', nocheck)

    @doc(zd9DnAScYux2tHzIRjJT)
    @BaseApi.timing_decorator
    def zd9DnAScYux2tHzIRjJT(self, nocheck=False):
        res = self.pc.KgbSrz63njmC8XfrU1jty(data='c')
        data = {
            "reasonType": 1,
            "userId": INFO['camera_user_id'],
            "consignmentReceiptStoreVOList": [
                {
                    "id": None,
                    "articlesNo": res[0]['articlesNo'],
                    "imei": self.imei,
                    "erpArticlesNo": None,
                    "erpImei": None,
                    "articlesTypeId": res[0]['articlesTypeId'],
                    "articlesTypeName": res[0]['articlesTypeName'],
                    "brandId": res[0]['brandId'],
                    "brandName": res[0]['brandName'],
                    "modelId": res[0]['modelId'],
                    "modelName": res[0]['modelName'],
                    "finenessId": None,
                    "finenessName": None,
                    "skuInfo": None,
                    "businessType": res[0]['businessType'],
                    "businessTypeStr": res[0]['businessTypeStr'],
                    "consignmentOrderNo": res[0]['consignmentOrderNo'],
                    "tenantId": res[0]['tenantId'],
                    "tenantStr": INFO['camera_username'],
                    "userId": INFO['camera_user_id'],
                    "inspectionCenterId": INFO['camera_check_the_center_id'],
                    "inspectionCenterCode": INFO['camera_merchant_id'],
                    "expressNo": None,
                    "auctionAfterSales": None
                }
            ],
            "orderVideoItemDTOList": [
                {
                    "videoUrl": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com/erp-video/1767147017529.mp4",
                    "orderNo": res[0]['consignmentOrderNo'],
                    "videoName": "收货视频01"
                }
            ],
            "auctionAfterSales": False
        }
        return self._make_request('post', 'q6kIpVZXv', data, 'camera', nocheck)

    @doc(IYU1aVy8aH3qWm62ZtJp)
    @BaseApi.timing_decorator
    def IYU1aVy8aH3qWm62ZtJp(self, nocheck=False):
        res = self.pc.KgbSrz63njmC8XfrU1jty()
        data = {
            "reasonType": 1,
            "userId": INFO['main_user_id'],
            "consignmentReceiptStoreVOList": [
                {
                    "id": None,
                    "articlesNo": res[0]['articlesNo'],
                    "imei": self.imei,
                    "erpArticlesNo": None,
                    "erpImei": None,
                    "articlesTypeId": res[0]['articlesTypeId'],
                    "articlesTypeName": res[0]['articlesTypeName'],
                    "brandId": res[0]['brandId'],
                    "brandName": res[0]['brandName'],
                    "modelId": res[0]['modelId'],
                    "modelName": res[0]['modelName'],
                    "finenessId": None,
                    "finenessName": None,
                    "skuInfo": None,
                    "businessType": res[0]['businessType'],
                    "businessTypeStr": res[0]['businessTypeStr'],
                    "consignmentOrderNo": res[0]['consignmentOrderNo'],
                    "tenantId": res[0]['tenantId'],
                    "tenantStr": INFO['main_username'],
                    "userId": INFO['main_user_id'],
                    "inspectionCenterId": INFO['check_the_center_id'],
                    "inspectionCenterCode": INFO['merchant_id'],
                    "expressNo": None,
                    "auctionAfterSales": None
                }
            ],
            "orderVideoItemDTOList": [
                {
                    "videoUrl": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com/erp-video/1767147017529.mp4",
                    "orderNo": res[0]['consignmentOrderNo'],
                    "videoName": "收货视频01"
                }
            ],
            "auctionAfterSales": False
        }
        return self._make_request('post', 'q6kIpVZXv', data, 'main', nocheck)


class I7YRIi2RnR(InitializeParams):
    """运营中心|订单管理"""

    @doc(zHywULjwAZbQYE4tEyui)
    @BaseApi.timing_decorator
    def zHywULjwAZbQYE4tEyui(self, nocheck=False):
        res = self.pc.UYV6mZaVwDk4HHhyuWRRp(i=2, j=3)
        res_2 = self.pc.VzruD2bzEUPV1JJY9d6vF(data='a')
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
                    "finenessName": res_2[0]['articlesInfo']['finenessName'],
                    "finenessSort": None,
                    "functionGradeId": None,
                    "functionGrade": None,
                    "supplierName": INFO['main_supplier_name'],
                    "warehouseId": INFO['main_item_warehouse_id'],
                    "warehouseName": INFO['main_item_warehouse_name'],
                    "articlesState": res_2[0]['articlesState'],
                    "inventoryStatus": res_2[0]['inventoryStatus'],
                    "articlesInfo": {
                        "createBy": INFO['customer_name'],
                        "createTime": res[0]['createTime'],
                        "updateBy": None,
                        "updateTime": None,
                        "remark": None,
                        "pageSize": 10,
                        "pageNum": 1,
                        "orderByColumn": "create_time",
                        "isAsc": "desc",
                        "erpStartTime": None,
                        "erpEndTime": None,
                        "id": res_2[0]['articlesInfo']['id'],
                        "articlesNo": res[0]['articlesNo'],
                        "articlesTypeId": 1,
                        "articlesTypeName": "手机",
                        "brandId": res[0]['brandId'],
                        "brandName": res[0]['brandName'],
                        "modelId": res[0]['modelId'],
                        "modelName": res[0]['modelName'],
                        "romId": res_2[0]['articlesInfo']['romId'],
                        "romName": res_2[0]['articlesInfo']['romName'],
                        "ramId": None,
                        "ramName": "",
                        "colorId": res_2[0]['articlesInfo']['colorId'],
                        "colorName": res_2[0]['articlesInfo']['colorName'],
                        "buyChannelId": res_2[0]['articlesInfo']['buyChannelId'],
                        "buyChannelName": res_2[0]['articlesInfo']['buyChannelName'],
                        "smallModelId": res_2[0]['articlesInfo']['smallModelId'],
                        "smallModelName": res_2[0]['articlesInfo']['smallModelName'],
                        "warrantyDurationId": res_2[0]['articlesInfo']['warrantyDurationId'],
                        "warrantyDurationName": res_2[0]['articlesInfo']['warrantyDurationName'],
                        "batteryHealthId": res_2[0]['articlesInfo']['batteryHealthId'],
                        "batteryHealthName": res_2[0]['articlesInfo']['batteryHealthName'],
                        "finenessId": res_2[0]['articlesInfo']['finenessId'],
                        "finenessName": res_2[0]['articlesInfo']['finenessName'],
                        "finenessSort": None,
                        "functionGradeId": None,
                        "functionGrade": None,
                        "networkStandardId": None,
                        "networkStandardName": None,
                        "machineTypeId": 862,
                        "machineTypeName": "二手优品",
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
                        "serialNo": res[0]['serialNo']
                    },
                    "isQualityReport": None,
                    "isShowExclamation": True,
                    "exclamationText": "当物品在ERP没有质检报告"
                }
            ]
        }
        return self._make_request('post', 'TWvSffqwL', data, 'main', nocheck)


class Pzx3xU1ulY(InitializeParams):
    """运营中心|物品出库"""

    @doc(YtFzTr37KoEb6ObJhKgF)
    @BaseApi.timing_decorator
    def YtFzTr37KoEb6ObJhKgF(self, nocheck=False):
        for _ in range(2):
            time.sleep(1.5)
            self.pc.KmxOWBECeMnMqtP1qACyx(data='a')
        res = self.pc.KmxOWBECeMnMqtP1qACyx(data='a')
        data = {
            "sendType": 1,
            "buyTenantId": INFO['camera_merchant_id'],
            "saleArticlesNoList": [
                res[0]['articlesNo']
            ],
            "ifUseSystemPickup": 0,
            "expressCompanyType": 1,
            "expressCompanyId": 1,
            "expressCompanyName": "顺丰",
            "expressNo": self.sf
        }
        return self._make_request('post', 'Z6QzyEre9', data, 'main', nocheck)

    @doc(zGpyxwdonEj5rUxkbGDz)
    @BaseApi.timing_decorator
    def zGpyxwdonEj5rUxkbGDz(self, nocheck=False):
        res = self.pc.KmxOWBECeMnMqtP1qACyx(data='a')
        data = {
            "sendType": 1,
            "buyTenantId": INFO['camera_merchant_id'],
            "saleArticlesNoList": [
                res[0]['articlesNo']
            ],
            "ifUseSystemPickup": 0,
            "expressCompanyType": 2,
            "expressCompanyId": 1,
            "expressCompanyName": "京东",
            "expressNo": self.jd
        }
        return self._make_request('post', 'Z6QzyEre9', data, 'main', nocheck)

    @doc(hVymbb8xmLoC1GpxmlSy)
    @BaseApi.timing_decorator
    def hVymbb8xmLoC1GpxmlSy(self, nocheck=False):
        res = self.pc.KmxOWBECeMnMqtP1qACyx(data='a')
        data = {
            "sendType": 1,
            "buyTenantId": INFO['camera_merchant_id'],
            "saleArticlesNoList": [
                res[0]['articlesNo']
            ],
            "ifUseSystemPickup": 1,
            "expressCompanyType": 1,
            "expressCompanyId": 1,
            "expressCompanyName": "顺丰",
            "expectPostTimeStart": self.get_formatted_datetime()
        }
        return self._make_request('post', 'Z6QzyEre9', data, 'main', nocheck)

    @doc(yTdtu0H22ya7KmgU59hG)
    @BaseApi.timing_decorator
    def yTdtu0H22ya7KmgU59hG(self, nocheck=False):
        res = self.pc.KmxOWBECeMnMqtP1qACyx(data='a')
        data = {
            "sendType": 1,
            "buyTenantId": INFO['camera_merchant_id'],
            "saleArticlesNoList": [
                res[0]['articlesNo']
            ],
            "ifUseSystemPickup": 1,
            "expressCompanyType": 2,
            "expressCompanyId": 1,
            "expressCompanyName": "京东",
            "expectPostTimeStart": self.get_formatted_datetime()
        }
        return self._make_request('post', 'Z6QzyEre9', data, 'main', nocheck)

    @doc(g4RyFUrC2BkjMHRKinuq)
    @BaseApi.timing_decorator
    def g4RyFUrC2BkjMHRKinuq(self, nocheck=False):
        res = self.pc.UAPqxpSx1qiMwyQEcIPXb(i=3)
        data = {
            "sendType": "2",
            "buyTenantId": INFO['camera_merchant_id'],
            "saleArticlesNoList": [
                res[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'Z6QzyEre9', data, 'main', nocheck)

    @doc(OP7wFFxaC2oDvVTeezXi)
    @BaseApi.timing_decorator
    def OP7wFFxaC2oDvVTeezXi(self, nocheck=False):
        res = self.pc.YBoIFlRaGyVtfzeObzsmf(i=1)
        obj = res[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj}, 'practical.json')
        data = {
            "childType": 1,
            "expectPostTimeStart": self.get_formatted_datetime(),
            "senderName": INFO['customer_name'],
            "senderPhone": INFO['receiving_phone'],
            "senderProvinceId": INFO['province_id'],
            "senderProvinceName": INFO['province_name'],
            "senderCityId": INFO['city_id'],
            "senderCityName": INFO['city_name'],
            "senderCountyId": INFO['city_name'],
            "senderCountyName": INFO['county_name'],
            "senderAddress": INFO['detailed_address'],
            "recipientName": INFO['camera_name'],
            "recipientPhone": INFO['camera_phone'],
            "recipientProvinceId": INFO['province_id'],
            "recipientProvinceName": INFO['province_name'],
            "recipientCityId": INFO['city_id'],
            "recipientCityName": INFO['city_name'],
            "recipientCountyId": INFO['county_id'],
            "recipientCountyName": INFO['county_name'],
            "recipientAddress": INFO['detailed_address'],
            "expressType": 1,
            "addressId": INFO['camera_user_address_pj_id'],
            "inspectionCenterId": INFO['check_the_center_id'],
            "inspectionCenterCode": INFO['merchant_id'],
            "inspectionCenterName": INFO['check_the_center_name'],
            "returnGoodsItem": [
                {
                    "returnOrderNo": res[0]['afterOrderNo'],
                    "articlesNo": obj
                }
            ]
        }
        return self._make_request('post', 'ML8Yeu3JI', data, 'main', nocheck)

    @doc(q4HsL6oaiZ29NvrH0p4P)
    @BaseApi.timing_decorator
    def q4HsL6oaiZ29NvrH0p4P(self, nocheck=False):
        res = self.pc.YBoIFlRaGyVtfzeObzsmf(i=1)
        obj = res[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj}, 'practical.json')
        data = {
            "childType": 1,
            "expectPostTimeStart": self.get_formatted_datetime(),
            "senderName": INFO['customer_name'],
            "senderPhone": INFO['receiving_phone'],
            "senderProvinceId": INFO['province_id'],
            "senderProvinceName": INFO['province_name'],
            "senderCityId": INFO['city_id'],
            "senderCityName": INFO['city_name'],
            "senderCountyId": INFO['city_name'],
            "senderCountyName": INFO['county_name'],
            "senderAddress": INFO['detailed_address'],
            "recipientName": INFO['camera_name'],
            "recipientPhone": INFO['camera_phone'],
            "recipientProvinceId": INFO['province_id'],
            "recipientProvinceName": INFO['province_name'],
            "recipientCityId": INFO['city_id'],
            "recipientCityName": INFO['city_name'],
            "recipientCountyId": INFO['county_id'],
            "recipientCountyName": INFO['county_name'],
            "recipientAddress": INFO['detailed_address'],
            "expressType": 2,
            "addressId": INFO['camera_user_address_pj_id'],
            "inspectionCenterId": INFO['check_the_center_id'],
            "inspectionCenterCode": INFO['merchant_id'],
            "inspectionCenterName": INFO['check_the_center_name'],
            "returnGoodsItem": [
                {
                    "returnOrderNo": res[0]['afterOrderNo'],
                    "articlesNo": obj
                }
            ]
        }
        return self._make_request('post', 'ML8Yeu3JI', data, 'main', nocheck)

    @doc(TNLKcCWf408wxkwt8y53)
    @BaseApi.timing_decorator
    def TNLKcCWf408wxkwt8y53(self, nocheck=False):
        res = self.pc.YBoIFlRaGyVtfzeObzsmf(i=1)
        obj = res[0]['articlesNo']
        ParamCache.cache_object({"articlesNo": obj}, 'practical.json')
        data = {
            "childType": 3,
            "addressId": INFO['camera_user_address_pj_id'],
            "inspectionCenterId": INFO['check_the_center_id'],
            "inspectionCenterCode": INFO['merchant_id'],
            "inspectionCenterName": INFO['check_the_center_name'],
            "returnGoodsItem": [
                {
                    "returnOrderNo": res[0]['afterOrderNo'],
                    "articlesNo": obj
                }
            ]
        }
        return self._make_request('post', 'ML8Yeu3JI', data, 'main', nocheck)


class ADixIQYwld(InitializeParams):
    """运营中心|壹准拍机|售后管理|售后订单"""

    @doc(nAYT9Iv7RAHKUiNICWDZ)
    @BaseApi.timing_decorator
    def nAYT9Iv7RAHKUiNICWDZ(self, nocheck=False):
        res = self.pc.CO4AXsbHeeFE7zOfrBooq(i=['1'])
        data = {
            "id": res[0]['id'],
            "refundAmount": 1,
            "auditInfo": {
                "auditResult": 1,
                "handleMode": 1
            },
            "auditType": 1
        }
        return self._make_request('post', 'Ka0Hquwaf', data, 'main', nocheck)

    @doc(nt1WLIYZKQBXObcXSO3i)
    @BaseApi.timing_decorator
    def nt1WLIYZKQBXObcXSO3i(self, nocheck=False):
        res = self.pc.CO4AXsbHeeFE7zOfrBooq(i=['11'])
        data = {
            "id": res[0]['id'],
            "refundAmount": 1,
            "auditInfo": {
                "auditResult": 1,
                "handleMode": 1
            },
            "auctionAfterSalesOrderReason": {
                "qualityInspectionReportList": []
            },
            "auditType": 2
        }
        return self._make_request('post', 'Ka0Hquwaf', data, 'main', nocheck)

    @doc(ZZ2zZAyUsP0T3BsHmyIR)
    @BaseApi.timing_decorator
    def ZZ2zZAyUsP0T3BsHmyIR(self, nocheck=False):
        res = self.pc.CO4AXsbHeeFE7zOfrBooq(i=['11'])
        data = {
            "id": res[0]['id'],
            "refundAmount": 1,
            "auditInfo": {
                "auditResult": 1,
                "handleMode": 1
            },
            "auctionAfterSalesOrderReason": {
                "qualityInspectionReportList": []
            },
            "auditType": 2
        }
        return self._make_request('post', 'Ka0Hquwaf', data, 'main', nocheck)

    @doc(yCDOX9xAevVaoqLEO8Xh)
    @BaseApi.timing_decorator
    def yCDOX9xAevVaoqLEO8Xh(self, nocheck=False):
        res = self.pc.CO4AXsbHeeFE7zOfrBooq(i=['1'])
        data = {
            "id": res[0]['id'],
            "refundAmount": 1,
            "auditInfo": {
                "auditResult": 1,
                "handleMode": 2
            },
            "auditType": 1
        }
        return self._make_request('post', 'Ka0Hquwaf', data, 'main', nocheck)

    @doc(Om4GtulmnevZNOlqppff)
    @BaseApi.timing_decorator
    def Om4GtulmnevZNOlqppff(self, nocheck=False):
        res = self.pc.CO4AXsbHeeFE7zOfrBooq(i=['11'])
        data = {
            "id": res[0]['id'],
            "refundAmount": 1,
            "auditInfo": {
                "auditResult": 1,
                "handleMode": 2
            },
            "auctionAfterSalesOrderReason": {
                "qualityInspectionReportList": []
            },
            "auditType": 2
        }
        return self._make_request('post', 'Ka0Hquwaf', data, 'main', nocheck)

    @doc(o8uJrB3BoBE3UlDBpUhK)
    @BaseApi.timing_decorator
    def o8uJrB3BoBE3UlDBpUhK(self, nocheck=False):
        res = self.pc.CO4AXsbHeeFE7zOfrBooq(i=['11'])
        data = {
            "id": res[0]['id'],
            "refundAmount": 1,
            "auditInfo": {
                "auditResult": 1,
                "handleMode": 2
            },
            "auctionAfterSalesOrderReason": {
                "qualityInspectionReportList": []
            },
            "auditType": 2
        }
        return self._make_request('post', 'Ka0Hquwaf', data, 'main', nocheck)

    @doc(SLVYtmn8n4nMwNGpeuK5)
    @BaseApi.timing_decorator
    def SLVYtmn8n4nMwNGpeuK5(self, nocheck=False):
        for _ in range(2):
            time.sleep(1.5)
            self.pc.CO4AXsbHeeFE7zOfrBooq(i=['1'])
        res = self.pc.CO4AXsbHeeFE7zOfrBooq(i=['1'])
        data = {
            "id": res[0]['id'],
            "auditInfo": {
                "auditResult": 1,
                "handleMode": 3
            },
            "auditType": 1
        }
        return self._make_request('post', 'Ka0Hquwaf', data, 'main', nocheck)

    @doc(oUd1bU9wcVj8ujL9j9cI)
    @BaseApi.timing_decorator
    def oUd1bU9wcVj8ujL9j9cI(self, nocheck=False):
        res = self.pc.CO4AXsbHeeFE7zOfrBooq(i=['1'])
        data = {
            "id": res[0]['id'],
            "auditInfo": {
                "auditResult": 0,
                "auditDesc": "审核反馈",
                "imageVideoUrl": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com//erp-imgfiles/%2Fepbox-erp/20260205/WIehcT%2B7sg/I4FjLToJM%2Bw%3D%3D.jpg"
            },
            "auditType": 1
        }
        return self._make_request('post', 'Ka0Hquwaf', data, 'main', nocheck)

    @doc(m2P7xHJlv31GMBi1Qzjb)
    @BaseApi.timing_decorator
    def m2P7xHJlv31GMBi1Qzjb(self, nocheck=False):
        res = self.pc.KgbSrz63njmC8XfrU1jty(data='b')
        obj = res[0]['consignmentOrderNo']
        ParamCache.cache_object({"order_no": obj}, 'practical.json')
        data = {
            "reasonType": 1,
            "userId": INFO['main_user_id'],
            "consignmentReceiptStoreVOList": [
                {
                    "id": res[0]['id'],
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "erpArticlesNo": None,
                    "erpImei": None,
                    "articlesTypeId": 1,
                    "articlesTypeName": res[0]['articlesTypeName'],
                    "brandId": res[0]['brandId'],
                    "brandName": res[0]['brandName'],
                    "modelId": res[0]['modelId'],
                    "modelName": res[0]['modelName'],
                    "finenessId": res[0]['finenessId'],
                    "finenessName": res[0]['finenessName'],
                    "skuInfo": res[0]['skuInfo'],
                    "businessType": res[0]['businessType'],
                    "businessTypeStr": res[0]['businessTypeStr'],
                    "consignmentOrderNo": obj,
                    "tenantId": res[0]['tenantId'],
                    "tenantStr": res[0]['tenantStr'],
                    "inspectionCenterId": INFO['check_the_center_id'],
                    "inspectionCenterCode": INFO['merchant_id'],
                    "inspectionCenterName": INFO['check_the_center_name'],
                    "expressNo": None,
                    "auctionAfterSales": True
                }
            ],
            "orderVideoItemDTOList": [
                {
                    "videoUrl": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com/erp-video/1770345760570.mp4",
                    "orderNo": obj,
                    "videoName": "收货视频01"
                }
            ],
            "auctionAfterSales": True
        }
        return self._make_request('post', 'q6kIpVZXv', data, 'main', nocheck)

    @doc(hjEKlIzRRSYkSa8yshVM)
    @BaseApi.timing_decorator
    def hjEKlIzRRSYkSa8yshVM(self, nocheck=False):
        res = self.pc.KgbSrz63njmC8XfrU1jty(data='b')
        obj = res[0]['consignmentOrderNo']
        ParamCache.cache_object({"order_no": obj}, 'practical.json')
        data = {
            "reasonType": 1,
            "userId": INFO['main_user_id'],
            "consignmentReceiptStoreVOList": [
                {
                    "id": res[0]['id'],
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "erpArticlesNo": None,
                    "erpImei": None,
                    "articlesTypeId": 1,
                    "articlesTypeName": res[0]['articlesTypeName'],
                    "brandId": res[0]['brandId'],
                    "brandName": res[0]['brandName'],
                    "modelId": res[0]['modelId'],
                    "modelName": res[0]['modelName'],
                    "finenessId": res[0]['finenessId'],
                    "finenessName": res[0]['finenessName'],
                    "skuInfo": res[0]['skuInfo'],
                    "businessType": res[0]['businessType'],
                    "businessTypeStr": res[0]['businessTypeStr'],
                    "consignmentOrderNo": obj,
                    "tenantId": res[0]['tenantId'],
                    "tenantStr": res[0]['tenantStr'],
                    "userId": res[0]['userId'],
                    "inspectionCenterId": INFO['check_the_center_id'],
                    "inspectionCenterCode": INFO['merchant_id'],
                    "expressNo": None,
                    "auctionAfterSales": True
                }
            ],
            "orderVideoItemDTOList": [
                {
                    "videoUrl": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com/erp-video/1770345760570.mp4",
                    "orderNo": obj,
                    "videoName": "收货视频01"
                }
            ],
            "auctionAfterSales": True
        }
        return self._make_request('post', 'q6kIpVZXv', data, 'main', nocheck)


class BCCqGPByjj(InitializeParams):
    """运营中心|壹准拍机|售后管理|售后退货管理"""


if __name__ == '__main__':
    api = ()
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
