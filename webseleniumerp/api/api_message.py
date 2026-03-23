# coding: utf-8
import json
from common.base_api import BaseApi


class MessageCenterApi(BaseApi):
    """消息管理|消息中心"""

    def system_msg(self, headers=None):
        """回收商发布"""
        headers = headers or self.headers['main']
        data = {"messageParentClass": "1", **self.get_page_params()}
        response = self.request_handle('post', self.urls['message_center'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def goods_trade(self, headers=None):
        """商品交易"""
        headers = headers or self.headers['main']
        data = {"messageParentClass": "2", **self.get_page_params()}
        response = self.request_handle('post', self.urls['message_center'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def push_list(self, headers=None):
        """推送公告"""
        headers = headers or self.headers['main']
        data = {"messageParentClass": "3", **self.get_page_params()}
        response = self.request_handle('post', self.urls['message_center'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class MessageReleaseListApi(BaseApi):
    """消息管理|消息发布列表"""

    def release_list(self, headers=None):
        """消息发布列表"""
        headers = headers or self.headers['main']
        data = {"selectType": "2", **self.get_page_params()}
        response = self.request_handle('post', self.urls['message_release_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def msg_records(self, headers=None):
        """消息发送记录"""
        headers = headers or self.headers['main']
        data = {"selectType": "1", **self.get_page_params()}
        response = self.request_handle('post', self.urls['message_release__records'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = None
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
