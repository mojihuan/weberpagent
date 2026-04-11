# coding: utf-8
import json
from common.base_api import BaseApi


class Of0qYX0IunlCsfIKGi4b5(BaseApi):
    """保卖小程序|首页"""

    def WiNPlq2wIljG(self, headers=None):
        """精确发货 物品信息列表"""
        headers = headers or self.headers['main']
        data = {"modelId": 17569}
        response = self.request_handle('post', self.urls['RICU26LCy'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)

    def wuqs6Abzx3BS(self, headers=None):
        """精确发货 外观成色列表"""
        headers = headers or self.headers['main']
        data = {"modelId": 17569, "businessModel": 1}
        response = self.request_handle('post', self.urls['WNpOw4zZ2'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)

    def bYFfx68rsKxb(self):
        """获取id"""
        return self._get_field_copy_value('WiNPlq2wIljG', 'main', 'id')


class D7NTmTMqMuHicClYboqMC(BaseApi):
    """保卖小程序|我的"""

    def NVuRscNpWXeL(self, i=None, j=None, headers=None, num=1, size=1000):
        """销售订单列表
         i：订单状态 1质检中 2待销售 3销售中 4已销售 5待平台确认 6报价确认 8退货中 9退货已出库 10已退货 7质检完成
         j：类型 1销售服务 2质检服务
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), "businessType": j, 'status': i}
        response = self.request_handle('post', self.urls['TSpz5ocd0'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def WGXX2ZOSwrbe(self, headers=None):
        """销售物品 退货详情"""
        res = self.NVuRscNpWXeL(i=8)
        headers = headers or self.headers['main']
        data = {"id": res[0]['id']}
        response = self.request_handle('post', self.urls['ef9HoHytv'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)

    def QxGZi5hQD6xY(self, headers=None, i=None):
        """订单信息 订单详情"""
        res = self.NVuRscNpWXeL(i=i)
        headers = headers or self.headers['main']
        data = {"id": res[0]['id']}
        response = self.request_handle('post', self.urls['hOW1S1Eux'], data=json.dumps(data),
                                       headers=headers)
        return self.get_response_data(response, 'data', dict)

    def CyIwoGFLypcc(self, i=None, j=None, headers=None):
        """订单信息 订单列表
         i：订单状态 1待发货 2待取件 3待收货 4已收货
         j：类型 1销售服务 2质检服务
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "businessType": j}
        if i:
            data['status'] = int(i)
        response = self.request_handle('post', self.urls['SrcDaQjua'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def VDwQYOYWJkul(self):
        """获取成色名称"""
        return self._get_field_copy_value('QxGZi5hQD6xY', 'main', 'articlesInfoList.finenessName')


if __name__ == '__main__':
    api = ()
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
