# coding: utf-8
import json
from common.base_api import BaseApi


class InventoryAddressManageApi(BaseApi):
    """库存管理|出库管理|地址管理"""

    def address_manage(self, headers=None, num=1, size=1000):
        """地址管理列表"""
        headers = headers or self.headers['idle']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['address_manage_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    # 获取id
    def get_data_id(self):
        return self._get_field_copy_value('address_manage', 'idle', 'id')

    # 获取壹准保卖id
    def get_yz_id(self):
        return self._get_field_copy_value('address_manage', 'main', 'id', index=2)

    # 获取通用业务id
    def get_ty_id(self):
        return self._get_field_copy_value('address_manage', 'main', 'id')

    # 获取壹准拍机id
    def get_pj_id(self):
        return self._get_field_copy_value('address_manage', 'camera', 'id', index=3)


class InventoryCountApi(BaseApi):
    """库存管理|库存盘点"""

    def inventory_count(self, headers=None, num=1, size=1000):
        """库存盘点列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['inventory_count'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    # 获取盘点单号
    def get_stock_no(self):
        return self._get_field_copy_value('inventory_count', 'main', 'stockNo')

    # 获取盘点id
    def get_id(self):
        return self._get_field_copy_value('inventory_count', 'main', 'id')


class InventoryListApi(BaseApi):
    """库存管理|库存列表"""

    def inventory_list(self, headers=None, i=None, j=None, num=1, size=1000, t=None):
        """库存列表
         i：库存状态 2库存中 1待入库 3已出库
         j：物品状态 2待收货 13待销售 3待分货 7维修中 5质检中 19销售预售中 14销售铺货中 16待送修 9已销售 15销售售后中 17送修中 11采购售后完成 12采购售后中 18仅出库 10待采购售后
         t: 品类id
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'inventoryStatus': i, 'articlesState': j, 'articlesTypeId': t}
        response = self.request_handle('post', self.urls['item_inventory_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def details_of_the_total_cost_of_inventory_count(self, headers=None):
        """库存列表 总成本详情 统计"""
        headers = headers or self.headers['main']
        articles_no = self.get_all_articles_no()
        data = {**self.get_page_params()}
        response = self.request_handle('get', self.urls['total_cost_details_const'] + '/' + articles_no, data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)

    def details_of_the_total_cost_of_inventory(self, headers=None, i=0):
        """库存列表 总成本详情"""
        headers = headers or self.headers['main']
        articles_no = self.get_all_articles_no()
        data = {**self.get_page_params(), 'articlesNo': articles_no}
        response = self.request_handle('post', self.urls['total_cost_details'], data=json.dumps(data), headers=headers)
        rows = self.get_response_data(response, 'rows', list)
        if len(rows) > i >= 0:
            return rows[i]
        else:
            print("走这个逻辑了")
            return None

    def details_of_total_inventory_revenue_count(self, headers=None):
        """库存列表 总成本详情 统计"""
        headers = headers or self.headers['main']
        articles_no = self.get_all_articles_no()
        data = {**self.get_page_params()}
        response = self.request_handle('get', self.urls['details_of_total_revenue_const'] + '/' + articles_no, data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)

    def details_of_total_inventory_revenue(self, headers=None, i=0):
        """库存列表 总成本详情"""
        headers = headers or self.headers['main']
        articles_no = self.get_all_articles_no()
        data = {**self.get_page_params(), 'articlesNo': articles_no}
        response = self.request_handle('post', self.urls['details_of_total_revenue'], data=json.dumps(data), headers=headers)
        rows = self.get_response_data(response, 'rows', list)
        if len(rows) > i >= 0:
            return rows[i]
        else:
            return None

    def item_details_sell_info(self, headers=None):
        """物品详情 销售信息"""
        headers = headers or self.headers['main']
        articles_no = self.get_all_articles_no()
        data = {'articlesNo': articles_no}
        response = self.request_handle('post', self.urls['item_details_sell'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)

    def operation_log(self, headers=None):
        """物品详情 操作日志"""
        headers = headers or self.headers['main']
        articles_no = self.get_all_articles_no()
        data = {'articlesNoList': [articles_no]}
        response = self.request_handle('post', self.urls['operation_log'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)

    def get_all_articles_no(self, i=None, j=None, index=0):
        """获取库存列表 物品编号
         i：库存状态 2库存中 1待入库 3已出库
         j：物品状态 13待销售 3待分货 7维修中 5质检中 19销售预售中 14销售铺货中 16待送修 9已销售 15销售售后中 17送修中 11采购售后完成 12采购售后中 18仅出库 10待采购售后
         index: 下标
        """
        return self._get_field_copy_value('inventory_list', 'main', 'articlesNo', i=i, j=j, index=index)

    def get_vice_articles_no(self, i=None, j=None):
        """获取库存列表 物品编号"""
        return self._get_field_copy_value('inventory_list', 'vice', 'articlesNo', i=i, j=j)

    def get_all_imei(self, i=None, j=None, index=0):
        """获取库存列表 imei"""
        return self._get_field_copy_value('inventory_list', 'main', 'imei', i=i, j=j, index=index)


class InventoryLogisticsChangeRecordApi(BaseApi):
    """库存管理|入库管理|物流修改记录"""

    #
    def logistics_change_record(self, headers=None, num=1, size=1000):
        """物流修改记录列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['logistics_change_record'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class InventoryLogisticsIntoWarehouseApi(BaseApi):
    """库存管理|入库管理|物流签收入库"""

    def __init__(self):
        super().__init__()
        self.logistics = InventoryLogisticsListApi()

    def logistics_list(self, headers=None, num=1, size=1000):
        """物流签收入库"""
        headers = headers or self.headers['main']
        logistics_no = self.logistics.get_logistics_no()
        data = {**self.get_page_params(num, size), 'logisticsNo': logistics_no}
        response = self.request_handle('post', self.urls['logistics_sign_into_the_warehouse'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    # 获取物品编号
    def get_articles_no(self):
        return self._get_field_copy_value('logistics_list', 'main', 'articlesNo')


class InventoryLogisticsListApi(BaseApi):
    """库存管理|入库管理|物流列表"""

    def material_flow_list(self, headers=None, num=1, size=1000, i=None, j=None, k=None):
        """物流列表
        i imei
        j 平台物品编号
        k 状态
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'imei': i, 'platformArticlesNo': j, 'sortationStatus': k}
        response = self.request_handle('post', self.urls['material_flow_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def material_flow_list_detail(self, headers=None):
        """物流列表详情"""
        headers = headers or self.headers['main']
        logistics_no = self.get_logistics_no()
        data = {**self.get_page_params(), "logisticsNo": logistics_no}
        response = self.request_handle('post', self.urls['logistics_sign_into_the_warehouse'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    # 获取物流编号
    def get_logistics_no(self):
        return self._get_field_copy_value('material_flow_list', 'main', 'logisticsNo')


class InventoryModelDistributionApi(BaseApi):
    """库存管理|库存统计|库存型号分布"""

    def model_distribution_list(self, headers=None, num=1, size=1000):
        """库存型号分布列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'articlesTypeId': "1"}
        response = self.request_handle('post', self.urls['model_distribution'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class InventoryOutStockLogisticsListApi(BaseApi):
    """库存管理|出库管理|出库物流记录"""

    def out_stock_logistics_list(self, headers=None, num=1, size=1000):
        """出库物流记录列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['out_stock_logistics_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class InventoryOutboundOrdersListApi(BaseApi):
    """库存管理|出库管理|仅出库订单列表"""

    def only_outbound_list(self, headers=None, num=1, size=1000):
        """仅出库列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['out_bound_orders_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def list_of_returned_orders(self, headers=None, num=1, size=1000):
        """退回单列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['list_of_returned_orders'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def only_outbound_order_details(self, headers=None, item_id=None):
        """仅出库订单详情"""
        headers = headers or self.headers['main']
        item_id = item_id or self.get_id()
        data = {'id': item_id, **self.get_page_params(), 'total': 0, 'type': 1}
        response = self.request_handle('post', self.urls['only_outbound_order_details'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)

    # 获取id
    def get_id(self):
        return self._get_field_copy_value('only_outbound_list', 'main', 'id')


class InventoryPeopleDistributionApi(BaseApi):
    """库存管理|库存统计|库存人员分布"""

    def people_distribution_list(self, headers=None, num=1, size=1000):
        """库存人员分布列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['people_distribution'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class InventoryReceiveItemsApi(BaseApi):
    """库存管理|移交接收管理|接收物品"""

    def stay_work_list(self, i=None, j=None, headers=None, k=None):
        """物品接收
         i：物品状态 1待维修 2待收货 3待分货 4待质检 5质检中 6待维修 7维修中
         j: 品类 1手机
        """
        headers = headers or self.headers['main']
        data = {'articlesType': 1, **self.get_page_params(), 'articlesState': i, 'articlesTypeId': j, 'reasonType': k}
        response = self.request_handle('post', self.urls['inventory_receive_items'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res

    def receive_items(self, headers=None, num=1, size=1000, i=None):
        """移交单接收"""
        headers = headers or self.headers['main']
        data = {'articlesType': '1', **self.get_page_params(num, size), 'reasonType': i}
        response = self.request_handle('post', self.urls['receive_items'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def receive_items_detail(self, headers=None, j=1):
        """移交单接收详情"""
        headers = headers or self.headers['main']
        req_res = self.receive_items()
        data = {"articlesType": j, "orderNo": req_res[0]['orderNo']}
        response = self.request_handle('post', self.urls['hand_over_no_detail'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        res[0]['orderNo'] = req_res[0]['orderNo']
        return res


class InventorySendOutRepairApi(BaseApi):
    """库存管理|出库管理|送修出库"""


class InventoryTransferRecordsApi(BaseApi):
    """库存管理|移交接收管理|移交记录"""

    def receive_log(self, headers=None, num=1, size=1000, i=None, j=None):
        """移交记录列表
        i 状态
        j 原因
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'articlesType': 1, 'status': i, 'reasonType': j}
        response = self.request_handle('post', self.urls['handover_records_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def receive_log_detail(self, headers=None):
        """移交记录列表详情"""
        headers = headers or self.headers['main']
        order_no = self.get_order_no()
        data = {"orderNo": order_no, "articlesType": 1}
        response = self.request_handle('post', self.urls['hand_over_no_detail'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res

    # 获取单号
    def get_order_no(self):
        return self._get_field_copy_value('receive_log', 'main', 'orderNo')


class InventoryWaitReceiveApi(BaseApi):
    """库存管理|入库管理|待接收物品"""

    def wait_receive_list(self, headers=None, num=1, size=1000):
        """待接收物品列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), "erpStartTime": self.get_the_date(-7), "erpEndTime": self.get_the_date()}
        response = self.request_handle('post', self.urls['inventory_receive_items'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class InventoryWarehouseAllocationApi(BaseApi):
    """库存管理|库存调拨"""

    def warehouse_transfers(self, headers=None, num=1, size=1000):
        """仓库调拨列表"""
        headers = headers or self.headers['main']
        data = {'articlesType': '1', **self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['warehouse_allocation'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def transfer_details(self, headers=None):
        """调拨详情"""
        headers = headers or self.headers['main']
        id = self.get_id()
        data = {'articlesType': '1', 'id': id}
        response = self.request_handle('post', self.urls['transfer_details'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)

    # 获取id
    def get_id(self):
        return self._get_field_copy_value('warehouse_transfers', 'main', 'id')


class InventoryWarningListApi(BaseApi):
    """库存管理|库存统计|库龄预警"""

    def warning_list(self, headers=None, num=1, size=1000):
        """库龄预警列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'articlesTypeId': 1}
        response = self.request_handle('post', self.urls['curling_warning'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = InventoryAddressManageApi()
    result = api.address_manage()
    print(json.dumps(result, indent=4, ensure_ascii=False))

