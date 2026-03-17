"""随机数生成器模块

提供各种随机数据生成函数，用于测试数据生成。
这些函数将被注入到前置条件执行环境中供用户使用。

使用示例:
    context['waybill'] = sf_waybill()
    context['phone'] = random_phone()
    context['imei'] = random_imei()
"""

import random
import uuid


def sf_waybill() -> str:
    """生成 SF 物流单号

    格式: "SF" + 12位随机字母数字组合
    返回: 14位字符串，以 "SF" 开头

    Returns:
        14位 SF 物流单号字符串
    """
    # 使用 UUID4 的十六进制形式（去除连字符）取前12位
    uuid_hex = uuid.uuid4().hex[:12].upper()
    return f"SF{uuid_hex}"


def random_phone() -> str:
    """生成 11 位手机号

    格式: "13" + 9位随机数字
    返回: 11位字符串，以 "13" 开头

    Returns:
        11位手机号字符串
    """
    return "13" + ''.join(random.choices('0123456789', k=9))


def random_imei() -> str:
    """生成 15 位 IMEI

    格式: "I" + 14位随机数字
    返回: 15位字符串，以 "I" 开头

    Returns:
        15位 IMEI 字符串
    """
    return "I" + ''.join(random.choices('0123456789', k=14))


def random_serial() -> str:
    """生成 8 位序列号

    格式: 8位纯数字
    返回: 8位字符串

    Returns:
        8位序列号字符串
    """
    return ''.join(random.choices('0123456789', k=8))


def random_numbers(n: int) -> str:
    """生成指定长度的随机数字字符串

    Args:
        n: 数字位数

    Returns:
        n位纯数字字符串
    """
    return ''.join(random.choices('0123456789', k=n))
