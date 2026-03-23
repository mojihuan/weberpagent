# coding: utf-8
import json
from common.base_api import BaseApi
from config.user_info import INFO


class HelpGenerateOrderApi(BaseApi):
    """帮卖管理|帮卖上架列表"""

    def help_list_of_batches(self, headers=None):
        """帮卖上架列表 批次列表"""
        headers = headers or self.headers['main']
        data = {'entryType': 1, **self.get_page_params()}
        response = self.request_handle('post', self.urls['help_sell_listings'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def help_list_of_orders(self, i=None, headers=None):
        """帮卖上架列表 订单列表
         i：物品状态 wsg待发货 wtg待收货 rg已收货 wr待质检 wbi待议价 wb待确认 ws待结算 wrg待退机 rig退机中 wsr待售出
        """
        headers = headers or self.headers['main']
        data = {'entryType': 1, **self.get_page_params(), 'batchState': i}
        response = self.request_handle('post', self.urls['list_of_orders'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def initiate_a_list_of_helpers(self, headers=None):
        """发起帮卖列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'helpSellTenantId': INFO['main_help_sell_tenant_id']}
        response = self.request_handle('post', self.urls['initiate_a_list_of_helpers'], data=json.dumps(data),  headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class HelpSellTheListOfGoodsApi(BaseApi):
    """帮卖管理|帮卖来货列表"""

    def help_incoming_goods_list(self, headers=None):
        """帮卖来货 订单列表"""
        headers = headers or self.headers['vice']
        data = {'entryType': 2, **self.get_page_params()}
        response = self.request_handle('post', self.urls['help_incoming_goods'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def help_batch_no_list(self, headers=None):
        """帮卖来货 批次列表"""
        headers = headers or self.headers['vice']
        data = {'entryType': 2, **self.get_page_params()}
        response = self.request_handle('post', self.urls['batch_no_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    # 获取采购物品编号
    def get_help_sell_articles_no(self):
        return self._get_field_copy_value('help_incoming_goods_list', 'vice', 'helpSellArticlesNo')


class HelpServiceConfigurationApi(BaseApi):
    """帮卖管理|帮卖业务配置"""

    def service_configuration(self, headers=None):
        """帮卖业务配置"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['service_configuration'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    # 获取帮卖id
    def get_merchant_code(self):
        return self._get_field_copy_value('service_configuration', 'vice', 'merchantCode')


if __name__ == '__main__':
    api = HelpGenerateOrderApi()
    result = api.help_list_of_orders(i='wsg')
    print(json.dumps(result, indent=4, ensure_ascii=False))

