# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.import_case import *


class TestRepairAuditList(BaseCase, unittest.TestCase):
    """维修管理|维修审核列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return repair_r.RepairAuditListRequest()
        else:
            return repair_p.RepairAuditListPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0the_maintenance_audit_passed(self):
        """[审核]-审核已通过"""
        self.pre.operations(data=['FA1', 'HC5', 'MA1'])
        case = self.common_operations(login='main')
        case.the_maintenance_audit_passed()
        res = [lambda: self.pc.repair_review_list_assert(auditTime='now', auditStatusStr='已通过')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_audit_rejection(self):
        """[审核]-审核未通过"""
        self.pre.operations(data=['FA1', 'HC5', 'MA1'])
        case = self.common_operations()
        case.audit_rejection()
        res = [lambda: self.pc.repair_review_list_assert(auditTime='now', auditStatusStr='未通过')]
        self.assert_all(*res)


class TestRepairCentreItem(BaseCase, unittest.TestCase):
    """维修管理|维修中物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return repair_r.RepairCentreItemRequest()
        else:
            return repair_p.RepairCentreItemPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0submit_the_maintenance_results(self):
        """[提交维修结果]-移交库存"""
        self.pre.operations(data=['FA1', 'HC5'])
        case = self.common_operations(login='main')
        case.submit_the_maintenance_results()
        res = [lambda: self.pc.repair_items_assert(auditStatusStr='待审核', consignerTime='now')]
        self.assert_all(*res)


    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_fast_submit_repair_results(self):
        """[快速维修]-移交库存"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.fast_submit_repair_results()
        res = [lambda: self.pc.repair_items_assert(auditStatusStr='待审核', consignerTime='now')]
        self.assert_all(*res)


    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_add_accessories_submit_repair_results(self):
        """[提交维修结果]-添加单个配件-移交库存"""
        self.pre.operations(data=['FA1', 'HC5'])
        case = self.common_operations()
        case.add_accessories_submit_repair_results()
        res = [lambda: self.pc.repair_items_assert(auditStatusStr='待审核', consignerTime='now')]
        self.assert_all(*res)


    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_scan_the_code_to_add_accessories(self):
        """[提交维修结果]-扫码添加单个配件-移交库存"""
        self.pre.operations(data=['FA1', 'HC5'])
        case = self.common_operations()
        case.scan_the_code_to_add_accessories()
        res = [lambda: self.pc.repair_items_assert(auditStatusStr='待审核', consignerTime='now')]
        self.assert_all(*res)


    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_fast_submit_repair_bulk_submission(self):
        """[批量提交维修结果]-移交库存"""
        self.pre.operations(data=['FA1', 'HC5'])
        case = self.common_operations()
        case.fast_submit_repair_bulk_submission()
        res = [lambda: self.pc.repair_items_assert(auditStatusStr='待审核', consignerTime='now')]
        self.assert_all(*res)


    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_unrepaired_handover(self):
        """[未修移交]-移交库存"""
        self.pre.operations(data=['FA1', 'HC5'])
        case = self.common_operations()
        case.unrepaired_handover()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='待接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_scan_unverified_handover(self):
        """[扫码精确未修移交]-移交库存"""
        self.pre.operations(data=['FA1', 'HC4'])
        case = self.common_operations()
        case.scan_unverified_handover()
        res = [lambda: self.pc.inventory_handover_record_assert(statusStr='待接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_purpose_of_transfer_repair(self):
        """[提交维修结果]-移交维修"""
        self.pre.operations(data=['FA1', 'HC5'])
        case = self.common_operations()
        case.purpose_of_transfer_repair()
        res = [lambda: self.pc.repair_items_assert(auditStatusStr='待审核', consignerTime='now')]
        self.assert_all(*res)


    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_purpose_of_transfer_sales(self):
        """[提交维修结果]-移交销售"""
        self.pre.operations(data=['FA1', 'HC5'])
        case = self.common_operations()
        case.purpose_of_transfer_sales()
        res = [lambda: self.pc.repair_items_assert(auditStatusStr='待审核', consignerTime='now')]
        self.assert_all(*res)


    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_submit_maintenance_and_disassembly_parts(self):
        """[物品拆件]-添加物品确认"""
        self.pre.operations(data=['FA1', 'HC5'])
        case = self.common_operations()
        case.submit_maintenance_and_disassembly_parts()
        res = [lambda: self.pc.repair_parts_manage_assert(apartNo='CJ', apartTime='now')]
        self.assert_all(*res)


class TestRepairDataStatistics(BaseCase, unittest.TestCase):
    """维修管理|维修数据统计"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return None
        else:
            return repair_p.RepairDataStatisticsPages(self.driver)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0derived_data(self):
        """[导出]"""
        case = self.common_operations(login='main')
        case.derived_data()
        res = [lambda: self.pc.system_export_list_assert(name='维修数据统计导出', state=2, createTime='now')]
        self.assert_all(*res)


class TestPurchaseGoodsReceived(BaseCase, unittest.TestCase):
    """维修管理|待接收物品"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return None
        else:
            return repair_p.RepairGoodsReceivedPages(self.driver)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0goods_received(self):
        """[接收]-单个物品接收"""
        self.pre.operations(data=['FA1', 'HC4'])
        case = self.common_operations(login='special')
        case.goods_received()
        res = [lambda: self.pc.handover_record(statusStr='待接收', createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_scan_goods_received(self):
        """[扫码精确接收]-单个物品接收"""
        self.pre.operations(data=['FA1', 'HC4'])
        case = self.common_operations()
        case.scan_goods_received()
        res = [lambda: self.pc.handover_record(statusStr='已接收', createTime='now')]
        self.assert_all(*res)


class TestRepairProjectList(BaseCase, unittest.TestCase):
    """维修管理|维修项目列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return repair_r.RepairProjectListRequest()
        else:
            return repair_p.RepairProjectListPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0new_maintenance_items_iphone(self):
        """[手机tab]-新增维修项目-品类手机"""
        case = self.common_operations(login='idle')
        case.new_maintenance_items_iphone()
        res = [lambda: self.pc.repair_project_list_assert(i=1, headers='idle')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_new_maintenance_items_ipa(self):
        """[手机tab]-新增维修项目-品类平板电脑"""
        case = self.common_operations()
        case.add_maintenance_items_flat()
        res = [lambda: self.pc.repair_project_list_assert(i=3, headers='idle')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_editor_maintenance_items(self):
        """[手机tab]-编辑-修改信息保存"""
        case = self.common_operations()
        case.editor_maintenance_items()
        res = [lambda: self.pc.repair_project_list_assert(i=1, headers='idle')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_delete_maintenance_items(self):
        """[手机tab]-删除"""
        case = self.common_operations()
        case.delete_maintenance_items()

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_new_model_configuration(self):
        """[手机tab]-机型配置-新增品牌型号"""
        case = self.common_operations()
        case.new_model_configuration()
        res = [lambda: self.pc.repair_project_list_assert(i=1, headers='idle')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_delete_model_configuration(self):
        """[手机tab]-机型配置-删除"""
        self.pre.operations(data=['MB1'])
        case = self.common_operations()
        case.delete_model_configuration()

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_add_maintenance_items_flat(self):
        """[平板电脑tab]-新增维修项目-品类平板电脑"""
        self.pre.operations(data=['MB1'])
        case = self.common_operations()
        case.add_maintenance_items_flat()
        res = [lambda: self.pc.repair_project_list_assert(headers='idle')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_add_maintenance_items_book(self):
        """[笔记本电脑tab]-新增维修项目-品类笔记本电脑"""
        self.pre.operations(data=['MB1'])
        case = self.common_operations()
        case.add_maintenance_items_book()
        res = [lambda: self.pc.repair_project_list_assert(headers='idle')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_add_maintenance_items_watch(self):
        """[智能手表tab]-新增维修项目-品类智能手表"""
        self.pre.operations(data=['MB1'])
        case = self.common_operations()
        case.add_maintenance_items_watch()
        res = [lambda: self.pc.repair_project_list_assert(headers='idle')]
        self.assert_all(*res)


if __name__ == '__main__':
    unittest.main()
