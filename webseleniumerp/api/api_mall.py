# coding: utf-8
import json
from common.base_api import BaseApi

class MallAftermarketListApi(BaseApi):
    """商城管理|售后列表"""

    def sales_list(self, headers=None):
        """售后列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['commodity_sales_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class MallBranchManageApi(BaseApi):
    """商城管理|网点管理"""

    def branch_manage_list(self, headers=None):
        """网点管理"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['commodity_branch_manage'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class MallCommodityManageApi(BaseApi):
    """商城管理|商品管理"""

    def commodity_manage(self, headers=None):
        """商品管理 1上架中 2已销售 3已下架 4已退回"""
        headers = headers or self.headers['main']
        data = {'articlesState': 1, **self.get_page_params(), 'statusList': ['3', '4']}
        response = self.request_handle('post', self.urls['commodity_manage_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = None
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
