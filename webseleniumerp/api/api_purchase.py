# coding: utf-8
import json
from common.base_api import BaseApi


class PurchaseAfterSalesListApi(BaseApi):
    """商品采购|采购售后管理|采购售后列表"""

    def after_sales_list(self, headers=None, num=1, size=1000):
        """采购售后列表"""
        headers = headers or self.headers['main']
        data = {'type': 1, **self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['purchase_after_sales_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def after_sales_orders_list(self, headers=None, num=1, size=1000):
        """采购售后中列表"""
        headers = headers or self.headers['main']
        data = {'type': 2, **self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['purchase_after_sales_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def after_sales_detail(self, headers=None):
        """采购售后订单详情"""
        headers = headers or self.headers['main']
        sale_id = self.get_sale_id()
        response = self.request_handle('get', self.urls['purchase_aftermarket_order_details'] + '/' + sale_id, headers=headers)
        return self.get_response_data(response, 'data', dict)

    # 获取id
    def get_sale_id(self):
        return self._get_field_copy_value('after_sales_list', 'main', 'id')

    # 获取imei
    def get_imei(self):
        return self._get_field_copy_value('after_sales_list', 'main', 'imei')


class PurchaseArrivalNoticesApi(BaseApi):
    """商品采购|采购管理|到货通知单列表"""

    def arrival_notices_list(self, headers=None):
        """到货通知单列表"""
        headers = headers or self.headers['main']
        data = {"stateList": [2, 3], **self.get_page_params()}
        response = self.request_handle('post', self.urls['arrival_notices'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class PurchaseItemsToBeReceivedApi(BaseApi):
    """商品采购|采购售后管理|待接收物品"""

    def receive_items_list(self, headers=None, num=1, size=1000):
        """待接收物品列表"""
        headers = headers or self.headers['main']
        data = {'articlesState': 10, 'articlesType': 1, **self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['inventory_receive_items'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res


class PurchaseLyArrivalApi(BaseApi):
    """商品采购|绿怡来货列表"""

    def ly_arrival_list(self, headers=None):
        """绿怡来货列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['ly_arrival'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PurchaseOrderListApi(BaseApi):
    """商品采购|采购管理|采购订单列表"""

    def order_list(self, headers=None, num=1, size=1000, i=None, j=None):
        """采购订单列表"""
        headers = headers or self.headers['main']
        data = {'articlesType': 1, **self.get_page_params(num, size), 'state': i, 'payStateStr': j}
        response = self.request_handle('post', self.urls['purchase_order_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def purchase_order_details(self, headers=None):
        """采购单详情"""
        headers = headers or self.headers['main']
        purchase_no = self.get_purchase_order_number()
        data = {'purchaseNo': purchase_no, **self.get_page_params()}
        response = self.request_handle('post', self.urls['purchase_order_details'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)

    # 获取采购单号
    def get_purchase_order_number(self):
        return self._get_field_copy_value('order_list', 'main', 'orderNo')

    # 获取imei
    def get_imei(self):
        return self._get_field_copy_value('purchase_order_details', 'main', 'imei')

    # 获取物流单号
    def get_logistics_no(self):
        return self._get_field_copy_value('order_list', 'main', 'logisticsNo')


class PurchasePostSaleListApi(BaseApi):
    """商品采购|采购售后管理|待售后列表"""

    def post_sale_list(self, headers=None, num=1, size=1000):
        """采购待售后列表"""
        headers = headers or self.headers['main']
        data = {'type': 1, **self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['post_sale_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PurchaseSupplierManageApi(BaseApi):
    """商品采购|供应商管理"""

    def supplier_manage(self, headers=None):
        """供应商管理"""
        headers = headers or self.headers['main']
        data = {'type': 2, **self.get_page_params()}
        response = self.request_handle('post', self.urls['supplier_manage'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)

    # 获取供应商名称
    def get_supplier_name(self):
        return self._get_field_copy_value('supplier_manage', 'idle', 'supplierName')

    # 获取供应商名称
    def get_default_supplier_name(self):
        return self._get_field_copy_value('supplier_manage', 'main', 'supplierName')

    # 获取供应商id
    def get_id(self):
        return self._get_field_copy_value('supplier_manage', 'main', 'id')


class PurchaseTaskListApi(BaseApi):
    """商品采购|采购任务"""

    def purchase_task_list(self, headers=None, num=1, size=1000):
        """采购任务"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['procurement_tasks'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PurchaseUnShippedOrderListApi(BaseApi):
    """商品采购|采购管理|未发货订单列表"""

    def un_shipped_order_list(self, headers=None):
        """未发货订单列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['un_shipped_order'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PurchaseWorkOrderApi(BaseApi):
    """商品采购|采购管理|采购工单"""

    def work_orders_list(self, headers=None, num=1, size=1000):
        """采购工单列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['work_orders'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    # 获取业务工序id
    def get_task_id(self):
        return self._get_field_copy_value('work_orders_list', 'main', 'taskProgressList.id')


if __name__ == '__main__':
    api = PurchaseOrderListApi()
    result = api.order_list()
    print(json.dumps(result, indent=4, ensure_ascii=False))
