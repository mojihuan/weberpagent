# coding: utf-8
import json
from common.base_api import BaseApi


class QualityCentreItemApi(BaseApi):
    """质检管理|质检中物品"""

    def quality_centre_item(self, headers=None, num=1, size=1000):
        """质检中物品"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['quality_centre_item'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class QualityContentTemplateApi(BaseApi):
    """质检管理|质检内容模版"""

    def content_template(self, headers=None):
        """质检内容模版"""
        headers = headers or self.headers['idle']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['quality_content_template'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class QualityCountApi(BaseApi):
    """质检管理|质检统计数据"""

    def count_list(self, headers=None):
        """质检统计数据"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "erpStartTime": self.get_the_date(-14), "erpEndTime": self.get_the_date()}
        response = self.request_handle('post', self.urls['quality_count'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class QualityRecordListApi(BaseApi):
    """质检管理|质检记录列表"""

    def quality_record_list(self, headers=None):
        """质检记录列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['quality_record_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class QualityStaticsApi(BaseApi):
    """质检管理|质检统计数据"""

    def quality_statics_list(self, headers=None):
        """质检统计数据"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['quality_statics'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class QualityStoreApi(BaseApi):
    """质检管理|先质检后入库"""

    def quality_store_list(self, headers=None, i=None, num=1, size=1000):
        """非库内物品列表
        i: 1人工选择 2壹准验机app
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'type': i}
        response = self.request_handle('post', self.urls['quality_check_and_stock'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def quality_inspection_list(self, headers=None, num=1, size=1000):
        """非库内质检记录列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['no_quality_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class QualityTemplatesApi(BaseApi):
    """质检管理|质检模版管理"""

    def content_template(self, headers=None):
        """质检模版管理"""
        headers = headers or self.headers['idle']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['quality_template'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class QualityWaitReceiveApi(BaseApi):
    """质检管理|待接收物品"""

    def wait_turn_over_list(self, headers=None):
        """待接收物品列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "articlesState": 4, "articlesType": "1"}
        response = self.request_handle('post', self.urls['wait_turn_over'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res

    # 获取物品编号
    def get_list_articles_no(self):
        return self._get_field_copy_value('wait_turn_over_list', 'main', 'articlesNo')


class QualityWaitTurnOverApi(BaseApi):
    """质检管理|待移交物品"""

    def wait_turn_over_list(self, headers=None, num=1, size=1000):
        """待移交物品列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['wait_turn_over'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = None
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
