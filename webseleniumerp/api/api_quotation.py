# coding: utf-8
import json
from common.base_api import BaseApi


class QuotationBaseListApi(BaseApi):
    """报价管理|基础保价单"""

    def base_list(self, headers=None):
        """基础保价单"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['base_quotation'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class QuotationConfigurationApi(BaseApi):
    """报价管理|报价配置"""

    def config_list(self, headers=None):
        """报价配置"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(size=99999)}
        response = self.request_handle('post', self.urls['configuration'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class QuotationMyListApi(BaseApi):
    """报价管理|我的保价单"""

    def base_list(self, headers=None):
        """我的保价单"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['my_quotation'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class QuotationRecordsListApi(BaseApi):
    """报价管理|报价记录"""

    def record_list(self, headers=None):
        """报价记录"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['records_quotation'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = None
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
