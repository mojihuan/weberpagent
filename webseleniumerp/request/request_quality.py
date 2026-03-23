# coding: utf-8
import json
from common.base_api import BaseApi
from common.base_params import InitializeParams, is_performance_close
from common.import_desc import *
from config.user_info import INFO

qualityCategoryList = BaseApi.load_json_file('request_quality.json')['qualityCategoryList']
optionIdList = BaseApi.load_json_file('request_quality.json')['optionIdList']
backfillList = BaseApi.load_json_file('request_quality.json')['backfillList']


class QualityCentreItemRequest(InitializeParams):
    """质检管理|质检中物品"""

    @doc(q_submit_quality_results)
    @BaseApi.timing_decorator
    def submit_quality_results(self, nocheck=False):
        res = self.pc.quality_centre_item_data()
        data = {
            "presalePrice": "1000",
            "imageUrl": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com//erp-imgfiles/%2Fepbox-erp/20260206/WIehcT%2B7sg/I4FjLToJM%2Bw%3D%3D.jpg",
            "saleImageUrl": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com//erp-imgfiles/%2Fepbox-erp/20260206/WIehcT%2B7sg/I4FjLToJM%2Bw%3D%3D.jpg",
            "receiveId": INFO['special_user_id'],
            "type": "6",
            "deliveryRemark": "移交说明",
            "qualityCategoryList": qualityCategoryList,
            "articlesInfo": {
                "imei": res[0]['imei'],
                "brandName": res[0]['brandName'],
                "modelName": res[0]['modelName'],
                "modelId": res[0]['modelId'],
                "brandId": res[0]['brandId'],
                "serialNo": res[0]['platformArticlesNo'],
                "smallModelId": 72,
                "buyChannelId": 16,
                "colorId": 1712,
                "romId": 41,
                "ramId": None,
                "finenessId": 37,
                "machineTypeId": 862,
                "warrantyDurationId": 23005,
                "batteryHealthId": 23028,
                "finenessName": "充新",
                "colorName": "黑色钛金属",
                "romName": "256G",
                "buyChannelName": "国行",
                "smallModelName": "其他型号",
                "machineTypeName": "二手优品"
            },
            "articlesNo": res[0]['articlesNo'],
            "optionIdList": optionIdList,
            "createBy": INFO['main_account'],
            "templateId": 2,
            "isOther": 1
        }
        return self._make_request('post', 'submit_quality_results', data, 'main', nocheck)

    @doc(q_submit_quality_results_by_no_transfer)
    @BaseApi.timing_decorator
    def submit_quality_results_by_no_transfer(self, nocheck=False):
        res = self.pc.quality_centre_item_data()
        data = {
            "qualityCategoryList": qualityCategoryList,
            "articlesInfo": {
                "imei": res[0]['imei'],
                "brandName": res[0]['brandName'],
                "modelName": res[0]['modelName'],
                "modelId": res[0]['modelId'],
                "brandId": res[0]['brandId'],
                "serialNo": res[0]['platformArticlesNo'],
                "smallModelId": 72,
                "buyChannelId": 16,
                "colorId": 1712,
                "romId": 41,
                "ramId": None,
                "finenessId": "",
                "machineTypeId": 862,
                "warrantyDurationId": 23005,
                "batteryHealthId": 23028,
                "colorName": "黑色钛金属",
                "romName": "256G",
                "buyChannelName": "国行",
                "smallModelName": "其他型号",
                "machineTypeName": "二手优品"
            },
            "articlesNo": res[0]['articlesNo'],
            "optionIdList": optionIdList,
            "templateId": 2,
            "isOther": 1
        }
        return self._make_request('post', 'submit_quality_results', data, 'main', nocheck)

    @doc(q_unverified_handover)
    @BaseApi.timing_decorator
    def unverified_handover(self, nocheck=False):
        res = self.pc.quality_centre_item_data()
        data = {
            "type": "6",
            "userId": INFO['main_user_id'],
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "remark": "eee",
            "createBy": INFO['super_admin_account']
        }
        return self._make_request('post', 'item_inventory_transfer', data, 'main', nocheck)


class QualityContentTemplateRequest(InitializeParams):
    """质检管理|质检内容模版"""

    @doc(q_new_template_added)
    @BaseApi.timing_decorator
    def new_template_added(self, nocheck=False):
        data = {
            "qualityName": "质检内容名称" + self.imei,
            "isNormal": 0,
            "qualityContentOptionsDTOList": [
                {
                    "optionName": "分类名称一" + self.imei,
                    "optionType": 1,
                    "isDefault": 0
                },
                {
                    "optionName": "分类名称二" + self.imei,
                    "optionType": 2,
                    "isDefault": 0
                }
            ]
        }
        return self._make_request('post', 'new_template_added', data, 'idle', nocheck)

    @doc(q_editor_template)
    @BaseApi.timing_decorator
    def editor_template(self, nocheck=False):
        res = self.pc.quality_content_template_data()
        data = {
            "createBy": res[0]['createBy'],
            "createTime": res[0]['createTime'],
            "pageSize": 10,
            "pageNum": 1,
            "orderByColumn": "create_time",
            "isAsc": "desc",
            "id": res[0]['id'],
            "qualityName": res[0]['qualityName'],
            "optionsStr": res[0]['optionsStr'],
            "isNormal": 0,
            "qualityContentOptionsDTOList": [
                {
                    "optionName": "分类名称一" + self.serial,
                    "optionType": 1,
                    "isDefault": 0
                },
                {
                    "optionName": "分类名称二" + self.serial,
                    "optionType": 2,
                    "isDefault": 0
                }
            ]
        }
        return self._make_request('put', 'inspection_content_edit', data, 'idle', nocheck)

    @doc(q_delete_template)
    @BaseApi.timing_decorator
    def delete_template(self, nocheck=False):
        res = self.pc.quality_content_template_data()
        data = [
            res[0]['id']
        ]
        return self._make_request('post', 'inspection_content_delete', data, 'idle', nocheck)


class QualityGoodsReceivedRequest(InitializeParams):
    """质检管理|待接收物品"""


class QualityStoreRequest(InitializeParams):
    """质检管理|先质检后入库"""

    @doc(q_quality_artificial_add)
    @BaseApi.timing_decorator
    def quality_artificial_add(self, nocheck=False):
        data = {
            "presalePrice": "2000",
            "imageUrl": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com//erp-imgfiles/%2Fepbox-erp/20260206/WIehcT%2B7sg/I4FjLToJM%2Bw%3D%3D.jpg",
            "qualityCategoryList": qualityCategoryList,
            "articlesInfo": {
                "brandId": 1,
                "brandName": "苹果",
                "articlesTypeId": 1,
                "articlesReflection": "[0]",
                "articlesTypeName": "手机",
                "modelId": 17569,
                "modelName": "iPhone 16 Pro Max",
                "finenessId": 38,
                "imei": self.imei,
                "colorId": 1712,
                "colorName": "黑色钛金属",
                "smallModelId": 72,
                "smallModelName": "其他型号",
                "buyChannelId": 16,
                "buyChannelName": "国行",
                "machineTypeId": 862,
                "machineTypeName": "二手优品",
                "finenessName": "靓机",
                "romId": 41,
                "romName": "256G",
                "serialNo": self.serial
            },
            "saleImageUrl": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com//erp-imgfiles/%2Fepbox-erp/20260206/WIehcT%2B7sg/I4FjLToJM%2Bw%3D%3D.jpg",
            "isUpdateReport": False,
            "optionIdList": optionIdList,
            "templateId": 2,
            "isOther": 1
        }
        return self._make_request('post', 'quality_add', data, 'main', nocheck)


class QualityWaitTurnOverRequest(InitializeParams):
    """质检管理|待移交物品"""

    @doc(q_quality_inspection)
    @BaseApi.timing_decorator
    def quality_inspection(self, nocheck=False):
        res = self.pc.quality_wait_turn_over_data()
        data = {
            "articlesNo": "397526641408",
            "imageUrl": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com//erp-imgfiles/%2Fepbox-erp/20260206/WIehcT%2B7sg/I4FjLToJM%2Bw%3D%3D.jpg",
            "qualityCategoryList": qualityCategoryList,
            "articlesInfo": {
                "imei": res[0]['imei'],
                "brandName": res[0]['brandName'],
                "modelName": res[0]['modelName'],
                "modelId": res[0]['modelId'],
                "brandId": res[0]['brandId'],
                "serialNo": res[0]['platformArticlesNo'],
                "smallModelId": 72,
                "buyChannelId": 16,
                "colorId": 1712,
                "romId": 41,
                "machineTypeId": 862,
                "finenessId": 39,
                "finenessName": "小花",
                "colorName": "黑色钛金属",
                "romName": "256G",
                "buyChannelName": "国行",
                "smallModelName": "其他型号",
                "machineTypeName": "二手优品"
            },
            "saleImageUrl": "https://erp-imgfiles.oss-cn-hangzhou.aliyuncs.com//erp-imgfiles/%2Fepbox-erp/20260206/WIehcT%2B7sg/I4FjLToJM%2Bw%3D%3D.jpg",
            "backfillList": backfillList,
            "type": "6",
            "receiveId": INFO['main_user_id'],
            "deliveryRemark": "移交说明",
            "optionIdList": optionIdList,
            "createBy": INFO['main_account'],
            "templateId": 2,
            "isOther": 1
        }
        return self._make_request('post', 'submit_quality_results', data, 'main', nocheck)

    @doc(q_handover_inventory)
    @BaseApi.timing_decorator
    def handover_inventory(self, nocheck=False):
        res = self.pc.quality_wait_turn_over_data()
        data = {
            "type": "6",
            "userId": res[0]['userId'],
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "createBy": res[0]['createBy']
        }
        return self._make_request('post', 'item_inventory_transfer', data, 'main', nocheck)


if __name__ == '__main__':
    api = None
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
