# coding: utf-8
import json
from common.base_api import BaseApi
from config.user_info import INFO


class PurkQXBjQXG3tz8hUb1SF(BaseApi):
    """帮卖管理|帮卖上架列表"""

    def WCyqKh1Jrosc(self, headers=None):
        """帮卖上架列表 批次列表"""
        headers = headers or self.headers['main']
        data = {'entryType': 1, **self.get_page_params()}
        response = self.request_handle('post', self.urls['II5MugGsC'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def l6TOXA4JkEjO(self, i=None, headers=None):
        """帮卖上架列表 订单列表
         i：物品状态 wsg待发货 wtg待收货 rg已收货 wr待质检 wbi待议价 wb待确认 ws待结算 wrg待退机 rig退机中 wsr待售出
        """
        headers = headers or self.headers['main']
        data = {'entryType': 1, **self.get_page_params(), 'batchState': i}
        response = self.request_handle('post', self.urls['NQhtPXjZJ'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def gavz8010zhrA(self, headers=None):
        """发起帮卖列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'helpSellTenantId': INFO['main_help_sell_tenant_id']}
        response = self.request_handle('post', self.urls['VCrH1OtH2'], data=json.dumps(data),  headers=headers)
        return self.get_response_data(response, 'rows', list)


class Jc9Odo2T6JqvbWDRSsDXy(BaseApi):
    """帮卖管理|帮卖来货列表"""

    def vw76zdVHgk8Q(self, headers=None):
        """帮卖来货 订单列表"""
        headers = headers or self.headers['vice']
        data = {'entryType': 2, **self.get_page_params()}
        response = self.request_handle('post', self.urls['eTY0iqTUy'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def aOGxkzDL4EwQ(self, headers=None):
        """帮卖来货 批次列表"""
        headers = headers or self.headers['vice']
        data = {'entryType': 2, **self.get_page_params()}
        response = self.request_handle('post', self.urls['LLtmdLu67'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def yqJBX8AoDZGR(self):
        """获取采购物品编号"""
        return self._get_field_copy_value('vw76zdVHgk8Q', 'vice', 'helpSellArticlesNo')


class Ea7Wjr4ctTv69frbEUPZJ(BaseApi):
    """帮卖管理|帮卖业务配置"""

    def OUYQFhYf3krT(self, headers=None):
        """帮卖业务配置"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['aDl1NQwvp'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def NdHOKUMLaooD(self):
        """获取帮卖id"""
        return self._get_field_copy_value('OUYQFhYf3krT', 'vice', 'merchantCode')


if __name__ == '__main__':
    api = ()
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))

