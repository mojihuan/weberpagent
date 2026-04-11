# coding: utf-8
import json
from common.base_api import BaseApi
from common.base_params import InitializeParams
from common.import_desc import *


class QRSsWbYWV1(InitializeParams):
    """消息管理|消息发布列表"""

    @doc(p2KvndGL0zVJEDKHGIPU)
    @BaseApi.timing_decorator
    def p2KvndGL0zVJEDKHGIPU(self, nocheck=False):
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
        return self._make_request('post', 'CTDGoffF5', data, 'main', nocheck)

    @doc(qJP3yR1nymSHmVoKgKFz)
    @BaseApi.timing_decorator
    def qJP3yR1nymSHmVoKgKFz(self, nocheck=False):
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

        return self._make_request('post', 'g9QGSsci5', data, 'main', nocheck)

    @doc(fNGpyQ3gggozz0uW4Ko0)
    @BaseApi.timing_decorator
    def fNGpyQ3gggozz0uW4Ko0(self, nocheck=False):
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

        return self._make_request('post', 'CTDGoffF5', data, 'main', nocheck)

    @doc(ELqbuERMQsawGlkE9Ala)
    @BaseApi.timing_decorator
    def ELqbuERMQsawGlkE9Ala(self, nocheck=False):
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
        return self._make_request('post', 'fBQcHW1U6', data, 'main', nocheck)

    @doc(FAEFTmKmDM49LcbTv3tL)
    @BaseApi.timing_decorator
    def FAEFTmKmDM49LcbTv3tL(self, nocheck=False):
        res = self.pc.KxO3PKRgVuNDVjQUSHVcl()
        data = {
            "auditResult": "1",
            "ids": [
                res[0]['id']
            ],
            "selectType": "2",
            "operationType": 7
        }
        return self._make_request('post', 'KXoQfjXQR', data, 'main', nocheck)

    @doc(yNFy3et5XdWwF0gE1VJQ)
    @BaseApi.timing_decorator
    def yNFy3et5XdWwF0gE1VJQ(self, nocheck=False):
        res = self.pc.KxO3PKRgVuNDVjQUSHVcl()
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
        return self._make_request('post', 'KXoQfjXQR', data, 'main', nocheck)


if __name__ == '__main__':
    api = ()
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
