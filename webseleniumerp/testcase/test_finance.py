# coding: utf-8
import unittest
from common.base_case import BaseCase
from common.import_case import *


class TestFinanceAccountList(BaseCase, unittest.TestCase):
    """财务管理|资金账户|账户列表"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return finance_r.FinanceAccountListRequest()
        else:
            return finance_p.FinanceAccountListPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0create_account(self):
        """[新建账户]其他-默认初始余额"""
        case = self.common_operations(login='idle')
        case.create_account()

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_edit_account(self):
        """[修改]修改账户类型为微信-充值"""
        case = self.common_operations()
        case.edit_account()

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_account_transfer(self):
        """[账户间转账]互相转账"""
        case = self.common_operations()
        case.account_transfer()


class TestFinanceBillReview(BaseCase, unittest.TestCase):
    """财务管理|业务记账|账单审核"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return finance_r.FinanceBillReviewRequest()
        else:
            return finance_p.FinanceBillReviewPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0financial_audit_deal_with(self):
        """[应付账单]审核-审核通过"""
        self.pre.operations(data=['FA3'])
        case = self.common_operations(login='main')
        case.financial_audit_deal_with()
        res = [lambda: self.pc.finance_bill_review_assert(i=1, type=1, auditStatus=1, billTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_audit_accounts_payable_turn_down(self):
        """[应付账单]审核-审核拒绝"""
        self.pre.operations(data=['FA3'])
        case = self.common_operations()
        case.audit_accounts_payable_turn_down()
        res = [lambda: self.pc.finance_bill_review_assert(i=1, type=1, auditStatus=2, billTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_audit_accounts_payable_batch_audit(self):
        """[应付账单]批量审核-审核通过"""
        self.pre.operations(data=['FA3'])
        case = self.common_operations()
        case.audit_accounts_payable_batch_audit()
        res = [lambda: self.pc.finance_bill_review_assert(i=1, type=1, auditStatus=1, billTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_financial_audit_receivable(self):
        """[应收账单]审核-审核通过"""
        self.pre.operations(data=['FA1', 'HC1', 'HB3'])
        case = self.common_operations()
        case.financial_audit_receivable()
        res = [lambda: self.pc.finance_bill_review_assert(i=2, type=2, auditStatus=1, billTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_account_receivable_audit_turn_down(self):
        """[应收账单]审核-审核拒绝"""
        self.pre.operations(data=['FA1', 'HC1', 'HB3'])
        case = self.common_operations()
        case.account_receivable_audit_turn_down()
        res = [lambda: self.pc.finance_bill_review_assert(i=2, type=2, auditStatus=2, billTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_account_receivable_audit_batch_audit(self):
        """[应收账单]批量审核-审核通过"""
        self.pre.operations(data=['FA1', 'HC1', 'HB3'])
        case = self.common_operations()
        case.account_receivable_audit_batch_audit()
        res = [lambda: self.pc.finance_bill_review_assert(i=2, type=2, auditStatus=1, billTime='now')]
        self.assert_all(*res)


class TestFinanceBillReviewTwo(TestFinanceBillReview):
    """财务管理|业务记账|账单审核"""

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_financial_audit_receivable_vice(self):
        """[应收账单]批量审核-帮卖订单-审核通过"""
        self.pre.operations(data=['FA1', 'GA1', 'GA3', 'GA4', 'GA7', 'HA1', 'GB1', 'HB1'])
        case = self.common_operations(login='vice')
        case.financial_audit_receivable_vice()
        res = [lambda: self.pc.finance_bill_review_assert(headers='vice', i=2, type=2, auditStatus=1, billTime='now')]
        self.assert_all(*res)


@unittest.skip("暂时跳过整个类的执行")
class TestFinanceCopingWithEachOther(BaseCase, unittest.TestCase):
    """财务管理|业务记账|往来应付"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return finance_r.FinanceCopingWithEachOtherRequest()
        else:
            return finance_p.FinanceCopingWithEachOtherPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0supplier_settlement(self):
        """[按供应商结算]部分金额结算"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations(login='main')
        case.supplier_settlement()
        res = [lambda: self.pc.finance_payment_settlement_assert(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_order_settlement(self):
        """[按机器批量结算]部分金额结算"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.order_settlement()
        res = [lambda: self.pc.finance_payment_settlement_assert(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_import_order_settlement(self):
        """[按机器批量结算]导入物品-部分金额结算"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.import_order_settlement()
        res = [lambda: self.pc.finance_payment_settlement_assert(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_settle_by_order_machine(self):
        """[按订单批量结算]全部金额结算"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.settle_by_order_machine()
        res = [lambda: self.pc.finance_payment_settlement_assert(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_settle_vendor_amount_all(self):
        """[按供应商结算]全部金额结算"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.settle_vendor_amount_all()
        res = [lambda: self.pc.finance_payment_settlement_assert(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_prepayment_deduction_all(self):
        """[按供应商结算]部分金额结算-预付款抵扣全部金额"""
        self.pre.operations(data=['FA1', 'BA1'])
        case = self.common_operations()
        case.prepayment_deduction_all()
        res = [lambda: self.pc.finance_payment_settlement_assert(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_prepayment_deduction_part(self):
        """[按供应商结算]部分金额结算-预付款抵扣部分金额"""
        self.pre.operations(data=['FA1', 'BA1'])
        case = self.common_operations()
        case.prepayment_deduction_part()
        res = [lambda: self.pc.finance_payment_settlement_assert(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_settle_by_order_part(self):
        """[按订单批量结算]部分金额结算"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.settle_by_order_part()
        res = [lambda: self.pc.finance_payment_settlement_assert(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_settle_by_order_prepaid_part(self):
        """[按订单批量结算]全部金额结算-预付款抵扣部分金额"""
        self.pre.operations(data=['FA1', 'BA1'])
        case = self.common_operations()
        case.settle_by_order_prepaid_part()
        res = [lambda: self.pc.finance_payment_settlement_assert(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_settle_by_order_prepaid_all(self):
        """[按订单批量结算]全部金额结算-预付款抵扣全部金额"""
        self.pre.operations(data=['FA1', 'BA1'])
        case = self.common_operations()
        case.settle_by_order_prepaid_all()
        res = [lambda: self.pc.finance_payment_settlement_assert(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_settle_machine_settlement(self):
        """[按机器批量结算]-全部金额结算"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.settle_machine_settlement()
        res = [lambda: self.pc.finance_payment_settlement_assert(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_machine_deduction_party(self):
        """[按机器批量结算]-部分金额结算-预付款抵扣部分金额"""
        self.pre.operations(data=['FA1', 'BA1'])
        case = self.common_operations()
        case.machine_deduction_party()
        res = [lambda: self.pc.finance_payment_settlement_assert(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_machine_deduction_all(self):
        """[按机器批量结算]-全部金额结算-预付款抵扣全部金额"""
        self.pre.operations(data=['FA1', 'BA1'])
        case = self.common_operations()
        case.machine_deduction_all()
        res = [lambda: self.pc.finance_payment_settlement_assert(receiptTime='now')]
        self.assert_all(*res)


class TestFinanceCostIncomeAdjustment(BaseCase, unittest.TestCase):
    """财务管理|成本收入调整"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return finance_r.FinanceCostIncomeAdjustmentRequest()
        else:
            return finance_p.FinanceCostIncomeAdjustmentPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0new_adjustment_order_cost(self):
        """[新增调整单]添加物品-成本调整-采购金额调整"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations(login='main')
        case.new_adjustment_order_cost()
        res = [lambda: self.pc.finance_cost_income_adjustment_assert(adjustmentNum=1, adjustmentTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_new_adjustment_order_cost_other_costs(self):
        """[新增调整单]添加物品-成本调整-其他成本调整"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.new_adjustment_order_cost_other_costs()
        res = [lambda: self.pc.finance_cost_income_adjustment_assert(adjustmentNum=1, adjustmentTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_cost_adjustment_add_items_by_document(self):
        """[新增调整单]成本调整-其他成本调整-按单据添加物品"""
        self.pre.operations(data=['FA1'])
        case = self.common_operations()
        case.cost_adjustment_add_items_by_document()
        res = [lambda: self.pc.finance_cost_income_adjustment_assert(adjustmentNum=1, adjustmentTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_new_adjustment_order_income(self):
        """[新增调整单]添加物品-收入调整-销售金额调整"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2'])
        case = self.common_operations()
        case.new_adjustment_order_income()
        res = [lambda: self.pc.finance_cost_income_adjustment_assert(adjustmentNum=1, adjustmentTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_new_adjustment_order_income_other_income(self):
        """[新增调整单]添加物品-收入调整-其他收入调整"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2'])
        case = self.common_operations()
        case.new_adjustment_order_income_other_income()
        res = [lambda: self.pc.finance_cost_income_adjustment_assert(adjustmentNum=1, adjustmentTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_revenue_adjustment_add_items_by_document(self):
        """[新增调整单]收入调整-其他收入调整-按单据添加物品"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2'])
        case = self.common_operations()
        case.revenue_adjustment_add_items_by_document()
        res = [lambda: self.pc.finance_cost_income_adjustment_assert(adjustmentNum=1, adjustmentTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_multi_item_other_income_adjustments(self):
        """[新增调整单]添加物品-收入调整-其他收入调整"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2'])
        case = self.common_operations()
        case.multi_item_other_income_adjustments()
        res = [lambda: self.pc.finance_cost_income_adjustment_assert(adjustmentNum=2, adjustmentTime='now')]
        self.assert_all(*res)


class TestFinanceDailyDisburse(BaseCase, unittest.TestCase):
    """财务管理|业务记账|日常支出"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return finance_r.FinanceDailyDisburseRequest()
        else:
            return finance_p.FinanceDailyDisbursePages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0new_disburse(self):
        """[新增支出项]默认支出类型-金额正数"""
        case = self.common_operations(login='main')
        case.new_disburse()
        res = [lambda: self.pc.finance_daily_expenditure_assert(createTime='now', receiptNo='OT')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_new_expenditure_items_negative_amount(self):
        """[新增支出项]默认支出类型-金额负数"""
        case = self.common_operations()
        case.new_expenditure_items_negative_amount()
        res = [lambda: self.pc.finance_daily_expenditure_assert(createTime='now', receiptNo='OT')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_added_daily_expense_bills(self):
        """[新增支出项]新增支出日常单"""
        case = self.common_operations()
        case.added_daily_expense_bills()
        res = [lambda: self.pc.finance_daily_expenditure_assert(createTime='now', receiptNo='OT')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_new_expenditure_adjustment_order(self):
        """[新增支出项]新增支出调整单"""
        case = self.common_operations()
        case.new_expenditure_adjustment_order()
        res = [lambda: self.pc.finance_daily_expenditure_assert(createTime='now', receiptNo='OT')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_daily_expenses_export_all(self):
        """[导出全部]"""
        case = self.common_operations()
        case.daily_expenses_export_all()
        res = [lambda: self.pc.system_export_list_assert(state=2, createTime='now', name='日常费用单据信息导出')]
        self.assert_all(*res)


class TestFinanceDailyIncome(BaseCase, unittest.TestCase):
    """财务管理|业务记账|日常收入"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return finance_r.FinanceDailyIncomeRequest()
        else:
            return finance_p.FinanceDailyIncomePages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0new_income(self):
        """[新增收入项]-默认收入类型-金额正数"""
        case = self.common_operations(login='main')
        case.new_income()
        res = [lambda: self.pc.finance_daily_income_assert(createTime='now', receiptNo='IN')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_default_revenue_type_negative_amount(self):
        """[新增支出项]默认收入类型-金额负数"""
        case = self.common_operations()
        case.default_revenue_type_negative_amount()
        res = [lambda: self.pc.finance_daily_income_assert(createTime='now', receiptNo='IN')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_new_daily_income_bills(self):
        """[新增支出项]新增收入日常单"""
        case = self.common_operations()
        case.new_daily_income_bills()
        res = [lambda: self.pc.finance_daily_income_assert(createTime='now', receiptNo='IN')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_new_revenue_adjustment_order(self):
        """[新增支出项]新增收入调整单"""
        case = self.common_operations()
        case.new_revenue_adjustment_order()
        res = [lambda: self.pc.finance_daily_income_assert(createTime='now', receiptNo='IN')]
        self.assert_all(*res)


@unittest.skip("暂时跳过整个类的执行")
class TestFinanceExchangesAndReceivables(BaseCase, unittest.TestCase):
    """财务管理|业务记账|往来应收"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return finance_r.FinanceExchangesAndReceivablesRequest()
        else:
            return finance_p.FinanceExchangesAndReceivablesPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0customers_settle_bills(self):
        """[按客户结算]部分金额结算"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2'])
        case = self.common_operations(login='main')
        case.customers_settle_bills()
        res = [lambda: self.pc.finance_collection_and_settlement_assert(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_the_customer_settles_the_full_amount(self):
        """[按客户结算]全部金额结算"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2'])
        case = self.common_operations()
        case.the_customer_settles_the_full_amount()
        res = [lambda: self.pc.finance_collection_and_settlement_assert(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_settle_all_prepaid_part_of_the_amount(self):
        """[按客户结算]部分金额结算-预收款抵扣部分金额"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2', 'BA2'])
        case = self.common_operations()
        case.settle_all_prepaid_part_of_the_amount()
        res = [lambda: self.pc.finance_collection_and_settlement_assert(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_full_settlement_the_entire_amount_of_the_presale(self):
        """[按客户结算]部分金额结算-预收款抵扣全部金额"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2', 'BA2'])
        case = self.common_operations()
        case.full_settlement_the_entire_amount_of_the_presale()
        res = [lambda: self.pc.finance_collection_and_settlement_assert(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_settlement_un_edit_amount(self):
        """[按订单批量结算]全部金额结算"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2'])
        case = self.common_operations()
        case.settlement_un_edit_amount()
        res = [lambda: self.pc.finance_collection_and_settlement_assert(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_settlement_edit_amount(self):
        """[按订单批量结算]部分金额结算"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2'])
        case = self.common_operations()
        case.settlement_edit_amount()
        res = [lambda: self.pc.finance_collection_and_settlement_assert(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_settlement_edit_largest_amount(self):
        """[按订单批量结算]结算最大金额"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2'])
        case = self.common_operations()
        case.settlement_edit_largest_amount()
        res = [lambda: self.pc.finance_collection_and_settlement_assert(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_all_settlement_prepaid_part_of_the_amount(self):
        """[按订单批量结算]全部金额结算-预收款抵扣部分金额"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2', 'BA2'])
        case = self.common_operations()
        case.all_settlement_prepaid_part_of_the_amount()
        res = [lambda: self.pc.finance_collection_and_settlement_assert(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_settle_all_advance_receipt_of_the_entire_amount(self):
        """[按订单批量结算]全部金额结算-预收款抵扣全部金额"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2', 'BA2'])
        case = self.common_operations()
        case.settle_all_advance_receipt_of_the_entire_amount()
        res = [lambda: self.pc.finance_collection_and_settlement_assert(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_settlement_export(self):
        """[导出]"""
        case = self.common_operations()
        case.settlement_export()
        res = [lambda: self.pc.system_export_list_assert(name='应收对账详情导出', state=2, createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_customer_order_machine_settlement(self):
        """[按机器批量结算]部分金额结算"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2'])
        case = self.common_operations()
        case.customer_order_machine_settlement()
        res = [lambda: self.pc.finance_collection_and_settlement_assert(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_customer_import_order_settlement(self):
        """[按机器批量结算]导入物品-结算"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2'])
        case = self.common_operations()
        case.customer_import_order_settlement()
        res = [lambda: self.pc.finance_collection_and_settlement_assert(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_settle_the_full_amount_by_the_machine(self):
        """[按机器批量结算]全部金额结算"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2'])
        case = self.common_operations()
        case.settle_the_full_amount_by_the_machine()
        res = [lambda: self.pc.finance_collection_and_settlement_assert(receiptTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('api')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_the_machine_settles_all_part_of_the_amount(self):
        """[按机器批量结算]部分金额结算-预收款抵扣部分金额"""
        self.pre.operations(data=['FA1', 'HC1', 'HB2', 'BA2'])
        case = self.common_operations()
        case.the_machine_settles_all_part_of_the_amount()
        res = [lambda: self.pc.finance_collection_and_settlement_assert(receiptTime='now')]
        self.assert_all(*res)


class TestFinancePrePayReceived(BaseCase, unittest.TestCase):
    """财务管理|业务记账|预付预收"""

    def get_instantiation(self):
        if self.auto_type == 'api':
            return finance_r.FinancePrePayReceivedRequest()
        else:
            return finance_p.FinancePrePayReceivedPages(self.driver)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with(clear_cache=True)
    def test_0add_prepay(self):
        """[预付款tab]-新增预付款"""
        case = self.common_operations(login='main')
        case.add_prepay()
        res = [lambda: self.pc.finance_prepay_receive_list_assert(createTime='now', billNo='YF', i=2)]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_add_prepay_export(self):
        """[预付款tab]-导出"""
        case = self.common_operations()
        case.add_prepay_export()
        res = [lambda: self.pc.system_export_list_assert(name='预付/预收账单导出', state=2, createTime='now')]
        self.assert_all(*res)

    @BaseCase.auto('all')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_add_received(self):
        """[预收款tab]-新增预收款"""
        case = self.common_operations()
        case.add_received()
        res = [lambda: self.pc.finance_prepay_receive_list_assert(i=2, createTime='now', billNo='YF')]
        self.assert_all(*res)

    @BaseCase.auto('ui')
    @BaseCase.author('Jack')
    @BaseCase.retry_with()
    def test_add_received_export(self):
        """[预收款tab]-导出"""
        case = self.common_operations()
        case.add_received_export()
        res = [lambda: self.pc.system_export_list_assert(name='预付/预收账单导出', state=2, createTime='now')]
        self.assert_all(*res)


if __name__ == '__main__':
    unittest.main()
