# coding: utf-8
import json
from common.base_api import BaseApi
from config.user_info import INFO


class RepairItemsApi(BaseApi):
    """维修管理|已维修物品"""

    def repair_items(self, headers=None, num=1, size=1000):
        """已维修物品列表"""
        headers = headers or self.headers['main']
        data = {'repairEndTime': self.get_the_date(), 'repairStartTime': self.get_the_date(),
                **self.get_page_params(num, size), 'statusList': ['3', '4']}
        response = self.request_handle('post', self.urls['repair_items'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def repair_record(self, headers=None):
        """维修记录"""
        headers = headers or self.headers['main']
        articles_no = self.get_articles_no()
        data = {'articlesNo': articles_no}
        response = self.request_handle('post', self.urls['repair_record'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    # 获取物品编号
    def get_articles_no(self):
        return self._get_field_copy_value('repair_items', 'main', 'articlesNo')


class RepairListApi(BaseApi):
    """维修管理|维修中物品列表"""

    def project_list(self, headers=None, num=1, size=1000):
        """维修中物品列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['list_of_items_under_repair'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class RepairPartsManageApi(BaseApi):
    """维修管理|拆件管理"""

    def parts_manage_list(self, headers=None):
        """拆件管理列表-按单据"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['parts_manage'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def detail_list(self, headers=None):
        """拆件管理列表-按明细"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['parts_detail_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class RepairProjectListApi(BaseApi):
    """维修管理|维修项目列表"""

    def project_list(self, i=None, headers=None):
        """维修项目列表
         i: 品类 1手机 2平板 3电脑 4手表

        """
        headers = headers or self.headers['main']
        data = {'articlesTypeId': i}
        response = self.request_handle('post', self.urls['repair_project_list'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)

    def model_list(self, i=None, headers=None):
        """机型配置列表
         i: 品类 1手机 3平板 4电脑 5手表

        """
        headers = headers or self.headers['main']
        data = {'articlesTypeId': i}
        response = self.request_handle('post', self.urls['repair_model_list'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)


class RepairReceiveApi(BaseApi):
    """维修管理|待接收物品"""

    def repair_wait_receive(self, headers=None):
        """待接收物品"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "articlesState": 6, "articlesType": "1"}
        response = self.request_handle('post', self.urls['accessory_receive_items'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res

    def repair_wait_receive_attachment(self, headers=None):
        """待接收配件"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "articlesState": 18, "articlesType": "2"}
        response = self.request_handle('post', self.urls['warehousing_receive_items'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res

    # 获取物品编号
    def get_list_articles_no(self):
        return self._get_field_copy_value('repair_wait_receive', 'main', 'articlesNo')


class RepairReviewListApi(BaseApi):
    """维修管理|维修审核列表"""

    def repair_audit_list(self, i=None, headers=None, num=1, size=1000):
        """维修审核列表
         i：审核状态 1待审核 2已通过 3未通过

        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'statusList': ['3', '4'], 'auditStatus': i}
        response = self.request_handle('post', self.urls['repair_review_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class RepairStaticsListApi(BaseApi):
    """维修管理-维修数据统计"""

    def get_list(self, headers=None):
        """维修数据统计"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "statusList": ["3", "4"], "userId": INFO['main_user_id']}
        response = self.request_handle('post', self.urls['repair_statics_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = None
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
