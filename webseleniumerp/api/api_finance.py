# coding: utf-8
import json
import time

from common.base_api import BaseApi
from config.user_info import INFO


class FinanceAccountListApi(BaseApi):
    """财务管理|资金账户|账户列表"""

    def account_list(self, headers=None, num=1, size=1000):
        """账户列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['finance_account_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def account_statistics(self, headers=None):
        """账户列表 统计"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['finance_account_list'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)

    # 获取账户编号
    def get_account_no(self):
        return self._get_field_copy_value('account_list', 'main', 'accountNo')

    # 获取账户编号
    def get_account_no_vice(self):
        return self._get_field_copy_value('account_list', 'vice', 'accountNo')

    # 获取账户名称
    def get_account_name(self):
        return self._get_field_copy_value('account_list', 'main', 'accountName')

    # 获取账户id
    def get_account_id_idle(self):
        return self._get_field_copy_value('account_list', 'idle', 'id')

    # 获取账户id
    def get_account_id_idle_two(self):
        return self._get_field_copy_value('account_list', 'idle', 'id', index=1)


class FinanceAnalyzeApi(BaseApi):
    """财务管理|财务报表|经营分析表"""

    def statics_data(self, headers=None):
        """统计"""
        headers = headers or self.headers['main']
        year = self.get_the_date().split('-')[0]
        response = self.request_handle('get', self.urls['business_analyze_statics'] + year, headers=headers)
        return self.get_response_data(response, 'data', list)


class FinanceBillReviewApi(BaseApi):
    """财务管理|业务记账|账单审核"""

    def payable_bill(self, headers=None, i=None, j=None, num=1, size=1000):
        """应付账单
        i：1应付 2应收
        j: 0待审核 1审核通过 2未通过
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'bill_type': i, 'auditStatus': j}
        response = self.request_handle('post', self.urls['bill_review'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class FinanceCollectionAndSettlementApi(BaseApi):
    """财务管理|业务记账|收款结算单"""

    def collection_and_settlement(self, headers=None, num=1, size=1000):
        """收款结算单列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'userType': '1'}
        response = self.request_handle('post', self.urls['payment_settlement'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class FinanceCommissionPaySettingApi(BaseApi):
    """财务管理|财务设置|分佣付款设置"""

    def commission_pay_setting_list(self, headers=None):
        """分佣付款设置"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "payType": "1"}
        response = self.request_handle('post', self.urls['commission_setting'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)


class FinanceCommissionSettingApi(BaseApi):
    """财务管理|财务设置|分佣收款设置"""

    def commission_setting_list(self, headers=None):
        """分佣收款设置"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "payType": "1"}
        response = self.request_handle('post', self.urls['commission_setting'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)


class FinanceCopingWithEachOtherApi(BaseApi):
    """财务管理|业务记账|往来应付"""

    def reconciliation_details_list(self, headers=None, num=1, size=1000):
        """对账详情"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'supplierId': str(INFO['main_supplier_id']), 'userType': "2",  'startTime': self.get_the_date(-181), 'endTime': self.get_the_date()}
        response = self.request_handle('post', self.urls['reconciliation_details'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def machine_list(self, headers=None):
        """按机器结算 添加机器 机器列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'supplierId': str(INFO['main_supplier_id']), 'userType': 2, 'payType': '2'}
        response = self.request_handle('post', self.urls['machine_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def pay_list(self, headers=None, num=1, size=1000):
        """往来应付列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), "billOff": 0, "userType": "2", "payType": "2",   'supplierId': INFO['main_supplier_id']}
        response = self.request_handle('post', self.urls['coping_with_each_other'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def prepaid_slips_list(self, headers=None):
        """按供应商结算 列表"""
        headers = headers or self.headers['main']
        data = {"supplierId": INFO['main_supplier_id'], "preType": "2"}
        response = self.request_handle('post', self.urls['prepaid_slips_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res

    def reconciliation_details_list_info(self, headers=None):
        """对账详情 单据详情"""
        headers = headers or self.headers['main']
        bill_no = self.get_bill_no()
        data = {**self.get_page_params(), 'total': 0, 'billNo': bill_no}
        response = self.request_handle('post', self.urls['details_of_the_receivables'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    # 获取单据编号
    def get_bill_no(self):
        return self._get_field_copy_value('reconciliation_details_list', 'main', 'billNo')

class FinanceCostIncomeAdjustmentApi(BaseApi):
    """财务管理|成本收入调整"""

    def cost_income_adjustment(self, headers=None, num=1, size=1000):
        """单据列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['cost_income_adjustment'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def document_list_details(self, headers=None, adjustment_no=None):
        """单据列表 详情"""
        headers = headers or self.headers['main']
        adjustment_no = adjustment_no or self.get_adjustment_no()
        data = {**self.get_page_params()}
        response = self.request_handle('get', self.urls['cost_income_adjustment_detail'] + '/' + adjustment_no, data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res

    def list_of_items(self, headers=None, num=1, size=1000):
        """物品列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['cost_income_adjustment_item_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def get_adjustment_no(self):
        """获取单据编号"""
        return self._get_field_copy_value('cost_income_adjustment', 'main', 'adjustmentNo')


class FinanceCustomerPaySettingApi(BaseApi):
    """财务管理|财务设置|客户收款设置"""

    def pay_setting_list(self, headers=None):
        """客户收款设置"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['supplier_setting'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)


class FinanceDailyExpenditureApi(BaseApi):
    """财务管理|业务记账|日常支出"""

    def daily_expenditure(self, headers=None, num=1, size=1000):
        """日常支出列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'payType': '2'}
        response = self.request_handle('post', self.urls['daily_expenditure_income'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def expense_statistics_amount(self, headers=None):
        """统计金额"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'payType': '2'}
        response = self.request_handle('post', self.urls['daily_expenditure_income_total'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)


class FinanceDailyIncomeApi(BaseApi):
    """财务管理|业务记账|日常收入"""

    def daily_income(self, headers=None, num=1, size=1000):
        """日常收入列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'payType': '1'}
        response = self.request_handle('post', self.urls['daily_expenditure_income'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def expense_statistics_amount(self, headers=None):
        """统计金额"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'payType': '1'}
        response = self.request_handle('post', self.urls['daily_expenditure_income_total'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', dict)


class FinanceExchangesAndReceivablesApi(BaseApi):
    """财务管理|业务记账|往来应收"""

    def reconciliation_details_list(self, headers=None, num=1, size=1000):
        """对账详情"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'supplierId': str(INFO['main_sale_supplier_id']), 'userType': 1, 'startTime': self.get_the_date(), 'endTime': self.get_the_date()}
        response = self.request_handle('post', self.urls['receivables_reconciliation_details'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def machine_list(self, headers=None):
        """按机器结算-添加机器-机器列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'supplierId': str(INFO['main_sale_supplier_id']), 'userType': 1, 'payType': '1'}
        response = self.request_handle('post', self.urls['machine_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def receive_list(self, headers=None, num=1, size=1000):
        """往来应收列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), "billOff": 0, "userType": "1", "payType": "1", 'supplierId': INFO['main_sale_supplier_id']}
        response = self.request_handle('post', self.urls['coping_with_each_other'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def customer_settlement_advance_receipts(self, headers=None):
        """按客户结算 列表"""
        headers = headers or self.headers['main']
        data = {"preType": "1", 'supplierId': INFO['main_sale_supplier_id']}
        response = self.request_handle('post', self.urls['prepaid_slips_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res

    def reconciliation_details_list_info(self, headers=None):
        """对账详情 单据详情"""
        headers = headers or self.headers['main']
        bill_no = self.get_bill_no()
        data = {**self.get_page_params(), 'total': 0, 'billNo': bill_no}
        response = self.request_handle('post', self.urls['details_of_the_receivables'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    # 获取单据号
    def get_bill_no(self):
        return self._get_field_copy_value('reconciliation_details_list', 'main', 'billNo')

    # 获取未收金额合计
    def get_periodic_end_amount(self):
        return self._get_field_copy_value('receive_list', 'main', 'periodicEndAmount')


class FinanceFeeSettingApi(BaseApi):
    """财务管理|财务设置|费用项目类型设置"""

    def setting_list(self, headers=None):
        """费用项目类型设置"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['fee_setting'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)


class FinancePaymentSettlementApi(BaseApi):
    """财务管理|业务记账|付款结算单"""

    def payment_settlement(self, headers=None, num=1, size=1000):
        """付款结算单列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'userType': '2'}
        response = self.request_handle('post', self.urls['payment_settlement'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res


class FinancePrepayReceiveListApi(BaseApi):
    """财务管理|业务记账|预收预付"""

    def prepay_list(self, i=None, headers=None, num=1, size=1000):
        """预付、预收列表
        i：1 预付 2预收
        """
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size), 'preType': i}
        response = self.request_handle('post', self.urls['prepaid_list'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def receive_prepay_detail(self, headers=None):
        """预收/预付详情"""
        headers = headers or self.headers['main']
        response = self.request_handle('get', self.urls['prepaid_detail'] + self.get_prepay_list_id(), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    # 获取预付id
    def get_prepay_list_id(self):
        return self._get_field_copy_value('prepay_list', 'main', 'id')


class FinanceSupplierSettingApi(BaseApi):
    """财务管理|财务设置|供应商付款设置"""

    def supplier_setting_list(self, headers=None):
        """供应商付款设置"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['supplier_setting'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'data', list)


class FinanceTransactionDetailsApi(BaseApi):
    """财务管理|资金账户|交易明细"""

    def transaction_details(self, headers=None, num=1, size=1000):
        """交易明细"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(num, size)}
        response = self.request_handle('post', self.urls['transaction_details'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'rows', list)
        self.make_pkl_file(res)
        return res

    def get_merchant_name(self):
        return self._get_field_copy_value('transaction_details', 'main', 'merchantName')


if __name__ == '__main__':
    api = FinanceBillReviewApi()
    result = api.payable_bill(i=2, j=0)
    print(json.dumps(result, indent=4, ensure_ascii=False))
