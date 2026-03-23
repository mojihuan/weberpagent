# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.decorators import cached
from common.import_case import *


class TestFulfillmentItemToBeQuoted(BaseCase, unittest.TestCase):
    """运营中心|待报价物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return fulfillment_r.FulfillmentItemItemToBeQuotedRequest()
        else:
            return fulfillment_p.FulfillmentItemsToBeQuotedPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0commodity_quotes(self):
        """[商品报价]"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB4', 'CD1'])
        case = self.common_operations(login='main')
        case.commodity_quotes()
        res = [lambda: self.pc.fulfillment_items_to_be_quoted_assert(reportTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_requote(self):
        """[重新报价]"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB4', 'CD1', 'DA1'])
        case = self.common_operations()
        case.requote()
        res = [lambda: self.pc.fulfillment_items_to_be_quoted_assert(reportTime='now')]
        self.assert_all(*res)


class TestFulfillmentQualityManage(BaseCase, unittest.TestCase):
    """运营中心|质检管理"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return fulfillment_r.FulfillmentQualityManageRequest()
        else:
            return fulfillment_p.FulfillmentQualityManagePages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0receive_items_in_bulk(self):
        """[待领取物品tab]-批量接收"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2'])
        case = self.common_operations(login='main')
        case.receive_items_in_bulk()
        res = [lambda: self.pc.fulfillment_quality_manage_assert(data='a', distributorTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_direct_platform_review_receive_in_batches(self):
        """[待领取物品tab]-直拍-平台申诉通过-批量接收"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF5', '@BB5', 'DC1', '@BB4', 'CF6'])
        case = self.common_operations()
        case.direct_platform_review_receive_in_batches()
        res = [lambda: self.pc.fulfillment_quality_manage_assert(data='a', distributorTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_quality_receive_items_in_bulk(self):
        """[待领取物品tab]-质检服务-批量接收"""
        self.pre.operations(data=['@AA2', '@AB1', 'CA1'])
        case = self.common_operations()
        case.quality_receive_items_in_bulk()
        res = [lambda: self.pc.fulfillment_quality_manage_assert(data='a', distributorTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_submit_the_quality_inspection_results(self):
        """[质检中物品tab]-提交质检结果"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3'])
        case = self.common_operations()
        case.submit_the_quality_inspection_results()
        res = [lambda: self.pc.fulfillment_quality_manage_assert(data='c', qualityFinishTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_quality_submit_the_quality_inspection_results(self):
        """[质检中物品tab]-质检服务-提交质检结果"""
        self.pre.operations(data=['@AA2', '@AB1', 'CA1', 'CB1'])
        case = self.common_operations()
        case.quality_submit_the_quality_inspection_results()
        res = [lambda: self.pc.fulfillment_quality_manage_assert(data='c', qualityFinishTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_submit_the_quality_inspection_results_no(self):
        """[质检中物品tab]-提交质检结果-不传图"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3'])
        case = self.common_operations()
        case.submit_the_quality_inspection_results_no()
        res = [lambda: self.pc.fulfillment_quality_manage_assert(data='c', qualityFinishTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_passed_the_re_inspection(self):
        """[重验申请tab]-审核通过"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB9'])
        case = self.common_operations()
        case.passed_the_re_inspection()
        res = [lambda: self.pc.fulfillment_quality_manage_assert(data='b', reviewTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_rereview_rejected(self):
        """[重验申请tab]-审核拒绝"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB9'])
        case = self.common_operations()
        case.rereview_rejected()
        res = [lambda: self.pc.fulfillment_quality_manage_assert(data='b', reviewTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_modify_the_report(self):
        """[已质检物品tab]-修改报告"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6'])
        case = self.common_operations()
        case.modify_the_report()
        res = [lambda: self.pc.fulfillment_quality_manage_assert(data='c', qualityFinishTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_unverified_handover(self):
        """[质检中物品tab]-未验移交"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3'])
        case = self.common_operations()
        case.unverified_handover()
        res = [lambda: self.pc.fulfillment_quality_manage_assert(distributorTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_not_quality(self):
        """[质检中物品tab]-无需质检"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3'])
        case = self.common_operations()
        case.not_quality()
        res = [lambda: self.pc.auction_my_assert(j=1, status=5)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_product_image_shooting_and_uploading(self):  # todo 差异图未上传不知道怎么造数据
        """[商品图拍摄tab]-拍商品图"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB5'])
        case = self.common_operations()
        case.product_image_shooting_and_uploading()
        # res = [lambda: self.pc.fulfillment_quality_manage_assert(data='d', goodsImageStatusStr='已上传')]
        # self.assert_all(*res)  

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_direct_shot_physical_re_inspection_received(self):
        """[待领取物品tab]-直拍-实物复检-批量接收"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF2', '@BB3', 'CF3'])
        case = self.common_operations()
        case.direct_shot_physical_re_inspection_received()
        res = [lambda: self.pc.fulfillment_quality_manage_assert(data='a', distributorTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_direct_shot_of_the_real_thing_submit_quality(self):
        """[质检中物品tab]-直拍-实物复检-提交质检结果"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF2', '@BB4', 'CF3', 'CB7'])

        case = self.common_operations()
        case.direct_shot_of_the_real_thing_submit_quality()
        res = [lambda: self.pc.fulfillment_quality_manage_assert(data='c', qualityFinishTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_direct_platform_review_submit_quality(self):
        """[质检中物品tab]-直拍-平台申诉通过-提交质检结果"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF5', '@BB5', 'DC1', '@BB4', 'CF6', 'CB9'])
        case = self.common_operations()
        case.direct_platform_review_submit_quality()
        res = [lambda: self.pc.fulfillment_quality_manage_assert(data='c', qualityFinishTime='now')]
        self.assert_all(*res)


class TestFulfillmentReturnsManage(BaseCase, unittest.TestCase):
    """运营中心|退货管理"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return fulfillment_r.FulfillmentReturnsManageRequest()
        else:
            return fulfillment_p.FulfillmentReturnsManage(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0return_to_the_warehouse(self):
        """[待退货tab]-物品明细-邮寄退货出库"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB2'])
        case = self.common_operations(login='main')
        case.return_to_the_warehouse()
        res = [lambda: self.pc.fulfillment_returns_manage_assert(data='a', i=3, outboundTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_return_to_the_warehouse_use_jd(self):
        """[待退货tab]-物品明细-京东邮寄-退货出库"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB2'])
        case = self.common_operations()
        case.return_to_the_warehouse_use_jd()
        res = [lambda: self.pc.fulfillment_returns_manage_assert(data='a', i=3, outboundTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_return_to_the_warehouse_export_information(self):
        """[待退货tab]-物品明细-导出信息"""
        case = self.common_operations()
        case.return_to_the_warehouse_export_information()
        res = [lambda: self.pc.system_export_list_assert(state=2, name='送修单列表导出', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_self_submitted_library(self):
        """[待取货tab]-自提退货出库"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB3'])
        case = self.common_operations()
        case.self_submitted_library()
        res = [lambda: self.pc.fulfillment_returns_manage_assert(data='a', i=4, outboundTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_self_submitted_library_export_information(self):
        """[待取货tab]-物品明细-导出信息"""
        case = self.common_operations()
        case.self_submitted_library_export_information()
        res = [lambda: self.pc.system_export_list_assert(state=2, name='送修单列表导出', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_the_return_has_been_removed_batch(self):
        """[退货已出库tab]-批次明细-更改物流"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB2', 'CC1'])
        case = self.common_operations()
        case.the_return_has_been_removed_batch()
        res = [lambda: self.pc.fulfillment_returns_manage_assert(data='批次明细列表', i=3, outboundTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_the_return_has_been_removed_items(self):
        """[退货已出库tab]-物品明细-更改物流"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB2', 'CC1'])
        case = self.common_operations()
        case.the_return_has_been_removed_items()
        res = [lambda: self.pc.fulfillment_returns_manage_assert(data='a', i=3, outboundTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_the_return_has_been_removed_batch_export(self):
        """[退货已出库tab]-批次明细-导出信息"""
        case = self.common_operations()
        case.the_return_has_been_removed_batch_export()
        res = [lambda: self.pc.system_export_list_assert(state=2, name='送修单列表导出', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_the_return_has_been_removed_items_export(self):
        """[已退货tab]-物品明细-导出信息"""
        case = self.common_operations()
        case.the_return_has_been_removed_items_export()
        res = [lambda: self.pc.system_export_list_assert(state=2, name='送修单列表导出', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_cancelled_select_code(self):
        """[已取消tab]-输入正确查询自提码-自提退货出库"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB2', 'CC1', '@AB10'])
        case = self.common_operations()
        case.cancelled_select_code()
        res = [lambda: self.pc.fulfillment_returns_manage_assert(data='a', i=4, outboundTime='now')]
        self.assert_all(*res)


class TestFulfillmentSignIntoTheLibrary(BaseCase, unittest.TestCase):
    """运营中心|收货入库"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return fulfillment_r.FulfillmentSignIntoTheLibraryRequest()
        else:
            return fulfillment_p.FulfillmentSignIntoTheLibraryPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0unpacking_and_receiving_goods_into_storage(self):
        """[收货入库]上传视频入库"""
        self.pre.operations(data=['@AA1', '@AB5'])
        case = self.common_operations(login='main')
        case.unpacking_and_receiving_goods_into_storage()
        res = [lambda: self.pc.fulfillment_order_manage_assert(signTime='now', statusDesc='已收货')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_quality_inspection_upload_videos_for_storage(self):
        """[收货入库]质检服务-上传视频入库"""
        self.pre.operations(data=['@AA2', '@AB1'])
        case = self.common_operations()
        case.quality_inspection_upload_videos_for_storage()
        res = [lambda: self.pc.fulfillment_order_manage_assert(signTime='now', statusDesc='已收货')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_goods_are_received_and_into_storage_no_imei(self):
        """[收货入库]无imei-已打印"""
        self.pre.operations(data=['@AA1', '@AB5'])
        case = self.common_operations()
        case.goods_are_received_and_into_storage_no_imei()
        res = [lambda: self.pc.fulfillment_order_manage_assert(signTime='now', statusDesc='已收货')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_goods_are_received_and_into_storage_online_record(self):
        """[收货入库]在线录制包裹视频"""
        self.pre.operations(data=['@AA1', '@AB5'])
        case = self.common_operations()
        case.goods_are_received_and_into_storage_online_record()
        res = [lambda: self.pc.fulfillment_order_manage_assert(signTime='now', statusDesc='已收货')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_received_goods_into_the_warehouse_express_no(self):
        """[收货入库]物流单号添加物品"""
        self.pre.operations(data=['@AA1', '@AB5'])
        case = self.common_operations()
        case.received_goods_into_the_warehouse_express_no()
        res = [lambda: self.pc.fulfillment_order_manage_assert(signTime='now', statusDesc='已收货')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_received_goods_into_the_warehouse_modify_imei(self):
        """[收货入库]批量修改imei"""
        self.pre.operations(data=['@AA1', '@AB5'])
        case = self.common_operations()
        case.received_goods_into_the_warehouse_modify_imei()
        res = [lambda: self.pc.fulfillment_order_manage_assert(signTime='now', statusDesc='已收货')]
        self.assert_all(*res)


class TestFulfillmentOrderManage(BaseCase, unittest.TestCase):
    """运营中心|订单管理"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return fulfillment_r.FulfillmentOrderManageRequest()
        else:
            return fulfillment_p.FulfillmentOrderManagePages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0fast_guaranteed_items(self):
        """[快速保卖]-选择物品-确定"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations(login='main')
        case.fast_guaranteed_items()
        res = [lambda: self.pc.fulfillment_order_manage_assert(placeOrderTime='now', statusDesc='已收货')]
        self.assert_all(*res)


class TestFulfillmentItemsAreOutOfStorage(BaseCase, unittest.TestCase):
    """运营中心|物品出库"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return fulfillment_r.FulfillmentItemsAreOutOfStorageRequest()
        else:
            return fulfillment_p.FulfillmentItemsAreOutOfStoragePages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0direct_shot_express_sales_out_of_the_warehouse(self):
        """[销售出库]-直拍-顺丰快递-销售出库"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1'])
        self.wait_default()
        case = self.common_operations(login='main')
        case.direct_shot_express_sales_out_of_the_warehouse()
        res = [lambda: self.pc.fulfillment_sales_and_shipment_manage_assert(data='b', sendTime='now', sendTypeDesc='快递邮寄')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_direct_shot_jd_express_sales_out_of_the_warehouse(self):
        """[销售出库]-直拍-京东快递-销售出库"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1'])
        self.wait_default()
        case = self.common_operations()
        case.direct_shot_jd_express_sales_out_of_the_warehouse()
        res = [lambda: self.pc.fulfillment_sales_and_shipment_manage_assert(data='b', sendTime='now', sendTypeDesc='快递邮寄')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_direct_shooting_order_sales_out_of_the_warehouse(self):
        """[销售出库]-直拍-系统叫件顺丰-销售出库"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1'])
        self.wait_default()
        case = self.common_operations()
        case.direct_shooting_order_sales_out_of_the_warehouse()
        res = [lambda: self.pc.fulfillment_sales_and_shipment_manage_assert(data='b', sendTime='now', sendTypeDesc='快递邮寄')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_direct_shooting_order_sales_out_of_the_warehouse_jd(self):
        """[销售出库]-直拍-系统叫件京东-销售出库"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1'])
        self.wait_default()
        case = self.common_operations()
        case.direct_shooting_order_sales_out_of_the_warehouse_jd()
        res = [lambda: self.pc.fulfillment_sales_and_shipment_manage_assert(data='b', sendTime='now', sendTypeDesc='快递邮寄')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_direct_shooting_self_pick_up_and_sales(self):
        """[销售出库]-直拍-自提-销售出库"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', '@BB6'])
        case = self.common_operations()
        case.direct_shooting_self_pick_up_and_sales()
        res = [lambda: self.pc.fulfillment_sales_and_shipment_manage_assert(data='b', sendTime='now', sendTypeDesc='快递邮寄')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_direct_sf_after_sales_delivery(self):
        """[拍机售后出库]-直拍-快递顺丰-售后出库"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF7'])
        case = self.common_operations()
        case.direct_sf_after_sales_delivery()
        obj = cached('articlesNo')
        res = [lambda: self.pc.fulfillment_after_sales_return_manage_assert(outboundTime='now', articlesNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_direct_jd_after_sales_delivery(self):
        """[拍机售后出库]-直拍-快递京东-售后出库"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF7'])
        case = self.common_operations()
        case.direct_jd_after_sales_delivery()
        obj = cached('articlesNo')
        res = [lambda: self.pc.fulfillment_after_sales_return_manage_assert(outboundTime='now', articlesNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_direct_zt_after_sales_delivery(self):
        """[拍机售后出库]-直拍-自提-售后出库"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF7'])
        case = self.common_operations()
        case.direct_zt_after_sales_delivery()
        obj = cached('articlesNo')
        res = [lambda: self.pc.fulfillment_after_sales_return_manage_assert(outboundTime='now', articlesNo=obj)]
        self.assert_all(*res)


class TestFulfillmentAQuasiCamera(BaseCase, unittest.TestCase):
    """运营中心|壹准拍机|售后管理|售后订单"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return fulfillment_r.FulfillmentAQuasiCameraRequest()
        else:
            return None

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0online_review_direct_shooting_passed(self):
        """[线上审核]-直拍-仅退差-审核通过"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2'])
        case = self.common_operations(login='main')
        case.online_review_direct_shooting_passed()
        res = [lambda: self.pc.fulfillment_camera_after_sales_order_assert(i=['5'], afterStatusStr='补差成功', firstAuditResultStr='通过', firstAuditTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_the_direct_auction_price_difference_was_approved(self):
        """[线上审核]-直拍-优先补差-审核通过"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2'])
        case = self.common_operations()
        case.the_direct_auction_price_difference_was_approved()
        res = [lambda: self.pc.fulfillment_camera_after_sales_order_assert(i=['6'], afterStatusStr='补差成功', firstAuditResultStr='通过', firstAuditTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_direct_shot_return_refund_approved(self):
        """[线上审核]-直拍-退货退款-审核通过"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2'])
        case = self.common_operations()
        case.direct_shot_return_refund_approved()
        res = [lambda: self.pc.fulfillment_camera_after_sales_order_assert(i=['7'], afterStatusStr='待寄回', firstAuditResultStr='通过', firstAuditTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_direct_shot_review_rejection(self):
        """[线上审核]-直拍-审核拒绝"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2'])
        case = self.common_operations()
        case.direct_shot_review_rejection()
        res = [lambda: self.pc.fulfillment_camera_after_sales_order_assert(i=['2'], afterStatusStr='待申诉', firstAuditResultStr='通过', firstAuditTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_to_be_received_signature_into_the_library(self):
        """[待接收]-直拍-签收入库"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF2', '@BB4'])
        case = self.common_operations()
        case.to_be_received_signature_into_the_library()
        obj = cached('order_no')
        res = [lambda: self.pc.fulfillment_camera_after_sales_order_assert(i=['11'], afterStatusStr='实物复检', orderNo=obj)]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_direct_auction_review_refund_price_difference(self):
        """[实物复检]-直拍-复检审核-仅退差"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF2', '@BB4', 'CF3', 'CB7', 'CB8'])
        case = self.common_operations()
        case.direct_auction_review_refund_price_difference()
        res = [lambda: self.pc.fulfillment_camera_after_sales_order_assert(i=['5'], afterStatusStr='补差成功', recheckAuditResultStr='通过', recheckAuditTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_direct_platform_review_only_the_difference(self):
        """[实物复检]-直拍-平台申诉通过-复检审核-仅退差"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF5', '@BB5', 'DC1', '@BB4', 'CF6', 'CB9', 'CB10'])
        case = self.common_operations()
        case.direct_platform_review_only_the_difference()
        res = [lambda: self.pc.fulfillment_camera_after_sales_order_assert(i=['5'], afterStatusStr='补差成功', recheckAuditResultStr='通过', recheckAuditTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_direct_shot_review_priority_spread(self):
        """[实物复检]-直拍-复检审核-优先补差"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF2', '@BB4', 'CF3', 'CB7', 'CB8'])
        case = self.common_operations()
        case.direct_shot_review_priority_spread()
        res = [lambda: self.pc.fulfillment_camera_after_sales_order_assert(i=['6'], afterStatusStr='补差成功', firstAuditResultStr='通过', firstAuditTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_direct_platform_review_priority_difference(self):
        """[实物复检]-直拍-平台申诉通过-复检审核-优先补差"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF5', '@BB5', 'DC1', '@BB4', 'CF6', 'CB9', 'CB10'])
        case = self.common_operations()
        case.direct_platform_review_priority_difference()
        res = [lambda: self.pc.fulfillment_camera_after_sales_order_assert(i=['6'], afterStatusStr='补差成功', firstAuditResultStr='通过', firstAuditTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_direct_platform_review_sign_into_the_library(self):
        """[待接收]-直拍-平台申诉通过-签收入库"""
        self.pre.operations(data=['@AA1', '@AB5', 'CA2', 'CB3', 'CB6', '@AB4', 'DB1', 'DB2', '@BA1', 'CE1', '@BB1', '@BB2', 'CF5', '@BB5', 'DC1', '@BB7'])
        case = self.common_operations()
        case.direct_platform_review_sign_into_the_library()
        obj = cached('order_no')
        res = [lambda: self.pc.fulfillment_camera_after_sales_order_assert(i=['11'], afterStatusStr='实物复检', orderNo=obj)]
        self.assert_all(*res)


class TestFulfillmentAfterSalesReturnManage(BaseCase, unittest.TestCase):
    """运营中心|壹准拍机|售后管理|售后退货管理"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return fulfillment_r.FulfillmentAfterSalesReturnManageRequest()
        else:
            return None


if __name__ == '__main__':
    unittest.main()
