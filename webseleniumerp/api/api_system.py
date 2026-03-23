# coding: utf-8
import json
from common.base_api import BaseApi


class SystemMessageReceptionManageApi(BaseApi):
    """系统管理|消息接收配置"""

    def message_reception_manage_list(self, headers=None):
        """消息接收配置列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['message_reception_manage'], data=json.dumps(data),
                                       headers=headers)
        return self.get_response_data(response, 'data', [])


class SystemApiLogManageApi(BaseApi):
    """系统管理|接口缓存日志"""

    def api_log_manage_list(self, headers=None):
        """接口缓存日志列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['interface_log'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class SystemDeptManageApi(BaseApi):
    """系统管理|部门管理"""

    def dept_manage_list(self, headers=None):
        """部门管理列表"""
        headers = headers or self.headers['main']
        response = self.request_handle('get', self.urls['dept_manage'], headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res


class SystemBaseImportManageApi(BaseApi):
    """系统管理|导入模板管理"""

    def base_import_manage_list(self, headers=None):
        """导入模板列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['base_import_manage'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class SystemDictManageApi(BaseApi):
    """系统管理|字典管理"""

    def dict_manage_list(self, headers=None):
        """字典管理列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "params": {}}
        response = self.request_handle('post', self.urls['base_config_dict'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class SystemDispositionListApi(BaseApi):
    """系统管理|关键词配置"""

    def disposition_list(self, headers=None):
        """关键词配置"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['disposition_list'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class SystemExportListApi(BaseApi):
    """系统管理|导出列表"""

    def export_list(self, headers=None):
        """导出列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['export_list'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class SystemGeneralConfigApi(BaseApi):
    """系统管理|基础设置|常规配置"""

    def general_config_list(self, headers=None):
        """常规配置列表"""
        headers = headers or self.headers['main']
        response = self.request_handle('post', self.urls['general_config'], data=json.dumps({}), headers=headers)
        return self.get_response_data(response, 'rows', list)


class SystemInterfaceLogApi(BaseApi):
    """系统管理|接口缓存日志"""

    def interface_log(self, headers=None):
        """接口缓存日志"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['interface_log'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class SystemInterfaceManageApi(BaseApi):
    """系统管理|接口管理"""

    def interface_manage_list(self, headers=None):
        """接口管理列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['interface_manage'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class SystemInternationalConfigManageApi(BaseApi):
    """系统管理|国际化配置"""

    def international_config_manage_list(self, headers=None):
        """配置列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['international_config_manage'], data=json.dumps(data),
                                       headers=headers)
        return self.get_response_data(response, 'rows', list)


class SystemKeyConfigManageApi(BaseApi):
    """系统管理|关键字配置"""

    def key_config_manage_list(self, headers=None):
        """关键字配置列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "params": {}}
        response = self.request_handle('post', self.urls['disposition_list'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class SystemLogManageApi(BaseApi):
    """系统管理|日志管理|操作日志"""

    def operate_log_list(self, headers=None):
        """操作日志列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['log_operate_list'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)

    def login_log_list(self, headers=None):
        """登录日志列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['log_login_list'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class SystemMenuManageApi(BaseApi):
    """系统管理|菜单管理"""

    def menu_manage_list(self, headers=None):
        """菜单管理列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['menu_manage'], data=json.dumps(data), headers=headers)
        res = self.get_response_data(response, 'data', list)
        self.make_pkl_file(res)
        return res


class SystemNoticeManageApi(BaseApi):
    """系统管理|通知公告"""

    def notice_manage_list(self, headers=None):
        """通知公告列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['notice_manage'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class SystemParametersSettingManageApi(BaseApi):
    """系统管理|参数设置"""

    def parameters_setting_manage_list(self, headers=None):
        """参数设置列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), "params": {}}
        response = self.request_handle('post', self.urls['base_config_parameters'], data=json.dumps(data),
                                       headers=headers)
        return self.get_response_data(response, 'rows', list)


class SystemPostManageApi(BaseApi):
    """系统管理|岗位管理"""

    def post_manage_list(self, headers=None):
        """角色管理"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['post_manage'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class SystemPrintTemplateConfigApi(BaseApi):
    """系统管理|基础设置|打印标签模板配置"""

    def print_template_config_list(self, headers=None):
        """打印标签模板配置列表"""
        headers = headers or self.headers['main']
        data = {"params": {**self.get_page_params(), "name": "", "ismain": ""}}
        response = self.request_handle('post', self.urls['print_template_config'], data=json.dumps(data),
                                       headers=headers)
        return self.get_response_data(response, 'rows', list)


class SystemQualityBarcodeConfigApi(BaseApi):
    """系统管理|基础设置|质检条码打印配置"""

    def quality_barcode_config(self, headers=None):
        """质检条码打印配置"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['quality_barcode_config'], data=json.dumps(data),
                                       headers=headers)
        return self.get_response_data(response, 'rows', list)


class SystemQualityPrintConfigApi(BaseApi):
    """系统管理|基础设置|质检模板打印配置"""

    def quality_print_config(self, headers=None):
        """质检模板打印配置"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['quality_print_config'], data=json.dumps(data),
                                       headers=headers)
        return self.get_response_data(response, 'rows', list)


class SystemQueryManageApi(BaseApi):
    """系统管理|壹查查管理"""

    def query_record_list(self, headers=None):
        """查询记录列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['imei_check_list'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class SystemRoleManageApi(BaseApi):
    """系统管理|角色管理"""

    def role_manage_list(self, headers=None):
        """角色管理"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['role_manage'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class SystemThirdPartyAccountsManageApi(BaseApi):
    """系统管理|第三方账号管理"""

    def third_party_accounts_manage_list(self, headers=None):
        """采购列表"""
        headers = headers or self.headers['main']
        data = {'classId': "1", **self.get_page_params()}
        response = self.request_handle('post', self.urls['third_party_purchase_list'], data=json.dumps(data),
                                       headers=headers)
        return self.get_response_data(response, 'rows', list)

    def system_sales_list(self, headers=None):
        """销售列表"""
        headers = headers or self.headers['main']
        data = {'classId': "2", **self.get_page_params()}
        response = self.request_handle('post', self.urls['third_party_sales_list'], data=json.dumps(data),
                                       headers=headers)
        return self.get_response_data(response, 'rows', list)

    # 获取采购账号id
    def get_id(self):
        return self._get_field_copy_value('third_party_accounts_manage_list', 'main', 'id')


class SystemUserManageApi(BaseApi):
    """系统管理|用户管理"""

    def user_manage_list(self, headers=None):
        """用户管理"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params(), 'params': {}}
        response = self.request_handle('post', self.urls['user_manage'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)

    # 获取用户id
    def get_user_id(self):
        return self._get_field_copy_value('user_manage_list', 'main', 'userId')

    # 获取用户id
    def get_user_id_vice(self):
        return self._get_field_copy_value('user_manage_list', 'vice', 'userId')

    # 获取第二条用户id
    def get_user_id_two(self):
        return self._get_field_copy_value('user_manage_list', 'main', 'userId', index=1)

    # 获取用户名称
    def get_user_name(self):
        return self._get_field_copy_value('user_manage_list', 'main', 'userName')

    # 获取用户id
    def get_user_id_idle(self):
        return self._get_field_copy_value('user_manage_list', 'idle', 'userId')


class SystemWarehouseManageApi(BaseApi):
    """系统管理|仓库管理"""

    def warehouse_manage_list(self, headers=None):
        """仓库管理"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['warehouse_manage'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)

    # 获取深圳配件仓id
    def get_id(self):
        return self._get_field_copy_value('warehouse_manage_list', 'main', 'id')

    # 获取广州物品仓id
    def get_id_two(self):
        return self._get_field_copy_value('warehouse_manage_list', 'main', 'id', index=1)

    # 获取默认物品仓id
    def get_id_three(self):
        return self._get_field_copy_value('warehouse_manage_list', 'main', 'id', index=2)

    # 获取默认配件仓id
    def get_id_four(self):
        return self._get_field_copy_value('warehouse_manage_list', 'main', 'id', index=3)

    # 获取仓库id
    def get_id_five(self):
        return self._get_field_copy_value('warehouse_manage_list', 'vice', 'id')


class SystemWorkOrderSettingApi(BaseApi):
    """系统管理|基础设置|工单配置"""

    def list_of_defects(self, headers=None):
        """瑕疵项列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['problem_list'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)

    def business_sequence_list(self, headers=None):
        """业务工序列表"""
        headers = headers or self.headers['main']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['work_list'], data=json.dumps(data), headers=headers)
        return self.get_response_data(response, 'rows', list)


class SystemPriceCalculationLogApi(BaseApi):
    """系统管理|日志管理|价格计算日志"""

    def list_of_defects(self, headers=None):
        """价格计算日志列表"""
        headers = headers or self.headers['super']
        data = {**self.get_page_params()}
        response = self.request_handle('post', self.urls['price_calculation_log'], data=json.dumps(data),
                                       headers=headers)
        return self.get_response_data(response, 'rows', list)

    # 获取价格计算日志id
    def get_id(self):
        return self._get_field_copy_value('list_of_defects', 'super', 'id')

    # 获取价格模版id
    def get_template_id(self):
        return self._get_field_copy_value('price_breakdown', 'super', 'template_id')

    # 获取价格计算id
    def get_price_id(self):
        return self._get_field_copy_value('price_breakdown', 'super', 'price_id')


class SystemPermissionListApi(BaseApi):
    """系统管理|权限列表"""

    def permission_list(self, headers=None):
        """权限列表"""
        headers = headers or self.headers['main']
        response = self.request_handle('get', self.urls['user_center'], headers=headers)
        data =  self.get_response_data(response, 'permissions', list)
        # 将请求结果保存到当前路径得permission.json文件中
        filename = 'permission_main.json'
        self.save_json_file(data, filename)
        return data


if __name__ == '__main__':
    api = SystemMenuManageApi()
    result = api.menu_manage_list()
    # print(json.dumps(result, indent=4, ensure_ascii=False))
