# coding: utf-8
import json
from common.base_api import BaseApi


class DetectCustomDetectionApi(BaseApi):
    """壹准验机管理|自定义检测列表"""

    def custom_detection_list(self, headers=None):
        """自定义检测列表"""
        headers = headers or self.headers['main']
        data = {"level": 0, **self.get_page_params()}
        response = self.request_handle('post', self.urls['custom_detection'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res


class DetectListOfModelsApi(BaseApi):
    """壹准验机管理|机型列表"""

    def list_of_models_list(self, headers=None):
        """机型列表"""
        headers = headers or self.headers['main']
        data = {"machineDetectionSwitch": 2, "total": 0, **self.get_page_params()}
        response = self.request_handle('post', self.urls['list_of_models'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class DetectInspectionManageApi(BaseApi):
    """壹准验机管理|检测管理"""

    def inspection_manage_list(self, headers=None):
        """检测管理列表"""
        headers = headers or self.headers['main']
        data = {"templateId": 97}
        response = self.request_handle('post', self.urls['inspection_manage'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res


class DetectQualityOrdersListApi(BaseApi):
    """壹准验机管理|质检订单列表"""

    def quality_orders_list(self, headers=None):
        """质检订单列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['quality_orders_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class DetectQualityReportExportedApi(BaseApi):
    """壹准验机管理|质检报告导出"""

    def quality_report_exported_list(self, headers=None):
        """质检报告导出列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "erpStartTime": self.get_the_date(-30), "erpEndTime": self.get_the_date()}
        response = self.request_handle('post', self.urls['quality_report_exported'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = DetectInspectionManageApi()
    result = api.inspection_manage_list()
    print(json.dumps(result, indent=4, ensure_ascii=False))
