# coding: utf-8
import json
import time
from common.base_api import BaseApi
from common.base_params import InitializeParams, is_performance_close
from common.import_desc import *
from config.user_info import INFO


class FinanceAccountListRequest(InitializeParams):
    """财务管理|资金账户|账户列表"""

    @doc(f_create_account)
    @BaseApi.timing_decorator
    def create_account(self, nocheck=False):
        data = {
            "accountName": "账户名称" + self.imei,
            "accountType": 6,
            "accountBalance": 9999,
            "remark": "备注"
        }
        return self._make_request('post', 'add_account', data, 'idle', nocheck)

    @doc(f_edit_account)
    @BaseApi.timing_decorator
    def edit_account(self, nocheck=False):
        res = self.pc.finance_account_list_data()
        data = {
            "id": res[0]['id'],
            "accountName": res[0]['accountName'],
            "accountType": res[0]['accountType'],
            "rechargePrice": 5,
            "remark": "备注"
        }
        return self._make_request('put', 'edit_account', data, 'idle', nocheck)

    @doc(f_account_transfer)
    @BaseApi.timing_decorator
    def account_transfer(self, nocheck=False):
        data = {
            "time": self.get_formatted_datetime(),
            "accountBalance": 5,
            "id": INFO['idle_account_no'],
            "rollId": INFO['idle_out_account_no']
        }
        return self._make_request('post', 'transfer_account', data, 'idle', nocheck)


class FinanceBillReviewRequest(InitializeParams):
    """财务管理|业务记账|账单审核"""

    @doc(f_financial_audit_deal_with)
    @BaseApi.timing_decorator
    def financial_audit_deal_with(self, nocheck=False):
        for _ in range(5):
            time.sleep(2)
            self.pc.finance_bill_review_data(i=1, j=0)
        res = self.pc.finance_bill_review_data(i=1, j=0)
        data = {
            "billNoList": [
                res[0]['billNo']
            ],
            "auditStatus": 1,
            "accountNo": INFO['main_account_no'],
            "ids": [
                res[0]['id']
            ],
            "oldAccountNoList": [
                INFO['main_account_no']
            ]
        }
        return self._make_request('put', 'the_submission_is_approved', data, 'main', nocheck)

    @doc(f_audit_accounts_payable_turn_down)
    @BaseApi.timing_decorator
    def audit_accounts_payable_turn_down(self, nocheck=False):
        res = self.pc.finance_bill_review_data(i=1, j=0)
        data = {
            "billNoList": [
                res[0]['billNo']
            ],
            "auditStatus": 2,
            "remark": "原因",
            "ids": [
                res[0]['id']
            ],
            "oldAccountNoList": [
                INFO['main_account_no']
            ]
        }
        return self._make_request('put', 'the_submission_is_approved', data, 'main', nocheck)

    @doc(f_financial_audit_receivable)
    @BaseApi.timing_decorator
    def financial_audit_receivable(self, nocheck=False):
        for _ in range(5):
            time.sleep(2)
            self.pc.finance_bill_review_data(i=2, j=0)
        res = self.pc.finance_bill_review_data(i=2, j=0)
        data = {
            "billNoList": [
                res[0]['billNo']
            ],
            "auditStatus": 1,
            "accountNo": INFO['main_account_no'],
            "ids": [
                res[0]['id']
            ],
            "oldAccountNoList": [
                INFO['main_account_no']
            ]
        }
        return self._make_request('put', 'the_submission_is_approved', data, 'main', nocheck)

    @doc(f_account_receivable_audit_turn_down)
    @BaseApi.timing_decorator
    def account_receivable_audit_turn_down(self, nocheck=False):
        res = self.pc.finance_bill_review_data(i=2, j=0)
        data = {
            "billNoList": [
                res[0]['billNo']
            ],
            "auditStatus": 2,
            "remark": "test",
            "ids": [
                res[0]['id']
            ],
            "oldAccountNoList": [
                INFO['main_account_no'],
            ]
        }
        return self._make_request('put', 'the_submission_is_approved', data, 'main', nocheck)

    @doc(f_financial_audit_receivable_vice)
    @BaseApi.timing_decorator
    def financial_audit_receivable_vice(self, nocheck=False):
        res = self.pc.finance_bill_review_data(data='a', i=2, j=0)
        data = {
            "billNoList": [
                res[0]['billNo']
            ],
            "auditStatus": 1,
            "accountNo": INFO['vice_account_no'],
            "ids": [
                res[0]['id']
            ],
            "oldAccountNoList": [
                INFO['vice_account_no']
            ]
        }
        return self._make_request('put', 'the_submission_is_approved', data, 'vice', nocheck)


class FinanceCopingWithEachOtherRequest(InitializeParams):
    """财务管理|业务记账|往来应付"""

    @doc(f_settle_by_order_machine)
    @BaseApi.timing_decorator
    def settle_by_order_machine(self, nocheck=False):
        res = self.pc.finance_coping_with_each_other_data()
        data = {
            "accountNo": INFO['main_account_no'],
            "supplierId": INFO['main_supplier_id'],
            "userType": "2",
            "payType": "2",
            "remark": "备注",
            "accountName": INFO['main_account_name'],
            "supplierName": INFO['main_supplier_name'],
            "orderBills": [
                {
                    "billNo": res[0]['billNo'],
                    "settlementAmount": res[0]['payableAmount']
                }
            ]
        }
        return self._make_request('post', 'settle_by_order_machine', data, 'main', nocheck)

    @doc(f_supplier_settlement)
    @BaseApi.timing_decorator
    def supplier_settlement(self, nocheck=False):
        data = {
            "supplierId": INFO['main_supplier_id'],
            "isReconciliationDetailPage": True,
            "userType": "2",
            "payType": "2",
            "payTime": self.get_formatted_datetime(),
            "accountNo": INFO['main_account_no'],
            "amount": 5,
            "supplierName": INFO['main_supplier_name'],
            "accountName": INFO['main_account_name']
        }
        return self._make_request('post', 'settle_by_supplier', data, 'main', nocheck)

    @doc(f_order_settlement)
    @BaseApi.timing_decorator
    def order_settlement(self, nocheck=False):
        res = self.pc.finance_coping_with_each_other_data(data='b')
        data = {
            "accountNo": INFO['main_account_no'],
            "supplierId": INFO['main_supplier_id'],
            "userType": "2",
            "payType": "2",
            "supplierName": INFO['main_supplier_name'],
            "accountName": INFO['main_account_name'],
            "articlesBills": [
                {
                    "billNo": None,
                    "type": None,
                    "articlesNo": res[0]['articlesNo'],
                    "paidAmount": 1,
                    "payableAmount": res[0]['amount']
                }
            ]
        }
        return self._make_request('post', 'settle_by_order_machine', data, 'main', nocheck)

    @doc(f_settle_vendor_amount_all)
    @BaseApi.timing_decorator
    def settle_vendor_amount_all(self, nocheck=False):
        res = self.pc.finance_coping_with_each_other_data(data='d')
        data = {
            "supplierId": INFO['main_supplier_id'],
            "isReconciliationDetailPage": True,
            "userType": "2",
            "payType": "2",
            "amount": res[0]['amount'],
            "payTime": self.get_formatted_datetime(),
            "accountNo": INFO['main_account_no'],
            "supplierName": INFO['main_supplier_name'],
            "accountName": INFO['main_account_name']
        }
        return self._make_request('post', 'settle_by_supplier', data, 'main', nocheck)

    @doc(f_prepayment_deduction_all)
    @BaseApi.timing_decorator
    def prepayment_deduction_all(self, nocheck=False):
        res = self.pc.finance_coping_with_each_other_data(data='d')
        data = {
            "supplierId": INFO['main_supplier_id'],
            "isReconciliationDetailPage": True,
            "userType": "2",
            "payType": "2",
            "amount": res[0]['amount'],
            "payTime": self.get_formatted_datetime(),
            "accountNo": INFO['main_account_no'],
            "supplierName": INFO['main_supplier_name'],
            "accountName": INFO['main_account_name'],
            "deductionList": [
                {
                    "preId": res[0]["id"],
                    "deductionAmount": res[0]['userAmount']
                }
            ]
        }
        return self._make_request('post', 'settle_by_supplier', data, 'main', nocheck)

    @doc(f_prepayment_deduction_part)
    @BaseApi.timing_decorator
    def prepayment_deduction_part(self, nocheck=False):
        res = self.pc.finance_coping_with_each_other_data(data='d')
        data = {
            "supplierId": INFO['main_supplier_id'],
            "isReconciliationDetailPage": True,
            "userType": "2",
            "payType": "2",
            "amount": res[0]['amount'] / 2,
            "payTime": self.get_formatted_datetime(),
            "accountNo": INFO['main_account_no'],
            "supplierName": INFO['main_supplier_name'],
            "accountName": INFO['main_account_name'],
            "deductionList": [
                {
                    "preId": res[0]["id"],
                    "deductionAmount": res[0]['userAmount'] / 2
                }
            ]
        }
        return self._make_request('post', 'settle_by_supplier', data, 'main', nocheck)

    @doc(f_settle_by_order_part)
    @BaseApi.timing_decorator
    def settle_by_order_part(self, nocheck=False):
        res = self.pc.finance_coping_with_each_other_data()
        data = {
            "accountNo": INFO['main_account_no'],
            "supplierId": INFO['main_supplier_id'],
            "userType": "2",
            "payType": "2",
            "accountName": INFO['main_account_name'],
            "supplierName": INFO['main_supplier_name'],
            "orderBills": [
                {
                    "billNo": res[0]['billNo'],
                    "settlementAmount": res[0]['payableAmount'] / 2
                }
            ]
        }
        return self._make_request('post', 'settle_by_order_machine', data, 'main', nocheck)

    @doc(f_settle_by_order_prepaid_part)
    @BaseApi.timing_decorator
    def settle_by_order_prepaid_part(self, nocheck=False):
        res = self.pc.finance_coping_with_each_other_data()
        res_2 = self.pc.finance_coping_with_each_other_data(data='d')
        data = {
            "accountNo": INFO['main_account_no'],
            "accountName": INFO['main_account_name'],
            "supplierId": INFO['main_supplier_id'],
            "userType": "2",
            "payType": "2",
            "supplierName": INFO['main_supplier_name'],
            "orderBills": [
                {
                    "billNo": res[0]['billNo'],
                    "settlementAmount": res[0]['payableAmount']
                }
            ],
            "deductionList": [
                {
                    "preId": res_2[0]["id"],
                    "deductionAmount": res_2[0]['userAmount'] / 2
                }
            ]
        }
        return self._make_request('post', 'settle_by_order_machine', data, 'main', nocheck)

    @doc(f_settle_by_order_prepaid_all)
    @BaseApi.timing_decorator
    def settle_by_order_prepaid_all(self, nocheck=False):
        res = self.pc.finance_coping_with_each_other_data()
        res_2 = self.pc.finance_coping_with_each_other_data(data='d')
        data = {
            "accountNo": INFO['main_account_no'],
            "accountName": INFO['main_account_name'],
            "supplierId": INFO['main_supplier_id'],
            "userType": "2",
            "payType": "2",
            "supplierName": INFO['main_supplier_name'],
            "orderBills": [
                {
                    "billNo": res[0]['billNo'],
                    "settlementAmount": res[0]['payableAmount']
                }
            ],
            "deductionList": [
                {
                    "preId": res_2[0]["id"],
                    "deductionAmount": res_2[0]['userAmount']
                }
            ]
        }
        return self._make_request('post', 'settle_by_order_machine', data, 'main', nocheck)

    @doc(f_settle_machine_settlement)
    @BaseApi.timing_decorator
    def settle_machine_settlement(self, nocheck=False):
        res = self.pc.finance_coping_with_each_other_data(data="b")
        data = {
            "accountNo": INFO['main_account_no'],
            "accountName": INFO['main_account_name'],
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "userType": "2",
            "payType": "2",
            "articlesBills": [
                {
                    "billNo": None,
                    "type": None,
                    "articlesNo": res[0]['articlesNo'],
                    "paidAmount": res[0]['unpaidAmount'],
                    "payableAmount": res[0]['amount']
                }
            ]
        }
        return self._make_request('post', 'settle_by_order_machine', data, 'main', nocheck)

    @doc(f_machine_deduction_party)
    @BaseApi.timing_decorator
    def machine_deduction_party(self, nocheck=False):
        res = self.pc.finance_coping_with_each_other_data(data="b")
        res_2 = self.pc.finance_coping_with_each_other_data(data='d')
        data = {
            "accountNo": INFO['main_account_no'],
            "accountName": INFO['main_account_name'],
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "userType": "2",
            "payType": "2",
            "articlesBills": [
                {
                    "billNo": None,
                    "type": None,
                    "articlesNo": res[0]['articlesNo'],
                    "paidAmount": res[0]['unpaidAmount'],
                    "payableAmount": res[0]['amount']
                }
            ],
            "deductionList": [
                {
                    "preId": res_2[0]['id'],
                    "deductionAmount": res_2[0]['userAmount'] / 2
                }
            ]
        }
        return self._make_request('post', 'settle_by_order_machine', data, 'main', nocheck)

    @doc(f_machine_deduction_all)
    @BaseApi.timing_decorator
    def machine_deduction_all(self, nocheck=False):
        res = self.pc.finance_coping_with_each_other_data(data="b")
        res_2 = self.pc.finance_coping_with_each_other_data(data='d')
        data = {
            "accountNo": INFO['main_account_no'],
            "accountName": INFO['main_account_name'],
            "supplierId": INFO['main_supplier_id'],
            "supplierName": INFO['main_supplier_name'],
            "userType": "2",
            "payType": "2",
            "articlesBills": [
                {
                    "billNo": None,
                    "type": None,
                    "articlesNo": res[0]['articlesNo'],
                    "paidAmount": res[0]['unpaidAmount'],
                    "payableAmount": res[0]['amount']
                }
            ],
            "deductionList": [
                {
                    "preId": res_2[0]["id"],
                    "deductionAmount": res_2[0]['userAmount']
                }
            ]
        }
        return self._make_request('post', 'settle_by_order_machine', data, 'main', nocheck)


class FinanceCostIncomeAdjustmentRequest(InitializeParams):
    """财务管理|成本收入调整"""

    @doc(f_new_adjustment_order_cost)
    @BaseApi.timing_decorator
    def new_adjustment_order_cost(self, nocheck=False):
        res = self.pc.inventory_list_data(i=2)
        data = {
            "adjustmentType": "1",
            "accountNo": INFO['main_account_no'],
            "adjustmentReason": 1,
            "articles": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "modelId": res[0]['modelId'],
                    "modelName": res[0]['modelName'],
                    "merchantId": INFO['main_supplier_id'],
                    "beforePrice": res[0]['purchasePrice'],
                    "afterPrice": 5,
                    "adjustmentPrice": 5,
                    "remark": "备注"
                }
            ]
        }
        return self._make_request('post', 'purchase_amount_change', data, 'main', nocheck)

    @doc(f_new_adjustment_order_cost_other_costs)
    @BaseApi.timing_decorator
    def new_adjustment_order_cost_other_costs(self, nocheck=False):
        res = self.pc.inventory_list_data()
        data = {
            "adjustmentType": "1",
            "adjustmentRemark": 750,
            "accountNo": INFO['main_account_no'],
            "adjustmentReason": 2,
            "articles": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "modelId": res[0]['modelId'],
                    "modelName": res[0]['modelName'],
                    "merchantId": INFO['main_supplier_id'],
                    "beforePrice": res[0]['purchasePrice'],
                    "afterPrice": 22,
                    "adjustmentPrice": 22,
                    "remark": "备注"
                }
            ]
        }
        return self._make_request('post', 'purchase_amount_change', data, 'main', nocheck)

    @doc(f_new_adjustment_order_income)
    @BaseApi.timing_decorator
    def new_adjustment_order_income(self, nocheck=False):
        res = self.pc.inventory_list_data(i='3', j='9')
        res_2 = self.pc.sell_sale_item_list_data()
        data = {
            "adjustmentType": "2",
            "accountNo": INFO['main_account_no'],
            "adjustmentReason": 1,
            "articles": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "modelId": res[0]['modelId'],
                    "modelName": res[0]['modelName'],
                    "merchantId": INFO['main_supplier_id'],
                    "beforePrice": res_2[0]['salePrice'],
                    "afterPrice": 50,
                    "adjustmentPrice": 50,
                    "remark": "备注"
                }
            ]
        }
        return self._make_request('post', 'purchase_amount_change', data, 'main', nocheck)

    @doc(f_new_adjustment_order_income_other_income)
    @BaseApi.timing_decorator
    def new_adjustment_order_income_other_income(self, nocheck=False):
        res = self.pc.inventory_list_data(i='3', j='9')
        res_2 = self.pc.sell_sale_item_list_data()
        data = {
            "adjustmentType": "2",
            "adjustmentRemark": 749,
            "accountNo": INFO['main_account_no'],
            "adjustmentReason": 2,
            "articles": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "modelId": res[0]['modelId'],
                    "modelName": res[0]['modelName'],
                    "merchantId": INFO['main_supplier_id'],
                    "beforePrice": res_2[0]['salePrice'],
                    "afterPrice": 50,
                    "adjustmentPrice": 50,
                    "remark": "test"
                }
            ]
        }
        return self._make_request('post', 'purchase_amount_change', data, 'main', nocheck)

    @doc(f_multi_item_other_income_adjustments)
    @BaseApi.timing_decorator
    def multi_item_other_income_adjustments(self, nocheck=False):
        res = self.pc.inventory_list_data(i='3', j='9')
        res_2 = self.pc.sell_sale_item_list_data()
        data = {
            "adjustmentType": "2",
            "adjustmentRemark": 749,
            "accountNo": INFO['main_account_no'],
            "adjustmentReason": 2,
            "articles": [
                {
                    "articlesNo": res[0]['articlesNo'],
                    "imei": res[0]['imei'],
                    "modelId": res[0]['modelId'],
                    "modelName": res[0]['modelName'],
                    "merchantId": INFO['main_supplier_id'],
                    "beforePrice": res_2[0]['salePrice'],
                    "afterPrice": 22,
                    "adjustmentPrice": 22,
                    "remark": "test"
                },
                {
                    "articlesNo": res[1]['articlesNo'],
                    "imei": res[1]['imei'],
                    "modelId": res[1]['modelId'],
                    "modelName": res[1]['modelName'],
                    "merchantId": INFO['main_supplier_id'],
                    "beforePrice": res_2[1]['salePrice'],
                    "afterPrice": 11,
                    "adjustmentPrice": 11,
                    "remark": "test"
                }
            ]
        }
        return self._make_request('post', 'purchase_amount_change', data, 'main', nocheck)


class FinanceDailyDisburseRequest(InitializeParams):
    """财务管理|业务记账|日常支出"""

    @doc(f_new_disburse)
    @BaseApi.timing_decorator
    def new_disburse(self, nocheck=False):
        data = {
            "type": 746,
            "amount": 100,
            "accountNo": INFO['main_account_no'],
            "time": self.get_formatted_datetime(),
            "userId": INFO['main_user_id'],
            "payType": "2",
            "accountName": INFO['main_account_name'],
            "userName": f"admin({INFO['main_account']})"
        }
        return self._make_request('post', 'daily_expenses', data, 'main', nocheck)

    @doc(f_new_expenditure_items_negative_amount)
    @BaseApi.timing_decorator
    def new_expenditure_items_negative_amount(self, nocheck=False):
        data = {
            "type": 746,
            "amount": -230,
            "accountNo": INFO['main_account_no'],
            "time": self.get_formatted_datetime(),
            "userId": INFO['main_user_id'],
            "payType": "2",
            "accountName": INFO['main_account_name'],
            "userName": f"admin({INFO['main_account']})"
        }
        return self._make_request('post', 'daily_expenses', data, 'main', nocheck)


class FinanceDailyIncomeRequest(InitializeParams):
    """财务管理|业务记账|日常收入"""

    @doc(f_new_income)
    @BaseApi.timing_decorator
    def new_income(self, nocheck=False):
        data = {
            "type": 748,
            "amount": 1,
            "accountNo": INFO['main_account_no'],
            "time": self.get_formatted_datetime(),
            "userId": INFO['main_user_id'],
            "remark": "备注",
            "payType": "1",
            "accountName": INFO['main_account_name'],
            "userName": f"admin({INFO['main_account']})"
        }
        return self._make_request('post', 'daily_income', data, 'main', nocheck)

    @doc(f_default_revenue_type_negative_amount)
    @BaseApi.timing_decorator
    def default_revenue_type_negative_amount(self, nocheck=False):
        data = {
            "type": 748,
            "amount": -100,
            "accountNo": INFO['main_account_no'],
            "time": self.get_formatted_datetime(),
            "userId": INFO['main_user_id'],
            "remark": "备注",
            "payType": "1",
            "accountName": INFO['main_account_name'],
            "userName": f"admin({INFO['main_account']})"
        }
        return self._make_request('post', 'daily_income', data, 'main', nocheck)


class FinanceExchangesAndReceivablesRequest(InitializeParams):
    """财务管理|业务记账|往来应收"""

    @doc(f_customer_order_machine_settlement)
    @BaseApi.timing_decorator
    def customer_order_machine_settlement(self, nocheck=False):
        res = self.pc.finance_exchanges_and_receivables_data(data='b')
        data = {
            "accountNo": INFO['main_account_no'],
            "supplierId": INFO['main_sale_supplier_id'],
            "userType": "1",
            "payType": "1",
            "remark": "备注",
            "accountName": INFO['main_account_name'],
            "supplierName": INFO['vice_sales_customer_name'],
            "articlesBills": [
                {
                    "billNo": None,
                    "type": None,
                    "articlesNo": res[0]['articlesNo'],
                    "paidAmount": 5,
                    "payableAmount": res[0]['amount']
                }
            ]
        }
        return self._make_request('post', 'settle_by_machine', data, 'main', nocheck)

    @doc(f_settle_the_full_amount_by_the_machine)
    @BaseApi.timing_decorator
    def settle_the_full_amount_by_the_machine(self, nocheck=False):
        res = self.pc.finance_exchanges_and_receivables_data(data='b')
        data = {
            "accountNo": INFO['main_account_no'],
            "supplierId": INFO['main_sale_supplier_id'],
            "userType": "1",
            "payType": "1",
            "remark": "备注",
            "accountName": INFO['main_account_name'],
            "supplierName": INFO['vice_sales_customer_name'],
            "articlesBills": [
                {
                    "billNo": None,
                    "type": None,
                    "articlesNo": res[0]['articlesNo'],
                    "paidAmount": res[0]['unpaidAmount'],
                    "payableAmount": res[0]['amount']
                }
            ]
        }
        return self._make_request('post', 'settle_by_machine', data, 'main', nocheck)

    @doc(f_the_machine_settles_all_part_of_the_amount)
    @BaseApi.timing_decorator
    def the_machine_settles_all_part_of_the_amount(self, nocheck=False):
        res = self.pc.finance_exchanges_and_receivables_data(data='b')
        res_2 = self.pc.finance_exchanges_and_receivables_data(data='d')
        data = {
            "accountNo": INFO['main_account_no'],
            "supplierId": INFO['main_sale_supplier_id'],
            "userType": "1",
            "payType": "1",
            "accountName": INFO['main_account_name'],
            "supplierName": INFO['vice_sales_customer_name'],
            "articlesBills": [
                {
                    "billNo": None,
                    "type": None,
                    "articlesNo": res[0]['articlesNo'],
                    "paidAmount": res[0]['unpaidAmount'],
                    "payableAmount": res[0]['amount']
                }
            ],
            "deductionList": [
                {
                    "preId": res_2[0]['id'],
                    "deductionAmount": res_2[0]['userAmount'] / 2
                }
            ]
        }
        return self._make_request('post', 'settle_by_machine', data, 'main', nocheck)

    @doc(f_customers_settle_bills)
    @BaseApi.timing_decorator
    def customers_settle_bills(self, nocheck=False):
        data = {
            "supplierId": INFO['main_sale_supplier_id'],
            "isReconciliationDetailPage": True,
            "userType": "1",
            "payType": "1",
            "amount": 5,
            "payTime": self.get_formatted_datetime(),
            "remark": "备注",
            "accountNo": INFO['main_account_no'],
            "supplierName": INFO['vice_sales_customer_name'],
            "accountName": INFO['main_account_name']
        }
        return self._make_request('post', 'settle_by_order_supplier', data, 'main', nocheck)

    @doc(f_the_customer_settles_the_full_amount)
    @BaseApi.timing_decorator
    def the_customer_settles_the_full_amount(self, nocheck=False):
        res = self.pc.finance_exchanges_and_receivables_data(data='d')
        data = {
            "supplierId": INFO['main_sale_supplier_id'],
            "isReconciliationDetailPage": True,
            "userType": "1",
            "payType": "1",
            "amount": res[0]['amount'],
            "payTime": self.get_formatted_datetime(),
            "accountNo": INFO['main_account_no'],
            "supplierName": INFO['vice_sales_customer_name'],
            "accountName": INFO['main_account_name']
        }
        return self._make_request('post', 'settle_by_order_supplier', data, 'main', nocheck)

    @doc(f_settlement_un_edit_amount)
    @BaseApi.timing_decorator
    def settlement_un_edit_amount(self, nocheck=False):
        res = self.pc.finance_exchanges_and_receivables_data()
        data = {
            "accountNo": INFO['main_account_no'],
            "supplierId": INFO['main_sale_supplier_id'],
            "userType": "1",
            "payType": "1",
            "accountName": INFO['main_account_name'],
            "supplierName": INFO['vice_sales_customer_name'],
            "orderBills": [
                {
                    "billNo": res[0]['billNo'],
                    "settlementAmount": res[0]['payableAmount']
                }
            ]
        }
        return self._make_request('post', 'settle_by_order_machine', data, 'main', nocheck)

    @doc(f_all_settlement_prepaid_part_of_the_amount)
    @BaseApi.timing_decorator
    def all_settlement_prepaid_part_of_the_amount(self, nocheck=False):
        res = self.pc.finance_exchanges_and_receivables_data()
        res_2 = self.pc.finance_exchanges_and_receivables_data(data='d')
        data = {
            "accountNo": INFO['main_account_no'],
            "supplierId": INFO['main_sale_supplier_id'],
            "userType": "1",
            "payType": "1",
            "remark": "备注",
            "accountName": INFO['main_account_name'],
            "supplierName": INFO['vice_sales_customer_name'],
            "orderBills": [
                {
                    "billNo": res[0]['billNo'],
                    "settlementAmount": res[0]['payableAmount']
                }
            ],
            "deductionList": [
                {
                    "preId": res_2[0]['id'],
                    "deductionAmount": res_2[0]['userAmount'] / 2
                }
            ]
        }
        return self._make_request('post', 'settle_by_order_machine', data, 'main', nocheck)

    @doc(f_settle_all_advance_receipt_of_the_entire_amount)
    @BaseApi.timing_decorator
    def settle_all_advance_receipt_of_the_entire_amount(self, nocheck=False):
        res = self.pc.finance_exchanges_and_receivables_data()
        res_2 = self.pc.finance_exchanges_and_receivables_data(data='d')
        data = {
            "accountNo": INFO['main_account_no'],
            "supplierId": INFO['main_sale_supplier_id'],
            "userType": "1",
            "payType": "1",
            "remark": "备注",
            "accountName": INFO['main_account_name'],
            "supplierName": INFO['vice_sales_customer_name'],
            "orderBills": [
                {
                    "billNo": res[0]['billNo'],
                    "settlementAmount": res[0]['payableAmount']
                }
            ],
            "deductionList": [
                {
                    "preId": res_2[0]['id'],
                    "deductionAmount": res_2[0]['userAmount']
                }
            ]
        }
        return self._make_request('post', 'settle_by_order_machine', data, 'main', nocheck)

    @doc(f_settle_all_prepaid_part_of_the_amount)
    @BaseApi.timing_decorator
    def settle_all_prepaid_part_of_the_amount(self, nocheck=False):
        res = self.pc.finance_exchanges_and_receivables_data(data='d')
        data = {
            "supplierId": INFO['main_sale_supplier_id'],
            "isReconciliationDetailPage": True,
            "userType": "1",
            "payType": "1",
            "payTime": self.get_formatted_datetime(),
            "accountNo": INFO['main_account_no'],
            "amount": res[0]['amount'] / 2,
            "accountName": INFO['main_account_name'],
            "supplierName": INFO['vice_sales_customer_name'],
            "deductionList": [
                {
                    "preId": res[0]['id'],
                    "deductionAmount": res[0]['userAmount'] / 2
                }
            ]
        }
        return self._make_request('post', 'settle_by_order_supplier', data, 'main', nocheck)

    @doc(f_full_settlement_the_entire_amount_of_the_presale)
    @BaseApi.timing_decorator
    def full_settlement_the_entire_amount_of_the_presale(self, nocheck=False):
        res = self.pc.finance_exchanges_and_receivables_data(data='d')
        data = {
            "supplierId": INFO['main_sale_supplier_id'],
            "isReconciliationDetailPage": True,
            "userType": "1",
            "payType": "1",
            "payTime": self.get_formatted_datetime(),
            "accountNo": INFO['main_account_no'],
            "amount": res[0]['amount'] / 2,
            "accountName": INFO['main_account_name'],
            "supplierName": INFO['vice_sales_customer_name'],
            "deductionList": [
                {
                    "preId": res[0]['id'],
                    "deductionAmount": res[0]['userAmount']
                }
            ]
        }
        return self._make_request('post', 'settle_by_order_supplier', data, 'main', nocheck)


class FinancePrePayReceivedRequest(InitializeParams):
    """财务管理|业务记账|预付预收"""

    @doc(f_add_prepay)
    @BaseApi.timing_decorator
    def add_prepay(self, nocheck=False):
        data = {
            "amount": 100,
            "preType": "2",
            "receiptTime": self.get_the_date(),
            "remark": "备注",
            "supplierId": INFO['main_supplier_id'],
            "accountNo": INFO['main_account_no'],
            "userId": INFO['main_user_id'],
            "supplierName": INFO['main_supplier_name'],
            "userName": INFO['main_account'],
        }
        return self._make_request('post', 'add_prepay', data, 'main', nocheck)

    @doc(f_add_received)
    @BaseApi.timing_decorator
    def add_received(self, nocheck=False):
        data = {
            "preType": "1",
            "receiptTime": self.get_the_date(),
            "remark": "备注",
            "amount": 100,
            "supplierId": INFO['main_sale_supplier_id'],
            "accountNo": INFO['main_account_no'],
            "userId": INFO['main_user_id'],
            "supplierName": INFO['vice_sales_customer_name'],
            "userName": INFO['main_manager']
        }
        return self._make_request('post', 'add_prepay', data, 'main', nocheck)


if __name__ == '__main__':
    api = None
    result = api
    print(json.dumps(result, indent=4, ensure_ascii=False))
