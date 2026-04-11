# coding: utf-8
"""
数据查询和配置模块
用于获取系统中各种实体的ID和账户信息
"""

from api.api_system import K5PFamUMZnUdvWDYKxdNk
from api.api_finance import NQXuyZ5kySQBpsQJxR3vC
from api.api_system import KS9xZ6UDYk9dq6xnv7T0t
from api.api_sell import PaCOjaNKGGuX7m5M6knOA
from api.api_purchase import UCpwX0dlRXRmKVzfDX5dd
from api.api_system import RMgCwZF84pZe4Io1Je8Vu
from api.api_inventory import Ie1Dlx6hKL0xHjTgV7J4p
from api.api_purse import Vssd8T4BpUd8tbwsdelWv
from api.api_help import Ea7Wjr4ctTv69frbEUPZJ
from api.api_platform import VzF4todMPF4UN7aNpYfCs, B63gyanXogW9NpUu1Gr1K

# 创建API实例
apis = {
    'user': K5PFamUMZnUdvWDYKxdNk(),
    'account': NQXuyZ5kySQBpsQJxR3vC(),
    'warehouse': KS9xZ6UDYk9dq6xnv7T0t(),
    'customer': PaCOjaNKGGuX7m5M6knOA(),
    'supplier': UCpwX0dlRXRmKVzfDX5dd(),
    'third_party': RMgCwZF84pZe4Io1Je8Vu(),
    'address': Ie1Dlx6hKL0xHjTgV7J4p(),
    'wallet': Vssd8T4BpUd8tbwsdelWv(),
    'help': Ea7Wjr4ctTv69frbEUPZJ(),
    'platform': VzF4todMPF4UN7aNpYfCs(),
    'check_the_machine': B63gyanXogW9NpUu1Gr1K()

}


# 获取各种实体ID和账户信息
def get_system_variables():
    """获取系统中所有需要的变量信息"""
    return {
        # 用户和商户id
        'Ae1Zt6ZiWt5z': (apis['user'].Ae1Zt6ZiWt5z(), '奥特曼用户id'),
        'YEPWmdrz4R2Y': (apis['user'].YEPWmdrz4R2Y(), '奥特曼库管用户id'),
        'ztstv48nYgYW': (apis['user'].ztstv48nYgYW(), '蝙蝠侠用户id'),
        'aOwdVLwXzO6f': (apis['user'].aOwdVLwXzO6f(), '专用账号用户id'),
        'MmYE3zmy4nRl': (apis['user'].MmYE3zmy4nRl(), '拍机账号用户id'),
        'nB1TOOFzla57': (apis['platform'].nB1TOOFzla57(), '商户id'),
        'HQFhRAOshzqB': (apis['platform'].HQFhRAOshzqB(), '拍机商户id'),

        # 财务id
        'wUybbFZAc1F0': (apis['account'].wUybbFZAc1F0(), '奥特曼财务账户id'),
        'QIaTbZQd4c2R': (apis['account'].QIaTbZQd4c2R(), '蝙蝠侠财务账户id'),
        'NDv9JRmcGNSo': (apis['account'].NDv9JRmcGNSo(), '财务账户id'),
        'CRx8SuT6pM8C': (apis['account'].CRx8SuT6pM8C(), '财务账户id'),

        # 仓库id
        'w6NzYX8tgUAr': (apis['warehouse'].w6NzYX8tgUAr(), '深圳配件仓id'),
        'yNOMoxdkvP0y': (apis['warehouse'].yNOMoxdkvP0y(), '广州物品仓id'),
        'dTTvelGrt6RF': (apis['warehouse'].dTTvelGrt6RF(), '默认物品仓id'),
        'WuzYTkWyJjXJ': (apis['warehouse'].WuzYTkWyJjXJ(), '默认配件仓id'),
        'fSZMiSz97PD8': (apis['warehouse'].fSZMiSz97PD8(), '蝙蝠侠仓库id'),

        # 客户和供应商id
        'Dr0F7PV8ZEXi': (apis['customer'].Dr0F7PV8ZEXi(), '销售客户id'),
        'X2OzrVJcQf2u': (apis['customer'].X2OzrVJcQf2u(), '蝙蝠侠帮卖销售客户id'),
        'WJ1hPxxMWpfI': (apis['supplier'].WJ1hPxxMWpfI(), '供应商id'),

        # 第三方和地址id
        'kZWJsYmRWxEf': (apis['third_party'].kZWJsYmRWxEf(), '采购账号id'),
        'kTPaZWqxyWsq': (apis['address'].kTPaZWqxyWsq(), '壹准保卖-地址管理-收货地址id'),
        'KwGZrW0yw6eZ': (apis['address'].KwGZrW0yw6eZ(), '通用业务-地址管理-收货地址id'),
        'QMZr0EnpAFgz': (apis['address'].QMZr0EnpAFgz(), '拍机账号-壹准拍机业务-地址管理-收货地址id'),

        # 钱包id
        'cCEgx5T9KbpZ': (apis['wallet'].cCEgx5T9KbpZ(), '快递易钱包id'),
        'rBWq7DI98n6x': (apis['wallet'].rBWq7DI98n6x(), '蝙蝠侠快递易钱包id'),

        # 帮卖id
        'NdHOKUMLaooD': (apis['help'].NdHOKUMLaooD(), '帮卖商家id'),

        # 电话
        'OebN1M0GCfbt': (apis['platform'].OebN1M0GCfbt(), '奥特曼电话'),
        'eXKDs5mfSsmy': (apis['platform'].eXKDs5mfSsmy(), '蝙蝠侠电话'),
        'TqsIFsirS5UH': (apis['platform'].TqsIFsirS5UH(), '卢卡斯电话'),

        # 验机中心id
        't25mwHNJH3Is': (apis['check_the_machine'].t25mwHNJH3Is(), '验机中心id'),
        'gMPvjk57y0hb': (apis['check_the_machine'].gMPvjk57y0hb(), '验机中心名称'),
        'UoR79Z3TA8yQ': (apis['check_the_machine'].UoR79Z3TA8yQ(), '拍机验机中心id'),
        'tfLR31KkCRRN': (apis['check_the_machine'].tfLR31KkCRRN(), '拍机验机中心名称'),
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
