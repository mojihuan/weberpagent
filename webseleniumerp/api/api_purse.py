# coding: utf-8
import json
from common.base_api import BaseApi


class PurseWalletCenterApi(BaseApi):
    """钱包管理|钱包中心"""

    def wallet_center(self, headers=None):
        """钱包中心"""
        headers = headers or self.headers['main']
        data = {'orderStatus': 2, **self.get_page_params()}
        response = self.request_handle('post', self.urls['wallet_center_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    # 获取钱包账号id
    def get_account_no(self):
        return self._get_field_copy_value('wallet_center', 'main', 'accountNo')

    # 获取钱包账号id
    def get_account_no_vice(self):
        return self._get_field_copy_value('wallet_center', 'vice', 'accountNo')


class PurseWalletOrderListApi(BaseApi):
    """钱包管理|钱包订单列表"""

    def pending_payment(self, headers=None):
        """钱包订单列表-待付款"""
        headers = headers or self.headers['main']
        data = {'orderStatus': 1, **self.get_page_params()}
        response = self.request_handle('post', self.urls['wallet_order_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def confirm_to_the_payment(self, headers=None):
        """钱包订单列表-确认到款中"""
        headers = headers or self.headers['main']
        data = {'orderStatus': 2, **self.get_page_params()}
        response = self.request_handle('post', self.urls['wallet_order_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = None
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
