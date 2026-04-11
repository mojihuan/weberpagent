# coding: utf-8
import time

from common.base_assert import BaseAssert
from common.base_assertions_field import AssertionsRes


class BaseModuleAssert(BaseAssert):
    """通用断言模块基类"""

    def __init__(self):
        super().__init__()
        self._api_cache = {}

    def _get_cached_api(self, path):
        """获取缓存的API对象path"""
        cache_key = path

        if cache_key not in self._api_cache:
            parts = path.split('.')
            current = self.api

            for part in parts:
                current = getattr(current, part)
            self._api_cache[cache_key] = current
        return self._api_cache[cache_key]

    def _call_module_api(self, module_name, api_methods, headers=None, data='main', **kwargs):
        """
        通用 API 调用方法
        Args:
            module_name: 模块名称
            api_methods: API 方法字典
            headers: 请求头
            method: 调用方法
            **kwargs: 其他参数
        """
        time.sleep(0.5)

        # 第一次调用：强制刷新数据
        main_method = api_methods.get('main')
        if main_method:
            try:
                # 提取可能传递给 API 的特殊参数（如 i, j 等）
                api_params = {'headers': self._process_headers_for_api(headers)}
                special_params = ['i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
                for key, value in kwargs.items():
                    if key in special_params:
                        api_params[key] = value

                main_method(**api_params)
                time.sleep(1)  # 等待数据刷新
            except Exception as e:
                print(f"刷新数据时发生错误：{str(e)}")

        # 第二次调用：获取最新数据进行断言
        return self._assert_api_response(
            module_name,
            api_methods,
            AssertionsRes().assertive_field if hasattr(AssertionsRes(),
                                                       'assertive_field') else AssertionsRes.assertive_field,
            headers,
            data,
            **kwargs
        )

    def _process_headers_for_api(self, headers):
        """
        处理 headers 参数，将字符串标识转换为实际的 header 字典
        Args:
            headers: 请求头标识或字典
        Returns:
            处理后的 header 字典
        """
        if headers is None:
            # 如果没有传入 headers，使用默认的 main header
            from common.import_api import ImportApi
            api = ImportApi()
            # 获取第一个可用的 API 对象的 headers
            for attr_name in dir(api):
                attr = getattr(api, attr_name)
                if hasattr(attr, 'headers') and isinstance(attr.headers, dict):
                    return attr.headers.get('main', {})
            return {}

        # 如果 headers 是字符串标识，需要转换
        if isinstance(headers, str):
            header_mapping = {
                'main': 'main',
                'idle': 'idle',
                'vice': 'vice',
                'special': 'special',
                'platform': 'platform',
                'super': 'super',
                'camera': 'camera',
            }
            # 从任意 API 对象中获取实际的 header 字典
            from common.import_api import ImportApi
            api_instance = ImportApi()
            for attr_name in dir(api_instance):
                attr = getattr(api_instance, attr_name)
                if hasattr(attr, 'headers') and isinstance(attr.headers, dict):
                    header_key = header_mapping.get(headers, headers)
                    return attr.headers.get(header_key, {})
            return {}

        # 如果已经是字典，直接返回
        return headers


class PcAssert(BaseModuleAssert):
    """公共断言"""

    def H13p6B(self, data='main', **kwargs):
        """配件管理|配件库存|库存列表"""
        api = self._get_cached_api('CtRBRcFNn2LnUPfJF5Yhu')
        methods = {
            'main': api.H2lnntBLD8A3,  # 库存列表
            'a': api.OS0dslt8oIW6,  # 物品详情
            'b': api.ryjErEJrLvhi,  # 物品详情 采购信息
            'c': api.X2VJTiwTrgcC,  # 物品详情 销售信息
            'd': api.Wo6IwyvOfpNM,  # 物品详情 操作日志
        }
        return self._call_module_api('CtRBRcFNn2LnUPfJF5Yhu', methods, data=data, **kwargs)

    def nbxNKL(self, data='main', **kwargs):
        """配件管理|配件销售|销售列表"""
        api = self._get_cached_api('IW1UwaP9R0hojKPOJQSH4')
        methods = {
            'main': api.xTgxXhKIdF5f,  # 销售列表
            'a': api.iVaMuxcu6FrP  # 销售详情
        }
        return self._call_module_api('IW1UwaP9R0hojKPOJQSH4', methods, data=data, **kwargs)

    def HQ55MW(self, data='main', **kwargs):
        """配件管理|配件采购|采购列表"""
        api = self._get_cached_api('OiUAWoPURtS5QdkSFauge')
        methods = {
            'main': api.PA6i54jUEr6x,  # 采购列表
            'a': api.NOWFR2ysZMiz  # 采购详情
        }
        return self._call_module_api('OiUAWoPURtS5QdkSFauge', methods, data=data, **kwargs)

    def uzsnM0(self, data='main', **kwargs):
        """配件管理|配件采购|采购售后列表"""
        api = self._get_cached_api('KjMTctZhHuOMIT0xd1AP3')
        methods = {
            'main': api.G5wHf1sqe1zu,  # 采购售后列表
            'a': api.osRwiAV9t4QT  # 采购售后详情
        }
        return self._call_module_api('KjMTctZhHuOMIT0xd1AP3', methods, data=data, **kwargs)

    def rmoeta(self, data='main', **kwargs):
        """配件管理|配件销售|销售售后列表"""
        api = self._get_cached_api('Nd81xbVVnxevE1Oy8yXcy')
        methods = {
            'main': api.VGeFY2YzIHzc,  # 销售售后列表
            'a': api.FOLBxm2fXcoW  # 销售售后详情
        }
        return self._call_module_api('Nd81xbVVnxevE1Oy8yXcy', methods, data=data, **kwargs)

    def Dp7Ih9(self, data='main', **kwargs):
        """配件管理|入库管理|分拣列表"""
        api = self._get_cached_api('LnfQBDqBvleaE2O0412qk')
        methods = {
            'main': api.IB3TfKONJp2x,  # 分拣列表
            'a': api.PaJDXqH7P5A0  # 包裹视频
        }
        return self._call_module_api('LnfQBDqBvleaE2O0412qk', methods, data=data, **kwargs)

    def znEgfM(self, data='main', **kwargs):
        """配件管理|入库管理|新到货入库"""
        api = self._get_cached_api('KFkHdZyASZRhMrmNKfHiQ')
        methods = {
            'main': api.aYrCZLAaSxA7,  # 新到货入库列表
        }
        return self._call_module_api('KFkHdZyASZRhMrmNKfHiQ', methods, data=data, **kwargs)

    def we4jOX(self, data='main', **kwargs):
        """配件管理|配件库存|库存调拨"""
        api = self._get_cached_api('DgyYP8ygDMIIeEEXHuLbW')
        methods = {
            'main': api.QGOxnhn1YW7x,  # 调拨列表
            'a': api.ZT5PSTjrth3p,  # 调拨详情
        }
        return self._call_module_api('DgyYP8ygDMIIeEEXHuLbW', methods, data=data, **kwargs)

    def yTiuCZ(self, data='main', **kwargs):
        """配件管理|移交接收管理|移交记录"""
        api = self._get_cached_api('BFOjFKv6ZxII7V5LzQcr4')
        methods = {
            'main': api.pvspNI89ooNR,  # 移交记录列表
            'a': api.ABCpFCzCuSNt,  # 移交记录详情
        }
        return self._call_module_api('BFOjFKv6ZxII7V5LzQcr4', methods, data=data, **kwargs)

    def xl40Pj(self, data='main', **kwargs):
        """配件管理|移交接收管理|移交物品"""
        api = self._get_cached_api('Yitlwlf3LfoaHccm1J6mF')
        methods = {
            'main': api.pk3yPDL8mWlJ,  # 移交物品列表
        }
        return self._call_module_api('Yitlwlf3LfoaHccm1J6mF', methods, data=data, **kwargs)

    def wb3p9S(self, data='main', **kwargs):
        """配件管理|移交接收管理|接收物品"""
        api = self._get_cached_api('AMaXd2PkDsrT5cj1SArOe')
        methods = {
            'main': api.s3Ycs7Oyt5DL,  # 移交单接收列表
            'a': api.mfaVZuvBLcri,  # 物品接收列表
            'b': api.NPp0AJ9kG7cr,  # 移交单接收详情
        }
        return self._call_module_api('AMaXd2PkDsrT5cj1SArOe', methods, data=data, **kwargs)

    def A5MvUv(self, data='main', **kwargs):
        """配件管理|配件统计|赠送明细"""
        api = self._get_cached_api('Gwz4FEbJD7duHFXM43CTo')
        methods = {
            'main': api.t3GVi2bbFIzs,  # 赠送明细列表
        }
        return self._call_module_api('Gwz4FEbJD7duHFXM43CTo', methods, data=data, **kwargs)

    def ZFsvTM(self, data='main', **kwargs):
        """配件管理|入库管理|旧配件入库"""
        api = self._get_cached_api('RjB1dOTFUrlGReUmemgQr')
        methods = {
            'main': api.U6Xw8Ui8Ti9x,  # 旧配件入库列表
            'a': api.eGKYE973IfbO  # 旧配件入库详情
        }
        return self._call_module_api('RjB1dOTFUrlGReUmemgQr', methods, data=data, **kwargs)

    def U4VyVc(self, data='main', **kwargs):
        """配件管理|配件统计|销售明细"""
        api = self._get_cached_api('Y9pPmEIVBiqj7NBb64Jy4')
        methods = {
            'main': api.acB0a2Y5bfRO,  # 销售明细列表
        }
        return self._call_module_api('Y9pPmEIVBiqj7NBb64Jy4', methods, data=data, **kwargs)

    def dPrUg2(self, data='main', **kwargs):
        """配件管理|配件维护"""
        api = self._get_cached_api('Ln0faZ5CGpaYmkrcCVg4X')
        methods = {
            'main': api.c69L92JCEAfA,  # 配件维护列表
        }
        return self._call_module_api('Ln0faZ5CGpaYmkrcCVg4X', methods, data=data, **kwargs)

    def zXhXVF(self, data='main', **kwargs):
        """财务管理|资金账户|账户列表"""
        api = self._get_cached_api('NQXuyZ5kySQBpsQJxR3vC')
        methods = {
            'main': api.xsn47jtSUiZ8,  # 账户列表
            'a': api.dBMS1qAcYEzH  # 账户统计
        }
        return self._call_module_api('NQXuyZ5kySQBpsQJxR3vC', methods, data=data, **kwargs)

    def wYx7PP(self, data='main', **kwargs):
        """财务管理|资金账户|交易明细"""
        api = self._get_cached_api('KkU8jJZhRGbWRP2ZjHKyg')
        methods = {
            'main': api.ChMjJGNgwb2P,  # 交易明细列表
        }
        return self._call_module_api('KkU8jJZhRGbWRP2ZjHKyg', methods, data=data, **kwargs)

    def GaYl3w(self, data='main', **kwargs):
        """财务管理|业务记账|付款结算单"""
        api = self._get_cached_api('TLt2NsvdRPrlyXBduaMZ4')
        methods = {
            'main': api.bIUbOOYwwkaD,  # 付款结算单列表
        }
        return self._call_module_api('TLt2NsvdRPrlyXBduaMZ4', methods, data=data, **kwargs)

    def CsnLYF(self, data='main', **kwargs):
        """财务管理|业务记账|收款结算单"""
        api = self._get_cached_api('H9Xjv30kk5a6ul7sNOTeg')
        methods = {
            'main': api.dRsMaRuoo4vp,  # 收款结算单列表
        }
        return self._call_module_api('H9Xjv30kk5a6ul7sNOTeg', methods, data=data, **kwargs)

    def rfhFfE(self, data='main', **kwargs):
        """财务管理|业务记账|账单审核
        i：1应付 2应收
        """
        api = self._get_cached_api('VFy40VMBZGf8pQEkVFRor')
        methods = {
            'main': api.zS2mEs09Al0d,  # 应付账单列表
        }
        return self._call_module_api('VFy40VMBZGf8pQEkVFRor', methods, data=data, **kwargs)

    def zliHLE(self, data='main', **kwargs):
        """财务管理|成本收入调整"""
        api = self._get_cached_api('CxWYtVbPEgBMsAbMB1sNz')
        methods = {
            'main': api.R7ocRWn8F0VR,  # 单据列表
            'a': api.tJdw1dzjQNC9,  # 单据列表详情
            'b': api.oIoZoEJlkHmY  # 物品列表
        }
        return self._call_module_api('CxWYtVbPEgBMsAbMB1sNz', methods, data=data, **kwargs)

    def JedUWt(self, data='main', **kwargs):
        """财务管理|业务记账|日常支出"""
        api = self._get_cached_api('OApuzLHbCS388IVB9m2c9')
        methods = {
            'main': api.StQZwBU9k4GX,  # 日常支出列表
            'a': api.z91RXolcKAt2  # 统计金额
        }
        return self._call_module_api('OApuzLHbCS388IVB9m2c9', methods, data=data, **kwargs)

    def nRHG7d(self, data='main', **kwargs):
        """财务管理|业务记账|日常收入"""
        api = self._get_cached_api('LgTsekFh4kT1Jm0Xt5UhY')
        methods = {
            'main': api.xZn2CBfoX85Y,  # 日常收入列表
            'a': api.BXqoSGwoTjgD  # 统计金额
        }
        return self._call_module_api('LgTsekFh4kT1Jm0Xt5UhY', methods, data=data, **kwargs)

    def gtB02x(self, data='main', **kwargs):
        """财务管理|业务记账|往来应收"""
        api = self._get_cached_api('A9mwkPeNc1x7YnLCF9jUk')
        methods = {
            'main': api.onzqxhWPmd6i,  # 对账详情
            'a': api.oIkWBNgsRuRQ  # 对账详情 单据详情
        }
        return self._call_module_api('A9mwkPeNc1x7YnLCF9jUk', methods, data=data, **kwargs)

    def QGFzSF(self, data='main', **kwargs):
        """财务管理|业务记账|往来应付"""
        api = self._get_cached_api('MOyeqlzcgLqhqdWBrkyYg')
        methods = {
            'main': api.VPtqPg96V4bb,  # 对账详情
            'a': api.Anlk8HQ08DoN  # 对账详情-单据详情
        }
        return self._call_module_api('MOyeqlzcgLqhqdWBrkyYg', methods, data=data, **kwargs)

    def Xji7fR(self, data='main', **kwargs):
        """财务管理|业务记账|预收预付"""
        api = self._get_cached_api('ZDGSH9p2RLv5QuD68Ivi9')
        methods = {
            'main': api.poj74krsYufe,  # 预付、预收列表
        }
        return self._call_module_api('ZDGSH9p2RLv5QuD68Ivi9', methods, data=data, **kwargs)

    def dKWl3w(self, data='main', **kwargs):
        """运营中心|订单管理
        i：订单状态 1待发货 2待取件 3待收货 4已收货 5已完成 6已取消 7已退货
        """
        api = self._get_cached_api('VzruD2bzEUPV1JJY9d6vF')
        methods = {
            'main': api.G1ZATPtlzjWF,  # 订单列表
        }
        return self._call_module_api('VzruD2bzEUPV1JJY9d6vF', methods, data=data, **kwargs)

    def scDt2J(self, data='main', **kwargs):
        """运营中心|待报价物品"""
        api = self._get_cached_api('RjVgo4LDzg4voonKUBXr1')
        methods = {
            'main': api.vSNmU0ZwGwPu,  # 列表
        }
        return self._call_module_api('RjVgo4LDzg4voonKUBXr1', methods, data=data, **kwargs)

    def hnqSw4(self, data='main', **kwargs):
        """运营中心|退货管理
        i：订单状态 1待退货 2待取货 3退货已出库 4已退货 5已取消
        """
        api = self._get_cached_api('M4Xsay25almyg0RzXz4ui')
        methods = {
            'main': api.WCB6NcIMpsMe,  # 商户明细列表
            'a': api.ua4JlujLXZDP,  # 物品明细列表
            'b': api.VnssCpqfEIlk  # 批次明细列表
        }
        return self._call_module_api('M4Xsay25almyg0RzXz4ui', methods, data=data, **kwargs)

    def BsGxx9(self, data='main', **kwargs):
        """运营中心|质检管理
        [d]i类型 1未上传 2已上传
        """
        api = self._get_cached_api('FYXRA4IxF49PvhUCLpp5Z')
        methods = {
            'main': api.KhNjoVcM4iuf,  # 待领取物品列表
            'a': api.OHXGClp3BoJm,  # 质检中物品列表
            'b': api.eDr2hpq6xEBa,  # 重验申请列表
            'c': api.oSzj9Md6vHyl,  # 已质检物品列表
            'd': api.YkybIUUCs2Dh  # 商品图拍摄列表
        }
        return self._call_module_api('FYXRA4IxF49PvhUCLpp5Z', methods, data=data, **kwargs)

    def uZ6Nyg(self, data='main', **kwargs):
        """运营中心|销售发货管理"""
        api = self._get_cached_api('KmxOWBECeMnMqtP1qACyx')
        methods = {
            'main': api.N3GKYzC6P5TZ,  # 待发货 按物品
            'a': api.Oqr9od3TrupA,  # 待发货 按商户
            'b': api.fNSLGMFC7atc,  # 待收货 按物品
            'c': api.clirkK4CTUj0,  # 待收货 按包裹
            'd': api.uByZKczL88yQ,  # 已收货 按包裹
            'e': api.ntnTnNcZjnPi,  # 已收货 按物品
        }
        return self._call_module_api('KmxOWBECeMnMqtP1qACyx', methods, data=data, **kwargs)

    def jOTfI6(self, data='main', **kwargs):
        """帮卖管理|帮卖上架列表"""
        api = self._get_cached_api('PurkQXBjQXG3tz8hUb1SF')
        methods = {
            'main': api.l6TOXA4JkEjO,  # 订单列表
            'a': api.WCyqKh1Jrosc,  # 批次列表
            'b': api.gavz8010zhrA  # 发起帮卖列表
        }
        return self._call_module_api('PurkQXBjQXG3tz8hUb1SF', methods, data=data, **kwargs)

    def q1h1xu(self, data='main', **kwargs):
        """帮卖管理|帮卖来货列表"""
        api = self._get_cached_api('Jc9Odo2T6JqvbWDRSsDXy')
        methods = {
            'main': api.vw76zdVHgk8Q,  # 订单列表
            'a': api.aOGxkzDL4EwQ  # 批次列表
        }
        return self._call_module_api('Jc9Odo2T6JqvbWDRSsDXy', methods, data=data, **kwargs)

    def v3jQpR(self, data='main', **kwargs):
        """帮卖管理|帮卖业务配置"""
        api = self._get_cached_api('Ea7Wjr4ctTv69frbEUPZJ')
        methods = {
            'main': api.OUYQFhYf3krT,  # 帮卖业务配置列表
        }
        return self._call_module_api('Ea7Wjr4ctTv69frbEUPZJ', methods, data=data, **kwargs)

    def ZJX008(self, data='main', **kwargs):
        """库存管理|出库管理|地址管理"""
        api = self._get_cached_api('Ie1Dlx6hKL0xHjTgV7J4p')
        methods = {
            'main': api.X41neJLZTAeU,  # 列表
        }
        return self._call_module_api('Ie1Dlx6hKL0xHjTgV7J4p', methods, data=data, **kwargs)

    def tTzybz(self, data='main', **kwargs):
        """库存管理|入库管理|物流列表"""
        api = self._get_cached_api('D2grXOWzOv0I5f5rFGf6A')
        methods = {
            'main': api.bI2yFNa61M9Q,  # 物流列表
            'a': api.t9tSA8AX8kJj,  # 物流列表详情
        }
        return self._call_module_api('D2grXOWzOv0I5f5rFGf6A', methods, data=data, **kwargs)

    def ABgSE1(self, data='main', **kwargs):
        """库存管理|出库管理|仅出库订单列表"""
        api = self._get_cached_api('QYSFzOWmZ2zYnize8ppKN')
        methods = {
            'main': api.ORF5PGdo8vkp,  # 仅出库列表
            'a': api.jkCbj4E7lnmd,  # 退回单列表
            'b': api.FlBn7VEIrt0P  # 仅出库订单详情
        }
        return self._call_module_api('QYSFzOWmZ2zYnize8ppKN', methods, data=data, **kwargs)

    def vSap98(self, data='main', **kwargs):
        """库存管理|移交接收管理|接收物品"""
        api = self._get_cached_api('LWT9dymUmXdvWqLk1qEeA')
        methods = {
            'main': api.wX85yA1a0yOb,  # 物品接收列表
            'a': api.XbUs4Xjcx1eU,  # 移交单接收列表
            'b': api.fPKMGLwa2uJG  # 移交单接收详情
        }
        return self._call_module_api('LWT9dymUmXdvWqLk1qEeA', methods, data=data, **kwargs)

    def qOAsRC(self, data='main', **kwargs):
        """库存管理|库存盘点"""
        api = self._get_cached_api('Ux7lF2b6qktEytPTzyaQW')
        methods = {
            'main': api.dGxdNvDrm0gW,  # 库存盘点列表
        }
        return self._call_module_api('Ux7lF2b6qktEytPTzyaQW', methods, data=data, **kwargs)

    def c0oQwY(self, data='main', **kwargs):
        """库存管理|库存调拨"""
        api = self._get_cached_api('XHyhIffDlKvRSMGo6DlG2')
        methods = {
            'main': api.scIEFidBwtZs,  # 库存调拨列表
        }
        return self._call_module_api('XHyhIffDlKvRSMGo6DlG2', methods, data=data, **kwargs)

    def XtWLz8(self, data='main', **kwargs):
        """库存管理|库存列表"""
        api = self._get_cached_api('UYV6mZaVwDk4HHhyuWRRp')
        methods = {
            'main': api.I8TzeuUVWOYr,  # 库存列表
            'a': api.DiPuR7wiWR9p,  # 物品详情 销售信息
            'b': api.operation_log,  # 物品详情 操作日志
            'c': api.EbJ4mgpvdxWd,  # 库存列表 总成本详情 统计
            'd': api.QPjBR7LSwxnq,  # 库存列表 总成本详情
            'e': api.JGJO4DeQYuKZ,  # 库存列表 总收入详情 统计
            'f': api.MDmyPNWh4b2g  # 库存列表 总收入详情
        }
        return self._call_module_api('UYV6mZaVwDk4HHhyuWRRp', methods, data=data, **kwargs)

    def jbliLf(self, data='main', **kwargs):
        """库存管理|移交接收管理|移交记录"""
        api = self._get_cached_api('PzpwGb0gERxw3s5t4WiGd')
        methods = {
            'main': api.YsmsUS99q8Mf,  # 移交记录列表
            'a': api.O2cpz6NJM1Ql,  # 移交记录详情
        }
        return self._call_module_api('PzpwGb0gERxw3s5t4WiGd', methods, data=data, **kwargs)

    def MGvDr5(self, data='main', **kwargs):
        """首页|个人中心"""
        api = self._get_cached_api('INBsa7uXWvRflmozMyZ7Y')
        methods = {
            'main': api.rI0La6FxSuFu,  # 个人中心信息
        }
        return self._call_module_api('INBsa7uXWvRflmozMyZ7Y', methods, data=data, **kwargs)

    def dbii4b(self, data='main', **kwargs):
        """消息管理|消息发布列表"""
        api = self._get_cached_api('KxO3PKRgVuNDVjQUSHVcl')
        methods = {
            'main': api.qTd9V34NC3MZ,  # 消息发布列表
        }
        return self._call_module_api('KxO3PKRgVuNDVjQUSHVcl', methods, data=data, **kwargs)

    def czuDPA(self, data='main', **kwargs):
        """平台管理|订单管理|订单审核"""
        api = self._get_cached_api('V3LpfoN0H354ztNVHPWtf')
        methods = {
            'main': api.TdbQGLoDJMFo,  # 订单审核列表
        }
        return self._call_module_api('V3LpfoN0H354ztNVHPWtf', methods, data=data, **kwargs)

    def EtRRIT(self, data='main', **kwargs):
        """平台管理|卖场管理|暗拍卖场列表
        i；1-已上架；2-待上架；3-已下架
        """
        api = self._get_cached_api('EEdalTouEaLL3VEx3wMnz')
        methods = {
            'main': api.pzCWj3Ksrd4P,  # 暗拍卖场列表
            'a': api.i2hsWJeCQxKo,  # 查看场次详情 场次列表
            'b': api.q5mIVNB1zQPk,  # 查看场次详情 商品列表
        }
        return self._call_module_api('EEdalTouEaLL3VEx3wMnz', methods, data=data, **kwargs)

    def rkNFDq(self, data='main', **kwargs):
        """平台管理|卖场管理|直拍卖场列表"""
        api = self._get_cached_api('BaxRsHzRpoNsTb8fnSa9e')
        methods = {
            'main': api.gXHSWafumwCe,  # 直拍卖场列表
            'a': api.oTwifIq7ER6o,  # 查看场次详情 场次列表
            'b': api.sh3cTsLUbzwu,  # 查看场次详情 商品列表
        }
        return self._call_module_api('BaxRsHzRpoNsTb8fnSa9e', methods, data=data, **kwargs)

    def vgett6(self, data='main', **kwargs):
        """平台管理|虚拟库存|虚拟库存列表
        i：物品状态 1质检中 2待销售 3销售中 4已销售 5待平台确认 6报价确认 7质检完成 8退货中 9退货已出库 10已退货
        """
        api = self._get_cached_api('VvIs5cfbQJsDekJKZZOr1')
        methods = {
            'main': api.ppkzpNKKe2Vc,  # 虚拟库存列表
        }
        return self._call_module_api('VvIs5cfbQJsDekJKZZOr1', methods, data=data, **kwargs)

    def ieulBh(self, data='main', **kwargs):
        """平台管理|虚拟库存|上拍商品管理
         i：类型 1可上拍商品 2已上拍商品 0待定价物品
        """
        api = self._get_cached_api('HnlUtAPz07JtZRXny3Ogs')
        methods = {
            'main': api.FgMfvbUdU4qZ,  # 上拍商品管理列表
        }
        return self._call_module_api('HnlUtAPz07JtZRXny3Ogs', methods, data=data, **kwargs)

    def eTpj8W(self, data='main', **kwargs):
        """平台管理|运营中心|待指定物品"""
        api = self._get_cached_api('YVqIQus8roZWysBseaMP0')
        methods = {
            'main': api.DSpcSKcA7pw5,  # 待指定物品列表
        }
        return self._call_module_api('YVqIQus8roZWysBseaMP0', methods, data=data, **kwargs)

    def LXtfeb(self, data='main', **kwargs):
        """商品采购|采购管理|采购订单列表"""
        api = self._get_cached_api('Z6BEKs3GvdIWf6a1Dj2uP')
        methods = {
            'main': api.QYMK9r8Zx1lb,  # 采购订单列表
            'b': api.ua4pZjFEITx3,  # 采购单详情
        }
        return self._call_module_api('Z6BEKs3GvdIWf6a1Dj2uP', methods, data=data, **kwargs)

    def wEEUyb(self, data='main', **kwargs):
        """运营中心|bot订单管理"""
        api = self._get_cached_api('KsJkf77pdK7sRJY6s9lfO')
        methods = {
            'main': api.FTdfLz90lzeR,  # bot订单管理列表
        }
        return self._call_module_api('KsJkf77pdK7sRJY6s9lfO', methods, data=data, **kwargs)

    def HMLcuW(self, data='main', **kwargs):
        """商品采购|采购任务"""
        api = self._get_cached_api('ZzpxfXbO9fEmLG1gxxzjP')
        methods = {
            'main': api.we5YUPreA4h0,  # 采购任务列表
            'a': api.u0vCCOCkGc1P,  # 采购退货信息
        }
        return self._call_module_api('ZzpxfXbO9fEmLG1gxxzjP', methods, data=data, **kwargs)

    def gsWmaV(self, data='main', **kwargs):
        """商品采购|供应商管理"""
        api = self._get_cached_api('UCpwX0dlRXRmKVzfDX5dd')
        methods = {
            'main': api.q9RXyfc2X1UG,  # 供应商管理列表
        }
        return self._call_module_api('UCpwX0dlRXRmKVzfDX5dd', methods, data=data, **kwargs)

    def BtoGb1(self, data='main', **kwargs):
        """商品采购|采购售后管理|采购售后列表
        i: 售后类型 1采购售后完成 2采购售后中
        j: 售后状态 1采购退货退款 2采购拒退 3采购换货 5采购售后中 7采购退差价
        """
        api = self._get_cached_api('Jz32tuIMNM7geguh5D8TF')
        methods = {
            'main': api.a3xoH8PZvyPQ,  # 采购售后列表
            'a': api.WXQJQaZicxQh  # 采购售后详情
        }
        return self._call_module_api('Jz32tuIMNM7geguh5D8TF', methods, data=data, **kwargs)

    def ttqNVt(self, data='main', **kwargs):
        """商品采购|采购管理|采购工单"""
        api = self._get_cached_api('WmKG9OkI9OlJlOENUzgNu')
        methods = {
            'main': api.b1R30NI8UzKR,  # 采购工单列表
            'a': api.O4zibjbjN1p4,  # 报工明细详情
        }
        return self._call_module_api('WmKG9OkI9OlJlOENUzgNu', methods, data=data, **kwargs)

    def p1kRiO(self, data='main', **kwargs):
        """商品采购|采购管理|未发货订单列表"""
        api = self._get_cached_api('Y6hDdvp1tY9uk0H51cn91')
        methods = {
            'main': api.B2HBJYTnnYyI,  # 未发货订单列表
        }
        return self._call_module_api('Y6hDdvp1tY9uk0H51cn91', methods, data=data, **kwargs)

    def uhvTi6(self, data='main', **kwargs):
        """商品采购|采购管理|到货通知单列表"""
        api = self._get_cached_api('THtT7YW545kAG73W2gHDj')
        methods = {
            'main': api.Yf0yiomYxwUn,  # 到货通知单列表
        }
        return self._call_module_api('THtT7YW545kAG73W2gHDj', methods, data=data, **kwargs)

    def QPF5WW(self, data='main', **kwargs):
        """商品采购|采购管理|待售后列表"""
        api = self._get_cached_api('purchase_post_sale_list')
        methods = {
            'main': api.post_sale_list,  # 待售后列表
        }
        return self._call_module_api('purchase_post_sale_list', methods, data=data, **kwargs)

    def k60zWG(self, data='main', **kwargs):
        """商品采购|采购售后管理|待接收物品"""
        api = self._get_cached_api('Rwpqef340gYUd4Hgkbq8l')
        methods = {
            'main': api.JsXBVOMtGANq,  # 待接收物品
        }
        return self._call_module_api('Rwpqef340gYUd4Hgkbq8l', methods, data=data, **kwargs)

    def dHWcCR(self, data='main', **kwargs):
        """钱包管理|钱包订单列表"""
        api = self._get_cached_api('R8iWM0wvi9l16aL5WVUbW')
        methods = {
            'main': api.oJ5lEbrOf6ug,  # 钱包订单列表 待付款
            'a': api.oS6cf6cv3m8d  # 钱包订单列表 确认到款中
        }
        return self._call_module_api('R8iWM0wvi9l16aL5WVUbW', methods, data=data, **kwargs)

    def RWfXxd(self, data='main', **kwargs):
        """质检管理|质检记录列表"""
        api = self._get_cached_api('QyKIiWECv2ppl2UxZhwh3')
        methods = {
            'main': api.vAUM2VniBdJP,  # 质检记录列表
        }
        return self._call_module_api('QyKIiWECv2ppl2UxZhwh3', methods, data=data, **kwargs)

    def qjDA2x(self, data='main', **kwargs):
        """质检管理|质检内容模版"""
        api = self._get_cached_api('TzjKXVa7hC8j6pmsPJQvk')
        methods = {
            'main': api.WY9tdqjthqMp,  # 质检内容模版
        }
        return self._call_module_api('TzjKXVa7hC8j6pmsPJQvk', methods, data=data, **kwargs)

    def J9mkzk(self, data='main', **kwargs):
        """质检管理|先质检后入库"""
        api = self._get_cached_api('LNkpjm7bSdFieVvrwYNga')
        methods = {
            'main': api.rvPD6y5UvbdO,  # 非库内物品列表
            'a': api.i5eQu4jjL9ji  # 非库内质检列表
        }
        return self._call_module_api('LNkpjm7bSdFieVvrwYNga', methods, data=data, **kwargs)

    def oCiIiV(self, data='main', **kwargs):
        """配件管理|入库管理|待接收物品"""
        api = self._get_cached_api('BF3x3lYIzbEHMnrvr80JO')
        methods = {
            'main': api.iigq4MszOhe3,  # 待接收物品列表
        }
        return self._call_module_api('BF3x3lYIzbEHMnrvr80JO', methods, data=data, **kwargs)

    def zyw2kH(self, data='main', **kwargs):
        """维修管理|维修审核列表"""
        api = self._get_cached_api('ZdhlTgRrRPGEMOegDrOfk')
        methods = {
            'main': api.dUaU2azQ6FGY,  # 维修审核列表
        }
        return self._call_module_api('ZdhlTgRrRPGEMOegDrOfk', methods, data=data, **kwargs)

    def aP7LrV(self, data='main', **kwargs):
        """维修管理|已维修物品"""
        api = self._get_cached_api('ZAMtQ4KJqvZUBTAc0PR9C')
        methods = {
            'main': api.EfbrT89zLBmF,  # 维修物品列表
        }
        return self._call_module_api('ZAMtQ4KJqvZUBTAc0PR9C', methods, data=data, **kwargs)

    def DkaFca(self, data='main', **kwargs):
        """维修管理|维修项目列表"""
        api = self._get_cached_api('Gv7PVAqUJKoyfROzOacmx')
        methods = {
            'main': api.bltCvd8b8uHx,  # 维修项目列表
            'a': api.UsdOQX8s4QX3  # 机型配置列表
        }
        return self._call_module_api('Gv7PVAqUJKoyfROzOacmx', methods, data=data, **kwargs)

    def tqIszF(self, data='main', **kwargs):
        """已维修管理|拆件管理"""
        api = self._get_cached_api('PjQrObCdCglLnCtpMNnBl')
        methods = {
            'main': api.aEYHWNFkQu3e,  # 拆件管理列表 按单据
        }
        return self._call_module_api('PjQrObCdCglLnCtpMNnBl', methods, data=data, **kwargs)

    def rv5p3j(self, data='main', **kwargs):
        """商品销售|销售售后管理|销售售后列表"""
        api = self._get_cached_api('Kw5nIo3WQBrH2BPScRj1B')
        methods = {
            'main': api.CfIRP7WqVPD0,  # 销售售后完成
            'a': api.TB2VQJLBUDje  # 销售售后中
        }
        return self._call_module_api('Kw5nIo3WQBrH2BPScRj1B', methods, data=data, **kwargs)

    def FlzJ63(self, data='main', **kwargs):
        """商品销售|销售管理|销售中物品列表"""
        api = self._get_cached_api('Ez77PXDybIrSTaH32RHsz')
        methods = {
            'main': api.TyFTRRkgcx28,  # 销售中物品列表
        }
        return self._call_module_api('Ez77PXDybIrSTaH32RHsz', methods, data=data, **kwargs)

    def bfCKxO(self, data='main', **kwargs):
        """商品销售|销售管理|已销售物品列表"""
        api = self._get_cached_api('JU8QYbNi3BDlSn2XaNZKe')
        methods = {
            'main': api.L6IQgdpG4iaP,  # 已销售物品列表
        }
        return self._call_module_api('JU8QYbNi3BDlSn2XaNZKe', methods, data=data, **kwargs)

    def IgXZcq(self, data='main', **kwargs):
        """商品销售|销售管理|已销售订单列表"""
        api = self._get_cached_api('OY2fdbdieaa3seD31U6ZQ')
        methods = {
            'main': api.B37xGAx8rLVJ,  # 已销售订单列表
        }
        return self._call_module_api('OY2fdbdieaa3seD31U6ZQ', methods, data=data, **kwargs)

    def x9ZGyS(self, data='main', **kwargs):
        """商品销售|销售管理|销售中订单列表 """
        api = self._get_cached_api('PvQWvJ1ETZicFTZpXHiQa')
        methods = {
            'main': api.lZHWz7XAePfb,  # 销售中订单列表
        }
        return self._call_module_api('PvQWvJ1ETZicFTZpXHiQa', methods, data=data, **kwargs)

    def WlmTfF(self, data='main', **kwargs):
        """商品销售|销售管理|待接收物品"""
        api = self._get_cached_api('Mb5NtymgNZq58BhIE7Umz')
        methods = {
            'main': api.z8Q8CdTAeeYa,  # 待接收物品
        }
        return self._call_module_api('Mb5NtymgNZq58BhIE7Umz', methods, data=data, **kwargs)

    def AOPQEJ(self, data='main', **kwargs):
        """商品销售|销售管理|待销售物品"""
        api = self._get_cached_api('XTk41pUDr28xCf1YL17uR')
        methods = {
            'main': api.CSDYFXdhL7n5,  # 待销售物品
        }
        return self._call_module_api('XTk41pUDr28xCf1YL17uR', methods, data=data, **kwargs)

    def dkiPbY(self, data='main', **kwargs):
        """商品销售|销售数据统计"""
        api = self._get_cached_api('RCRdrY38amwbJyUzKuJcM')
        methods = {
            'main': api.oatZoHAFV0w1,  # 销售数据统计
        }
        res = self._call_module_api('RCRdrY38amwbJyUzKuJcM', methods, data=data, **kwargs)
        return res

    def oYAm4N(self, data='main', **kwargs):
        """送修管理|已送修物品"""
        api = self._get_cached_api('QM4hD6LNhqKxZAitqFFJl')
        methods = {
            'main': api.bkXQFPd3Pz5I,  # 已送修物品列表
        }
        return self._call_module_api('QM4hD6LNhqKxZAitqFFJl', methods, data=data, **kwargs)

    def WqPUcl(self, data='main', **kwargs):
        """送修管理|送修单列表"""
        api = self._get_cached_api('MMuymWgzUDbCSdlZPeMMY')
        methods = {
            'main': api.FaEsPLDSYo0I,  # 送修单列表
        }
        return self._call_module_api('MMuymWgzUDbCSdlZPeMMY', methods, data=data, **kwargs)

    def T241Se(self, data='main', **kwargs):
        """系统管理|导出列表"""
        api = self._get_cached_api('Q8OvSXksksDjZpL6LBBTR')
        methods = {
            'main': api.WPRG5rjvVxID,  # 导出列表
        }
        return self._call_module_api('Q8OvSXksksDjZpL6LBBTR', methods, data=data, **kwargs)

    def XXAUcy(self, data='main', **kwargs):
        """保卖管理|订单列表"""
        api = self._get_cached_api('BAc7o7mzTE8oACvyeArJW')
        methods = {
            'main': api.PoY7iA7QafwP,  # 订单列表
        }
        return self._call_module_api('BAc7o7mzTE8oACvyeArJW', methods, data=data, **kwargs)

    def cJ1jYN(self, data='main', **kwargs):
        """保卖管理|商品管理"""
        api = self._get_cached_api('Krj5gFvH88BTJJo3iWzJX')
        methods = {
            'main': api.G1RYa7qCCi7R,  # 商品列表
        }
        return self._call_module_api('Krj5gFvH88BTJJo3iWzJX', methods, data=data, **kwargs)

    def OTblQj(self, data='main', **kwargs):
        """保卖管理|退货管理"""
        api = self._get_cached_api('TD9Y1EebwgkWWw4gbKGII')
        methods = {
            'main': api.MTU290s6GvCd,  # 退货列表
        }
        return self._call_module_api('TD9Y1EebwgkWWw4gbKGII', methods, data=data, **kwargs)

    def bijXOp(self, data='main', **kwargs):
        """拍机管理|售后管理|售后订单"""
        api = self._get_cached_api('ZpUG9P3oxkPb5GFqBrxGQ')
        methods = {
            'main': api.Hz8EMlxg5WBm,  # 售后订单列表
        }
        return self._call_module_api('ZpUG9P3oxkPb5GFqBrxGQ', methods, data=data, **kwargs)

    def CVkKoG(self, data='main', **kwargs):
        """拍机管理|拍机场次列表"""
        api = self._get_cached_api('Z4B1h5YLGNro3dwGrXQhF')
        methods = {
            'main': api.ZuIQQpaDevaL,  # 拍机场次列表
            'a': api.nOhPEhCFHgIT,  # 拍机场次列表 查看场次商品
        }
        return self._call_module_api('Z4B1h5YLGNro3dwGrXQhF', methods, data=data, **kwargs)

    def Wogeh9(self, data='main', **kwargs):
        """运营中心|壹准拍机|售后管理|售后订单
        i 订单状态
        [2]待申诉 [1]线上审核 [3]线上拒退 [4]申诉中 [5]补差成功 [6]可补差
        [7]待寄回 [8]超时取消 [9]主动取消 [10]待接收 [11]实物复检 [12]实物拒退 [13]退货成功
        """
        api = self._get_cached_api('CO4AXsbHeeFE7zOfrBooq')
        methods = {
            'main': api.ZyxQLsb9tEjy,  # 售后订单列表
        }
        return self._call_module_api('CO4AXsbHeeFE7zOfrBooq', methods, data=data, **kwargs)

    def z91bun(self, data='main', **kwargs):
        """平台管理|壹准拍机|售后管理|申诉管理
        i订单类型 0待处理 1申诉成功 2申诉失败 3申诉取消
        """
        api = self._get_cached_api('NLUkzWtFzjZSO2vR8Yhhb')
        methods = {
            'main': api.nG1FaeCsMOtb,  # 申诉管理列表
        }
        return self._call_module_api('NLUkzWtFzjZSO2vR8Yhhb', methods, data=data, **kwargs)

    def VU8ebM(self, data='main', **kwargs):
        """平台管理|壹准拍机|售后管理|售后订单
        i 订单状态
        [2]待申诉 [1]线上审核 [3]线上拒退 [4]申诉中 [5]补差成功 [6]可补差
        [7]待寄回 [8]超时取消 [9]主动取消 [10]待接收 [11]实物复检 [12]实物拒退 [13]退货成功
        """
        api = self._get_cached_api('Oo2tySvRkxOQdjcwVsPry')
        methods = {
            'main': api.LCazQKpPMzmB,  # 售后订单列表
        }
        return self._call_module_api('Oo2tySvRkxOQdjcwVsPry', methods, data=data, **kwargs)

    def wWf0eg(self, data='main', **kwargs):
        """运营中心|壹准拍机|售后管理|售后退货管理
        i 类型  1待退货 2退货已出库
        """
        api = self._get_cached_api('YBoIFlRaGyVtfzeObzsmf')
        methods = {
            'main': api.awpLxMlBWNtR,  # 售后退货列表
        }
        return self._call_module_api('YBoIFlRaGyVtfzeObzsmf', methods, data=data, **kwargs)

    def aY387y(self, data='main', **kwargs):
        """保卖小程序|我的
        i：订单状态 1质检中 2待销售 3销售中 4已销售 5待平台确认 6报价确认 8退货中 9退货已出库 10已退货 7质检完成
        j：类型 1销售服务 2质检服务
        [b] i: 订单状态
        i：订单状态 1待发货 2待取件 3待收货 4已收货 5已完成 6已取消 7已退货
        j：类型 1销售服务 2质检服务
        """
        api = self._get_cached_api('D7NTmTMqMuHicClYboqMC')
        methods = {
            'main': api.NVuRscNpWXeL,  # 销售物品 订单列表
            'a': api.WGXX2ZOSwrbe,  # 销售物品 退货详情
            'b': api.CyIwoGFLypcc,  # 订单信息 订单列表
            'c': api.QxGZi5hQD6xY  # 订单信息 订单详情
        }
        return self._call_module_api('D7NTmTMqMuHicClYboqMC', methods, data=data, **kwargs)

    def jEJvoj(self, data='main', **kwargs):
        """拍机小程序|竞拍"""
        api = self._get_cached_api('B1VzuYLyr5G9mdeT7BDwW')
        methods = {
            'main': api.QwNTfbys2CCL,  # 竞价列表 直拍
            'a': api.Uf0OesfH65Pq,  # 竞价列表 暗拍
        }
        return self._call_module_api('B1VzuYLyr5G9mdeT7BDwW', methods, data=data, **kwargs)

    def Alrd2T(self, data='main', **kwargs):
        """拍机小程序|我的
        i：订单状态 1待支付 2待发货 3待收货 4已收货 5已售后 6已取消
        [a] i：订单状态 1待支付 2已支付 3已取消
        [b] i：订单状态 1待收货 2已收货
        [c] i: 订单状态
        审核中：[1]线上审核 [11]实物复检 [10]待接收 [4]申诉中
        待处理：[7]待寄回 [6]可补差 [2]待申诉
        售后成功：[5]补差成功 [13]退货成功
        售后失败：[9]主动取消 [8]超时取消 [3]线上拒退 [12]实物拒退
        """
        api = self._get_cached_api('UAPqxpSx1qiMwyQEcIPXb')
        methods = {
            'main': api.R0ylvsKYSTRn,  # 拍机商品列表
            'a': api.aKHpuJH4LWMe,  # 我的购买列表
            'b': api.lbnWyhZHxWy3,  # 我的包裹列表
            'c': api.DnyApTb8QiIk,  # 退货售后列表
        }
        return self._call_module_api('UAPqxpSx1qiMwyQEcIPXb', methods, data=data, **kwargs)
