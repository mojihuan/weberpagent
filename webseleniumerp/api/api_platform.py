# coding: utf-8
import json
from common.base_api import BaseApi
from config.user_info import INFO


class PlatformVirtualInventoryListApi(BaseApi):
    """平台管理|虚拟库存|虚拟库存列表"""

    def virtual_inventory_list(self, i=None, headers=None):
        """虚拟库存列表
         i：物品状态 1质检中 2待销售 3销售中 4已销售 5待平台确认 6报价确认 7质检完成 8退货中 9退货已出库 10已退货

        """
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'status': i, 'inspectionCenterCode': INFO['merchant_id']}
        response = self.request_handle('post', self.urls['virtual_inventory_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    # 获取id
    def get_id(self):
        return self._get_field_copy_value('virtual_inventory_list', 'super', 'id')

    # 获取物品编号
    def get_articles_no(self):
        return self._get_field_copy_value('virtual_inventory_list', 'super', 'articlesNo')


class PlatformAuctionProductManageApi(BaseApi):
    """平台管理|虚拟库存|上拍商品管理"""

    def list_of_auctioned_products(self, headers=None, i=None):
        """上拍商品管理列表
         i：类型 1可上拍商品 2已上拍商品 0待定价物品
        """
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'type': i, 'centerId': INFO['check_the_center_id']}
        response = self.request_handle('post', self.urls['list_of_dark_auction_houses'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def select_the_list_of_sessions(self, headers=None, i=None):
        """选择场次列表
        i：类型 1暗拍 2直拍
        """
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'marketCategory': i}
        response = self.request_handle('post', self.urls['auction_product_manage'], data=json.dumps(data),  headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformAuctionBusinessSettingsApi(BaseApi):
    """平台管理|配置中心|拍机业务设置"""

    def base_config_parameters(self, headers=None):
        """基础配置-参数配置"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'businessType': 2}
        response = self.request_handle('post', self.urls['base_config_parameters'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def base_config_dict(self, headers=None):
        """基础配置-字典配置"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'businessType': 1}
        response = self.request_handle('post', self.urls['base_config_dict'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformExpenseConfigApi(BaseApi):
    """平台管理|配置中心|费用配置"""

    def expense_config_list(self, headers=None):
        """费用配置列表"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['expense_config'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformMarginAllocationApi(BaseApi):
    """平台管理|配置中心|保证金配置"""

    def margin_allocation_list(self, headers=None):
        """保证金配置列表"""
        headers = headers or self.headers['super']
        data = {}
        response = self.request_handle('post', self.urls['margin_allocation'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res


class PlatformYzAuctionApi(BaseApi):
    """平台管理|壹准拍机|售后管理|售后订单"""

    def after_sales_order_list(self, i=None, headers=None):
        """售后订单列表,：
        i 订单状态
        [2]待申诉 [1]线上审核 [3]线上拒退 [4]申诉中 [5]补差成功 [6]可补差
        [7]待寄回 [8]超时取消 [9]主动取消 [10]待接收 [11]实物复检 [12]实物拒退 [13]退货成功
        """
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), "afterStatusList": i}
        response = self.request_handle('post', self.urls['after_sales_order'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    # 获取售后物品编号
    def get_after_sales_articles_no(self):
        return self._get_field_copy_value('after_sales_order_list', 'super', 'articlesNo')


class PlatformGrievanceManageApi(BaseApi):
    """平台管理|壹准拍机|售后管理|申诉管理"""

    def statement_list(self, i=None, headers=None):
        """申述管理列表,：
         i订单类型 0待处理 2申诉成功 2申诉失败 3申诉取消
        """
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), "status": i}
        response = self.request_handle('post', self.urls['statement_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformAfterSalesReturnManageApi(BaseApi):
    """平台管理|壹准拍机|售后管理|售后退货管理"""

    def can_after_sales_attr_list(self, headers=None):
        """可售后属性列表"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['aftermarket_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformAftermarketAttributesApi(BaseApi):
    """平台管理|壹准拍机|售后管理|可售后属性"""

    def can_after_sales_attr_list(self, headers=None):
        """可售后属性列表"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['aftermarket_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformDistributionApi(BaseApi):
    """平台管理|分销管理|分销商管理"""

    def distributors_list(self, headers=None):
        """分销商管理"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['distributor_manage'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformDistributionOrdersApi(BaseApi):
    """平台管理|分销管理|分销商业绩"""

    def orders_list(self, headers=None):
        """分销商业绩"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['distributor_performance'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformDistributionRolesApi(BaseApi):
    """平台管理|分销管理|分销商角色"""

    def roles_list(self, headers=None):
        """分销商角色"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['distributor_role'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformHelpSellConfigApi(BaseApi):
    """平台管理|帮卖管理|帮卖商家配置"""

    def help_sell_config(self, headers=None):
        """帮卖商家配置"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['help_sellers_configure'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformHelpSellListApi(BaseApi):
    """平台管理|帮卖管理|帮卖交易列表"""

    def help_sell_list(self, headers=None):
        """帮卖交易列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['help_sell_listings'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformItemsOrdersManagementApi(BaseApi):
    """平台管理|运营中心|订单管理"""

    def order_management_list(self, i=None, headers=None):
        """订单管理列表
         i订单状态 1：待发货2：待取件3：待收货4：已收货5：已完成6：已取消7：已退货

        """
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'status': i}
        response = self.request_handle('post', self.urls['orders_management'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformItemsReturnsManagementApi(BaseApi):
    """平台管理|运营中心|退货管理"""

    def pending_returns_merchant_list(self, headers=None):
        """待退货 商户明细"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'status': "1"}
        response = self.request_handle('post', self.urls['pending_returns_merchant_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def pending_returns_articles_list(self, headers=None):
        """待退货 物品明细"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'status': "1"}
        response = self.request_handle('post', self.urls['returns_articles_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def waiting_for_pickup_articles_list(self, headers=None):
        """待取货 物品明细"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'status': "2"}
        response = self.request_handle('post', self.urls['returns_articles_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def return_finish_out_merchant_list(self, headers=None):
        """退货已出库 批次明细"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'status': "3"}
        response = self.request_handle('post', self.urls['return_finish_merchant_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def return_finish_out_articles_list(self, headers=None):
        """退货已出库 物品明细"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'status': "3"}
        response = self.request_handle('post', self.urls['returns_articles_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def return_finish_merchant_list(self, headers=None):
        """已退货 批次明细"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'status': "4"}
        response = self.request_handle('post', self.urls['return_finish_merchant_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def return_finish_articles_list(self, headers=None):
        """已退货 物品明细"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'status': "4"}
        response = self.request_handle('post', self.urls['returns_articles_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def cancelled_articles_list(self, headers=None):
        """取消退货 物品明细"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'status': "5"}
        response = self.request_handle('post', self.urls['returns_articles_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformItemsToBeSpecifiedApi(BaseApi):
    """平台管理|运营中心|待指定物品"""

    def item_to_be_specified_list(self, headers=None):
        """待指定物品列表"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params(num=1, size=999999), 'inspectionCenterCode': INFO['merchant_id']}
        response = self.request_handle('post', self.urls['items_to_be_specified'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list, index=-1)
        self.make_pkl_file(res)
        return res


class PlatformItemsRuleManagementApi(BaseApi):
    """平台管理|运营中心|规则管理"""

    def rule_management_list(self, headers=None):
        """规则管理列表"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['rule_management'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformListOfDarkAuctionHousesApi(BaseApi):
    """平台管理|卖场管理|暗拍卖场列表"""

    def list_of_dark_auction_houses(self, i=1, headers=None):
        """暗拍卖场列表
        i；1-已上架；2-待上架；3-已下架
        """
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), "marketCategory": "1", "status": i}
        response = self.request_handle('post', self.urls['list_of_direct_shots'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def edit_details(self, headers=None):
        """编辑详情"""
        res = self.get_id()
        headers = headers or self.headers['super']
        data = {"id": res}
        response = self.request_handle('post', self.urls['straight_shot_edit_details'], data=json.dumps(data),  headers=headers)
        return self.get_response_data(response, 'data', dict)

    def view_session_details(self, headers=None):
        """查看场次详情 场次列表"""
        res = self.get_id()
        headers = headers or self.headers['super']
        data = {'erpEndTime': self.get_the_date(days=2), 'erpStartTime': self.get_the_date(), 'marketId': res}
        response = self.request_handle('post', self.urls['straight_shot_view_session_details'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def product_list(self, headers=None):
        """查看场次详情 商品列表"""
        res = self.get_id()
        res_2 = self.get_list_of_sessions_id()
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'marketId': res, 'sessionId': res_2}
        response = self.request_handle('post', self.urls['list_of_dark_auction_houses'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def get_id(self):
        """
        获取id
        i: 可选参数，用于指定不同的状态来获取对应的id
        返回对应状态下的id
        """
        return self._get_field_copy_value('list_of_dark_auction_houses', 'super', 'id')

    # 获取查看场次详情 场次列表id
    def get_list_of_sessions_id(self):
        return self._get_field_copy_value('view_session_details', 'super', 'id')


class PlatformListOfDirectAuctionHousesApi(BaseApi):
    """平台管理|卖场管理|直拍卖场列表"""

    def list_of_stores(self, headers=None, i=None):
        """直拍卖场列表
         i: 上架状态 1已上架 2待上架 3已下架
        """
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'marketCategory': 2, 'status': i}
        response = self.request_handle('post', self.urls['list_of_direct_shots'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def edit_details(self, headers=None):
        """编辑详情"""
        res = self.get_id()
        headers = headers or self.headers['super']
        data = {"id": res}
        response = self.request_handle('post', self.urls['straight_shot_edit_details'], data=json.dumps(data),
                                       headers=headers)
        return self.get_response_data(response, 'data', dict)

    def view_session_details(self, headers=None):
        """查看场次详情 场次列表"""
        res = self.get_id()
        headers = headers or self.headers['super']
        data = {'erpEndTime': self.get_the_date(days=2), 'erpStartTime': self.get_the_date(), 'marketId': res}
        response = self.request_handle('post', self.urls['straight_shot_view_session_details'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def product_list(self, headers=None):
        """查看场次详情 商品列表"""
        res = self.get_id()
        res_2 = self.get_list_of_sessions_id()
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'marketId': res, 'sessionId': res_2}
        response = self.request_handle('post', self.urls['list_of_dark_auction_houses'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    # 获取id
    def get_id(self):
        return self._get_field_copy_value('list_of_stores', 'super', 'id')

    # 获取查看场次详情 场次列表id
    def get_list_of_sessions_id(self):
        return self._get_field_copy_value('view_session_details', 'super', 'id')


class PlatformSalesLookBoardDataApi(BaseApi):
    """平台管理|卖场管理|销售看板数据"""

    def real_time_data(self, headers=None):
        """今日竞拍实时数据"""
        headers = headers or self.headers['super']
        response = self.request_handle('get', self.urls['real_time_data'], headers=headers)
        return self.get_response_data(response, 'data', dict)

    def real_time_list(self, headers=None):
        """规则管理列表"""
        headers = headers or self.headers['super']
        data = {"pageNum": 1, "pageSize": 999}  # 这里没有分页
        response = self.request_handle('post', self.urls['real_time_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    # 获取进行中的场次
    def get_in_progress_num(self):
        return self._get_field_copy_value('real_time_data', 'super', 'auctionCount')

    # 获取进行中的场次
    def get_to_start_num(self):
        return self._get_field_copy_value('real_time_data', 'super', 'waitCount')


class PlatformLogisticsConfigApi(BaseApi):
    """平台管理|物流折扣配置"""

    def logistics_config_list(self, headers=None):
        """物流折扣配置"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['logistics_config'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformLogisticsOrdersListApi(BaseApi):
    """平台管理|订单管理|商户物流订单"""

    def orders_list(self, headers=None):
        """商户物流订单列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['platform_orders_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformMessageReleaseListApi(BaseApi):
    """平台管理|消息管理|消息发布列表"""

    def order_review(self, headers=None):
        """消息发布列表-回收商发布"""
        headers = headers or self.headers['platform']
        data = {"publishSource": "2", "selectType": "1", **self.get_page_params()}
        response = self.request_handle('post', self.urls['message_release_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def release_list(self, headers=None):
        """消息发布列表-平台发布"""
        headers = headers or self.headers['platform']
        data = {"selectType": "1", "publishSource": "1", **self.get_page_params()}
        response = self.request_handle('post', self.urls['message_release_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def msg_records(self, headers=None):
        """消息发布记录"""
        headers = headers or self.headers['platform']
        data = {"selectType": "1", **self.get_page_params()}
        response = self.request_handle('post', self.urls['message_release_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformIntensityFiveGoodsApi(BaseApi):
    """平台管理|同售管理|95分商品列表(运营)"""

    def goods_list(self, headers=None):
        """95分商品列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params(), "platformType": "2"}
        response = self.request_handle('post', self.urls['_95_point_product_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformOrderReviewApi(BaseApi):
    """平台管理|订单管理|订单审核"""

    def order_review(self, headers=None):
        """订单审核"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['platform_audit_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformOrderListApi(BaseApi):
    """平台管理|订单管理|商户订单"""

    def orders_list(self, headers=None):
        """商户订单列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['platform_orders_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformProductManageApi(BaseApi):
    """平台管理|产品管理"""

    def product_manage_list(self, headers=None):
        """产品管理"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params(), "menuCheckStrictly": True}
        response = self.request_handle('post', self.urls['product_manage'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformProductReviewApi(BaseApi):
    """平台管理|同售管理|商品审核"""

    def product_review(self, headers=None):
        """商品审核"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['review_of_goods_sold_together'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def product_review_wait_audit(self, headers=None):
        """商品审核-待审核列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params(), "auditState": "1"}
        response = self.request_handle('post', self.urls['review_of_goods_sold_together'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformPurchaseManageApi(BaseApi):
    """平台管理|商户管理"""

    def manage_list(self, headers=None):
        """商户管理列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['merchant_management'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)

    def manage_list_by_vice(self, headers=None):
        """商户管理列表 帮卖账号搜索"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params(), "name": INFO['vice_sales_customer_name']}
        response = self.request_handle('post', self.urls['merchant_management'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)

    def manage_list_by_main(self, headers=None):
        """商户管理列表 主账号搜索"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params(), "name": INFO['main_username']}
        response = self.request_handle('post', self.urls['merchant_management'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)

    def manage_list_by_camera(self, headers=None):
        """商户管理列表 拍机账号搜索"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params(), "name": INFO['camera_username']}
        response = self.request_handle('post', self.urls['merchant_management'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)

    # 获取vice账号手机号
    def get_phone_vice(self):
        return self._get_field_copy_value('manage_list_by_vice', 'platform', 'phone')

    # 获取主账号手机号
    def get_phone_main(self):
        return self._get_field_copy_value('manage_list_by_main', 'platform', 'phone')

    # 获取主账号商户id
    def get_code(self):
        return self._get_field_copy_value('manage_list_by_main', 'super', 'code')

    # 获取拍机账号商户id
    def get_camera_code(self):
        return self._get_field_copy_value('manage_list_by_camera', 'super', 'code')

    # 获取拍机账号手机号
    def get_phone_camera(self):
        return self._get_field_copy_value('manage_list_by_camera', 'platform', 'phone')


class PlatformQuotationApi(BaseApi):
    """平台管理|报价管理|报价单列表"""

    def quotation_list(self, headers=None):
        """报价单列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['list_of_platform_quotes'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformQuotationCalculateApi(BaseApi):
    """平台管理|报价管理|酷换机计算规则"""

    def calculate_config(self, headers=None):
        """酷换机计算规则"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['cool_calculation_rules'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformQuotationDeductionApi(BaseApi):
    """平台管理|报价管理|配置管理|扣费项管理"""

    def quotation_list(self, headers=None):
        """扣费项管理"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['platform_deduction_item_manage'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformQuotationLevelApi(BaseApi):
    """平台管理|报价管理|配置管理|等级说明"""

    def level_list(self, headers=None):
        """等级说明"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['platform_level_description'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformQuotationQualityApi(BaseApi):
    """平台管理|报价管理|配置管理|成色等级"""

    def quality_list(self, headers=None):
        """成色等级列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['platform_quality_grade_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformQuotationMenuApi(BaseApi):
    """平台管理|报价管理|配置管理|回收菜单"""

    def quotation_menu_list(self, headers=None):
        """回收菜单"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['platform_recycling_menu'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformQuotationRecordsApi(BaseApi):
    """平台管理|报价管理|发布记录"""

    def quotation_records(self, headers=None):
        """发布记录"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['platform_quotation_release_record'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformQuotationRecycleApi(BaseApi):
    """平台管理|报价管理|回收商报价单"""

    def quotation_recycles_list(self, headers=None):
        """回收商报价单"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['platform_recycler_quotation'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformSoldAccountsApi(BaseApi):
    """平台管理|同售管理|同售账号管理"""

    def account_list(self, headers=None):
        """同售账号列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['co_sale_account_management'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformSoldDwGoodsApi(BaseApi):
    """平台管理|同售管理|得物95分|95分商品列表"""

    def de_wu_goods_list(self, headers=None):
        """95分商品列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params(), "platformType": 2}
        response = self.request_handle('post', self.urls['de_wu_orders_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformSoldDwOrdersApi(BaseApi):
    """平台管理|同售管理|得物95分|95分订单列表"""

    def de_wu_orders_list(self, headers=None):
        """95分订单列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['de_wu_orders_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformSoldDwRebackApi(BaseApi):
    """平台管理|得物95分|后验回退列表"""

    def de_wu_re_back_list(self, headers=None):
        """后验回退列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['de_wu_re_back'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformSoldDwSalesApi(BaseApi):
    """平台管理|同售管理|得物95分|售后列表"""

    def de_wu_sales_list(self, headers=None):
        """售后列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params(), "platformType": 2}
        response = self.request_handle('post', self.urls['xy_sales_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformSoldFeeApi(BaseApi):
    """平台管理|同售管理|服务费管理"""

    def sold_fee_list(self, headers=None):
        """服务费管理"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['service_fee_management'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformSoldLogisticsApi(BaseApi):
    """平台管理|同售管理|同售托管|物流列表"""

    def sold_fee_list(self, headers=None):
        """物流列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['sell_the_same_logistics_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformSoldMerchantFeeApi(BaseApi):
    """平台管理|商户基础数据管理|日常费用管理"""

    def merchant_fee_list(self, headers=None):
        """日常费用管理"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['merchant_fee'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformSoldNinetyFiveOrdersApi(BaseApi):
    """平台管理|同售管理|同售托管|95分订单列表"""

    def orders_list(self, headers=None):
        """95分订单列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['de_wu_orders_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformSoldNinetyFiveSalesApi(BaseApi):
    """平台管理|同售管理|同售托管|95分售后列表"""

    def sales_list(self, headers=None):
        """95分售后列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params(), "platformType": 2}
        response = self.request_handle('post', self.urls['xy_sales_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformSoldPayoutOrdersApi(BaseApi):
    """平台管理|同售管理|赔付订单列表"""

    def payout_orders(self, headers=None):
        """赔付订单列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params(), "orderStatus": "0"}
        response = self.request_handle('post', self.urls['payout_orders_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformSoldQualityRecordsApi(BaseApi):
    """平台管理|同售管理|同售托管|质检记录"""

    def quality_records(self, headers=None):
        """质检记录"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['sold_with_quality_inspection_records'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformSoldSendAddressApi(BaseApi):
    """平台管理|同售管理|同售发货地址管理"""

    def send_address(self, headers=None):
        """同售发货地址管理"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['co_sale_shipping_address_manage'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformSoldSmsListApi(BaseApi):
    """平台管理|发送短信记录"""

    def sms_list(self, headers=None):
        """服务费管理"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['发送短信记录'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformSoldXianYuOrdersApi(BaseApi):
    """平台管理|同售管理|闲鱼订单列表(运营)"""

    def xian_yu_orders(self, headers=None):
        """闲鱼订单列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['idle_fish_orders'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformWalletConfigApi(BaseApi):
    """平台管理|钱包配置"""

    def wallet_config_list(self, headers=None):
        """钱包配置"""
        headers = headers or self.headers['platform']
        response = self.request_handle('post', self.urls['wallet_config'], data=json.dumps({}), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformXianYuGoodsApi(BaseApi):
    """平台管理|同售管理|闲鱼严选|商品列表"""

    def goods_list(self, headers=None):
        """商品列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['xy_goods_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformXianYuOrdersApi(BaseApi):
    """平台管理|同售管理|闲鱼严选|订单列表"""

    def orders_list(self, headers=None):
        """订单列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['idle_fish_orders'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformXianYuSalesApi(BaseApi):
    """平台管理|同售管理|闲鱼严选|售后列表"""

    def sales_list(self, headers=None):
        """售后列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['xy_sales_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformYzAppApi(BaseApi):
    """平台管理|壹准APP功能管理"""

    def sold_fee_list(self, headers=None):
        """壹准APP功能管理"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['yz_app'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformsBannerConfigApi(BaseApi):
    """平台管理|壹准速收|横幅配置"""

    def banners_list(self, headers=None):
        """横幅配置"""
        if headers is None:
            headers = self.headers['platform']
        data = {**self.get_page_params(), "configType": "1"}
        response = self.request_handle('post', self.urls['banner_config'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformsImListApi(BaseApi):
    """平台管理|壹准速收|会话管理|聊天记录列表"""

    def im_list(self, headers=None):
        """聊天记录列表"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['chat_history_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformsMerchantApi(BaseApi):
    """平台管理|壹准速收|回收商管理"""

    def merchant_list(self, headers=None):
        """商家管理"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params(), "selectType": "2"}
        response = self.request_handle('post', self.urls['quick_collection_merchant_manage'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformsOrdersApi(BaseApi):
    """平台管理|壹准速收|回收订单"""

    def orders_list(self, headers=None):
        """回收订单"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params(), "userType": "1"}
        response = self.request_handle('post', self.urls['collect_your_order_quickly'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformRecycleMerchantsApi(BaseApi):
    """平台管理|壹准速收|回收商管理"""

    def sign_list(self, headers=None):
        """回收商管理"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['recycle_merchants'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformServiceFeeApi(BaseApi):
    """平台管理|壹准速收|服务费配置"""

    def orders_list(self, headers=None):
        """服务费配置"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['service_fee'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformSignReceiveApi(BaseApi):
    """平台管理|壹准速收|到货签收"""

    def sign_list(self, headers=None):
        """到货签收"""
        headers = headers or self.headers['platform']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['sign_receive'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformInspectionCenterManageApi(BaseApi):
    """平台管理|运营中心|验机中心管理"""

    def list_of_inspection_centers(self, headers=None, num=1, size=1000):
        """验机中心管理列表"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params(num, size), 'operationCenterTenantId': INFO['merchant_id']}
        response = self.request_handle('post', self.urls['check_center_management'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    # 获取验机中心id
    def get_check_the_center_id(self):
        return self._get_field_copy_value('list_of_inspection_centers', 'super', 'id')

    # 获取验机中心code
    def get_operation_center_tenant_id(self):
        return self._get_field_copy_value('list_of_inspection_centers', 'super', 'operationCenterTenantId')

    # 获取验机中心名称
    def get_operation_center_name(self):
        return self._get_field_copy_value('list_of_inspection_centers', 'super', 'operationCenterName')


class PlatformGuaranteedSalePriceListApi(BaseApi):
    """平台管理|机型价格|Tob保卖|价格列表"""

    def __init__(self):
        super().__init__()
        self.model_price_template = PlatformModelPriceTemplateApi()

    def price_list(self, headers=None):
        """价格列表"""
        res = self.model_price_template.get_id()
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'productType': "1", 'quotationPriceTemplateId': res}
        response = self.request_handle('post', self.urls['guaranteed_sale_price_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformSuShouSalePriceListApi(BaseApi):
    """平台管理|机型价格|ToC速收|价格列表"""

    def __init__(self):
        super().__init__()
        self.model_price_template = PlatformModelPriceTemplateApi()

    def price_list(self, headers=None):
        """价格列表"""
        res = self.model_price_template.get_id()
        headers = headers or self.headers['super']
        data = {**self.get_page_params(), 'productType': "1", 'quotationPriceTemplateId': res}
        response = self.request_handle('post', self.urls['su_shou_sale_price_list'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class PlatformModelPriceTemplateApi(BaseApi):
    """平台管理|机型价格|价格模板"""

    def list_of_price_templates(self, headers=None):
        """价格模板列表"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['model_price_template'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    # 获取id
    def get_id(self):
        return self._get_field_copy_value('list_of_price_templates', 'super', 'id', index=2)


class PlatformFranchiseesReleaseRecordsApi(BaseApi):
    """平台管理|机型价格|发布记录|加盟商发布记录"""


class PlatformPlatformReleaseRecordApi(BaseApi):
    """平台管理|机型价格|发布记录|平台发布记录"""


class PlatformGuaranteeSaleCalculationRulesApi(BaseApi):
    """平台管理|机型价格|Tob保卖|计算规则"""


class PlatformGuaranteeSalesAndDeductionManageApi(BaseApi):
    """平台管理|机型价格|Tob保卖|增扣项管理"""


class PlatformTradingGoodsCenterManageApi(BaseApi):
    """平台管理-交易中心"""

    def sale_goods_list(self, headers=None, i=None):
        """销售商品交易"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params()}
        if i:
            data['articlesStatus'] = i
        response = self.request_handle('post', self.urls['platform_trading_center_sales_goods'], data=json.dumps(data),
                                       headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


if __name__ == '__main__':
    api = PlatformGrievanceManageApi()
    result = api.statement_list()
    print(json.dumps(result, indent=4, ensure_ascii=False))
