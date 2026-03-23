# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.import_case import *


class TestQualityCentreItem(BaseCase, unittest.TestCase):
    """质检管理|质检中物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return quality_r.QualityCentreItemRequest()
        else:
            return quality_p.QualityCentreItemPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0submit_quality_results(self):
        """[提交质检结果]-默认检测项-移交库存"""
        self.pre.operations(data=['FA1', 'HC3'])
        case = self.common_operations(login='main')
        case.submit_quality_results()
        res = [lambda: self.pc.quality_record_list_assert(qualityFinishTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_submit_quality_results_by_no_transfer(self):
        """[提交质检结果]-无移交"""
        self.pre.operations(data=['FA1', 'HC3'])
        case = self.common_operations()
        case.submit_quality_results_by_no_transfer()
        res = [lambda: self.pc.quality_record_list_assert(qualityFinishTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_fast_submit_inspection_results(self):
        """[快速质检]-添加物品-提交质检结果"""
        self.pre.operations(data=['FA1', 'HC3'])
        case = self.common_operations()
        case.fast_submit_inspection_results()
        res = [lambda: self.pc.quality_record_list_assert(qualityFinishTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_unverified_handover(self):
        """[未验移交]-移交库存"""
        self.pre.operations(data=['FA1', 'HC3'])
        case = self.common_operations()
        case.unverified_handover()
        res = [lambda: self.pc.inventory_list_assert(data='b', typeStr='移交', time='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_more_unverified_handover_purchase(self):
        """[扫码批量未验移交]-未验移交采购售后"""
        self.pre.operations(data=['FA1', 'HC3'])
        case = self.common_operations()
        case.more_unverified_handover_purchase()
        res = [lambda: self.pc.inventory_list_assert(data='b', typeStr='移交', time='now')]
        self.assert_all(*res)


class TestQualityContentTemplate(BaseCase, unittest.TestCase):
    """质检管理|质检内容模版"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return quality_r.QualityContentTemplateRequest()
        else:
            return quality_p.QualityContentTemplatePages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0new_template_added(self):
        """[新增]-默认选项"""
        case = self.common_operations(login='idle')
        case.new_template_added()
        res = [lambda: self.pc.quality_content_template_assert(headers='idle', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_editor_template(self):
        """[编辑]-默认选项"""
        self.pre.operations(data=['LC1'])
        case = self.common_operations()
        case.editor_template()
        res = [lambda: self.pc.quality_content_template_assert(headers='idle', updateTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_delete_template(self):
        """[删除]"""
        self.pre.operations(data=['LC1'])
        case = self.common_operations()
        case.delete_template()


class TestQualityGoodsReceived(BaseCase, unittest.TestCase):
    """质检管理|待接收物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return quality_r.QualityGoodsReceivedRequest()
        else:
            return quality_p.QualityGoodsReceivedPages(self.driver)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_goods_received(self):
        """[接收]-单个物品接收"""
        self.pre.operations(data=['FA1', 'HC2'])
        case = self.common_operations(login='special')
        case.goods_received()
        res = [lambda: self.pc.handover_record(statusStr='已接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_scan_goods_received(self):
        """[扫码精确接收]-单个物品接收"""
        self.pre.operations(data=['FA1', 'HC2'])
        case = self.common_operations()
        case.scan_goods_received()
        res = [lambda: self.pc.handover_record(statusStr='已接收', createTime='now')]
        self.assert_all(*res)


class TestQualityStore(BaseCase, unittest.TestCase):
    """质检管理|先质检后入库"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return quality_r.QualityStoreRequest()
        else:
            return quality_p.QualityStorePages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0quality_artificial_add(self):
        """[非库存物品tab]-人工快速质检-选择苹果手机-提交质检报告"""
        self.pre.operations(data=['FA1', 'HC3'])
        case = self.common_operations(login='main')
        case.quality_artificial_add()
        res = [lambda: self.pc.quality_store_assert(updateTime='now', articlesStatusStr='非库内物品', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_purchase_warehousing_handover_batch(self):
        """[非库内物品tab]-批量采购入库-采购入库成功"""
        self.pre.operations(data=['KA1', 'HC3', 'LA1'])
        case = self.common_operations()
        case.purchase_warehousing_handover_batch()
        res = [lambda: self.pc.purchase_order_list_assert(purchaseTime='now', stateStr='已发货')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_purchase_warehousing_handover(self):
        """[非库内物品tab]-采购入库-采购入库成功"""
        self.pre.operations(data=['KA1', 'HC3', 'LA1'])
        case = self.common_operations()
        case.purchase_warehousing_handover()
        res = [lambda: self.pc.purchase_order_list_assert(purchaseTime='now', stateStr='已发货')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_purchase_warehousing_put_on_the_mall(self):
        """[非库内物品tab]-采购入库-采购入库上架商城"""
        self.pre.operations(data=['KA1', 'HC3', 'LA1'])
        case = self.common_operations()
        case.purchase_warehousing_put_on_the_mall()

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_item_report_create_again(self):
        """[非库内物品tab]-编辑报告-重新生成质检报告"""
        case = self.common_operations()
        case.item_report_create_again()
        res = [lambda: self.pc.quality_store_assert(
            updateTime='now', articlesStatusStr='非库内物品', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_item_report_edit(self):
        """[非库内物品tab]-编辑报告-修改当前报告"""
        case = self.common_operations()
        case.item_report_edit()
        res = [lambda: self.pc.quality_store_assert(
            updateTime='now', articlesStatusStr='非库内物品', createTime='now')]
        self.assert_all(*res)


class TestQualityWaitTurnOver(BaseCase, unittest.TestCase):
    """质检管理|待移交物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return quality_r.QualityWaitTurnOverRequest()
        else:
            return quality_p.QualityWaitTurnOverPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0quality_inspection(self):
        """[复检]-移交质检"""
        self.pre.operations(data=['KA1', 'HC3', 'LB1'])
        case = self.common_operations(login='main')
        case.quality_inspection()
        res = [lambda: self.pc.quality_record_list_assert(qualityTypeStr='人工选择', qualityFinishTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_handover_inventory(self):
        """[移交]-移交库存"""
        self.pre.operations(data=['KA1', 'HC3', 'LB1'])
        case = self.common_operations()
        case.handover_inventory()
        res = [lambda: self.pc.quality_record_list_assert(qualityTypeStr='人工选择', qualityFinishTime='now')]
        self.assert_all(*res)


if __name__ == '__main__':
    unittest.main()
