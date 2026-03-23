# coding: utf-8
import json
from common.base_api import BaseApi
from common.base_params import InitializeParams, is_performance_close
from common.import_desc import *


class MessageReleaseListRequest(InitializeParams):
    """消息管理|消息发布列表"""

    @doc(m_publish_the_message)
    @BaseApi.timing_decorator
    def publish_the_message(self, nocheck=False):
        data = {
            "messageType": "1",
            "title": "消息标题",
            "content": "<p>消息内容</p>",
            "publishType": "1",
            "publishChannel": "1,2",
            "publishTimeType": "1",
            "selectType": "2",
            "addType": 2
        }
        return self._make_request('post', 'publish_the_message', data, 'main', nocheck)

    @doc(m_release_the_review_message)
    @BaseApi.timing_decorator
    def release_the_review_message(self, nocheck=False):
        data = {
            "messageType": "2",
            "title": "消息标题",
            "content": "<p>消息内容</p>",
            "publishType": "2",
            "publishChannel": "1,2",
            "publishTimeType": "1",
            "selectType": "2",
            "addType": 3
        }

        return self._make_request('post', 'release_the_review_message', data, 'main', nocheck)

    @doc(m_release_new_news_timed_release_time)
    @BaseApi.timing_decorator
    def release_new_news_timed_release_time(self, nocheck=False):
        data = {
            "messageType": "15",
            "title": "消息标题1",
            "content": "<p>1234</p>",
            "publishType": "1",
            "publishChannel": "1,2",
            "publishTimeType": "2",
            "scheduledPublishTime": self.get_formatted_datetime(days=1),
            "selectType": "2",
            "addType": 2
        }

        return self._make_request('post', 'publish_the_message', data, 'main', nocheck)

    @doc(m_release_new_news_save_the_draft)
    @BaseApi.timing_decorator
    def release_new_news_save_the_draft(self, nocheck=False):
        data = {
            "messageType": "6",
            "title": "消息标题1",
            "content": "<p>123</p>",
            "publishType": "1",
            "publishChannel": "1",
            "publishTimeType": "1",
            "selectType": "2",
            "addType": 1
        }
        return self._make_request('post', 'add_or_update', data, 'main', nocheck)

    @doc(m_approved)
    @BaseApi.timing_decorator
    def approved(self, nocheck=False):
        res = self.pc.message_release_list_data()
        data = {
            "auditResult": "1",
            "ids": [
                res[0]['id']
            ],
            "selectType": "2",
            "operationType": 7
        }
        return self._make_request('post', 'message_audit', data, 'main', nocheck)

    @doc(m_refuse)
    @BaseApi.timing_decorator
    def refuse(self, nocheck=False):
        res = self.pc.message_release_list_data()
        data = {
            "auditResult": "2",
            "reason": "test1",
            "platformReason": "test1",
            "ids": [
                res[0]['id']
            ],
            "selectType": "2",
            "operationType": 7
        }
        return self._make_request('post', 'message_audit', data, 'main', nocheck)


if __name__ == '__main__':
    api = MessageReleaseListRequest()
    result = api.refuse()
    print(json.dumps(result, indent=4, ensure_ascii=False))
