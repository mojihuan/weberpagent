# coding: utf-8
"""
数据查询和配置模块
用于获取系统中各种实体的ID和账户信息
"""

from api.api_system import SystemUserManageApi
from api.api_finance import FinanceAccountListApi
from api.api_system import SystemWarehouseManageApi
from api.api_sell import SellCustomersManageApi
from api.api_purchase import PurchaseSupplierManageApi
from api.api_system import SystemThirdPartyAccountsManageApi
from api.api_inventory import InventoryAddressManageApi
from api.api_purse import PurseWalletCenterApi
from api.api_help import HelpServiceConfigurationApi
from api.api_platform import PlatformPurchaseManageApi, PlatformInspectionCenterManageApi

# 创建API实例
apis = {
    'user': SystemUserManageApi(),
    'account': FinanceAccountListApi(),
    'warehouse': SystemWarehouseManageApi(),
    'customer': SellCustomersManageApi(),
    'supplier': PurchaseSupplierManageApi(),
    'third_party': SystemThirdPartyAccountsManageApi(),
    'address': InventoryAddressManageApi(),
    'wallet': PurseWalletCenterApi(),
    'help': HelpServiceConfigurationApi(),
    'platform': PlatformPurchaseManageApi(),
    'check_the_machine': PlatformInspectionCenterManageApi()

}


# 获取各种实体ID和账户信息
def get_system_variables():
    """获取系统中所有需要的变量信息"""
    return {
        # 用户和商户id
        'main_user_id': (apis['user'].get_user_id(), '奥特曼用户id'),
        'special_user_id': (apis['user'].get_user_id_two(), '奥特曼库管用户id'),
        'vice_user_id': (apis['user'].get_user_id_vice(), '蝙蝠侠用户id'),
        'idle_user_id': (apis['user'].get_user_id_idle(), '专用账号用户id'),
        'merchant_id': (apis['platform'].get_code(), '商户id'),
        'camera_merchant_id': (apis['platform'].get_camera_code(), '拍机商户id'),

        # 财务id
        'main_account_no': (apis['account'].get_account_no(), '奥特曼财务账户id'),
        'vice_account_no': (apis['account'].get_account_no_vice(), '蝙蝠侠财务账户id'),
        'idle_account_no': (apis['account'].get_account_id_idle(), '财务账户id'),
        'idle_out_account_no': (apis['account'].get_account_id_idle_two(), '财务账户id'),

        # 仓库id
        'main_warehouse_id': (apis['warehouse'].get_id(), '深圳配件仓id'),
        'main_item_warehouse_id': (apis['warehouse'].get_id_two(), '广州物品仓id'),
        'main_in_warehouse_id': (apis['warehouse'].get_id_three(), '默认物品仓id'),
        'main_item_in_warehouse_id': (apis['warehouse'].get_id_four(), '默认配件仓id'),
        'vice_warehouse_id': (apis['warehouse'].get_id_five(), '蝙蝠侠仓库id'),

        # 客户和供应商id
        'main_sale_supplier_id': (apis['customer'].get_id(), '销售客户id'),
        'vice_help_sale_supplier_id': (apis['customer'].get_id_vice(), '蝙蝠侠帮卖销售客户id'),
        'main_supplier_id': (apis['supplier'].get_id(), '供应商id'),

        # 第三方和地址id
        'main_purchase_user_id': (apis['third_party'].get_id(), '采购账号id'),
        'main_user_address_yz_id': (apis['address'].get_yz_id(), '壹准保卖-地址管理-收货地址id'),
        'main_user_address_id': (apis['address'].get_ty_id(), '通用业务-地址管理-收货地址id'),
        'camera_user_address_pj_id': (apis['address'].get_pj_id(), '拍机账号-壹准拍机业务-地址管理-收货地址id'),

        # 钱包id
        'main_wallet_account_no': (apis['wallet'].get_account_no(), '快递易钱包id'),
        'vice_wallet_account_no': (apis['wallet'].get_account_no_vice(), '蝙蝠侠快递易钱包id'),

        # 帮卖id
        'main_help_sell_tenant_id': (apis['help'].get_merchant_code(), '帮卖商家id'),

        # 电话
        'receiving_phone': (apis['platform'].get_phone_main(), '奥特曼电话'),
        'shipping_phone': (apis['platform'].get_phone_vice(), '蝙蝠侠电话'),
        'camera_phone': (apis['platform'].get_phone_camera(), '卢卡斯电话'),

        # 验机中心id
        'check_the_center_id': (apis['check_the_machine'].get_check_the_center_id(), '验机中心id'),
        'check_the_center_name': (apis['check_the_machine'].get_operation_center_name(), '验机中心名称'),
    }

def print_variables():
    """打印所有变量信息"""
    variables = get_system_variables()

    for var_name, (var_value, comment) in variables.items():
        if isinstance(var_value, str):
            print(f'"{var_name}": "{var_value}", # {comment}')
        else:
            print(f'"{var_name}": {var_value}, # {comment}')


if __name__ == '__main__':
    print_variables()
