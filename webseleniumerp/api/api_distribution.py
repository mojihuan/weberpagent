# coding: utf-8
import json
from common.base_api import BaseApi


class DistributionListApi(BaseApi):
    """分销管理|分销商管理"""

    def distributor_list(self, headers=None):
        """分销商管理"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['distributor_management'], data=json.dumps(data),      headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class DistributionOrdersApi(BaseApi):
    """分销管理|分销商业绩"""

    def distribution_orders_list(self, headers=None):
        """分销商业绩"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['distributor_performance_list'], data=json.dumps(data),  headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = None
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
