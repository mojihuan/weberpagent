# coding: utf-8
import json
import time
from common.base_api import BaseApi
from common.base_params import InitializeParams, is_performance_close
from common.file_cache_manager import ParamCache
from common.import_desc import *
from config.user_info import INFO

qualityCategoryList = BaseApi.load_json_file('request_fulfillment.json')['qualityCategoryList']
optionIdList = BaseApi.load_json_file('request_fulfillment.json')['optionIdList']
backfillList = BaseApi.load_json_file('request_fulfillment.json')['backfillList']


class FulfillmentItemItemToBeQuotedRequest(InitializeParams):
    """运营中心|待报价物品"""

    @doc(f_commodity_quotes)
    @BaseApi.timing_decorator
    def commodity_quotes(self, nocheck=False):
        res = self.pc.fulfillment_items_to_be_quoted_data()
        data = {
            "reportAmount": self.number,
            "id": res[-1]['id']
        }
        return self._make_request('post', 'quoted_items', data, 'main', nocheck)

    @doc(f_requote)
    @BaseApi.timing_decorator
    def requote(self, nocheck=False):
        res = self.pc.fulfillment_items_to_be_quoted_data()
        data = {
            "reportAmount": self.number,
            "id": res[0]['id']
        }
        return self._make_request('post', 'quoted_items', data, 'main', nocheck)


class FulfillmentQualityManageRequest(InitializeParams):
    """运营中心|质检管理"""

    @doc(f_receive_items_in_bulk)
    @BaseApi.timing_decorator
    def receive_items_in_bulk(self, nocheck=False):
        res = self.pc.fulfillment_quality_manage_data()
        data = {
            "distributorIds": [
                res[0]['id']
            ]
        }
        return self._make_request('post', 'receive_in_batches', data, 'main', nocheck)

    @doc(f_direct_platform_review_receive_in_batches)
    @BaseApi.timing_decorator
    def direct_platform_review_receive_in_batches(self, nocheck=False):
        res = self.pc.fulfillment_quality_manage_data()
        data = {
            "distributorIds": [
                res[0]['id']
            ]
        }
        return self._make_request('post', 'receive_in_batches', data, 'main', nocheck)

    @doc(f_direct_shot_physical_re_inspection_received)
    @BaseApi.timing_decorator
    def direct_shot_physical_re_inspection_received(self, nocheck=False):
        res = self.pc.fulfillment_quality_manage_data()
        data = {
            "distributorIds": [
                res[0]['id']
            ]
        }
        return self._make_request('post', 'receive_in_batches', data, 'main', nocheck)

    @doc(f_quality_receive_items_in_bulk)
    @BaseApi.timing_decorator
    def quality_receive_items_in_bulk(self, nocheck=False):
        res = self.pc.fulfillment_quality_manage_data()
        data = {
            "distributorIds": [
                res[0]['id']
            ]
        }
        return self._make_request('post', 'receive_in_batches', data, 'main', nocheck)

    @doc(f_submit_the_quality_inspection_results)
    @BaseApi.timing_decorator
    def submit_the_quality_inspection_results(self, nocheck=False):
        self.wait_default()
        res = self.pc.fulfillment_quality_manage_data(data='a')
        res_2 = self.pc.fulfillment_quality_manage_data(data='e')
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
        return self._make_request('post', 'yy_submit_quality_results', data, 'main', nocheck)

    @doc(f_direct_shot_of_the_real_thing_submit_quality)
    @BaseApi.timing_decorator
    def direct_shot_of_the_real_thing_submit_quality(self, nocheck=False):
        self.wait_default()
        res = self.pc.fulfillment_quality_manage_data(data='a')
        res_2 = self.pc.fulfillment_quality_manage_data(data='e')
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
        return self._make_request('post', 'yy_submit_quality_results', data, 'main', nocheck)

    @doc(f_direct_platform_review_submit_quality)
    @BaseApi.timing_decorator
    def direct_platform_review_submit_quality(self, nocheck=False):
        self.wait_default()
        res = self.pc.fulfillment_quality_manage_data(data='a')
        res_2 = self.pc.fulfillment_quality_manage_data(data='e')
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
        return self._make_request('post', 'yy_submit_quality_results', data, 'main', nocheck)

    @doc(f_quality_submit_the_quality_inspection_results)
    @BaseApi.timing_decorator
    def quality_submit_the_quality_inspection_results(self, nocheck=False):
        self.wait_default()
        res = self.pc.fulfillment_quality_manage_data(data='a')
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
        return self._make_request('post', 'yy_submit_quality_results', data, 'main', nocheck)

    @doc(f_submit_the_quality_inspection_results_no)
    @BaseApi.timing_decorator
    def submit_the_quality_inspection_results_no(self, nocheck=False):
        self.wait_default()
        res = self.pc.fulfillment_quality_manage_data(data='a')
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
        return self._make_request('post', 'yy_submit_quality_results', data, 'main', nocheck)

    @doc(f_passed_the_re_inspection)
    @BaseApi.timing_decorator
    def passed_the_re_inspection(self, nocheck=False):
        res = self.pc.fulfillment_quality_manage_data(data='c')
        data = {
            "recheckId": res[0]['id'],
            "recheckStatus": "2",
            "reviewReason": "审核说明"
        }
        return self._make_request('post', 'approved_by_the_review', data, 'main', nocheck)

    @doc(f_rereview_rejected)
    @BaseApi.timing_decorator
    def rereview_rejected(self, nocheck=False):
        res = self.pc.fulfillment_quality_manage_data(data='c')
        data = {
            "recheckId": res[0]['id'],
            "recheckStatus": "3",
            "reviewReason": "审核说明"
        }
        return self._make_request('post', 'approved_by_the_review', data, 'main', nocheck)

    @doc(f_modify_the_report)
    @BaseApi.timing_decorator
    def modify_the_report(self, nocheck=False):
        res = self.pc.fulfillment_quality_manage_data(data='b')
        res_2 = self.pc.fulfillment_quality_manage_data(data='e')
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
        return self._make_request('post', 'modify_the_report', data, 'main', nocheck)

    @doc(f_unverified_handover)
    @BaseApi.timing_decorator
    def unverified_handover(self, nocheck=False):
        res = self.pc.fulfillment_quality_manage_data(data='a')
        data = {
            "reasonType": 1,
            "userId": INFO['main_user_id'],
            "qualityIds": [
                res[0]['id']
            ]
        }
        return self._make_request('post', 'unverified_handover', data, 'main', nocheck)

    @doc(f_not_quality)
    @BaseApi.timing_decorator
    def not_quality(self, nocheck=False):
        res = self.pc.fulfillment_quality_manage_data(data='a')
        data = {
            "qualityId": res[0]['id'],
            "reasonTypeList": [
                1,
                2
            ]
        }
        return self._make_request('post', 'not_quality', data, 'main', nocheck)

    @doc(f_product_image_shooting_and_uploading)
    @BaseApi.timing_decorator
    def product_image_shooting_and_uploading(self, nocheck=False):
        res = self.pc.fulfillment_quality_manage_data(data='d', i=1)
        data = {
            "articlesNo": res[0]['articlesNo'],
            "type": 1,
            "imageVideoUrls": [
                "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com/erp-video/1767608255124.jpeg"
            ]
        }
        return self._make_request('post', 'yy_product_image_shooting', data, 'main', nocheck)


class FulfillmentReturnsManageRequest(InitializeParams):
    """运营中心|退货管理"""

    @doc(f_return_to_the_warehouse)
    @BaseApi.timing_decorator
    def return_to_the_warehouse(self, nocheck=False):
        res = self.pc.fulfillment_returns_manage_data(data='a', i=1)
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
        return self._make_request('post', 'return_to_the_warehouse', data, 'main', nocheck)

    @doc(f_self_submitted_library)
    @BaseApi.timing_decorator
    def self_submitted_library(self, nocheck=False):
        res = self.pc.auction_my_data(data='a')
        data = [
            res['pickupCode']
        ]
        return self._make_request('post', 'self_submitted_library', data, 'main', nocheck)


class FulfillmentSignIntoTheLibraryRequest(InitializeParams):
    """运营中心|收货入库"""

    # 搜索订单号
    @BaseApi.timing_decorator
    def search_tracking_numbers(self, nocheck=False):
        res = self.pc.fulfillment_order_manage_data(i=3)
        data = {
            "consignmentOrderNo": res[0]['orderNo']
        }
        return self._make_request('post', 'search_tracking_numbers', data, 'main', nocheck)

    @doc(f_unpacking_and_receiving_goods_into_storage)
    @BaseApi.timing_decorator
    def unpacking_and_receiving_goods_into_storage(self, nocheck=False):
        res = self.pc.fulfillment_sign_into_the_library_data()
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
        return self._make_request('post', 'warehousing', data, 'main', nocheck)

    @doc(f_quality_inspection_upload_videos_for_storage)
    @BaseApi.timing_decorator
    def quality_inspection_upload_videos_for_storage(self, nocheck=False):
        res = self.pc.fulfillment_sign_into_the_library_data()
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
        return self._make_request('post', 'warehousing', data, 'main', nocheck)


class FulfillmentOrderManageRequest(InitializeParams):
    """运营中心|订单管理"""

    @doc(f_fast_guaranteed_items)
    @BaseApi.timing_decorator
    def fast_guaranteed_items(self, nocheck=False):
        res = self.pc.inventory_list_data(i=2, j=3)
        res_2 = self.pc.fulfillment_order_manage_data(data='a')
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
        return self._make_request('post', 'quick_guarantee_order', data, 'main', nocheck)


class FulfillmentItemsAreOutOfStorageRequest(InitializeParams):
    """运营中心|物品出库"""

    @doc(f_direct_shot_express_sales_out_of_the_warehouse)
    @BaseApi.timing_decorator
    def direct_shot_express_sales_out_of_the_warehouse(self, nocheck=False):
        for _ in range(2):
            time.sleep(1.5)
            self.pc.fulfillment_sales_and_shipment_manage_data(data='a')
        res = self.pc.fulfillment_sales_and_shipment_manage_data(data='a')
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
        return self._make_request('post', 'auction_sales_outbound', data, 'main', nocheck)

    @doc(f_direct_shot_jd_express_sales_out_of_the_warehouse)
    @BaseApi.timing_decorator
    def direct_shot_jd_express_sales_out_of_the_warehouse(self, nocheck=False):
        res = self.pc.fulfillment_sales_and_shipment_manage_data(data='a')
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
        return self._make_request('post', 'auction_sales_outbound', data, 'main', nocheck)

    @doc(f_direct_shooting_order_sales_out_of_the_warehouse)
    @BaseApi.timing_decorator
    def direct_shooting_order_sales_out_of_the_warehouse(self, nocheck=False):
        res = self.pc.fulfillment_sales_and_shipment_manage_data(data='a')
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
        return self._make_request('post', 'auction_sales_outbound', data, 'main', nocheck)

    @doc(f_direct_shooting_order_sales_out_of_the_warehouse_jd)
    @BaseApi.timing_decorator
    def direct_shooting_order_sales_out_of_the_warehouse_jd(self, nocheck=False):
        res = self.pc.fulfillment_sales_and_shipment_manage_data(data='a')
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
        return self._make_request('post', 'auction_sales_outbound', data, 'main', nocheck)

    @doc(f_direct_shooting_self_pick_up_and_sales)
    @BaseApi.timing_decorator
    def direct_shooting_self_pick_up_and_sales(self, nocheck=False):
        res = self.pc.bidding_my_data(i=3)
        data = {
            "sendType": "2",
            "buyTenantId": INFO['camera_merchant_id'],
            "saleArticlesNoList": [
                res[0]['articlesNo']
            ]
        }
        return self._make_request('post', 'auction_sales_outbound', data, 'main', nocheck)

    @doc(f_direct_sf_after_sales_delivery)
    @BaseApi.timing_decorator
    def direct_sf_after_sales_delivery(self, nocheck=False):
        res = self.pc.fulfillment_after_sales_return_manage_data(i=1)
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
        return self._make_request('post', 'after_sales_delivery', data, 'main', nocheck)

    @doc(f_direct_jd_after_sales_delivery)
    @BaseApi.timing_decorator
    def direct_jd_after_sales_delivery(self, nocheck=False):
        res = self.pc.fulfillment_after_sales_return_manage_data(i=1)
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
        return self._make_request('post', 'after_sales_delivery', data, 'main', nocheck)

    @doc(f_direct_zt_after_sales_delivery)
    @BaseApi.timing_decorator
    def direct_zt_after_sales_delivery(self, nocheck=False):
        res = self.pc.fulfillment_after_sales_return_manage_data(i=1)
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
        return self._make_request('post', 'after_sales_delivery', data, 'main', nocheck)


class FulfillmentAQuasiCameraRequest(InitializeParams):
    """运营中心|壹准拍机|售后管理|售后订单"""

    @doc(f_online_review_direct_shooting_passed)
    @BaseApi.timing_decorator
    def online_review_direct_shooting_passed(self, nocheck=False):
        res = self.pc.fulfillment_camera_after_sales_order_data(i=['1'])
        data = {
            "id": res[0]['id'],
            "refundAmount": 1,
            "auditInfo": {
                "auditResult": 1,
                "handleMode": 1
            },
            "auditType": 1
        }
        return self._make_request('post', 'camera_online_review', data, 'main', nocheck)

    @doc(f_direct_auction_review_refund_price_difference)
    @BaseApi.timing_decorator
    def direct_auction_review_refund_price_difference(self, nocheck=False):
        res = self.pc.fulfillment_camera_after_sales_order_data(i=['11'])
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
        return self._make_request('post', 'camera_online_review', data, 'main', nocheck)

    @doc(f_direct_platform_review_only_the_difference)
    @BaseApi.timing_decorator
    def direct_platform_review_only_the_difference(self, nocheck=False):
        res = self.pc.fulfillment_camera_after_sales_order_data(i=['11'])
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
        return self._make_request('post', 'camera_online_review', data, 'main', nocheck)

    @doc(f_the_direct_auction_price_difference_was_approved)
    @BaseApi.timing_decorator
    def the_direct_auction_price_difference_was_approved(self, nocheck=False):
        res = self.pc.fulfillment_camera_after_sales_order_data(i=['1'])
        data = {
            "id": res[0]['id'],
            "refundAmount": 1,
            "auditInfo": {
                "auditResult": 1,
                "handleMode": 2
            },
            "auditType": 1
        }
        return self._make_request('post', 'camera_online_review', data, 'main', nocheck)

    @doc(f_direct_shot_review_priority_spread)
    @BaseApi.timing_decorator
    def direct_shot_review_priority_spread(self, nocheck=False):
        res = self.pc.fulfillment_camera_after_sales_order_data(i=['11'])
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
        return self._make_request('post', 'camera_online_review', data, 'main', nocheck)

    @doc(f_direct_platform_review_priority_difference)
    @BaseApi.timing_decorator
    def direct_platform_review_priority_difference(self, nocheck=False):
        res = self.pc.fulfillment_camera_after_sales_order_data(i=['11'])
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
        return self._make_request('post', 'camera_online_review', data, 'main', nocheck)

    @doc(f_direct_shot_return_refund_approved)
    @BaseApi.timing_decorator
    def direct_shot_return_refund_approved(self, nocheck=False):
        for _ in range(2):
            time.sleep(1.5)
            self.pc.fulfillment_camera_after_sales_order_data(i=['1'])
        res = self.pc.fulfillment_camera_after_sales_order_data(i=['1'])
        data = {
            "id": res[0]['id'],
            "auditInfo": {
                "auditResult": 1,
                "handleMode": 3
            },
            "auditType": 1
        }
        return self._make_request('post', 'camera_online_review', data, 'main', nocheck)

    @doc(f_direct_shot_review_rejection)
    @BaseApi.timing_decorator
    def direct_shot_review_rejection(self, nocheck=False):
        res = self.pc.fulfillment_camera_after_sales_order_data(i=['1'])
        data = {
            "id": res[0]['id'],
            "auditInfo": {
                "auditResult": 0,
                "auditDesc": "审核反馈",
                "imageVideoUrl": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com//erp-imgfiles/%2Fepbox-erp/20260205/WIehcT%2B7sg/I4FjLToJM%2Bw%3D%3D.jpg"
            },
            "auditType": 1
        }
        return self._make_request('post', 'camera_online_review', data, 'main', nocheck)

    @doc(f_to_be_received_signature_into_the_library)
    @BaseApi.timing_decorator
    def to_be_received_signature_into_the_library(self, nocheck=False):
        res = self.pc.fulfillment_sign_into_the_library_data(data='b')
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
        return self._make_request('post', 'warehousing', data, 'main', nocheck)

    @doc(f_direct_platform_review_sign_into_the_library)
    @BaseApi.timing_decorator
    def direct_platform_review_sign_into_the_library(self, nocheck=False):
        res = self.pc.fulfillment_sign_into_the_library_data(data='b')
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
        return self._make_request('post', 'warehousing', data, 'main', nocheck)


class FulfillmentAfterSalesReturnManageRequest(InitializeParams):
    """运营中心|壹准拍机|售后管理|售后退货管理"""


if __name__ == '__main__':
    api = FulfillmentQualityManageRequest()
    result = api.quality_submit_the_quality_inspection_results()
    print(json.dumps(result, indent=4, ensure_ascii=False))
