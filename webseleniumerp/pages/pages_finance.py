# coding: utf-8
import os
from common.base_page import BasePage, ImportDataEdit, reset_after_execution
from common.base_params import InitializeParams
from common.import_desc import *
from config.settings import DATA_PATHS
from config.user_info import INFO


class CommonPages(BasePage, InitializeParams):
    def __init__(self, driver):
        super().__init__(driver)
        self._steps_queue = []
        self.file = ImportDataEdit(driver)
        self.file_paths = self.file.file_paths = {
            'financial_settlement': os.path.join(DATA_PATHS['excel'], 'financial_settlement_import.xlsx')
        }

    def menu(self, menu_type, key):
        """获取元素"""
        menu_mapping = {
            'main': self.elem_positioning['positioning'],
        }
        if menu_type in menu_mapping:
            return self.exc(lambda: menu_mapping[menu_type][key])
        else:
            raise ValueError(f"menu not found: {menu_type}")


class FinanceAccountListPages(CommonPages):
    """财务管理|资金账户|账户列表"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='financial_manage_menu', desc='财务管理')
         .step(key='financial_capital_account_menu', desc='资金账户')
         .step(key='financial_account_list_menu', desc='账户列表')
         .wait())
        return self

    @reset_after_execution
    @doc(f_create_account)
    def create_account(self):
        self.menu_manage()
        (self.step(key='be_put_in_storage', desc='新建账户')
         .step(key='account_type', desc='账户类型')
         .custom(lambda: self.up_arrow_return())
         .step(key='account_name', value='名称' + self.get_time_stamp(), action='input', desc='账户名称')
         .step(key='initial_balance', value='1', action='input', desc='初始余额')
         .step(key='financial_notes', value='备注信息', action='input', desc='备注')
         .step(key='verify', desc='确认')
         .wait())
        return self

    @reset_after_execution
    @doc(f_account_transfer)
    def account_transfer(self):
        self.menu_manage()
        (self.step(key='scan_the_code_receive', desc='账户间转账')
         .step(key='date', desc='日期')
         .step(key='date_ok', desc='确定')
         .step(key='amount', value='5', action='input', desc='金额')
         .step(key='transfer_out_account', desc='转出账户')
         .custom(lambda: self.down_arrow_return())
         .step(key='transfer_to_account', desc='转入账户')
         .custom(lambda: self.up_arrow_return())
         .step(key='transfer_to_account_confirmation', desc='确认')
         .wait())
        return self


class FinanceBillReviewPages(CommonPages):
    """财务管理|业务记账|账单审核"""

    def menu_manage(self):
        """菜单"""
        (self.scroll(key='financial_manage_menu', desc='财务管理')
         .step(key='financial_manage_menu', desc='财务管理')
         .step(key='financial_business_bookkeeping_menu', desc='业务记账')
         .step(key='financial_bill_review_menu', desc='账单审核')
         .wait())
        return self

    @reset_after_execution
    @doc(f_financial_audit_deal_with)
    def financial_audit_deal_with(self):
        self.menu_manage()
        (self.step(key='examine', desc='审核')
         .step(key='instructions', value=self.serial, action='input', desc='说明')
         .step(key='review_confirmation', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_audit_accounts_payable_turn_down)
    def audit_accounts_payable_turn_down(self):
        self.menu_manage()
        (self.step(key='examine', desc='审核')
         .step(key='repair_audit_turn_down', desc='未通过')
         .step(key='instructions', value=self.serial, action='input', desc='说明')
         .step(key='review_confirmation', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_audit_accounts_payable_batch_audit)
    def audit_accounts_payable_batch_audit(self):
        self.menu_manage()
        (self.step(key='search', desc='搜索')
         .custom(lambda: self.tab_return(2))
         .step(key='batch_audit', desc='批量审核')
         .step(key='send_payment_account', desc='付款账户')
         .custom(lambda: self.down_arrow_return())
         .step(key='instructions', value=self.serial, action='input', desc='说明')
         .step(key='review_confirmation', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_financial_audit_receivable)
    def financial_audit_receivable(self):
        self.menu_manage()
        (self.step(key='delivery_receipt', desc='应收账单')
         .step(key='examine', desc='审核')
         .step(key='instructions', value=self.serial, action='input', desc='说明')
         .step(key='review_confirmation', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_account_receivable_audit_turn_down)
    def account_receivable_audit_turn_down(self):
        self.menu_manage()
        (self.step(key='delivery_receipt', desc='应收账单')
         .step(key='examine', desc='审核')
         .step(key='repair_audit_turn_down', desc='未通过')
         .step(key='instructions', value=self.serial, action='input', desc='说明')
         .step(key='review_confirmation', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_account_receivable_audit_batch_audit)
    def account_receivable_audit_batch_audit(self):
        self.menu_manage()
        (self.step(key='delivery_receipt', desc='应收账单')
         .step(key='search', desc='搜索')
         .custom(lambda: self.tab_return(2))
         .step(key='batch_audit', desc='批量审核')
         .step(key='collection_account', desc='收款账户')
         .custom(lambda: self.down_arrow_return())
         .step(key='instructions', value=self.serial, action='input', desc='说明')
         .step(key='review_confirmation', desc='确定')
         .wait())
        return self


class FinanceCopingWithEachOtherPages(CommonPages):
    """财务管理|业务记账|往来应付"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='financial_manage_menu', desc='财务管理')
         .step(key='financial_business_bookkeeping_menu', desc='业务记账')
         .step(key='financial_accounts_payable_menu', desc='往来应付')
         .wait())
        return self

    @reset_after_execution
    @doc(f_supplier_settlement)
    def supplier_settlement(self):
        self.menu_manage()
        (self.step(key='suppliers', desc='供应商')
         .step(key='suppliers', value=INFO['main_supplier_name'], action='input', desc='供应商')
         .custom(lambda: self.up_arrow_return())
         .step(key='search', desc='搜索')
         .step(key='reconciliation', desc='对账')
         .step(key='supplier_settlement', desc='按供应商结算')
         .step(key='payment_time', desc='付款时间')
         .step(key='now', desc='确定')
         .step(key='remark', value=self.serial, action='input', desc='备注')
         .step(key='send_payment_account', desc='付款账户')
         .custom(lambda: self.up_arrow_return())
         .step(key='settlement_amount', value='5', action='input', desc='结算金额')
         .step(key='vendor_settlement_confirmation', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_import_order_settlement)
    def import_order_settlement(self):
        self.menu_manage()
        self.file.get_inventory_data('financial_settlement', 'imei', i=2, j=3)
        (self.step(key='customer', desc='供应商')
         .step(key='customer', value=INFO['main_supplier_name'], action='input', desc='供应商')
         .custom(lambda: self.up_arrow_return())
         .step(key='search', desc='搜索')
         .step(key='reconciliation', desc='对账')
         .custom(lambda: self.wait_time(2))
         .step(key='machine_settlement', desc='按机器批量结算')
         .custom(lambda: self.wait_time(3))
         .step(key='import_into_machine', desc='导入机器')
         .step(key='handover_import', value=self.file_path('financial_settlement'), action='upload', desc='上传文件')
         .step(key='import_the_machine_to_confirm', desc='确定')
         .step(key='account', desc='付款账户')
         .custom(lambda: self.up_arrow_return())
         .scroll('machine_settlement_amount', desc='结算金额')
         .step(key='reject_the_note', value='3', action='input', desc='结算金额')
         .step(key='submit_settlement', desc='提交结算')
         .wait())
        return self


class FinanceCostIncomeAdjustmentPages(CommonPages):
    """财务管理|成本收入调整"""

    def menu_manage(self):
        """菜单"""
        (self.scroll(key='financial_manage_menu', desc='财务管理')
         .step(key='financial_manage_menu', desc='财务管理')
         .step(key='financial_cost_income_adjustment_menu', desc='成本收入调整')
         .wait())
        return self

    @reset_after_execution
    @doc(f_new_adjustment_order_cost)
    def new_adjustment_order_cost(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=2)[0]['articlesNo'])
        (self.step(key='sales_after_sales_btn', desc='新增调整单')
         .step(key='item_input', desc='物品输入框')
         .custom(lambda: self.affix())
         .step(key='add_item_btn', desc='添加')
         .custom(lambda: self.wait_time())
         .step(key='new_purchase_amount', value='14', action='input', desc='新采购金额')
         .step(key='generate_purchase_order', desc='确认')
         .step(key='send_payment_account', desc='付款账户')
         .custom(lambda: self.up_arrow_return())
         .step(key='new_adjustment_order_confirmation', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_cost_adjustment_add_items_by_document)
    def cost_adjustment_add_items_by_document(self):
        self.menu_manage()
        self.copy(self.pc.finance_coping_with_each_other_data()[0]['billNo'])
        (self.step(key='sales_after_sales_btn', desc='新增调整单')
         .step(key='other_costs_other_income', desc='其他成本')
         .step(key='reason_adjustment', desc='调整原因')
         .custom(lambda: self.down_arrow_return())
         .step(key='add_items_by_document', desc='按单据添加物品')
         .step(key='document_number_ipt', desc='单据号输入框')
         .custom(lambda: self.affix())
         .step(key='document_number_search', desc='搜索')
         .step(key='confirm_the_selection', desc='确认选择')
         .scroll('new_purchase_amount', desc='调整后金额')
         .step(key='new_purchase_amount', value='16', action='input', desc='调整后金额')
         .step(key='generate_purchase_order', desc='确认')
         .step(key='send_payment_account', desc='付款账户')
         .custom(lambda: self.up_arrow_return())
         .step(key='new_adjustment_order_confirmation', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_new_adjustment_order_income)
    def new_adjustment_order_income(self):
        self.menu_manage()
        self.copy(self.pc.inventory_list_data(i=3, j=9)[0]['imei'])
        (self.step(key='sales_after_sales_btn', desc='新增调整单')
         .step(key='income_adjustment', desc='收入调整')
         .step(key='item_input', desc='物品输入框')
         .custom(lambda: self.affix())
         .step(key='add_item_btn', desc='添加')
         .scroll('amount_of_sales', desc='最新销售金额')
         .step(key='amount_of_sales', value='18', action='input', desc='最新销售金额')
         .step(key='generate_purchase_order', desc='确认')
         .step(key='collection_account', desc='收款账户')
         .custom(lambda: self.up_arrow_return())
         .step(key='the_sales_adjustment_order_is_determined', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_revenue_adjustment_add_items_by_document)
    def revenue_adjustment_add_items_by_document(self):
        self.menu_manage()
        self.copy(self.pc.finance_exchanges_and_receivables_data()[0]['billNo'])
        (self.step(key='sales_after_sales_btn', desc='新增调整单')
         .step(key='income_adjustment', desc='收入调整')
         .step(key='other_costs_other_income', desc='其他收入')
         .step(key='reason_adjustment', desc='调整原因')
         .custom(lambda: self.down_arrow_return())
         .step(key='add_items_by_document', desc='按单据添加物品')
         .step(key='document_number_ipt', desc='单据号输入框')
         .custom(lambda: self.affix())
         .step(key='document_number_search', desc='搜索')
         .step(key='confirm_the_selection', desc='确认选择')
         .scroll('amount_of_sales', desc='调整后金额')
         .custom(lambda: self.wait_time())
         .step(key='amount_of_sales', value='7', action='input', desc='调整后金额')
         .step(key='generate_purchase_order', desc='确认')
         .step(key='collection_account', desc='收款账户')
         .custom(lambda: self.up_arrow_return())
         .step(key='the_sales_adjustment_order_is_determined', desc='确定')
         .wait())
        return self


class FinanceDailyDisbursePages(CommonPages):
    """财务管理|业务记账|日常支出"""

    def menu_manage(self):
        """菜单"""
        (self.scroll(key='financial_manage_menu', desc='财务管理')
         .step(key='financial_manage_menu', desc='财务管理')
         .step(key='financial_business_bookkeeping_menu', desc='业务记账')
         .step(key='financial_daily_expenditure_menu', desc='日常支出')
         .wait())
        return self

    @reset_after_execution
    @doc(f_new_disburse)
    def new_disburse(self):
        self.menu_manage()
        (self.step(key='new_disburse', desc='新增支出项')
         .step(key='disburse_type', desc='支出类型')
         .custom(lambda: self.down_arrow_return())
         .step(key='disburse_price', value='234', action='input', desc='支出价格')
         .step(key='disburse_account', desc='支出账户')
         .custom(lambda: self.down_arrow_return())
         .step(key='handle', desc='经办人')
         .custom(lambda: self.down_arrow_return())
         .step(key='instructions', value=self.serial, action='input', desc='备注')
         .step(key='new_spend_confirmation', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_added_daily_expense_bills)
    def added_daily_expense_bills(self):
        self.menu_manage()
        (self.step(key='new_disburse', desc='新增支出项')
         .step(key='new_types', desc='新增类型')
         .step(key='transaction_type', desc='交易类型')
         .custom(lambda: self.down_arrow_return(2))
         .step(key='types_of_daily_expenses', value='充话费' + self.serial, action='input', desc='日常费用类型')
         .step(key='type_of_use', desc='用途类型')
         .custom(lambda: self.down_arrow_return())
         .step(key='use_type_confirmation', desc='确定')
         .step(key='disburse_type', desc='支出类型')
         .custom(lambda: self.down_arrow_return())
         .step(key='disburse_price', value='100', action='input', desc='支出价格')
         .step(key='disburse_account', desc='支出账户')
         .custom(lambda: self.down_arrow_return())
         .step(key='handle', desc='经办人')
         .custom(lambda: self.down_arrow_return())
         .step(key='instructions', value=self.serial, action='input', desc='备注')
         .step(key='new_spend_confirmation', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_new_expenditure_adjustment_order)
    def new_expenditure_adjustment_order(self):
        self.menu_manage()
        (self.step(key='new_disburse', desc='新增支出项')
         .step(key='new_types', desc='新增类型')
         .step(key='transaction_type', desc='交易类型')
         .custom(lambda: self.down_arrow_return(2))
         .step(key='types_of_daily_expenses', value='充话费' + self.serial, action='input', desc='日常费用类型')
         .step(key='type_of_use', desc='用途类型')
         .custom(lambda: self.down_arrow_return(2))
         .step(key='use_type_confirmation', desc='确定')
         .step(key='disburse_type', desc='支出类型')
         .custom(lambda: self.down_arrow_return())
         .step(key='disburse_price', value='125', action='input', desc='支出价格')
         .step(key='disburse_account', desc='支出账户')
         .custom(lambda: self.down_arrow_return())
         .step(key='handle', desc='经办人')
         .custom(lambda: self.down_arrow_return())
         .step(key='instructions', value=self.serial, action='input', desc='备注')
         .step(key='new_spend_confirmation', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_daily_expenses_export_all)
    def daily_expenses_export_all(self):
        self.menu_manage()
        (self.step(key='scan_the_code_receive', desc='导出全部')
         .wait())
        return self


class FinanceDailyIncomePages(CommonPages):
    """财务管理|业务记账|日常收入"""

    def menu_manage(self):
        """菜单"""
        (self.scroll(key='financial_manage_menu', desc='财务管理')
         .step(key='financial_manage_menu', desc='财务管理')
         .step(key='financial_business_bookkeeping_menu', desc='业务记账')
         .step(key='financial_daily_income_menu', desc='日常收入')
         .wait())
        return self

    @reset_after_execution
    @doc(f_new_income)
    def new_income(self):
        self.menu_manage()
        (self.step(key='new_income', desc='新增收入项')
         .step(key='income_type', desc='收入类型')
         .custom(lambda: self.down_arrow_return())
         .step(key='income_price', value='21', action='input', desc='收入价格')
         .step(key='income_account', desc='收入账户')
         .custom(lambda: self.down_arrow_return())
         .step(key='handle', desc='经办人')
         .custom(lambda: self.down_arrow_return())
         .step(key='instructions', value='新增收入项备注', action='input', desc='备注')
         .step(key='new_spend_confirmation', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_new_daily_income_bills)
    def new_daily_income_bills(self):
        self.menu_manage()
        (self.step(key='new_income', desc='新增收入项')
         .step(key='new_types', desc='新增类型')
         .step(key='transaction_type', desc='交易类型')
         .custom(lambda: self.down_arrow_return(2))
         .step(key='types_of_daily_expenses', value='充话费' + self.serial, action='input', desc='日常费用类型')
         .step(key='type_of_use', desc='用途类型')
         .custom(lambda: self.down_arrow_return())
         .step(key='the_type_of_use_is_determined', desc='确定')
         .custom(lambda: self.wait_time())
         .step(key='income_type', desc='收入类型')
         .custom(lambda: self.down_arrow_return())
         .step(key='income_price', value='100', action='input', desc='收入价格')
         .step(key='income_account', desc='收入账户')
         .custom(lambda: self.down_arrow_return())
         .step(key='handle', desc='经办人')
         .custom(lambda: self.down_arrow_return())
         .step(key='instructions', value=self.serial, action='input', desc='备注')
         .step(key='new_spend_confirmation', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_new_revenue_adjustment_order)
    def new_revenue_adjustment_order(self):
        self.menu_manage()
        (self.step(key='new_income', desc='新增收入项')
         .step(key='new_types', desc='新增类型')
         .step(key='transaction_type', desc='交易类型')
         .custom(lambda: self.down_arrow_return(2))
         .step(key='types_of_daily_expenses', value='充话费' + self.serial, action='input', desc='日常费用类型')
         .step(key='type_of_use', desc='用途类型')
         .custom(lambda: self.down_arrow_return())
         .step(key='the_type_of_use_is_determined', desc='确定')
         .custom(lambda: self.wait_time())
         .step(key='income_type', desc='收入类型')
         .custom(lambda: self.down_arrow_return())
         .step(key='income_price', value='100', action='input', desc='收入价格')
         .step(key='income_account', desc='收入账户')
         .custom(lambda: self.down_arrow_return())
         .step(key='handle', desc='经办人')
         .custom(lambda: self.down_arrow_return())
         .step(key='instructions', value=self.serial, action='input', desc='备注')
         .step(key='new_spend_confirmation', desc='确定')
         .wait())
        return self


class FinanceExchangesAndReceivablesPages(CommonPages):
    """财务管理|业务记账|往来应收"""

    def menu_manage(self):
        """菜单"""
        (self.step(key='financial_manage_menu', desc='财务管理')
         .step(key='financial_business_bookkeeping_menu', desc='业务记账')
         .step(key='financial_receivables_menu', desc='往来应收')
         .wait())
        return self

    @reset_after_execution
    @doc(f_customers_settle_bills)
    def customers_settle_bills(self):
        self.menu_manage()
        (self.step(key='customer', desc='客户')
         .step(key='customer', value=INFO['vice_sales_customer_name'], action='input', desc='客户')
         .custom(lambda: self.up_arrow_return())
         .step(key='search', desc='搜索')
         .step(key='receivables_reconciliation', desc='对账')
         .custom(lambda: self.wait_time())
         .step(key='customer_settlement', desc='按客户结算')
         .step(key='collection_time', desc='收款时间')
         .step(key='confirmation_of_the_payment_time', desc='确定')
         .step(key='collection_account', desc='收款账户')
         .custom(lambda: self.up_arrow_return())
         .step(key='settlement_amount', value='8', action='input', desc='结算金额')
         .step(key='remark', value=self.serial, action='input', desc='备注')
         .step(key='vendor_settlement_confirmation', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_customer_import_order_settlement)
    def customer_import_order_settlement(self):
        self.menu_manage()
        self.file.get_inventory_data('financial_settlement', 'imei', i=3, j=9)
        (self.step(key='customer', desc='客户')
         .step(key='customer', value=INFO['vice_sales_customer_name'], action='input', desc='客户')
         .custom(lambda: self.up_arrow_return())
         .step(key='search', desc='搜索')
         .step(key='receivables_reconciliation', desc='对账')
         .custom(lambda: self.wait_time())
         .step(key='order_settlement', desc='按机器批量结算')
         .step(key='import_into_machine_btn', desc='导入机器')
         .step(key='machine_settlement_import', value=self.file_path('financial_settlement'), action='upload', desc='上传文件')
         .step(key='import_the_machine_to_confirm', desc='确定')
         .step(key='please_select_the_payout_account', desc='收款账户')
         .custom(lambda: self.up_arrow_return())
         .scroll('machine_settlement_input_amount', desc='结算金额')
         .step(key='reject_the_note', value='11', action='input', desc='结算金额')
         .step(key='submit_settlement', desc='提交结算')
         .wait())
        return self

    @reset_after_execution
    @doc(f_settlement_edit_amount)
    def settlement_edit_amount(self):
        self.menu_manage()
        (self.step(key='customer', desc='客户')
         .step(key='customer', value=INFO['vice_sales_customer_name'], action='input', desc='客户')
         .custom(lambda: self.up_arrow_return())
         .step(key='search', desc='搜索')
         .step(key='receivables_reconciliation', desc='对账')
         .custom(lambda: self.wait_time())
         .step(key='search', desc='搜索')
         .custom(lambda: self.tab_return(7))
         .step(key='settlement_by_order', desc='按订单批量结算')
         .step(key='please_select_the_payout_account', desc='收款账号')
         .custom(lambda: self.down_arrow_return())
         .step(key='reject_the_note', value='2', action='input', desc='结算金额')
         .step(key='order_tip_ok_btn', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_settlement_edit_largest_amount)
    def settlement_edit_largest_amount(self):
        self.menu_manage()
        (self.step(key='customer', desc='客户')
         .step(key='customer', value=INFO['vice_sales_customer_name'], action='input', desc='客户')
         .custom(lambda: self.up_arrow_return())
         .step(key='search', desc='搜索')
         .step(key='receivables_reconciliation', desc='对账')
         .custom(lambda: self.wait_time())
         .step(key='settlement_btn', desc='结算')
         .step(key='please_select_the_payout_account', desc='收款账号')
         .custom(lambda: self.down_arrow_return())
         .step(key='reject_the_note', value='99999', action='input', desc='结算金额')
         .step(key='order_tip_ok_btn', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_settlement_export)
    def settlement_export(self):
        self.menu_manage()
        (self.step(key='customer', desc='客户')
         .step(key='customer', value=INFO['vice_sales_customer_name'], action='input', desc='客户')
         .custom(lambda: self.up_arrow_return())
         .step(key='search', desc='搜索')
         .step(key='receivables_reconciliation', desc='对账')
         .step(key='export_btn', desc='导出')
         .wait())
        return self


class FinancePrePayReceivedPages(CommonPages):
    """财务管理|业务记账|预付预收"""

    def menu_manage(self):
        """菜单"""
        (self.scroll(key='financial_manage_menu', desc='财务管理')
         .step(key='financial_manage_menu', desc='财务管理')
         .step(key='financial_business_bookkeeping_menu', desc='业务记账')
         .step(key='financial_prepay_received_nemu', desc='预付/预收')
         .wait())
        return self

    @reset_after_execution
    @doc(f_add_prepay)
    def add_prepay(self):
        self.menu_manage()
        (self.step(key='delivery_receipt', desc='预付款tab')
         .step(key='add_prepay_btn', desc='新增预付款')
         .step(key='supplier_btn', desc='供应商')
         .custom(lambda: self.down_arrow_return())
         .step(key='please_enter_the_amount_of_the_prepayment', value=16, action='input', desc='金额')
         .step(key='pay_account_input', desc='预付账户')
         .custom(lambda: self.down_arrow_return())
         .step(key='payment_time', value=self.date_time, action='input', desc='日期')
         .custom(lambda: self.carriage_return())
         .step(key='handle', desc='经办人')
         .custom(lambda: self.down_arrow_return())
         .step(key='remark_input', value=self.serial, action='input', desc='备注')
         .step(key='determination', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_add_prepay_export)
    def add_prepay_export(self):
        self.menu_manage()
        (self.step(key='delivery_receipt', desc='预付款tab')
         .step(key='scan_receive_btn', desc='导出')
         .wait())
        return self

    @reset_after_execution
    @doc(f_add_received)
    def add_received(self):
        self.menu_manage()
        (self.step(key='procurement_info', desc='预收款tab')
         .step(key='add_received_btn', desc='新增预收款')
         .step(key='customer_btn', desc='供应商')
         .custom(lambda: self.down_arrow_return())
         .step(key='pre_receipt_price_input', value=13, action='input', desc='金额')
         .step(key='receive_account_input', desc='预收账户')
         .custom(lambda: self.down_arrow_return())
         .step(key='collection_time', value=self.date_time, action='input', desc='日期')
         .custom(lambda: self.carriage_return())
         .step(key='handle', desc='经办人')
         .custom(lambda: self.down_arrow_return())
         .step(key='remark_input', value=self.serial, action='input', desc='备注')
         .step(key='determination', desc='确定')
         .wait())
        return self

    @reset_after_execution
    @doc(f_add_received_export)
    def add_received_export(self):
        self.menu_manage()
        (self.step(key='procurement_info', desc='预收tab')
         .step(key='scan_receive_btn', desc='导出')
         .wait())
        return self
