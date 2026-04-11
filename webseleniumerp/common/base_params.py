# coding: utf-8
import json
import inspect
import os

from common.base_api import BaseApi
from config.settings import DATA_PATHS

is_performance_close = DATA_PATHS['performance'] == 'close'


class BaseImport(BaseApi):
    """
    基础导入类，继承自 BaseApi
    该类提供了一个通用的数据获取框架，通过传入不同的 API 类来实现各种业务功能，
    主要用于封装各种业务模块的 API 调用，并提供统一的数据获取方法。
    Attributes:
        api: 实际的 API 实例，默认为 ImportApi 类的实例
    """

    def __init__(self, api_class=None):
        super().__init__()
        if api_class is None:
            from common.import_api import ImportApi
            api_class = ImportApi
        self.post_api = api_class()
        self._request = None  # 延迟初始化

    @property
    def post_request(self):
        """延迟加载 ImportRequest 实例"""
        if self._request is None:
            # 避免循环导入，在使用时才导入
            import sys
            module_name = 'common.import_request'
            if module_name in sys.modules:
                # 如果模块已经加载，直接从中获取类
                ImportRequest = sys.modules[module_name].ImportRequest
            else:
                # 否则正常导入
                from common.import_request import ImportRequest
            self._request = ImportRequest()
        return self._request

    def _get_data(self, api_attr, data, type_map, **kwargs):
        """
        通用数据获取方法
        Args:
            api_attr: API属性名
            data: 数据类型
            type_map: 数据类型映射字典，格式为 {data: (method_name, header_type)}
            **kwargs: 传递给具体方法的参数
        """
        obj = getattr(self.post_api, api_attr)
        if data in type_map:
            method_name, header_type = type_map[data]
            method = getattr(obj, method_name)
            header = obj.headers[header_type]
            kwargs['headers'] = header
            return method(**kwargs)
        else:
            raise ValueError("params_error")

    def _make_request(self, method, url_key, data, header_key=None, nocheck=False):
        """
        通用请求方法
        Args:
            method: HTTP方法 ('get', 'post', 'put', 'delete' 等)
            url_key: 在 self.urls 中的键名
            data: 请求数据
            header_key: 在 self.headers 中的键名
            nocheck: 是否只返回数据而不发送请求
        Returns:
            处理后的响应结果
        """
        if nocheck:
            return data

        try:
            caller_frame = inspect.currentframe().f_back
            caller_method_name = caller_frame.f_code.co_name
        except Exception:
            caller_method_name = "unknown"

        file_name, class_name, default_method_name = self.get_file_and_class_name()
        actual_method_name = caller_method_name if caller_method_name != "_make_request" else default_method_name

        response = self.request_handle(
            method,
            self.urls[url_key],
            data=json.dumps(data),
            headers=self.headers[header_key],
            stress=f'{file_name}.{class_name}.{actual_method_name}'
        )
        return self.get_handle_response(response)

    def validate_request_data(self, generated_data, method_name=None, filename=None, cache_dir='cache_assert'):
        """
        通用数据验证方法，验证失败时自动抛出 ValueError 异常
        Args:
            generated_data: 生成的请求数据
            method_name: 方法名，用于错误信息，如果不传则自动获取调用者方法名
            filename: 缓存文件名，如果不传则自动使用调用方法名
            cache_dir: 缓存目录名称，默认为 cache_assert
        Raises:
            ValueError: 当验证失败时抛出
        """
        # 检查全局开关是否启用
        from config.settings import DATA_PATHS
        if not DATA_PATHS.get('validation_enabled', False):
            return

        if method_name is None or filename is None:
            # 自动获取调用者的方法名
            try:
                caller_frame = inspect.currentframe().f_back
                # 如果调用者是装饰器或包装函数，继续向上查找
                while caller_frame and caller_frame.f_code.co_name in ['wrapper', '_validate_data_with_cache', 'validate_request_data']:
                    caller_frame = caller_frame.f_back
                actual_method_name = caller_frame.f_code.co_name

                if method_name is None:
                    method_name = actual_method_name
                if filename is None:
                    filename = f"{actual_method_name}.json"
            except Exception:
                if method_name is None:
                    method_name = "unknown"
                if filename is None:
                    filename = "unknown.json"

        is_valid, errors = self._validate_data_with_cache(generated_data, filename, cache_dir)

        if not is_valid:
            error_msg = "数据验证失败:\n" + "\n".join(f"  - {error}" for error in errors)
            raise ValueError(f"{method_name} 方法{error_msg}")

    def _get_cache_file_path(self, filename=None, cache_dir='cache_assert'):
        """
        通用缓存文件路径生成方法
        Args:
            filename: 缓存文件名，如果不传则自动使用调用方法名
            cache_dir: 缓存目录名称，默认为 cache_assert
        Returns:
            缓存文件的绝对路径
        """
        if filename is None:
            # 自动获取调用者的方法名作为文件名
            try:
                # 获取调用者的栈帧（跳过当前方法，找上一层）
                caller_frame = inspect.currentframe().f_back
                # 如果调用者是装饰器或包装函数，继续向上查找
                while caller_frame and caller_frame.f_code.co_name in ['wrapper', '_validate_data_with_cache']:
                    caller_frame = caller_frame.f_back
                caller_method_name = caller_frame.f_code.co_name
                filename = f"{caller_method_name}.json"
            except Exception:
                filename = "unknown.json"

        # 使用统一的路径管理
        from common.file_cache_manager import ParamCache
        return ParamCache.get_cache_file_path(filename, cache_dir)

    def _validate_data_structure(self, generated_data, cache_file_path):
        """
        验证生成的数据结构与缓存文件是否一致
        :param generated_data: 生成的请求数据
        :param cache_file_path: 缓存的 JSON 文件路径
        :return: (是否匹配，错误信息列表)
        """
        errors = []

        # 读取缓存文件
        if not os.path.exists(cache_file_path):
            return False, [f"缓存文件不存在：{cache_file_path}"]

        with open(cache_file_path, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)

        # 条件 1: 检查参数结构是否一致
        def get_structure(data, prefix=''):
            """递归获取数据结构"""
            if isinstance(data, dict):
                structure = {}
                for key, value in data.items():
                    structure[key] = get_structure(value, f"{prefix}{key}.")
                return structure
            elif isinstance(data, list):
                if len(data) > 0:
                    return [get_structure(data[0], prefix)]
                return []
            else:
                return type(data).__name__

        generated_structure = get_structure(generated_data)
        cache_structure = get_structure(cache_data)

        if generated_structure != cache_structure:
            errors.append(f"参数结构不一致 - 期望结构：{cache_structure}, 实际结构：{generated_structure}")

        # 条件 2: 检查参数是否多了或者少了
        def get_all_keys(data, prefix=''):
            """递归获取所有键名"""
            keys = set()
            if isinstance(data, dict):
                for key, value in data.items():
                    full_key = f"{prefix}{key}"
                    keys.add(full_key)
                    keys.update(get_all_keys(value, f"{full_key}."))
            elif isinstance(data, list) and len(data) > 0:
                keys.update(get_all_keys(data[0], prefix))
            return keys

        generated_keys = get_all_keys(generated_data)
        cache_keys = get_all_keys(cache_data)

        extra_keys = generated_keys - cache_keys
        missing_keys = cache_keys - generated_keys

        if extra_keys:
            errors.append(f"参数多了：{extra_keys}")
        if missing_keys:
            errors.append(f"参数少了：{missing_keys}")

        # 条件 3: 检查参数名是否一致（通过层级路径对比）
        def get_key_paths(data, path=''):
            """获取所有键的路径"""
            paths = {}
            if isinstance(data, dict):
                for key, value in data.items():
                    current_path = f"{path}.{key}" if path else key
                    paths[current_path] = type(value).__name__
                    if isinstance(value, (dict, list)):
                        paths.update(get_key_paths(value, current_path))
            elif isinstance(data, list) and len(data) > 0:
                paths.update(get_key_paths(data[0], path))
            return paths

        generated_paths = get_key_paths(generated_data)
        cache_paths = get_key_paths(cache_data)

        # 检查相同路径下的类型是否一致
        for path, gen_type in generated_paths.items():
            if path in cache_paths:
                if gen_type != cache_paths[path]:
                    errors.append(f"参数类型不匹配 - 路径：{path}, 期望类型：{cache_paths[path]}, 实际类型：{gen_type}")

        return len(errors) == 0, errors

    def _validate_data_with_cache(self, generated_data, filename=None, cache_dir='cache_assert'):
        """
        通用数据验证方法，自动使用缓存文件验证
        Args:
            generated_data: 生成的请求数据
            filename: 缓存文件名，如果不传则自动使用调用方法名
            cache_dir: 缓存目录名称，默认为 cache_assert
        Returns:
            (是否匹配，错误信息列表)
        """
        # 检查全局开关是否启用
        from config.settings import DATA_PATHS
        if not DATA_PATHS.get('validation_enabled', False):
            return True, []

        cache_file = self._get_cache_file_path(filename, cache_dir)
        return self._validate_data_structure(generated_data, cache_file)


class InitializeParams(BaseImport):

    def __init__(self):
        super().__init__()
        self.pc = PcImport()


class PcImport(BaseImport):

    def CtRBRcFNn2LnUPfJF5Yhu(self, data='main', **kwargs):
        """配件管理|配件库存|库存列表
        i: 库存状态 2库存中 1待入库 3已出库
        j: 品类
        k：品牌
        l：型号
        """
        type_map = {
            'main': ('H2lnntBLD8A3', 'main'),  # 库存列表
        }
        return self._get_data('CtRBRcFNn2LnUPfJF5Yhu', data, type_map, **kwargs)

    def BF3x3lYIzbEHMnrvr80JO(self, data='main', **kwargs):
        """配件管理|入库管理|待接收物品"""
        type_map = {
            'main': ('iigq4MszOhe3', 'main'),  # 待接收物品列表
        }
        return self._get_data('BF3x3lYIzbEHMnrvr80JO', data, type_map, **kwargs)

    def Ln0faZ5CGpaYmkrcCVg4X(self, data='main', **kwargs):
        """配件管理|配件维护"""
        type_map = {
            'main': ('c69L92JCEAfA', 'idle'),  # 配件维护列表
        }
        return self._get_data('Ln0faZ5CGpaYmkrcCVg4X', data, type_map, **kwargs)

    def RjB1dOTFUrlGReUmemgQr(self, data='main', **kwargs):
        """配件管理|入库管理|旧配件入库"""
        type_map = {
            'main': ('U6Xw8Ui8Ti9x', 'main'),  # 旧配件入库列表
            'a': ('eGKYE973IfbO', 'main'),  # 旧配件入库详情
        }
        return self._get_data('RjB1dOTFUrlGReUmemgQr', data, type_map, **kwargs)

    def IW1UwaP9R0hojKPOJQSH4(self, data='main', **kwargs):
        """配件管理|配件销售|销售列表"""
        type_map = {
            'main': ('xTgxXhKIdF5f', 'main'),  # 销售列表
            'a': ('iVaMuxcu6FrP', 'main'),  # 销售详情
            'b': ('q83zbqHUQwKT', 'main'),  # 销售售后
        }
        return self._get_data('IW1UwaP9R0hojKPOJQSH4', data, type_map, **kwargs)

    def OiUAWoPURtS5QdkSFauge(self, data='main', **kwargs):
        """配件管理|配件采购|采购列表"""
        type_map = {
            'main': ('PA6i54jUEr6x', 'main'),  # 采购列表
            'a': ('lJHIDIvQhKow', 'main'),  # 采购售后
        }
        return self._get_data('OiUAWoPURtS5QdkSFauge', data, type_map, **kwargs)

    def DgyYP8ygDMIIeEEXHuLbW(self, data='main', **kwargs):
        """配件管理|配件库存|库存调拨"""
        type_map = {
            'main': ('QGOxnhn1YW7x', 'main'),  # 库存调拨列表
            'a': ('ZT5PSTjrth3p', 'main'),  # 库存调拨详情
            'b': ('rpHRNtqAmFV0', 'main'),  # 撤销调拨详情
        }
        return self._get_data('DgyYP8ygDMIIeEEXHuLbW', data, type_map, **kwargs)

    def AMaXd2PkDsrT5cj1SArOe(self, data='main', **kwargs):
        """配件管理|移交接收管理|接收物品"""
        type_map = {
            'main': ('s3Ycs7Oyt5DL', 'main'),  # 移交单接收列表
            'a': ('mfaVZuvBLcri', 'main'),  # 物品接收列表
        }
        return self._get_data('AMaXd2PkDsrT5cj1SArOe', data, type_map, **kwargs)

    def LnfQBDqBvleaE2O0412qk(self, data='main', **kwargs):
        """配件管理|入库管理|分拣列表"""
        type_map = {
            'main': ('IB3TfKONJp2x', 'main'),  # 分拣列表
        }
        return self._get_data('LnfQBDqBvleaE2O0412qk', data, type_map, **kwargs)

    def KFkHdZyASZRhMrmNKfHiQ(self, data='main', **kwargs):
        """配件管理|入库管理|新到货入库"""
        type_map = {
            'main': ('aYrCZLAaSxA7', 'main'),  # 新到货入库列表
        }
        return self._get_data('KFkHdZyASZRhMrmNKfHiQ', data, type_map, **kwargs)

    def NQXuyZ5kySQBpsQJxR3vC(self, data='main', **kwargs):
        """财务管理|资金账户|账户列表"""
        type_map = {
            'main': ('xsn47jtSUiZ8', 'idle'),  # 账户列表
        }
        return self._get_data('NQXuyZ5kySQBpsQJxR3vC', data, type_map, **kwargs)

    def VFy40VMBZGf8pQEkVFRor(self, data='main', **kwargs):
        """财务管理|业务记账|账单审核
        i：1应付 2应收
        j: 0待审核 1审核通过 2未通过
        """
        type_map = {
            'main': ('zS2mEs09Al0d', 'main'),  # 应付应收账单
            'a': ('zS2mEs09Al0d', 'vice'),  # 应付应收账单
        }
        return self._get_data('VFy40VMBZGf8pQEkVFRor', data, type_map, **kwargs)

    def MOyeqlzcgLqhqdWBrkyYg(self, data='main', **kwargs):
        """财务管理|业务记账|往来应付"""
        type_map = {
            'main': ('VPtqPg96V4bb', 'main'),  # 对账详情
            'a': ('aXD0ILNAtA0v', 'main'),  # 按机器结算 添加机器 机器列表
            'b': ('Anlk8HQ08DoN', 'main'),  # 对账详情 单据详情
            'c': ('NrrYfPEfdJwE', 'main'),  # 往来应付列表
            'd': ('rRW8valbixkj', 'main'),  # 按供应商结算 列表
        }
        return self._get_data('MOyeqlzcgLqhqdWBrkyYg', data, type_map, **kwargs)

    def A9mwkPeNc1x7YnLCF9jUk(self, data='main', **kwargs):
        """财务管理|业务记账|往来应收"""
        type_map = {
            'main': ('onzqxhWPmd6i', 'main'),  # 对账详情
            'a': ('iL6f7yggjwGo', 'main'),  # 按机器结算 添加机器 机器列表
            'b': ('oIkWBNgsRuRQ', 'main'),  # 对账详情 单据详情
            'c': ('bWw7A4mK6xtK', 'main'),  # 往来应收列表
            'd': ('uznhxIKxB5lv', 'main'),  # 按客户结算 列表
        }
        return self._get_data('A9mwkPeNc1x7YnLCF9jUk', data, type_map, **kwargs)

    def PurkQXBjQXG3tz8hUb1SF(self, data='main', **kwargs):
        """帮卖管理|帮卖上架列表
        i：物品状态 wsg待发货 wtg待收货 rg已收货 wr待质检 wbi待议价 wb待确认 ws待结算 wrg待退机 rig退机中 wsr待售出
        """
        type_map = {
            'main': ('l6TOXA4JkEjO', 'main'),  # 订单列表
            'a': ('gavz8010zhrA', 'main'),  # 发起帮卖列表
        }
        return self._get_data('PurkQXBjQXG3tz8hUb1SF', data, type_map, **kwargs)

    def Jc9Odo2T6JqvbWDRSsDXy(self, data='main', **kwargs):
        """帮卖管理|帮卖来货列表"""
        type_map = {
            'main': ('vw76zdVHgk8Q', 'vice'),  # 订单列表
        }
        return self._get_data('Jc9Odo2T6JqvbWDRSsDXy', data, type_map, **kwargs)

    def Ea7Wjr4ctTv69frbEUPZJ(self, data='main', **kwargs):
        """帮卖管理|帮卖业务配置"""
        type_map = {
            'main': ('OUYQFhYf3krT', 'vice'),  # 帮卖业务配置列表
        }
        return self._get_data('Ea7Wjr4ctTv69frbEUPZJ', data, type_map, **kwargs)

    def Ie1Dlx6hKL0xHjTgV7J4p(self, data='main', **kwargs):
        """库存管理|出库管理|地址管理"""
        type_map = {
            'main': ('X41neJLZTAeU', 'idle'),  # 地址管理列表
        }
        return self._get_data('Ie1Dlx6hKL0xHjTgV7J4p', data, type_map, **kwargs)

    def UYV6mZaVwDk4HHhyuWRRp(self, data='main', **kwargs):
        """库存管理|库存列表
        i：库存状态 2库存中 1待入库 3已出库
        j：物品状态 13待销售 3待分货 7维修中 5质检中 19销售预售中 14销售铺货中 16待送修 9已销售 15销售售后中 17送修中 11采购售后完成 12采购售后中 18仅出库 10待采购售后
        """
        type_map = {
            'main': ('I8TzeuUVWOYr', 'main'),  # 库存列表
            'a': ('I8TzeuUVWOYr', 'vice'),  # 库存列表
            'b': ('DiPuR7wiWR9p', 'main'),  # 物品详情 销售信息
            'c': ('LtZxEhUVdwQS', 'main'),  # 物品详情 操作日志
        }
        return self._get_data('UYV6mZaVwDk4HHhyuWRRp', data, type_map, **kwargs)

    def QYSFzOWmZ2zYnize8ppKN(self, data='main', **kwargs):
        """库存管理|出库管理|仅出库订单列表"""
        type_map = {
            'main': ('ORF5PGdo8vkp', 'main'),  # 仅出库列表
            'a': ('FlBn7VEIrt0P', 'main'),  # 仅出库订单详情
        }
        return self._get_data('QYSFzOWmZ2zYnize8ppKN', data, type_map, **kwargs)

    def LWT9dymUmXdvWqLk1qEeA(self, data='main', **kwargs):
        """库存管理|移交接收管理|接收物品
        i：物品状态 1待维修 2待收货 3待分货 4待质检 5质检中 6待维修 7维修中
        """
        type_map = {
            'main': ('wX85yA1a0yOb', 'main'),  # 物品接收列表
            'a': ('XbUs4Xjcx1eU', 'main'),  # 移交单接收列表
            'b': ('fPKMGLwa2uJG', 'main'),  # 移交单接收详情
        }
        return self._get_data('LWT9dymUmXdvWqLk1qEeA', data, type_map, **kwargs)

    def PzpwGb0gERxw3s5t4WiGd(self, data='main', **kwargs):
        """库存管理|移交接收管理|移交记录
        """
        type_map = {
            'main': ('YsmsUS99q8Mf', 'main'),  # 移交记录列表
            'a': ('O2cpz6NJM1Ql', 'main'),  # 移交记录详情
        }
        return self._get_data('PzpwGb0gERxw3s5t4WiGd', data, type_map, **kwargs)

    def BFOjFKv6ZxII7V5LzQcr4(self, data='main', **kwargs):
        """配件管理|移交接收管理|移交记录
        """
        type_map = {
            'main': ('pvspNI89ooNR', 'main'),  # 移交记录列表
            'a': ('ABCpFCzCuSNt', 'main'),  # 移交记录详情
        }
        return self._get_data('BFOjFKv6ZxII7V5LzQcr4', data, type_map, **kwargs)

    def Ux7lF2b6qktEytPTzyaQW(self, data='main', **kwargs):
        """库存管理|库存盘点"""
        type_map = {
            'main': ('dGxdNvDrm0gW', 'main'),  # 库存盘点列表
        }
        return self._get_data('Ux7lF2b6qktEytPTzyaQW', data, type_map, **kwargs)

    def XHyhIffDlKvRSMGo6DlG2(self, data='main', **kwargs):
        """库存管理|库存调拨"""
        type_map = {
            'main': ('scIEFidBwtZs', 'main'),  # 仓库调拨列表
            'a': ('pbck8gdOUVzz', 'main'),  # 仓库调拨详情
        }
        return self._get_data('XHyhIffDlKvRSMGo6DlG2', data, type_map, **kwargs)

    def D2grXOWzOv0I5f5rFGf6A(self, data='main', **kwargs):
        """库存管理|入库管理|物流列表"""
        type_map = {
            'main': ('bI2yFNa61M9Q', 'main'),  # 物流列表
            'a': ('t9tSA8AX8kJj', 'main'),  # 物流列表详情
        }
        return self._get_data('D2grXOWzOv0I5f5rFGf6A', data, type_map, **kwargs)

    def WbrwTMcyqVsFRjRMcUD9e(self, data='main', **kwargs):
        """库存管理|入库管理|物流签收入库"""
        type_map = {
            'main': ('joJXaZxu9B1W', 'main'),  # 物流列表
        }
        return self._get_data('WbrwTMcyqVsFRjRMcUD9e', data, type_map, **kwargs)

    def KxO3PKRgVuNDVjQUSHVcl(self, data='main', **kwargs):
        """消息管理|消息发布列表"""
        type_map = {
            'main': ('qTd9V34NC3MZ', 'main'),  # 消息发布列表
        }
        return self._get_data('KxO3PKRgVuNDVjQUSHVcl', data, type_map, **kwargs)

    def AlZdueYspz0c2CHbT7D29(self, data='main', **kwargs):
        """平台管理|同售管理|商品审核"""
        type_map = {
            'main': ('ILGktF8orGlt', 'platform'),  # 待审核列表
        }
        return self._get_data('AlZdueYspz0c2CHbT7D29', data, type_map, **kwargs)

    def IyY9m4jNrW6D0vQNpkgVH(self, data='main', **kwargs):
        """平台管理|消息管理|消息发布列表"""
        type_map = {
            'main': ('cCF5oVBu3uHW', 'platform'),  # 回收商发布列表
        }
        return self._get_data('IyY9m4jNrW6D0vQNpkgVH', data, type_map, **kwargs)

    def V3LpfoN0H354ztNVHPWtf(self, data='main', **kwargs):
        """平台管理|订单管理|订单审核"""
        type_map = {
            'main': ('TdbQGLoDJMFo', 'platform'),  # 订单审核列表
        }
        return self._get_data('V3LpfoN0H354ztNVHPWtf', data, type_map, **kwargs)

    def VzF4todMPF4UN7aNpYfCs(self, data='main', **kwargs):
        """平台管理|商户管理"""
        type_map = {
            'main': ('LZRK5ZWFXGxQ', 'platform'),  # 商户管理列表
        }
        return self._get_data('VzF4todMPF4UN7aNpYfCs', data, type_map, **kwargs)

    def YVqIQus8roZWysBseaMP0(self, data='main', **kwargs):
        """平台管理|运营中心|待指定物品"""
        type_map = {
            'main': ('DSpcSKcA7pw5', 'super'),  # 待指定物品列表
        }
        return self._get_data('YVqIQus8roZWysBseaMP0', data, type_map, **kwargs)

    def BaxRsHzRpoNsTb8fnSa9e(self, data='main', **kwargs):
        """平台管理|卖场管理|直拍卖场列表
        i: 上架状态 1已上架 2待上架 3已下架
        """
        type_map = {
            'main': ('gXHSWafumwCe', 'super'),  # 直拍卖场列表
            'a': ('wpfOmsjWdkny', 'super'),  # 编辑详情
            'b': ('oTwifIq7ER6o', 'super'),  # 查看场次详情 场次列表
            'c': ('sh3cTsLUbzwu', 'super'),  # 查看场次详情 商品列表
        }
        return self._get_data('BaxRsHzRpoNsTb8fnSa9e', data, type_map, **kwargs)

    def EEdalTouEaLL3VEx3wMnz(self, data='main', **kwargs):
        """平台管理|卖场管理|暗拍卖场列表
        i: 上架状态 1已上架 2待上架 3已下架
        """
        type_map = {
            'main': ('pzCWj3Ksrd4P', 'super'),  # 暗拍卖场列表
            'a': ('TezdhkF6QXGQ', 'super'),  # 编辑详情
            'b': ('i2hsWJeCQxKo', 'super'),  # 查看场次详情 场次列表
            'c': ('q5mIVNB1zQPk', 'super'),  # 查看场次详情 商品列表
        }
        return self._get_data('EEdalTouEaLL3VEx3wMnz', data, type_map, **kwargs)

    def HnlUtAPz07JtZRXny3Ogs(self, data='main', **kwargs):
        """平台管理|虚拟库存|上拍商品管理
        i：类型 1可上拍商品 2已上拍商品 3待定价物品     这里是从pc或者小程序的查询列表去拿最新数据的，比如我新增采购单，物品编号是唯一的
        那么这个用力就是用这个物品编号，另外的用例需要新造数据去拿数据，不然数据混淆，举个例子
        [a]：i：类型 1暗拍 2直拍
        """
        type_map = {
            'main': ('FgMfvbUdU4qZ', 'super'),  # 上拍商品管理列表
            'a': ('LWfPhO8u3XJv', 'super'),  # 选择场次列表
        }
        return self._get_data('HnlUtAPz07JtZRXny3Ogs', data, type_map, **kwargs)

    def B63gyanXogW9NpUu1Gr1K(self, data='main', **kwargs):
        """平台管理|运营中心|验机中心管理"""
        type_map = {
            'main': ('cQkBD5in87Ys', 'super'),  # 验机中心管理列表
        }
        return self._get_data('B63gyanXogW9NpUu1Gr1K', data, type_map, **kwargs)

    def Jz32tuIMNM7geguh5D8TF(self, data='main', **kwargs):
        """商品采购|采购售后管理|采购售后列表"""
        type_map = {
            'main': ('a3xoH8PZvyPQ', 'main'),  # 采购售后列表
        }
        return self._get_data('Jz32tuIMNM7geguh5D8TF', data, type_map, **kwargs)

    def ZzpxfXbO9fEmLG1gxxzjP(self, data='main', **kwargs):
        """商品采购|采购任务"""
        type_map = {
            'main': ('we5YUPreA4h0', 'main'),  # 采购任务列表
            'a': ('sOOabMKgYnDs', 'main'),  # 更新到货详情
            'b': ('i13Vwm2s7hDn', 'main'),  # 采购录入详情
        }
        return self._get_data('ZzpxfXbO9fEmLG1gxxzjP', data, type_map, **kwargs)

    def XHVW0IhQgPnb63fnaqTdN(self, data='main', **kwargs):
        """商品采购|采购售后管理|待售后列表"""
        type_map = {
            'main': ('gx9ALZDTXtyL', 'main'),  # 待售后列表
        }
        return self._get_data('XHVW0IhQgPnb63fnaqTdN', data, type_map, **kwargs)

    def Z6BEKs3GvdIWf6a1Dj2uP(self, data='main', **kwargs):
        """商品采购|采购管理|采购订单列表"""
        type_map = {
            'main': ('QYMK9r8Zx1lb', 'main'),  # 采购订单列表
            'a': ('ua4pZjFEITx3', 'main'),  # 采购单详情
        }
        return self._get_data('Z6BEKs3GvdIWf6a1Dj2uP', data, type_map, **kwargs)

    def UCpwX0dlRXRmKVzfDX5dd(self, data='main', **kwargs):
        """商品采购|供应商管理"""
        type_map = {
            'main': ('q9RXyfc2X1UG', 'idle'),  # 供应商管理列表
        }
        return self._get_data('UCpwX0dlRXRmKVzfDX5dd', data, type_map, **kwargs)

    def WmKG9OkI9OlJlOENUzgNu(self, data='main', **kwargs):
        """商品采购|采购管理|采购工单"""
        type_map = {
            'main': ('b1R30NI8UzKR', 'main'),  # 采购工单列表
        }
        return self._get_data('WmKG9OkI9OlJlOENUzgNu', data, type_map, **kwargs)

    def Rwpqef340gYUd4Hgkbq8l(self, data='main', **kwargs):
        """商品采购|采购售后管理|待接收物品"""
        type_map = {
            'main': ('JsXBVOMtGANq', 'main'),  # 待接收物品列表
        }
        return self._get_data('Rwpqef340gYUd4Hgkbq8l', data, type_map, **kwargs)

    def Y6hDdvp1tY9uk0H51cn91(self, data='main', **kwargs):
        """商品采购|采购管理|未发货订单列表"""
        type_map = {
            'main': ('B2HBJYTnnYyI', 'main'),  # 未发货订单列表
        }
        return self._get_data('Y6hDdvp1tY9uk0H51cn91', data, type_map, **kwargs)

    def THtT7YW545kAG73W2gHDj(self, data='main', **kwargs):
        """商品采购|采购管理|到货通知单列表"""
        type_map = {
            'main': ('Yf0yiomYxwUn', 'main'),  # 到货通知单列表
        }
        return self._get_data('THtT7YW545kAG73W2gHDj', data, type_map, **kwargs)

    def UJwDgUZKhNNEKJEIdEAKw(self, data='main', **kwargs):
        """质检管理|质检中物品"""
        type_map = {
            'main': ('diFPISdg6WyC', 'main'),  # 质检中物品列表
        }
        return self._get_data('UJwDgUZKhNNEKJEIdEAKw', data, type_map, **kwargs)

    def TzjKXVa7hC8j6pmsPJQvk(self, data='main', **kwargs):
        """质检管理|质检内容模版"""
        type_map = {
            'main': ('WY9tdqjthqMp', 'idle'),  # 质检内容模版列表
        }
        return self._get_data('TzjKXVa7hC8j6pmsPJQvk', data, type_map, **kwargs)

    def PYi7eKoJOr5suysXpCFvf(self, data='main', **kwargs):
        """质检管理|待移交物品"""
        type_map = {
            'main': ('eJitQXxutgtJ', 'main'),  # 待移交物品列表
        }
        return self._get_data('PYi7eKoJOr5suysXpCFvf', data, type_map, **kwargs)

    def QyKIiWECv2ppl2UxZhwh3(self, data='main', **kwargs):
        """质检管理|质检记录列表"""
        type_map = {
            'main': ('vAUM2VniBdJP', 'main'),  # 质检记录列表
        }
        return self._get_data('QyKIiWECv2ppl2UxZhwh3', data, type_map, **kwargs)

    def ZdhlTgRrRPGEMOegDrOfk(self, data='main', **kwargs):
        """维修管理|维修审核列表"""
        type_map = {
            'main': ('dUaU2azQ6FGY', 'main'),  # 维修审核列表 待审核
        }
        return self._get_data('ZdhlTgRrRPGEMOegDrOfk', data, type_map, **kwargs)

    def Gv7PVAqUJKoyfROzOacmx(self, data='main', **kwargs):
        """维修管理|维修项目列表
        i: 品类 1手机 2平板 3电脑 4手表
        """
        type_map = {
            'main': ('bltCvd8b8uHx', 'idle'),
            'a': ('bltCvd8b8uHx', 'main'),
        }
        return self._get_data('Gv7PVAqUJKoyfROzOacmx', data, type_map, **kwargs)

    def JU8QYbNi3BDlSn2XaNZKe(self, data='main', **kwargs):
        """商品销售|销售管理|已销售物品列表
        i：销售状态 2已销售 3已取消 1销售中
        j：销售类型 1销售 3铺货 5预售
        """
        type_map = {
            'main': ('L6IQgdpG4iaP', 'main'),  # 已销售物品列表
        }
        return self._get_data('JU8QYbNi3BDlSn2XaNZKe', data, type_map, **kwargs)

    def Ez77PXDybIrSTaH32RHsz(self, data='main', **kwargs):
        """商品销售|销售管理|销售中物品列表
        i：销售状态 2已销售 3已取消 1销售中
        j：销售类型 1销售 3铺货 5预售
        """
        type_map = {
            'main': ('TyFTRRkgcx28', 'main'),  # 销售中物品列表
            'a': ('fReTQwlPp5ig', 'main'),  # 销售物品详情
            'b': ('JPomkBOsk0MN', 'main'),  # 下架详情
        }
        return self._get_data('Ez77PXDybIrSTaH32RHsz', data, type_map, **kwargs)

    def XTk41pUDr28xCf1YL17uR(self, data='main', **kwargs):
        """商品销售|销售管理|待销售物品"""
        type_map = {
            'main': ('CSDYFXdhL7n5', 'main'),  # 待销售物品列表
            'a': ('enB0x369cbFt', 'main'),  # 待销售物品 详情
        }
        return self._get_data('XTk41pUDr28xCf1YL17uR', data, type_map, **kwargs)

    def Nd81xbVVnxevE1Oy8yXcy(self, data='main', **kwargs):
        """配件管理|配件销售|销售售后列表"""
        type_map = {
            'main': ('VGeFY2YzIHzc', 'main'),  # 销售售后列表
            'a': ('FOLBxm2fXcoW', 'main'),  # 销售售后详情
        }
        return self._get_data('Nd81xbVVnxevE1Oy8yXcy', data, type_map, **kwargs)

    def Kw5nIo3WQBrH2BPScRj1B(self, data='main', **kwargs):
        """商品销售|销售售后管理|销售售后列表"""
        type_map = {
            'main': ('CfIRP7WqVPD0', 'main'),  # 销售售后完成
            'a': ('TB2VQJLBUDje', 'main'),  # 销售售后中
        }
        return self._get_data('Kw5nIo3WQBrH2BPScRj1B', data, type_map, **kwargs)

    def Mb5NtymgNZq58BhIE7Umz(self, data='main', **kwargs):
        """商品销售|销售管理|待接收物品"""
        type_map = {
            'main': ('z8Q8CdTAeeYa', 'main'),  # 待接收物品列表
        }
        return self._get_data('Mb5NtymgNZq58BhIE7Umz', data, type_map, **kwargs)

    def PvQWvJ1ETZicFTZpXHiQa(self, data='main', **kwargs):
        """商品销售|销售管理|销售中订单列表"""
        type_map = {
            'main': ('lZHWz7XAePfb', 'main'),  # 销售中订单列表
        }
        return self._get_data('PvQWvJ1ETZicFTZpXHiQa', data, type_map, **kwargs)

    def OY2fdbdieaa3seD31U6ZQ(self, data='main', **kwargs):
        """商品销售|销售管理|已销售订单列表"""
        type_map = {
            'main': ('B37xGAx8rLVJ', 'main'),  # 销售中订单列表
        }
        return self._get_data('OY2fdbdieaa3seD31U6ZQ', data, type_map, **kwargs)

    def QM4hD6LNhqKxZAitqFFJl(self, data='main', **kwargs):
        """送修管理|已送修物品"""
        type_map = {
            'main': ('bkXQFPd3Pz5I', 'main'),  # 已送修物品列表
        }
        return self._get_data('QM4hD6LNhqKxZAitqFFJl', data, type_map, **kwargs)

    def MMuymWgzUDbCSdlZPeMMY(self, data='main', **kwargs):
        """送修管理|送修单列表"""
        type_map = {
            'main': ('FaEsPLDSYo0I', 'main'),  # 送修单列表
        }
        return self._get_data('MMuymWgzUDbCSdlZPeMMY', data, type_map, **kwargs)

    def WziJGBshZjou10L8PleRe(self, data='main', **kwargs):
        """系统管理|基础设置|工单配置
        i：业务名称 付款 报价 退货 工序
        """
        type_map = {
            'main': ('keAqvfuWduT9', 'main'),  # 瑕疵项列表
            'a': ('tJ7mRunfhfkN', 'main'),  # 业务工序列表
        }
        return self._get_data('WziJGBshZjou10L8PleRe', data, type_map, **kwargs)

    def BoKPsGPfTNvMGy8lEDfDK(self, data='main', **kwargs):
        """商城管理|网点管理"""
        type_map = {
            'main': ('nNxpGKdNDGBb', 'main'),  # 网点管理列表
        }
        return self._get_data('BoKPsGPfTNvMGy8lEDfDK', data, type_map, **kwargs)

    def VzruD2bzEUPV1JJY9d6vF(self, data='main', **kwargs):
        """运营中心|订单管理
        i：订单状态 1待发货 2待取件 3待收货 4已收货 5已完成 6已取消 7已退货
        """
        type_map = {
            'main': ('G1ZATPtlzjWF', 'main'),  # 订单列表
            'a': ('URWCKM7vfuMg', 'main'),  # 物品列表
        }
        return self._get_data('VzruD2bzEUPV1JJY9d6vF', data, type_map, **kwargs)

    def FYXRA4IxF49PvhUCLpp5Z(self, data='main', **kwargs):
        """运营中心|质检管理
        [d]i类型 1未上传 2已上传
        """
        type_map = {
            'main': ('KhNjoVcM4iuf', 'main'),  # 待领取物品列表
            'a': ('OHXGClp3BoJm', 'main'),  # 质检中物品列表
            'b': ('oSzj9Md6vHyl', 'main'),  # 已质检物品列表
            'c': ('eDr2hpq6xEBa', 'main'),  # 重验申请列表
            'd': ('YkybIUUCs2Dh', 'main'),  # 商品图拍摄
            'e': ('AY6K1XbHNTzW', 'main'),  # 质检模版
            'f': ('KhNjoVcM4iuf', 'camera'),  # 待领取物品列表
            'g': ('OHXGClp3BoJm', 'camera'),  # 质检中物品列表
            'h': ('AY6K1XbHNTzW', 'camera'),  # 质检模版
        }
        return self._get_data('FYXRA4IxF49PvhUCLpp5Z', data, type_map, **kwargs)

    def KgbSrz63njmC8XfrU1jty(self, data='main', **kwargs):
        """运营中心|收货入库"""
        type_map = {
            'main': ('skBKV5OKhyz7', 'main'),  # 搜索保卖订单号
            'a': ('h1cdqp8AtfOD', 'main'),  # 搜索保卖物流单号
            'b': ('jxEKaglEujSi', 'main'),  # 搜索拍机订单号
            'c': ('skBKV5OKhyz7', 'camera'),  # 搜索保卖订单号
        }
        return self._get_data('KgbSrz63njmC8XfrU1jty', data, type_map, **kwargs)

    def M4Xsay25almyg0RzXz4ui(self, data='main', **kwargs):
        """运营中心|退货管理
         i：订单状态 1待退货 2待取货 3退货已出库 4已退货 5已取消
        """
        type_map = {
            'main': ('WCB6NcIMpsMe', 'main'),  # 商户明细列表
            'a': ('ua4JlujLXZDP', 'main'),  # 物品明细列表
            'b': ('VnssCpqfEIlk', 'main'),  # 批次明细列表
        }
        return self._get_data('M4Xsay25almyg0RzXz4ui', data, type_map, **kwargs)

    def RjVgo4LDzg4voonKUBXr1(self, data='main', **kwargs):
        """运营中心|待报价物品"""
        type_map = {
            'main': ('vSNmU0ZwGwPu', 'main'),  # 待报价物品列表
        }
        return self._get_data('RjVgo4LDzg4voonKUBXr1', data, type_map, **kwargs)

    def M55r2pn7CkJ0DzgKvHhuX(self, data='main', **kwargs):
        """运营中心|物品出库"""
        type_map = {
            'main': ('OpUzgQkpwsBG', 'main'),  # 物品出库 销售出库
        }
        return self._get_data('M55r2pn7CkJ0DzgKvHhuX', data, type_map, **kwargs)

    def KmxOWBECeMnMqtP1qACyx(self, data='main', **kwargs):
        """运营中心|销售发货管理"""
        type_map = {
            'main': ('Oqr9od3TrupA', 'main'),  # 待发货 按商户
            'a': ('N3GKYzC6P5TZ', 'main'),  # 待发货 按物品
            'b': ('fNSLGMFC7atc', 'main'),  # 待收货 按物品
            'c': ('clirkK4CTUj0', 'main'),  # 待收货 按包裹
            'd': ('uByZKczL88yQ', 'main'),  # 已收货 按包裹
            'e': ('ntnTnNcZjnPi', 'main'),  # 已收货 按物品
        }
        return self._get_data('KmxOWBECeMnMqtP1qACyx', data, type_map, **kwargs)

    def TD9Y1EebwgkWWw4gbKGII(self, data='main', **kwargs):
        """保卖管理|退货管理
         i：订单状态 1待退货 2待取货 3退货已出库 4已退货 5已取消
        """
        type_map = {
            'main': ('MTU290s6GvCd', 'main'),  # 物品明细列表
            'a': ('BxBcWC50E2qm', 'main'),  # 批次明细列表
        }
        return self._get_data('TD9Y1EebwgkWWw4gbKGII', data, type_map, **kwargs)

    def BAc7o7mzTE8oACvyeArJW(self, data='main', **kwargs):
        """保卖管理|订单列表
        i：订单状态 1待发货 2待取件 3待收货 4已收货 5已完成 6已取消 7已退货
        """
        type_map = {
            'main': ('PoY7iA7QafwP', 'main'),  # 订单列表
            'a': ('v6lgcdrrB6rn', 'main'),  # 物品列表
        }
        return self._get_data('BAc7o7mzTE8oACvyeArJW', data, type_map, **kwargs)

    def Krj5gFvH88BTJJo3iWzJX(self, data='main', **kwargs):
        """保卖管理|商品管理
        i：订单状态 1质检中 2待销售 3销售中
        """
        type_map = {
            'main': ('G1RYa7qCCi7R', 'main'),  # 商品管理列表
        }
        return self._get_data('Krj5gFvH88BTJJo3iWzJX', data, type_map, **kwargs)

    def ZpUG9P3oxkPb5GFqBrxGQ(self, data='main', **kwargs):
        """拍机管理|售后管理|售后订单"""
        type_map = {
            'main': ('Hz8EMlxg5WBm', 'camera'),  # 售后订单列表
        }
        return self._get_data('ZpUG9P3oxkPb5GFqBrxGQ', data, type_map, **kwargs)

    def CO4AXsbHeeFE7zOfrBooq(self, data='main', **kwargs):
        """运营中心|壹准拍机|售后管理|售后订单
        i 订单状态
        [2]待申诉 [1]线上审核 [3]线上拒退 [4]申诉中 [5]补差成功 [6]可补差
        [7]待寄回 [8]超时取消 [9]主动取消 [10]待接收 [11]实物复检 [12]实物拒退 [13]退货成功
        """
        type_map = {
            'main': ('ZyxQLsb9tEjy', 'main'),  # 售后订单列表
        }
        return self._get_data('CO4AXsbHeeFE7zOfrBooq', data, type_map, **kwargs)

    def NLUkzWtFzjZSO2vR8Yhhb(self, data='main', **kwargs):
        """平台管理|壹准拍机|售后管理|申诉管理
        i订单类型 0待处理 1申诉成功 2申诉失败 3申诉取消
        """
        type_map = {
            'main': ('nG1FaeCsMOtb', 'super'),  # 申诉管理列表
        }
        return self._get_data('NLUkzWtFzjZSO2vR8Yhhb', data, type_map, **kwargs)

    def YBoIFlRaGyVtfzeObzsmf(self, data='main', **kwargs):
        """运营中心|壹准拍机|售后管理|售后退货管理
        i 类型  1待退货 2退货已出库
        """
        type_map = {
            'main': ('awpLxMlBWNtR', 'super'),  # 售后退货列表
        }
        return self._get_data('YBoIFlRaGyVtfzeObzsmf', data, type_map, **kwargs)

    def Z4B1h5YLGNro3dwGrXQhF(self, data='main', **kwargs):
        """拍机管理|拍机场次列表"""
        type_map = {
            'main': ('ZuIQQpaDevaL', 'camera'),  # 拍机场次列表
            'a': ('nOhPEhCFHgIT', 'camera'),  # 查看场次商品
        }
        return self._get_data('Z4B1h5YLGNro3dwGrXQhF', data, type_map, **kwargs)

    def D7NTmTMqMuHicClYboqMC(self, data='main', **kwargs):
        """保卖小程序|我的
         i：订单状态 1质检中 2待销售 3销售中 4已销售 5待平台确认 6报价确认 8退货中 9退货已出库 10已退货 7质检完成
         j：类型 1销售服务 2质检服务
        [b]
         i：订单状态 1待发货 2待取件 3待收货 4已收货
         j：类型 1销售服务 2质检服务
        """
        type_map = {
            'main': ('NVuRscNpWXeL', 'main'),  # 销售物品 订单列表
            'a': ('WGXX2ZOSwrbe', 'main'),  # 销售物品 退货详情
            'b': ('CyIwoGFLypcc', 'main'),  # 订单信息 订单列表
        }
        return self._get_data('D7NTmTMqMuHicClYboqMC', data, type_map, **kwargs)

    def Of0qYX0IunlCsfIKGi4b5(self, data='main', **kwargs):
        """保卖小程序|首页"""
        type_map = {
            'main': ('WiNPlq2wIljG', 'main'),  # 精确发货 物品信息列表
            'a': ('wuqs6Abzx3BS', 'main'),  # 精确发货 外观成色列表
        }
        return self._get_data('Of0qYX0IunlCsfIKGi4b5', data, type_map, **kwargs)

    def B1VzuYLyr5G9mdeT7BDwW(self, data='main', **kwargs):
        """拍机小程序|竞拍"""
        type_map = {
            'main': ('QwNTfbys2CCL', 'camera'),  # 竞拍列表 直拍
            'a': ('Uf0OesfH65Pq', 'camera'),  # 竞拍列表 暗拍
        }
        return self._get_data('B1VzuYLyr5G9mdeT7BDwW', data, type_map, **kwargs)

    def UAPqxpSx1qiMwyQEcIPXb(self, data='main', **kwargs):
        """拍机小程序|我的
        i：订单状态 1待支付 2待发货 3待收货 4已收货  5已售后 6已取消
        [a]i: 订单状态
        审核中：[1]线上审核 [11]实物复检 [10]待接收 [4]申诉中
        待处理：[7]待寄回 [6]可补差 [2]待申诉
        售后成功：[5]补差成功 [13]退货成功
        售后失败：[9]主动取消 [8]超时取消 [3]线上拒退 [12]实物拒退
        """
        type_map = {
            'main': ('R0ylvsKYSTRn', 'camera'),  # 商品列表
            'a': ('DnyApTb8QiIk', 'camera'),  # 售后退货列表
        }
        return self._get_data('UAPqxpSx1qiMwyQEcIPXb', data, type_map, **kwargs)

    def KsJkf77pdK7sRJY6s9lfO(self, data='main', **kwargs):
        """运营中心|bot订单管理"""
        type_map = {
            'main': ('FTdfLz90lzeR', 'main'),  # bot订单管理列表
        }
        return self._get_data('KsJkf77pdK7sRJY6s9lfO', data, type_map, **kwargs)

    def VnVeCrt7kNUg7iObK5ZBc(self, data='main', **kwargs):
        """运营中心|bot收货入库"""
        type_map = {
            'main': ('KdrTCtXRVAJ7', 'main'),  # 搜索订单号
        }
        return self._get_data('VnVeCrt7kNUg7iObK5ZBc', data, type_map, **kwargs)
