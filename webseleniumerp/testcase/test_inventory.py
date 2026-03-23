# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.decorators import cached
from common.import_case import *
from config.constant import DICT_DATA


class TestInventoryAddressManage(BaseCase, unittest.TestCase):
    """库存管理|出库管理|地址管理"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.InventoryAddressManageRequest()
        else:
            return inventory_p.InventoryAddressManagePages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0add_address(self):
        """[新增]-通用业务新增地址"""
        case = self.common_operations(login='idle')
        case.add_address()
        res = [lambda: self.pc.inventory_address_manage_assert(headers='idle', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_delete_address(self):
        """[删除]-删除地址"""
        self.pre.operations(data=['HH1'])
        case = self.common_operations()
        case.delete_address()

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_edit_address(self):
        """[编辑]-修改地址信息"""
        self.pre.operations(data=['HH1'])
        case = self.common_operations()
        case.edit_address()
        res = [lambda: self.pc.inventory_address_manage_assert(headers='idle', createTime='now')]
        self.assert_all(*res)


class TestInventoryHandOverGoodsRecords(BaseCase, unittest.TestCase):
    """库存管理|移交接收管理|移交记录"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.InventoryHandOverGoodsRecordsRequest()
        else:
            return None

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0hand_over_records_search_by_imei(self):
        """[搜索]-imei查询"""
        case = self.common_operations(login='main')
        case.hand_over_records_search_by_imei()
        obj = cached('imei')
        res = [lambda: self.pc.inventory_handover_record_assert(data='a', imei=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_hand_over_records_search_by_order_no(self):
        """[搜索]-移交单号查询"""
        case = self.common_operations()
        case.hand_over_records_search_by_order_no()
        obj = cached('orderNo')
        res = [lambda: self.pc.inventory_handover_record_assert(orderNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_hand_over_records_search_by_status(self):
        """[搜索]-移交单状态查询"""
        list_data = DICT_DATA['b']
        for item in list_data:
            case = self.common_operations()
            case.hand_over_records_search_by_status(item)
            obj = cached('status')
            res = [lambda: self.pc.inventory_handover_record_assert(i=obj, status=obj)]
            self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_hand_over_records_search_by_reason_type(self):
        """[搜索]-移交原因查询"""
        type_ary = DICT_DATA['e']
        for item in type_ary:
            case = self.common_operations()
            case.hand_over_records_search_by_reason_type(item['key'])
            obj = cached('reasonType')
            res = [lambda: self.pc.inventory_handover_record_assert(j=obj, reasonType=obj)]
            self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_hand_over_records_search_by_person(self):
        """[搜索]-移交人查询"""
        case = self.common_operations()
        case.hand_over_records_search_by_person()
        obj = cached('distributorId')
        res = [lambda: self.pc.inventory_handover_record_assert(distributorId=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_hand_over_records_search_by_receive_id(self):
        """[搜索]-接收人查询"""
        case = self.common_operations()
        case.hand_over_records_search_by_receive_id()
        obj = cached('receiveId')
        res = [lambda: self.pc.inventory_handover_record_assert(receiveId=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_hand_over_records_search_by_receive_id(self):
        """[搜索]-接收人查询"""
        case = self.common_operations()
        case.hand_over_records_search_by_receive_id()
        obj = cached('receiveId')
        res = [lambda: self.pc.inventory_handover_record_assert(receiveId=obj)]
        self.assert_all(*res)


class TestInventoryHandOverGoods(BaseCase, unittest.TestCase):
    """库存管理|移交接收管理|移交物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.InventoryHandOverGoodsRequest()
        else:
            return inventory_p.InventoryHandOverGoodsPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0hand_over_goods(self):
        """[移交]-移交物品给库存"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations(login='main')
        case.hand_over_goods()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_import_hand_over_goods(self):
        """[导入物品]-移交物品给库存"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.import_hand_over_goods()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)


class TestInventoryItemSignWarehousing(BaseCase, unittest.TestCase):
    """库存管理|入库管理|物品签收入库"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.InventoryItemSignWarehousingRequest()
        else:
            return inventory_p.InventoryItemSignWarehousingPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0sign_for_receipt(self):
        """[签收入库]-单个物品签收-暂不移交"""
        self.pre.operations(data=['FA2'])
        case = self.common_operations(login='main')
        case.sign_for_receipt()
        res = [lambda: self.pc.inventory_logistics_list_assert(statusStr='已分拣', businessTime='now',
                                                               sortationTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_import_sign_for_receipt(self):
        """[签收入库]导入入库物品-单个物品签收-暂不移交"""
        self.pre.operations(data=['FA2'])
        case = self.common_operations()
        case.import_sign_for_receipt()
        res = [lambda: self.pc.inventory_logistics_list_assert(statusStr='已分拣', businessTime='now',
                                                               sortationTime='now')]
        self.assert_all(*res)


class TestInventoryLogisticsList(BaseCase, unittest.TestCase):
    """库存管理|入库管理|物流列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.InventoryLogisticsListRequest()
        else:
            return None

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0logistics_list_search_by_logistics_no(self):
        """[搜索]-物流单号搜索"""
        case = self.common_operations(login='main')
        case.logistics_list_search_by_logistics_no()
        obj = cached('logisticsNo')
        res = [lambda: self.pc.inventory_logistics_list(logisticsNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_logistics_list_search_by_imei(self):
        """[搜索]-imei搜索"""
        case = self.common_operations()
        case.logistics_list_search_by_imei()
        obj = cached('articlesNo')
        res = [lambda: self.pc.inventory_logistics_list(data='a', articlesNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_logistics_list_search_by_platform_articles_no(self):
        """[搜索]-平台物品编号搜索todo"""
        case = self.common_operations()
        case.logistics_list_search_by_platform_articles_no()
        obj = cached('platformArticlesNo')
        print('==obj:', obj)
        res = [lambda: self.pc.inventory_logistics_list(i=obj, data='a', platformArticlesNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_logistics_list_search_by_business_no(self):
        """[搜索]-业务单号搜索"""
        case = self.common_operations()
        case.logistics_list_search_by_business_no()
        obj = cached('businessNo')
        res = [lambda: self.pc.inventory_logistics_list(data='a', businessNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_logistics_list_search_by_sortation_status(self):
        """[搜索]-业务单号搜索"""
        ary_data = DICT_DATA['b']
        for item in ary_data:
            case = self.common_operations()
            case.logistics_list_search_by_sortation_status(item)
            obj = cached('status')
            res = [lambda: self.pc.inventory_logistics_list(k=obj, status=obj)]
            self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_logistics_list_search_by_sortation_id(self):
        """[搜索]-分拣人搜索"""
        case = self.common_operations()
        case.logistics_list_search_by_sortation_id()
        obj = cached('userName')
        res = [lambda: self.pc.inventory_logistics_list(userName=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_logistics_list_search_by_date(self):
        """[搜索]-分拣人搜索"""
        case = self.common_operations()
        case.logistics_list_search_by_date()
        res = [lambda: self.pc.inventory_logistics_list(sortationTime='now')]
        self.assert_all(*res)


class TestInventoryList(BaseCase, unittest.TestCase):
    """库存管理|库存列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.InventoryListRequest()
        else:
            return inventory_p.InventoryListPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0sale_out_of_warehouse_has(self):
        """[物品详情]-销售信息tab-更新已销售-已收款出库"""
        self.pre.operations(data=['FA1', 'HC1'])
        case = self.common_operations(login='main')
        case.sale_out_of_warehouse_has()
        res = [lambda: self.pc.sell_sale_item_list_assert(saleTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sale_out_of_warehouse_not(self):
        """[物品详情]-销售信息tab-更新已销售-未收款出库"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.sale_out_of_warehouse_not()
        res = [lambda: self.pc.sell_sale_item_list_assert(saleTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_return_after_sale_has(self):
        """[物品详情]-销售信息-销售售后-退货已收货"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2'])
        case = self.common_operations()
        case.return_after_sale_has()
        res = [lambda: self.pc.sell_after_sales_list_assert(data='a', createTime='now', saleTypeStr='退货')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_return_after_sale_not(self):
        """[物品详情]-销售信息-销售售后-退货未收货"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2'])
        case = self.common_operations()
        case.return_after_sale_not()
        res = [lambda: self.pc.sell_after_sales_list_assert(data='a', createTime='now', saleTypeStr='退货')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_return_only_parts_has(self):
        """[物品详情]-销售信息-销售售后-仅退配件已收货"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2'])
        case = self.common_operations()
        case.return_only_parts_has()
        res = [lambda: self.pc.sell_after_sales_list_assert(createTime='now', saleTypeStr='仅退配件')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_return_only_parts_not(self):
        """[物品详情]-销售信息-销售售后-仅退配件未收货"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2'])
        case = self.common_operations()
        case.return_only_parts_not()
        res = [lambda: self.pc.sell_after_sales_list_assert(data='a', createTime='now', saleTypeStr='仅退配件')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_price_adjustment_after_sales(self):
        """[物品详情]-销售信息-销售售后-调价"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2'])
        case = self.common_operations()
        case.price_adjustment_after_sales()
        res = [lambda: self.pc.sell_after_sales_list_assert(createTime='now', saleTypeStr='调价')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_refund_only_after_purchase(self):
        """[物品详情]-采购信息-仅退款"""
        self.pre.operations(data=['FA2'])
        case = self.common_operations()
        case.refund_only_after_purchase()
        res = [lambda: self.pc.purchase_order_list_assert(stateStr='已取消', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_item_info_edit(self):
        """[物品详情]-编辑-物品信息修改"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.item_info_edit()
        res = [lambda: self.pc.inventory_list_assert(data='b', time='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_transfer_purchase_special(self):
        """[移交]库存移交库管-采购售后"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.inventory_transfer_purchase_special()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='待接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_transfer_quality_special(self):
        """[移交]库存移交库管-质检"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.inventory_transfer_quality_special()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='待接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_transfer_repair_special(self):
        """[移交]库存移交库管-维修"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.inventory_transfer_repair_special()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='待接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_transfer_sell_special(self):
        """[移交]库存移交库管-销售"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.inventory_transfer_sell_special()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='待接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_transfer_send_special(self):
        """[移交]库存移交库管-送修"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.inventory_transfer_send_special()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='待接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_transfer_purchase_main(self):
        """[移交]库存移交自己-采购售后"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.inventory_transfer_purchase_main()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_transfer_quality_main(self):
        """[移交]库存移交自己-质检"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.inventory_transfer_quality_main()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_transfer_repair_main(self):
        """[移交]库存移交自己-维修"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.inventory_transfer_repair_main()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_transfer_sell_main(self):
        """[移交]库存移交自己-销售"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.inventory_transfer_sell_main()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_transfer_send_main(self):
        """[移交]库存移交自己-送修-todo"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.inventory_transfer_send_main()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_list_search_by_imei(self):
        """[搜索]-imei查询"""
        case = self.common_operations()
        case.inventory_list_search_by_imei()
        obj = cached('imei')
        res = [lambda: self.pc.inventory_list_assert(imei=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_list_search_by_supplier(self):
        """[搜索]-供应商查询"""
        case = self.common_operations()
        case.inventory_list_search_by_supplier()
        obj = cached('supplierId')
        res = [lambda: self.pc.inventory_list_assert(supplierId=obj, createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_list_search_by_purchaser(self):
        """[搜索]-采购人员查询"""
        case = self.common_operations()
        case.inventory_list_search_by_purchaser()
        obj = cached('purchaseId')
        res = [lambda: self.pc.inventory_list_assert(purchaseId=obj, createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_list_search_by_type_id(self):
        """[搜索]-品类查询"""
        type_ary = DICT_DATA['d']
        for i in type_ary:
            case = self.common_operations()
            case.inventory_list_search_by_type_id(i)
            obj = cached('articlesTypeId')
            res = [lambda: self.pc.inventory_list_assert(t=i, articlesTypeId=obj)]
            self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_list_search_by_purchase_date(self):
        """[搜索]-采购日期查询"""
        case = self.common_operations()
        case.inventory_list_search_by_purchase_date()
        res = [lambda: self.pc.inventory_list_assert(createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_list_search_by_saler(self):
        """[搜索]-销售人员查询"""
        case = self.common_operations()
        case.inventory_list_search_by_saler()
        obj = cached('belongId')
        res = [lambda: self.pc.inventory_list_assert(belongId=obj, createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_list_search_by_sale_custom(self):
        """[搜索]-销售客户查询"""
        case = self.common_operations()
        case.inventory_list_search_by_sale_custom()
        obj = cached('salesChannelNo')
        res = [lambda: self.pc.inventory_list_assert(salesChannelNo=obj, createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_list_search_by_articles_state(self):
        """[搜索]-物品状态查询"""
        type_ary = DICT_DATA['a']
        for item in type_ary:
            case = self.common_operations()
            case.inventory_list_search_by_articles_state(item)
            result = cached('articlesState')
            res = [lambda: self.pc.inventory_list_assert(j=result, articlesState=result)]
            self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_list_search_by_inventory_status(self):
        """[搜索]-库存状态查询---test-zxp"""
        type_ary = DICT_DATA['b']
        for item in type_ary:
            case = self.common_operations()
            case.inventory_list_search_by_inventory_status(item)
            obj = cached('inventoryStatus')
            res = [lambda: self.pc.inventory_list_assert(i=obj, inventoryStatus=obj)]
            self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_list_search_by_warehouse_id(self):
        """[搜索]-仓库查询"""
        case = self.common_operations()
        case.inventory_list_search_by_warehouse_id()
        obj = cached('warehouseId')
        res = [lambda: self.pc.inventory_list_assert(warehouseId=obj, createTime='now')]
        self.assert_all(*res)


class TestInventoryNewItem(BaseCase, unittest.TestCase):
    """库存管理|入库管理|物流签收入库"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.InventoryNewItemRequest()
        else:
            return inventory_p.InventoryNewItemPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0logistics_signature_for_receipt(self):
        """[签收入库]-暂不移交入库"""
        self.pre.operations(data=['FA2'])
        case = self.common_operations(login='main')
        case.logistics_signature_for_receipt()
        res = [lambda: self.pc.inventory_logistics_list_assert(statusStr='已分拣', businessTime='now', sortationTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_help_sell_logistics_signature_for_receipt(self):
        """[签收入库]-帮卖订单-暂不移交入库"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA4', 'GA5'])
        case = self.common_operations()
        case.help_sell_logistics_signature_for_receipt()
        res = [lambda: self.pc.inventory_logistics_list_assert(statusStr='已分拣', businessTime='now', sortationTime='now')]
        self.assert_all(*res)


class TestInventoryOutboundOrdersList(BaseCase, unittest.TestCase):
    """库存管理|出库管理|仅出库订单列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.InventoryOutboundOrdersListRequest()
        else:
            return inventory_p.InventoryOutboundOrdersListPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0return_outgoing_items_warehousing(self):
        """[出库物品退回]-直接入库"""
        self.pre.operations(data=['FA1', 'HC1', 'HE1'])
        case = self.common_operations(login='main')
        case.return_outgoing_items_warehousing()
        res = [lambda: self.pc.inventory_outbound_orders_list_assert(data='a', returnTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_return_outgoing_items_route(self):
        """[出库物品退回]-退回在途"""
        self.pre.operations(data=['FA1', 'HC1', 'HE1'])
        case = self.common_operations()
        case.return_outgoing_items_route()
        res = [lambda: self.pc.inventory_outbound_orders_list_assert(data='a', returnTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_outbound_sales_only_received(self):
        """[仅出库销售]-已收款确认"""
        self.pre.operations(data=['FA1', 'HC1', 'HE1'])
        case = self.common_operations()
        case.outbound_sales_only_received()
        res = [lambda: self.pc.inventory_outbound_orders_list_assert(outTime='now', orderNo='Ck')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_outbound_sales_only_uncollected(self):
        """[仅出库销售]-未收款确认"""
        self.pre.operations(data=['FA1', 'HC1', 'HE1'])
        case = self.common_operations()
        case.outbound_sales_only_uncollected()
        res = [lambda: self.pc.inventory_outbound_orders_list_assert(outTime='now', orderNo='Ck')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_create_an_outbound_only_order(self):
        """[新建订单]"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.create_an_outbound_only_order()
        res = [lambda: self.pc.inventory_outbound_orders_list_assert(outTime='now', orderNo='Ck')]
        self.assert_all(*res)


class TestPurchaseAndSellOut(BaseCase, unittest.TestCase):
    """库存管理|出库管理|采购售后出库"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.InventoryPurchaseAndSellOutRequest()
        else:
            return inventory_p.InventoryPurchaseAndSellOutPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0purchase_after_sales_warehouse(self):
        """[采购售后出库]-普通快递-添加物品出库"""
        self.pre.operations(data=['FA1', 'HC6'])
        case = self.common_operations(login='main')
        case.purchase_after_sales_warehouse()
        res = [lambda: self.pc.purchase_after_sales_list_assert(saleStateStr='采购售后中', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_import_purchase_and_sell_out(self):
        """[采购售后出库]-普通快递-导入物品出库"""
        self.pre.operations(data=['FA1', 'HC6'])
        case = self.common_operations()
        case.import_purchase_and_sell_out()
        res = [lambda: self.pc.purchase_after_sales_list_assert(saleStateStr='采购售后中', createTime='now')]
        self.assert_all(*res)


class TestInventoryReceiveItem(BaseCase, unittest.TestCase):
    """库存管理|移交接收管理|接收物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.InventoryReceiveItemRequest()
        else:
            return inventory_p.InventoryReceiveItemPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0item_acceptance_repair_status(self):
        """[物品接收tab]-移交维修-接收"""
        self.pre.operations(data=['FA1', 'HC4'])
        case = self.common_operations(login='main')
        case.item_acceptance_repair_status()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_receive_item_search_by_imei(self):
        """[搜索]-imei查询"""
        case = self.common_operations()
        case.inventory_receive_item_search_by_imei()
        obj = cached('imei')
        res = [lambda: self.pc.inventory_receive_items_assert(imei=obj, deliveryTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_receive_item_search_by_articles_type_id(self):
        """[搜索]-品类查询"""
        type_ary = DICT_DATA['d']
        for item in type_ary:
            case = self.common_operations()
            case.inventory_receive_item_search_by_articles_type_id(item['key'])
            obj = cached('articlesType')
            res = [lambda: self.pc.inventory_receive_items_assert(j=item['key'], articlesTypeName=item['val'])]
            self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_receive_item_search_by_brand_id(self):
        """[搜索]-品牌查询"""
        case = self.common_operations()
        case.inventory_receive_item_search_by_brand_id()
        obj = cached('brandName')
        res = [lambda: self.pc.inventory_receive_items_assert(brandName=obj, deliveryTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_receive_item_search_by_model_name(self):
        """[搜索]-机型查询"""
        case = self.common_operations()
        case.inventory_receive_item_search_by_model_name()
        obj = cached('modelName')
        res = [lambda: self.pc.inventory_receive_items_assert(modelName=obj, deliveryTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_receive_item_search_by_articles_state(self):
        """[搜索]-物品状态查询"""
        ary_data = DICT_DATA['f']
        for item in ary_data:
            case = self.common_operations()
            case.inventory_receive_item_search_by_articles_state(item['key'], item['val'])
            obj = cached('articlesStateStr')
            res = [lambda: self.pc.inventory_receive_items_assert(i=item['key'], articlesStateStr=obj)]
            self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_receive_item_search_by_hand_over_person(self):
        """[搜索]-移交人查询"""
        case = self.common_operations()
        case.inventory_receive_item_search_by_hand_over_person()
        obj = cached('operateName')
        res = [lambda: self.pc.inventory_receive_items_assert(operateName=obj, deliveryTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_receive_item_search_by_receive_person(self):
        """[搜索]-接收人查询"""
        case = self.common_operations()
        case.inventory_receive_item_search_by_receive_person()
        obj = cached('reUserName')
        res = [lambda: self.pc.inventory_receive_items_assert(reUserName=obj, deliveryTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_receive_item_search_by_reason_type(self):
        """[搜索]-移交原因查询"""
        type_ary = DICT_DATA['e']
        for item in type_ary:
            case = self.common_operations()
            case.inventory_receive_item_search_by_reason_type(item['key'])
            obj = cached('reasonType')
            res = [lambda: self.pc.inventory_receive_items_assert(k=obj, reasonType=obj)]
            self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_receive_item_search_by_reason_time(self):
        """[搜索]-移交时间查询"""
        self.pre.operations(data=['FA1', 'HC4'])
        case = self.common_operations()
        case.inventory_receive_item_search_by_reason_time()
        res = [lambda: self.pc.inventory_receive_items_assert(deliveryTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_receive_item_search_by_receive_order_no(self):
        """[搜索]-移交单号查询"""
        self.pre.operations(data=['FA1', 'HC4'])
        case = self.common_operations()
        case.inventory_receive_item_search_by_receive_order_no()
        obj = cached('orderNo')
        res = [lambda: self.pc.inventory_receive_items_assert(orderNo=obj, deliveryTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_receive_order_no_search_by_imei(self):
        """[搜索]-imei查询"""
        self.pre.operations(data=['FA1', 'HC4'])
        case = self.common_operations()
        case.inventory_receive_order_no_search_by_imei()
        obj = cached('imei')
        res = [lambda: self.pc.inventory_receive_items_assert(data='b', imei=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_receive_order_no_search_by_order_no(self):
        """[搜索]-移交单号查询"""
        self.pre.operations(data=['FA1', 'HC4'])
        case = self.common_operations()
        case.inventory_receive_order_no_search_by_order_no()
        obj = cached('orderNo')
        res = [lambda: self.pc.inventory_receive_items_assert(data='a', orderNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_receive_order_no_search_by_status(self):
        """[搜索]-移交单状态查询"""
        self.pre.operations(data=['FA1', 'HC4'])
        case = self.common_operations()
        case.inventory_receive_order_no_search_by_status()
        obj = cached('status')
        res = [lambda: self.pc.inventory_receive_items_assert(data='a', status=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_receive_order_no_search_by_reason_type(self):
        """[搜索]-移交原因查询"""
        type_ary = DICT_DATA['e']
        for item in type_ary:
            case = self.common_operations()
            case.inventory_receive_order_no_search_by_reason_type(item['key'])
            obj = cached('reasonType')
            res = [lambda: self.pc.inventory_receive_items_assert(data='a', i=obj, reasonType=obj)]
            self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_receive_order_no_search_by_distributor(self):
        """[搜索]-移交人查询"""
        self.pre.operations(data=['FA1', 'HC4'])
        case = self.common_operations()
        case.inventory_receive_order_no_search_by_distributor()
        obj = cached('distributorId')
        res = [lambda: self.pc.inventory_receive_items_assert(data='a', distributorId=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_receive_order_no_search_by_user_id(self):
        """[搜索]-接收人查询"""
        self.pre.operations(data=['FA1', 'HC4'])
        case = self.common_operations()
        case.inventory_receive_order_no_search_by_user_id()
        obj = cached('receiveId')
        res = [lambda: self.pc.inventory_receive_items_assert(data='a', receiveId=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_inventory_receive_order_no_search_by_date(self):
        """[搜索]-移交时间查询"""
        self.pre.operations(data=['FA1', 'HC4'])
        case = self.common_operations()
        case.inventory_receive_order_no_search_by_date()
        res = [lambda: self.pc.inventory_receive_items_assert(data='a', createTime='now')]
        self.assert_all(*res)


class TestInventorySaleOutWarehouse(BaseCase, unittest.TestCase):
    """库存管理|出库管理|销售出库"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.InventorySaleOutWarehouseRequest()
        else:
            return inventory_p.InventorySaleOutWarehousePages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0sales_out_warehouse_received(self):
        """[销售出库tab]-普通快递-已收款-添加物品出库"""
        self.pre.operations(data=['FA1', 'HC1'])
        case = self.common_operations(login='main')
        case.sales_out_warehouse_received()
        res = [lambda: self.pc.sell_sale_item_list_assert(salesOrder='SA', articlesStateStr='已销售', saleTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sales_out_warehouse_not_received(self):
        """[销售出库tab]-普通快递-未收款-添加物品出库"""
        self.pre.operations(data=['FA1', 'HC1'])
        case = self.common_operations()
        case.sales_out_warehouse_not_received()
        res = [lambda: self.pc.sell_sale_item_list_assert(salesOrder='SA', articlesStateStr='已销售', saleTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_import_sell_get_out(self):
        """[销售出库tab]-普通快递-未收款-导入物品出库"""
        self.pre.operations(data=['FA1', 'HC1'])
        case = self.common_operations()
        case.import_sell_get_out()
        res = [lambda: self.pc.sell_sale_item_list_assert(salesOrder='SA', articlesStateStr='已销售', saleTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_distribution(self):
        """[铺货预售出库tab]-铺货-普通快递-已收款-添加物品出库"""
        self.pre.operations(data=['FA1', 'HC1'])
        case = self.common_operations()
        case.sell_distribution()
        res = [lambda: self.pc.sell_order_list_for_sale_assert(batchNo='SJ', shelfTime='now', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_import_sell_distribution(self):
        """[铺货预售出库tab]-铺货-普通快递-已收款-导入物品出库"""
        self.pre.operations(data=['FA1', 'HC1'])
        case = self.common_operations()
        case.import_sell_distribution()
        res = [lambda: self.pc.sell_order_list_for_sale_assert(batchNo='SJ', shelfTime='now', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_advance_sale(self):
        """[铺货预售出库tab]-预售-普通快递-添加物品出库"""
        self.pre.operations(data=['FA1', 'HC1'])
        case = self.common_operations()
        case.sell_advance_sale()
        res = [lambda: self.pc.sell_order_list_for_sale_assert(batchNo='SJ', shelfTime='now', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_import_sell_advance_sale(self):
        """[铺货预售出库tab]-预售-普通快递-导入物品出库"""
        self.pre.operations(data=['FA1', 'HC1'])
        case = self.common_operations()
        case.import_sell_advance_sale()
        res = [lambda: self.pc.sell_order_list_for_sale_assert(batchNo='SJ', shelfTime='now', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_outbound_accessories(self):
        """[销售出库tab]-添加赠送配件-添加物品出库"""
        self.pre.operations(data=['FA1', 'HC1'])
        case = self.common_operations()
        case.sell_outbound_accessories()
        res = [lambda: self.pc.attachment_gift_details_assert(createTime='now', orderNo='SA')]
        self.assert_all(*res)  # 配件管理|配件统计|赠送明细

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_0sales_out_warehouse_help_sell(self):
        """[销售出库tab]-帮卖订单-普通快递-已收款-添加物品出库"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA4', 'GA7', 'HA1', 'GB1'])
        case = self.common_operations()
        case.sales_out_warehouse_help_sell()
        res = [lambda: self.pc.sell_sale_item_list_assert(headers='vice', salesOrder='SA', saleTime='now')]
        self.assert_all(*res)


class TestInventorySellAfterSaleDelivery(BaseCase, unittest.TestCase):
    """库存管理|出库管理|销售售后出库"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.InventorySellAfterSaleDeliveryRequest()
        else:
            return inventory_p.InventorySellAfterSaleDeliveryPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0sell_get_out(self):
        """[售后类型换货]-普通快递-添加物品出库"""
        self.pre.operations(data=['FA1', 'FA1', 'HC1', 'HB2', 'IA1'])
        case = self.common_operations(login='main')
        case.sell_get_out()
        res = [lambda: self.pc.sell_after_sales_list_assert(updateTime='now', saleTypeStr='换货', articlesStatusStr='待分货')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_after_sale_refusal_return(self):
        """[售后类型拒退]-普通快递-添加物品出库"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2', 'IA1'])
        case = self.common_operations()
        case.sell_after_sale_refusal_return()
        res = [lambda: self.pc.sell_after_sales_list_assert(updateTime='now', saleTypeStr='拒退退回', articlesStatusStr='已销售')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_sell_after_sale_repair(self):
        """[售后类型返修]-普通快递-添加物品出库"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2', 'IA1'])
        case = self.common_operations()
        case.sell_after_sale_repair()
        res = [lambda: self.pc.sell_after_sales_list_assert(updateTime='now', saleTypeStr='返修', articlesStatusStr='已销售')]
        self.assert_all(*res)


class TestInventorySendOutRepair(BaseCase, unittest.TestCase):
    """库存管理|出库管理|送修出库"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.InventorySendOutRepairRequest()
        else:
            return inventory_p.InventorySendOutRepairPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0send_out_the_warehouse(self):
        """[送修出库]-普通快递-添加物品出库"""
        self.pre.operations(data=['FA1', 'HC9'])
        case = self.common_operations(login='main')
        case.send_out_the_warehouse()
        res = [lambda: self.pc.send_been_sent_repair(repairStatusName='送修中', repairTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_import_send_out_for_repair(self):
        """[送修出库]-普通快递-导入物品出库"""
        self.pre.operations(data=['FA1', 'HC9'])
        case = self.common_operations()
        case.import_send_out_for_repair()
        res = [lambda: self.pc.send_been_sent_repair(repairStatusName='送修中', repairTime='now')]
        self.assert_all(*res)


class TestInventoryStockCount(BaseCase, unittest.TestCase):
    """库存管理|库存盘点"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.InventoryStockCountRequest()
        else:
            return inventory_p.InventoryStockCountPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0completed_inventory_count(self):
        """[新建盘点]-开始盘点-添加物品完成盘点"""
        case = self.common_operations(login='main')
        case.completed_inventory_count()
        res = [lambda: self.pc.inventory_count_assert(stockResult=1, updateTime='now', stockNo='PD')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_delete_count(self):
        """[删除]-删除盘点"""
        self.pre.operations(data=['HF1'])
        case = self.common_operations()
        case.delete_count()


class TestInventoryStockTransfer(BaseCase, unittest.TestCase):
    """库存管理|仓库调拨"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return inventory_r.InventoryStoreTransferRequest()
        else:
            return inventory_p.InventoryStoreTransferPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0new_allocation(self):
        """[新增调拨]-普通快递-搜索添加物品调拨"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations(login='main')
        case.new_allocation()
        res = [lambda: self.pc.inventory_warehouse_allocation_assert(createTime='now', statusStr='待接收')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_import_new_allot(self):
        """[新增调拨]-普通快递-导入物品调拨"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.import_new_allot()
        res = [lambda: self.pc.inventory_warehouse_allocation_assert(createTime='now', statusStr='待接收')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_select_add_item_transfer(self):
        """[新增调拨]-普通快递-选择添加物品调拨"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.select_add_item_transfer()
        res = [lambda: self.pc.inventory_warehouse_allocation_assert(createTime='now', statusStr='待接收')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_receive(self):
        """[接收]-暂不操作接收"""
        self.pre.operations(data=['FA1', 'HD1'])
        case = self.common_operations()
        case.receive()
        res = [lambda: self.pc.inventory_warehouse_allocation_assert(createTime='now', statusStr='已完成')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_cancel(self):
        """[撤销]-确认撤销"""
        self.pre.operations(data=['FA1', 'HD1'])
        case = self.common_operations()
        case.cancel()
        res = [lambda: self.pc.inventory_warehouse_allocation_assert(createTime='now', statusStr='已撤销')]
        self.assert_all(*res)


if __name__ == '__main__':
    unittest.main()
