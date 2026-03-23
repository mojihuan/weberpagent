# coding: utf-8
import json
from common.base_api import BaseApi
from config.user_info import INFO


class FulfillmentItemsToBeQuotedApi(BaseApi):
    """运营中心|待报价物品"""

    def items_to_be_quoted_list(self, headers=None):
        """待报价物品列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num=1, size=999999)}
        response = self.request_handle('post', self.urls['items_to_be_quoted'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list, index=-1)


class FulfillmentOrderManageApi(BaseApi):
    """运营中心|订单管理"""

    def order_list(self, i=None, headers=None, num=1, size=9999):
        """订单列表
         i：订单状态 1待发货 2待取件 3待收货 4已收货 5已完成 6已取消 7已退货
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'status': i}
        response = self.request_handle('post', self.urls['operational_order_manage'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def order_by_index(self, index=None, i=None, headers=None):
        """
        获取订单列表中指定索引的数据
         index: 索引位置（从0开始）
         i：订单状态 1待发货 2待取件 3待收货 4已收货 5已完成 6已取消 7已退货
        指定索引的订单数据或None（如果索引超出范围）
        """
        order_list_result = self.order_list(i=i, headers=headers)
        if len(order_list_result) > index:
            return order_list_result[index]
        return None

    def item_list(self, headers=None):
        """物品列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['warranted_order_list_item'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def get_all_order_no(self, index=0, i=None):
        """获取订单列表 订单号"""
        return self._get_field_copy_value('order_list', 'main', 'orderNo', index=index, i=i)

    def get_all_express_no(self, index=0, i=None):
        """获取订单列表 物流单号"""
        return self._get_field_copy_value('order_list', 'main', 'expressNo', index=index, i=i)


class FulfillmentQualityManageApi(BaseApi):
    """运营中心|质检管理"""

    def quality_manage_list(self, headers=None):
        """待领取物品列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['pending_collection'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def items_in_quality_inspection_list(self, headers=None):
        """质检中物品列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['items_in_quality_inspection'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def re_examine_the_application_list(self, headers=None):
        """重验申请列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['re_examine_the_application'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def inspected_items_list(self, headers=None, num=1, size=9999):
        """已质检物品列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['inspected_items'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def product_image_shooting_list(self, headers=None, i=None, num=1, size=9999):
        """商品图拍摄列表
        i类型 1未上传 2已上传
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'goodsImageStatus': i}
        response = self.request_handle('post', self.urls['product_image_shooting'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def quality_inspection_template(self, headers=None):
        """质检模版"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'brandId': 1, 'categoryId': 1}
        response = self.request_handle('post', self.urls['quality_inspection_template'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    # 获取物品编号
    def get_articles_no(self):
        return self._get_field_copy_value('inspected_items_list', 'main', 'articlesNo')


class FulfillmentReturnsManageApi(BaseApi):
    """运营中心|退货管理"""

    def merchant_details_list(self, i=None, headers=None):
        """商户明细列表
         i：订单状态 1待退货 2待取货 3退货已出库 4已退货 5已取消
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'status': i}
        response = self.request_handle('post', self.urls['merchant_details_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def item_detail_list(self, i=None, headers=None):
        """物品明细列表
         i：订单状态 1待退货 2待取货 3退货已出库 4已退货 5已取消
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'status': i}
        response = self.request_handle('post', self.urls['item_detail_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def batch_detail_list(self, i=None, headers=None):
        """批次明细列表
         i：订单状态 1待退货 2待取货 3退货已出库 4已退货 5已取消
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'status': i}
        response = self.request_handle('post', self.urls['batch_detail_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class FulfillmentSignIntoTheLibraryApi(BaseApi):
    """运营中心|收货入库"""

    def __init__(self):
        super().__init__()
        self.order_manage = FulfillmentOrderManageApi()
        self.camera_after_sales_order = FulfillmentCameraAfterSalesOrderApi()

    def search_tracking_numbers(self, headers=None):
        """搜索保卖订单号"""
        order_no = self.order_manage.order_list(i=3)
        headers = headers or self.headers['main']
        data = {"consignmentOrderNo": order_no[0]['orderNo']}
        response = self.request_handle('post', self.urls['search_tracking_numbers'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res

    def search_pj_tracking_numbers(self, headers=None):
        """搜索拍机订单号"""
        order_no = self.camera_after_sales_order.get_order_no()
        headers = headers or self.headers['main']
        data = {"consignmentOrderNo": order_no}
        response = self.request_handle('post', self.urls['search_tracking_numbers'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res

    def search_tracking_express(self, headers=None):
        """搜索保卖物流单号"""
        express_no = self.order_manage.order_list(i=3)
        headers = headers or self.headers['main']
        data = {"expressNo": express_no[0]['expressNo']}
        response = self.request_handle('post', self.urls['search_tracking_numbers'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res


class FulfillmentSellGoodsTransactionsApi(BaseApi):
    """运营中心|销售商品交易"""

    def order_by_index(self, headers=None, num=1, size=10, i=None):
        """销售商品交易列表
         i：订单状态 1待支付 2待发货 3待收货 4已收货 5已售后 6已取消"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        if i is not None:
            data['articlesStatus'] = i
        response = self.request_handle('post', self.urls['fulfillment_sell_goods'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class FulfillmentBotOrderApi(BaseApi):
    """运营中心|bot订单管理"""

    def bot_order_list(self, headers=None, num=1, size=9999):
        """bot订单管理列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['bot_order_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class FulfillmentVirtualListApi(BaseApi):
    """运营中心|虚拟库存列表"""

    def yun_ying_virtual_list(self, headers=None, num=1, size=9999):
        """虚拟库存列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['yun_ying_virtual_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class FulfillmentSalesAndShipmentManageApi(BaseApi):
    """运营中心|销售发货管理"""

    def sales_and_shipment_manage_list(self, headers=None):
        """待发货 按商户"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['sales_and_shipment_manage'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def sales_and_shipment_manage_item_list(self, headers=None):
        """待发货 按物品"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'buyTenantId': INFO['camera_merchant_id']}
        response = self.request_handle('post', self.urls['sales_and_shipment_manage_item'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def snap_the_order_to_be_received_list(self, headers=None):
        """待收货 按物品"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'buyTenantId': INFO['camera_merchant_id']}
        response = self.request_handle('post', self.urls['snap_the_order_to_be_received'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def sales_and_fulfillment_management_list(self, headers=None):
        """待收货 按包裹"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['sales_and_fulfillment_management'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def snap_machine_has_been_received_list(self, headers=None):
        """已收货 按包裹"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['snap_machine_has_been_received'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def snap_machine_has_been_received_item_list(self, headers=None):
        """已收货 按物品"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'buyTenantId': INFO['camera_merchant_id']}
        response = self.request_handle('post', self.urls['snap_machine_has_been_received_item'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    # 获取平台物品编号
    def get_articles_no(self):
        return self._get_field_copy_value('sales_and_shipment_manage_item_list', 'main', 'articlesNo')


class FulfillmentItemsAreOutOfStorageApi(BaseApi):
    """运营中心|物品出库"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sales_manage = FulfillmentSalesAndShipmentManageApi()

    def item_outbound_list(self, headers=None):
        """物品出库列表-销售出库
        """
        articles_no = self.sales_manage.get_articles_no()
        headers = headers or self.headers['main']
        data = {"articlesNoList": [articles_no], "status": 1}
        response = self.request_handle('post', self.urls['items_are_out_of_storage'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res


class FulfillmentCameraAfterSalesOrderApi(BaseApi):
    """运营中心|壹准拍机|售后管理|售后订单"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def camera_after_sales_order_list(self, headers=None, i=None):
        """售后订单列表
        i 订单状态
        [2]待申诉 [1]线上审核 [3]线上拒退 [4]申诉中 [5]补差成功 [6]可补差
        [7]待寄回 [8]超时取消 [9]主动取消 [10]待接收 [11]实物复检 [12]实物拒退 [13]退货成功
        """
        if i is None:
            i = ['10']
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'centerId': INFO['check_the_center_id'], 'afterStatusList': i}
        response = self.request_handle('post', self.urls['camera_after_sales_order_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    # 获取订单号
    def get_order_no(self):
        return self._get_field_copy_value('camera_after_sales_order_list', 'main', 'orderNo')


class FulfillmentAfterSalesReturnManageApi(BaseApi):
    """运营中心|壹准拍机|售后管理|售后退货管理"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def after_sales_return_list(self, headers=None, i=None):
        """售后退货列表
        i 类型  1待退货 2退货已出库
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'returnStatus': i}
        response = self.request_handle('post', self.urls['after_sales_return_manage'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = FulfillmentOrderManageApi()
    result = api.order_list()
    # print(json.dumps(result, indent=4, ensure_ascii=False))

