# coding: utf-8
import json
import random
from common.base_api import BaseApi
from common.base_params import InitializeParams, is_performance_close
from common.import_desc import *
from config.user_info import INFO


class RepairAuditListRequest(InitializeParams):
    """维修管理|维修审核列表"""

    @doc(r_the_maintenance_audit_passed)
    @BaseApi.timing_decorator
    def the_maintenance_audit_passed(self, nocheck=False):
        res = self.pc.repair_review_list_data(i=1)
        data = {
            "auditStatus": "2",
            "auditRemark": self.serial,
            "id": res[0]['id']
        }

        return self._make_request('post', 'repair_review_submission', data, 'main', nocheck)

    @doc(r_audit_rejection)
    @BaseApi.timing_decorator
    def audit_rejection(self, nocheck=False):
        res = self.pc.repair_review_list_data(i=1)
        data = {
            "auditStatus": "3",
            "auditRemark": self.serial,
            "id": res[0]['id']
        }
        return self._make_request('post', 'repair_review_submission', data, 'main', nocheck)


class RepairCentreItemRequest(InitializeParams):
    """维修管理|维修中物品"""

    @doc(r_submit_the_maintenance_results)
    @BaseApi.timing_decorator
    def submit_the_maintenance_results(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='7')
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
        return self._make_request('post', 'submit_the_maintenance_results', data, 'main', nocheck)

    @doc(r_purpose_of_transfer_repair)
    @BaseApi.timing_decorator
    def purpose_of_transfer_repair(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='7')
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
        return self._make_request('post', 'submit_the_maintenance_results', data, 'main', nocheck)

    @doc(r_purpose_of_transfer_sales)
    @BaseApi.timing_decorator
    def purpose_of_transfer_sales(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='7')
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
        return self._make_request('post', 'submit_the_maintenance_results', data, 'main', nocheck)

    @doc(r_unrepaired_handover)
    @BaseApi.timing_decorator
    def unrepaired_handover(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='7')
        data = {
            "type": "6",
            "userId": INFO['idle_user_id'],
            "articlesNoList": [
                res[0]['articlesNo']
            ],
            "createBy": INFO['customer_name']
        }
        return self._make_request('post', 'item_inventory_transfer', data, 'main', nocheck)

    @doc(r_add_accessories_submit_repair_results)
    @BaseApi.timing_decorator
    def add_accessories_submit_repair_results(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='7')
        res_2 = self.pc.attachment_inventory_list_data(i='2')
        res_3 = self.pc.repair_project_list_data()
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
        return self._make_request('post', 'submit_the_maintenance_results', data, 'main', nocheck)

    @doc(r_submit_maintenance_and_disassembly_parts)
    @BaseApi.timing_decorator
    def submit_maintenance_and_disassembly_parts(self, nocheck=False):
        res = self.pc.inventory_list_data(i='2', j='7')
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
        return self._make_request('post', 'item_disassembly_submission', data, 'main', nocheck)


class RepairProjectListRequest(InitializeParams):
    """维修管理|维修项目列表"""

    @doc(r_new_maintenance_items_iphone)
    @BaseApi.timing_decorator
    def new_maintenance_items_iphone(self, nocheck=False):
        res = self.pc.repair_project_list_data(i=1)
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
        return self._make_request('post', 'project_list_add', data, 'idle', nocheck)

    @doc(r_add_maintenance_items_flat)
    @BaseApi.timing_decorator
    def add_maintenance_items_flat(self, nocheck=False):
        res = self.pc.repair_project_list_data()
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
        return self._make_request('post', 'project_list_add', data, 'idle', nocheck)

    @doc(r_add_maintenance_items_book)
    @BaseApi.timing_decorator
    def add_maintenance_items_book(self, nocheck=False):
        res = self.pc.repair_project_list_data()
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
        return self._make_request('post', 'project_list_add', data, 'idle', nocheck)

    @doc(r_add_maintenance_items_watch)
    @BaseApi.timing_decorator
    def add_maintenance_items_watch(self, nocheck=False):
        res = self.pc.repair_project_list_data()
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
        return self._make_request('post', 'project_list_add', data, 'idle', nocheck)

    @doc(r_editor_maintenance_items)
    @BaseApi.timing_decorator
    def editor_maintenance_items(self, nocheck=False):
        res = self.pc.repair_project_list_data()
        data = {
            "name": res['tableData'][0]['name'],
            "defaultPrice": 0,
            "id": res['tableData'][0]['id'],
            "categoryId": res['tableData'][0]['typeId'],
        }
        return self._make_request('put', 'project_list_edit', data, 'idle', nocheck)

    @doc(r_delete_maintenance_items)
    @BaseApi.timing_decorator
    def delete_maintenance_items(self, nocheck=False):
        res = self.pc.repair_project_list_data()
        data = [
            res['tableData'][0]['id'],
        ]
        return self._make_request('put', 'project_list_delete', data, 'idle', nocheck)

    @doc(r_new_model_configuration)
    @BaseApi.timing_decorator
    def new_model_configuration(self, nocheck=False):
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
        return self._make_request('post', 'added_model_config', data, 'idle', nocheck)


if __name__ == '__main__':
    api = None
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
