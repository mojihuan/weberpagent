# coding: utf-8
import json
from common.base_api import BaseApi


class SendBeenSentRepairApi(BaseApi):
    """送修管理|已送修物品"""

    def send_been_sent_repair(self, headers=None, num=1, size=1000):
        """已送修物品"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['send_been_sent_repair'], data=json.dumps(data),  headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class SendListOfRepairOrdersApi(BaseApi):
    """送修管理|送修单列表"""

    def send_list(self, headers=None, num=1, size=1000):
        """送修单列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['list_of_repair_orders'], data=json.dumps(data),   headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class SendStayRepairApi(BaseApi):
    """送修管理|送修单列表"""

    def send_list(self, headers=None, num=1, size=1000):
        """送修单列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['wait_send_repair'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class SendWaitReceiveApi(BaseApi):
    """送修管理|待接收物品"""

    def send_list(self, headers=None):
        """待接收物品"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['wait_receive'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)

    # 获取物品编号
    def get_list_articles_no(self):
        return self._get_field_copy_value('send_list', 'main', 'articlesNo')


if __name__ == '__main__':
    api = SendBeenSentRepairApi()
    result = api.send_been_sent_repair()
    print(json.dumps(result, indent=4, ensure_ascii=False))
