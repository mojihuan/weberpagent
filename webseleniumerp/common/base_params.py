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

    def attachment_inventory_list_data(self, data='main', **kwargs):
        """配件管理|配件库存|库存列表
        i: 库存状态 2库存中 1待入库 3已出库
        j: 品类
        k：品牌
        l：型号
        """
        type_map = {
            'main': ('attachment_inventory_list', 'main'),  # 库存列表
        }
        return self._get_data('attachment_inventory_list', data, type_map, **kwargs)

    def attachment_goods_received_data(self, data='main', **kwargs):
        """配件管理|入库管理|待接收物品"""
        type_map = {
            'main': ('list_of_items_to_be_received', 'main'),  # 待接收物品列表
        }
        return self._get_data('attachment_goods_received', data, type_map, **kwargs)

    def attachment_maintenance_data(self, data='main', **kwargs):
        """配件管理|配件维护"""
        type_map = {
            'main': ('maintenance_list', 'idle'),  # 配件维护列表
        }
        return self._get_data('attachment_maintenance', data, type_map, **kwargs)

    def attachment_old_warehouse_data(self, data='main', **kwargs):
        """配件管理|入库管理|旧配件入库"""
        type_map = {
            'main': ('accessories_inventory_list', 'main'),  # 旧配件入库列表
            'a': ('accessories_inventory_detail', 'main'),  # 旧配件入库详情
        }
        return self._get_data('attachment_old_warehouse', data, type_map, **kwargs)

    def attachment_sales_list_data(self, data='main', **kwargs):
        """配件管理|配件销售|销售列表"""
        type_map = {
            'main': ('sales_list', 'main'),  # 销售列表
            'a': ('sales_details', 'main'),  # 销售详情
            'b': ('sales_after_sales', 'main'),  # 销售售后
        }
        return self._get_data('attachment_sales_list', data, type_map, **kwargs)

    def attachment_purchase_list_data(self, data='main', **kwargs):
        """配件管理|配件采购|采购列表"""
        type_map = {
            'main': ('purchase_list', 'main'),  # 采购列表
            'a': ('procurement_after_sales', 'main'),  # 采购售后
        }
        return self._get_data('attachment_purchase_list', data, type_map, **kwargs)

    def attachment_warehouse_allocation_data(self, data='main', **kwargs):
        """配件管理|配件库存|库存调拨"""
        type_map = {
            'main': ('warehouse_allocation', 'main'),  # 库存调拨列表
            'a': ('inventory_transfer_details_list', 'main'),  # 库存调拨详情
            'b': ('revoke_the_transfer_details', 'main'),  # 撤销调拨详情
        }
        return self._get_data('attachment_warehouse_allocation', data, type_map, **kwargs)

    def attachment_receive_items_data(self, data='main', **kwargs):
        """配件管理|移交接收管理|接收物品"""
        type_map = {
            'main': ('handover_order_received_list', 'main'),  # 移交单接收列表
            'a': ('item_received_list', 'main'),  # 物品接收列表
        }
        return self._get_data('attachment_receive_items', data, type_map, **kwargs)

    def attachment_sorting_list_data(self, data='main', **kwargs):
        """配件管理|入库管理|分拣列表"""
        type_map = {
            'main': ('sorting_list', 'main'),  # 分拣列表
        }
        return self._get_data('attachment_sorting_list', data, type_map, **kwargs)

    def attachment_new_arrival_data(self, data='main', **kwargs):
        """配件管理|入库管理|新到货入库"""
        type_map = {
            'main': ('new_arrival_list', 'main'),  # 分拣列表
        }
        return self._get_data('attachment_new_arrival', data, type_map, **kwargs)

    def finance_account_list_data(self, data='main', **kwargs):
        """财务管理|资金账户|账户列表"""
        type_map = {
            'main': ('account_list', 'idle'),  # 账户列表
        }
        return self._get_data('finance_account_list', data, type_map, **kwargs)

    def finance_bill_review_data(self, data='main', **kwargs):
        """财务管理|业务记账|账单审核
        i：1应付 2应收
        j: 0待审核 1审核通过 2未通过
        """
        type_map = {
            'main': ('payable_bill', 'main'),  # 应付应收账单
            'a': ('payable_bill', 'vice'),  # 应付应收账单
        }
        return self._get_data('finance_bill_review', data, type_map, **kwargs)

    def finance_coping_with_each_other_data(self, data='main', **kwargs):
        """财务管理|业务记账|往来应付"""
        type_map = {
            'main': ('reconciliation_details_list', 'main'),  # 对账详情
            'a': ('machine_list', 'main'),  # 按机器结算 添加机器 机器列表
            'b': ('reconciliation_details_list_info', 'main'),  # 对账详情 单据详情
            'c': ('pay_list', 'main'),  # 往来应付列表
            'd': ('prepaid_slips_list', 'main'),  # 按供应商结算 列表
        }
        return self._get_data('finance_coping_with_each_other', data, type_map, **kwargs)

    def finance_exchanges_and_receivables_data(self, data='main', **kwargs):
        """财务管理|业务记账|往来应收"""
        type_map = {
            'main': ('reconciliation_details_list', 'main'),  # 对账详情
            'a': ('machine_list', 'main'),  # 按机器结算 添加机器 机器列表
            'b': ('reconciliation_details_list_info', 'main'),  # 对账详情 单据详情
            'c': ('receive_list', 'main'),  # 往来应收列表
            'd': ('customer_settlement_advance_receipts', 'main'),  # 按客户结算 列表
        }
        return self._get_data('finance_exchanges_and_receivables', data, type_map, **kwargs)

    def help_generate_order_data(self, data='main', **kwargs):
        """帮卖管理|帮卖上架列表
        i：物品状态 wsg待发货 wtg待收货 rg已收货 wr待质检 wbi待议价 wb待确认 ws待结算 wrg待退机 rig退机中 wsr待售出
        """
        type_map = {
            'main': ('help_list_of_orders', 'main'),  # 订单列表
            'a': ('initiate_a_list_of_helpers', 'main'),  # 发起帮卖列表
        }
        return self._get_data('help_generate_order', data, type_map, **kwargs)

    def help_sell_the_list_of_goods_data(self, data='main', **kwargs):
        """帮卖管理|帮卖来货列表"""
        type_map = {
            'main': ('help_incoming_goods_list', 'vice'),  # 订单列表
        }
        return self._get_data('help_sell_the_list_of_goods', data, type_map, **kwargs)

    def help_service_configuration_data(self, data='main', **kwargs):
        """帮卖管理|帮卖业务配置"""
        type_map = {
            'main': ('service_configuration', 'vice'),  # 帮卖业务配置列表
        }
        return self._get_data('help_service_configuration', data, type_map, **kwargs)

    def inventory_address_manage_data(self, data='main', **kwargs):
        """库存管理|出库管理|地址管理"""
        type_map = {
            'main': ('address_manage', 'idle'),  # 地址管理列表
        }
        return self._get_data('inventory_address_manage', data, type_map, **kwargs)

    def inventory_list_data(self, data='main', **kwargs):
        """库存管理|库存列表
        i：库存状态 2库存中 1待入库 3已出库
        j：物品状态 13待销售 3待分货 7维修中 5质检中 19销售预售中 14销售铺货中 16待送修 9已销售 15销售售后中 17送修中 11采购售后完成 12采购售后中 18仅出库 10待采购售后
        """
        type_map = {
            'main': ('inventory_list', 'main'),  # 库存列表
            'a': ('inventory_list', 'vice'),  # 库存列表
            'b': ('item_details_sell_info', 'main'),  # 物品详情 销售信息
            'c': ('operation_log', 'main'),  # 物品详情 操作日志
        }
        return self._get_data('inventory_list', data, type_map, **kwargs)

    def inventory_outbound_orders_list_data(self, data='main', **kwargs):
        """库存管理|出库管理|仅出库订单列表"""
        type_map = {
            'main': ('only_outbound_list', 'main'),  # 仅出库列表
            'a': ('only_outbound_order_details', 'main'),  # 仅出库订单详情
        }
        return self._get_data('inventory_outbound_orders_list', data, type_map, **kwargs)

    def inventory_receive_items_data(self, data='main', **kwargs):
        """库存管理|移交接收管理|接收物品
        i：物品状态 1待维修 2待收货 3待分货 4待质检 5质检中 6待维修 7维修中
        """
        type_map = {
            'main': ('stay_work_list', 'main'),  # 物品接收列表
            'a': ('receive_items', 'main'),  # 移交单接收列表
            'b': ('receive_items_detail', 'main'),  # 移交单接收详情
        }
        return self._get_data('inventory_receive_items', data, type_map, **kwargs)

    def inventory_receive_records_data(self, data='main', **kwargs):
        """库存管理|移交接收管理|移交记录
        """
        type_map = {
            'main': ('receive_log', 'main'),  # 移交记录列表
            'a': ('receive_log_detail', 'main'),  # 移交记录-物品详情
        }
        return self._get_data('inventory_transfer_records', data, type_map, **kwargs)

    def attachment_handover_records_data(self, data='main', **kwargs):
        """配件管理|移交接收管理|移交记录
        """
        type_map = {
            'main': ('handover_records_list', 'main'),  # 移交记录列表
            'a': ('handover_records_details', 'main'),  # 移交记录详情
        }
        return self._get_data('attachment_handover_records', data, type_map, **kwargs)

    def inventory_count_data(self, data='main', **kwargs):
        """库存管理|库存盘点"""
        type_map = {
            'main': ('inventory_count', 'main'),  # 库存盘点列表
        }
        return self._get_data('inventory_count', data, type_map, **kwargs)

    def inventory_warehouse_allocation_data(self, data='main', **kwargs):
        """库存管理|仓库调拨"""
        type_map = {
            'main': ('warehouse_transfers', 'main'),  # 仓库调拨列表
            'a': ('transfer_details', 'main'),  # 仓库调拨详情
        }
        return self._get_data('inventory_warehouse_allocation', data, type_map, **kwargs)

    def inventory_logistics_list_data(self, data='main', **kwargs):
        """库存管理|入库管理|物流列表"""
        type_map = {
            'main': ('material_flow_list', 'main'),  # 物流列表
            'a': ('material_flow_list_detail', 'main'),  # 物流列表详情
        }
        return self._get_data('inventory_logistics_list', data, type_map, **kwargs)

    def inventory_logistics_into_warehouse_data(self, data_type='main'):
        """库存管理|入库管理|物流签收入库"""
        type_map = {
            'main': ('logistics_list', 'main'),  # 物流列表
        }
        return self._get_data('inventory_logistics_into_warehouse', data_type, type_map)

    def message_release_list_data(self, data='main', **kwargs):
        """消息管理|消息发布列表"""
        type_map = {
            'main': ('release_list', 'main'),  # 消息发布列表
        }
        return self._get_data('message_release_list', data, type_map, **kwargs)

    def platform_product_review_data(self, data='main', **kwargs):
        """平台管理|同售管理|商品审核"""
        type_map = {
            'main': ('product_review_wait_audit', 'platform'),  # 待审核列表
        }
        return self._get_data('platform_product_review', data, type_map, **kwargs)

    def platform_message_release_list_data(self, data='main', **kwargs):
        """平台管理|消息管理|消息发布列表"""
        type_map = {
            'main': ('order_review', 'platform'),  # 回收商发布列表
        }
        return self._get_data('platform_message_release_list', data, type_map, **kwargs)

    def platform_order_review_data(self, data='main', **kwargs):
        """平台管理|订单管理|订单审核"""
        type_map = {
            'main': ('order_review', 'platform'),  # 订单审核列表
        }
        return self._get_data('platform_order_review', data, type_map, **kwargs)

    def platform_purchase_manage_data(self, data='main', **kwargs):
        """平台管理|商户管理"""
        type_map = {
            'main': ('manage_list_by_main', 'platform'),  # 商户管理列表
        }
        return self._get_data('platform_purchase_manage', data, type_map, **kwargs)

    def platform_items_to_be_specified_data(self, data='main', **kwargs):
        """平台管理|运营中心|待指定物品"""
        type_map = {
            'main': ('item_to_be_specified_list', 'super'),  # 待指定物品列表
        }
        return self._get_data('platform_items_to_be_specified', data, type_map, **kwargs)

    def platform_list_of_direct_auction_houses_data(self, data='main', **kwargs):
        """平台管理|卖场管理|直拍卖场列表
        i: 上架状态 1已上架 2待上架 3已下架
        """
        type_map = {
            'main': ('list_of_stores', 'super'),  # 直拍卖场列表
            'a': ('edit_details', 'super'),  # 编辑详情
            'b': ('view_session_details', 'super'),  # 查看场次详情 场次列表
            'c': ('product_list', 'super'),  # 查看场次详情 商品列表
        }
        return self._get_data('platform_list_of_direct_auction_houses', data, type_map, **kwargs)

    def platform_list_of_dark_auction_houses_data(self, data='main', **kwargs):
        """平台管理|卖场管理|暗拍卖场列表
        i: 上架状态 1已上架 2待上架 3已下架
        """
        type_map = {
            'main': ('list_of_dark_auction_houses', 'super'),  # 暗拍卖场列表
            'a': ('edit_details', 'super'),  # 编辑详情
            'b': ('view_session_details', 'super'),  # 查看场次详情 场次列表
            'c': ('product_list', 'super'),  # 查看场次详情 商品列表
        }
        return self._get_data('platform_list_of_dark_auction_houses', data, type_map, **kwargs)

    def platform_auction_product_manage_data(self, data='main', **kwargs):
        """平台管理|虚拟库存|上拍商品管理
        i：类型 1可上拍商品 2已上拍商品 3待定价物品     这里是从pc或者小程序的查询列表去拿最新数据的，比如我新增采购单，物品编号是唯一的
        那么这个用力就是用这个物品编号，另外的用例需要新造数据去拿数据，不然数据混淆，举个例子
        [a]：i：类型 1暗拍 2直拍
        """
        type_map = {
            'main': ('list_of_auctioned_products', 'super'),  # 上拍商品管理列表
            'a': ('select_the_list_of_sessions', 'super'),  # 选择场次列表
        }
        return self._get_data('platform_auction_product_manage', data, type_map, **kwargs)

    def platform_inspection_center_manage_data(self, data='main', **kwargs):
        """平台管理|运营中心|验机中心管理"""
        type_map = {
            'main': ('list_of_inspection_centers', 'super'),  # 验机中心管理列表
        }
        return self._get_data('platform_inspection_center_manage', data, type_map, **kwargs)

    def purchase_after_sales_list_data(self, data='main', **kwargs):
        """商品采购|采购售后管理|采购售后列表"""
        type_map = {
            'main': ('after_sales_orders_list', 'main'),  # 采购售后中列表
        }
        return self._get_data('purchase_after_sales_list', data, type_map, **kwargs)

    def purchase_post_sale_list_data(self, data='main', **kwargs):
        """商品采购|采购售后管理|待售后列表"""
        type_map = {
            'main': ('post_sale_list', 'main'),  # 待售后列表
        }
        return self._get_data('purchase_post_sale_list', data, type_map, **kwargs)

    def purchase_order_list_data(self, data='main', **kwargs):
        """商品采购|采购管理|采购订单列表"""
        type_map = {
            'main': ('order_list', 'main'),  # 采购订单列表
            'a': ('after_sales_detail', 'main'),  # 采购单详情
        }
        return self._get_data('purchase_order_list', data, type_map, **kwargs)

    def purchase_supplier_manage_data(self, data='main', **kwargs):
        """商品采购|供应商管理"""
        type_map = {
            'main': ('supplier_manage', 'idle'),  # 供应商管理列表
        }
        return self._get_data('purchase_supplier_manage', data, type_map, **kwargs)

    def purchase_work_order_data(self, data='main', **kwargs):
        """商品采购|采购管理|采购工单"""
        type_map = {
            'main': ('work_orders_list', 'main'),  # 采购工单列表
        }
        return self._get_data('purchase_work_order', data, type_map, **kwargs)

    def purchase_items_to_be_received_data(self, data='main', **kwargs):
        """商品采购|采购售后管理|待接收物品"""
        type_map = {
            'main': ('receive_items_list', 'main'),  # 待接收物品列表
        }
        return self._get_data('purchase_items_to_be_received', data, type_map, **kwargs)

    def purchase_unsend_order_list(self, data='main', **kwargs):
        """商品采购|采购售后管理|未发货订单列表"""
        type_map = {
            'main': ('un_shipped_order_list', 'main'),  # 未发货订单列表
        }
        return self._get_data('purchase_un_shipped_order_list', data, type_map, **kwargs)

    def purchase_arrival_list(self, data='main', **kwargs):
        """商品采购|采购售后管理|到货通知单列表"""
        type_map = {
            'main': ('arrival_notices_list', 'main'),  # 未发货订单列表
        }
        return self._get_data('purchase_arrival_notices', data, type_map, **kwargs)

    def quality_centre_item_data(self, data='main', **kwargs):
        """质检管理|质检中物品"""
        type_map = {
            'main': ('quality_centre_item', 'main'),  # 质检中物品列表
        }
        return self._get_data('quality_centre_item', data, type_map, **kwargs)

    def quality_content_template_data(self, data='main', **kwargs):
        """质检管理|质检内容模版"""
        type_map = {
            'main': ('content_template', 'idle'),  # 质检内容模版列表
        }
        return self._get_data('quality_content_template', data, type_map, **kwargs)

    def quality_wait_turn_over_data(self, data='main', **kwargs):
        """质检管理|待移交物品"""
        type_map = {
            'main': ('wait_turn_over_list', 'main'),  # 待移交物品列表
        }
        return self._get_data('quality_wait_turn_over', data, type_map, **kwargs)

    def quality_record_list_data(self, data='main', **kwargs):
        """质检管理|质检记录列表"""
        type_map = {
            'main': ('quality_record_list', 'main'),  # 质检记录列表
        }
        return self._get_data('quality_record_list', data, type_map, **kwargs)

    def repair_review_list_data(self, data='main', **kwargs):
        """维修管理|维修审核列表"""
        type_map = {
            'main': ('repair_audit_list', 'main'),  # 维修审核列表 待审核
        }
        return self._get_data('repair_review_list', data, type_map, **kwargs)

    def repair_project_list_data(self, data='main', **kwargs):
        """维修管理|维修项目列表
        i: 品类 1手机 2平板 3电脑 4手表
        """
        type_map = {
            'main': ('project_list', 'idle'),
            'a': ('project_list', 'main'),
        }
        return self._get_data('repair_project_list', data, type_map, **kwargs)

    def sell_sale_order_list_data(self, data='main', **kwargs):
        """商品销售|销售管理|已销售订单列表
        """
        type_map = {
            'main': ('sold_order_list', 'main'),  # 已销售物品列表
        }
        return self._get_data('sell_sold_order', data, type_map, **kwargs)

    def sell_sale_item_list_data(self, data='main', **kwargs):
        """商品销售|销售管理|已销售物品列表
        i：销售状态 2已销售 3已取消 1销售中
        j：销售类型 1销售 3铺货 5预售
        """
        type_map = {
            'main': ('sell_sale_item_list', 'main'),  # 已销售物品列表
        }
        return self._get_data('sell_sale_item_list', data, type_map, **kwargs)

    def sell_list_of_items_for_sale_data(self, data='main', **kwargs):
        """商品销售|销售管理|销售中物品列表
        i：销售状态 2已销售 3已取消 1销售中
        j：销售类型 1销售 3铺货 5预售
        """
        type_map = {
            'main': ('goods_list_for_sale', 'main'),  # 销售中物品列表
            'a': ('sales_goods_detail', 'main'),  # 销售中物品列表 销售物品详情
            'b': ('sales_goods_list_delisting_details', 'main'),  # 销售中物品列表 下架详情
        }
        return self._get_data('sell_list_of_items_for_sale', data, type_map, **kwargs)

    def sell_items_for_sale_data(self, data='main', **kwargs):
        """商品销售|销售管理|待销售物品"""
        type_map = {
            'main': ('items_for_sale', 'main'),  # 待销售物品列表
            'a': ('items_detail', 'main'),  # 待销售物品 详情
        }
        return self._get_data('sell_items_for_sale', data, type_map, **kwargs)

    def sell_after_sales_list_data(self, data='main', **kwargs):
        """商品销售|销售售后管理|销售售后列表"""
        type_map = {
            'main': ('sales_and_after_sales_are_completed', 'main'),  # 销售售后完成列表
            'a': ('in_the_after_sales_service', 'main'),  # 销售售后中列表
        }
        return self._get_data('sell_after_sales_list', data, type_map, **kwargs)

    def sell_goods_received_data(self, data='main', **kwargs):
        """商品销售|销售管理|待接收物品"""
        type_map = {
            'main': ('goods_received_list', 'main'),  # 待接收物品列表
        }
        return self._get_data('sell_goods_received', data, type_map, **kwargs)

    def selling_order_list_data(self, data='main', **kwargs):
        """商品销售|销售管理|销售中订单列表"""
        type_map = {
            'main': ('order_list_for_sale', 'main'),  # 销售中订单列表
        }
        return self._get_data('sell_order_list_for_sale', data, type_map, **kwargs)

    def sell_order_list_data(self, data='main', **kwargs):
        """商品销售|销售管理|已销售订单列表"""
        type_map = {
            'main': ('order_list_for_sale', 'main'),  # 销售中订单列表
        }
        return self._get_data('sell_order_list_for_sale', data, type_map, **kwargs)

    def send_been_sent_repair_data(self, data='main', **kwargs):
        """送修管理|已送修物品"""
        type_map = {
            'main': ('send_been_sent_repair', 'main'),  # 已送修物品列表
        }
        return self._get_data('send_been_sent_repair', data, type_map, **kwargs)

    def send_list_of_repair_orders_data(self, data='main', **kwargs):
        """送修管理|送修单列表"""
        type_map = {
            'main': ('send_list', 'main'),  # 送修单列表
        }
        return self._get_data('send_list_of_repair_orders', data, type_map, **kwargs)

    def sold_ninety_five_item_list_data(self, data='main', **kwargs):
        """同售管理|得物95分|95商品列表
        i：物品状态 3已发布 2发布失败
        """
        type_map = {
            'main': ('get_ninety_five_item_list', 'main'),  # 95商品列表
        }
        return self._get_data('sold_ninety_five_item_list', data, type_map, **kwargs)

    def system_work_order_setting_data(self, data='main', **kwargs):
        """系统管理|基础设置|工单配置"""
        type_map = {
            'main': ('list_of_defects', 'main'),  # 瑕疵项列表
            'a': ('business_sequence_list', 'main'),  # 业务工序列表
        }
        return self._get_data('system_work_order_setting', data, type_map, **kwargs)

    def mall_branch_manage_data(self, data='main', **kwargs):
        """商城管理||网点管理"""
        type_map = {
            'main': ('branch_manage_list', 'main'),  # 网点管理列表
        }
        return self._get_data('mall_branch_manage', data, type_map, **kwargs)

    def fulfillment_order_manage_data(self, data='main', **kwargs):
        """运营中心|订单管理
        i：订单状态 1待发货 2待取件 3待收货 4已收货 5已完成 6已取消 7已退货
        """
        type_map = {
            'main': ('order_list', 'main'),  # 订单列表
            'a': ('item_list', 'main'),  # 物品列表
        }
        return self._get_data('fulfillment_order_manage', data, type_map, **kwargs)

    def fulfillment_quality_manage_data(self, data='main', **kwargs):
        """运营中心|质检管理
        [d]i类型 1未上传 2已上传
        """
        type_map = {
            'main': ('quality_manage_list', 'main'),  # 待领取物品列表
            'a': ('items_in_quality_inspection_list', 'main'),  # 质检中物品列表
            'b': ('inspected_items_list', 'main'),  # 已质检物品列表
            'c': ('re_examine_the_application_list', 'main'),  # 重验申请列表
            'd': ('product_image_shooting_list', 'main'),  # 商品图拍摄
            'e': ('quality_inspection_template', 'main'),  # 质检模版
        }
        return self._get_data('fulfillment_quality_manage', data, type_map, **kwargs)

    def fulfillment_sign_into_the_library_data(self, data='main', **kwargs):
        """运营中心|收货入库"""
        type_map = {
            'main': ('search_tracking_numbers', 'main'),  # 搜索保卖订单号
            'a': ('search_tracking_express', 'main'),  # 搜索保卖物流单号
            'b': ('search_pj_tracking_numbers', 'main'),  # 搜索拍机订单号
        }
        return self._get_data('fulfillment_sign_into_the_library', data, type_map, **kwargs)

    def fulfillment_returns_manage_data(self, data='main', **kwargs):
        """运营中心|退货管理
         i：订单状态 1待退货 2待取货 3退货已出库 4已退货 5已取消
        """
        type_map = {
            'main': ('merchant_details_list', 'main'),  # 商户明细列表
            'a': ('item_detail_list', 'main'),  # 物品明细列表
            'b': ('batch_detail_list', 'main'),  # 批次明细列表
        }
        return self._get_data('fulfillment_returns_manage', data, type_map, **kwargs)

    def fulfillment_items_to_be_quoted_data(self, data='main', **kwargs):
        """运营中心|待报价物品"""
        type_map = {
            'main': ('items_to_be_quoted_list', 'main'),  # 待报价物品列表
        }
        return self._get_data('fulfillment_items_to_be_quoted', data, type_map, **kwargs)

    def fulfillment_items_are_out_of_storage_data(self, data='main', **kwargs):
        """运营中心|物品出库"""
        type_map = {
            'main': ('item_outbound_list', 'main'),  # 物品出库 销售出库
        }
        return self._get_data('fulfillment_items_are_out_of_storage', data, type_map, **kwargs)

    def fulfillment_sales_and_shipment_manage_data(self, data='main', **kwargs):
        """运营中心|销售发货管理"""
        type_map = {
            'main': ('sales_and_shipment_manage_list', 'main'),  # 待发货 按商户
            'a': ('sales_and_shipment_manage_item_list', 'main'),  # 待发货 按物品
            'b': ('snap_the_order_to_be_received_list', 'main'),  # 待收货 按物品
            'c': ('sales_and_fulfillment_management_list', 'main'),  # 待收货 按包裹
            'd': ('snap_machine_has_been_received_list', 'main'),  # 已收货 按包裹
            'e': ('snap_machine_has_been_received_item_list', 'main'),  # 已收货 按物品
        }
        return self._get_data('fulfillment_sales_and_shipment_manage', data, type_map, **kwargs)

    def guarantee_returns_manage_data(self, data='main', **kwargs):
        """保卖管理|退货管理
         i：订单状态 1待退货 2待取货 3退货已出库 4已退货 5已取消
        """
        type_map = {
            'main': ('item_detail_list', 'main'),  # 物品明细列表
            'a': ('batch_detail_list', 'main'),  # 批次明细列表
        }
        return self._get_data('guarantee_returns_manage', data, type_map, **kwargs)

    def guarantee_order_manage_data(self, data='main', **kwargs):
        """保卖管理|订单列表
        i：订单状态 1待发货 2待取件 3待收货 4已收货 5已完成 6已取消 7已退货
        """
        type_map = {
            'main': ('order_list', 'main'),  # 订单管理列表
            'a': ('item_list', 'main'),  # 物品列表
        }
        return self._get_data('guarantee_order_manage', data, type_map, **kwargs)

    def guarantee_goods_manage_data(self, data='main', **kwargs):
        """保卖管理|商品管理
        i：订单状态 1质检中 2待销售 3销售中
        """
        type_map = {
            'main': ('order_list', 'main'),  # 商品管理列表
        }
        return self._get_data('guarantee_goods_manage', data, type_map, **kwargs)

    def camera_after_sales_order_data(self, data='main', **kwargs):
        """拍机管理|售后管理|售后订单"""
        type_map = {
            'main': ('after_sales_list', 'camera'),  # 售后订单列表
        }
        return self._get_data('camera_after_sales_order', data, type_map, **kwargs)

    def fulfillment_camera_after_sales_order_data(self, data='main', **kwargs):
        """运营中心|壹准拍机|售后管理|售后订单
        i 订单状态
        [2]待申诉 [1]线上审核 [3]线上拒退 [4]申诉中 [5]补差成功 [6]可补差
        [7]待寄回 [8]超时取消 [9]主动取消 [10]待接收 [11]实物复检 [12]实物拒退 [13]退货成功
        """
        type_map = {
            'main': ('camera_after_sales_order_list', 'main'),  # 售后订单列表
        }
        return self._get_data('fulfillment_camera_after_sales_order', data, type_map, **kwargs)

    def platform_grievance_manage_data(self, data='main', **kwargs):
        """平台管理|壹准拍机|售后管理|申诉管理
        i订单类型 0待处理 1申诉成功 2申诉失败 3申诉取消
        """
        type_map = {
            'main': ('statement_list', 'super'),  # 申诉管理列表
        }
        return self._get_data('platform_grievance_manage', data, type_map, **kwargs)

    def fulfillment_after_sales_return_manage_data(self, data='main', **kwargs):
        """运营中心|壹准拍机|售后管理|售后退货管理
        i 类型  1待退货 2退货已出库
        """
        type_map = {
            'main': ('statement_list', 'super'),  # 售后退货列表
        }
        return self._get_data('fulfillment_after_sales_return_manage', data, type_map, **kwargs)

    def camera_list_of_airport_visits_data(self, data='main', **kwargs):
        """拍机管理|拍机场次列表"""
        type_map = {
            'main': ('list_of_airport_visits', 'camera'),  # 拍机场次列表
            'a': ('view_the_products_of_the_session', 'camera'),  # 查看场次商品
        }
        return self._get_data('camera_list_of_airport_visits', data, type_map, **kwargs)

    def auction_my_data(self, data='main', **kwargs):
        """保卖小程序-我的
         i：订单状态 1质检中 2待销售 3销售中 4已销售 5待平台确认 6报价确认 8退货中 9退货已出库 10已退货 7质检完成
         j：类型 1销售服务 2质检服务
        [b]
         i：订单状态 1待发货 2待取件 3待收货 4已收货
         j：类型 1销售服务 2质检服务
        """
        type_map = {
            'main': ('sell_order_list', 'main'),  # 销售物品 订单列表
            'a': ('sell_return_details', 'main'),  # 销售物品 退货中 退货详情
            'b': ('order_list', 'main'),  # 订单信息 订单列表
        }
        return self._get_data('auction_my', data, type_map, **kwargs)

    def auction_index_data(self, data='main', **kwargs):
        """保卖小程序-首页"""
        type_map = {
            'main': ('item_info_list', 'main'),  # 精确发货 物品信息列表
            'a': ('list_of_appearance_finishes', 'main'),  # 精确发货 外观成色列表
        }
        return self._get_data('auction_index', data, type_map, **kwargs)

    def bidding_camera_data(self, data='main', **kwargs):
        """拍机小程序-竞拍"""
        type_map = {
            'main': ('zhi_auction_list', 'camera'),  # 竞拍列表 直拍
            'a': ('an_auction_list', 'camera'),  # 竞拍列表 暗拍
        }
        return self._get_data('bidding_camera', data, type_map, **kwargs)

    def bidding_my_data(self, data='main', **kwargs):
        """拍机小程序-我的
        i：订单状态 1待支付 2待发货 3待收货 4已收货  5已售后 6已取消
        [a]i: 订单状态
        审核中：[1]线上审核 [11]实物复检 [10]待接收 [4]申诉中
        待处理：[7]待寄回 [6]可补差 [2]待申诉
        售后成功：[5]补差成功 [13]退货成功
        售后失败：[9]主动取消 [8]超时取消 [3]线上拒退 [12]实物拒退
        """
        type_map = {
            'main': ('racket_product_list', 'camera'),  # 商品列表
            'a': ('pat_machine_return_after_sales_list', 'camera'),  # 售后退货列表
        }
        return self._get_data('bidding_my', data, type_map, **kwargs)
