# coding: utf-8
import json
from common.base_api import BaseApi
from config.user_info import INFO


class AttachmentAfterSalesListApi(BaseApi):
    """配件管理|配件销售|销售售后列表"""

    def after_sales_list(self, headers=None, num=1, size=1000):
        """销售售后列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['after_sales_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def after_sales_list_detail(self, headers=None):
        """销售售后列表 详情"""
        headers = headers or self.headers['main']
        after_sales = self.after_sales_list()
        data = {**self.get_page_params(), 'orderNo': after_sales[0]['orderNo']}
        response = self.request_handle('post', self.urls['after_sales_detail'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class AttachmentGiftDetailsApi(BaseApi):
    """配件管理|配件统计|赠送明细"""

    def gift_details_list(self, headers=None, num=1, size=1000):
        """赠送明细列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['gift_details'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class AttachmentGoodsReceivedApi(BaseApi):
    """配件管理|入库管理|待接收物品"""

    def list_of_items_to_be_received(self, headers=None, num=1, size=1000):
        """待接收物品列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['items_to_be_received'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class AttachmentHandoverRecordsApi(BaseApi):
    """配件管理|移交接收管理|移交记录"""

    def handover_records_list(self, headers=None, num=1, size=1000, i=None):
        """移交记录"""
        headers = headers or self.headers['main']
        data = {'articlesType': 2, 'status': i, **self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['handover_records'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def handover_records_details(self, headers=None):
        """移交记录详情"""
        headers = headers or self.headers['main']
        data = {"orderNo": self.get_order_no(), "articlesType": 2}
        response = self.request_handle('post', self.urls['hand_over_no_detail'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res

    # 获取订单号
    def get_order_no(self):
        return self._get_field_copy_value('handover_records_list', 'main', 'orderNo')


class AttachmentInventoryDetailsApi(BaseApi):
    """配件管理|配件库存|库存明细"""

    def inventory_details_list(self, headers=None, num=1, size=1000):
        """库存明细列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'total': 0}
        response = self.request_handle('post', self.urls['inventory_details'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def inventory_details_stats(self, headers=None):
        """库存明细统计"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'total': 0}
        response = self.request_handle('post', self.urls['inventory_stats'], data=json.dumps(data), headers=headers)
        return response.json()["data"]


class AttachmentInventoryListApi(BaseApi):
    """配件管理|配件库存|库存列表"""

    def attachment_inventory_list(self, i=None, j=None, k=None, l=None, m=None, a=None, headers=None, num=1, size=1000):
        """库存列表
        i: 库存状态 2库存中 1待入库 3已出库
        j: 品类
        k：品牌
        l：型号
        m：配件成色 1新配件 2旧配件采购
        a：配件渠道 1原厂 2非原厂
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'inventoryStatus': i, 'articlesTypeId': j, 'brandId': k,
                'modelId': l, 'accessoryQuality': m, 'channelType': a}
        response = self.request_handle('post', self.urls['inventory_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def inventory_detail(self, headers=None):
        """库存列表详情"""
        headers = headers or self.headers['main']
        articles_no = self.get_articles_no()
        data = {'articlesNo': articles_no}
        response = self.request_handle('post', self.urls['inventory_detail'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)

    def inventory_purchase_info(self, headers=None):
        """库存列表-配件详情-采购信息"""
        headers = headers or self.headers['main']
        articles_no = self.get_articles_no()
        data = {'articlesNo': articles_no}
        response = self.request_handle('post', self.urls['inventory_purchase_info'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)

    def inventory_sell_info(self, headers=None):
        """库存列表-配件详情-销售信息"""
        headers = headers or self.headers['main']
        articles_no = self.get_articles_no()
        data = {'articlesNo': articles_no}
        response = self.request_handle('post', self.urls['inventory_sell_info'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)

    def inventory_log_info(self, headers=None):
        """库存列表-配件详情-操作日志"""
        headers = headers or self.headers['main']
        articles_no = self.get_articles_no()
        data = {'articlesNoList': [articles_no]}
        response = self.request_handle('post', self.urls['operation_log'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)

    #
    def get_all_articles_no(self, i=None, index=0):
        """获取库存列表 物品编号
         i: 库存状态 2库存中 1待入库 3已出库
         index
        """
        return self._get_field_copy_value('attachment_inventory_list', 'main', 'articlesNo', i=i, index=index)

    # 获取库存列表 物品编号
    def get_articles_no(self):
        return self._get_field_copy_value('attachment_inventory_list', 'main', 'articlesNo')


class AttachmentMaintenanceApi(BaseApi):
    """配件管理|配件维护"""

    def maintenance_list(self, headers=None, i=None, num=1, size=1000):
        """配件维护列表
        i：状态 0开启用 1停用
        """
        headers = headers or self.headers['idle']
        data = {**self.get_page_params(num, size), 'status': i}
        response = self.request_handle('post', self.urls['maintenance_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class AttachmentNewArrivalApi(BaseApi):
    """配件管理|入库管理|新到货入库"""

    def __init__(self):
        super().__init__()
        self.sorting_list = AttachmentSortingListApi()

    def new_arrival_list(self, headers=None, num=1, size=1000):
        """新到货入库"""
        sorting_list = self.sorting_list.get_tracking_number()
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'logisticsNo': sorting_list}
        response = self.request_handle('post', self.urls['new_arrival'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, '', list)
        self.make_pkl_file(res)
        return res


class AttachmentOldWarehouseApi(BaseApi):
    """配件管理|入库管理|旧配件入库"""

    def accessories_inventory_list(self, headers=None, num=1, size=1000):
        """旧配件入库列表"""
        headers = headers or self.headers['main']
        data = {'total': 0, **self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['list_of_old_accessories'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def accessories_inventory_detail(self, headers=None):
        """旧配件入库列表 详情"""
        headers = headers or self.headers['main']
        res = self.accessories_inventory_list()
        data = {'total': 0, **self.get_page_params(), "orderNo": res[0]['orderNo']}
        response = self.request_handle('post', self.urls['details_of_old_accessories'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)


class AttachmentPurchaseListApi(BaseApi):
    """配件管理|配件采购|采购列表"""

    def purchase_list(self, headers=None, num=1, size=1000, i=None, j=None):
        """采购列表
        i: 采购单状态 3已发货 4已收货
        j: 付款状态 1已付款 2未付款
        """
        headers = headers or self.headers['main']
        data = {'articlesType': 2, **self.get_page_params(num, size), 'state': i, 'payState': j}
        response = self.request_handle('post', self.urls['purchase_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def purchase_list_detail(self, headers=None):
        """采购列表 详情"""
        headers = headers or self.headers['main']
        order_no = self.get_order_no()
        data = {**self.get_page_params(), 'purchaseNo': order_no}
        response = self.request_handle('post', self.urls['purchase_detail'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)

    def procurement_after_sales(self, headers=None):
        """采购售后详情"""
        headers = headers or self.headers['main']
        order_no = self.get_order_no()
        data = {"supplierId": INFO['main_supplier_id'], "purchaseNoList": [order_no]}
        response = self.request_handle('post', self.urls['purchase_after_sales'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)

    # 获取采购单号
    def get_order_no(self):
        return self._get_field_copy_value('purchase_list', 'main', 'orderNo')


class AttachmentPurchaseSalesListApi(BaseApi):
    """配件管理|配件采购|采购售后列表"""

    def purchase_sales_list(self, headers=None, num=1, size=1000):
        """采购售后列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['purchase_sales_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def purchase_sales_list_detail(self, headers=None):
        """采购售后列表详情"""
        headers = headers or self.headers['main']
        purchase_sales = self.purchase_sales_list()
        data = {"saleNo": purchase_sales[0]['saleNo'], **self.get_page_params()}
        response = self.request_handle('post', self.urls['purchase_sales_detail'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class AttachmentReceiveItemsApi(BaseApi):
    """配件管理|移交接收管理|接收物品"""

    def item_received_list(self, headers=None, num=1, size=1000):
        """物品接收列表"""
        headers = headers or self.headers['main']
        data = {'articlesType': '2', **self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['items_to_be_received'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def handover_order_received_list(self, headers=None, i=None, num=1, size=1000):
        """移交单接收列表
        i：移交单状态 1待接收 2已接收 3已取消
        """
        headers = headers or self.headers['main']
        data = {'articlesType': '2', **self.get_page_params(num, size), 'status': i}
        response = self.request_handle('post', self.urls['receive_items'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class AttachmentHandOverTheListOfItemsApi(BaseApi):
    """配件管理|移交接收管理|移交物品"""

    def __init__(self):
        super().__init__()
        self.inventory_list = AttachmentInventoryListApi()

    def hand_over_the_list_of_items(self, headers=None):
        """移交物品列表"""
        articles_no = self.inventory_list.get_articles_no()
        headers = headers or self.headers['main']
        data = {"articlesNo": articles_no}
        response = self.request_handle('post', self.urls['accessories_search_items'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', dict)
        self.make_pkl_file(res)
        return res


class AttachmentSalesDetailsApi(BaseApi):
    """配件管理|配件统计|销售明细"""

    def statics_list(self, i=1, headers=None):
        """销售明细列表
         i：1本月 2上月
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "total": 99, "month": i}
        response = self.request_handle('post', self.urls['list_of_sales_details'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)

    def statics_detail(self, i=1, headers=None):
        """销售明细统计-本月
         i：1本月 2上月
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "total": 99, "month": i}
        response = self.request_handle('post', self.urls['sales_details_statics'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)


class AttachmentSalesListApi(BaseApi):
    """配件管理|配件销售|销售列表"""

    def sales_list(self, headers=None, num=1, size=1000, i=None):
        """销售列表
        i: 收款状态 1已收款 2未收款
        """
        headers = headers or self.headers['main']
        data = {'articlesType': 2, **self.get_page_params(num, size), 'status': i}
        response = self.request_handle('post', self.urls['sales_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def sales_details(self, headers=None):
        """销售详情"""
        headers = headers or self.headers['main']
        order_no = self.get_order_no()
        data = {'orderNo': order_no, **self.get_page_params()}
        response = self.request_handle('post', self.urls['sales_details'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)

    def sales_after_sales(self, headers=None):
        """销售售后"""
        headers = headers or self.headers['main']
        order_no = self.get_order_no()
        data = {"saleOrderNoList": [order_no]}
        response = self.request_handle('post', self.urls['sales_after_sales'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)

    # 获取销售单号
    def get_order_no(self):
        return self._get_field_copy_value('sales_list', 'main', 'orderNo')


class AttachmentSortingListApi(BaseApi):
    """配件管理|入库管理|分拣列表"""

    def sorting_list(self, headers=None, i=None, num=1, size=1000):
        """分拣列表
        i: 分拣状态 1未分拣 2已分拣
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'sortationStatus': i}
        response = self.request_handle('post', self.urls['sorting_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def package_video(self, headers=None):
        """包裹视频"""
        headers = headers or self.headers['main']
        tracking_number = self.get_tracking_number()
        data = {'articlesType': 2, 'logisticsNo': tracking_number}
        response = self.request_handle('post', self.urls['sorting_package_video'], data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            return response.json()
        return None

    # 获取物流单号
    def get_tracking_number(self):
        return self._get_field_copy_value('sorting_list', 'main', 'logisticsNo')


class AttachmentStaticsDetailApi(BaseApi):
    """配件管理|配件统计|维修明细"""

    def statics_detail_list(self, month=1, headers=None, num=1, size=1000):
        """维修明细列表
         month：1本月 2上月
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), "month": month}
        response = self.request_handle('post', self.urls['list_of_repair_details'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def statics_detail_list_detail(self, headers=None):
        """维修消耗 详情"""
        headers = headers or self.headers['main']
        res = self.statics_detail_list()
        data = {**self.get_page_params(), "modelId": res[0]['modelId'], "brandId": res[0]['brandId'], "accessoryNo": res[0]['accessoryNo']}
        response = self.request_handle('post', self.urls['repair_details_detail'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class AttachmentWarehouseAllocationApi(BaseApi):
    """配件管理|配件库存|库存调拨"""

    def warehouse_allocation(self, headers=None, num=1, size=1000):
        """库存调拨列表"""
        headers = headers or self.headers['main']
        data = {'articlesType': '2', **self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['warehouse_allocation'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def inventory_transfer_details_list(self, headers=None):
        """库存调拨列表 详情"""
        headers = headers or self.headers['main']
        res = self.warehouse_allocation()
        data = {'articlesType': '2', 'id': res[0]['id']}
        response = self.request_handle('post', self.urls['transfer_details'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)

    def revoke_the_transfer_details(self, headers=None):
        """撤销调拨 详情"""
        headers = headers or self.headers['main']
        res = self.warehouse_allocation()
        data = {'articlesType': '2', 'id': res[0]['id']}
        response = self.request_handle('post', self.urls['revoke_the_transfer_details'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)

    # 获取库存调拨列表 详情 物品编号
    def get_articles_no(self):
        return self._get_field_copy_value('inventory_transfer_details_list', 'main', 'itemList.articlesNo')


if __name__ == '__main__':
    api = AttachmentNewArrivalApi()
    result = api.new_arrival_list()
    print(json.dumps(result, indent=4, ensure_ascii=False))
